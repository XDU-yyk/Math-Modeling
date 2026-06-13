# Modex 数模工作流研究发现

## Initial Evidence

- 工作区根目录是 `D:\Modex`，实际应用目录是 `D:\Modex\Modex-MH-Agent`。
- `D:\Modex\Modex-MH-Agent` 看起来是打包后的 Electron 应用，不是 git 仓库。
- 应用入口文件位于 `D:\Modex\Modex-MH-Agent\resources\app\main.js`。
- 应用资源下有 `backend`、`dist`、`skills`、`templates`、`tools` 目录。
- `runtime` 内包含 `node`、`python`、`git`、`pandoc`、`texlive`、`draw.io`，说明它把论文/报告/图形/代码执行所需工具链一起打包。
- `resources\app\skills` 中存在大量 workflow/skill 目录，包括 `comp-prob-analysis`、`comp-modeling`、`comp-code`、`comp-paper-zh`、`comp-compile-zh`、`comp-stats-topic`。
- `resources\app\skills\.skill_meta.json` 存在，长度 33 字节，需要进一步读取确认是否标记加密。
- `resources\app\skills\.skill_meta.json` 内容为 `{"version": 2, "encrypted": true}`，证明 skill 体系整体是加密格式。
- 后端数据库包含 `workflows`、`workflow_steps`、`workflow_logs`、`checkpoints`、`settings` 表，工作流核心是模板化 pipeline、步骤状态、日志、产物列表、人工 checkpoint。
- `main.js` 显示 Electron 主进程会启动内嵌 Python 后端：`python.exe -m uvicorn main:app --host 127.0.0.1 --port <port>`，工作目录是 `resources\app\backend`。
- `main.js` 会把 `runtime\node`、`runtime\git`、`runtime\texlive` 等加入 PATH，并为 Claude CLI 设置 Git Bash 路径。
- `backend\main.py` 暴露 `/api/templates`，从 `services.workflow_engine.TEMPLATES` 返回模板 display name、pipeline_skill 和 sub_steps。
- `backend\main.py` 在启动时会恢复未完成工作流，并启动 heartbeat 检查/恢复僵尸工作流。
- 前端通过 `/api/workflows` 创建、启动、暂停、重启工作流；创建请求包含 `template`、`title`、`params`、`enable_checkpoints`。
- 前端产物展示规则里把 `comp-code` 的产物归为 `code/`，`comp-paper-zh`/`comp-paper-en` 归为 `paper/`，`comp-compile-zh`/`comp-compile-en` 归为 `paper/*.pdf` 和日志。
- `comp-code` 有 `references\checks` 子目录，覆盖 consistency、evaluation、optimization、physical、prediction、sanity_check 等检查维度。
- `comp-modeling` 有 `references\error_prevention.md.enc` 和 `methods_table.md.enc`，说明建模 skill 强调方法选择和错误预防。
- `comp-paper-zh` 带大量竞赛模板：cumcm、huawei、mathorcup、shuweibei、stats、mcm、apmcm 等；模板里的正文 `main.tex` 多数也加密，但 `.cls`、字体、图片资源可见。
- `templates` 顶层提供研究类输入模板：research brief、research contract、experiment plan、findings、paper plan 等，说明 Modex 工作流强调先收敛问题和 claims，再跑实验/写作。
- 直接用内置 Python 只读导入 `services.workflow_engine` 成功；`TEMPLATES` 有 34 个模板。
- 中文数模模板如 `comp_cumcm`、`comp_huawei`、`comp_mathorcup`、`comp_teddy`、`comp_certcup`、`comp_huazhong`、`comp_huadong`、`comp_wuyi`、`comp_shuwei`、`comp_zhongqing`、`comp_yangtze`、`comp_diangong`、`comp_shenzhen`、`comp_huashu`、`comp_tianfu`、`comp_liaoning` 共用主链路：
  1. `comp-prob-analysis` 赛题分析，checkpoint 为 `approve`
  2. `comp-modeling` 建模求解，checkpoint 为 `feedback`
  3. `comp-code` 编程实现，checkpoint 为 `approve`
  4. `paper-figure` 图表生成，无 checkpoint
  5. `paper-figure-drawio` 流程与架构图绘制，无 checkpoint
  6. `comp-paper-zh` 竞赛论文撰写，checkpoint 为 `approve`
  7. `comp-compile-zh` 编译与合规检查，无 checkpoint
- 英文数模模板如 `comp_mcm`、`comp_certcup_en`、`comp_shuwei_en` 使用同样骨架，但论文和编译步骤换成 `comp-paper-en`、`comp-compile-en`。
- `comp_stats` 统计建模大赛链路略不同：`comp-stats-topic` 选题与数据规划 -> `comp-code` 数据采集与统计分析 -> 图表 -> 流程图 -> `comp-paper-zh` -> `comp-compile-zh`。
- `config` 中当前路径为：`API_PORT=18088`、`SKILLS_DIR=D:\Modex\Modex-MH-Agent\resources\app\skills`、`TEMPLATES_DIR=D:\Modex\Modex-MH-Agent\resources\app\templates`、`TOOLS_DIR=D:\Modex\Modex-MH-Agent\resources\app\tools`。
- `claude_runner` 字符串显示执行模型是 `Claude Code CLI`，按 skill 加载 `SKILL.md`/解密后的 prompt，然后运行 `claude -p`。
- `workflow_engine` 公开结构：
  - `StepDef(skill_name, display_name, output_files, primary_output, has_checkpoint, checkpoint_type)`
  - `TemplateDef(pipeline_skill, display_name, sub_steps)`
  - 关键函数包括 `create_new_workflow`、`run_workflow`、`run_single_step`、`wait_checkpoint`、`resolve_checkpoint`、`_generate_claude_md`、`_scan_workspace`、`_build_context_summary`、`_resolve_template`。
