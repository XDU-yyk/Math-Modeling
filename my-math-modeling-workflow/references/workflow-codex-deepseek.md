# Codex + DeepSeek 双模型数模工作流

适用场景：比赛时间紧、题目复杂、希望把“分析/审稿”和“实现/跑代码”分开。  
核心分工：Codex 负责题意、路线、任务书、质量门和论文；DeepSeek 负责代码、模型求解、图表和结果文件。

## 0. 新建比赛项目

在 PowerShell 中进入工作流目录：

```powershell
cd "D:\Math Modeling\my-math-modeling-workflow"
python scripts/init_project.py "D:\Math Modeling\projects\2026-国赛-A" --competition 国赛 --problem A
```

把赛题 PDF、附件和数据放入项目目录：

```text
D:\Math Modeling\projects\2026-国赛-A\赛题.pdf
D:\Math Modeling\projects\2026-国赛-A\data\附件1.xlsx
D:\Math Modeling\projects\2026-国赛-A\data\附件2.csv
```

## 1. Codex 做赛题分析

目标：只完成 `PROBLEM_ANALYSIS.md`，不要建模、不要写论文。

给 Codex：

```text
请使用 D:\Math Modeling\my-math-modeling-workflow 的数模工作流。
项目目录是：D:\Math Modeling\projects\2026-国赛-A

请读取赛题和 data/ 中的数据，只完成 PROBLEM_ANALYSIS.md。
要求：
1. 拆清每个小问的目标、输入、输出、约束和评价指标。
2. 写出数据需求、已有数据、缺失数据和不能假设的边界。
3. 结合 examples/knowledge/papers-index.md 查找相似题型。
4. 不要直接建模，不要写代码，不要写论文。
完成后暂停，等我确认题意理解。
```

确认点：人工检查 `PROBLEM_ANALYSIS.md`。如果题意错了，必须先改，不能进入建模。

## 2. Codex 做建模路线

目标：完成 `MODELING_PLAN.md`，给出 2-3 条路线并推荐一条。

给 Codex：

```text
继续使用项目目录：D:\Math Modeling\projects\2026-国赛-A

请基于 PROBLEM_ANALYSIS.md 生成 MODELING_PLAN.md。
要求：
1. 给出 2-3 条候选建模路线。
2. 每条路线写清适用条件、数据要求、优缺点、求解算法和失败备选方案。
3. 结合 examples/knowledge/cross-paper/ 中的历史论文模式。
4. 最后给出“子问题 -> 模型 -> 算法 -> 验证指标”的表格。
5. 不要写代码，不要写论文。
完成后暂停，等我确认模型路线。
```

确认点：人工确认模型路线。路线不稳时，不要交给 DeepSeek。

## 3. Codex 生成 DeepSeek 任务书

运行：

```powershell
python scripts/build_deepseek_brief.py "D:\Math Modeling\projects\2026-国赛-A"
```

输出：`IMPLEMENTATION_TASKS.md`

确认点：检查任务书是否包含输入、输出、脚本接口、运行命令、验收标准。

## 4. DeepSeek 做实现

给 DeepSeek：

```text
你现在只负责实现，不负责重新设计工作流。

工作流目录：
D:\Math Modeling\my-math-modeling-workflow

具体赛题项目目录：
D:\Math Modeling\projects\2026-国赛-A

请先阅读：
1. IMPLEMENTATION_TASKS.md
2. PROBLEM_ANALYSIS.md
3. MODELING_PLAN.md
4. D:\Math Modeling\my-math-modeling-workflow\references\quality-gates.md

你的任务：
1. 在 code/ 中实现数据读取、预处理、模型求解和图表生成。
2. 在 figures/ 中生成图表。
3. 在 logs/ 中记录运行日志。
4. 更新 RESULTS.md，写清运行命令、输入数据、关键参数、核心结果表和图表索引。

限制：
1. 不要修改 D:\Math Modeling\my-math-modeling-workflow 下的工作流设计文件。
2. 不要写论文正文。
3. 不要把没有代码、数据或人工假设支撑的结论写入 RESULTS.md。
4. 如果使用模拟数据，必须在代码注释和 RESULTS.md 中明确标注。
5. 随机过程必须设置随机种子。

完成后告诉我：
1. 运行了哪些命令。
2. 生成或修改了哪些文件。
3. 结果是否可复现。
4. 还有哪些风险或待人工确认点。
```

## 5. Codex 验收 DeepSeek 输出

运行：

```powershell
python scripts/check_artifacts.py "D:\Math Modeling\projects\2026-国赛-A"
python scripts/check_results_consistency.py "D:\Math Modeling\projects\2026-国赛-A"
```

给 Codex：

```text
DeepSeek 已完成实现。请审查项目目录：
D:\Math Modeling\projects\2026-国赛-A

请重点检查：
1. code/ 是否能按 RESULTS.md 的命令复现结果。
2. RESULTS.md 的数字是否来自代码或数据。
3. figures/ 中图表是否与 RESULTS.md 和论文计划一致。
4. 是否存在模拟数据、硬编码结论、未声明假设或无法复现结果。
5. 用 check_artifacts.py 和 check_results_consistency.py 的结果给出返工清单。

不要写论文，先完成验收。
```

如果验收失败，把返工清单交回 DeepSeek。

## 6. Codex 写论文

只有当结果可信后，才进入论文阶段。

给 Codex：

```text
现在实现和 RESULTS.md 已通过验收。
项目目录：D:\Math Modeling\projects\2026-国赛-A

请生成 paper/main.md 或 paper/main.tex。
要求：
1. 论文数字必须能追溯到 RESULTS.md 或代码输出。
2. 图表引用必须对应 figures/ 中的真实文件。
3. 假设、符号、模型公式、求解过程和结果解释要一致。
4. 使用中文数模论文结构：摘要、关键词、问题重述、问题分析、模型假设、符号说明、模型建立与求解、灵敏度分析、模型评价、参考文献、附录。
5. 写完后更新 CHECK_REPORT.md。
```

## 7. 最终检查

运行：

```powershell
python scripts/check_artifacts.py "D:\Math Modeling\projects\2026-国赛-A"
python scripts/check_results_consistency.py "D:\Math Modeling\projects\2026-国赛-A"
```

最终人工检查：

- 每个小问都有回答。
- 每个数字有来源。
- 每张图有文件、有正文引用、有解释。
- 代码能从空运行生成结果。
- 模拟数据、缺失数据和限制条件已说明。

## 快速原则

- Codex：想清楚、拆清楚、审清楚、写清楚。
- DeepSeek：跑得动、算得出、图表全、结果可复现。
- 不跳过确认点：题意确认、路线确认、结果确认、论文确认。
