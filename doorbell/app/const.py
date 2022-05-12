from enum import Enum, IntEnum
from os import  environ

class MODE_COMMAND_PAYLOAD():
    NORMAL="normal"
    HALLOWEEN="halloween"
    CHRISTMAS="christmas"

class BELL_COMMAND_PAYLOAD():
    DO="do"

class DOORLOCK_COMMAND_PAYLOAD():
    LOCK="LOCK"
    UNLOCK="UNLOCK"

class DOORLOCK_STATE():
    LOCKED="LOCKED"
    UNLOCKED="UNLOCKED"


class GARAGE_COMMAND_PAYLOAD():
    OPEN="OPEN"
    CLOSE="CLOSE"
    STOP="STOP"

class GARAGE_STATUS_PAYLOAD():
    OPEN="open"
    OPENING="opening"
    CLOSED="closed"
    CLOSING="closing"


SCREEN_TIMER = 20
LOGOUT_TIMER = 3*60
LOGIN_TIMEOUT = 2*60
# CONTROL_TIMEOUT = 1*60

PIN_SIZE = 4


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
LEFT_BOX_WIDTH = SCREEN_HEIGHT
RIGHT_BOX_WIDTH = SCREEN_WIDTH - LEFT_BOX_WIDTH

RSSI_THRESHOLD = -75


MQTT_BROKER     =environ.get('MQTT_BROKER')
MQTT_PORT       =int(environ.get('MQTT_PORT'))
MQTT_USERNAME   =environ.get('MQTT_USERNAME')
MQTT_PASSWORD   =environ.get('MQTT_PASSWORD')
MQTT_CLIENT_ID  =environ.get('MQTT_CLIENT_ID')
LOCKMASTER_URL  =environ.get('LOCKMASTER_URL')

NoneType = type(None)

class LoginState(IntEnum):
    OUT = 0
    PIN_IN=1
    PRESENCE_IN=2