"""Summarize extracted paper evidence for workflow design."""

from __future__ import annotations

import collections
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SUMMARY_PATH = ROOT / "knowledge" / "paper-extraction-summary.json"
OUTPUT_PATH = ROOT / "knowledge" / "extraction-evidence-summary.md"

SECTION_KEYS = [
    "摘要",
    "关键词",
    "问题重述",
    "问题分析",
    "模型假设",
    "符号说明",
    "模型建立",
    "模型求解",
    "结果分析",
    "灵敏度",
    "敏感性",
    "误差分析",
    "模型评价",
    "模型推广",
    "参考文献",
    "附录",
]


def main() -> None:
    data = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
    method_counter: collections.Counter[str] = collections.Counter()
    section_counter: collections.Counter[str] = collections.Counter()

    for paper in data["papers"]:
        method_counter.update(paper.get("method_terms", {}))
        headings = paper.get("headings", [])
        for heading in headings:
            for key in SECTION_KEYS:
                if key in heading:
                    section_counter[key] += 1

    lines: list[str] = [
        "# 论文抽取证据汇总",
        "",
        f"- 论文数：{data['paper_count']}",
        f"- 总页数：{data['total_pages']}",
        f"- 可抽取字符数：{data['total_chars']}",
        "",
        "## 高频方法词",
        "",
        "| 方法词 | 命中次数 |",
        "| --- | ---: |",
    ]
    for term, count in method_counter.most_common(50):
        lines.append(f"| {term} | {count} |")

    lines.extend([
        "",
        "## 高频结构词",
        "",
        "| 结构词 | 命中次数 |",
        "| --- | ---: |",
    ])
    for term, count in section_counter.most_common():
        lines.append(f"| {term} | {count} |")

    lines.extend([
        "",
        "## 单篇线索表",
        "",
        "| # | 页数 | 文件 | 高频方法 | 前部结构线索 |",
        "| --- | ---: | --- | --- | --- |",
    ])
    for paper in data["papers"]:
        methods = "、".join(list(paper.get("method_terms", {}).keys())[:8])
        headings = "；".join(paper.get("headings", [])[:8])
        file_name = paper["file"].replace("|", "\\|")
        lines.append(f"| {paper['index']:02d} | {paper['pages']} | {file_name} | {methods} | {headings} |")

    OUTPUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()
