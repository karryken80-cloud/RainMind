# 产物契约（Phase 4）

默认目录：`<cwd>/studies/<slug>/`，`<slug>` 为 URL 安全短名（小写、连字符）。

## manifest.md（YAML frontmatter）

```yaml
---
title: <研究课题名>
slug: <url-safe slug>
created: <ISO 日期>
status: draft | confirmed
tier_standard: JCR
tier_source: WoS-JCR | CiteScore | SJR
nature_index_year: <年份>
files:
  survey: 文献调研.md
  plan: 研究计划.md
key_decisions:
  - <已确认的关键决策 1>
---
```

- `status`：Phase 3 全部确认前为 `draft`；全部确认后为 `confirmed`。
- `key_decisions`：记录 Phase 3 六项决策的最终结论，供后续流水线阶段直接消费。

## 文献调研.md 必需章节

1. **研究问题与检索式**：最终科学问题、各源检索式、检索日期、命中/去重/初筛数。
2. **文献清单表**：每行含 标题 | 作者 | 年份 | 期刊 | DOI | JCR分区 | Nature Index | 相关性(高/中/低) | 核心贡献 | 方法 | 局限；带稳定编号 `[n]`。
3. **主题脉络**：按主题聚类，说明研究如何演进、主要争论点。
4. **研究缺口**：明确的 gap 列表，每条 gap 指向文献依据 `[n]`。

## 研究计划.md 必需章节

1. 背景与意义
2. 科学问题（一句话 + 可验证假设）
3. 创新点（与已有工作的差异，标注文献 `[n]`）
4. 数据与资料（来源、可得性、替代方案）
5. 方法与技术路线（主方法 + 备选 + 理由）
6. 可行性与风险（关键风险 + 缓解）
7. 时间线与里程碑
8. 参考文献（复用调研清单编号 `[n]`）