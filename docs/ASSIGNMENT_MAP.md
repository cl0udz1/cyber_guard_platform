# ASSIGNMENT_MAP.md

## Team Assignment Summary

| Role | Student ID | Name | Domain Ownership |
|---|---|---|---|
| A | 220028863 | BANDER SHOWAIL | Auth, users, orgs, workspaces, memberships, RBAC |
| B | 220053973 | FARIS BIN SUMAYDI | Artifact submission, scan jobs, normalization, pipeline entry flow |
| C | 220042711 | OMAR ABDURASHEED | Enrichment adapters, AI mode routing, caching, orchestration support |
| D | 220041379 | MUHANNAD ALKHARMANI | Reports, dashboard backend, sharing/review backend flow, report schemas |
| E | 220050709 | GHAZA ALAMTRAFA | Frontend scan, reports, dashboard, public threats, workspace UI |
| F | 220003069 | ABDULLAH BAALI | Docs, tests, diagrams, status tracking, integration alignment, repo integration |

## Assignment Rules

- Each person owns a main area.
- Shared files require coordination first.
- Abdullah BAALI is the current integrator / maintainer for merge coordination.
- If your task depends on another owner, update the status tracker instead of silently waiting.

## A — 220028863 — BANDER SHOWAIL

- Domain ownership: Auth, users, orgs, workspaces, memberships, RBAC
- Main folders:
  - `backend/app/api/routes/`
  - `backend/app/schemas/`
  - `backend/app/core/`
  - `backend/app/models/`
- Main files:
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
  - shared frontend types
- Dependencies:
  - report and dashboard owners need stable auth/workspace context
  - Abdullah needs route names to stay stable for docs/tests
- Deliverables:
  - clear auth route behavior
  - clear workspace/org contract
  - simple RBAC rules for org vs admin areas
- Done criteria:
  - auth, org, and workspace route files are stable
  - membership and RBAC assumptions are documented in code/comments
  - no unclear field names remain in auth/org/workspace schemas
- Example first commit:
  - `backend: lock auth and workspace route contracts`

## B — 220053973 — FARIS BIN SUMAYDI

- Domain ownership: Artifact submission, scan jobs, normalization, pipeline entry flow
- Main folders:
  - `backend/app/api/routes/`
  - `backend/app/schemas/`
  - `backend/app/services/`
  - `backend/app/utils/`
- Main files:
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
  - `frontend/src/pages/scan/*`
- Dependencies:
  - Omar depends on stable pipeline inputs
  - Ghaza depends on stable scan job request/response shapes
- Deliverables:
  - clean artifact input handling
  - normalized scan job flow
  - clear handoff from submission into orchestration
- Done criteria:
  - scan job route and artifact schemas are understandable and stable
  - normalization logic is clearly separated from enrichment logic
  - comments explain what is still placeholder
- Example first commit:
  - `backend: shape scan job and artifact entry flow`

## C — 220042711 — OMAR ABDURASHEED

- Domain ownership: Enrichment adapters, AI mode routing, caching, orchestration support
- Main folders:
  - `backend/app/services/`
  - `backend/app/services/enrichment/`
  - `backend/app/services/ai/`
- Main files:
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
  - `docs/API_CONTRACT.md`
  - frontend files
- Dependencies:
  - Faris owns pipeline entry and artifact contract
  - Muhannad depends on report-ready outputs from orchestration
- Deliverables:
  - multi-source adapter structure stays clear
  - local/API AI modes remain optional and separable
  - duplicate scan behavior is visible through caching
- Done criteria:
  - orchestrator flow is readable
  - adapters follow one consistent result shape
  - AI routing is documented and not hard-coded into the wrong layer
- Example first commit:
  - `backend: refine enrichment and ai adapter flow`

## D — 220041379 — MUHANNAD ALKHARMANI

- Domain ownership: Reports, dashboard backend, sharing/review backend flow, report schemas
- Main folders:
  - `backend/app/api/routes/`
  - `backend/app/schemas/`
  - `backend/app/services/`
  - `backend/app/models/`
- Main files:
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
  - `frontend/src/pages/*`
  - `docs/TEST_PLAN.md`
- Dependencies:
  - Omar provides enrichment/orchestration outputs
  - Ghaza depends on stable report/dashboard/public schemas
  - Abdullah depends on stable sharing/review docs
- Deliverables:
  - private report flow
  - dashboard response flow
  - publish request and admin review structure
- Done criteria:
  - report and dashboard schemas are stable
  - public sharing flow respects Disconnect by Design
  - admin review behavior is documented and easy to follow
- Example first commit:
  - `backend: scaffold reports and review flow`

## E — 220050709 — GHAZA ALAMTRAFA

- Domain ownership: Frontend scan, reports, dashboard, public threats, workspace UI
- Main folders:
  - `frontend/src/app/`
  - `frontend/src/pages/`
  - `frontend/src/components/`
  - `frontend/src/types/`
  - `frontend/src/mocks/`
- Main files:
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
  - backend route/service files
- Dependencies:
  - Bander, Faris, Omar, and Muhannad must keep schemas stable
  - Abdullah needs page ownership reflected in docs
- Deliverables:
  - UI scaffold matches backend route groups
  - pages clearly show future work areas
  - components are grouped by domain, not mixed randomly
- Done criteria:
  - frontend stays buildable
  - page ownership remains obvious
  - placeholders still explain what belongs there next
- Example first commit:
  - `frontend: organize scan report and dashboard pages`

## F — 220003069 — ABDULLAH BAALI

- Domain ownership: Docs, tests, diagrams, status tracking, integration alignment, repo integration
- Main folders:
  - `docs/`
  - `backend/tests/`
  - `frontend/src/api/`
  - `frontend/src/features/`
- Main files:
  - `docs/ASSIGNMENT_MAP.md`
  - `docs/IMPLEMENTATION_STATUS.md`
  - `docs/TASK_CARDS.md`
  - `docs/SUBMISSION_RULES.md`
  - `docs/TEAM_WORKFLOW.md`
  - `docs/WEEK_1_TODO.md` to `docs/WEEK_6_TODO.md`
  - `docs/diagrams/*`
  - `backend/tests/unit/*`
  - `backend/tests/integration/*`
  - `backend/tests/contract/*`
  - `frontend/src/api/endpoints.ts`
- Avoid unless coordinated:
  - feature implementation files outside docs/tests/integration
  - backend service logic
  - frontend page logic
- Dependencies:
  - needs stable route names and schema names from all owners
  - acts as integration point for weak Git users
- Deliverables:
  - status tracker stays current
  - weekly TODO files stay actionable
  - tests and diagrams stay aligned to the scaffold
  - merges and handoffs are coordinated
- Done criteria:
  - docs reflect the current repo truth
  - tests remain runnable
  - handoffs from all teammates are recorded cleanly
- Example first commit:
  - `docs: set team workflow and status tracker`
