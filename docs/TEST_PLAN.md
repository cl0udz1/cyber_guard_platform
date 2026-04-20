# TEST_PLAN.md

## Purpose

This plan expands testing beyond simple endpoint checks. The updated product has private/public separation, RBAC, multi-source enrichment, optional AI paths, and moderated public publishing, so the test plan needs to reflect that.

## Test Layers

### Unit

- permission helpers
- sanitization/privacy rules
- normalization behavior
- enrichment adapter shape
- AI mode selection logic
- report generation rules
- cache behavior

### Integration

- auth and `/me`
- workspace/org route access
- scan job submission and polling
- report retrieval and publish request flow
- public feed access
- admin review access and decision flow

### Contract

- route surface in OpenAPI
- request/response field shape for major route groups
- phase-2 endpoints clearly labeled and isolated

### Manual

- frontend shell navigation
- role-based page expectations
- dashboard and public threats content review
- assignment map and TODO workflow review

## Priority Coverage Areas

| Area | Why It Matters | Suggested Coverage |
|---|---|---|
| Auth + RBAC | Prevents wrong users from reaching private/admin surfaces | route tests for auth, `/me`, admin review denial/allow |
| Sanitization + privacy | Critical design rule | unit tests for forbidden keys and sanitized summaries |
| Multi-source adapters | Replaces old single-source assumption | unit tests for adapter outputs and orchestrator aggregation |
| AI mode selection | Local vs API behavior changes pipeline expectations | unit tests for local/api/off mode branches |
| Report generation | Core user-facing deliverable | integration test from scan job to report retrieval |
| Admin review flow | Required for external public sharing governance | integration tests for queue and decisions |
| Public threats publishing | Must remain identity-safe | publish-request validation and public feed tests |
| Caching / duplicates | Important for repeat submissions and demo stability | duplicate submission test for same normalized artifact |

## Suggested Automated Suite

### Current Scaffold Tests

- `backend/tests/unit/test_permissions.py`
- `backend/tests/unit/test_sanitization_service.py`
- `backend/tests/unit/test_enrichment_adapters.py`
- `backend/tests/integration/test_auth_routes.py`
- `backend/tests/integration/test_scan_jobs_routes.py`
- `backend/tests/integration/test_public_threats_routes.py`
- `backend/tests/contract/test_api_contract_shape.py`

Current local baseline:

- the current automated suite passes locally
- auth, scan jobs, and public threats already have scaffold integration coverage
- permissions, sanitization, enrichment adapter shape, and API route presence already have automated checks

### Next Tests To Add

- org/workspace creation authorization
- report retrieval and publish-request flow
- report publish-request sanitizer edge cases
- external upload review request path
- admin review queue and decision success path
- integrations catalog response shape
- dashboard response shape and filters
- AI mode `off` path

## Manual Checklist

1. Open the frontend scaffold shell and confirm all sections are visible.
2. Confirm the repo tree matches the assignment map.
3. Create a scan job via API and verify a report ID is returned.
4. Retrieve the report and confirm source summary plus AI summary fields exist.
5. Request publication and confirm the response is review-oriented, not directly linked to org/workspace fields.
6. Open the public threats endpoint and confirm it exposes only public-safe data.
7. Verify admin review routes reject non-admin callers.

## Exit Criteria

- unit, integration, and contract tests pass locally
- the public/private boundary has at least one dedicated automated test
- route groups in docs and OpenAPI match
- MVP route groups that exist in `docs/API_CONTRACT.md` are either covered by tests now or listed above as next coverage work
- weekly TODO files point to test ownership clearly
