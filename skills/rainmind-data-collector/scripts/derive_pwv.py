#!/usr/bin/env python3
"""Derive ZWD and PWV from GNSS ZTD using surface pressure (ZHD) and Tm."""
import argparse, csv, math

def zhd_saastamoinen(P_hPa, lat_deg, h_m):
    lat = math.radians(lat_deg)
    return (0.0022768 * P_hPa) / (1 - 0.00266 * math.cos(2 * lat) - 0.00000028 * h_m)

def pwv_from_tm(zwd_m, Tm_K):
    k2p = 16.48
    k3 = 3.776e5
    rho = 1000.0
    Rv = 461.5
    Pi = 1e6 / (rho * Rv * (k3 / Tm_K + k2p))
    return Pi * zwd_m

def main():
    ap = argparse.ArgumentParser(description='ZTD -> ZWD -> PWV')
    ap.add_argument('--ztd', required=True, help='CSV: station,datetime,ZTD_m,pressure_hPa,Tm_K')
    ap.add_argument('--lat', type=float, required=True)
    ap.add_argument('--h', type=float, required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()

    with open(args.ztd, encoding='utf-8', newline='') as f, open(args.out, 'w', encoding='utf-8', newline='') as o:
        r = csv.DictReader(f)
        w = csv.writer(o)
        w.writerow(['station', 'datetime', 'ZTD_m', 'ZHD_m', 'ZWD_m', 'PWV_mm'])
        for row in r:
            ztd = float(row['ZTD_m'])
            P = float(row['pressure_hPa'])
            Tm = float(row['Tm_K'])
            zhd = zhd_saastamoinen(P, args.lat, args.h)
            zwd = ztd - zhd
            pwv = pwv_from_tm(zwd, Tm)
            w.writerow([row['station'], row['datetime'], ztd, round(zhd, 6), round(zwd, 6), round(pwv, 3)])
    print(f'[ok] {args.out}')

if __name__ == '__main__':
    main()