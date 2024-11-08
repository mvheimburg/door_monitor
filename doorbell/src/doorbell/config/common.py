from __future__ import annotations
from enum import StrEnum, auto

from pydantic_settings import BaseSettings
from pydantic import (
    Field,
)


class BUILD_TYPE(StrEnum):
    LOCALHOST = auto()
    RELEASE = auto()


class CommonSettings(BaseSettings):
    build_type: BUILD_TYPE = Field(alias='BUILD_TYPE',
                                   default=BUILD_TYPE.LOCALHOST)
    port: int = Field(alias='DOORBELL_PORT',
                                   default=5556)


COMMON = CommonSettings()