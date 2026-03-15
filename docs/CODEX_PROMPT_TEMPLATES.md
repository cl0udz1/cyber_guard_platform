# CODEX_PROMPT_TEMPLATES.md

## Purpose

These are editable prompts for safe Codex use in this repo.

Replace bracketed sections before sending.

## Template 1 - Inspect First

```text
You are working inside the local repository for cyber_guard_platform.
The local filesystem is the source of truth.
This repo is a scaffold, not a finished app.
My assigned area is [area].
Only inspect these files:
- [file 1]
- [file 2]
- [file 3]

First read those files and tell me:
1) what each file currently does
2) what is still placeholder
3) what I should implement next without overbuilding

Do not edit anything yet.
Do not invent extra features.
```

## Template 2 - Small Safe Edit

```text
You are working inside the local repository for cyber_guard_platform.
The local filesystem is the source of truth.
This repo is a scaffold, not a finished app.
Only edit these files:
- [file 1]
- [file 2]

Task:
[small task here]

Rules:
- keep the code simple
- keep it easy for a student to explain later
- do not add new dependencies
- do not add extra routes/models/pages outside the request
- preserve TODO comments and scaffold placeholders where appropriate
```

## Template 3 - Keep It Simple

Use this when Codex gives code that is too advanced:

```text
Rewrite your last change in a simpler, student-readable way.

Constraints:
- smaller functions
- clearer names
- fewer abstractions
- scaffold-level only
- easy to explain in a team meeting
- do not add extra behavior
```

## Template 4 - Stop Hallucination / Scope Drift

Use this if Codex starts inventing things:

```text
Stop.
The local repo is the source of truth.
Do not invent new architecture, routes, models, dependencies, or features.
Stay inside these files only:
- [file 1]
- [file 2]

Redo the change as a small scaffold-level update only.
```

## Template 5 - Add Comments And Ownership Hints

```text
Only update comments and headers in these files:
- [file 1]
- [file 2]

Add short sections for:
- Purpose
- Owner
- Inputs/Outputs
- TODO

Do not add real feature logic.
Keep the comments practical and readable.
```

## Template 6 - Add A Small Test

```text
You are working inside the local repository for cyber_guard_platform.
This repo is a scaffold.
Only edit these files:
- [test file]
- [related source file if needed]

Add one small test for:
[exact behavior]

Rules:
- do not expand scope
- do not rewrite unrelated code
- keep the test easy to understand
- match the current route/schema names exactly
```

## Template 7 - Ask Codex To Explain The Result

Use this after a change:

```text
Explain the change you just made in plain student-friendly language.

Tell me:
1) what changed
2) why it changed
3) what is still placeholder
4) how I should explain this to my supervisor or teammate
```
