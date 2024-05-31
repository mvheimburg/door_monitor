from typing import Callable, NoReturn
from enum import Enum
from pydantic import BaseModel
from functools import partial
from doorbell.app.const import Size
import flet as ft


# class ACTIONS(Enum):
#     DELETE = ft.icons.BACKSPACE
#     SUBMIT = "Submit"
#     CANCEL = "Cancel"
#     BLANK = ""


KEYS = [
    1,              2,              3,
    4,              5,              6,
    7,              8,              9,
    "-",  0,              "-"
]


class Pin(list[int]):
    # text: str = "_ _ _ _"

    def append(self, object: int) -> None:
        if not len(self) >= 4:
            return super().append(object)
        
    @property
    def text(self):
        textlist = ["*" for v in self]
        textlist += ["_"] * (4 - len(textlist))
        return " ".join(textlist)




class KeyPad(ft.Container):

    def __init__(self):
        super().__init__(width=Size.width/2, height=Size.height)
        # self.validate = validate
        # self.close = close
        # self.width = Size.width
        # self.height = Size.height
        
        self.pin = Pin()
        self.keypad = ft.Row([
                    ft.Column(
                        controls=[self.add_butt(key) for key in [1, 4, 7, ""]]
                    ),
                    ft.Column(
                        controls=[self.add_butt(key) for key in [2, 5, 8, 0]]
                    ),
                    ft.Column(
                        controls=[self.add_butt(key) for key in [3, 6, 9, ""]]
                    ),
                ])

        # self.content = ft.Row([
        #     ft.Column([
        #         self.keypad
        #          ]),
        #     ft.Column([
        #         ft.Row([
        #             ft.Text(self.pin.text)
        #         ])
        #     ])
        # ])
        self.content = self._content(self.pin.text)

    def _content(self, text: str):
        return ft.Row([
            ft.Column([
                self.keypad
                 ]),
            ft.Column([
                ft.Row([
                    ft.Text(text)
                ])
            ])
        ])

        # self.content = ft.GridView(
        #     # expand=1,
        #     horizontal=False,
        #     runs_count=4,
        #     max_extent=80,
        #     child_aspect_ratio=2.0,
        #     spacing=5,
        #     run_spacing=5,
        # )
        # for key in KEYS


    def add_butt(self, key: str | int) -> ft.TextButton | ft.Container:
        if isinstance(key, int):
            return ft.TextButton(
                    text=str(key),
                    on_click=partial(self.num_pressed, key)
                )
        else:
            return ft.Container()

    def num_pressed(self, num: int, *args):
        print(num)
        print(args)
        self.pin.append(num)
        self.content = self._content(self.pin.text)
        self.update()


        # self.content = ft.Column(
        #     controls=[ft.Row(
        #          controls=[ft.TextButton(
        #                 text=str(key),
        #                 on_click=partial(self.num_pressed, key)
        #             ) for key in [1, 2, 3]]
        #     ),
        #     ft.Row(
        #          controls=[ft.TextButton(
        #                 text=str(key),
        #                 on_click=partial(self.num_pressed, key)
        #             ) for key in [4, 5, 6]]
        #     ),
        #     ft.Row(
        #          controls=[ft.TextButton(
        #                 text=str(key),
        #                 on_click=partial(self.num_pressed, key)
        #             ) for key in [7, 8, 9]]
        #     ),
        #     ft.Row(
        #          controls=[ft.Container(), ft.TextButton(
        #                 text=str(0),
        #                 on_click=partial(self.num_pressed, 0)
        #             ), ft.Container()]
        #     )
        # ])