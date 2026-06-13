# 纯 DeepSeek 单模型数模工作流

适用场景：只想使用一个模型完成全流程，或者 Codex 不参与具体比赛。  
核心原则：DeepSeek 必须同时扮演“分析者、实现者、审稿人”，所以每一步都要强制产出文件和自检报告，不能直接从题目跳到论文。

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

## 1. 给 DeepSeek 的总控提示词

比赛开始后，先发这段，不要直接让它写论文：

```text
你现在负责一个数学建模比赛项目，但必须严格按阶段推进，不能跳步。

工作流目录：
D:\Math Modeling\my-math-modeling-workflow

项目目录：
D:\Math Modeling\projects\2026-国赛-A

请先阅读：
1. D:\Math Modeling\my-math-modeling-workflow\SKILL.md
2. D:\Math Modeling\my-math-modeling-workflow\references\workflow-blueprint.md
3. D:\Math Modeling\my-math-modeling-workflow\references\quality-gates.md
4. D:\Math Modeling\my-math-modeling-workflow\references\model-selection-guide.md
5. D:\Math Modeling\my-math-modeling-workflow\references\paper-writing-guide.md
6. D:\Math Modeling\my-math-modeling-workflow\examples\knowledge\papers-index.md
7. D:\Math Modeling\my-math-modeling-workflow\examples\knowledge\cross-paper\*.md

规则：
1. 每个阶段必须写入项目目录中的标准产物文件。
2. 每完成一个阶段先停下来，给出自检结果和下一阶段建议。
3. 不允许在题意未确认前建模。
4. 不允许在模型路线未确认前写代码。
5. 不允许在结果未验证前写论文。
6. 不允许把没有代码、数据或人工假设支撑的结论写入论文。
7. 如果使用模拟数据，必须在代码注释、RESULTS.md 和论文中明确标注。

现在只做阶段 1：读取赛题和数据，生成 PROBLEM_ANALYSIS.md。
完成后暂停。
```

## 2. 阶段 1：赛题分析

DeepSeek 输出文件：`PROBLEM_ANALYSIS.md`

必须包含：

- 背景重述
- 每个小问的目标、输入、输出、约束
- 评价指标
- 变量与符号草案
- 数据需求、已有数据、缺失数据
- 不能假设的边界
- 与历史论文相似题型

阶段完成后，要求 DeepSeek 自检：

```text
请自检 PROBLEM_ANALYSIS.md：
1. 是否每个小问都有目标、输入、输出和约束？
2. 是否列出数据需求和缺失数据？
3. 是否有未经题目允许的假设？
4. 是否引用了历史论文模式但没有照抄？
如果有问题，请先修正，不要进入建模。
```

## 3. 阶段 2：建模路线

给 DeepSeek：

```text
继续阶段 2：基于 PROBLEM_ANALYSIS.md 生成 MODELING_PLAN.md。

要求：
1. 给出 2-3 条候选路线。
2. 每条路线写清适用条件、数据要求、优点、缺点、求解算法和失败备选方案。
3. 给出推荐路线及理由。
4. 写出“子问题 -> 模型 -> 算法 -> 验证指标”表格。
5. 结合 model-selection-guide.md 和 examples/knowledge/cross-paper/。
6. 不要写代码，不要写论文。
完成后暂停并自检。
```

自检：

- 路线是否覆盖所有小问。
- 模型是否有数据支撑。
- 是否有备选方案。
- 是否能用代码实现。

## 4. 阶段 3：实现任务拆分

运行：

```powershell
python scripts/build_deepseek_brief.py "D:\Math Modeling\projects\2026-国赛-A"
```

如果只让 DeepSeek 自己做，也可以给它：

```text
请基于 PROBLEM_ANALYSIS.md 和 MODELING_PLAN.md 生成 IMPLEMENTATION_TASKS.md。

要求：
1. 明确 code/ 下需要哪些脚本。
2. 明确每个脚本的输入、输出、运行命令。
3. 明确中间文件、图表文件和日志文件。
4. 明确验收标准。
5. 不要开始写代码，先完成任务拆分。
```

## 5. 阶段 4：代码与结果

给 DeepSeek：

```text
现在进入实现阶段。

请读取 IMPLEMENTATION_TASKS.md，然后实现：
1. code/main.py 作为主入口。
2. 必要的数据预处理脚本。
3. 必要的模型求解脚本。
4. 必要的可视化脚本。
5. logs/ 中的运行日志。
6. RESULTS.md。

要求：
1. 所有路径相对于项目根目录。
2. 代码必须能从命令行运行。
3. 随机过程必须设置随机种子。
4. RESULTS.md 必须包含运行命令、输入数据说明、关键参数、核心表格、图表索引和异常说明。
5. 如果使用模拟数据，必须明确标注。
6. 完成后实际运行代码，并报告命令和输出文件。
```

实现后运行检查：

```powershell
python scripts/check_artifacts.py "D:\Math Modeling\projects\2026-国赛-A"
```

## 6. 阶段 5：图表与可视化

给 DeepSeek：

```text
请基于 RESULTS.md 和 code/ 输出生成 figures/ 和 FIGURE_PLAN.md。

要求：
1. 每张图必须对应一个结论或模型环节。
2. 图表有标题、坐标轴、单位、数据来源。
3. 至少包含一张流程图或技术路线图。
4. FIGURE_PLAN.md 写清每张图对应论文哪个章节。
5. 不要写论文正文。
```

## 7. 阶段 6：论文写作

只有结果和图表确认后，再给 DeepSeek：

```text
现在进入论文写作阶段。

请读取：
1. PROBLEM_ANALYSIS.md
2. MODELING_PLAN.md
3. MODELING_REPORT.md
4. RESULTS.md
5. FIGURE_PLAN.md
6. figures/

生成 paper/main.md 或 paper/main.tex。

要求：
1. 论文使用中文数模论文结构。
2. 每个小问必须有明确回答。
3. 每个数字必须来自 RESULTS.md 或代码输出。
4. 每张图必须来自 figures/。
5. 不要编造实验结果。
6. 对模拟数据、缺失数据、模型局限要明确说明。
```

## 8. 阶段 7：最终一致性检查

运行：

```powershell
python scripts/check_artifacts.py "D:\Math Modeling\projects\2026-国赛-A"
python scripts/check_results_consistency.py "D:\Math Modeling\projects\2026-国赛-A"
```

把检查结果给 DeepSeek：

```text
这是最终检查输出。请逐项修正：
1. 缺失产物。
2. 无法追溯的论文数字。
3. 缺失图表。
4. 未引用图表。
5. 模板占位内容。

修正后重新运行检查，直到没有阻断性问题。
```

## 单模型风险控制

纯 DeepSeek 工作流最大风险是“自己写、自己信、自己过”。必须额外做这些事：

- 每阶段停顿一次，人工快速看一遍。
- 所有结论必须落到文件，不接受只在聊天里说。
- 代码先跑，结果后写，论文最后写。
- 论文中的数字必须能在 `RESULTS.md` 找到。
- `RESULTS.md` 中的关键结果必须能由 `code/` 复现。
- 如果时间不够，优先保证题意、模型、代码、结果可信，再压缩论文润色。

## 选择建议

- 时间紧、题目难、需要更稳：用 Codex + DeepSeek。
- 只有一个模型可用、题目较简单：用纯 DeepSeek。
- 无论哪种，都不要跳过 `PROBLEM_ANALYSIS.md` 和 `MODELING_PLAN.md`。
