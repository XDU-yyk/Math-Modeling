r"""跨论文知识聚合脚本

用法:
    python build_knowledge.py

功能:
    1. 读取 paper-extraction-summary.json 和 per-paper 文件。
    2. 按题型/方法标签分组，生成跨论文汇总数据。
    3. 更新 cross-paper/*.md 文件的自动生成部分，保留已有的人工撰述。

策略:
    - 如果 cross-paper 文件已经包含 # AUTO-GENERATED 标记，则只替换标记之间的内容。
    - 如果没有标记，则在文件末尾追加自动生成内容。
    - 不会删除或覆盖 Codex 已生成的固定内容。
"""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path
from datetime import datetime


EXAMPLES_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = EXAMPLES_DIR / "knowledge"
SUMMARY_PATH = KNOWLEDGE_DIR / "paper-extraction-summary.json"
CROSS_PAPER_DIR = KNOWLEDGE_DIR / "cross-paper"


def load_papers() -> list[dict]:
    if not SUMMARY_PATH.exists():
        raise FileNotFoundError(f"未找到 {SUMMARY_PATH}，请先运行 analyze_papers_local.py")
    data = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
    return data["papers"]


# ---- 各 cross-paper 文件的自动生成逻辑 ----


def build_auto_modeling_methods(papers: list[dict]) -> str:
    """生成 modeling-methods-from-examples.md 的自动更新部分"""
    lines = [
        f"<!-- AUTO-GENERATED {datetime.now().strftime('%Y-%m-%d %H:%M')} -->",
        "",
        "## 各论文方法一览（自动更新）",
        "",
        "| # | 文件 | 页数 | 高频方法（前8） |",
        "|---|------|------|----------------|",
    ]
    for p in papers:
        terms = p.get("method_terms", {})
        sorted_terms = sorted(terms.items(), key=lambda x: (-x[1], x[0]))
        top = "、".join(t for t, _ in sorted_terms[:8])
        file_short = p["file"].replace("|", "\\|")
        lines.append(f"| {p['index']:02d} | {file_short} | {p['pages']} | {top} |")

    # 方法总频统计
    method_counter: collections.Counter[str] = collections.Counter()
    for p in papers:
        method_counter.update(p.get("method_terms", {}))
    
    lines.extend([
        "",
        "## 方法总频排名（自动更新）",
        "",
        "| 方法词 | 总命中次数 |",
        "| --- | ---: |",
    ])
    for term, count in method_counter.most_common(40):
        lines.append(f"| {term} | {count} |")

    return "\n".join(lines)


def build_auto_paper_structures(papers: list[dict]) -> str:
    """生成 paper-structures-from-examples.md 的自动更新部分"""
    lines = [
        f"<!-- AUTO-GENERATED {datetime.now().strftime('%Y-%m-%d %H:%M')} -->",
        "",
        "## 各论文结构信号（自动更新）",
        "",
        "| # | 文件 | 检测到的章节信号 |",
        "|---|------|-----------------|",
    ]
    for p in papers:
        headings = p.get("headings", [])
        # 只取有意义的章节线索
        chapter_signals = [h for h in headings if any(
            kw in h for kw in ["问题", "模型", "摘要", "假设", "符号", "分析", "求解", "灵敏度", "评价", "推广", "参考", "附录"]
        )][:6]
        sig = "  →  ".join(chapter_signals) if chapter_signals else "未检测到"
        file_short = p["file"].replace("|", "\\|")
        lines.append(f"| {p['index']:02d} | {file_short} | {sig} |")

    # 章节信号统计
    section_counter: collections.Counter[str] = collections.Counter()
    section_keys = ["问题重述", "问题分析", "模型假设", "符号说明", "模型建立", "模型求解", "结果分析", "灵敏度", "敏感性", "误差分析", "模型评价", "模型推广", "参考文献", "附录", "摘要", "关键词"]
    for p in papers:
        for heading in p.get("headings", []):
            for key in section_keys:
                if key in heading:
                    section_counter[key] += 1

    lines.extend([
        "",
        "## 章节信号频次（自动更新）",
        "",
        "| 章节信号 | 命中论文数 |",
        "| --- | ---: |",
    ])
    for term, count in section_counter.most_common():
        if count >= len(papers) * 0.1:  # 至少 10% 的论文命中才显示
            lines.append(f"| {term} | {count} |")

    return "\n".join(lines)


