import flet as ft
import asyncio
from pathlib import Path
from typing import Callable

from doorbell.uix.bellcontainer import BellContainer
from doorbell.views.myview import MyView
from doorbell.const import Size
from doorbell.utils import get_images
from doorbell.const import BELL_WAV, ASSETS, Size


class Home(MyView):

    def __init__(self, ring_bell: Callable):
        super().__init__()
        # self.route = Views.HOME
        self.image_list = get_images("familie")
        print(f"found images: {self.image_list}")
        self.current_image = 0
        self.running: bool = False
        # self.image = self.next_image()
        self.ring_bell = ring_bell
        self.controls = [self.image_container, self.button_container]
    


    @property
    def button_container(self) -> BellContainer:
        but = ft.IconButton(icon=ft.icons.DOORBELL_ROUNDED, icon_size=80, on_click=self.ring_bell)
        return BellContainer(
            content=but,
            alignment=ft.alignment.center,
            expand=True)

    @property
    def image_container(self) -> ft.GestureDetector:
        image = self.next_image()
        return ft.GestureDetector(
            content=image,
            # alignment=ft.alignment.center,
            width=Size.height,
            on_double_tap=self.ring_bell)

    # def _view(self):
    #     # img_control = self.image
    #     return BellContainer(
    #                 content=ft.Row([
    #                     self.image
    #                     # ft.GestureDetector(
    #                     #     content=self.image,
    #                     #     on_double_tap=self.app.show_keypad,
    #                     #     ),
    #                     # BellContainer(
    #                     #     content=self.button,
    #                     #     alignment=ft.alignment.center,
    #                     #     expand=True)
    #                     ],),
    #                 padding=0,
                    

    def next_image(self) -> ft.Image:
        self.current_image += 1
        if self.current_image > len(self.image_list) - 1:
            self.current_image = 0
        src = self.image_list[self.current_image]
        return ft.Image(
                src=src,
                # width=Size.width/2,
                # height=Size.height,
                fit=ft.ImageFit.FIT_HEIGHT,
            )

    # def start(self):
        # self.app.run_task(self.image_carousel)

#  def open_dlg(e):
#                 page.dialog = dlg
#                 dlg.open = True
#                 page.update()

#             def open_dlg_modal(e):
#                 page.dialog = dlg_modal
#                 dlg_modal.open = True
#                 page.update()


   

    # def did_mount(self):
    #     self.running = True
    #     # update_weather calls sync requests.get() and time.sleep() and therefore has to be run in a separate thread
    #     self.app.run_task(self.image_carousel)

    # def will_unmount(self):
    #     self.running = False

    # async def image_carousel(self):
    #     while self.running:
    #         await asyncio.sleep(60)
    #         self.image = self.next_image()
    #         self.view = self._view()
    #         self.update()
