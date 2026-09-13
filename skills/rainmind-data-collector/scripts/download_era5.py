#!/usr/bin/env python3
"""Download ERA5 via CDS API from a data-request YAML (era5 section)."""
import argparse, pathlib, sys, yaml

def check_credentials():
    rc = pathlib.Path.home() / '.cdsapirc'
    if not rc.exists():
        sys.stderr.write('ERROR: 未找到 ~/.cdsapirc。请先注册 Copernicus CDS 并按 references/credentials.md 创建该文件。\n')
        sys.exit(2)

def main():
    ap = argparse.ArgumentParser(description='Download ERA5 via CDS API')
    ap.add_argument('--request', required=True, help='data-request YAML with era5 section')
    ap.add_argument('--output-dir', default='.', help='output directory')
    ap.add_argument('--dry-run', action='store_true', help='print requests only')
    args = ap.parse_args()

    check_credentials()
    import cdsapi
    req = yaml.safe_load(open(args.request, encoding='utf-8'))
    era5 = req['era5']
    out = pathlib.Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    for ds in era5['requests']:
        name = ds.pop('name')
        target = out / f'{name}.nc'
        if args.dry_run:
            print(f'[dry-run] {name}: {ds} -> {target}')
            continue
        c = cdsapi.Client()
        c.retrieve(era5['dataset'], ds, str(target))
        print(f'[ok] {target}')

if __name__ == '__main__':
    main()