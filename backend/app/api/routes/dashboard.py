"""
Purpose:
    Workspace dashboard overview endpoint.
Inputs:
    Authenticated principal context.
Outputs:
    High-level dashboard metrics for the current workspace.
Dependencies:
    Dashboard service and auth dependency.
TODO Checklist:
    - [ ] Add time-range query parameters once chart work starts.
    - [ ] Replace placeholder counts with DB-backed aggregates.
"""

from fastapi import APIRouter, Depends
from datetime import datetime

from app.api.deps import get_current_principal, get_dashboard_service
from app.schemas.auth import CurrentPrincipal
from app.schemas.dashboard import DashboardOverviewResponse
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/overview", response_model=DashboardOverviewResponse)
async def get_dashboard_overview(
    principal: CurrentPrincipal = Depends(get_current_principal),
    dashboard_service: DashboardService = Depends(get_dashboard_service),
    start_date: datetime | None = None,
    end_date: datetime | None = None,
) -> DashboardOverviewResponse:
    """Return high-level metrics for the active workspace."""
    return dashboard_service.build_overview(
        principal.workspace_id or "demo-workspace",
        start_date=start_date,
        end_date=end_date,
    )
