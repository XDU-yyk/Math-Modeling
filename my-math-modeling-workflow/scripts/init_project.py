r"""项目初始化脚本

用法:
    python init_project.py <项目目录> [选项]

参数:
    项目目录          要创建或初始化的项目路径（会创建标准目录和 starter 文件）
    --competition     比赛类型，如 "国赛" "美赛" "华为杯" "MathorCup" "数维杯" 等
    --problem         题号，如 "A" "B" "C" "D"
    --latex           使用 LaTeX 版论文模板（默认使用 Markdown）
    --lang            语言，zh（中文）或 en（英文），默认 zh

示例:
    python init_project.py D:\projects\cumcm-2026-A --competition 国赛 --problem A
    python init_project.py ./my-project --competition 美赛 --problem B --lang en --latex

规则:
    - 空目录：创建完整结构。
    - 已有部分文件：只补充缺失的目录和 starter 文件。
    - 不会覆盖用户已有内容。
    - 会和现有文件对比后给出差异报告。
"""

from __future__ import annotations

import sys
import argparse
from pathlib import Path
from datetime import datetime


# 标准目录
STD_DIRS = [
    "data",
    "code",
    "figures",
    "paper",
    "logs",
]

# Starter 文件模板
STARTER_FILES = {
    "PROJECT_BRIEF.md": """# 项目登记

> 自动生成于 {datetime}

## 基本信息

- 比赛类型：{competition}
- 题号：{problem}
- 语言：{language}
- 论文格式：{paper_format}
- 项目目录：{project_dir}

## 题目概要

<!-- 请用一两句话概括题目 -->

## 已知数据

<!-- 列出已有数据文件及其来源 -->

## 缺失数据

<!-- 列出需要但不可获得的数据，以及打算如何处理 -->

## 交付物格式

<!-- 例如：PDF 论文 + 可运行代码 + 附录 -->

## 时间预算

<!-- 例如：3 天，每天 8 小时 -->

## 边界

<!-- 明确不能假设的事项 -->
""",

    "PROBLEM_ANALYSIS.md": """# 赛题分析

> 待填写。此文件应在项目初始化后，由 Codex 读取题目 PDF 后生成。

## 背景重述

<!-- 用中文简要重述题目背景 -->

## 子问题拆解

### 问题一
- 目标：
- 输入：
- 输出：
- 约束：
- 评价指标（如有明确提示）：

### 问题二
- 目标：
- 输入：
- 输出：
- 约束：
- 评价指标：

### 问题三
- 目标：
- 输入：
- 输出：
- 约束：
- 评价指标：

### 问题四（如有）

- 目标：
- 输入：
- 输出：
- 约束：
- 评价指标：

## 变量与符号草案

| 符号 | 含义 | 单位 |
|------|------|------|
|      |      |      |

## 数据需求

| 数据项 | 来源 | 可获得性 |
|--------|------|----------|
|        |      |          |

## 与历史论文相似题型

<!-- Codex 在读题后从 examples/knowledge/papers-index.md 查找并填入 -->
""",

    "MODELING_PLAN.md": """# 建模路线

> 待填写。此文件应在完成赛题分析后，由 Codex 结合历史论文知识库生成。

## 候选路线

### 路线 1
- 主模型：
- 适用条件：
- 数据要求：
- 优点：
- 缺点：
- 求解算法：
- 备选方案：

### 路线 2
- 主模型：
- 适用条件：
- 数据要求：

### 路线 3（如有）
- 主模型：

## 推荐路线及理由

## 子问题到模型映射

| 子问题 | 模型 | 求解算法 | 验证指标 |
|--------|------|----------|----------|
| 问题一 |      |          |          |
| 问题二 |      |          |          |
| 问题三 |      |          |          |
| 问题四 |      |          |          |

## 确认

<!-- 用户确认模型路线后，才能进入实现阶段。 -->
- [ ] 用户已确认模型路线
""",

    "MODELING_REPORT.md": """# 建模报告

> 待填写。此文件应在代码实现后，由 Codex 整合模型细节、公式、参数和结果生成。

## 最终模型

### 问题一：{问题一标题}

#### 模型公式
#### 参数说明
#### 求解流程
#### 关键结果

### 问题二：{问题二标题}

#### 模型公式
#### 参数说明
#### 求解流程
#### 关键结果

## 假设回收

<!-- 每个假设的验证状态 -->

## 创新点
""",

    "RESULTS.md": """# 结果说明

> 待填写。此文件应在代码运行后，记录运行命令、核心结果表、图表索引和异常说明。

## 运行环境

- Python 版本：
- 关键包版本：

## 运行命令

```bash
# 示例：数据处理
# python code/preprocess.py --input data/raw --output data/processed

# 示例：模型求解
# python code/main.py --data data/processed --output results/
```

## 结果表

### 问题一

| 指标 | 值 | 单位 |
|------|-----|------|
|      |     |      |

### 问题二

| 指标 | 值 | 单位 |
|------|-----|------|
|      |     |      |

## 图表索引

| 图表文件 | 对应章节 | 说明 |
|----------|----------|------|
| figures/fig1.png | | |
| figures/fig2.png | | |

## 异常与说明

<!-- 记录运行中的异常、缺失值处理、模拟数据标注等 -->

## 灵敏度分析结果

<!-- 参数扰动的结果表格和结论 -->
""",

    "CHECK_REPORT.md": """# 合规检查报告

> 待填写。在论文完成后运行一致性检查。

## 题目响应检查

| 小问 | 是否回答 | 对应章节 | 备注 |
|------|----------|----------|------|
| 问题一 | | | |
| 问题二 | | | |
| 问题三 | | | |

## 模型假设冲突检查

| 假设 | 题目是否允许 | 备注 |
|------|-------------|------|
|      |             |      |

## 结果一致性

| 论文中数字 | 可在 RESULTS.md 找到 | 可在代码中找到 |
|-----------|---------------------|---------------|
|           |                     |               |

## 图表引用检查

| 图表 | 正文是否引用 | 说明 |
|------|-------------|------|
|      |             |      |

## 变量/符号/单位统一性

## 灵敏度/稳健性检查

## 未声明假设检查

## 总体评价
""",
}


