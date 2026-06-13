r"""产物检查脚本

用法:
    python check_artifacts.py <项目目录>

功能:
    1. 检查标准产物是否存在
    2. 检查关键文件是否为空、章节是否不完整
    3. 判断当前完成到哪个阶段
    4. 输出中文检查报告

示例:
    python check_artifacts.py D:\projects\cumcm-2026-A
    python check_artifacts.py ./my-project
"""

from __future__ import annotations

import sys
import re
from pathlib import Path
from argparse import ArgumentParser


# 阶段定义与对应产物
STAGES = {
    0: {"name": "项目建档", "files": ["PROJECT_BRIEF.md"]},
    1: {"name": "赛题分析", "files": ["PROBLEM_ANALYSIS.md"]},
    2: {"name": "建模路线", "files": ["MODELING_PLAN.md"]},
    3: {"name": "实现任务拆分", "files": ["IMPLEMENTATION_TASKS.md"]},
    4: {"name": "代码与结果", "files": ["code/", "RESULTS.md"]},
    5: {"name": "图表与可视化", "files": ["figures/", "FIGURE_PLAN.md"]},
    6: {"name": "论文写作", "files": ["paper/"]},
    7: {"name": "合规检查", "files": ["CHECK_REPORT.md"]},
}

# 每个文件的章节检查（至少应出现的标题）
REQUIRED_SECTIONS: dict[str, list[str]] = {
    "PROJECT_BRIEF.md": ["比赛类型", "题目", "数据"],
    "PROBLEM_ANALYSIS.md": ["背景", "问题", "符号"],
    "MODELING_PLAN.md": ["候选", "模型", "路线"],
    "MODELING_REPORT.md": ["模型", "结果", "假设"],
    "RESULTS.md": ["运行", "结果", "图表"],
    "CHECK_REPORT.md": ["检查", "一致"],
    "IMPLEMENTATION_TASKS.md": ["实现", "任务"],
}


def file_exists_and_not_empty(project_dir: Path, filename: str) -> bool:
    """检查文件是否存在且非空（且非纯占位符模板）"""
    path = project_dir / filename
    if not path.exists():
        return False
    try:
        text = path.read_text(encoding="utf-8", errors="ignore").strip()
        return len(text) >= 50
    except Exception:
        return False


def looks_like_unfilled_template(text: str) -> bool:
    """判断文件是否仍主要是初始化模板。"""
    if "待填写" in text or "<!--" in text:
        return True

    empty_field_pattern = re.compile(
        r"^\s*-\s*(目标|输入|输出|约束|评价指标|Python 版本|关键包版本)[：:]\s*$",
        re.MULTILINE,
    )
    if empty_field_pattern.search(text):
        return True

    empty_table_pattern = re.compile(r"\|\s*\|\s*\|")
    return bool(empty_table_pattern.search(text))


def file_ready_for_stage(project_dir: Path, filename: str, stage_id: int) -> bool:
    """检查阶段产物是否已经从 starter 模板推进到可验收内容。"""
    path = project_dir / filename
    if not file_exists_and_not_empty(project_dir, filename):
        return False

    if stage_id == 0 and filename == "PROJECT_BRIEF.md":
        return True

    text = path.read_text(encoding="utf-8", errors="ignore")
    return not looks_like_unfilled_template(text)


def dir_exists_and_not_empty(project_dir: Path, dirname: str) -> bool:
    """检查目录是否存在且至少有一个文件"""
    path = project_dir / dirname
    if not path.exists() or not path.is_dir():
        return False
    return any(path.iterdir())


def check_file_sections(project_dir: Path, filename: str) -> list[str]:
    """检查文件的必要章节"""
    path = project_dir / filename
    if not path.exists():
        return [f"{filename} 不存在"]

    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return [f"{filename} 无法读取"]

    issues: list[str] = []

    # 检查是否基本为空（多空行或全占位符）
    meaningful = [l for l in text.splitlines() if l.strip() and not l.strip().startswith(">")]
    if len(meaningful) < 5:
        issues.append(f"{filename} 内容过少（仅 {len(meaningful)} 行有意义内容）")
        return issues

    # 检查"待填写"占位符密度
    placeholder_count = text.count("待填写")
    if placeholder_count >= 5:
        issues.append(f'{filename} 含 {placeholder_count} 处待填写，疑似未填写')

    # 检查必要章节
    req = REQUIRED_SECTIONS.get(filename, [])
    for keyword in req:
        if keyword not in text:
            issues.append(f'{filename} 缺少章节关键词: "{keyword}"')

    return issues


def determine_stage(project_dir: Path) -> dict:
    """判断当前阶段"""
    results: dict = {
        "current_stage": 0,
        "stage_name": "项目建档",
        "stage_status": {},
        "missing_files": [],
        "all_issues": [],
    }

    # 按顺序检查每个阶段
    for stage_id in range(8):
        stage = STAGES[stage_id]
        stage_ok = True
        stage_files = stage["files"]

        for f in stage_files:
            if f.endswith("/"):
                exists = dir_exists_and_not_empty(project_dir, f)
            else:
                exists = file_ready_for_stage(project_dir, f, stage_id)

            if not exists:
                stage_ok = False
                if f not in results["missing_files"]:
                    results["missing_files"].append(f)

        results["stage_status"][stage_id] = stage_ok

    # 当前阶段按“从 0 开始连续完成”判定，避免后置模板文件误抬阶段。
    current_stage = -1
    for stage_id in range(8):
        if not results["stage_status"].get(stage_id):
            break
        current_stage = stage_id

    if current_stage >= 0:
        results["current_stage"] = current_stage
        results["stage_name"] = STAGES[current_stage]["name"]
    else:
        results["current_stage"] = -1
        results["stage_name"] = "未完成项目建档"

    # 检查已存在文件的章节
    for stage_id in range(results["current_stage"] + 1):
        for f in STAGES[stage_id]["files"]:
            if not f.endswith("/") and file_exists_and_not_empty(project_dir, f):
                issues = check_file_sections(project_dir, f)
                results["all_issues"].extend(issues)

    return results


