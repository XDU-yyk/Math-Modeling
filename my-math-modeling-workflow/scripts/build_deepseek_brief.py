r"""DeepSeek 实现任务书生成器

用法:
    python build_deepseek_brief.py <项目目录>

功能:
    1. 读取 PROBLEM_ANALYSIS.md 和 MODELING_PLAN.md
    2. 生成 IMPLEMENTATION_TASKS.md
    3. 明确每个实现任务的输入、输出、运行命令和验收标准

示例:
    python build_deepseek_brief.py D:\projects\cumcm-2026-A
"""

from __future__ import annotations

import sys
import re
from pathlib import Path
from datetime import datetime
from argparse import ArgumentParser


def read_if_exists(path: Path) -> str:
    """读取文件，不存在返回空字符串"""
    if path.exists():
        return path.read_text(encoding="utf-8", errors="ignore")
    return ""


def extract_sections(text: str) -> dict[str, str]:
    """从 markdown 中提取各子问题描述"""
    sections: dict[str, str] = {}
    # 找所有 ## 开头描述子问题的段落
    current_section = "header"
    current_lines: list[str] = []

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("##") or stripped.startswith("###"):
            if current_lines:
                sections[current_section] = "\n".join(current_lines)
            current_section = stripped.lstrip("#").strip()
            current_lines = []
        else:
            if stripped:
                current_lines.append(stripped)

    if current_lines:
        sections[current_section] = "\n".join(current_lines)

    return sections


def extract_sub_problems(analysis_text: str) -> list[dict]:
    """从 PROBLEM_ANALYSIS.md 提取子问题列表"""
    problems: list[dict] = []
    # 匹配 "### 问题一" ~ "### 问题四"
    for i in range(1, 6):
        pattern = rf"### 问题{['一','二','三','四','五'][i-1]}"
        match = re.search(pattern, analysis_text)
        if match:
            start = match.end()
            # 找到下一个 ### 或 ## 作为结束
            next_section = re.search(r"\n(?:###|##)", analysis_text[start:])
            end = start + next_section.start() if next_section else len(analysis_text)
            content = analysis_text[start:end].strip()
            
            # 提取各字段
            def extract_field(text: str, field: str) -> str:
                m = re.search(rf"- {field}[：:]\s*(.+)", text)
                return m.group(1).strip() if m else ""
            
            prob = {
                "index": i,
                "name": f"问题{i}",
                "goal": extract_field(content, "目标"),
                "input": extract_field(content, "输入"),
                "output": extract_field(content, "输出"),
                "constraint": extract_field(content, "约束"),
                "metric": extract_field(content, "评价指标"),
            }
            # 把没有显式字段的内容作为原始描述
            if not any([prob["goal"], prob["input"], prob["output"]]):
                prob["raw"] = content[:300]
            problems.append(prob)

    return problems


def extract_model_mapping(plan_text: str) -> list[dict]:
    """从 MODELING_PLAN.md 提取模型映射"""
    mappings: list[dict] = []
    
    # 尝试解析表格 "子问题到模型映射"
    table_pattern = r"\|\s*(问题[一二三四五六]|问题\d)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|"
    for match in re.finditer(table_pattern, plan_text):
        mappings.append({
            "problem": match.group(1),
            "model": match.group(2).strip(),
            "algorithm": match.group(3).strip(),
            "metric": match.group(4).strip(),
        })

    return mappings