def file_has_content(filepath: Path) -> bool:
    """判断文件是否有用户已写内容（不只是模板占位）"""
    if not filepath.exists():
        return False
    text = filepath.read_text(encoding="utf-8", errors="ignore")
    # 如果文件包含 "待填写" 行 >= 3 条，认为是空模板
    placeholders = text.count("待填写")
    if placeholders >= 3:
        return False
    # 如果文件大于 200 字节且不是纯空白，认为有内容
    if len(text.strip()) > 200:
        return True
    return False


def init_project(
    project_dir: Path,
    competition: str = "",
    problem: str = "",
    use_latex: bool = False,
    language: str = "zh",
) -> dict:
    """初始化或补全项目目录"""
    report: dict[str, list[str]] = {
        "created_dirs": [],
        "skipped_dirs": [],
        "created_files": [],
        "skipped_files": [],
        "existing_files": [],
    }

    # 创建标准目录
    for d in STD_DIRS:
        dir_path = project_dir / d
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            report["created_dirs"].append(d)
        else:
            report["skipped_dirs"].append(d)

    # 写入 starter 文件
    paper_format = "LaTeX" if use_latex else "Markdown"
    lang_label = "中文" if language == "zh" else "English"

    for filename, template in STARTER_FILES.items():
        filepath = project_dir / filename
        if file_has_content(filepath):
            report["existing_files"].append(filename)
            continue

        content = template
        content = content.replace("{datetime}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        content = content.replace("{competition}", competition or "待指定")
        content = content.replace("{problem}", problem or "待指定")
        content = content.replace("{language}", lang_label)
        content = content.replace("{paper_format}", paper_format)
        content = content.replace("{project_dir}", str(project_dir))

        if filepath.exists():
            # 文件存在但为空或用占位符，覆盖写入
            report["skipped_files"].append(filename + "（覆盖空模板）")
        else:
            report["created_files"].append(filename)

        filepath.write_text(content, encoding="utf-8")

    # 如果使用 LaTeX，创建 paper/main.tex（简单骨架）
    if use_latex:
        latex_path = project_dir / "paper" / "main.tex"
        if not latex_path.exists():
            latex_path.parent.mkdir(parents=True, exist_ok=True)
            latex_path.write_text(r"""% 数模论文主文件
% 自动生成，请根据比赛要求调整

\documentclass[12pt,a4paper]{article}

% === 中文支持 ===
\usepackage[UTF8]{ctex}

% === 数学 ===
\usepackage{amsmath,amssymb}

% === 图形 ===
\usepackage{graphicx}
\usepackage{float}

% === 表格 ===
\usepackage{booktabs}
\usepackage{array}

% === 超链接 ===
\usepackage{hyperref}

% === 页面设置 ===
\usepackage[margin=2.5cm]{geometry}

\title{数学建模论文}
\author{队伍名称}
\date{\today}

\begin{document}

\maketitle

\begin{abstract}
请在此填写摘要。
\end{abstract}

\section{问题重述}
\section{问题分析}
\section{模型假设}
\section{符号说明}
\section{问题一的建模与求解}
\section{问题二的建模与求解}
\section{灵敏度分析与模型检验}
\section{模型评价与推广}

\begin{thebibliography}{9}
\end{thebibliography}

\section*{附录}

\end{document}
""", encoding="utf-8")
            report["created_files"].append("paper/main.tex")

    return report


def print_report(report: dict) -> None:
    """打印初始化报告"""
    print("=" * 50)
    print("项目初始化报告")
    print("=" * 50)

    if report["created_dirs"]:
        print(f"\n[OK] 已创建 {len(report['created_dirs'])} 个目录：")
        for d in report["created_dirs"]:
            print(f"   + {d}/")
    if report["skipped_dirs"]:
        print(f"\n[SKIP] 已存在 {len(report['skipped_dirs'])} 个目录：")
        for d in report["skipped_dirs"]:
            print(f"   . {d}/")
    if report["created_files"]:
        print(f"\n[OK] 已创建 {len(report['created_files'])} 个文件：")
        for f in report["created_files"]:
            print(f"   + {f}")
    if report["skipped_files"]:
        print(f"\n[REFRESH] 已刷新 {len(report['skipped_files'])} 个空模板文件：")
        for f in report["skipped_files"]:
            print(f"   * {f}")
    if report["existing_files"]:
        print(f"\n[LOCK] 已跳过 {len(report['existing_files'])} 个已有用户内容的文件：")
        for f in report["existing_files"]:
            print(f"   . {f}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="初始化数模项目",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python init_project.py D:\\projects\\cumcm-2026-A --competition 国赛 --problem A
  python init_project.py ./my-project --competition 美赛 --problem B --lang en --latex
        """,
    )
    parser.add_argument("project_dir", type=str, help="项目根目录")
    parser.add_argument("--competition", type=str, default="", help="比赛类型")
    parser.add_argument("--problem", type=str, default="", help="题号")
    parser.add_argument(
        "--latex", action="store_true", default=False, help="使用 LaTeX 模板"
    )
    parser.add_argument(
        "--lang", type=str, default="zh", choices=["zh", "en"], help="语言"
    )

    args = parser.parse_args()
    project_dir = Path(args.project_dir)

    report = init_project(
        project_dir,
        competition=args.competition,
        problem=args.problem,
        use_latex=args.latex,
        language=args.lang,
    )
    print_report(report)


if __name__ == "__main__":
    main()
