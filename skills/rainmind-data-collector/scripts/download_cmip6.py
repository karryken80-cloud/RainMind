#!/usr/bin/env python3
"""Query and download CMIP6 files from an ESGF node via search API + wget."""
import argparse, json, subprocess, sys, urllib.parse, urllib.request

NODE = 'https://esgf-node.llnl.gov/esg-search/search'

def search(query):
    params = urllib.parse.urlencode({**query, 'format': 'application/solr+json', 'limit': '10000', 'type': 'File'})
    with urllib.request.urlopen(f'{NODE}?{params}', timeout=60) as r:
        return json.load(r)['response']['docs']

def main():
    ap = argparse.ArgumentParser(description='Download CMIP6 files')
    ap.add_argument('--experiment', required=True, help='e.g. historical, ssp245, hist-nat')
    ap.add_argument('--variable', required=True, help='e.g. pr, tas, psl')
    ap.add_argument('--table', default='day', help='e.g. day, Amon')
    ap.add_argument('--source-id', default=None, help='optional model id')
    ap.add_argument('--grid-label', default='gn')
    ap.add_argument('--output-dir', default='.')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    q = dict(project='CMIP6', experiment_id=args.experiment, variable_id=args.variable,
             table_id=args.table, grid_label=args.grid_label)
    if args.source_id:
        q['source_id'] = args.source_id

    docs = search(q)
    if not docs:
        print('no files found')
        sys.exit(1)
    for d in docs:
        url = d['url'].split('|')[0]
        fname = d['title']
        target = f'{args.output_dir}/{fname}'
        if args.dry_run:
            print(f'[dry-run] {url} -> {target}')
            continue
        subprocess.run(['wget', '--continue', '-O', target, url])
        print(f'[ok] {target}')

if __name__ == '__main__':
    main()