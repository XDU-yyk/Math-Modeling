# DeepSeek 实现任务书模板

Codex 负责写本文件，DeepSeek 按本文件实现具体功能。

## 任务摘要

- 项目：
- 当前阶段：
- 要实现的目标：
- 不做的内容：

## 输入文件

| 文件 | 说明 | 是否必需 |
| --- | --- | --- |
| `data/...` |  | yes/no |
| `PROBLEM_ANALYSIS.md` | 题意和子问题 | yes |
| `MODELING_PLAN.md` | 模型路线 | yes |

## 输出文件

| 文件 | 说明 | 验收 |
| --- | --- | --- |
| `code/main.py` | 主入口 | 能按命令运行 |
| `RESULTS.md` | 结果说明 | 包含表格、参数、图表索引 |
| `figures/...` | 图表 | 有标题、单位、数据来源 |

## 接口约定

```text
python code/main.py --input data --output results
```

DeepSeek 实现时必须：

- 保持路径相对项目根目录。
- 把随机种子写入代码或配置。
- 把关键参数集中在配置段。
- 对缺失数据和异常数据给出处理日志。
- 输出机器可读结果，例如 `results/metrics.json` 或 `results/tables/*.csv`。

## 验收标准

- 命令能运行。
- 结果文件存在。
- 日志无未处理异常。
- `RESULTS.md` 能解释主要输出。
- 生成图表能被论文引用。
- 没有把模拟结果伪装成真实结果。

## Codex 审核清单

Codex 收到 DeepSeek 实现后检查：

1. 文件是否符合输出约定。
2. 代码是否真的读取输入数据。
3. 结果数字是否能复现。
4. 图表是否对应论文论点。
5. 是否需要更新 `MODELING_REPORT.md` 或 `PAPER_OUTLINE.md`。
