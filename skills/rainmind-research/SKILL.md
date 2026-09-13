---
name: rainmind-research
description: 大气科学 RainMind 研究流水线的双模式总路由。默认按阶段分段执行；用户明确要求“自动完成整个流水线、端到端、一条龙、自动控制”时，可编排 study→data collector→worker→writer→teacher→writer revision 全流程。用于“用 RainMind 做大气科学研究”“开始一项大气科学研究”“自动跑完整流水线”“一步一步完成阶段”等请求；具体阶段由对应子技能负责。
---

# RainMind Research — 大气科学研究流水线（总路由）

本技能是 RainMind 流水线的总控制层，不亲自完成检索、采集、实验、写作或审稿，只负责模式选择、阶段路由、状态交接、确认门和循环终止。

## 两种运行模式

### A. 分段模式（默认）

触发语：

- “一步一步做”
- “分段执行”
- “先做阶段 1”
- “只完成数据采集”
- “每个阶段完成后停下”
- 用户只点名一个阶段，且没有要求自动继续

行为：

1. 只启动用户点名或当前应在的阶段。
2. 交给该阶段子技能完成全部工作。
3. 阶段完成后更新 `studies/<slug>/pipeline-manifest.md`，汇报完成内容、证据和未决项。
4. 停止，不自动进入下一阶段。
5. 给出下一阶段建议，但等待用户明确批准。

### B. 自动端到端模式

触发语：

- “自动完成整个流水线”
- “端到端完成”
- “一条龙做完”
- “自动控制实行整个流水线”
- “按阶段自动继续，不要每步都问我”
- “从选题一直做到论文修订”

行为：

1. 建立或读取 `studies/<slug>/pipeline-manifest.md`，记录当前模式、阶段状态、产物和 blocker。
2. 按顺序执行：
   `rainmind-study → rainmind-data-collector → rainmind-worker → rainmind-writer → rainmind-teacher → rainmind-writer revision`
3. 某阶段产物完整、manifest 状态为 confirmed、无 blocker 时，自动进入下一阶段。
4. 自动模式允许在阶段内自行执行脚本、下载公开数据、运行实验、生成图表和 Word 稿件，但不得绕过任何凭据、费用、破坏性操作或研究范围确认门。
5. 自动模式必须保留阶段状态和中间产物，便于用户在任何阶段审计或接管。
6. 出现硬停止门或 blocker 时，保存现场并停下询问用户；不得跳过、伪造或静默换方案。

## 阶段路由

| 阶段 | owner | 主要产物 |
|---|---|---|
| 1 | `$rainmind-study` | `文献调研.md`、`研究计划.md`、`manifest.md`、`pipeline-manifest.md` 初版 |
| 2 | `$rainmind-data-collector` | `data/`、`data-manifest.md`、下载与处理脚本 |
| 3 | `$rainmind-worker` | `code/experiments.yaml`、实验脚本、`results/`、`experiment-report.md` |
| 4 | `$rainmind-writer` | `manuscript/<期刊>_初稿.docx`、`outline.md`、`figure-map.md` |
| 5 | `$rainmind-teacher` | `review/review-report.md`、`review/revision-checklist.md` |
| 4R | `$rainmind-writer` revision loop | `manuscript/<期刊>_修订稿.docx`、`revision-plan.md`、`revision-response.md` |

审稿-修订循环最多执行 3 轮；若连续两轮仍有 blocking scientific issue，停止并请用户决定扩大实验还是降低结论强度。

## pipeline-manifest.md

位置：`studies/<slug>/pipeline-manifest.md`。

建议字段：

```yaml
mode: stepwise | autonomous
status: running | blocked | completed
current_stage: study | data | worker | writer | teacher | revision
completed_stages: []
next_stage: data
last_updated: <ISO date>
artifacts: {}
blocking: []
user_gates: []
```

每次进入下一阶段前必须先更新该文件。

## 必须停下确认的硬门

以下情况无论 stepwise 还是 autonomous 都必须停下：

1. `$rainmind-study` 的科学问题或 Phase 3 关键决策尚未确认。
2. `$rainmind-data-collector` 需要账号、许可证、私密数据、付费服务或下载体积/范围与计划不符。
3. `$rainmind-worker` 的实验清单未被用户确认，或新问题需要偏离已确认实验方案。
4. `$rainmind-writer` 缺少目标期刊或目标期刊要求无法确认。
5. `$rainmind-teacher` 要求新增实验、替换外部数据或重训模型，但该动作超出已确认范围。
6. 任何下载、实验或修订涉及破坏性文件操作、外部付费、生产系统或隐私数据。
7. 当前阶段无法达到最低完成标准，或必须改变核心科学问题。

## 自动模式的阶段衔接规则

1. **Study 完成**：只有当科学问题与 Phase 3 六项决策已确认，才自动进入 data。
2. **Data 完成**：数据、许可、覆盖时段和质量记录齐全后进入 worker；缺凭据或范围冲突时停止。
3. **Worker 完成**：实验清单已确认且结果、日志、图表和 experiment-report 齐全后进入 writer。
4. **Writer 完成**：已产出实际 Word 初稿、图表和公式检查通过后进入 teacher。
5. **Teacher 完成**：根据 review checklist 分类自动处理 text/analysis 问题；若出现 experiment/data 类 blocking 项，停止并请求批准。
6. **Revision 完成**：writer 生成修订稿和 revision-response 后再次交给 teacher；直到无 blocking 或达到 3 轮上限。
7. **最终完成**：更新 `pipeline-manifest.md` 为 completed，汇总最终稿件、数据、代码、结果和仍存在的不确定性。

## 模式切换与优先级

- 用户明确说“自动/端到端/一条龙” → `autonomous`。
- 用户明确说“一步一步/分段/只做某阶段” → `stepwise`。
- 未指定时默认 `stepwise`。
- autonomous 运行中，用户可随时说“切成一步一步”或“先停在这里”，之后改为手动批准每个阶段。
- stepwise 运行中，用户可随时说“之后自动继续”，从当前阶段起切换为 autonomous。
- 安全、授权、费用、破坏性操作和科学范围确认门的优先级高于自动继续。

## 执行规则

1. 先判断模式，再读取 `pipeline-manifest.md`；若无文件则根据当前请求创建。
2. 把完整阶段范围交给对应子技能，不自行替代其核心工作。
3. 每次阶段完成后记录真实产物、关键决定、未决项和下一阶段。
4. 不静默跳过失败阶段，不把未确认状态写成 completed。
5. stepwise 模式一次只推进一个阶段；autonomous 模式仅在无硬门时自动推进。
