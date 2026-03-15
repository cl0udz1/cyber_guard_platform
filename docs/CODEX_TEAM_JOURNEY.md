# CODEX_TEAM_JOURNEY.md

## Purpose

This file is the easiest AI onboarding entry point for this repo.

Each teammate can point Codex to this file, say their name, and let Codex narrow itself to the correct files, boundaries, and first tasks.

This file is written for both:

- the student using Codex
- the AI assistant reading the repo context

## Project Truth For AI

If an AI tool reads this file, treat the following as required:

- local filesystem is the source of truth
- this repository is a scaffold, not a finished app
- do not invent extra product scope
- do not edit files outside the named teammate section
- keep code simple, readable, and student-explainable
- preserve placeholders, TODOs, and ownership hints where they still belong
- inspect existing files before making changes
- do not replace the scaffold with a polished implementation

## Product Summary

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

Critical rule:

- public threat data must not link back to private identity or workspace data

## How A Teammate Should Use This File

1. Open the full repo in VS Code.
2. Open Codex.
3. Paste this starter message:

```text
Read docs/CODEX_TEAM_JOURNEY.md.
I am [YOUR NAME].
Use only my section.

First tell me:
1) my owned area
2) the files I should focus on first
3) the files I should avoid unless coordinated
4) my safest first task this week

Do not edit anything yet.
```

4. After Codex explains your area, use this follow-up:

```text
Now inspect only my listed files and suggest one small scaffold-level change.
Keep it simple and easy to explain later.
Do not add extra features, files, or dependencies.
Do not edit anything outside my area.
```

## Name Map

Use one of these exact names:

- BANDER SHOWAIL
- FARIS BIN SUMAYDI
- OMAR ABDURASHEED
- MUHANNAD ALKHARMANI
- GHAZA ALAMTRAFA
- ABDULLAH BAALI

## Shared Rules For Every Teammate

- create your own branch before real edits
- stay inside your assigned files
- update the weekly TODO file and implementation status when work changes
- if blocked, leave notes instead of disappearing
- if Codex starts inventing architecture, stop and correct it
- if code becomes too advanced to explain, simplify it before keeping it

## A - BANDER SHOWAIL

- Student ID: `220028863`
- Branch: `bander/auth-orgs`
- Area: Auth, users, orgs, workspaces, memberships, RBAC
- First files:
  - `backend/app/api/routes/auth.py`
  - `backend/app/api/routes/users.py`
  - `backend/app/api/routes/orgs.py`
  - `backend/app/api/routes/workspaces.py`
  - `backend/app/schemas/auth.py`
  - `backend/app/schemas/user.py`
  - `backend/app/schemas/org.py`
  - `backend/app/schemas/workspace.py`
  - `backend/app/models/user.py`
  - `backend/app/models/organization.py`
  - `backend/app/models/workspace.py`
  - `backend/app/models/membership.py`
  - `backend/app/core/permissions.py`
- Avoid unless coordinated:
  - `backend/app/api/deps.py`
  - `docs/API_CONTRACT.md`
  - frontend files
- Week 1 focus:
  - confirm route names and schema names are clear
  - confirm org/workspace/membership boundaries are readable
  - add only small scaffold improvements if needed
- Good first edits:
  - clarify route headers and TODO comments
  - tighten schema field comments or example placeholders
  - make RBAC notes easier to follow
- Done when:
  - auth/workspace contract is easier to understand
  - no random auth logic is overbuilt
  - code remains simple to explain

### Prompt For Bander

```text
Read docs/CODEX_TEAM_JOURNEY.md.
I am BANDER SHOWAIL.
Use only my section.

Then inspect only these files:
- backend/app/api/routes/auth.py
- backend/app/api/routes/users.py
- backend/app/api/routes/orgs.py
- backend/app/api/routes/workspaces.py
- backend/app/schemas/auth.py
- backend/app/schemas/user.py
- backend/app/schemas/org.py
- backend/app/schemas/workspace.py
- backend/app/models/user.py
- backend/app/models/organization.py
- backend/app/models/workspace.py
- backend/app/models/membership.py
- backend/app/core/permissions.py

First summarize:
1) what these files currently do
2) what is still placeholder
3) the safest next small scaffold-level improvement

Do not edit anything yet.
Do not invent real auth implementation.
Keep everything easy for a student to explain.
```

