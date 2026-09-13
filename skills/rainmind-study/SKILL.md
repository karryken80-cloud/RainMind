---
name: rainmind-study
description: 输入大气科学研究问题，调研已发表论文（JCR Q1/Q2 与 Nature Index 优秀文章），并用“分阶段询问”的方式与用户共同制定研究计划，产出 文献调研.md、研究计划.md 与 manifest.md。用于大气科学选题、文献调研、研究计划制定等请求；明确的下游写作、执行或审稿请求由后续阶段子技能处理。
---

# RainMind Study — 大气科学文献调研与研究计划（阶段 1）

把一个大气科学问题/方向变成「可追溯的文献调研 + 经你确认的研究计划」。本技能是 RainMind 流水线的阶段 1，只负责调研与计划，不替你写作或执行下游阶段。

## 核心原则

1. **先问后查** — 检索前先问清目标与约束，避免方向跑偏。
2. **先证据后计划** — 研究计划的每个判断都要能落到文献调研里的具体条目。
3. **逐项确认再定稿** — 计划关键决策必须以“建议 + 请确认或修改”的方式问用户，确认后才写进 研究计划.md。
4. **分级可审计** — 每条文献的 JCR Q1/Q2 与 Nature Index 判定都要记录来源与年份。
5. **该停就停** — 检索覆盖不足、方向冲突、数据不可得是停下来和用户确认的理由，不是硬凑计划。

## 工作流（5 阶段）

### Phase 0 输入与澄清（询问）
接收具体问题或模糊方向；模糊方向先收敛为一个可证伪的科学问题。按 [interview-protocol.md](references/interview-protocol.md) 的 Phase 0 清单逐项问清：研究问题/方向、用途（期刊/基金/学位）、目标层级与候选期刊、时间预算、已有数据/算力/团队专长、可接受创新幅度。得到答案后再进入检索。

### Phase 1 多源检索
按 [search-strategy.md](references/search-strategy.md) 生成中英文检索式并聚合检索，去重后用标题+摘要初筛。覆盖不足时先向用户确认是否扩检索词/放宽范围，不要静默换方向。

### Phase 2 分级与精读
按 [tier-classification.md](references/tier-classification.md) 给每条候选文献标注 JCR Q1/Q2 与 Nature Index，并记录分级来源与年份。只保留 Q1/Q2 或 Nature Index；确需纳入的经典/高被引例外须经用户确认。对关键论文提取目标/方法/数据/主要结论/局限，形成主题聚类与研究缺口。

### Phase 3 询问式制定研究计划
把「科学问题、创新点、方法路线、数据方案、可行性/风险、时间线」逐项按 [interview-protocol.md](references/interview-protocol.md) 的 Phase 3 话术，以“建议 + 请确认或修改”形式问用户，逐项确认后才进入产出。

### Phase 4 产出
按 [artifact-schema.md](references/artifact-schema.md) 写 文献调研.md、研究计划.md、manifest.md 到 `studies/<slug>/`（默认 `<cwd>/studies/<slug>/`；cwd 不明确时先问输出目录）。`<slug>` 由研究问题生成 URL 安全短名。

## 单事件归因专用手册

当研究问题是“某场具体极端降雨/洪水事件的归因”时，加载 [single-event-attribution.md](references/single-event-attribution.md)：给出 6 步执行流程、研究特色框架与一个中国梅雨工作示例，Phase 2/3 直接按其中 checklist 执行。

## 投稿要求

目标期刊遵循用户“高 IF、非水刊”偏好：默认主投 GPS Solutions，备选 IEEE TGRS / AMT，可冲击 npj Climate and Atmospheric Science；排除 Remote Sensing (MDPI) 等易被诟病期刊。详见 [journal-policy.md](references/journal-policy.md)。

## 停止与确认规则

- Phase 0 未得到完整答案前不检索。
- Phase 3 任一关键决策未确认前不落盘 研究计划.md。
- 检索无法达到可支撑计划的覆盖度时，明确告诉用户缺什么、缺在哪，而不是补造结论。