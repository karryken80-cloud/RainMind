# 检索策略（Phase 1）

## 检索式构建

- 从 Phase 0 确认的科学问题拆出 3-6 个核心概念；每个概念给中文 + 英文 + 常见缩写/同义词（例如 “气溶胶-云相互作用 aerosol-cloud interaction / aerosol indirect effect”、“东亚夏季风 East Asian summer monsoon / EASM”）。
- 用 AND 连接核心概念、OR 连接同义词；优先用英文检索式，中文补充检索中文核心期刊与综述。
- 记录最终检索式、来源、检索日期，写入 文献调研.md 的「问题与检索式」。

## 来源顺序与用法

按以下顺序尝试，上一来源不可用或无结果再下一来源；优先 API 端点，返回不可用时退回 web 搜索 + 打开出版商页。

1. **Web of Science / Scopus**（若有机构权限）：按 JCR 分区/被引筛，最权威；用其检索界面或机构登录。
2. **OpenAlex**：`https://api.openalex.org/works?search=<query>&per-page=25`，可用 `filter=title_and_abstract.search:` 收紧；看 `primary_location.source.display_name`、`cited_by_count`、`publication_year`。
3. **Crossref**：`https://api.crossref.org/works?query=<query>&rows=25`，取 title/DOI/container-title/year。
4. **Semantic Scholar**：`https://api.semanticscholar.org/graph/v1/paper/search?query=<query>&fields=title,abstract,year,externalIds,venue,citationCount`。
5. **arXiv**：`http://export.arxiv.org/api/query?search_query=all:<query>&max_results=25`（气候/大气物理预印本；标注为 preprint，不作正式分级依据）。
6. **Google Scholar / 出版商页**：兜底，注意反爬与结果稳定性；只作发现线索，不作为分区判定依据。

## 去重与初筛

- 去重键：DOI（统一小写）；无 DOI 用规范化标题（去空格/标点/大小写）。
- 初筛标准（标题+摘要）：与科学问题直接相关；剔除纯技术报告、无同行评议的预印本（arXiv 单独标注）、明显重复研究。
- 每轮检索记录：来源、查询式、命中数、去重后数、初筛通过数；覆盖不足时停下问用户，而不是静默换方向。

## 覆盖不足的判定

- 任一核心概念找不到 Q1/Q2 或 Nature Index 文献 → 向用户说明并建议：放宽年份、换检索词、纳入综述/经典文献，或调整问题。