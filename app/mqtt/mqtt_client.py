import json
import logging

import paho.mqtt.client as mqtt
from pydantic import ValidationError

from app.core.config import settings
from app.core.database import SessionLocal
from app.schemas.status_schema import StatusReportRequest
from app.services.sync_service import report_status


logger = logging.getLogger(__name__)


class MQTTManager:
    def __init__(self) -> None:
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self._started = False

    def start(self) -> None:
        if self._started:
            return
        self.client.connect(settings.mqtt_host, settings.mqtt_port, keepalive=60)
        self.client.loop_start()
        self._started = True
        logger.info("MQTT client started, broker=%s:%s", settings.mqtt_host, settings.mqtt_port)

    def stop(self) -> None:
        if not self._started:
            return
        self.client.loop_stop()
        self.client.disconnect()
        self._started = False
        logger.info("MQTT client stopped")

    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            client.subscribe(settings.mqtt_topic_status)
            logger.info("MQTT connected and subscribed: %s", settings.mqtt_topic_status)
        else:
            logger.error("MQTT connection failed with code: %s", reason_code)

    def on_message(self, client, userdata, msg):
        db = SessionLocal()
        try:
            payload_raw = msg.payload.decode("utf-8")
            payload_dict = json.loads(payload_raw)
            payload = StatusReportRequest.model_validate(payload_dict)
            report_status(db, payload)
            logger.info("MQTT status processed for device_id=%s", payload.device_id)
        except (json.JSONDecodeError, ValidationError) as exc:
            logger.error("Invalid MQTT payload: %s", exc)
            db.rollback()
        except Exception as exc:
            logger.exception("Failed to process MQTT message: %s", exc)
            db.rollback()
        finally:
            db.close()


mqtt_manager = MQTTManager()
