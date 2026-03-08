from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.device_schema import DeviceRegisterRequest, DeviceResponse
from app.services.device_service import list_devices, register_device


router = APIRouter(prefix="/devices", tags=["devices"])


@router.post("/register", response_model=DeviceResponse)
def register_device_api(payload: DeviceRegisterRequest, db: Session = Depends(get_db)):
    return register_device(db, payload)


@router.get("", response_model=list[DeviceResponse])
def list_devices_api(db: Session = Depends(get_db)):
    return list_devices(db)
