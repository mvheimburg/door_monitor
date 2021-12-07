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