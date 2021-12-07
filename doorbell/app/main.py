
#!/usr/local/bin/python
# -*- coding: utf-8 -*-
__author__ = 'mvheimburg'

import asyncio
import sys
from os import environ, path

import yaml
from fastapi import Depends, FastAPI, Body

import uvicorn

    
from models import MQTTConfig, APIConfig, Door, DoorsConfig, MqttStringConfig
from frontend.app import DoorMonitorApp
from definitions import ROOT_DIR





def create_app() -> FastAPI:
    cfg = None
    cfg_path = path.join(ROOT_DIR, "config.yaml")
    with open(cfg_path, 'r') as stream:
        cfg = yaml.load(stream, Loader=yaml.FullLoader)
    print(cfg)

    bell_config = MqttStringConfig(**cfg['bell'])

    door_list = []
    for door, d_cfg in  cfg['doors'].items():
        print(f"new_door: {door}")
        new_door = Door(door_id=door, name=d_cfg['name'], command_topic=d_cfg['command_topic'], state_topic=d_cfg['state_topic'])
        # new_door.set_relay()
        door_list.append(new_door)
        
    doors_config = DoorsConfig(doors=door_list)

    print(cfg['garage'])

    garage_config=MqttStringConfig(**cfg['garage'])

    mode_config = MqttStringConfig(**cfg['mode'])


    frontend = DoorMonitorApp(doors_config, bell_config, garage_config, mode_config)
    frontend.run()

    app = FastAPI()


    @app.put("/user_out_of_bounds/")
    async def read_item(uuid:str=Body(...)):
        return frontend.user_out_of_bounds(uuid)



    return app


app = create_app()