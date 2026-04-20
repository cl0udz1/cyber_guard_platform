"""
Purpose:
    Shared pytest fixtures for the refreshed Cyber Guard scaffold.
Inputs:
    FastAPI app and JWT helper utilities.
Outputs:
    Test client plus authenticated headers for org and admin roles.
Dependencies:
    pytest, fastapi.testclient, backend app package.
TODO Checklist:
    - [ ] Add DB session fixtures once routes persist real data.
    - [ ] Add seeded organization/workspace fixtures when model tests begin.
"""

import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_cyber_guard.db")

from app.core.security import create_access_token
from app.db.base import Base
from app.db.session import engine
from app.main import app


@pytest.fixture()
def client() -> TestClient:
    """Return a plain TestClient for scaffold route testing."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def reset_db_schema() -> None:
    """Reset schema for each test so DB-backed services remain deterministic."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture()
def org_auth_header() -> dict[str, str]:
    """Org-scoped auth header for standard private routes."""
    token = create_access_token(
        {
            "sub": "analyst@example.edu",
            "email": "analyst@example.edu",
            "role": "org_admin",
            "organization_id": "demo-org",
            "workspace_id": "demo-workspace",
        }
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def admin_auth_header() -> dict[str, str]:
    """Platform-admin auth header for moderation routes."""
    token = create_access_token(
        {
            "sub": "platform.admin@example.edu",
            "email": "platform.admin@example.edu",
            "role": "platform_admin",
            "organization_id": "demo-org",
            "workspace_id": "demo-workspace",
        }
    )
    return {"Authorization": f"Bearer {token}"}
