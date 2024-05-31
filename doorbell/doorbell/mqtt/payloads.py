from enum import StrEnum


class PARTYMODE_COMMAND_PAYLOAD():
    NORMAL = "normal"
    HALLOWEEN = "halloween"
    CHRISTMAS = "christmas"


class BELL(StrEnum):
    DO = "do"


class DOORLOCK_COMMAND_PAYLOAD():
    LOCK = "LOCK"
    UNLOCK = "UNLOCK"


class DOORLOCK_STATE():
    LOCKED = "LOCKED"
    UNLOCKED = "UNLOCKED"


class GARAGE_COMMAND():
    OPEN = "OPEN"
    CLOSE = "CLOSE"
    STOP = "STOP"


class GARAGE_STATUS_PAYLOAD():
    OPEN = "open"
    OPENING = "opening"
    CLOSED = "closed"
    CLOSING = "closing"
