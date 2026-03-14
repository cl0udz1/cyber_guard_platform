# WEEK_4_TODO.md

## Week Goal

Stabilize the report, dashboard, anonymized sharing, and admin review scaffold.

## Target Outcome

The repo shows a complete private-to-public flow at scaffold level without breaking the privacy boundary.

## Deliverables

- report retrieval path
- dashboard backend summary path
- publish request path
- admin review queue path
- public-threat representation path

## Owner-By-Owner Tasks

| Owner | Tasks | Files |
|---|---|---|
| BANDER SHOWAIL | Review access expectations for report/public/admin routes. | `backend/app/api/deps.py`, `backend/app/core/permissions.py`, `backend/app/api/routes/admin_reviews.py` |
| FARIS BIN SUMAYDI | Confirm report flow still matches artifact/scan job assumptions. | `backend/app/schemas/scan.py`, `backend/app/schemas/artifact.py`, `backend/app/api/routes/scan_jobs.py` |
| OMAR ABDURASHEED | Confirm orchestration outputs are enough for report and dashboard usage. | `backend/app/services/scan_orchestrator.py`, `backend/app/services/enrichment/*`, `backend/app/services/ai/*` |
| MUHANNAD ALKHARMANI | Own report, dashboard, public sharing, sanitization, and admin review backend shape. | `backend/app/api/routes/reports.py`, `dashboard.py`, `public_threats.py`, `admin_reviews.py`, `backend/app/services/report_service.py`, `dashboard_service.py`, `public_sharing_service.py`, `admin_review_service.py`, `sanitization_service.py` |
| GHAZA ALAMTRAFA | Make report/dashboard/public-threat/workspace pages reflect current backend flow clearly. | `frontend/src/pages/reports/*`, `frontend/src/pages/dashboard/*`, `frontend/src/pages/public-threats/*`, `frontend/src/pages/workspace/*` |
| ABDULLAH BAALI | Update diagrams, test plan, and status tracker to match the report/public flow. | `docs/DATA_FLOW.md`, `docs/diagrams/*`, `docs/TEST_PLAN.md`, `docs/IMPLEMENTATION_STATUS.md` |

## Files Involved

- `backend/app/api/routes/reports.py`
- `backend/app/api/routes/dashboard.py`
- `backend/app/api/routes/public_threats.py`
- `backend/app/api/routes/admin_reviews.py`
- `backend/app/services/public_sharing_service.py`
- `backend/app/services/sanitization_service.py`
- `frontend/src/pages/reports/*`
- `frontend/src/pages/dashboard/*`
- `frontend/src/pages/public-threats/*`

## Dependencies

- public sharing depends on report outputs
- admin review depends on public sharing policy
- frontend display depends on backend schema stability

## Definition Of Done

- private report flow and public-sharing flow are both understandable
- public-safe content stays separate from identity/workspace data
- dashboard and report ownership are clearly visible

## Supervisor / Demo Readiness Checkpoint

- show the private report to public-threat path and explain the sanitization/review gate

## Carry-Over Notes

- note any unresolved privacy rules here
- note any shared backend/frontend naming conflicts here
