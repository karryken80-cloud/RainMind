---
name: rainmind-worker
description: RainMind 流水线阶段 3：基于 rainmind-data-collector 已采集的数据和已确认的实验方案，用 Python 生成并运行实验代码，产出结果、出版级图和实验报告。用于“执行实验、生成并运行 py、跑模型、产出实验结果、重做论文图”等请求；只执行已确认方案，不擅自修改方案。
---

# RainMind Worker — 实验执行（阶段 3）

读取研究计划与已采集数据，把「方法与技术路线」拆成可运行的 Python 实验，生成并运行 `.py`，产出结果并写实验报告。只执行已确认方案，不改方案、不自行加实验。

## 工作流

1. **读方案与数据**：定位 `studies/<slug>/研究计划.md`、`manifest.md`、`data-manifest.md` 与 `data/`。
2. **生成实验清单**：把方法拆成 `code/experiments.yaml`（字段见 [experiment-plan-schema.md](references/experiment-plan-schema.md)），逐项与用户确认。
3. **生成 Python**：按 [python-conventions.md](references/python-conventions.md) 为每个实验写 `code/expNN_*.py`，从 `data-manifest.md` 的 local_path 读数据。
4. **运行**：按顺序执行，用 `scripts/run_experiment.py --script code/xxx.py --log-dir results/logs` 记录日志与退出码。
5. **报告**：按 [report-schema.md](references/report-schema.md) 写 `experiment-report.md`，列明每个实验的输入/输出/关键结果/失败原因。
6. 结果与图放 `results/`、`results/figures/`。
7. **出版级出图**：凡任务要求论文图、汇报图、重做现有图，或结果将进入高分区论文，必须先加载 `$nature-figure`，并按下方「画图依据」执行。简单 `subplots`、每张表一图、只换颜色不重构证据链，不算完成。

## 画图依据（强制）

- **上位规范**：出版级图表以 `$nature-figure` 为唯一制图规范。先读其 `manifest.yaml`、`static/core/contract.md`、`static/core/stance.md` 和所选后端的 fragment。
- **后台门禁**：Python 与 R 只能二选一。已有 Python/matplotlib 工作流时默认 Python；后端确定后，绘图、预览、导出和视觉 QA 全部使用该后端，禁止跨语言代画。
- **Figure Contract**：画图前先写清五件事：一句可被推翻的核心结论、各面板的证据链、figure archetype、目标期刊/尺寸、导出与源数据契约。没有 Contract 和面板图就不画。
- **一图一论点**：一张主图只回答一个 Results 级科学问题。每个面板必须承担不同证据角色，例如设置、主证据、基线对照、分解、分层、压力测试或失败边界；不要用多个指标重复同一证据。
- **证据层级决定版式**：优先一个 hero panel 加从属面板，按重要性分配面积；不要把所有子图做成等权 dashboard。面板顺序应形成可读的证据推进，而不是表格转图。
- **数据完整性**：不得为了美观、排版或渲染速度删行、删站、删变量或换更弱基线。任何子集、缺失掩膜、排除规则都要记录 before/after 计数和原因。
- **统计进入图内**：每个定量面板必须可追溯 `n`、训练/验证/测试划分、重复或随机种子定义、指标定义、误差/区间定义、基线定义和检验方法。相关面板使用一致的 uncertainty 语义。
- **视觉依据**：白底、克制的蓝绿红中性语义色、统一方法配色、直接标注优先、legend 不重复、禁止 rainbow/jet/hsv；红绿不能作为唯一编码。只有显微/影像 plate 才使用黑底。
- **可调整性**：颜色、字体、字号、panel label 坐标、legend anchor、annotation offset、面板比例和轴范围必须集中为样式/config 常量或 YAML，不得散落魔法数字。用户应能只改配置就重排标注和样式。
- **投稿导出**：双栏宽度优先 183 mm，单栏 89 mm；所有渲染 glyph 最小 5 pt；输出可编辑的文字型 SVG/PDF，并提供 600 dpi TIFF 与 PNG 预览。图和图注必须自足。
- **布局可检核**：绘图脚本必须输出每个文本对象的边界框、字号、是否越界、是否非有限和两两重叠审计，至少生成 `*_text_layout.csv`、`*_text_overlaps.csv` 和 `*_text_layout.json`。最终图要求 non-finite bbox=0、outside figure=0、text overlap=0。若未达标，调整边距、面板比例、legend anchor、标签位置或最小字号；不得用白色遮罩掩盖碰撞，也不得随意删除必要标注。
- **图表 QA**：最终交付前运行 `nature-figure/scripts/validate_figure.py`、对每个 PDF 运行 `scripts/audit_pdf_text.py --min-pt 5`，并检查面板层级、留白、颜色显著性和完整 uncertainty。自动检查不能替代最终尺寸下的逐面板检查。
- **交付结构**：出版图放在 `studies/<slug>/results/figures/publication/`；同步交付 figure captions、source-data CSV、绘图脚本、SVG/PDF/TIFF/PNG 和 QA 记录。
- **停止规则**：若缺 Figure Contract、目标尺寸、后端或证据面板图，先停下补契约；不得用装饰性复杂排版掩盖证据不足。

## 停止规则

- 方案或实验清单未确认 → 不写码、不运行。
- 数据缺失 → 先提示用户补数据（可回 `$rainmind-data-collector`）。
- 某实验失败 → 记录失败项与原因，继续可独立的下一个，不静默跳过。
- 画图任务缺 Figure Contract、后端或面板证据图 → 先补契约，不直接出图。
- Figure 布局审计存在非有限边界框、越界文本或未解决重叠 → 先修布局，不交付最终图。