def check_code_files(project_dir: Path) -> list[str]:
    """检查 code/ 目录"""
    issues: list[str] = []
    code_dir = project_dir / "code"
    if not code_dir.exists() or not code_dir.is_dir():
        issues.append("code/ 目录不存在")
        return issues

    py_files = list(code_dir.glob("*.py"))
    if not py_files:
        issues.append("code/ 中没有 .py 文件")
    else:
        # 检查是否有主入口
        main_candidates = ["main.py", "run.py", "solve.py", "start.py"]
        has_main = any((code_dir / m).exists() for m in main_candidates)
        if not has_main:
            issues.append("code/ 中未找到主入口文件（main.py / run.py）")

    return issues


def check_figures(project_dir: Path) -> list[str]:
    """检查 figures/ 目录"""
    issues: list[str] = []
    fig_dir = project_dir / "figures"
    if not fig_dir.exists() or not fig_dir.is_dir():
        issues.append("figures/ 目录不存在")
        return issues

    image_files = list(fig_dir.glob("*.png")) + list(fig_dir.glob("*.jpg")) + \
                   list(fig_dir.glob("*.pdf")) + list(fig_dir.glob("*.svg"))
    if not image_files:
        issues.append("figures/ 中没有图片文件")

    return issues


def check_paper(project_dir: Path) -> list[str]:
    """检查 paper/ 目录"""
    issues: list[str] = []
    paper_dir = project_dir / "paper"
    if not paper_dir.exists() or not paper_dir.is_dir():
        issues.append("paper/ 目录不存在")
        return issues

    has_tex = any(paper_dir.glob("*.tex"))
    has_md = any(paper_dir.glob("*.md"))
    has_pdf = any(paper_dir.glob("*.pdf"))

    if not has_tex and not has_md:
        issues.append("paper/ 中没有 .tex 或 .md 论文文件")
    else:
        # 检查论文内容
        paper_file = None
        if has_tex:
            paper_file = next(paper_dir.glob("*.tex"))
        elif has_md:
            paper_file = next(paper_dir.glob("*.md"))

        if paper_file:
            text = paper_file.read_text(encoding="utf-8", errors="ignore")
            # 检查关键章节
            for keyword in ["摘要", "问题重述", "模型", "求解"]:
                if keyword not in text:
                    issues.append(f"论文中缺少关键词: {keyword}")
                    break

    if not has_pdf:
        issues.append("paper/ 中没有编译后的 PDF")

    return issues


def render_report(result: dict, issues_extended: list[str], project_dir: Path) -> str:
    """生成中文检查报告"""
    lines: list[str] = []
    lines.append("=" * 60)
    lines.append("[Check] 数模项目产物检查报告")
    lines.append("=" * 60)
    lines.append(f"项目目录: {project_dir}")
    lines.append(f"当前阶段: {result['current_stage']} — {result['stage_name']}")
    lines.append("")

    # 阶段完成情况
    lines.append("## 阶段完成情况")
    lines.append("")
    lines.append("| 阶段 | 名称 | 状态 |")
    lines.append("|------|------|------|")
    for stage_id in range(8):
        stage = STAGES[stage_id]
        status = "[OK] 已完成" if result["stage_status"].get(stage_id) else "[MISS] 未完成"
        if stage_id == result["current_stage"]:
            status += " <-- 当前"
        lines.append(f"| {stage_id} | {stage['name']} | {status} |")

    lines.append("")

    # 下一阶段建议
    next_stage = result["current_stage"] + 1
    if next_stage <= 7:
        next_stage_info = STAGES[next_stage]
        lines.append("## 下一阶段")
        lines.append(f"阶段 {next_stage} — {next_stage_info['name']}")
        lines.append(f"需要产物: {', '.join(next_stage_info['files'])}")
        if result["missing_files"]:
            missing_for_next = [
                f for f in result["missing_files"] 
                if f in next_stage_info["files"]
            ]
            if missing_for_next:
                lines.append(f"当前缺失: {', '.join(missing_for_next)}")

    lines.append("")

    # 文件问题
    all_issues = result["all_issues"] + issues_extended
    if all_issues:
        lines.append("## [!] 发现的问题")
        lines.append("")
        for issue in all_issues:
            lines.append(f"- {issue}")
    else:
        lines.append("## [OK] 未发现问题")
        lines.append("")

    lines.append("")
    lines.append("=" * 60)
    return "\n".join(lines)


def main() -> None:
    parser = ArgumentParser(description="检查数模项目产物")
    parser.add_argument("project_dir", type=str, help="项目根目录")
    args = parser.parse_args()

    project_dir = Path(args.project_dir)
    if not project_dir.exists():
        print(f"错误: 目录不存在: {project_dir}")
        sys.exit(1)

    result = determine_stage(project_dir)

    # 扩展检查
    extended_issues: list[str] = []
    if result["stage_status"].get(4):
        extended_issues.extend(check_code_files(project_dir))
    if result["stage_status"].get(5):
        extended_issues.extend(check_figures(project_dir))
    if result["stage_status"].get(6):
        extended_issues.extend(check_paper(project_dir))

    report = render_report(result, extended_issues, project_dir)
    print(report)

    if not result["stage_status"].get(7):
        print(f"提示: 项目仍在阶段 {result['current_stage']}，完成后请运行 check_results_consistency.py 做一致性检查。")


if __name__ == "__main__":
    main()
