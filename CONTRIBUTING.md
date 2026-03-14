# CONTRIBUTING.md

## Purpose

This guide is written for students, including teammates who are not confident with Git or GitHub yet. Follow the steps exactly and keep your work inside your assigned area.

## Before You Start

Read these first:

1. `README.md`
2. `docs/ASSIGNMENT_MAP.md`
3. your current weekly TODO file
4. `docs/IMPLEMENTATION_STATUS.md`

## Clone The Repo

```bash
git clone https://github.com/cl0udz1/cyber_guard_platform.git
cd cyber_guard_platform
```

If the old URL appears anywhere, use the current repo location above.

## Open The Repo

Recommended options:

- VS Code
- PyCharm
- WebStorm

Open the project root folder, not only `backend/` or `frontend/`.

## Create Your Branch

Always branch from the latest `main`.

```bash
git checkout main
git pull origin main
git checkout -b your-branch-name
```

## Branch Naming Rules

Use short branch names based on your assigned area:

- `bander/auth-orgs`
- `faris/scan-pipeline`
- `omar/integrations-ai`
- `muhannad/reports-dashboard`
- `ghaza/frontend-flows`
- `abdullah/docs-tests`

Do not invent random branch names like `test123`, `new-branch`, or `final`.

## Commit Message Style

Keep commits short, clear, and area-based.

Examples:

- `docs: finalize assignment map and workflow`
- `backend: scaffold scan orchestrator interfaces`
- `frontend: add report and dashboard placeholder pages`

Do not use commit messages like `update`, `fix stuff`, or `final final`.

## What You Should Edit

Edit only the files in your assigned area from `docs/ASSIGNMENT_MAP.md`.

## What You Should Not Edit Without Coordination

Do not change these unless you coordinate first:

- `README.md`
- `CONTRIBUTING.md`
- `docs/API_CONTRACT.md`
- `docs/ASSIGNMENT_MAP.md`
- `docs/IMPLEMENTATION_STATUS.md`
- shared backend dependency files such as `backend/app/api/deps.py`
- shared frontend structure files such as `frontend/src/app/AppShell.tsx`

If your task depends on one of those files, message the related owner and the integrator first.

## How To Mark TODOs Complete

When you finish part of your work:

1. update the relevant weekly TODO file
2. update your row in `docs/IMPLEMENTATION_STATUS.md`
3. leave short TODO notes in code if something is still unfinished

Do not silently leave half-finished work with no note.

## How To Submit Work With GitHub

1. finish your changes
2. run the relevant checks if possible
3. commit your work
4. push your branch

```bash
git push origin your-branch-name
```

5. open a Pull Request, or send the branch name to the integrator
6. include:
   - what files changed
   - what is done
   - what is not done
   - any blockers

## Alternate Workflow If You Need Manual Handoff

If you need a manual handoff path, do this instead:

1. still read the repo locally
2. edit only your assigned files
3. make a folder or zip containing only your changed files
4. send it to the integrator
5. include a short text note:
   - your name
   - files changed
   - done / in progress / blocked
   - what still needs review

Integrator for this repo:

- `220041379 - MUHANNAD ALKHARMANI`

This manual handoff path is allowed, but it is only safe if you stay inside your area.

## If You Are Stuck, Do This

1. stop editing random files
2. write down the exact file and exact blocker
3. update the status tracker with the blocker
4. message the related owner and the integrator
5. if needed, hand off your current files instead of waiting silently

## Final Rule

This repository is a scaffold. Keep changes focused, readable, and assignment-friendly. Do not try to finish the whole app alone from inside your branch.
