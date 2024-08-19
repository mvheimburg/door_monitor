from enum import StrEnum


class PARTYMODE():
    class COMMAND(StrEnum):
        NORMAL = "normal"
        HALLOWEEN = "halloween"
        CHRISTMAS = "christmas"

    class STATE(StrEnum):
        NORMAL = "normal"
        HALLOWEEN = "halloween"
        CHRISTMAS = "christmas"


class BELL():
    class COMMAND(StrEnum):
        DO = "do"


class DOORLOCK():
    class COMMAND(StrEnum):
        LOCK = "LOCK"
        UNLOCK = "UNLOCK"

    class STATE(StrEnum):
        LOCKED = "LOCKED"
        UNLOCKED = "UNLOCKED"


class GARAGE():
    class COMMAND(StrEnum):
        OPEN = "OPEN"
        CLOSE = "CLOSE"
        STOP = "STOP"

    class STATE(StrEnum):
        OPEN = "open"
        OPENING = "opening"
        CLOSED = "closed"
        CLOSING = "closing"
