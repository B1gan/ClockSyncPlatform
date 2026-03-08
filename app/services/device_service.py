from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.device import Device
from app.schemas.device_schema import DeviceRegisterRequest


def register_device(db: Session, payload: DeviceRegisterRequest) -> Device:
    existing = db.query(Device).filter(Device.device_sn == payload.device_sn).first()
    if existing:
        raise HTTPException(status_code=400, detail="device_sn already exists")

    device = Device(
        device_sn=payload.device_sn,
        device_model=payload.device_model,
        ip=payload.ip,
        firmware_version=payload.firmware_version,
    )
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


def list_devices(db: Session) -> list[Device]:
    return db.query(Device).order_by(Device.id.asc()).all()


def get_device_by_id(db: Session, device_id: int) -> Device | None:
    return db.query(Device).filter(Device.id == device_id).first()
