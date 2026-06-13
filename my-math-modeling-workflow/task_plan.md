# Modex 数模工作流反向梳理计划

## Goal

理解 `D:\Modex\Modex-MH-Agent` 的工作流设计和 skill 机制，并基于证据设计一套可在 Codex 中使用的个人数模工作流。

## Phases

| Phase | Status | Purpose |
| --- | --- | --- |
| 1. 建立工作记录 | complete | 创建可恢复的计划、发现和进度文件。 |
| 2. 盘点应用结构 | complete | 确认 Electron 入口、backend、templates、tools、skills、runtime 的职责。 |
| 3. 反向梳理 skill 机制 | complete | 分析 `skills` 目录、元数据、加密状态、comp 系列工作流边界。 |
| 4. 抽象 Modex 工作流设计 | complete | 归纳任务拆解、子 agent/skill 调度、产物流转、验证闭环。 |
| 5. 设计个人数模工作流 | complete | 已在 `my-math-modeling-workflow/` 内落地 workflow 与 Skill 大纲，并基于论文样本生成知识库。 |

## Constraints

- 先基于真实文件和运行路径，不凭记忆下结论。
- 不直接复制 Modex 加密 skill；若加密，只作为工作流蓝图重建 Codex-native skill。
- 在用户确认设计前，不落地新的个人 skill 目录或工作流实现。
- 说明和交付文档默认使用中文。

## Current Questions

- 用户是否希望用浏览器可视化 companion 展示工作流图；在未回复前先用文字推进研究。
- 个人数模工作流最终放在哪里：默认候选为 `C:\Users\yyk\.codex\skills`，待设计确认后再决定。

## Errors Encountered

| Error | Attempt | Resolution |
| --- | --- | --- |
| `rg.exe` Access is denied | 用 `rg` 搜索记忆文件 | 改用 PowerShell `Select-String` 和 `Get-ChildItem`。 |
| `D:\Modex` 不是 git 仓库 | 查询 `git status/log` | 按打包应用目录处理，不依赖 git。 |
| `strings.exe` not found | 尝试用打包 Git 提取 `.pyd` 字符串 | 下一步改用 PowerShell/.NET 或 Python 做二进制字符串提取。 |
| `quick_validate.py` 缺少 `yaml` | 尝试运行 skill-creator 自带校验 | 改用无依赖 Python 校验 `SKILL.md` frontmatter 的 `name`、`description` 和命名规则。 |
