from __future__ import annotations
from pathlib import Path
import yaml

from pydantic import BaseModel
from pydantic_settings import BaseSettings

from doorbell.models.models import MqttTopics



from pydantic import (
    Field,
)

class Setup(BaseSettings):
    qos: int = Field(alias='MQTT_QOS', default=0)
    ssl: bool = Field(alias='MQTT_SSL', default=False)

class MqttSettings(BaseSettings):
    host: str = Field(alias='MQTT_HOST', default='localhost')
    port: int = Field(alias='MQTT_PORT', default=1883)
    username: str | None = Field(alias='MQTT_USERNAME', default=None)
    password: str | None = Field(alias='MQTT_PASSWORD', default=None)
    client_id: str = Field(alias='MQTT_CLIENT_ID', default="CLIENT")
    setup: Setup = Setup()

    @property
    def url(self):
        return f"{self.host}:{self.port}"

class MqttCfg(BaseModel):
    bell: MqttTopics
    garage: MqttTopics
    mode: MqttTopics
    state: MqttTopics

    @classmethod
    def load(cls) -> MqttCfg:
        cfg = Path.cwd() / "doorbell" / "config" / "mqtt.yaml"
        with cfg.open('r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        c = cls(**data)
        return c