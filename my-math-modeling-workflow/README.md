# Math Modeling Workflow

基于 Modex 可恢复 pipeline 设计的数学建模竞赛工作流，支持 Codex + DeepSeek 双模型协作或纯 DeepSeek 单模型执行。

## 快速开始

```powershell
# 初始化一个新赛题项目
python scripts/init_project.py "D:\Math Modeling\projects\2026-国赛-A" --competition 国赛 --problem A
```

## 核心文档

| 文件 | 说明 |
|------|------|
| `SKILL.md` | Skill 入口定义，含 stage gates 和行为规则 |
| `references/workflow-blueprint.md` | 7 阶段蓝图，定义每个阶段的输入/输出/确认点 |
| `references/workflow-pipeline.md` | 两种分工模式的具体操作指引 |
| `references/quality-gates.md` | 质量关口检查规则 |
| `references/model-selection-guide.md` | 模型选择指南 |
| `references/paper-writing-guide.md` | 论文写作规范 |
| `references/implementation-brief.md` | DeepSeek 实现任务书模板 |

## 目录结构

```
my-math-modeling-workflow/
├── SKILL.md                     # Skill 入口
├── README.md                    # 本文件
├── TODO.md                      # 后续实现项
├── agents/
│   └── openai.yaml
├── references/                  # 工作流指南
├── scripts/                     # 项目脚手架
│   ├── init_project.py
│   ├── build_deepseek_brief.py
│   ├── check_artifacts.py
│   └── check_results_consistency.py
└── examples/                    # 论文示例知识库
    ├── README.md
    ├── papers/                  # 原始 PDF 归档
    ├── knowledge/               # 抽取的结构化知识
    └── scripts/                 # 知识抽取流水线
```

## 核心原则

1. **不跳步**：每阶段产出一个可检查文件，下一步只基于这些文件继续。
2. **先确认再推进**：题意确认 → 路线确认 → 结果确认 → 论文确认，每个确认点都必须通过。
3. **结果可追溯**：论文中每个数字必须能在 `RESULTS.md` 中找到来源，`RESULTS.md` 的每个结果必须能由 `code/` 复现。
