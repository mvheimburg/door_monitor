from __future__ import annotations
import yaml
from typing import Callable
from pathlib import Path
from pydantic import BaseModel
from doorbell import config
from paho.mqtt.client import MQTTMessage

class MqttTopic(BaseModel):
    command: str
    state: str


class MqttTopics(BaseModel):
    bell: MqttTopic
    garage: MqttTopic
    mode: MqttTopic
    state: MqttTopic

    @classmethod
    def load(cls) -> MqttTopics:
        p = Path(config.__file__).parent
        cfg = p / "topics.yaml"
        with cfg.open('r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        c = cls(**data)
        return c


class APIConfig(BaseModel):
    url: str


# class BellConfig(BaseModel):
#     command_topic: str
class AccessModel(BaseModel):
    name: str | None = None
    access_level: int = 0
    # login_state: LoginState = LoginState.OUT



class Subscription(BaseModel):
    """Represents a MQTT subscription.

    Attributes
    ----------
        topic : str
            The topic name.
        qos : int
            The quality of service(QoS) level: 0, 1 and 2. Refer to the MQTT spec for details.
    """

    topic: str
    qos: int
    # callback: Callable[[MQTTMessage], None]