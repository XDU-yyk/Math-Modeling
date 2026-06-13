"""Extract lightweight evidence from all example math-modeling PDFs.

This is a local analysis helper for designing the workflow outline. It avoids
network calls and uses only pypdf text extraction, so the output is evidence to
review rather than polished paper metadata.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from pypdf import PdfReader


EXAMPLES_DIR = Path(__file__).resolve().parent.parent
PAPERS_DIR = EXAMPLES_DIR / "papers"
KNOWLEDGE_DIR = EXAMPLES_DIR / "knowledge"
PER_PAPER_DIR = KNOWLEDGE_DIR / "per-paper"
TEXT_DIR = KNOWLEDGE_DIR / "extracted-text"
SUMMARY_PATH = KNOWLEDGE_DIR / "paper-extraction-summary.json"

METHOD_TERMS = [
    "层次分析",
    "AHP",
    "熵权",
    "TOPSIS",
    "灰色关联",
    "主成分",
    "PCA",
    "聚类",
    "K-means",
    "K均值",
    "回归",
    "线性回归",
    "Logistic",
    "随机森林",
    "XGBoost",
    "SVM",
    "支持向量机",
    "ARIMA",
    "LSTM",
    "神经网络",
    "深度学习",
    "Transformer",
    "图神经网络",
    "GNN",
    "时空图",
    "优化",
    "线性规划",
    "整数规划",
    "非线性规划",
    "多目标",
    "遗传算法",
    "粒子群",
    "模拟退火",
    "蒙特卡洛",
    "微分方程",
    "差分方程",
    "元胞自动机",
    "排队论",
    "马尔可夫",
    "时间序列",
    "预测",
    "评价",
    "仿真",
    "灵敏度",
    "敏感性",
    "误差分析",
    "残差",
    "稳健性",
    "相关性",
    "显著性",
    "可视化",
    "热力图",
    "GIS",
    "物理模型",
    "数值模拟",
    "动力学",
    "规划",
    "回归模型",
    "评价模型",
]

CHAPTER_WORDS = [
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

CN_NUMS = tuple("一二三四五六七八九十")


def normalize_text(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def looks_like_heading(line: str) -> bool:
    text = re.sub(r"\s+", " ", line.strip())
    if not text or len(text) > 80:
        return False
    if any(word in text for word in CHAPTER_WORDS):
        return True
    if text[:1] in CN_NUMS and len(text) >= 2 and text[1] in "、．. ":
        return True
    if re.match(r"^[0-9]+([.．][0-9]+){0,3}[、.． ]+\S+", text):
        return True
    if text.startswith("第") and ("章" in text[:8] or "节" in text[:8]):
        return True
    return False


def find_between_markers(text: str, start_words: list[str], end_words: list[str], limit: int) -> str:
    head = text[:limit]
    starts = [head.find(word) for word in start_words if head.find(word) >= 0]
    if not starts:
        return ""
    start = min(starts)
    start_word_len = max(len(word) for word in start_words if head.startswith(word, start))
    body_start = start + start_word_len
    end_candidates = [head.find(word, body_start) for word in end_words if head.find(word, body_start) >= 0]
    end = min(end_candidates) if end_candidates else min(len(head), body_start + 1400)
    return re.sub(r"\s+", " ", head[body_start:end]).strip()


def extract_pdf_text(pdf_path: Path) -> tuple[list[str], list[str]]:
    pages: list[str] = []
    errors: list[str] = []
    try:
        reader = PdfReader(str(pdf_path))
    except Exception as exc:  # noqa: BLE001 - collect extraction evidence.
        return [], [f"reader: {type(exc).__name__}: {exc}"]

    for index, page in enumerate(reader.pages, 1):
        try:
            pages.append(page.extract_text() or "")
        except Exception as exc:  # noqa: BLE001
            pages.append("")
            errors.append(f"page {index}: {type(exc).__name__}: {exc}")
    return pages, errors


def analyze_pdf(index: int, pdf_path: Path) -> dict:
    pages, errors = extract_pdf_text(pdf_path)
    text = normalize_text("\n".join(pages))

    headings: list[str] = []
    for line in (line.strip() for line in text.splitlines() if line.strip()):
        simple = re.sub(r"\s+", " ", line)
        if looks_like_heading(simple) and simple not in headings:
            headings.append(simple)
        if len(headings) >= 80:
            break

    lower = text.lower()
    term_counts = {
        term: lower.count(term.lower())
        for term in METHOD_TERMS
        if lower.count(term.lower())
    }
    term_counts = dict(sorted(term_counts.items(), key=lambda item: (-item[1], item[0]))[:35])

    abstract = find_between_markers(
        text,
        ["摘要", "摘 要"],
        ["关键词", "关键字", "Key words", "Keywords", "目录", "一、", "1."],
        18000,
    )
    keywords_line = find_between_markers(
        text,
        ["关键词", "关键字"],
        ["Abstract", "一、", "1.", "\n\n"],
        18000,
    )

    text_name = f"{index:02d}-{hashlib.md5(pdf_path.name.encode('utf-8')).hexdigest()[:8]}.txt"
    (TEXT_DIR / text_name).write_text(text, encoding="utf-8", errors="ignore")

    first_pages = normalize_text("\n\n".join(pages[:3])).strip()
    record = {
        "index": index,
        "file": pdf_path.name,
        "size": pdf_path.stat().st_size,
        "pages": len(pages),
        "chars": len(text),
        "extract_errors": errors,
        "abstract": abstract[:1600],
        "keywords_line": keywords_line[:700],
        "method_terms": term_counts,
        "headings": headings,
        "text_cache": f"extracted-text/{text_name}",
        "first_pages_excerpt": first_pages[:1200],
    }

    safe_stem = re.sub(r'[<>:"/\\|?*]+', "_", pdf_path.stem)[:50]
    per_path = PER_PAPER_DIR / f"{index:02d}-{safe_stem}.md"
    per_path.write_text(render_per_paper(record, first_pages), encoding="utf-8", errors="ignore")
    record["per_paper"] = f"per-paper/{per_path.name}"
    return record


def render_per_paper(record: dict, first_pages: str) -> str:
    lines: list[str] = [
        f"# {record['index']:02d} - {record['file']}",
        "",
        "> 自动抽取草稿：由 pypdf 文本层生成，需人工复核。",
        "",
        "## 元数据",
        f"- 原始文件：`{record['file']}`",
        f"- 页数：{record['pages']}",
        f"- 可抽取字符数：{record['chars']}",
        f"- 文本缓存：`{record['text_cache']}`",
    ]
    if record["extract_errors"]:
        lines.append(f"- 抽取错误：{len(record['extract_errors'])} 条")

    lines.extend(["", "## 摘要线索", record["abstract"] or "未能稳定识别摘要，请查看文本缓存。"])
    lines.extend(["", "## 关键词线索", record["keywords_line"] or "未能稳定识别关键词。"])
    lines.extend(["", "## 方法关键词统计"])
    if record["method_terms"]:
        lines.extend(f"- {key}: {value}" for key, value in record["method_terms"].items())
    else:
        lines.append("未命中预设方法关键词。")

    lines.extend(["", "## 标题/结构线索"])
    if record["headings"]:
        lines.extend(f"- {heading}" for heading in record["headings"][:50])
    else:
        lines.append("未能稳定识别标题。")

    lines.extend(["", "## 前三页片段", "```text", first_pages[:3800], "```"])
    return "\n".join(lines)


def main() -> None:
    PER_PAPER_DIR.mkdir(parents=True, exist_ok=True)
    TEXT_DIR.mkdir(parents=True, exist_ok=True)

    records = [
        analyze_pdf(index, pdf_path)
        for index, pdf_path in enumerate(sorted(PAPERS_DIR.glob("*.pdf")), 1)
    ]
    summary = {
        "paper_count": len(records),
        "total_pages": sum(record["pages"] for record in records),
        "total_chars": sum(record["chars"] for record in records),
        "papers": records,
    }
    SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"paper_count={summary['paper_count']}")
    print(f"total_pages={summary['total_pages']}")
    print(f"total_chars={summary['total_chars']}")
    for record in records:
        terms = ", ".join(list(record["method_terms"].keys())[:8])
        print(
            f"{record['index']:02d}\tpages={record['pages']}\tchars={record['chars']}"
            f"\tterms={terms}\tfile={record['file']}"
        )


if __name__ == "__main__":
    main()
