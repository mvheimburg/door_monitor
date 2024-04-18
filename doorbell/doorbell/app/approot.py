from abc import ABC, abstractmethod
from pathlib import Path
from flet import (
    Page
)


class AppRoot(ABC):

    @property
    @abstractmethod
    def page(self) -> Page:
        pass

    @property
    @abstractmethod
    def assets(self) -> Path:
        pass

    @abstractmethod
    def change_view(self, view: str):
        pass

    @abstractmethod
    async def ring_bell(self):
        pass

    @abstractmethod
    async def show_pin_start(self):
        pass

    @abstractmethod
    async def show_pin_end(self):
        pass

