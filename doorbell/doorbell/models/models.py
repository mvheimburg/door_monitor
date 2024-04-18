from pydantic import BaseModel
from typing import Optional
from doorbell_old.const import LoginState


class MqttTopics(BaseModel):
    command: str | None = None
    state: str | None = None
    current: str | None = None



class MQTTConfig(BaseModel):
    client_id: str
    port: int
    broker: str
    username: str
    password: str


class APIConfig(BaseModel):
    url: str




# class BellConfig(BaseModel):
#     command_topic: str
class AccessModel(BaseModel):
    name: str | None = None
    access_level: int = 0
    login_state: LoginState = LoginState.OUT


class Door(BaseModel):
    id: str
    name: str
    topic: MqttTopics = MqttTopics()
    state: str = "Unknown"

    def get_state(self):
        return self.state

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.topic.command=f"door/{self.id}/cmd"
        self.topic.state=f"door/{self.id}/state"

    def unlock(self):
        pass

    def lock(self):
        pass

