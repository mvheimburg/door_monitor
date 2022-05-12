from pydantic import BaseModel
from typing import Callable, Optional, List
from kivy.clock import Clock
from const import LoginState


class MqttTopics(BaseModel):
    command: Optional[str]
    state: Optional[str]



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
    name:Optional[str]
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



class DoorsConfig(BaseModel):
    doors: List[Door]

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



# class GarageConfig(BaseModel):
#     command_topic: str
#     state_topic: str
#     state: str = "Unkknown"

class MqttStringConfig(BaseModel):
    command_topic: Optional[str]
    state_topic: Optional[str]
    state: Optional[str]


# class Timer(BaseModel):
#     max_val:int
#     count:int
#     timer:Callable=None

#     def __init__(self, max_val):
#         self.count = max_val
        

#     def start_countdown(self):
#         self.timer = Clock.schedule_interval(self.tic, 1)

#     def tic(self, dt):
#         self.count -= 1




# class AccessState(BaseModel):
#     login_state: LoginState
#     user: Optional[AccessModel]

