# Skill 大纲

## 定位

`math-modeling-workflow` 是一个 orchestration skill。它不直接内置所有算法，而是负责：

- 判断项目阶段
- 读取历史论文知识库
- 设计建模路线
- 拆分 DeepSeek 实现任务
- 审核结果和论文一致性
- 维护标准产物

## 资源结构

```text
my-math-modeling-workflow/
  SKILL.md
  agents/openai.yaml
  references/
    workflow-blueprint.md
    skill-outline.md
    model-selection-guide.md
    paper-writing-guide.md
    quality-gates.md
    implementation-brief-for-deepseek.md
  examples/
    papers/
    knowledge/
      extraction-evidence-summary.md
      paper-extraction-summary.json
      per-paper/
      cross-paper/
    scripts/
      analyze_papers_local.py
      summarize_extraction.py
      extract_paper.py
      build_index.py
      build_knowledge.py
      run_all.py
```

## 触发场景

- 新赛题分析
- 数模项目初始化
- 建模路线选择
- 让 DeepSeek 实现代码前写任务书
- 审核 DeepSeek 代码/结果
- 论文大纲和正文审查
- 结果、图表、论文一致性检查
- 从已有项目文件恢复进度

## Skill 主流程

1. Inspect：读取当前目录和关键产物。
2. Recover：判断当前阶段。
3. Retrieve：读取 `examples/knowledge` 中相关历史模式。
4. Plan：写本阶段产物。
5. Gate：高风险节点暂停确认。
6. Delegate：需要实现时写 DeepSeek 任务书。
7. Review：检查 DeepSeek 输出。
8. Integrate：把确认后的结果进入论文和最终报告。

## 不做什么

- 不复制 Modex 加密 skill。
- 不把历史论文内容照搬到新论文。
- 不在没有数据或代码的情况下声称结果已经验证。
- 不直接承诺论文获奖。
- 不把 DeepSeek 未完成的实现写成已完成成果。

## 后续可实现脚本

DeepSeek 可实现：

- `scripts/init_project.py`
- `scripts/check_artifacts.py`
- `scripts/build_modeling_plan.py`
- `scripts/validate_results.py`
- `scripts/generate_paper_outline.py`
- `scripts/compare_paper_results.py`

每个脚本必须有 CLI 参数、输入输出说明和最小测试样例。