def build_auto_result_presentation(papers: list[dict]) -> str:
    """生成 result-presentation-from-examples.md 的自动更新部分"""
    chars = sum(p["chars"] for p in papers)
    pages = sum(p["pages"] for p in papers)
    
    return "\n".join([
        f"<!-- AUTO-GENERATED {datetime.now().strftime('%Y-%m-%d %H:%M')} -->",
        "",
        "## 数据集概览（自动更新）",
        "",
        f"- 论文总数：{len(papers)}",
        f"- 总页数：{pages}",
        f"- 总字符数：{chars}",
        f"- 平均页数：{pages / len(papers):.1f}",
        f"- 平均字符数：{chars / len(papers):.0f}",
        f"- 页数范围：{min(p['pages'] for p in papers)}–{max(p['pages'] for p in papers)}",
    ])


def build_auto_common_patterns(papers: list[dict]) -> str:
    """生成 common-patterns-from-examples.md 的自动更新部分"""
    # 统计每个论文的摘要片段
    abstracts_found = sum(1 for p in papers if p.get("abstract") and len(p["abstract"]) > 50)
    keywords_found = sum(1 for p in papers if p.get("keywords_line") and len(p["keywords_line"]) > 5)

    return "\n".join([
        f"<!-- AUTO-GENERATED {datetime.now().strftime('%Y-%m-%d %H:%M')} -->",
        "",
        "## 数据质量（自动更新）",
        "",
        f"- 成功抽取摘要的论文：{abstracts_found}/{len(papers)}",
        f"- 成功抽取关键词的论文：{keywords_found}/{len(papers)}",
        f"- 数据来源：pypdf 文本层抽取（非 OCR），中文精度有限",
        f"- 建议：对关键论文使用 marker 或 GPT 做高精度二次提取",
    ])


def merge_auto_content(file_path: Path, auto_content: str) -> str:
    """将自动生成内容合并到已有文件"""
    if not file_path.exists():
        return auto_content

    existing = file_path.read_text(encoding="utf-8")

    # 查找现有 AUTO-GENERATED 块
    start_marker = "<!-- AUTO-GENERATED"
    lines = existing.splitlines()
    start_idx = None
    end_idx = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith(start_marker) and start_idx is None:
            start_idx = i
        elif stripped.startswith(start_marker) and start_idx is not None:
            # 新的标记可能表示多个 auto 块，取最近的一个
            start_idx = i

    if start_idx is not None:
        # 找到标记，替换标记之后直到文件末尾或下一个手动标记之间的内容
        # 简单策略：从 AUTO-GENERATED 标记后的 "##" 开始替换到文件末尾的 auto 内容
        # 更安全的方式：保留标记前的所有内容，替换标记后的 ## 头及其以下
        before = "\n".join(lines[:start_idx])
        return before.strip() + "\n\n" + auto_content + "\n"
    else:
        # 没有标记，追加在末尾
        return existing.rstrip() + "\n\n" + auto_content + "\n"


def main() -> None:
    print("加载论文数据...")
    papers = load_papers()
    print(f"共 {len(papers)} 篇论文")

    CROSS_PAPER_DIR.mkdir(parents=True, exist_ok=True)

    builders = {
        "modeling-methods-from-examples.md": build_auto_modeling_methods,
        "paper-structures-from-examples.md": build_auto_paper_structures,
        "result-presentation-from-examples.md": build_auto_result_presentation,
        "common-patterns-from-examples.md": build_auto_common_patterns,
    }

    for filename, builder_fn in builders.items():
        file_path = CROSS_PAPER_DIR / filename
        print(f"更新 {filename}...")
        auto_content = builder_fn(papers)
        merged = merge_auto_content(file_path, auto_content)
        file_path.write_text(merged, encoding="utf-8")

    print("全部完成！")


if __name__ == "__main__":
    main()
