# 数据处理配方

## 通用
- 统一时间轴（UTC）、单位，裁剪到研究区。
- 保留原始文件与处理脚本，保证可复现。

## ERA5
- total_precipitation 单位是 m：小时→日/时段累计后 ×1000 得 mm。
- 用 surface_pressure 求 GNSS 的 ZHD；用 pressure-level 温度/比湿求 Tm。

## GNSS：ZTD → ZWD → PWV
- ZHD（Saastamoinen）：ZHD = 0.0022768·P / (1 − 0.00266·cos2φ − 2.8e-7·h)
- ZWD = ZTD − ZHD
- PWV = Π·ZWD，Π = 1e6 / (ρ·Rv·(k3/Tm + k2′))；Tm 用 ERA5 或 Bevis 经验式 Tm≈70.2+0.72·Ts。
- 脚本：scripts/derive_pwv.py --ztd input.csv --lat 39.6 --h 87 --out output.csv
- QC：剔除 ZWD<0 或跳变点；重采样到 1 h 与降雨标签对齐。

## CMIP6
- 多模式统一重网格到 ERA5 网格（xesmf bilinear 或 CDO remapbil）。
- 事件归因：historical(1850–2014) + ssp245(2015–事件年) 拼接为“当前气候”；hist-nat 为反事实。
- 变量命名与单位按 CF 约定；可选分位数映射订正到 ERA5。