- `config` 还显示：
  - `WORKSPACES_DIR=C:\Users\yyk\AppData\Roaming\MHAgent\workspaces`
  - `DB_PATH=C:\Users\yyk\AppData\Roaming\MHAgent\db\aris.db`
  - `CLAUDE_BIN=D:\Modex\Modex-MH-Agent\runtime\node\node_modules\@anthropic-ai\claude-code\bin\claude.exe`
  - `PANDOC_BIN=D:\Modex\Modex-MH-Agent\runtime\pandoc\pandoc.exe`
- FastAPI 路由覆盖 workflow 生命周期、artifacts、checkpoints、settings、editor、compile、docx export、AI edit/run-script/image-check 等。实际产品不是单纯工作流按钮，而是“流程执行 + 工作区编辑器 + 产物管理 + 格式导出”的一体化桌面壳。
- 典型中文数模 `StepDef` 产物：
  - 赛题分析：`PROBLEM_ANALYSIS.md`
  - 建模求解：`MODELING_REPORT.md`
  - 编程实现：`code/main.py`、`RESULTS.md`
  - 图表：`figures/latex_includes.tex`、`figures/`
  - 论文：`paper/main.tex`
  - 编译：`paper/main.pdf`

## Working Hypothesis

Modex 的工作流是“Electron 前端 + 本地 FastAPI backend + 编译 workflow engine + 打包 runtime + 加密 skills 目录”的组合。比赛数模链路可能由 `comp-prob-analysis -> comp-modeling -> comp-code -> comp-paper-zh -> comp-compile-zh` 等 skill 串接完成。

## Evidence To Collect Next

- 每个 `comp-*` 目录下实际文件名、元数据、是否有 `SKILL.md.enc`。
- `main.js` 如何启动 backend、传入 skills 路径和 runtime 路径。
- `backend` 里是否有 skill loader、workflow runner、agent dispatcher。
- `templates` 和 `shared-*` 目录是否提供报告模板、脚本或公共约束。
- 前端 bundle 中竞赛模板 key 与中文名称的对应关系。
- `workflow_engine` 内部是否能公开读到完整 dataclass 结构；目前模板 key、display、pipeline、sub_steps 已足够支撑个人工作流设计。
- Codex-native 个人工作流是否应该拆成多个 skills，还是一个 orchestration skill 加 references/scripts；需要给用户方案后确认。

## Reusable Design Pattern

Modex 的核心不是一个超长 prompt，而是一套可恢复的状态机：

1. `TemplateDef` 选择比赛/任务类型，并决定 `pipeline_skill`。
2. `StepDef` 明确每一步的 skill 名、显示名、预期输出文件、主输出、是否需要 checkpoint。
3. 每一步只负责一个产物层级，例如 `PROBLEM_ANALYSIS.md`、`MODELING_REPORT.md`、`RESULTS.md`、`paper/main.tex`、`paper/main.pdf`。
4. 后端用数据库记录 workflow、step、log、checkpoint 和 workspace 路径。
5. 执行前生成工作区上下文，执行中监听文件变化，执行后按预期产物和健康检查判断是否可进入下一步。
6. 人工 checkpoint 只放在高风险决策点：题目理解、模型路线、代码结果、论文终稿。
7. 工具链和模板与 skill 分开：runtime 负责 Python/Node/LaTeX/Pandoc/Draw.io，skills 负责阶段逻辑，templates/tools 负责可复用格式和脚本。

## Personal Math Modeling Workflow Options

### Option A: Single Orchestration Skill

创建一个 Codex skill，例如 `math-modeling-workflow`，把题目分析、建模、代码、图表、论文、编译检查写成一个分阶段流程。它用 `references/` 放方法表、论文结构、错误清单，用 `scripts/` 放项目初始化和产物检查脚本。

优点：最容易触发、维护和测试，不需要重建 Modex 的整套后端。

### Option B: Modex-like Multi-skill Suite

创建多个 skill：`mm-problem-analysis`、`mm-modeling`、`mm-code`、`mm-figures`、`mm-paper-zh`、`mm-compile-check`，再加一个协调 skill。

优点：最接近 Modex；缺点：第一版容易过度拆分，调试成本更高。

### Option C: Project-local Workflow Kit

不先创建全局 skill，而是在每个比赛项目中生成标准目录和 `workflow.md`、`checklists/`、`templates/`。Codex 通过项目文件推进流程。

优点：项目自包含；缺点：不如 skill 自动触发，跨项目复用弱一些。

## Recommended First Build

建议先做 Option A，并配一个小型项目模板：

- 全局 Codex skill：`math-modeling-workflow`
- `references/pipeline.md`：阶段、关口、预期产物
- `references/modeling-methods.md`：常见方法选择图谱
- `references/paper-structure-zh.md`：中文数模论文结构
- `references/error-checklist.md`：数据、模型、代码、结果、格式错误清单
- `scripts/init_project.py`：创建标准项目目录和起始 markdown 文件
- 后续再加 `scripts/check_artifacts.py`：检查关键产物是否存在且有基本内容

第一版保留 Modex 的“阶段关口 + 命名产物 + 人工确认点”，但不复制加密 skill，也不一开始重建桌面工作流引擎。
