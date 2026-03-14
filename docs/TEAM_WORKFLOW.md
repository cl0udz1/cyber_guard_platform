# TEAM_WORKFLOW.md

## Team Context

- Group: CRN Groups Info - Jeddah Male
- CRN: `27349`

## Source Of Truth

Official source of truth for the team is the GitHub repository on `main`.

Local copies are for working. The shared truth is what gets merged into the repo.

## Communication

Use one fast channel for daily coordination:

- WhatsApp, or
- Telegram

Keep messages short and practical:

- what changed
- what is blocked
- what file is affected
- who is needed

## Coordination Tracker

Use one simple shared tracker:

- Google Sheet, or
- a shared checklist document

The tracker should match:

- current weekly TODO file
- `docs/IMPLEMENTATION_STATUS.md`

## Integrator / Maintainer Role

Current integrator and merge coordinator:

- `220003069 - ABDULLAH BAALI`

Integrator responsibilities:

- review incoming branches or fallback file handoffs
- protect `main`
- check that status docs are updated
- merge only after area ownership is respected

## Branch Rules

Use these branch names:

- `bander/auth-orgs`
- `faris/scan-pipeline`
- `omar/integrations-ai`
- `muhannad/reports-dashboard`
- `ghaza/frontend-flows`
- `abdullah/docs-tests`

## Commit Style

Use short area-based commit messages:

- `docs: finalize assignment map and workflow`
- `backend: scaffold scan orchestrator interfaces`
- `frontend: add report and dashboard placeholder pages`

## Weekly Sync Flow

1. each member updates their area before the weekly sync
2. each member reports:
   - done
   - in progress
   - blocked
3. integrator checks status tracker and weekly TODO file
4. blockers are reassigned or escalated
5. merge plan for the week is agreed

## When Two People Need Related Files

If two areas touch the same file:

1. the current owner keeps primary control
2. the second person asks first
3. both agree who edits and who reviews
4. the integrator is informed if the file is shared or risky

Examples of shared files:

- `docs/API_CONTRACT.md`
- `docs/IMPLEMENTATION_STATUS.md`
- `backend/app/api/deps.py`
- shared frontend types

## Escalation Rules

Escalate to the integrator when:

- you are blocked for more than one day
- another task depends on your unfinished file
- two branches touch the same core file
- someone cannot use Git properly
- a change risks breaking the public/private data separation rule

## Fallback For Weak Git Users

This repo supports a controlled fallback:

- weak Git users still read the repo locally
- they edit only assigned files
- they send changed files or a zip to the integrator
- the integrator merges manually
- the teammate still must report status and blockers clearly

This fallback is a safety path, not an excuse to edit outside assigned areas.
