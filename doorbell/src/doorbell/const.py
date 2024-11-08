from pathlib import Path
from enum import IntEnum


ASSETS = Path().absolute() / "assets"
BELL_WAV = ASSETS / "audio" / "bell-ringing-05.wav"


class Size(IntEnum):
    height = 480
    width = 800