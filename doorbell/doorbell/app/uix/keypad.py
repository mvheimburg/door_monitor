
import flet as ft

class KeyPad(ft.Container):

    def __init__(self):
        ft.GridView(
            expand=1,
            runs_count=5,
            max_extent=150,
            child_aspect_ratio=1.0,
            spacing=5,
            run_spacing=5,
        )