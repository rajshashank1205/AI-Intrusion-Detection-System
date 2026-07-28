from pydantic import BaseModel


class ThreatDistributionItem(BaseModel):
    severity: str
    total: int