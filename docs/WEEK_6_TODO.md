# WEEK_6_TODO.md

## Week Goal

Stabilize the scaffold, clean the handoff path, and make the repo supervisor-ready.

## Target Outcome

The repo is easy to review, easy to assign from, and easy to continue building.

## Deliverables

- passing validation baseline
- current docs and diagrams
- clean handoff notes
- evidence checklist ready
- supervisor-ready progress summary

## Owner-By-Owner Tasks

| Owner | Tasks | Files |
|---|---|---|
| BANDER SHOWAIL | Review auth/org/workspace/RBAC files for clarity and TODO quality. | `backend/app/api/routes/auth.py`, `users.py`, `orgs.py`, `workspaces.py`, `backend/app/core/permissions.py` |
| FARIS BIN SUMAYDI | Review scan entry files for readability and clear TODOs. | `backend/app/api/routes/scan_jobs.py`, `backend/app/services/artifact_service.py`, `normalization_service.py`, `ioc_extraction_service.py` |
| OMAR ABDURASHEED | Review orchestration/adapters/AI/cache files for clean placeholder discipline. | `backend/app/services/scan_orchestrator.py`, `backend/app/services/enrichment/*`, `backend/app/services/ai/*`, `backend/app/services/caching_service.py` |
| MUHANNAD ALKHARMANI | Review reports/dashboard/public/admin files for privacy-safe wording and structure. | `backend/app/api/routes/reports.py`, `dashboard.py`, `public_threats.py`, `admin_reviews.py`, `backend/app/services/public_sharing_service.py`, `sanitization_service.py` |
| GHAZA ALAMTRAFA | Review frontend shell/page/component readability and assignment clarity. | `frontend/src/app/*`, `frontend/src/pages/*`, `frontend/src/components/*` |
| ABDULLAH BAALI | Run tests/build, update status/evidence/contract docs, and prepare supervisor update summary. | `backend/tests/*`, `frontend/src/api/endpoints.ts`, `docs/API_CONTRACT.md`, `docs/IMPLEMENTATION_STATUS.md`, `docs/EVIDENCE_INDEX.md`, `docs/SUPERVISOR_UPDATE_TEMPLATE.md`, `docs/HANDOFF_CHECKLIST.md` |

## Files Involved

- `backend/tests/*`
- `frontend/src/*`
- `docs/*`
- `docs/diagrams/*`

## Dependencies

- all owners must leave clear TODOs or blocker notes
- Abdullah needs final updates from all owners before freezing the supervisor-facing docs

## Definition Of Done

- `pytest -q` passes
- `npm run build` passes
- implementation status is current
- weekly TODO carry-over notes are honest and usable
- repo can be handed to the supervisor or a new teammate without confusion

## Supervisor / Demo Readiness Checkpoint

- prepare one short update using `docs/SUPERVISOR_UPDATE_TEMPLATE.md`

## Carry-Over Notes

- record unfinished items for the next cycle
- record blockers that need supervisor input
