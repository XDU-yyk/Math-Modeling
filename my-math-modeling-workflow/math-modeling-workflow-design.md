# 个人数模工作流设计草案

## 目标

基于 Modex 的真实工作流结构，创建一套可被 Codex 使用的个人数模 workflow。第一版不复制 Modex 的加密 skill，不重建桌面后端，只把它的有效设计转译成 Codex-native skill：

- 阶段清晰
- 产物命名固定
- 高风险节点需要用户确认
- 每一步都能从已有文件恢复上下文
- 代码、结果、图表、论文互相校验

## 推荐落地形态

创建全局 Codex skill：

```text
C:\Users\yyk\.codex\skills\math-modeling-workflow
```

目录结构：

```text
math-modeling-workflow/
  SKILL.md
  agents/
    openai.yaml
  references/
    pipeline.md
    modeling-methods.md
    paper-structure-zh.md
    error-checklist.md
  scripts/
    init_project.py
    check_artifacts.py
```

## 触发方式

这类请求应触发该 skill：

- “帮我做一道数学建模题”
- “搭一个数模项目”
- “分析这道赛题并建模”
- “按国赛/美赛/华为杯流程推进”
- “检查我的数模论文/代码/结果是否一致”
- “继续这个数模项目”

## 标准项目产物

每个项目以文件作为状态，不依赖隐藏会话：

```text
PROJECT_BRIEF.md
PROBLEM_ANALYSIS.md
MODELING_PLAN.md
MODELING_REPORT.md
RESULTS.md
CHECK_REPORT.md
data/
code/
figures/
paper/
logs/
```

核心产物职责：

- `PROJECT_BRIEF.md`：比赛类型、题目文件、约束、时间预算、选题/小问范围。
- `PROBLEM_ANALYSIS.md`：题意重述、变量/符号、目标、约束、数据需求、子问题拆解。
- `MODELING_PLAN.md`：候选模型、方法选择理由、求解路线、验证指标、风险。
- `MODELING_REPORT.md`：最终模型、公式、算法、参数、假设、敏感性分析。
- `code/`：数据清洗、求解、仿真、作图代码。
- `RESULTS.md`：运行命令、关键结果表、图表索引、结论与反常点。
- `figures/`：论文图、流程图、示意图、导出的图片。
- `paper/`：论文正文，第一版可用 Markdown，后续按比赛切 LaTeX。
- `CHECK_REPORT.md`：数据-模型-代码-结果-论文一致性检查。

## 阶段流程

### 1. 项目初始化

输入：题目 PDF/Word/图片、比赛类型、时间预算、已有数据。

输出：

- 标准目录
- `PROJECT_BRIEF.md`

确认点：

- 是否明确比赛类型和交付格式
- 是否明确要做全部题目还是部分题目

### 2. 赛题分析

输出：

- `PROBLEM_ANALYSIS.md`

检查：

- 每个小问是否被拆成可求解任务
- 是否列出已知数据、待补数据、不可获得数据
- 是否区分目标函数、约束条件、评价指标

确认点：

- 用户确认题意理解无偏差后进入建模。

### 3. 建模路线

输出：

- `MODELING_PLAN.md`

检查：

- 至少给出 2-3 个候选模型
- 说明为什么选主模型，为什么不用其他模型
- 明确变量、参数、假设、求解算法、验证指标

确认点：

- 用户可要求换模型、简化模型或增强创新性。

### 4. 代码与求解

输出：

- `code/main.py`
- `RESULTS.md`

检查：

- 代码能从 `data/` 读取输入并生成可复现结果
- 结果包含运行命令、关键表格、异常说明
- 若没有真实数据，必须显式标注模拟数据或假设数据

确认点：

- 用户确认结果可信后进入图表和论文。

### 5. 图表与流程图

输出：

- `figures/`
- 图表清单写入 `RESULTS.md` 或 `paper/figure_plan.md`

检查：

- 每张图对应一个论文论点
- 图题、坐标轴、单位、数据来源清楚
- 流程图能解释模型/算法/评价闭环

### 6. 论文撰写

输出：

- `paper/main.md` 或 `paper/main.tex`

默认中文结构：

1. 摘要
2. 问题重述
3. 模型假设
4. 符号说明
5. 模型建立与求解
6. 结果分析
7. 灵敏度/误差/稳健性分析
8. 模型评价与改进
9. 参考文献
10. 附录

确认点：

- 用户确认论文主叙事和结论。

### 7. 合规检查

输出：

- `CHECK_REPORT.md`

检查：

- 题目要求是否全部回应
- 模型、代码、结果、论文是否一致
- 图表是否有对应结论
- 单位、符号、编号、引用是否统一
- 是否存在“编造数据/未声明假设/结果无法复现”的风险

## Skill 行为规则

