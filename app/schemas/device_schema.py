from pydantic import BaseModel, ConfigDict, Field


class DeviceRegisterRequest(BaseModel):
    device_sn: str = Field(..., max_length=64)
    device_model: str = Field(..., max_length=64)
    ip: str = Field(..., max_length=45)
    firmware_version: str = Field(..., max_length=64)


class DeviceResponse(BaseModel):
    id: int
    device_sn: str
    device_model: str
    ip: str
    firmware_version: str

    model_config = ConfigDict(from_attributes=True)
