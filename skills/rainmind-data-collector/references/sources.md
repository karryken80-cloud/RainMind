# 数据源与下载指南（每个源：如何下载）

## ERA5（再分析）
- 账号：Copernicus CDS，配置 ~/.cdsapirc（见 credentials.md）。
- 下载脚本：scripts/download_era5.py --request data-request.yaml --output-dir data/era5。
- 常用变量：total_precipitation、surface_pressure、2m_temperature、2m_dewpoint_temperature、10m_u_component_of_wind、10m_v_component_of_wind、pressure-level specific_humidity。
- 区域子集：area: [N, W, S, E]（北、西、南、东），务必子集以控制体积。
- 许可：Copernicus Licence。

## GNSS ZTD/ZWD/PWV（公开，三选一）
1. CDS in-situ（推荐，复用 CDS 账号）：数据集 insitu-observations-gnss（E-GVAP，1996–present）。
   - 打开数据集页 → Download data 选站点/变量/年份 → Show API request 复制参数。
   - 下载脚本：scripts/download_gnss_cds.py --request data-request.yaml --output-dir data/gnss。
2. NGL 单站（公开免登录）：https://geodesy.unr.edu/NGLStationPages/stations/<STA>.sta → 5 Minute Troposphere Solutions → 下载 trop 文件。
3. CDDIS IGS 对流层 ZPD：目录 https://cddis.nasa.gov/archive/gps/products/troposphere/zpd/{year}/{doy}/，用 scripts/download_gnss_ztd.py（先打开目录核对文件名）。
- 派生 ZWD/PWV：见 processing.md；脚本 scripts/derive_pwv.py。

## CMIP6（模式）
- 账号：ESGF OpenID（部分数据节点需登录）。
- 下载脚本：scripts/download_cmip6.py --experiment ... --variable ... --table ...。
- 常用试验：historical、ssp245、DAMIP 的 hist-nat / hist-GHG / hist-aer。
- 常用变量：pr、tas、psl、hus；table：day / Amon。
- 许可：CMIP6 Terms of Use，引用标注模型与机构。