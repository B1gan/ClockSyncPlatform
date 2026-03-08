from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class OnlineStatusEnum(str, Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"


class SyncStatusEnum(str, Enum):
    SYNCING = "SYNCING"
    SYNCED = "SYNCED"
    ERROR = "ERROR"


class StatusReportRequest(BaseModel):
    device_id: int
    online_status: OnlineStatusEnum
    sync_status: SyncStatusEnum
    offset: float


class StatusResponse(BaseModel):
    id: int
    device_id: int
    online_status: OnlineStatusEnum
    sync_status: SyncStatusEnum
    offset: float
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
