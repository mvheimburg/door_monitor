from pydantic import BaseModel
from typing import Optional, List




class DoorState(BaseModel):
    # name: str
    locked: bool = False


class GarageState(BaseModel):
    closed: bool = True
    moving: bool = False



class ControlMemory(BaseModel):
    door_states: List[DoorState]
    garage_state: GarageState