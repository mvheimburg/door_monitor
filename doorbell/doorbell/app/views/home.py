import flet as ft
import asyncio


from doorbell.app.views.myview import MyView
from doorbell.app.const import Views, Size



class Home(MyView):

    def _get_images(self):
        IMAGES = "familie"
        family = self.app.assets / IMAGES
        image_list = list(family.glob("*.png"))
        ret = [f"{IMAGES}/{img.name}" for img in image_list]
        return ret

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.route = Views.HOME
        self.image_list = self._get_images()
        self.current_image = 0
        self.image = self.next_image()
        self.button = ft.IconButton(icon=ft.icons.DOORBELL_ROUNDED, icon_size=80, on_click=self.app.ring_bell)
        self.controls = self._controls()

    def _controls(self):
        # img_control = self.image
        return [
            ft.Container(
                content=ft.Row([
                    ft.GestureDetector(
                        content=self.image,
                        on_long_press_start=self.app.show_pin_start,
                        on_long_press_end=self.app.show_pin_end,
                        ),
                    ft.Container(
                        content=self.button,
                        alignment=ft.alignment.center,
                        expand=True)
                    ],),
                padding=0,
                width=Size.width,
                height=Size.height)
            ]

    def next_image(self) -> ft.Image:
        self.current_image += 1
        if self.current_image > len(self.image_list) - 1:
            self.current_image = 0
        return ft.Image(
                src=self.image_list[self.current_image],
                # width=Size.width/2,
                # height=Size.height,
                fit=ft.ImageFit.FIT_HEIGHT,
            )

    def start(self):
        self.app.run_task(self.image_carousel)

    async def image_carousel(self):
        while True:
            await asyncio.sleep(60)
            self.image = self.next_image()
            self.controls = self._controls()
            self.update()
