# 数模论文示例库

从历史比赛论文中提取的知识库，用于辅助数模工作流决策。

## 结构

```
examples/
  papers/          ← 原始 PDF（等你放入）
    {序号-比赛-年份-题号}/
      题目.pdf
      论文.pdf
  knowledge/       ← 从 PDF 提取的结构化知识
    papers-index.md               ← 所有论文元数据索引
    per-paper/                    ← 每篇论文的提取结果
    cross-paper/                  ← 跨论文汇总知识
  scripts/         ← 知识抽取流水线
    extract_paper.py
    build_index.py
    build_knowledge.py
    run_all.py
```

## 使用方式

### 首次使用

1. 下载 PDF 放入 `papers/`
2. 运行 `python scripts/run_all.py`
3. 手动复核 `knowledge/per-paper/` 和 `knowledge/cross-paper/`

### 日常

工作流 skill 会自动读取 `knowledge/` 中的内容，无需手动操作。

## 引用方式

skill 通过相对路径 `../examples/knowledge/` 引用知识文件。
