r"""单篇论文知识提取脚本

用法:
    python extract_paper.py <paper_pdf_or_dir>

参数:
    paper_pdf_or_dir 可以是:
    - examples/papers/ 下的 PDF 文件名，例如 "五一杯A题参考论文.pdf"
    - examples/papers/ 下的子目录名，目录中应包含 PDF
    - PDF 文件或目录的绝对/相对路径

功能:
    1. 使用 pypdf 读取 PDF 文本层
    2. 生成 examples/knowledge/per-paper/{index}-{stem}.md 草稿
    3. 更新 examples/knowledge/paper-extraction-summary.json 中对应记录

说明:
    本脚本不调用网络或大模型 API。它生成的是本地抽取草稿，适合先打通
    端到端工作流；重要论文仍建议后续用人工或模型做二次结构化复核。
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from analyze_papers_local import PAPERS_DIR, SUMMARY_PATH, analyze_pdf


def resolve_target(arg: str) -> Path:
    """解析用户传入的 PDF 文件或目录。"""
    raw = Path(arg)
    candidates = [
        raw,
        PAPERS_DIR / arg,
    ]
    if raw.suffix.lower() != ".pdf":
        candidates.append(PAPERS_DIR / f"{arg}.pdf")

    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()

    raise FileNotFoundError(f"未找到论文文件或目录: {arg}")


def choose_pdf(target: Path) -> Path:
    """从文件或目录中选择要抽取的 PDF。"""
    if target.is_file():
        if target.suffix.lower() != ".pdf":
            raise ValueError(f"目标不是 PDF 文件: {target}")
        return target

    preferred = sorted(target.glob("*论文*.pdf"))
    all_pdfs = sorted(target.glob("*.pdf"))
    pdfs = preferred or all_pdfs
    if not pdfs:
        raise FileNotFoundError(f"目录中未找到 PDF 文件: {target}")
    return pdfs[0].resolve()


def safe_stem(pdf_path: Path) -> str:
    return re.sub(r'[<>:"/\\|?*]+', "_", pdf_path.stem)[:50]


def load_summary() -> dict:
    if SUMMARY_PATH.exists():
        return json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
    return {"paper_count": 0, "total_pages": 0, "total_chars": 0, "papers": []}


def index_for_pdf(pdf_path: Path, records: list[dict]) -> int:
    """尽量沿用全量抽取时的稳定编号。"""
    for record in records:
        if record.get("file") == pdf_path.name:
            return int(record["index"])

    for index, candidate in enumerate(sorted(PAPERS_DIR.glob("*.pdf")), 1):
        if candidate.resolve() == pdf_path.resolve():
            return index

    used = [int(record["index"]) for record in records if str(record.get("index", "")).isdigit()]
    return (max(used) if used else 0) + 1


def save_summary(summary: dict, record: dict) -> None:
    records = [
        existing
        for existing in summary.get("papers", [])
        if existing.get("file") != record["file"]
    ]
    records.append(record)
    records.sort(key=lambda item: int(item.get("index", 999999)))

    summary["papers"] = records
    summary["paper_count"] = len(records)
    summary["total_pages"] = sum(int(item.get("pages", 0)) for item in records)
    summary["total_chars"] = sum(int(item.get("chars", 0)) for item in records)

    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    if len(sys.argv) < 2:
        print("用法: python extract_paper.py <paper_pdf_or_dir>")
        print("示例: python extract_paper.py 五一杯A题参考论文.pdf")
        sys.exit(1)

    try:
        target = resolve_target(sys.argv[1])
        pdf_path = choose_pdf(target)
        summary = load_summary()
        index = index_for_pdf(pdf_path, summary.get("papers", []))

        print(f"[1/3] 抽取 PDF 文本层: {pdf_path.name}")
        record = analyze_pdf(index, pdf_path)

        expected_md = f"{index:02d}-{safe_stem(pdf_path)}.md"
        print(f"[2/3] 写入 per-paper 草稿: {expected_md}")

        save_summary(summary, record)
        print(f"[3/3] 更新汇总: {SUMMARY_PATH}")
        print(
            f"完成: pages={record['pages']}, chars={record['chars']}, "
            f"errors={len(record['extract_errors'])}"
        )
    except Exception as exc:  # noqa: BLE001 - CLI should print friendly failure.
        print(f"错误: {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
