# TASK_CARDS.md

## Task Card A

- Owner: `220028863 - BANDER SHOWAIL`
- Goal: Lock the auth, user, org, workspace, membership, and RBAC scaffold so other owners can build on stable private-area boundaries.
- Files:
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
- Deliverables:
  - stable auth/workspace contracts
  - simple RBAC rules
  - clear membership assumptions
- Dependencies:
  - none to start
- Done when:
  - route names and field names stop changing
  - RBAC rules are visible in comments and helper functions
- Notes:
  - coordinate before touching shared docs or `api/deps.py`

## Task Card B

- Owner: `220053973 - FARIS BIN SUMAYDI`
- Goal: Own the artifact intake and scan job entry path.
- Files:
  - `backend/app/api/routes/scan_jobs.py`
  - `backend/app/schemas/artifact.py`
  - `backend/app/schemas/scan.py`
  - `backend/app/services/artifact_service.py`
  - `backend/app/services/normalization_service.py`
  - `backend/app/services/ioc_extraction_service.py`
  - `backend/app/utils/url_tools.py`
  - `backend/app/utils/email_tools.py`
  - `backend/app/utils/hashing.py`
- Deliverables:
  - clear artifact submission shapes
  - normalized scan job inputs
  - readable pipeline entry comments
- Dependencies:
  - Bander for auth/workspace context
- Done when:
  - another teammate can submit or mock a scan job without confusion
- Notes:
  - leave enrichment and AI routing to Omar unless coordinated

## Task Card C

- Owner: `220042711 - OMAR ABDURASHEED`
- Goal: Own enrichment, AI mode routing, cache behavior, and orchestration support.
- Files:
  - `backend/app/services/scan_orchestrator.py`
  - `backend/app/services/caching_service.py`
  - `backend/app/services/enrichment/*`
  - `backend/app/services/ai/*`
- Deliverables:
  - one clear multi-source adapter flow
  - local/API AI paths remain optional
  - cache behavior is easy to test
- Dependencies:
  - Faris for scan input shape
  - Muhannad for downstream report use
- Done when:
  - orchestration file is readable and adapter outputs stay consistent
- Notes:
  - do not push real external integrations unless the team agrees on scope

## Task Card D

- Owner: `220041379 - MUHANNAD ALKHARMANI`
- Goal: Own private reports, dashboard backend outputs, public sharing backend flow, and admin review backend.
- Files:
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
- Deliverables:
  - report flow shape
  - dashboard response shape
  - publish request and review queue shape
- Dependencies:
  - Omar for orchestration outputs
- Done when:
  - report/public/review flow is understandable end to end
- Notes:
  - protect the privacy boundary in every public-sharing decision

## Task Card E

- Owner: `220050709 - GHAZA ALAMTRAFA`
- Goal: Own the frontend pages and components for scan, reports, dashboard, public threats, and workspace areas.
- Files:
  - `frontend/src/app/*`
  - `frontend/src/pages/scan/*`
  - `frontend/src/pages/reports/*`
  - `frontend/src/pages/dashboard/*`
  - `frontend/src/pages/public-threats/*`
  - `frontend/src/pages/workspace/*`
  - `frontend/src/components/*`
  - `frontend/src/types/*`
- Deliverables:
  - page groups match backend route groups
  - placeholders explain what belongs next
  - UI stays buildable
- Dependencies:
  - backend contract stability from Bander, Faris, Omar, and Muhannad
- Done when:
  - a teammate can open the UI files and know where to continue work
- Notes:
  - coordinate before editing `frontend/src/api/endpoints.ts`

## Task Card F

- Owner: `220003069 - ABDULLAH BAALI`
- Goal: Own docs, tests, diagrams, implementation tracking, integration alignment, and merge coordination.
- Files:
  - `docs/*`
  - `docs/diagrams/*`
  - `backend/tests/*`
  - `frontend/src/api/endpoints.ts`
- Deliverables:
  - current docs
  - current status tracker
  - current weekly TODO files
  - current tests/diagrams
- Dependencies:
  - stable naming from all other owners
- Done when:
  - repo coordination docs stay trustworthy
  - merges and handoffs are organized
- Notes:
  - act as integrator for fallback submissions from weak Git users
