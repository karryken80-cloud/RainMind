---
name: rainmind-data-collector
description: RainMind 流水线阶段 2：按已确认的研究计划采集 ERA5 再分析、GNSS ZTD 产品与 CMIP6 模式数据到项目 data 目录，处理数据并写 data-manifest.md 记录来源、许可与时间覆盖。用于“采集数据、下载 ERA5/GNSS/CMIP6、建立下载凭据、准备研究数据”等请求；只采集与记录，不做分析。
---

# RainMind Data Collector — 数据采集（阶段 2）

读取 `rainmind-study` 产出的 `manifest.md` 与 `研究计划.md`，把「数据与资料」章节转成采集清单，经用户确认后下载并处理数据，记录来源。只做采集与记录，不改研究计划、不做分析。

## 工作流

1. **读计划**：提取数据需求，生成采集清单（源/变量/时段/区域/体积），逐项请用户确认。
2. **逐源提示如何下载**：按 [sources.md](references/sources.md) 给出账号、URL、参数与下载代码。
3. **凭据预检（先问再查）**：ERA5/CDS 先问用户是否已有/现在创建 CDS 账号，再查 `~/.cdsapirc`；CMIP6 需 ESGF OpenID；GNSS 公开或复用 CDS。缺失即停下并指导创建，不擅自访问。
4. **下载**：调用 `scripts/` 中脚本（区域子集优先、可续传），把下载代码保留在项目里以便复现。
5. **数据处理**：按 [processing.md](references/processing.md) 做裁剪、单位、时间对齐、GNSS `ZTD→ZWD→PWV`、CMIP6 拼接/重网格。
6. **校验与记录**：写 `data-manifest.md`（字段见 [data-manifest-schema.md](references/data-manifest-schema.md)），回报完成与未完成项。

## 停止规则

- 凭据缺失且用户未创建 → 停，不绕过授权。
- 体积/范围与计划不符 → 停，与用户确认。
- 某源失败 → 记录失败项并回报，不静默跳过。