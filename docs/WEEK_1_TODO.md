# WEEK_1_TODO.md

## Week Goal

Make sure every teammate understands the refreshed Cyber Guard scaffold, the assignment split, the branch workflow, and the privacy boundary before feature work starts.

## Target Outcome

The team is branch-ready, assignment-ready, and using one shared coordination flow.

## Deliverables

- assignment map finalized with names
- contributing/workflow docs understood by everyone
- branch names created
- status tracker baseline filled
- repo structure verified by all owners

## Owner-By-Owner Tasks

| Owner | Tasks | Files |
|---|---|---|
| BANDER SHOWAIL | Review auth/org/workspace route and schema boundaries. Confirm any naming issues now. | `backend/app/api/routes/auth.py`, `users.py`, `orgs.py`, `workspaces.py`, `backend/app/schemas/auth.py`, `org.py`, `workspace.py` |
| FARIS BIN SUMAYDI | Review scan job and artifact intake flow. Confirm artifact types and normalized input assumptions. | `backend/app/api/routes/scan_jobs.py`, `backend/app/schemas/artifact.py`, `scan.py`, `backend/app/services/artifact_service.py`, `normalization_service.py` |
| OMAR ABDURASHEED | Review enrichment/AI/cache/orchestrator ownership. Confirm which files are adapter-specific. | `backend/app/services/scan_orchestrator.py`, `backend/app/services/enrichment/*`, `backend/app/services/ai/*`, `backend/app/services/caching_service.py` |
| MUHANNAD ALKHARMANI | Review report/dashboard/public-sharing/admin-review backend flow. Confirm boundaries. | `backend/app/api/routes/reports.py`, `dashboard.py`, `public_threats.py`, `admin_reviews.py`, `backend/app/services/report_service.py`, `public_sharing_service.py` |
| GHAZA ALAMTRAFA | Review page/component ownership and frontend file grouping. | `frontend/src/app/*`, `frontend/src/pages/*`, `frontend/src/components/*`, `frontend/src/types/*` |
| ABDULLAH BAALI | Finalize docs workflow, status tracker baseline, weekly coordination setup, and initial contract/test alignment notes. | `README.md`, `CONTRIBUTING.md`, `docs/TEAM_WORKFLOW.md`, `docs/IMPLEMENTATION_STATUS.md`, `docs/ASSIGNMENT_MAP.md`, `docs/API_CONTRACT.md`, `docs/TEST_PLAN.md` |

## Files Involved

- `README.md`
- `CONTRIBUTING.md`
- `docs/ASSIGNMENT_MAP.md`
- `docs/IMPLEMENTATION_STATUS.md`
- `docs/TEAM_WORKFLOW.md`
- `docs/SUBMISSION_RULES.md`

## Dependencies

- Nobody starts broad implementation until all six owners agree the file split is clear.
- Abdullah needs owner confirmation from everyone before freezing the tracker baseline.

## Definition Of Done

- every teammate has read the required docs
- every teammate has their branch name
- status tracker is filled with owners and baseline notes
- no confusion remains about who owns what

## Supervisor / Demo Readiness Checkpoint

- team can explain the updated product concept and assignment split in one short meeting

## Carry-Over Notes

- add blockers here if any teammate still cannot clone, branch, or identify their files
- add renaming issues here if any schema/route names still feel unclear
