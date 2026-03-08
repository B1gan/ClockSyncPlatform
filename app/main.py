from fastapi import FastAPI

from app.api.device_api import router as device_router
from app.api.status_api import router as status_router
from app.core.config import settings
from app.core.database import init_db
from app.mqtt.mqtt_client import mqtt_manager


app = FastAPI(title=settings.app_name)

app.include_router(device_router)
app.include_router(status_router)


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    mqtt_manager.start()


@app.on_event("shutdown")
def on_shutdown() -> None:
    mqtt_manager.stop()


@app.get("/")
def health_check():
    return {"message": "Clock Sync Platform is running"}
