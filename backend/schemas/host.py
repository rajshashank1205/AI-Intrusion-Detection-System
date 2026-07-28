from pydantic import BaseModel


class ActiveHost(BaseModel):
    source_ip: str
    total: int