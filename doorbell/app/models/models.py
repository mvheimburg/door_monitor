from pydantic import BaseModel
from typing import Optional, List


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



class BellConfig(BaseModel):
    command_topic: str



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



class GarageConfig(BaseModel):
    command_topic: str
    state_topic: str
    state: str = "Unkknown"