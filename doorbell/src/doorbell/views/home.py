import flet as ft

from typing import Callable
from time import sleep
import threading
from doorbell.uix.bellcontainer import BellContainer
from doorbell.views.myview import MyView
from doorbell.const import Size
from doorbell.utils import get_images


class Home(MyView):
    def __init__(self, ring_bell: Callable):
        super().__init__()
        # self.route = Views.HOME
        self.image_list = get_images("familie")
        self.image_idx = 0
        self.current_image = self.next_image()
        self.running: bool = False
        # self.image = self.next_image()
        # self.ring_bell = ring_bell

        # self.image_container = ft.GestureDetector(
        #     content=self.current_image,
        #     # alignment=ft.alignment.center,
        #     width=Size.height,
        #     on_double_tap=self.dd,
        # )

        but = ft.IconButton(
            icon=ft.icons.DOORBELL_ROUNDED, icon_size=80, on_click=ring_bell
        )
        self.button_container = BellContainer(
            content=but, alignment=ft.alignment.center, expand=True
        )

        self.controls = self._controls()
        # self.controls = [self.image_container, self.button_container]

    def loop_images(self):
        t = threading.Thread(target=self.iterate_images, args=())
        t.start()

    def iterate_images(self):
        while True:
            print("swapping image")
            self.current_image = self.next_image()
            self.controls = self._controls()
            self.update()
            sleep(60)

    # @property
    # def button_container(self) -> BellContainer:
    #     but = ft.IconButton(icon=ft.icons.DOORBELL_ROUNDED, icon_size=80, on_click=self.ring_bell)
    #     return BellContainer(
    #         content=but,
    #         alignment=ft.alignment.center,
    #         expand=True)

    @property
    def image_container(self) -> ft.GestureDetector:
        return ft.GestureDetector(
            content=self.current_image,
            # alignment=ft.alignment.center,
            width=Size.height,
            on_double_tap=self.dd)

    def dd(self, *args):
        print("Double tap")

    def _controls(self):
        return [self.image_container, self.button_container]
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
        self.image_idx += 1
        if self.image_idx > len(self.image_list) - 1:
            self.image_idx = 0
        src = self.image_list[self.image_idx]
        print(f"next image is: {src}")
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
