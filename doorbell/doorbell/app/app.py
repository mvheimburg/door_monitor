from pathlib import Path
import time
import asyncio
import flet as ft
from flet import (
    Page,
    colors,
    Theme,
    View,
    Text

)
from doorbell.app.approot import AppRoot
from doorbell.app.const import Views, Size
from doorbell.app.views.home import Home

# url = "https://github.com/mdn/webaudio-examples/blob/main/audio-analyser/viper.mp3?raw=true"
url = "/audio/bell-ringing-05.wav"


class Timer():
    def __init__(self):
        self._start: float = 0.0
        self._end: float = 0.0

    @property
    def time(self) -> float:
        return self._end - self._start

    def start(self):
        self._start = time.time()

    def end(self) -> float:
        self._end = time.time()
        return self.time


class App(AppRoot):
    _page: ft.Page
    _assets: Path

    def __init__(self, assets: Path):
        self._assets = assets

        self.home = Home(app=self)
        self.pin_timer = Timer()
        self.views: list[ft.View] = [
            self.home,
            View(
                route=Views.LOGIN,
                controls=[
                    Text("Home")
                ])]

        self.bellsound = None
     

    def initialize(self):
        self.active_view = Views.HOME
        self.home.start()
        self.page.update()

    def deploy(self):
        ft.app(target=self.app, assets_dir=str(self.assets))

    def serve(self):
        return ft.app(target=self.app, assets_dir=str(self.assets), export_asgi_app=True)

    def app(self, page: Page):
        self._page = page
        self._page.title = "Doorbell"
        self._page.padding = 0
        self._page.window_width = Size.width
        self._page.window_height = Size.height
        self._page.window_resizable = False
        self._page.theme = Theme(
            font_family="Verdana")
        self._page.theme.page_transitions.windows = "cupertino"
        self._page.fonts = {
            "Pacifico": "/Pacifico-Regular.ttf"
        }
        self._page.bgcolor = colors.BLUE_GREY_200

        # context = ft.GestureDetector(
        #         mouse_cursor=ft.MouseCursor.CONTEXT_MENU,
        #     )
        
        # self.page.add()

        self.initialize()
        # self.main_page.start()

    @property
    def active_view(self):
        return self.get_view(self._active_view)
    
    @property
    def assets(self):
        return self._assets
    
    @property
    def page(self):
        return self._page
 
 
    @active_view.setter
    def active_view(self, view: str):
        print(f"Should set view {view}")
        self.page.views.clear()
        self._active_view = view
        self.page.views.append(self.active_view)
        self.page.update()

    def add_overlay(self, overlay):
        self._page.overlay.append(overlay)
        self._page.update()

    def run_task(self, func):
        self.page.run_task(func)

    def change_view(self, view: str):
        self.active_view = view

    def get_view(self, view: str) -> View:
        v = next(filter(lambda v: v.route == view, self.views), None)
        if v is None:
            raise ValueError("Unknown view")
        return v

    async def ring_bell(self, *args):
        print("Ringing bell")
        bellsound = ft.Audio(src=url,
                            autoplay=True,
                            volume=0.5,
                            balance=0,
                            on_loaded=lambda _: print("Loaded"),)
        self.add_overlay(bellsound)

    async def show_pin_start(self, *args):
        self.pin_timer.start()
        print("Styarting timer")

    async def show_pin_end(self, *args):
        if self.pin_timer.end() > 2:
            print("Show pin")

        else:
            print("Too short")