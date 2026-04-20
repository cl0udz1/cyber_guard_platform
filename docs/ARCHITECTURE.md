# ARCHITECTURE.md

## Purpose

This document explains the major parts of the refreshed Cyber Guard scaffold. It is intentionally practical: the goal is to help the team know where code belongs and how the system is supposed to fit together.

## System Shape

Cyber Guard remains a single web application stack:

- FastAPI backend
- React frontend
- SQLAlchemy models for future persistence
- scaffold async scan orchestration inside the backend service layer

This is not a microservice architecture. The repo is optimized for student implementation, not platform engineering complexity.

## Backend

### API Layer

`backend/app/api/routes/` groups the contract by domain:

- `auth.py`
- `users.py`
- `orgs.py`
- `workspaces.py`
- `scan_jobs.py`
- `reports.py`
- `public_threats.py`
- `admin_reviews.py`
- `dashboard.py`
- `integrations.py`

Routes are thin. They should validate access, call services, and return typed schemas.
The `integrations.py` surface is intentionally small: it exposes adapter availability and public API status without turning adapter internals into route logic.

### Core Layer

`backend/app/core/` holds:

- configuration
- security helpers
- permission helpers
- feature flags
- logging setup

This is where cross-cutting behavior belongs, not inside individual route files.

### Data Layer

`backend/app/models/` defines the domain entities:

- private identity/workspace entities
- artifact submission and scan entities
- report and review entities
- public report entity

The models are present so ownership is clear even though the repo is still scaffold-heavy.

### Service Layer

`backend/app/services/` is the main implementation surface for the team.

Important responsibilities:

- `auth_service.py`: scaffold auth behavior
- `artifact_service.py`: accepted artifact submission shape
- `normalization_service.py`: artifact normalization rules
- `ioc_extraction_service.py`: IOC extraction placeholder
- `scan_orchestrator.py`: coordinates the scan pipeline
- `services/enrichment/`: threat-intel adapter slots
- `services/ai/`: local vs API AI mode slots
- `report_service.py`: private threat report building
- `public_sharing_service.py`: anonymized sharing workflow
- `admin_review_service.py`: moderation queue
- `dashboard_service.py`: dashboard summary builder
- `sanitization_service.py`: Disconnect by Design guardrails
- `caching_service.py`: duplicate-submission behavior

## Frontend

The frontend is organized around assignment-friendly page groups:

- `pages/auth/`
- `pages/workspace/`
- `pages/scan/`
- `pages/reports/`
- `pages/dashboard/`
- `pages/public-threats/`
- `pages/admin/`

Component folders mirror those domains. The current UI is mostly placeholders, but the boundaries are deliberate so each teammate knows where real work should be implemented later.

## Async Jobs

The repo models scan work as async jobs even though the current scaffold executes inside one process. This is intentional. It lets the API contract, frontend flow, and documentation match the real product shape before the team adds a real queue/worker.
Tests and docs should describe that shape consistently: async from the product point of view, scaffold-inline from the current implementation point of view.

## Enrichment Adapters

The old single-source VirusTotal assumption is replaced with a multi-source adapter slot design:

- VirusTotal remains one adapter
- `source_a`, `source_b`, `source_c` are explicit placeholders for team-selected sources

This prevents the architecture from collapsing back into a VirusTotal-only mindset.

## AI Adapters

AI is optional and represented by two modes:

- local mode for privacy-sensitive deployments
- API mode for convenience

The scaffold intentionally keeps both behind small adapter files so the team can implement one, both, or neither without rewriting the scan pipeline.

## Public Sharing Boundary

This is the most important design rule in the repo:

- private identity/workspace/report data lives in the private platform domain
- public-safe threat content lives in the public threats domain
- sanitization is a deliberate policy gate
- public records must not expose direct identity/workspace linkage

That boundary appears in:

- models
- services
- API routes
- docs
- diagrams

If a future change weakens that separation, it should be treated as an architectural issue, not a small refactor.
