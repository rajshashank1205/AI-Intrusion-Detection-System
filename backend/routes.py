from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db

from backend.schemas.dashboard import DashboardResponse
from backend.schemas.threat_distribution import ThreatDistributionItem
from backend.schemas.host import ActiveHost

from backend.services.dashboard_service import get_dashboard_data
from backend.services.threat_services import get_threat_distribution
from backend.services.host_service import get_top_hosts
from backend.services.threat_analysis_service import get_threat_analysis

from backend.services.incident_service import (
    get_incidents,
    update_incident_status,
)

from backend.services.settings_service import ids_settings

# WebSocket manager
from backend.websocket_manager import manager


router = APIRouter()


# -----------------------------------
# Dashboard
# -----------------------------------

@router.get(
    "/dashboard",
    response_model=DashboardResponse
)
def dashboard(
    db: Session = Depends(get_db)
):
    return get_dashboard_data(db)


# -----------------------------------
# Threat Distribution
# -----------------------------------

@router.get(
    "/threat-distribution",
    response_model=list[ThreatDistributionItem],
)
def threat_distribution(
    db: Session = Depends(get_db)
):
    return get_threat_distribution(db)


# -----------------------------------
# Top Active Hosts
# -----------------------------------

@router.get(
    "/top-hosts",
    response_model=list[ActiveHost],
)
def top_hosts(
    db: Session = Depends(get_db)
):
    return get_top_hosts(db)


# -----------------------------------
# Threat Analysis
# -----------------------------------

@router.get("/threat-analysis")
def threat_analysis(
    db: Session = Depends(get_db)
):
    return get_threat_analysis(db)


# -----------------------------------
# Incidents
# -----------------------------------

@router.get("/incidents")
def incidents(
    db: Session = Depends(get_db)
):
    return get_incidents(db)


# -----------------------------------
# Update Incident Status
# -----------------------------------

@router.patch(
    "/incidents/{incident_id}/status"
)
def change_incident_status(
    incident_id: int,
    data: dict,
    db: Session = Depends(get_db)
):

    status = data.get("status")

    result = update_incident_status(
        db,
        incident_id,
        status
    )

    if result is None:

        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid incident ID "
                "or status."
            )
        )

    return result


# -----------------------------------
# IDS Settings
# -----------------------------------

@router.get("/settings")
def get_settings():

    return ids_settings.get_settings()


@router.put("/settings")
def update_settings(
    settings: dict
):

    return ids_settings.update_settings(
        settings
    )


# -----------------------------------
# Internal Alert Broadcast
# -----------------------------------

@router.post("/internal/broadcast-alert")
async def broadcast_alert(
    alert: dict
):

    await manager.broadcast(alert)

    return {
        "status": "broadcasted"
    }