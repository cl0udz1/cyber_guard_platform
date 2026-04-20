# WEEK_5_TODO.md

## Week Goal

Align the frontend shell tightly with the backend scaffold and keep docs/tests synchronized.

## Target Outcome

A beginner can open the frontend and immediately know where scan, report, dashboard, public-threat, and workspace work belongs.

## Deliverables

- clear frontend ownership map
- stable frontend page groups
- stable shared frontend types
- docs/tests synced to the current shape

## Owner-By-Owner Tasks

| Owner | Tasks | Files |
|---|---|---|
| BANDER SHOWAIL | Confirm frontend auth/workspace assumptions are still correct. | `frontend/src/pages/auth/*`, `frontend/src/pages/workspace/*`, `backend/app/schemas/auth.py`, `workspace.py` |
| FARIS BIN SUMAYDI | Confirm scan page uses the right artifact and job terminology. | `frontend/src/pages/scan/*`, `frontend/src/types/scan.ts`, `backend/app/schemas/artifact.py`, `scan.py` |
| OMAR ABDURASHEED | Confirm adapter/AI/cache behavior is described correctly in the UI placeholders. | `frontend/src/pages/scan/*`, `frontend/src/features/scan-jobs/*`, `frontend/src/utils/copy.ts` |
| MUHANNAD ALKHARMANI | Confirm report/dashboard/public-review wording matches backend flow. | `frontend/src/pages/reports/*`, `frontend/src/pages/dashboard/*`, `frontend/src/pages/public-threats/*`, `frontend/src/pages/admin/*` |
| GHAZA ALAMTRAFA | Own frontend cleanup, placeholder quality, and page/component alignment. | `frontend/src/app/*`, `frontend/src/pages/*`, `frontend/src/components/*`, `frontend/src/types/*`, `frontend/src/mocks/*` |
| ABDULLAH BAALI | Own test/doc sync and make sure the weekly/status docs and shared endpoint map still match the repo. | `backend/tests/*`, `frontend/src/api/endpoints.ts`, `docs/IMPLEMENTATION_STATUS.md`, `docs/TEST_PLAN.md`, `docs/WEEK_5_TODO.md` |

## Files Involved

- `frontend/src/app/*`
- `frontend/src/pages/*`
- `frontend/src/components/*`
- `frontend/src/types/*`
- `frontend/src/api/endpoints.ts`
- `docs/TEST_PLAN.md`

## Dependencies

- Ghaza depends on backend contracts remaining stable
- Abdullah depends on frontend structure not drifting away from docs

## Definition Of Done

- frontend folders map cleanly to the backend domains
- page ownership is obvious
- build stays green
- docs/tests describe the same structure users see in the repo

## Supervisor / Demo Readiness Checkpoint

- show the frontend shell and explain which teammate owns which page group

## Carry-Over Notes

- note any UI naming mismatches here
- note any page/component ownership conflicts here
