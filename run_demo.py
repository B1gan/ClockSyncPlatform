"""
演示模式启动脚本：使用 SQLite，无需 MySQL/Redis/MQTT。
"""
import os
os.environ.setdefault("USE_SQLITE", "true")

from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 使用 SQLite
DB_PATH = os.path.join(os.path.dirname(__file__), "clock_sync_demo.db")
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 创建表
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
Base = declarative_base()


class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    device_sn = Column(String(64), unique=True, nullable=False)
    device_model = Column(String(64), nullable=False)
    ip = Column(String(45), nullable=False)
    firmware_version = Column(String(64), nullable=False)


class DeviceStatus(Base):
    __tablename__ = "device_status"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    online_status = Column(String(16), nullable=False)
    sync_status = Column(String(16), nullable=False)
    offset = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)


Base.metadata.create_all(bind=engine)


# Schemas
class DeviceRegisterRequest(BaseModel):
    device_sn: str
    device_model: str
    ip: str
    firmware_version: str


class OffsetPoint(BaseModel):
    timestamp: str
    offset: float


class StatusOverview(BaseModel):
    total_devices: int
    online_devices: int
    sync_ok: int
    sync_warning: int
    sync_error: int
    offsets: list[OffsetPoint]


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    pass


app = FastAPI(title="Clock Sync Platform (Demo)", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health():
    return {"message": "Clock Sync Platform is running"}


@app.get("/devices")
def list_devices(db: Session = Depends(get_db)):
    devices = db.query(Device).order_by(Device.id).all()
    return [
        {"device_sn": d.device_sn, "device_model": d.device_model, "ip": d.ip, "firmware_version": d.firmware_version}
        for d in devices
    ]


@app.post("/devices/register")
def register_device(payload: DeviceRegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(Device).filter(Device.device_sn == payload.device_sn).first()
    if existing:
        from fastapi import HTTPException
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
    return {"message": "设备注册成功", "id": device.id}


@app.get("/status", response_model=StatusOverview)
def get_status(db: Session = Depends(get_db)):
    total = db.query(Device).count()
    statuses = db.query(DeviceStatus).order_by(DeviceStatus.timestamp.desc()).limit(100).all()
    online = sum(1 for s in statuses if s.online_status == "ONLINE")
    sync_ok = sum(1 for s in statuses if s.sync_status == "SYNCED")
    sync_warning = sum(1 for s in statuses if s.sync_status == "SYNCING")
    sync_error = sum(1 for s in statuses if s.sync_status == "ERROR")
    if not statuses:
        online = total
        sync_ok = total
        sync_warning = 0
        sync_error = 0

    now = datetime.utcnow()
    offsets = [
        OffsetPoint(
            timestamp=(now - timedelta(minutes=19 - i)).strftime("%Y-%m-%dT%H:%M:%S"),
            offset=round((__import__("random").random() * 2 - 1) * 5, 1),
        )
        for i in range(20)
    ]
    if statuses:
        offsets = [
            OffsetPoint(timestamp=s.timestamp.strftime("%Y-%m-%dT%H:%M:%S"), offset=round(s.offset, 1))
            for s in reversed(statuses[-20:])
        ]

    return StatusOverview(
        total_devices=total,
        online_devices=online if statuses else total,
        sync_ok=sync_ok if statuses else total,
        sync_warning=sync_warning,
        sync_error=sync_error,
        offsets=offsets,
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
