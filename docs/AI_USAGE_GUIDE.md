# AI_USAGE_GUIDE.md

## Purpose

This guide explains how team members can use AI tools, especially Codex inside VS Code, in a safe and course-appropriate way.

Use AI as an assistant, not as the owner of your task.

## Safe Use Policy

AI is allowed only if all of these remain true:

- you stay inside your assigned files
- you understand what the AI changed
- you can explain the code later in class or to the supervisor
- you do not let AI invent product scope that is not in the repo
- you keep the scaffold-first philosophy

## What AI Is Good For In This Repo

- understanding an existing file
- rewriting comments or TODOs clearly
- adding or improving placeholder structure
- creating simple scaffold-level route/service/page shapes
- updating docs and trackers
- generating tests from an already defined contract
- simplifying repetitive code

## What AI Must Not Do Here

- build large unassigned features
- invent new routes or models not in the current repo plan
- add random dependencies without approval
- replace the scaffold with a finished app
- write code so advanced that the student cannot explain it later
- silently edit files outside the assigned area

## Core Rules For Codex In VS Code

1. Always tell Codex which files you own.
2. Always say the local repo is the source of truth.
3. Always say the repo is a scaffold, not a finished app.
4. Tell Codex to inspect existing files first.
5. Tell Codex to edit only your assigned files unless coordination is needed.
6. Tell Codex to keep logic simple and student-readable.
7. Tell Codex not to add extra features.
8. Ask Codex to explain the change in plain language after editing.

## The Simplicity Rule

If AI gives you code that feels too clever, too polished, too abstract, or too hard to explain, do not accept it directly.

Ask it to rewrite the output with these constraints:

- simpler naming
- smaller functions
- clearer comments
- no extra abstractions
- scaffold-level only
- easy to explain in a project meeting

## The Scope Rule

Before accepting AI output, check:

- did it stay inside the assigned file list?
- did it keep the current product truth?
- did it avoid implementing extra features?
- did it preserve TODOs and placeholders where they still belong?

If the answer is no, reject the output and retry with a tighter prompt.

## The Explain-It Rule

Before you commit AI-assisted work, you should be able to explain:

1. why this file exists
2. what changed
3. what is still not implemented
4. why this approach fits the scaffold

If you cannot explain those four points, do not submit the change yet.

## Recommended Flow

1. Read your assigned files first.
2. Open Codex in VS Code.
3. Start with `docs/CODEX_TEAM_JOURNEY.md` so Codex narrows itself to your assigned area first.
4. Use a constrained prompt from `docs/CODEX_PROMPT_TEMPLATES.md`.
5. Review every changed file.
6. Simplify anything that feels too advanced.
7. Update the weekly TODO and status tracker.
8. Commit only after you understand the result.

## If Codex Starts Inventing Things

Stop and correct the prompt immediately.

Tell it:

- local repo is source of truth
- do not invent new architecture
- do not add routes or files outside my area
- keep scaffold-level only
- rewrite using simpler code and comments

## Final Rule

Do not submit AI-generated work that you cannot defend, explain, or maintain.
