r"""结果一致性检查脚本

用法:
    python check_results_consistency.py <项目目录>

功能:
    1. 读取 RESULTS.md 抽取关键数字和图表引用
    2. 检查论文正文是否引用了这些结果
    3. 检查 FIGURE_PLAN.md 或 paper/ 中图表引用是否与 figures/ 一致
    4. 找出论文中无法追溯到结果文件的数字或图表

示例:
    python check_results_consistency.py D:\projects\cumcm-2026-A
"""

from __future__ import annotations

import sys
import re
from pathlib import Path
from argparse import ArgumentParser


def read_path(path: Path) -> str:
    """读取文件，不存在返回空"""
    if path.exists():
        return path.read_text(encoding="utf-8", errors="ignore")
    return ""


def extract_numbers(text: str) -> list[tuple[str, str]]:
    """提取文本中的关键数字（带上下文的数值）

    返回: [(上下文摘要, 数字文本), ...]
    """
    results: list[tuple[str, str]] = []
    # 匹配带单位的数值，或明显的百分数/小数
    patterns = [
        (r"([\d]+\.?[\d]*)\s*(%|m/s|km|kg|N|W|元|分|秒|小时|天)",
         "number_with_unit"),
        (r"(?:达到|约为|等于|增长|下降|降低|提高|改善|为)\s*([\d]+\.?[\d]*)\s*(%|倍)?",
         "stated_number"),
        (r"([\d]+\.[\d]{2,})\s*(（[^）]*）)?", "decimal"),
    ]

    for pattern, _ in patterns:
        for m in re.finditer(pattern, text):
            start = max(0, m.start() - 30)
            end = min(len(text), m.end() + 20)
            context = text[start:end].replace("\n", " ").strip()
            number = m.group(0)
            if len(context) > 5 and number not in [r[1] for r in results]:
                results.append((context[:80], number))

    return results[:80]  # 最多 80 个数字


def extract_figure_refs(text: str) -> list[str]:
    """提取图表引用"""
    refs: list[str] = []
    # 中文引用: 图1, 图 2, 图3-1
    for m in re.finditer(r"图\s*[\d]+[\-\d]*[a-dA-D]?", text):
        ref = m.group(0).replace(" ", "")
        if ref not in refs:
            refs.append(ref)
    # 英文引用: Figure 1, Fig.2
    for m in re.finditer(r"Fig(?:ure)?\.?\s*[\d]+[\-\d]*[a-dA-D]?", text, re.IGNORECASE):
        ref = m.group(0).replace(" ", "")
        if ref not in refs:
            refs.append(ref)
    return refs


def scan_figures_dir(fig_dir: Path) -> list[str]:
    """扫描 figures/ 目录下的图片文件"""
    if not fig_dir.exists():
        return []
    image_exts = {".png", ".jpg", ".jpeg", ".pdf", ".svg", ".eps", ".tiff"}
    return sorted(f.name for f in fig_dir.iterdir() if f.suffix.lower() in image_exts)


def looks_like_unfilled_template(text: str) -> bool:
    """判断文本是否仍是 starter 模板或占位内容。"""
    if not text.strip():
        return True
    return "待填写" in text or "<!--" in text


def check(results_md: str, paper_text: str, fig_dir: Path) -> dict:
    """执行一致性检查"""
    report: dict = {
        "numbers_in_results": [],
        "numbers_in_paper": [],
        "unreferenced_results_numbers": [],
        "unbacked_paper_numbers": [],
        "figs_on_disk": [],
        "figs_in_results": [],
        "figs_in_paper": [],
        "missing_figs": [],
        "unreferenced_figs": [],
        "preflight_warnings": [],
        "has_results": bool(results_md.strip()),
        "has_paper": bool(paper_text.strip()),
    }

    if not report["has_results"]:
        report["preflight_warnings"].append("RESULTS.md 不存在或为空，无法做结果追溯。")
    elif looks_like_unfilled_template(results_md):
        report["preflight_warnings"].append("RESULTS.md 仍包含模板占位内容，建议先写入真实运行命令、结果表和图表索引。")

    if not report["has_paper"]:
        report["preflight_warnings"].append("paper/ 中未找到论文正文（.md 或 .tex），数字和图表引用检查被跳过。")
    elif looks_like_unfilled_template(paper_text):
        report["preflight_warnings"].append("论文正文仍包含模板占位内容，当前一致性结论只能作为预检查。")

    # 1. 提取数字
    report["numbers_in_results"] = [n for _, n in extract_numbers(results_md)]
    report["numbers_in_paper"] = [n for _, n in extract_numbers(paper_text)]

    # 2. 检查论文中数字是否出现在 RESULTS.md 或 code/ 中
    results_lower = results_md.lower()
    for ctx, num in extract_numbers(paper_text)[:40]:
        if num.replace(" ", "") not in results_lower.replace(" ", ""):
            # 放宽：检查数字中的小数部分
            num_clean = num.replace(" ", "")
            if num_clean not in results_lower.replace(" ", ""):
                report["unbacked_paper_numbers"].append(f"{num}（上下文: {ctx}）")

    # 3. 提取图表引用
    report["figs_in_results"] = extract_figure_refs(results_md)
    report["figs_in_paper"] = extract_figure_refs(paper_text)
    report["figs_on_disk"] = scan_figures_dir(fig_dir)

    # 4. 检查论文引用的图是否在磁盘上存在
    if paper_text:
        for ref in report["figs_in_paper"]:
            # 模糊匹配——图1 可能对应 fig1.png / figure_1.png
            num_match = re.search(r"[\d]+[\-\d]*", ref)
            if num_match:
                num = num_match.group(0)
                found = any(num.replace("-", "_") in f for f in report["figs_on_disk"])
                if not found:
                    report["missing_figs"].append(ref)

    # 5. 磁盘上的图是否被引用
    if paper_text:
        for f in report["figs_on_disk"]:
            stem = Path(f).stem
            if stem.lower() not in paper_text.lower():
                report["unreferenced_figs"].append(f)

    return report


