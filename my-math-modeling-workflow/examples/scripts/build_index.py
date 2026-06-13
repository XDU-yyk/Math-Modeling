r"""论文索引生成脚本

用法:
    python build_index.py

功能:
    1. 读取 examples/knowledge/paper-extraction-summary.json
    2. 从每个 per-paper 提取和文件名中解析比赛、年份、题号、核心模型、方法标签
    3. 生成/更新 examples/knowledge/papers-index.md
"""

from __future__ import annotations

import json
import re
from pathlib import Path


EXAMPLES_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = EXAMPLES_DIR / "knowledge"
SUMMARY_PATH = KNOWLEDGE_DIR / "paper-extraction-summary.json"
INDEX_PATH = KNOWLEDGE_DIR / "papers-index.md"

# 比赛名称关键词映射
COMPETITION_PATTERNS: list[tuple[str, str]] = [
    ("长三角", "长三角高校数学建模竞赛"),
    ("中青杯", "中青杯"),
    ("五一杯", "五一杯"),
    ("华中杯", "华中杯"),
    ("华东", "华东杯"),
    ("电工杯", "电工杯"),
    ("数维杯", "数维杯"),
    ("认证杯", "认证杯"),
    ("江西省研究生", "江西省研究生数学建模"),
    ("MathorCup", "MathorCup"),
    ("国赛", "全国大学生数学建模竞赛"),
]

PROBLEM_PATTERNS: list[tuple[str, str]] = [
    ("A题", "A"), ("B题", "B"), ("C题", "C"), ("D题", "D"),
    ("二阶段A", "A"), ("二阶段B", "B"), ("二阶段C", "C"),
    ("第二阶段D", "D"), ("第二阶段A", "A"), ("第二阶段B", "B"),
    ("第二阶段C", "C"), ("第二阶段D", "D"),
    ("一阶段", ""), 
]

# 从文件名解析元数据
def parse_paper_meta(paper: dict) -> dict:
    """从文件名和抽取数据中解析比赛、年份、题号"""
    file_name = paper["file"]
    index = paper["index"]

    # 尝试从文件名字面量解析比赛
    competition = ""
    for pattern, name in COMPETITION_PATTERNS:
        if pattern in file_name:
            competition = name
            break
    if not competition and "算网" in file_name:
        competition = "其他 / 专题研究"
    if not competition:
        competition = "待确认"

    # 解析年份
    year = ""
    year_match = re.search(r"20\d{2}", file_name)
    if year_match:
        year = year_match.group(0)

    # 解析题号
    problem = ""
    for pattern, label in PROBLEM_PATTERNS:
        if pattern in file_name:
            problem = label
            break

    # 核心模型
    terms = paper.get("method_terms", {})
    sorted_terms = sorted(terms.items(), key=lambda x: (-x[1], x[0]))
    top_methods = [t for t, _ in sorted_terms[:5]]
    core_models = "、".join(top_methods)

    # 方法标签
    all_terms = [t for t, _ in sorted_terms[:8]]
    method_tags = "、".join(all_terms)

    # 题目关键词（从文件名字面量提取）
    topic_keywords = file_name.replace(".pdf", "")
    # 去掉比赛名
    for pat, _ in COMPETITION_PATTERNS:
        topic_keywords = topic_keywords.replace(pat, "")
    topic_keywords = re.sub(r"20\d{2}", "", topic_keywords)
    topic_keywords = re.sub(r"[（(].*?[）)]", "", topic_keywords)
    topic_keywords = re.sub(r"[-_]", " ", topic_keywords)
    topic_keywords = " ".join(topic_keywords.split()[:6])

    return {
        "index": index,
        "file": file_name,
        "per_paper": paper.get("per_paper", ""),
        "competition": competition,
        "year": year,
        "problem": problem,
        "topic_keywords": topic_keywords,
        "core_models": core_models,
        "method_tags": method_tags,
        "pages": paper["pages"],
    }


def generate_index_md(metas: list[dict]) -> str:
    """生成 papers-index.md"""
    lines: list[str] = [
        "# 历史论文索引",
        "",
        "> 由 `scripts/build_index.py` 自动生成。",
        "> 如需修正信息，请修改文件名后重新运行脚本。",
        "",
        "| # | 比赛 | 年份 | 题号 | 题目关键词 | 页数 | 核心模型 | 方法标签 | 文件位置 |",
        "|---|------|------|------|-----------|------|----------|----------|----------|",
    ]

    for m in metas:
        idx = f"{m['index']:02d}"
        comp = m["competition"]
        year = m["year"] or "-"
        prob = m["problem"] or "-"
        keywords = m["topic_keywords"] or "-"
        pages = str(m["pages"])
        models = m["core_models"] or "-"
        tags = m["method_tags"] or "-"
        loc = m["per_paper"] or f"per-paper/{m['index']:02d}-{Path(m['file']).stem[:40]}.md"
        lines.append(f"| {idx} | {comp} | {year} | {prob} | {keywords} | {pages} | {models} | {tags} | {loc} |")

    lines.extend([
        "",
        "## 方法标签说明",
        "",
        "方法标签从论文正文中按关键词命中频率自动提取，仅反映论文中的词频，不一定是论文的核心方法。",
        "人工复核后可以调整 per-paper 文件中的元数据。",
    ])
    return "\n".join(lines) + "\n"


def main() -> None:
    if not SUMMARY_PATH.exists():
        print(f"错误: 未找到 {SUMMARY_PATH}")
        print("请先运行 analyze_papers_local.py 生成抽取数据")
        return

    data = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
    print(f"加载 {data['paper_count']} 篇论文数据")

    metas = [parse_paper_meta(paper) for paper in data["papers"]]

    index_md = generate_index_md(metas)
    INDEX_PATH.write_text(index_md, encoding="utf-8")

    print(f"已写入 {INDEX_PATH}")
    print(f"共 {len(metas)} 条索引")

    # 简要统计
    comps = set(m["competition"] for m in metas)
    print(f"覆盖比赛: {', '.join(sorted(comps))}")


if __name__ == "__main__":
    main()
