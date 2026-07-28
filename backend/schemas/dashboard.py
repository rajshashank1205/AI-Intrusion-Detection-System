from datetime import datetime

from pydantic import BaseModel


class Alert(BaseModel):
    id: int
    timestamp: datetime
    source_ip: str
    alert_type: str
    severity: str
    description: str


class DashboardResponse(BaseModel):
    active_threats: int
    packets_per_second: int
    connected_hosts: int
    ai_confidence: float
    recent_alerts: list[Alert]