# Python 实验代码约定

- 每个实验一个 .py，写在 studies/<slug>/code/，命名 exp01_<动作>.py。
- 数据读取用 data-manifest.md 里的 local_path；用相对项目根的 data/...，不硬编码绝对路径。
- 依赖写进 code/requirements.txt；用 venv/conda 管理环境。
- 可复现：固定 random_state、记录数据版本与关键库版本。
- 结果写 results/，图写 results/figures/，日志写 results/logs/。
- 每个脚本要能 `python code/exp01.py` 独立运行。