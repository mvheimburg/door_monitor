from __future__ import annotations
from pathlib import Path
import yaml

from pydantic import BaseModel

from doorbell.models.models import MqttTopics

class Setup(BaseModel):
    qos: int
    ssl: bool


class MqttCfg(BaseModel):
    setup: Setup
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