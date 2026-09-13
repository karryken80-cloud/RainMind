#!/usr/bin/env python3
"""Download GNSS water vapour/ZTD from Copernicus CDS (insitu-observations-gnss)."""
import argparse, pathlib, sys, yaml

def main():
    ap = argparse.ArgumentParser(description='Download GNSS in-situ data via CDS API')
    ap.add_argument('--request', required=True, help='YAML with gnss_cds section')
    ap.add_argument('--output-dir', default='.')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    rc = pathlib.Path.home() / '.cdsapirc'
    if not rc.exists():
        sys.stderr.write('ERROR: 未找到 ~/.cdsapirc，请先配置 CDS 账号。\n')
        sys.exit(2)

    import cdsapi
    req = yaml.safe_load(open(args.request, encoding='utf-8'))
    gnss = req['gnss_cds']
    out = pathlib.Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    for item in gnss['requests']:
        name = item.pop('name')
        target = out / f'{name}.zip'
        if args.dry_run:
            print(f'[dry-run] {name}: {item} -> {target}')
            continue
        c = cdsapi.Client()
        c.retrieve(gnss['dataset'], item, str(target))
        print(f'[ok] {target}')

if __name__ == '__main__':
    main()