1. 先读取项目已有文件，再决定从哪个阶段继续。
2. 如果用户只给题目，先做初始化和赛题分析，不直接写论文。
3. 如果没有数据，必须明确询问或标注数据假设。
4. 编程阶段必须优先生成可运行、可复现的代码。
5. 论文内容必须反向核对 `PROBLEM_ANALYSIS.md`、`MODELING_REPORT.md`、`RESULTS.md`。
6. 对中文数模交付，默认说明文字、图表标题、论文内容使用中文。
7. 每个阶段结束时给出下一步建议和是否需要用户确认。
8. **参考历史案例**：开始新赛题前，先读取 `examples/knowledge/papers-index.md` 查找同类题。建模选型时引用 `examples/knowledge/cross-paper/modeling-methods-from-examples.md`。论文撰写时参考 `examples/knowledge/cross-paper/paper-structures-from-examples.md`。结果呈现时参考 `examples/knowledge/cross-paper/result-presentation-from-examples.md`。

## 第一版验收

创建后应满足：

- `quick_validate.py` 能通过 skill 结构校验。
- `init_project.py` 能创建标准项目目录。
- `check_artifacts.py` 能在空项目、半完成项目、完成项目上给出清楚报告。
- `SKILL.md` 能让 Codex 按阶段推进，而不是一次性跳到论文终稿。
- skill 不引用或依赖 Modex 的加密 `.enc` 内容。

## 实施清单

收到确认后按这个顺序落地：

1. 用 `skill-creator` 的 `init_skill.py` 初始化 `math-modeling-workflow`，资源目录选择 `references,scripts`。
2. 生成 `agents/openai.yaml`，让 Codex UI 能显示技能名称、简介和默认提示。
3. 写 `SKILL.md`：
   - frontmatter 只包含 `name` 和 `description`
   - body 只保留核心调度规则
   - 长内容放入 `references/`
4. 写 `references/pipeline.md`，定义七阶段、输入、输出、确认点和继续规则。
5. 写 `references/modeling-methods.md`，提供方法选择表，不把它写成固定答案。
6. 写 `references/paper-structure-zh.md`，作为中文论文结构和章节约束。
7. 写 `references/error-checklist.md`，覆盖题意、数据、模型、代码、结果、图表、论文和格式一致性。
8. 写 `scripts/init_project.py`，生成标准项目目录和 starter markdown。
9. 写 `scripts/check_artifacts.py`，检查关键产物、空文件、阶段缺口和一致性提醒。
10. 运行 `quick_validate.py`。
11. 用临时目录测试 `init_project.py` 和 `check_artifacts.py`。
12. 把测试结果写回 `progress.md`。

## 验收矩阵

| 要求 | 证据 |
| --- | --- |
| skill 可被 Codex 自动发现 | `C:\Users\yyk\.codex\skills\math-modeling-workflow\SKILL.md` 存在且 frontmatter 合法 |
| 不复制 Modex 加密内容 | skill 内没有 `.enc` 文件，没有引用 Modex 解密正文 |
| 能初始化项目 | `init_project.py <dir>` 创建标准目录和 starter markdown |
| 能检查项目状态 | `check_artifacts.py <dir>` 对空项目、半完成项目给出分阶段报告 |
| 能按阶段推进 | `SKILL.md` 明确先读现有文件，再判断阶段，不直接跳到论文 |
| 中文数模默认中文 | `SKILL.md` 和 `paper-structure-zh.md` 明确中文交付默认中文 |
| 可从中断恢复 | `pipeline.md` 明确通过项目文件判断当前阶段 |
| 高风险点有确认 | `pipeline.md` 标出题意、建模路线、代码结果、论文终稿确认点 |

## 示例库集成

skill 不是凭空做决策的——它参考历史论文。详见独立的 `examples-design.md`。

核心链路：

```
examples/papers/*.pdf
    │  [extract_paper.py]
    ▼
examples/knowledge/per-paper/*.md
    │  [build_index.py] + [build_knowledge.py]
    ▼
examples/knowledge/
    ├── papers-index.md                    ← skill 查找同类题
    ├── cross-paper/modeling-methods-from-examples.md   ← skill 参考建模选型
    ├── cross-paper/paper-structures-from-examples.md   ← skill 参考论文结构
    └── cross-paper/result-presentation-from-examples.md ← skill 参考结果呈现
```

`SKILL.md` 行为规则已包含：

> 开始新赛题前，先读取 `examples/knowledge/papers-index.md`，查找历史同类题目。建模选型时引用 `cross-paper/modeling-methods-from-examples.md` 中的历史案例辅助决策。

## 后续增强

- 增加比赛模板：国赛、华为杯、MathorCup、美赛。
- 增加 LaTeX 论文模板。
- 增加数据质量检查脚本。
- 增加图表规范检查。
- 根据真实比赛项目拆分为多 skill 套件。
- 积累 10+ 论文后，用 `build_knowledge.py` 重新聚合 cross-paper 知识。