def generate_tasks(
    project_dir: Path,
    analysis_text: str,
    plan_text: str,
) -> str:
    """生成 IMPLEMENTATION_TASKS.md"""
    problems = extract_sub_problems(analysis_text)
    mappings = extract_model_mapping(plan_text)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines: list[str] = [
        "# DeepSeek 实现任务书",
        "",
        f"> 自动生成于 {now}",
        "",
        "## 任务摘要",
        "",
        f"- 项目：{project_dir.name}",
        f"- 当前阶段：代码与结果（阶段 4）",
        f"- 要实现的目标：按建模计划完成数据清洗、模型求解、结果输出和图表生成",
        f"- 不做的内容：论文正文写作（由 Codex 负责）",
        "",
        "## 输入文件",
        "",
        "| 文件 | 说明 | 是否必需 |",
        "| --- | --- | --- |",
        f"| `PROBLEM_ANALYSIS.md` | 题意和子问题 | 是 |",
        f"| `MODELING_PLAN.md` | 模型路线 | 是 |",
        f"| `data/` | 原始数据 | 如有 |",
        "",
        "## 输出文件",
        "",
        "| 文件 | 说明 | 验收标准 |",
        "| --- | --- | --- |",
        "| `code/main.py` | 主入口脚本 | 能运行，不报错 |",
        "| `code/preprocess.py` | 数据预处理 | 输出清洗后数据 |",
        "| `code/model.py` | 模型实现 | 函数可独立调用 |",
        "| `code/visualize.py` | 图表生成 | 生成 figures/ 下图片 |",
        "| `RESULTS.md` | 结果说明 | 包含命令、表格、图表索引 |",
        "| `figures/` | 图表文件 | 每张图有标题和来源 |",
        "| `logs/` | 运行日志 | 记录关键步骤 |",
        "",
        "## 接口约定",
        "",
    ]

    # 生成运行命令
    lines.append("### 主入口")
    lines.append("```bash")
    lines.append("python code/main.py --data data/ --output ./")
    lines.append("```")
    lines.append("")

    lines.extend([
        "### 实现要求",
        "",
        "1. 所有路径相对于项目根目录。",
        "2. 随机种子写入代码或配置文件，保证可复现。",
        "3. 关键参数集中在代码顶部或独立的 `config.py` 中。",
        "4. 对缺失数据、异常数据输出处理日志到 `logs/` 目录。",
        "5. 输出机器可读结果，例如 `metrics.json` 或 `results/tables/*.csv`。",
        "6. 如果是模拟数据或无真实数据，必须在代码注释和 `RESULTS.md` 中显式标注。",
        "",
    ])

    # 子问题实现任务
    if problems:
        lines.append("## 各子问题实现任务")
        lines.append("")
        for p in problems:
            # 查找对应模型
            model_info = ""
            algo_info = ""
            for m in mappings:
                if m["problem"] in p["name"] or p["name"] in m["problem"]:
                    model_info = m["model"]
                    algo_info = m["algorithm"]
                    break

            lines.append(f"### {p['name']}")
            lines.append("")
            lines.append(f"- 目标：{p['goal'] or '见 PROBLEM_ANALYSIS.md'}")
            lines.append(f"- 模型：{model_info or '见 MODELING_PLAN.md'}")
            lines.append(f"- 算法：{algo_info or '见 MODELING_PLAN.md'}")
            lines.append(f"- 输入：{p['input'] or 'data/ 下的原始数据'}")
            lines.append(f"- 输出：{p['output'] or '结果写入 RESULTS.md'}")
            if p.get("metric"):
                lines.append(f"- 验证指标：{p['metric']}")
            lines.append("")

    # 通用任务
    lines.extend([
        "## 通用实现任务",
        "",
        "### T0: 数据读取与预处理",
        "- 实现 `data/` 到清洗后数据的完整链路。",
        "- 对缺失值、异常值、量纲不一致做处理。",
        "- 输出预处理报告到 `logs/preprocess.log`。",
        "",
        "### T-plot: 图表生成",
        "- 每张图对应一个结论或模型环节。",
        "- 图表要有标题、坐标轴标签、单位、数据来源。",
        "- 至少包含一张技术路线/流程图。",
        "- 图表文件保存到 `figures/` 目录。",
        "",
        "### T-result: 结果汇总",
        "- 输出 `RESULTS.md`，包含运行命令、关键参数、核心表格和图表索引。",
        "- 如果使用模拟数据，必须显式标注。",
        "- 记录任何异常和未解决的警告。",
        "",
    ])

    # 验收标准
    lines.extend([
        "## 验收标准",
        "",
        "1. `python code/main.py` 能无错误运行。",
        "2. 结果文件存在且内容正确。",
        "3. 日志无未处理异常。",
        "4. `RESULTS.md` 能解释主要输出，不用看代码也能理解。",
        "5. 生成的图表能被论文正文直接引用。",
        "6. 没有把模拟结果伪装成真实数据。",
        "",
        "## 提交格式",
        "",
        "完成后将以下文件放在项目根目录：",
        "- `code/` （所有脚本）",
        "- `RESULTS.md`",
        "- `figures/` （所有图表）",
        "- `logs/` （运行日志）",
    ])

    return "\n".join(lines)


def main() -> None:
    parser = ArgumentParser(description="生成 DeepSeek 实现任务书")
    parser.add_argument("project_dir", type=str, help="项目根目录")
    args = parser.parse_args()

    project_dir = Path(args.project_dir)
    if not project_dir.exists():
        print(f"错误: 目录不存在: {project_dir}")
        sys.exit(1)

    analysis_path = project_dir / "PROBLEM_ANALYSIS.md"
    plan_path = project_dir / "MODELING_PLAN.md"

    analysis_text = read_if_exists(analysis_path)
    plan_text = read_if_exists(plan_path)

    if not analysis_text:
        print("警告: PROBLEM_ANALYSIS.md 不存在或为空")
    if not plan_text:
        print("警告: MODELING_PLAN.md 不存在或为空")

    tasks_md = generate_tasks(project_dir, analysis_text, plan_text)

    output_path = project_dir / "IMPLEMENTATION_TASKS.md"
    if output_path.exists():
        existing = output_path.read_text(encoding="utf-8", errors="ignore")
        if len(existing.strip()) > 200 and "待填写" not in existing:
            print(f"警告: {output_path} 已有内容，将被覆盖。")
    
    output_path.write_text(tasks_md, encoding="utf-8")
    print(f"已生成: {output_path}")
    print(f"内容长度: {len(tasks_md)} 字符")


if __name__ == "__main__":
    main()
