"""Endpoints module."""

from fastapi import APIRouter, Depends, Response, status, Form, Body
from dependency_injector.wiring import inject, Provide

from containers import Container
from frontend.app import DoorMonitorApp


router = APIRouter()


# @router.get('/get_users/')
# @inject
# async def get_users(
#         user_service: UserService = Depends(Provide[Container.user_service]),
# ):
#     print('/get_users/')
#     return user_service.get_users()

# @app.put("/presence_out_of_bounds/")

@router.get('/status/')
async def get_status():
    print('/status/')
    return {'status': 'OK'}



@router.put('/presence_out_of_bounds/')
@inject
async def presence_out_of_bounds(
    am:str=Body(...),
    frontend: DoorMonitorApp = Depends(Provide[Container.frontend]),
):
    return frontend.presence_out_of_bounds(am)


@router.put('/presence_detected/')
@inject
async def presence_detected(
    am:str=Body(...),
    frontend: DoorMonitorApp = Depends(Provide[Container.frontend]),
):
    return frontend.presence_detected(am)


# @app.put("/presence_detected/")
# async def presence_detected(am:AccessModel):
#     frontend.presence_detected(am)