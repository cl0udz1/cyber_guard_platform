# CODEX_VSCODE_QUICKSTART.md

## Purpose

This is a quick start for using Codex inside VS Code on this repo.

Fastest path:

- open Codex
- point it to `docs/CODEX_TEAM_JOURNEY.md`
- tell it your name
- let it focus on your section first

## Before Opening Codex

1. open the full project folder in VS Code
2. read `README.md`
3. read `CONTRIBUTING.md`
4. read your section in `docs/ASSIGNMENT_MAP.md`
5. open `docs/CODEX_TEAM_JOURNEY.md`
6. list your exact owned files first

## Easiest Starter Prompt

If you want the simplest possible start, use this:

```text
Read docs/CODEX_TEAM_JOURNEY.md.
I am [YOUR NAME].
Use only my section.

First tell me:
1) my area
2) my files
3) what to avoid
4) the safest first task

Do not edit anything yet.
```

## What To Tell Codex At The Start

Always tell Codex:

- this is a local repository
- the local filesystem is the source of truth
- this is a scaffold, not a finished app
- I only want edits in my assigned files
- keep the code simple and easy for a student to explain
- do not invent extra features, routes, or dependencies

## Good Session Pattern

1. ask Codex to inspect your files first
2. ask it to summarize what those files currently do
3. ask it to make one contained change
4. review the diff
5. ask it to explain the change in plain language

## Bad Session Pattern

Do not open with prompts like:

- build the whole feature
- finish this module
- make this production ready
- improve everything
- redesign the architecture

Those prompts are how AI starts overbuilding.

## Good First Prompt

```text
You are working inside the local repository for cyber_guard_platform.
The local filesystem is the source of truth.
This repo is a scaffold, not a finished app.
My assigned area is: [your area].
Only inspect and edit these files:
- [file 1]
- [file 2]
- [file 3]

First read those files and summarize:
1) what each file currently does
2) what is still placeholder
3) what the safest next small change is

Do not edit anything yet.
Do not invent extra routes, models, or dependencies.
Keep everything student-readable.
```

## If You Need A Real Edit

Use one small request at a time:

- add owner comments
- clarify a schema
- improve a placeholder page
- clean a route docstring
- add a small test

Do not ask for five different tasks in one prompt.

## Before Accepting Changes

Check:

- only my files changed
- no unrelated files changed
- no random new dependency was added
- the code is still scaffold-level
- I can explain it

Then update your weekly TODO and status tracker.