## B - FARIS BIN SUMAYDI

- Student ID: `220053973`
- Branch: `faris/scan-pipeline`
- Area: Artifact submission, scan jobs, normalization, pipeline entry flow
- First files:
  - `backend/app/api/routes/scan_jobs.py`
  - `backend/app/schemas/artifact.py`
  - `backend/app/schemas/scan.py`
  - `backend/app/services/artifact_service.py`
  - `backend/app/services/normalization_service.py`
  - `backend/app/services/ioc_extraction_service.py`
  - `backend/app/utils/url_tools.py`
  - `backend/app/utils/email_tools.py`
  - `backend/app/utils/hashing.py`
- Avoid unless coordinated:
  - `backend/app/services/enrichment/*`
  - `backend/app/services/ai/*`
  - frontend files
- Week 1 focus:
  - make artifact intake flow readable
  - keep file/hash, URL, and email indicator paths clear
  - avoid implementing full scan execution
- Good first edits:
  - improve placeholder comments for submission flow
  - make schema intent clearer
  - keep normalization boundaries obvious
- Done when:
  - scan intake path is understandable
  - artifact types are clearly represented
  - the handoff to orchestration is visible but still scaffold-level

### Prompt For Faris

```text
Read docs/CODEX_TEAM_JOURNEY.md.
I am FARIS BIN SUMAYDI.
Use only my section.

Then inspect only these files:
- backend/app/api/routes/scan_jobs.py
- backend/app/schemas/artifact.py
- backend/app/schemas/scan.py
- backend/app/services/artifact_service.py
- backend/app/services/normalization_service.py
- backend/app/services/ioc_extraction_service.py
- backend/app/utils/url_tools.py
- backend/app/utils/email_tools.py
- backend/app/utils/hashing.py

First summarize:
1) current scan intake flow
2) what is still placeholder
3) one small safe improvement that keeps this scaffold simple

Do not edit anything yet.
Do not add real integrations or advanced pipeline logic.
Keep everything student-readable.
```

## C - OMAR ABDURASHEED

- Student ID: `220042711`
- Branch: `omar/integrations-ai`
- Area: Enrichment adapters, AI mode routing, caching, orchestration support
- First files:
  - `backend/app/services/scan_orchestrator.py`
  - `backend/app/services/caching_service.py`
  - `backend/app/services/enrichment/base.py`
  - `backend/app/services/enrichment/virustotal_client.py`
  - `backend/app/services/enrichment/source_a_client.py`
  - `backend/app/services/enrichment/source_b_client.py`
  - `backend/app/services/enrichment/source_c_client.py`
  - `backend/app/services/ai/base.py`
  - `backend/app/services/ai/local_ai_service.py`
  - `backend/app/services/ai/api_ai_service.py`
- Avoid unless coordinated:
  - `backend/app/api/routes/scan_jobs.py`
  - docs contract files
  - frontend files
- Week 1 focus:
  - keep adapter boundaries consistent
  - keep optional AI modes clear
  - avoid turning stubs into full external integrations
- Good first edits:
  - standardize comments or interfaces across adapters
  - clarify orchestration handoff notes
  - make caching purpose more obvious
- Done when:
  - adapter outputs feel consistent
  - AI routing is easy to explain
  - orchestration shape is cleaner without adding complexity

### Prompt For Omar

```text
Read docs/CODEX_TEAM_JOURNEY.md.
I am OMAR ABDURASHEED.
Use only my section.

Then inspect only these files:
- backend/app/services/scan_orchestrator.py
- backend/app/services/caching_service.py
- backend/app/services/enrichment/base.py
- backend/app/services/enrichment/virustotal_client.py
- backend/app/services/enrichment/source_a_client.py
- backend/app/services/enrichment/source_b_client.py
- backend/app/services/enrichment/source_c_client.py
- backend/app/services/ai/base.py
- backend/app/services/ai/local_ai_service.py
- backend/app/services/ai/api_ai_service.py

First summarize:
1) the current orchestration and adapter structure
2) what is still placeholder
3) the safest next small improvement

Do not edit anything yet.
Do not implement real external clients.
Keep the structure simple and consistent.
```

