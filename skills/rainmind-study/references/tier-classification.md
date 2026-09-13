# 分级规则（Phase 2）

## JCR Q1/Q2

- **优先**：Web of Science JCR quartile（有权限时）。Q1/Q2 = JCR 分区 Q1 或 Q2。
- **回退**（无 WoS 权限）：
  - Scopus CiteScore percentile ≥ 50%（约 Q1/Q2 等效），或
  - SCImago SJR quartile Q1/Q2。
  - OpenAlex 的 `primary_location.source` 可辅助获取来源信息，但不直接给 JCR quartile，需交叉到 Scopus/SCImago 确认。
- **记录**：每条文献在清单里写明 `分区: Q1/Q2`、`分级来源: WoS-JCR / CiteScore / SJR` 与 `分级年份`。

## Nature Index

- 「Nature 优秀」= 官方 Nature Index 期刊清单（nature.com/nature-index 年度 list）。
- 用最新可得年度清单标记 `Nature Index: true`，并记录 `nature_index_year`。
- 不在清单内的 Science/PNAS 等顶刊默认不纳入“Nature 优秀”标记，除非用户明确要求扩展顶刊清单。

## 保留规则

- 默认只保留 JCR Q1/Q2 或 Nature Index 文章。
- 例外（经典奠基文献、极高被引、用户指定）：需用户确认后纳入，并在清单里标注“例外及理由”。

## 判定注意

- 综述文章也要标分区；可用作脉络梳理，但研究缺口必须以最新原始研究为主。
- 预印本不分级，只作“最新动向”参考。