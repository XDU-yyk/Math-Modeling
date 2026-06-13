# 数模论文示例库设计 — examples/

## 为什么需要 examples/

工作流 skill (`references/modeling-methods.md` 等) 提供的是通用方法框架，而 examples/ 是从真实比赛中提炼的"经验库"。GPT 跑新比赛时，能参考历史论文中的：

- 特定题型用了什么模型、为什么
- 论文怎么写才能拿奖
- 结果表格/图表怎么呈现才清晰
- 哪些坑前人踩过

当 examples/ 积累到 10+ 份后，skill 会越用越"聪明"——因为它不是背规则，而是参考真实案例做决策。

## 整体结构

```
examples/
  README.md                        # 示例库入口：索引说明 + 快速使用
  papers/                          # 原始 PDF 归档（只读，不修改）
    01-cumcm-2024-A/
      题目.pdf                     # 原题 PDF
      论文.pdf                     # 最终论文 PDF
    02-cumcm-2024-B/
      题目.pdf
      论文.pdf
    03-huawei-2024/
      题目.pdf
      论文.pdf
    ... (10+ 份)
  knowledge/                       # 从 PDF 提取的结构化知识（GPT 直接读取）
    papers-index.md                # 所有论文元数据表（比赛/年份/题号/模型/方法标签）
    per-paper/                     # 每篇论文的提取结果
      01-cumcm-2024-A.md
      02-cumcm-2024-B.md
      ...
    cross-paper/                   # 跨论文汇总（由脚本聚合生成）
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

## knowledge/ 文件规范

### papers-index.md

竞赛元数据表，方便 skill 按条件查找相关历史：

```markdown
# 历史论文索引

| # | 比赛 | 年份 | 题号 | 题目关键词 | 核心模型 | 方法标签 | 文件位置 |
|---|------|------|------|-----------|----------|----------|----------|
| 01 | 国赛 | 2024 | A | 龙舟/螺旋桨 | 微分方程、CFD | 物理建模、仿真 | per-paper/01-cumcm-2024-A.md |
| 02 | 华为杯 | 2024 | B | 网络流量预测 | LSTM、ARIMA | 时间序列、深度学习 | per-paper/02-huawei-2024.md |
| ... | ... | ... | ... | ... | ... | ... | ... |
```

**方法标签** 标准化列表（按需扩充）：
- 物理建模 / 微分方程 / 元胞自动机 / 多智能体
- 统计回归 / 时间序列 / 聚类 / 分类 / 降维
- 优化 / 线性规划 / 整数规划 / 启发式算法
- 深度学习 / CNN / LSTM / Transformer / GNN
- 评价 / AHP / TOPSIS / 熵权法 / 灰色关联
- 仿真 / 蒙特卡洛 / 随机过程 / 排队论

### per-paper/{id}.md

每篇论文的提取模板：

```markdown
# [比赛] [年份] [题号] — [题目关键词]

## 元数据
- 比赛：国赛 / 华为杯 / MathorCup / ...
- 年份：2024
- 题号：A
- 题目关键词：龙舟螺旋桨设计
- 核心模型：微分方程、CFD 仿真
- 方法标签：物理建模、仿真、优化

## 题目简析
原文题意一句话概括 + 关键约束/目标/数据

## 建模路线
- 主模型：XXX（为什么选它）
- 辅助模型：XXX（用于什么子问题）
- 不选的其他模型：XXX（理由）

## 求解方法
- 算法/求解器：XXX
- 关键参数：XXX
- 创新点/亮点：XXX

## 结果呈现
- 核心结论表格（摘要）
- 关键图表的描述
- 敏感性/误差分析方式

## 论文结构
- 章节大纲（实际论文的顶级标题）
- 摘要结构（背景→问题→模型→结果→结论）

## 可复用的模式
这个题里有什么做法可以搬到其他题
```

### cross-paper/*.md

由 `build_knowledge.py` 自动聚合生成，结构如下：

**modeling-methods-from-examples.md** — 按题型整理模型选择：

```markdown
# 历史建模方法参考

## 物理机理类（国赛 A 题常见）
| 年份 | 题目 | 模型 | 方法标签 |
|------|------|------|----------|
| 2024 | 龙舟螺旋桨 | 微分方程+CFD | 物理建模、仿真 |
| 2023 | 太阳能板朝向 | 几何光学+优化 | 物理建模、优化 |

## 数据预测类（华为杯常见）
| 年份 | 题目 | 模型 | 方法标签 |
|------|------|------|----------|
| 2024 | 网络流量预测 | LSTM+ARIMA | 时间序列、深度学习 |
| 2023 | 空气质量预测 | XGBoost+CNN | 时间序列、机器学习 |

...
```

## 工作流集成

`SKILL.md` 中增加一条行为规则：

> 开始新赛题前，先读取 `examples/knowledge/papers-index.md`，查找历史同类题目（相同方法标签或题型），阅读对应 `per-paper/` 提取作为参考。建模选型时引用 `cross-paper/modeling-methods-from-examples.md` 中的历史案例辅助决策。

`references/modeling-methods.md` 末尾增加：

> 实际案例参考：`examples/knowledge/cross-paper/modeling-methods-from-examples.md`

## 使用流程

### 首次入库

1. 下载 PDF（可手动或批量）
2. 放入 `papers/{序号-比赛-年份-题号}/`
3. 运行 `python scripts/run_all.py`（会依次执行 extract → index → knowledge）
4. 手动复核 `per-paper/` 和 `cross-paper/` 中 GPT 提取的内容

### 日常使用

GPT 跑新比赛时自动：
1. 读 `papers-index.md` 找同类题
2. 读对应 `per-paper/` 提取
3. 读 `cross-paper/` 汇总做决策

### 新增论文

1. 放入 `papers/` 新目录
2. 运行 `python scripts/run_all.py`
3. 提交更新

## 提取脚本设计要点

### extract_paper.py

```python
"""
用法: python extract_paper.py <paper_dir>

流程:
1. 读取 papers/<dir>/论文.pdf
2. 调用 pdf-to-md 工具转换成 markdown
3. 用 GPT 按 per-paper 模板提取结构化内容
4. 写入 knowledge/per-paper/<id>.md

注意: PDF→MD 用本地工具（pymupdf/marker），结构化提取用 GPT API
"""
```

### build_index.py

```python
"""
用法: python build_index.py

流程:
1. 扫描 papers/ 下所有子目录
2. 读取每个目录名提取元数据（序号-比赛-年份-题号）
3. 读取对应 per-paper/ 提取文件中的核心模型/方法标签
4. 生成完整的 papers-index.md
"""
```

### build_knowledge.py

```python
"""
用法: python build_knowledge.py

流程:
1. 读取所有 per-paper/ 提取
2. 按题型/方法标签分组
3. 聚合生成 cross-paper/ 下的四个知识文件
4. 保留已有的人工修正（不覆盖手动编辑过的行）
"""
```

## 跟 skill 的关系

```
my-math-modeling-workflow/          ← skill 目录（执行逻辑）
  SKILL.md
  references/
  scripts/
    init_project.py
    check_artifacts.py

examples/                           ← 知识库目录（历史数据）
  papers/                           ← 只读归档
  knowledge/                        ← GPT 读取的知识
  scripts/                          ← 抽取流水线
```

两者是兄弟目录，放在同一个项目根下。skill 通过相对路径 `../examples/knowledge/` 引用。
