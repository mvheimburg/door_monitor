from __future__ import annotations
from pathlib import Path
import yaml

from pydantic import BaseModel

from doorbell.models.models import MqttTopics
from doorbell.models.models import Door

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
        p = Path(__file__).parent
        cfg = p / "mqtt.yaml"
        with cfg.open('r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        c = cls(**data)
        return c


class DoorsConfig(BaseModel):
    doors: list[Door]

    def get_name_by_id(self, id: str):
        for door in self.doors:
            if door.id == id:
                return door.name

        return None

    def get_by_name(self, name: str):
        for door in self.doors:
            if door.name == name:
                return door
                
        return None

    def get_by_state_topic(self, topic: str):
        for door in self.doors:
            if door.topic.state == topic:
                return door

        return None

    @classmethod
    def load(cls) -> MqttCfg:
        p = Path(__file__).parent
        cfg = p / "doors.yaml"
        with cfg.open('r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        c = cls(**data)
        return c
