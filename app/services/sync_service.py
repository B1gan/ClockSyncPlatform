from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.redis_client import cache_device_status
from app.models.device_status import DeviceStatus
from app.schemas.status_schema import StatusReportRequest
from app.services.device_service import get_device_by_id


def report_status(db: Session, payload: StatusReportRequest) -> DeviceStatus:
    device = get_device_by_id(db, payload.device_id)
    if not device:
        raise HTTPException(status_code=404, detail="device not found")

    status = DeviceStatus(
        device_id=payload.device_id,
        online_status=payload.online_status.value,
        sync_status=payload.sync_status.value,
        offset=payload.offset,
    )
    db.add(status)
    db.commit()
    db.refresh(status)

    cache_device_status(
        device_id=payload.device_id,
        online_status=payload.online_status.value,
        sync_status=payload.sync_status.value,
        offset=payload.offset,
    )
    return status
