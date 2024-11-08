import flet as ft

from doorbell.const import Size


class MyView(ft.Row):
    def __init__(self):
        super().__init__(width=Size.width, height=Size.height)
