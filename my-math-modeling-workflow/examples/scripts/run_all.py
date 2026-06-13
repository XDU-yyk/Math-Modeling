r"""一键运行: 提取所有论文 -> 生成索引 -> 聚合知识

用法:
    python run_all.py [--extract] [--index] [--knowledge]

不传参数时三件事都做。
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parent


def selected(flag: str) -> bool:
    return flag in sys.argv or len(sys.argv) == 1


def run_script(script_name: str) -> None:
    """运行子脚本；失败时立即终止流水线。"""
    env = os.environ.copy()
    env.setdefault("PYTHONIOENCODING", "utf-8")
    command = [sys.executable, str(SCRIPTS_DIR / script_name)]
    result = subprocess.run(command, env=env)
    if result.returncode != 0:
        raise RuntimeError(f"{script_name} 运行失败，退出码 {result.returncode}")


def main() -> None:
    do_extract = selected("--extract")
    do_index = selected("--index")
    do_knowledge = selected("--knowledge")

    try:
        if do_extract:
            print("=" * 50)
            print("阶段 1/3: 提取所有论文")
            print("=" * 50)
            sys.stdout.flush()
            run_script("analyze_papers_local.py")

        if do_index:
            print("\n" + "=" * 50)
            print("阶段 2/3: 生成论文索引")
            print("=" * 50)
            sys.stdout.flush()
            run_script("build_index.py")

        if do_knowledge:
            print("\n" + "=" * 50)
            print("阶段 3/3: 聚合跨论文知识")
            print("=" * 50)
            sys.stdout.flush()
            run_script("build_knowledge.py")

        print("\n全部完成!")
        print(f"论文: {SCRIPTS_DIR.parent / 'papers'}")
        print(f"知识: {SCRIPTS_DIR.parent / 'knowledge'}")
    except Exception as exc:  # noqa: BLE001 - CLI friendly error.
        print(f"\n错误: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