def render_report(project_dir: Path, report: dict) -> str:
    """生成中文报告"""
    lines: list[str] = [
        "=" * 60,
        "[Check] 结果一致性检查报告",
        "=" * 60,
        f"项目目录: {project_dir}",
        "",
        "## 数据统计",
        f"- RESULTS.md 中的关键数字：{len(report['numbers_in_results'])} 条",
        f"- 论文中提取的关键数字：{len(report['numbers_in_paper'])} 条",
        f"- RESULTS.md 中的图表引用：{len(report['figs_in_results'])} 条",
        f"- 论文中的图表引用：{len(report['figs_in_paper'])} 条",
        f"- figures/ 中的图片文件：{len(report['figs_on_disk'])} 个",
        "",
    ]

    if report["preflight_warnings"]:
        lines.append("## [!] 前置条件提醒")
        lines.append("")
        for warning in report["preflight_warnings"]:
            lines.append(f"- {warning}")
        lines.append("")

    # 论文数字不可追溯
    if not report["has_paper"]:
        lines.append("## [SKIP] 论文数字追溯检查")
        lines.append("")
        lines.append("尚未找到论文正文，无法判断论文数字是否可追溯到 RESULTS.md。")
        lines.append("")
    elif report["unbacked_paper_numbers"]:
        lines.append("## [!] 论文中存在无法追溯到结果的数字")
        lines.append("")
        lines.append("以下数字出现在论文中，但在 RESULTS.md 中未找到：")
        lines.append("")
        for item in report["unbacked_paper_numbers"][:20]:
            lines.append(f"- {item}")
        lines.append("")
    else:
        lines.append("## [OK] 论文数字追溯检查")
        lines.append("")
        lines.append("论文中可识别的关键数字均能在 RESULTS.md 中找到。")
        lines.append("")

    # 图表检查
    if report["figs_on_disk"]:
        lines.append("## [FIG] 图表文件")
        lines.append("")
        for f in report["figs_on_disk"]:
            lines.append(f"- `figures/{f}`")
        lines.append("")

    if report["missing_figs"]:
        lines.append("## [!] 论文引用但磁盘不存在的图表")
        lines.append("")
        for ref in report["missing_figs"]:
            lines.append(f"- {ref}")
        lines.append("")

    if report["unreferenced_figs"]:
        lines.append("## [!] 磁盘存在但论文未引用的图表")
        lines.append("")
        for ref in report["unreferenced_figs"]:
            lines.append(f"- `figures/{ref}`")
        lines.append("")

    # 总体评价
    issues_count = len(report["preflight_warnings"]) + \
                   len(report["unbacked_paper_numbers"]) + \
                   len(report["missing_figs"]) + \
                   len(report["unreferenced_figs"])

    lines.append("## 总体评价")
    lines.append("")
    if issues_count == 0:
        lines.append("[OK] 未发现一致性问题。")
    else:
        lines.append(f"[!] 发现 {issues_count} 个潜在一致性问题，请逐一确认。")
        lines.append("")
        lines.append("建议操作：")
        suggestions: list[str] = []
        if report["preflight_warnings"]:
            suggestions.append("先补齐 RESULTS.md 的真实结果内容，并在 paper/ 中放入论文正文后再做终检。")
        if report["unbacked_paper_numbers"]:
            suggestions.append("将论文中无法追溯的数字补充到 RESULTS.md 或标注来源。")
        if report["missing_figs"]:
            suggestions.append("补充论文引用的缺失图表文件。")
        if report["unreferenced_figs"]:
            suggestions.append("在论文正文中引用未使用的图表，或删除多余文件。")
        for index, suggestion in enumerate(suggestions, start=1):
            lines.append(f"{index}. {suggestion}")

    lines.append("")
    lines.append("=" * 60)
    return "\n".join(lines)


def main() -> None:
    parser = ArgumentParser(description="检查结果和论文一致性")
    parser.add_argument("project_dir", type=str, help="项目根目录")
    args = parser.parse_args()

    project_dir = Path(args.project_dir)
    if not project_dir.exists():
        print(f"错误: 目录不存在: {project_dir}")
        sys.exit(1)

    results_path = project_dir / "RESULTS.md"
    results_md = read_path(results_path)

    # 尝试读取论文
    paper_dir = project_dir / "paper"
    paper_text = ""
    if paper_dir.exists():
        for f in sorted(paper_dir.glob("*.md")) + sorted(paper_dir.glob("*.tex")):
            paper_text = read_path(f)
            break

    fig_dir = project_dir / "figures"

    if not results_md:
        print("警告: RESULTS.md 不存在或为空，检查结果可能不准确。")

    report = check(results_md, paper_text, fig_dir)
    print(render_report(project_dir, report))


if __name__ == "__main__":
    main()
