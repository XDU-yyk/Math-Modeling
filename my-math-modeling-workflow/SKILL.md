---
name: math-modeling-workflow
description: Build, continue, review, or organize Chinese/English mathematical modeling competition projects. Use when Codex needs to analyze a modeling problem, choose models, plan solution code, coordinate figures and papers, check result consistency, or help DeepSeek implement concrete modeling functions from a workflow outline. This skill uses example-paper knowledge under examples/knowledge and follows a staged artifact workflow instead of jumping directly to a final paper.
---

# Math Modeling Workflow

Use this skill to run a mathematical modeling project as a staged, file-backed workflow. Keep Codex focused on workflow design, artifact contracts, review, and orchestration. Delegate concrete model/code implementation tasks to DeepSeek when the user asks for collaboration or implementation.

## First Steps

1. Inspect the current project files before giving advice.
2. Read `references/workflow-blueprint.md` for the stage contract.
3. Read `examples/knowledge/papers-index.md` and the relevant files under `examples/knowledge/cross-paper/` before choosing a modeling route.
4. If the user provides a new problem, create or update the standard artifacts instead of answering only in chat.
5. If existing artifacts are present, infer the current stage from files and continue from the next missing or weak artifact.

## Standard Artifacts

- `PROJECT_BRIEF.md`
- `PROBLEM_ANALYSIS.md`
- `MODELING_PLAN.md`
- `MODELING_REPORT.md`
- `code/`
- `RESULTS.md`
- `figures/`
- `paper/`
- `CHECK_REPORT.md`

## Stage Gates

Pause for user confirmation at these points unless the user explicitly asks for an uninterrupted draft:

- After `PROBLEM_ANALYSIS.md`, because misunderstanding the problem poisons the whole workflow.
- After `MODELING_PLAN.md`, because method selection determines code and paper narrative.
- After `RESULTS.md`, because numbers and assumptions must be trusted before writing.
- After the paper outline or final-paper plan, because paper narrative should match the user's intended competition story.

## Collaboration With DeepSeek

When working with DeepSeek:

- Codex writes the workflow outline, artifact requirements, interfaces, acceptance criteria, and review checklist.
- DeepSeek implements concrete functions, data processing, model training/solving code, plotting, and document conversion.
- Codex reviews DeepSeek output against `references/implementation-brief-for-deepseek.md` and `references/quality-gates.md`.
- Never let implementation claims enter the paper unless the corresponding code, data, result file, or manual assumption is visible.

## Reference Navigation

- Use `references/workflow-blueprint.md` for the full staged workflow.
- Use `references/skill-outline.md` for the skill architecture and resource plan.
- Use `references/model-selection-guide.md` for mapping problem types to model families.
- Use `references/paper-writing-guide.md` for paper structure and writing rules.
- Use `references/quality-gates.md` for consistency checks.
- Use `references/implementation-brief-for-deepseek.md` when handing implementation tasks to DeepSeek.

## Example Knowledge

The example-paper evidence is generated from 29 PDFs in `examples/papers/`, totaling 1068 pages and about 1.56 million extracted characters. Use these files as empirical guidance, not as unquestioned truth:

- `examples/knowledge/extraction-evidence-summary.md`
- `examples/knowledge/paper-extraction-summary.json`
- `examples/knowledge/cross-paper/common-patterns-from-examples.md`
- `examples/knowledge/cross-paper/modeling-methods-from-examples.md`
- `examples/knowledge/cross-paper/paper-structures-from-examples.md`
- `examples/knowledge/cross-paper/result-presentation-from-examples.md`

## Operating Rules

- Default explanatory text, paper text, chart labels, and workflow documents to Chinese for Chinese competitions.
- Separate problem understanding, modeling choice, implementation, results, and paper writing.
- Prefer reproducible scripts and visible result files over narrative-only claims.
- Record assumptions explicitly, especially when data is missing or simulated.
- Use example papers to guide structure and method selection, but do not copy text.
- Keep `SKILL.md` concise; put detailed guidance in `references/`.
