# 数模工作流与 Skill 实现大纲

## 当前成果

已完成：

- 阅读并抽取 `examples/papers/` 下 29 篇 PDF。
- 生成 `examples/knowledge/paper-extraction-summary.json`。
- 生成 `examples/knowledge/extraction-evidence-summary.md`。
- 生成 29 篇 `examples/knowledge/per-paper/*.md` 草稿。
- 更新四份 `examples/knowledge/cross-paper/*.md` 跨论文总结。
- 创建 `SKILL.md`、`agents/openai.yaml`、`references/*.md` 大纲。

## Codex 与 DeepSeek 分工

Codex 负责：

- 工作流设计
- 产物契约
- 任务拆分
- 文档和论文一致性审查
- 对 DeepSeek 实现结果做质量关口检查

DeepSeek 负责：

- 具体脚本实现
- 模型求解代码
- 数据处理和图表生成
- PDF/Word/LaTeX 转换工具
- 自动化知识抽取增强

## 第一阶段实现任务

### 1. 项目初始化脚本

文件：`scripts/init_project.py`

功能：

- 创建标准目录。
- 写入 starter markdown。
- 可指定比赛类型、题号、语言、是否使用 LaTeX。

验收：

- 空目录运行后生成完整结构。
- 重复运行不覆盖用户已有内容。

### 2. 产物检查脚本

文件：`scripts/check_artifacts.py`

功能：

- 检查标准产物是否存在。
- 检查空文件和关键章节缺失。
- 判断当前阶段。
- 输出中文检查报告。

验收：

- 空项目、半完成项目、完整项目均能给出明确报告。

### 3. DeepSeek 任务书生成器

文件：`scripts/build_deepseek_brief.py`

功能：

- 读取 `PROBLEM_ANALYSIS.md` 和 `MODELING_PLAN.md`。
- 生成 `IMPLEMENTATION_TASKS.md`。
- 明确输入、输出、运行命令、验收标准。

验收：

- 生成的任务书能直接交给 DeepSeek 实现。

### 4. 结果一致性检查

文件：`scripts/check_results_consistency.py`

功能：

- 从 `RESULTS.md` 抽取关键数字。
- 检查论文正文是否引用结果。
- 检查图表文件是否存在。

验收：

- 能列出缺失图表、未引用结果、疑似不一致数字。

### 5. 论文知识库增强

现有脚本：

- `examples/scripts/analyze_papers_local.py`
- `examples/scripts/summarize_extraction.py`

后续增强：

- 用更可靠的 PDF 版式抽取工具替代纯 pypdf。
- 从 per-paper 自动解析比赛、题号、核心模型和方法标签。
- 让 `build_index.py` 和 `build_knowledge.py` 从桩代码变为可运行。

## Skill 使用路径

1. 用户给题目或项目目录。
2. Codex 触发 `math-modeling-workflow`。
3. Codex 读取 `references/workflow-blueprint.md`。
4. Codex 读取 `examples/knowledge` 查找历史模式。
5. Codex 生成或更新当前阶段产物。
6. 到实现阶段时，Codex 写 DeepSeek 任务书。
7. DeepSeek 实现。
8. Codex 用 `quality-gates.md` 审核。
9. Codex 再推进图表和论文。

## 完成标准

第一版完整 workflow 完成时，应具备：

- 可发现的 `SKILL.md`。
- 清晰的 references。
- 可运行的项目初始化和检查脚本。
- 基于历史论文的知识库。
- DeepSeek 实现任务书模板。
- 结果和论文一致性检查流程。
