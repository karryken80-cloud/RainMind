# RainMind

> 面向大气科学研究的模块化 Codex Skill 流水线  
> A modular Codex skill pipeline for atmospheric science research.

RainMind 将“文献调研 → 研究计划 → 数据采集 → 实验执行 → Word 论文写作 → 同行审稿 → 修订再审”组织为一组可组合的 Codex Skills。每个阶段有独立职责、输入输出和停止规则，既可以一步一步运行，也可以由总路由自动编排完整流水线。

## 核心特点

- **双模式总控**
  - 分段模式：一次只执行一个阶段，完成后停下等待确认。
  - 自动端到端模式：按硬性确认门自动推进完整流水线。
- **可追溯研究流程**
  - 每阶段通过 `manifest.md`、`data-manifest.md`、`experiments.yaml`、`review/` 等文件交接。
  - 结果、图表和论文内容必须能追溯到数据、代码或文献。
- **审稿-修订闭环**
  - `rainmind-teacher` 输出结构化审稿报告、可勾销清单和补实验判断。
  - `rainmind-writer` 将审稿意见分类为 `text / analysis / experiment / data / reject`，再决定改写或补充实验。
- **出版级图表与 Word 稿件**
  - 出版图使用统一配色、面板证据逻辑和可编辑 SVG/PDF/TIFF 输出。
  - Word 稿件支持公式、三线表、图注、匿名投稿和审稿回归修订。
- **不编造结果**
  - 只使用实际采集的数据、已运行实验和可核验的新实验。
  - 缺少数据、凭据、基线或实验时明确停下，不静默补造。

## Skill 组成

| Skill | 作用 |
|---|---|
| `rainmind-research` | 总路由与双模式控制器，负责阶段分派、状态记录、硬门停止和审稿修订循环 |
| `rainmind-study` | 文献调研、论文分级、研究缺口分析、研究计划制定 |
| `rainmind-data-collector` | ERA5、GNSS、CMIP6 等数据采集、处理与 `data-manifest.md` 记录 |
| `rainmind-worker` | 生成并运行 Python 实验，产出结果、日志、出版图和实验报告 |
| `rainmind-writer` | 按目标期刊要求生成 Word 中文论文初稿，并根据审稿意见修订 |
| `rainmind-teacher` | 以目标期刊审稿人视角审查语言、图表、公式和科学性，输出修订清单与补实验判断 |

## 流水线结构

```text
rainmind-research
     |
     +-- rainmind-study
     |     文献调研 -> 研究计划 -> 风险与决策
     |
     +-- rainmind-data-collector
     |     数据下载 -> 预处理 -> data-manifest.md
     |
     +-- rainmind-worker
     |     实验代码 -> 训练/运行 -> 结果 -> 出版图
     |
     +-- rainmind-writer
     |     论文框架 -> Word 初稿 -> 图注与公式
     |
     +-- rainmind-teacher
     |     审稿报告 -> 修订清单 -> 补实验判断
     |
     +-- rainmind-writer revision
           修订稿 -> 再审 -> 收敛
```

## 安装

克隆仓库：

```bash
git clone https://github.com/karryken80-cloud/RainMind.git
```

将需要的 Skill 目录复制到 Codex 用户级 Skill 目录。官方当前文档描述的目录为：

```text
$HOME/.agents/skills/
```

部分 Codex 版本使用：

```text
$HOME/.codex/skills/
```

Windows PowerShell 示例：

```powershell
Copy-Item -Recurse -Path ".\RainMind\skills\*" -Destination "$HOME\.agents\skills\" -Force
```

如果不确定当前版本使用哪个目录，请在 Codex 中查看已安装 Skill 的路径，或将它作为仓库级 Skill 放在：

```text
<repo>/.agents/skills/
```

Codex 会在启动或刷新时检测 Skill；如果未出现，重启 Codex。

## 使用方式

### 1. 分段模式（默认）

适合逐步控制研究流程：

```text
使用 $rainmind-research，一步一步执行，先做阶段 1。
```

行为：

```text
执行一个阶段 -> 汇报结果 -> 更新状态 -> 停止 -> 等待用户确认
```

### 2. 自动端到端模式

适合在明确约束下自动推进：

```text
使用 $rainmind-research，自动完成整个流水线，遇到硬门时停下确认。
```

自动模式会依次运行：

```text
study -> data collector -> worker -> writer -> teacher -> writer revision
```

以下情况必须停下：

- 科学问题或关键研究决策尚未确认
- 需要账号、许可证、付费服务或私密数据
- 下载范围、体积或费用与计划不符
- 实验清单尚未确认
- 缺少目标期刊或官方投稿要求
- 审稿要求新增实验、替换数据或重训模型
- 涉及破坏性文件操作或生产系统

## 典型输出

- `studies/<slug>/文献调研.md`
- `studies/<slug>/研究计划.md`
- `studies/<slug>/manifest.md`
- `data/data-manifest.md`
- `code/experiments.yaml`
- `results/`：日志、指标、模型和出版图
- `manuscript/<期刊>_初稿.docx`
- `manuscript/<期刊>_修订稿.docx`
- `manuscript/review/review-report.md`
- `manuscript/review/revision-checklist.md`

## 推荐配套 Skill

RainMind 可与以下 Codex Skills 协作：

- `$nature-figure`：出版级科学图表
- `$documents`：DOCX 创建、渲染与校验
- `$skill-creator`：创建或更新 Skill
- `$plugin-creator`：把多个 Skill 打包为可分发 Plugin

## 数据与隐私

本仓库只包含可复用的 Skill 文件、说明和脚本，不包含：

- 研究数据
- API Key 或访问令牌
- `.cdsapirc` 等凭据
- 私有项目或内部文件
- 生成的论文、数据缓存或投稿材料

使用者需要自行准备数据、账号、算力和期刊访问权限。

## 版本状态

RainMind 当前处于持续迭代阶段。推荐将完整 Skill 集合作为 Plugin 分发；如果仅用于个人或团队项目，也可以直接使用 `skills/` 目录中的 Skill 文件夹。

## 许可证

当前仓库尚未指定开源许可证。在添加明确许可证前，请默认保留所有权利。