## D - MUHANNAD ALKHARMANI

- Student ID: `220041379`
- Branch: `muhannad/reports-dashboard`
- Area: Reports, dashboard backend, public sharing flow, admin review flow, integration coordination
- First files:
  - `backend/app/api/routes/reports.py`
  - `backend/app/api/routes/dashboard.py`
  - `backend/app/api/routes/public_threats.py`
  - `backend/app/api/routes/admin_reviews.py`
  - `backend/app/schemas/report.py`
  - `backend/app/schemas/dashboard.py`
  - `backend/app/schemas/public_threats.py`
  - `backend/app/schemas/admin_review.py`
  - `backend/app/services/report_service.py`
  - `backend/app/services/dashboard_service.py`
  - `backend/app/services/public_sharing_service.py`
  - `backend/app/services/admin_review_service.py`
  - `backend/app/services/sanitization_service.py`
  - `backend/app/models/threat_report.py`
  - `backend/app/models/public_report.py`
  - `backend/app/models/admin_review.py`
- Avoid unless coordinated:
  - `backend/app/services/scan_orchestrator.py`
  - frontend page files
  - `docs/TEST_PLAN.md`
- Week 1 focus:
  - make report flow clear from scan output to report
  - keep public sharing disconnected from private identity/workspace data
  - keep admin review flow readable and assignable
- Good first edits:
  - tighten route/service headers
  - clarify report and dashboard schema intent
  - strengthen sanitization/public-sharing TODO notes
- Done when:
  - report flow is easy to explain
  - Disconnect by Design is visible in the scaffold
  - nothing is overbuilt beyond the placeholder architecture

### Prompt For Muhannad

```text
Read docs/CODEX_TEAM_JOURNEY.md.
I am MUHANNAD ALKHARMANI.
Use only my section.

Then inspect only these files:
- backend/app/api/routes/reports.py
- backend/app/api/routes/dashboard.py
- backend/app/api/routes/public_threats.py
- backend/app/api/routes/admin_reviews.py
- backend/app/schemas/report.py
- backend/app/schemas/dashboard.py
- backend/app/schemas/public_threats.py
- backend/app/schemas/admin_review.py
- backend/app/services/report_service.py
- backend/app/services/dashboard_service.py
- backend/app/services/public_sharing_service.py
- backend/app/services/admin_review_service.py
- backend/app/services/sanitization_service.py
- backend/app/models/threat_report.py
- backend/app/models/public_report.py
- backend/app/models/admin_review.py

First summarize:
1) the private report flow
2) the public sharing and admin review flow
3) what is still placeholder
4) the safest first improvement

Do not edit anything yet.
Do not invent full persistence or review logic.
Keep it scaffold-level and easy to explain.
```

## E - GHAZA ALAMTRAFA

- Student ID: `220050709`
- Branch: `ghaza/frontend-flows`
- Area: Frontend scan, reports, dashboard, public threats, workspace UI
- First files:
  - `frontend/src/app/AppShell.tsx`
  - `frontend/src/pages/scan/ScanWorkspacePage.tsx`
  - `frontend/src/pages/reports/ReportsPage.tsx`
  - `frontend/src/pages/dashboard/DashboardPage.tsx`
  - `frontend/src/pages/public-threats/PublicThreatsPage.tsx`
  - `frontend/src/pages/workspace/WorkspacePage.tsx`
  - `frontend/src/components/scan/*`
  - `frontend/src/components/reports/*`
  - `frontend/src/components/dashboard/*`
  - `frontend/src/components/public-threats/*`
  - `frontend/src/components/admin-review/*`
  - `frontend/src/types/scan.ts`
  - `frontend/src/types/report.ts`
  - `frontend/src/types/dashboard.ts`
  - `frontend/src/types/publicThreat.ts`
- Avoid unless coordinated:
  - `frontend/src/api/endpoints.ts`
  - `docs/API_CONTRACT.md`
  - backend files
- Week 1 focus:
  - make page ownership obvious
  - keep page and component naming aligned with backend domains
  - avoid polished full UI work
- Good first edits:
  - improve page headers and placeholder copy
  - tighten type names if needed
  - make component grouping easier to understand
