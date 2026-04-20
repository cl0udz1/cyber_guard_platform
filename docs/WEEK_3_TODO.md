# WEEK_3_TODO.md

## Week Goal

Make the scan pipeline scaffold practical: artifact intake, normalization, IOC extraction, cache behavior, enrichment adapters, and AI mode routing.

## Target Outcome

The scan job flow reads like a real system even though it is still scaffold-level.

## Deliverables

- understandable `scan-jobs` path
- clear adapter boundaries
- clear AI mode boundaries
- duplicate submission behavior visible

## Owner-By-Owner Tasks

| Owner | Tasks | Files |
|---|---|---|
| BANDER SHOWAIL | Confirm auth/workspace access assumptions for scan routes. | `backend/app/api/deps.py`, `backend/app/api/routes/scan_jobs.py` |
| FARIS BIN SUMAYDI | Refine artifact intake, normalization, and pipeline entry comments/TODOs. | `backend/app/services/artifact_service.py`, `normalization_service.py`, `ioc_extraction_service.py`, `backend/app/utils/url_tools.py`, `email_tools.py`, `hashing.py` |
| OMAR ABDURASHEED | Own orchestration, adapters, cache behavior, and AI routing structure. | `backend/app/services/scan_orchestrator.py`, `backend/app/services/caching_service.py`, `backend/app/services/enrichment/*`, `backend/app/services/ai/*` |
| MUHANNAD ALKHARMANI | Confirm report-ready output shape from the pipeline. | `backend/app/services/report_service.py`, `backend/app/schemas/report.py`, `backend/app/api/routes/reports.py` |
| GHAZA ALAMTRAFA | Make scan-related frontend pages/components reflect the backend pipeline steps clearly. | `frontend/src/pages/scan/ScanWorkspacePage.tsx`, `frontend/src/components/scan/*`, `frontend/src/types/scan.ts` |
| ABDULLAH BAALI | Add or refine tests covering duplicate submission, adapter shape, and pipeline contract. | `backend/tests/integration/test_scan_jobs_routes.py`, `backend/tests/unit/test_enrichment_adapters.py`, `backend/tests/contract/test_api_contract_shape.py`, `docs/TEST_PLAN.md` |

## Files Involved

- `backend/app/services/scan_orchestrator.py`
- `backend/app/services/enrichment/*`
- `backend/app/services/ai/*`
- `backend/app/services/caching_service.py`
- `frontend/src/pages/scan/*`

## Dependencies

- Omar depends on Faris for stable artifact input shape.
- Muhannad depends on Omar for report-ready outputs.
- Ghaza depends on current request/response names staying stable.

## Definition Of Done

- same submission shape is understandable across backend docs, schemas, tests, and frontend placeholders
- multi-source enrichment is visible, not hidden behind one old source
- AI remains optional, not forced into the pipeline

## Supervisor / Demo Readiness Checkpoint

- show one scan submission example and explain the steps from submission to report generation

## Carry-Over Notes

- note any adapter naming or AI mode questions here
- record any unfinished caching behavior
