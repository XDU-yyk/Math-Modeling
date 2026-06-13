# 数模论文示例库

从历史比赛论文中提取的知识库，用于辅助数模工作流决策。

## 为什么需要 examples/

工作流 references 提供的是通用方法框架，而 examples/ 是从真实比赛中提炼的"经验库"。当 examples/ 积累到 10+ 份后，skill 会越用越"聪明"——因为它不是背规则，而是参考真实案例做决策。

## 整体结构

```
examples/
  papers/                          # 原始 PDF 归档（只读，不修改）
    01-cumcm-2024-A/
      题目.pdf                     # 原题 PDF
      论文.pdf                     # 最终论文 PDF
    02-cumcm-2024-B/
      ...
  knowledge/                       # 从 PDF 提取的结构化知识（GPT 直接读取）
    papers-index.md                # 所有论文元数据表
    per-paper/                     # 每篇论文的提取结果
      01-cumcm-2024-A.md
      ...
    cross-paper/                   # 跨论文汇总知识
      modeling-methods-from-examples.md     # 各题用了什么模型、按题型分类
      paper-structures-from-examples.md     # 各篇论文结构对比、摘要模式
      result-presentation-from-examples.md  # 结果表格/图表/敏感性的呈现方式
      common-patterns-from-examples.md      # 跨题复现的模式（数据清洗、灵敏度分析等）
  scripts/                         # 知识抽取流水线
    extract_paper.py               # 单篇: PDF → per-paper markdown
    build_index.py                 # 扫描 papers/ 生成/更新 papers-index.md
    build_knowledge.py             # 聚合 per-paper/ → cross-paper/ 知识文件
    run_all.py                     # 一键: extract + index + knowledge
```

## 数据流

```
papers/*.pdf
    │
    ▼  [extract_paper.py]  使用 pdf-to-md + GPT 提取
    │
per-paper/*.md  ← 每篇的结构化提取
    │
    ├──► [build_index.py]    →  papers-index.md（元数据表）
    │
    └──► [build_knowledge.py] →  cross-paper/*.md（跨论文知识）
```

## 使用方式

### 首次入库

1. 下载 PDF 放入 `papers/{序号-比赛-年份-题号}/`
2. 运行 `python scripts/run_all.py`（依次执行 extract → index → knowledge）
3. 手动复核 `knowledge/per-paper/` 和 `knowledge/cross-paper/` 中 GPT 提取的内容

### 日常使用

工作流 skill 会自动读取 `knowledge/` 中的内容：
1. 读 `papers-index.md` 找同类题
2. 读对应 `per-paper/` 提取
3. 读 `cross-paper/` 汇总做决策

### 新增论文

1. 放入 `papers/` 新目录
2. 运行 `python scripts/run_all.py`
3. 提交更新

## 引用方式

skill 通过相对路径 `../examples/knowledge/` 引用知识文件。
