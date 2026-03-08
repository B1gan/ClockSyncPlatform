from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    device_sn = Column(String(64), unique=True, nullable=False, index=True)
    device_model = Column(String(64), nullable=False)
    ip = Column(String(45), nullable=False)
    firmware_version = Column(String(64), nullable=False)

    statuses = relationship("DeviceStatus", back_populates="device", cascade="all, delete-orphan")
