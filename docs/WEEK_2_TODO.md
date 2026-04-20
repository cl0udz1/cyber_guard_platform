# WEEK_2_TODO.md

## Week Goal

Stabilize models, schemas, contracts, auth rules, and workspace boundaries.

## Target Outcome

The backend contract surface is clear enough that frontend and service work can proceed without guessing names.

## Deliverables

- stable auth/org/workspace/membership schema names
- stable artifact/report/public-threat schema names
- API contract aligned with actual route files
- implementation tracker updated with any dependency changes

## Owner-By-Owner Tasks

| Owner | Tasks | Files |
|---|---|---|
| BANDER SHOWAIL | Finalize auth, user, org, workspace, and permission scaffolds. | `backend/app/api/routes/auth.py`, `users.py`, `orgs.py`, `workspaces.py`, `backend/app/core/permissions.py`, `backend/app/models/user.py`, `organization.py`, `workspace.py`, `membership.py` |
| FARIS BIN SUMAYDI | Finalize artifact submission and scan job schema boundaries. | `backend/app/schemas/artifact.py`, `scan.py`, `backend/app/api/routes/scan_jobs.py` |
| OMAR ABDURASHEED | Review adapter and cache interfaces to ensure downstream compatibility. | `backend/app/services/scan_orchestrator.py`, `backend/app/services/enrichment/base.py`, `backend/app/services/ai/base.py`, `backend/app/services/caching_service.py` |
| MUHANNAD ALKHARMANI | Finalize report/dashboard/public/admin schema shape. | `backend/app/schemas/report.py`, `dashboard.py`, `public_threats.py`, `admin_review.py`, `backend/app/api/routes/reports.py`, `dashboard.py`, `public_threats.py`, `admin_reviews.py` |
| GHAZA ALAMTRAFA | Mirror stable backend contract names into frontend types and page assumptions. | `frontend/src/types/*`, `frontend/src/pages/*`, `frontend/src/api/endpoints.ts` |
| ABDULLAH BAALI | Update API contract, architecture/data-flow docs, status tracker, and test plan after names are locked. | `docs/API_CONTRACT.md`, `docs/ARCHITECTURE.md`, `docs/DATA_FLOW.md`, `docs/IMPLEMENTATION_STATUS.md`, `docs/TEST_PLAN.md` |

## Files Involved

- `backend/app/models/*`
- `backend/app/schemas/*`
- `backend/app/api/routes/*`
- `docs/API_CONTRACT.md`
- `frontend/src/types/*`

## Dependencies

- Ghaza and Abdullah need Band/Faris/Muhannad contract names to stop moving.
- Public/private separation must stay explicit in public report and admin review schemas.

## Definition Of Done

- the team can point to one stable file for each domain contract
- backend route names and main schema fields stop changing casually
- frontend owner can safely type against current backend docs

## Supervisor / Demo Readiness Checkpoint

- show one clean route map and one clean entity map with no old guest-scan leftovers

## Carry-Over Notes

- list any schema names still under discussion
- list any shared file conflicts needing integrator coordination
