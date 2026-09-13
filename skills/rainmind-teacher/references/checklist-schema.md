# revision-checklist.md 结构

| id | 位置 | 问题 | 建议 | 分类 | blocking | experiment_needed | 状态 |
|---|---|---|---|---|---|---|---|
| C01 | 2.1 节 | 逐时效结论过度声称 | 改为总体及11–24 h显著优于 LSTM | text | yes | no | todo |
| C02 | 1.4 节 | 统计未处理站间相关 | 增加站群 bootstrap 并按 Holm 校正 | analysis | yes | no | todo |
| C03 | 2.3 节 | 单季节、单种子泛化不足 | 增加多种子或反向年份验证 | experiment | yes | yes | todo |

规则：

- `id` 唯一且稳定，二轮审稿沿用原编号。
- `分类` 使用 `text / analysis / experiment / data / reject`。
- `blocking` 使用 `yes / no`。
- `experiment_needed` 使用 `yes / no`。
- `状态` 使用 `todo / done / rejected`。
- writer 必须在 `review/revision-plan.md` 中对所有 `blocking=yes` 或 `experiment_needed=yes` 条目给出处理决定。