- Done when:
  - frontend ownership is clear
  - scaffold pages are readable
  - UI placeholders still match the project plan

### Prompt For Ghaza

```text
Read docs/CODEX_TEAM_JOURNEY.md.
I am GHAZA ALAMTRAFA.
Use only my section.

Then inspect only these files:
- frontend/src/app/AppShell.tsx
- frontend/src/pages/scan/ScanWorkspacePage.tsx
- frontend/src/pages/reports/ReportsPage.tsx
- frontend/src/pages/dashboard/DashboardPage.tsx
- frontend/src/pages/public-threats/PublicThreatsPage.tsx
- frontend/src/pages/workspace/WorkspacePage.tsx
- frontend/src/components/scan/*
- frontend/src/components/reports/*
- frontend/src/components/dashboard/*
- frontend/src/components/public-threats/*
- frontend/src/components/admin-review/*
- frontend/src/types/scan.ts
- frontend/src/types/report.ts
- frontend/src/types/dashboard.ts
- frontend/src/types/publicThreat.ts

First summarize:
1) current page and component structure
2) what is still placeholder
3) one small safe improvement that keeps the frontend scaffold clear

Do not edit anything yet.
Do not redesign the full UI.
Keep the code and copy simple and easy to explain.
```

## F - ABDULLAH BAALI

- Student ID: `220003069`
- Branch: `abdullah/docs-tests`
- Area: Docs, tests, diagrams, implementation tracking, integration alignment
- First files:
  - `docs/API_CONTRACT.md`
  - `docs/TEST_PLAN.md`
  - `docs/ARCHITECTURE.md`
  - `docs/DATA_FLOW.md`
  - `docs/IMPLEMENTATION_STATUS.md`
  - `docs/WEEK_1_TODO.md`
  - `docs/WEEK_2_TODO.md`
  - `docs/WEEK_3_TODO.md`
  - `docs/WEEK_4_TODO.md`
  - `docs/WEEK_5_TODO.md`
  - `docs/WEEK_6_TODO.md`
  - `docs/diagrams/*`
  - `backend/tests/unit/*`
  - `backend/tests/integration/*`
  - `backend/tests/contract/*`
  - `frontend/src/api/endpoints.ts`
- Avoid unless coordinated:
  - backend feature implementation files
  - frontend page logic
  - service logic owned by other teammates
- Week 1 focus:
  - keep docs aligned with the local repo truth
  - keep tests and diagrams pointed at the same contracts
  - keep trackers current for the team
- Good first edits:
  - tighten docs wording where repo truth changed
  - mark tests or diagrams that still need alignment
  - clean status wording for clarity
- Done when:
  - docs and trackers are current
  - no obvious contract mismatch remains
  - handoff notes are easy for the integrator to follow

### Prompt For Abdullah

```text
Read docs/CODEX_TEAM_JOURNEY.md.
I am ABDULLAH BAALI.
Use only my section.

Then inspect only these files:
- docs/API_CONTRACT.md
- docs/TEST_PLAN.md
- docs/ARCHITECTURE.md
- docs/DATA_FLOW.md
- docs/IMPLEMENTATION_STATUS.md
- docs/WEEK_1_TODO.md
- docs/WEEK_2_TODO.md
- docs/WEEK_3_TODO.md
- docs/WEEK_4_TODO.md
- docs/WEEK_5_TODO.md
- docs/WEEK_6_TODO.md
- docs/diagrams/*
- backend/tests/unit/*
- backend/tests/integration/*
- backend/tests/contract/*
- frontend/src/api/endpoints.ts

First summarize:
1) what is aligned well already
2) what docs or tests still need sync
3) the safest next small update

Do not edit anything yet.
Do not rewrite product scope.
Keep changes practical and easy for the team to maintain.
```

## If Codex Starts Doing Too Much

Use this correction prompt:

```text
Stop.
Use the local repository as the source of truth.
Stay inside my assigned files only.
Do not invent extra routes, models, pages, dependencies, or product features.
Redo this as one small scaffold-level change that is easy for a student to explain later.
```

## Final Reminder

This file is meant to make starting easier, not to let AI take over the project.

Every teammate still needs to:

- review the changed files
- understand the result
- keep the scope small
- explain the work clearly later
