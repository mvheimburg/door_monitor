from typing import Callable
import json
from kivy.network.urlrequest import UrlRequest

from const import (
    LOCKMASTER_URL
)

def try_login(on_success:Callable, pin:int):
    req = f"{LOCKMASTER_URL}/get_access_level_by_pin/"
    params = json.dumps(pin)
    print(f"making request: {req}")
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    return UrlRequest(req, method='PUT', on_success=on_success, req_body=params, req_headers=headers)


def detected_beacon(on_success:Callable, uuid:str, rssi:int):
    req = f"{LOCKMASTER_URL}/detected_beacon/"
    params = json.dumps({'uuid':uuid,'rssi':rssi})
    print(f"making request: {req}")
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    return UrlRequest(req, method='PUT', on_success=on_success, req_body=params, req_headers=headers)


def unlock_door(on_success:Callable, door_name:str):
    req = f"{LOCKMASTER_URL}/unlock_door/"
    params = json.dumps(door_name)
    print(f"making request: {req}")
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    return UrlRequest(req, method='PUT', on_success=on_success, req_body=params, req_headers=headers)


def lock_door(on_success:Callable, door_name:str):
    req = f"{LOCKMASTER_URL}/lock_door/"
    params = json.dumps(door_name)
    print(f"making request: {req}")
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    return UrlRequest(req, method='PUT', on_success=on_success, req_body=params, req_headers=headers)


def toggle_door(on_success:Callable, door_name:str):
    req = f"{LOCKMASTER_URL}/toggle_door/"
    params = json.dumps(door_name)
    print(f"making request: {req}")
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    return UrlRequest(req, method='PUT', on_success=on_success, req_body=params, req_headers=headers)


def door_state(on_success:Callable, door_name:str):
    req = f"{LOCKMASTER_URL}/door_state/{door_name}/"
    # params = json.dumps({'door_name':door_name})
    print(f"making request: {req}")
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    return UrlRequest(req, method='GET', on_success=on_success, req_headers=headers)