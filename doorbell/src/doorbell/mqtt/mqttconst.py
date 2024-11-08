#define MQTT_GATE_TOPIC_CMD "garage/gate/cmd"
#define PAYLOAD_CMD_GATE_OPEN "OPEN"
#define PAYLOAD_CMD_GATE_CLOSE "CLOSE"
#define PAYLOAD_CMD_GATE_STOP "STOP"

#define MQTT_GATE_TOPIC_STATE "garage/gate/state"
#define PAYLOAD_GATE_OPENED "open"
#define PAYLOAD_GATE_OPENING "opening"
#define PAYLOAD_GATE_CLOSED "closed"
#define PAYLOAD_GATE_CLOSING "closing"

from enum import StrEnum


class GATE_CMD_PAYLOAD(StrEnum):
    OPEN = "OPEN"
    CLOSE = "CLOSE"
    STOP = "STOP"


class GATE_STATE_PAYLOAD(StrEnum):
    OPENED = "open"
    OPENING = "opening"
    CLOSED = "closed"
    CLOSING = "closing"


class GATE_STATE():
    TOPIC = "garage/gate/state"
    PAYLOAD = GATE_STATE_PAYLOAD


class GATE_CMD():
    TOPIC = "garage/gate/cmd"
    PAYLOAD = GATE_CMD_PAYLOAD


class GATE():
    STATE = GATE_STATE
    CMD = GATE_CMD


class CMD_CMD():
    TOPIC = "bell/ring/toggle"
    PAYLOAD = GATE_CMD_PAYLOAD

class BELL(StrEnum):
    TOPIC = "bell/ring/toggle"
    PAYLOAD = "do"

