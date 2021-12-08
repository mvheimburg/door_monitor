from pydantic import BaseModel
from typing import Callable, Optional, List
from kivy.clock import Clock

from const import(
     DOORLOCK_COMMAND_PAYLOAD
    ,DOORLOCK_STATUS_PAYLOAD
)


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
    access_level: int


class Door(BaseModel):
    door_id: str
    name: str
    command_topic: str
    state_topic: str
    state: str = "Unkknown"

    def get_state(self):
        return self.state



class DoorsConfig(BaseModel):
    doors: List[Door]

    def get_by_id(self, id: str):
        for door in self.doors:
            if door.door_id == id:
                return door

        return None

    def get_by_name(self, name: str):
        for door in self.doors:
            if door.name == name:
                return door
                
        return None


    def get_by_state_topic(self, topic: str):
        for door in self.doors:
            if door.state_topic == topic:
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
