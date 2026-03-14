# Cyber Guard Platform

## Course Context

- Course: Senior Project II
- Group: CRN Groups Info - Jeddah Male
- CRN: `27349`

## What This Repo Is

This repository is a scaffold-first implementation map for the Cyber Guard Platform. It is designed so six students can start work immediately, understand ownership quickly, and build in parallel without turning the repo into chaos.

The local filesystem is the current source of truth for this project structure.

## What This Repo Is Not

- not a finished production application
- not the place to overengineer infrastructure
- not a giant polished demo
- not a free-for-all where everyone edits everything

Many files are intentionally placeholders with comments, TODOs, and ownership hints. That is expected.

## Updated Project Summary

Cyber Guard is a web platform where Users and Organizations can:

- create accounts
- work inside organizations with workspaces and roles
- submit file/hash, URL, and email indicator artifacts
- run asynchronous scan jobs
- normalize artifacts and enrich them from multiple threat-intel sources
- optionally run AI analysis in local mode or API mode
- generate private threat reports and dashboard visuals
- publish anonymized reports to a public Threats page
- send external reports through admin review before public publishing
- optionally expose a future Public Threats API

Critical rule: public threat data must not link back to private identity or workspace data.

## Start Here

Read these in this order before you change anything:

1. `README.md`
2. `CONTRIBUTING.md`
3. `docs/ASSIGNMENT_MAP.md`
4. `docs/WEEK_1_TODO.md`
5. `docs/IMPLEMENTATION_STATUS.md`

If you skip that order, you will probably touch the wrong files.

## Quick Structure Summary

```text
backend/   -> FastAPI scaffold, models, schemas, services, tests
frontend/  -> React scaffold, pages, components, mocks, types
docs/      -> assignment map, workflow, weekly TODOs, diagrams, status tracking
```

Important high-level folders:

- `backend/app/api/routes/` for endpoint ownership
- `backend/app/services/` for real implementation work
- `backend/app/models/` and `backend/app/schemas/` for data contracts
- `frontend/src/pages/` and `frontend/src/components/` for UI ownership
- `docs/` for coordination, assignment, and reporting

## Start Working In One Simple Flow

1. Read the required files above.
2. Find your name in `docs/ASSIGNMENT_MAP.md`.
3. Create your branch using the branch format from `CONTRIBUTING.md`.
4. Work only inside your assigned files unless you coordinate first.
5. Update the weekly TODO file and `docs/IMPLEMENTATION_STATUS.md`.
6. Submit your work to the integrator.

## How To Submit Work

Normal path:

- create your branch
- commit only your assigned changes
- push your branch
- ask the integrator to review/merge

Alternate submission path:

- edit only your assigned files locally
- send the changed files or a zipped patch to the integrator
- send a short note with: what changed, what is unfinished, what is blocked

Detailed instructions are in `CONTRIBUTING.md` and `docs/SUBMISSION_RULES.md`.

## Who Integrates And Merges Changes

Current integrator / maintainer for this team scaffold:

- `220041379 - MUHANNAD ALKHARMANI`

That role is documented so contributors always have a safe submission path.

## Quick Validation Commands

Backend:

```bash
cd backend
pytest -q
```

Frontend:

```bash
cd frontend
npm run build
```

## Key Coordination Docs

- `CONTRIBUTING.md`
- `docs/TEAM_WORKFLOW.md`
- `docs/ASSIGNMENT_MAP.md`
- `docs/IMPLEMENTATION_STATUS.md`
- `docs/TASK_CARDS.md`
- `docs/SUBMISSION_RULES.md`
- `docs/HANDOFF_CHECKLIST.md`

## Scaffold Reminder

This repo should continue to feel like a smart scaffold with placeholders, TODOs, ownership hints, and coordination docs. If you are about to turn a placeholder into a full subsystem by yourself, stop and check the assignment map first.
