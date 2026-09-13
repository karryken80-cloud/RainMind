#!/usr/bin/env python3
"""Run one experiment script, capture stdout/stderr, write a log, return exit code."""
import argparse, pathlib, subprocess, sys, time

def main():
    ap = argparse.ArgumentParser(description='Run an experiment .py and log its output')
    ap.add_argument('--script', required=True, help='python script to run')
    ap.add_argument('--log-dir', default='results/logs')
    args = ap.parse_args()

    script = pathlib.Path(args.script).resolve()
    logdir = pathlib.Path(args.log_dir)
    logdir.mkdir(parents=True, exist_ok=True)
    log = logdir / (script.stem + '.log')
    t0 = time.time()
    with open(log, 'w', encoding='utf-8') as f:
        f.write(f'[run] {script}\n[start] {time.strftime("%Y-%m-%d %H:%M:%S")}\n\n')
        proc = subprocess.run([sys.executable, str(script)], stdout=f, stderr=subprocess.STDOUT)
        f.write(f'\n[exit] {proc.returncode}\n[elapsed] {time.time()-t0:.1f}s\n')
    print(f'[{"ok" if proc.returncode == 0 else "fail"}] {script} -> {log}')
    sys.exit(proc.returncode)

if __name__ == '__main__':
    main()