from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class DeviceStatus(Base):
    __tablename__ = "device_status"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False, index=True)
    online_status = Column(String(16), nullable=False)
    sync_status = Column(String(16), nullable=False)
    offset = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    device = relationship("Device", back_populates="statuses")
