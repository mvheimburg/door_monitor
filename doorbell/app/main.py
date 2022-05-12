
#!/usr/local/bin/python
# -*- coding: utf-8 -*-
__author__ = 'mvheimburg'

import sys
from os import environ, path
from threading import Thread
from functools import partial
import yaml
from fastapi import Depends, FastAPI, Body
# from fastapi.middleware.cors import CORSMiddleware
# import uvicorn


# from kivy.app import async_runTouchApp
    
from models import MQTTConfig, APIConfig, Door, DoorsConfig, MqttStringConfig, AccessModel
from frontend.app import DoorMonitorApp
from definitions import ROOT_DIR

# from containers import Container
# import endpoints as ep

# import trio
# from hypercorn.trio import serve
# from hypercorn.config import Config

# # import asyncio
# # from hypercorn.asyncio import serve

# def start_frontend(frontend):
#     # frontend.run()
#     trio.run(partial(frontend.async_run, async_lib='trio'))



# def create_app() -> FastAPI:


#     app = FastAPI()
#     app.container = Container()
#     config_path = path.join(ROOT_DIR, "config.yaml")
#     app.container.config.from_yaml(config_path)
#     app.container.wire(modules=[ep])
#     # with open(cfg_path, 'r') as stream:
#     #     cfg = yaml.load(stream, Loader=yaml.FullLoader)
#     # print(cfg)


#     frontend=app.container.frontend()
#     frontend_t = Thread(target=start_frontend, args=(frontend,), daemon=True)
#     frontend_t.start()
#     # frontend.run()
#     # frontend.async_run(async_lib='trio')
#     # trio.run(partial(frontend.async_run, async_lib='trio'))
#     # asyncio.create_task(frontend.async_run())
#     # loop = asyncio.get_event_loop()
#     # loop.run_until_complete(frontend.async_run())

#     print("Frontend started")

#     # print("Adding middleware....")
#     # # app.add_middleware(
#     #     CORSMiddleware,
#     #     allow_origins=["*"],
#     #     allow_credentials=True,
#     #     allow_methods=["*"],
#     #     allow_headers=["*"],
#     # )

#     # @app.put("/presence_out_of_bounds/")
#     # async def presence_out_of_bounds(am:str=Body(...)):
#     #     return frontend.presence_out_of_bounds(am)


#     # @app.put("/presence_detected/")
#     # async def presence_detected(am:AccessModel):
#     #     frontend.presence_detected(am)

#     app.include_router(ep.router)

#     return app



# config = Config()
# config.bind = ["0.0.0.0:80"]
# app = create_app()
# trio.run(serve, app, config)
# # asyncio.run(serve(app, config))


# if __name__ == '__main__':


# app = FastAPI()

cfg = None
cfg_path = path.join(ROOT_DIR, "config.yaml")
with open(cfg_path, 'r') as stream:
    cfg = yaml.load(stream, Loader=yaml.FullLoader)
print(cfg)
frontend=DoorMonitorApp(cfg)
frontend.run()


# @app.get("/test/")
# async def test():
#     return "test"

# @app.put("/presence_detected/")
# async def presence_detected(am:dict=Body(...)):
#     global frontend
#     # am=AccessModel(**am, login_state = LoginState.PRESENCE_IN)
#     print(am)
#     frontend.presence_detected(am)
#     return True
