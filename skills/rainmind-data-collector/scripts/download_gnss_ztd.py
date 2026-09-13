#!/usr/bin/env python3
"""Download GNSS ZTD products from an open archive via a URL template."""
import argparse, pathlib, urllib.request

def main():
    ap = argparse.ArgumentParser(description='Download GNSS ZTD products')
    ap.add_argument('--station', required=True, action='append', help='4-char station id, repeatable')
    ap.add_argument('--year', required=True, type=int)
    ap.add_argument('--template', required=True, help='URL template with {station} {year} {doy}')
    ap.add_argument('--start-doy', type=int, default=1)
    ap.add_argument('--end-doy', type=int, default=365)
    ap.add_argument('--output-dir', default='.')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    out = pathlib.Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    for sta in args.station:
        for doy in range(args.start_doy, args.end_doy + 1):
            url = args.template.format(station=sta.lower(), year=args.year, doy=doy)
            target = out / f'{sta}_{args.year}_{doy:03d}.ztd'
            if args.dry_run:
                print(f'[dry-run] {url} -> {target}')
                continue
            try:
                urllib.request.urlretrieve(url, target)
                print(f'[ok] {target}')
            except Exception as e:
                print(f'[skip] {url}: {e}')

if __name__ == '__main__':
    main()