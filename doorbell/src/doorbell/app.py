import flet as ft
from flet import Theme
from doorbell.views.home import Home
from doorbell.mqtt.client import MqttClient
import logging
from doorbell.const import BELL_WAV, ASSETS, Size

# from doorbell.mqtt.config import MqttSettings
# MqttSettings = MqttSettings()
import uvicorn
from doorbell.config import COMMON

_LOGGER = logging.getLogger(__name__)
_LOGGER.level = 10


class App:
    _page: ft.Page

    def __init__(
        self,
        mqttc: MqttClient | None = None
    ):
        self._mqttc = mqttc or MqttClient(logger=_LOGGER, message_handle=self.message_handle)
        self._bellsound = ft.Audio(
            src=BELL_WAV,
            # autoplay=True,
            volume=0.5,
            balance=0,
            on_loaded=lambda _: print("wav rdy"),
        )

    async def ring_bell(self, *args):
        _LOGGER.debug("Ringing bell")
        self._bellsound.play()
        # async with mqttc:
        await self._mqttc.ring_bell()
        # page.update()

    async def message_handle(self, topic: str, payload: str):
        print(topic)
        print(payload)

    async def run(self, page: ft.Page):
        self._page = page
        self._page.title = "Doorbell"
        self._page.padding = 0
        self._page.window.width = Size.width
        self._page.window.height = Size.height
        self._page.window.resizable = False
        self._page.theme = Theme(font_family="Verdana")
        self._page.theme.page_transitions.windows = "cupertino"
        self._page.fonts = {"Pacifico": "/Pacifico-Regular.ttf"}

        self._page.overlay.append(self._bellsound)
        self._page.add(Home(ring_bell=self.ring_bell))
        await self._mqttc.connect()

    #         self.home = Home(app=self)
    #         self.pin_timer = Timer()
    #         self.views: list[ft.View] = [
    #             self.home,
    #             View(
    #                 route=Views.LOGIN,
    #                 controls=[
    #                     Text("Home")
    #                 ])]
    #         self.keypad = KeyPad()
    #         self.keypad_dlg = ft.AlertDialog(
    #                 modal=True,
    #                 # title=ft.Text("Please confirm"),
    #                 content=self.keypad,
    #                 actions=[
    #                     ft.TextButton("Submit", on_click=self.validate),
    #                     ft.TextButton("Close", on_click=self.hide_keypad),
    #                 ],
    #                 # opacity=0.5,
    #                 actions_alignment=ft.MainAxisAlignment.END,
    #                 # on_dismiss=lambda e: print("Modal dialog dismissed!"),
    #             )

    #         ## MQTT
    #         # self.mqttc = MqttClient()
    #         # self._topics = MqttTopics.load()
    #         # self.mqttc.subscribe_callback(self._topics.garage.state,
    #         #                               self.update_garage)
    #         # self.mqttc.subscribe_callback(self._topics.mode.state,
    #         #                               self.update_mode)
    #         # self.mqttc.subscribe_callback(self._topics.state.state,
    #         #                               self.update_state)
    #         # self.mqttc.subscribe_callback(self._topics.bell.state,
    #         #                               self.update_bell)
    #         # self.mqttc.connect_std_creds()

    async def deploy(self):
        await ft.app_async(target=self.run, assets_dir=ASSETS)

    def serve(self):
        app = ft.app(target=self.run, assets_dir=ASSETS, export_asgi_app=True)
        uvicorn.run(app, host="0.0.0.0", port=COMMON.port, log_level="debug")

        # return ft.app(target=self.run, assets_dir=ASSETS, export_asgi_app=True)

    # def run(self):

    #         self._page.title = "Doorbell"
    #         self._page.padding = 0
    #         self._page.window_width = Size.width
    #         self._page.window_height = Size.height
    #         self._page.window_resizable = False
    #         self._page.theme = Theme(
    #             font_family="Verdana")
    #         self._page.theme.page_transitions.windows = "cupertino"
    #         self._page.fonts = {
    #             "Pacifico": "/Pacifico-Regular.ttf"
    #         }
    #         self._page.bgcolor = colors.BLUE_GREY_200

    #         # context = ft.GestureDetector(
    #         #         mouse_cursor=ft.MouseCursor.CONTEXT_MENU,
    #         #     )

    #         # self.page.add()

    #         self.change_view(Views.HOME)
    # self.main_page.start()

    #     @property
    #     def active_view(self):
    #         return self.get_view(self._active_view)

    #     @property
    #     def assets(self) -> Path:
    #         return self._assets

    @property
    def page(self):
        return self._page


#     # @active_view.setter
#     # def active_view(self, view: str):
#     #     print(f"Should set view {view}")
#     #     self.page.views.clear()
#     #     self._active_view = view
#     #     self.page.views.append(self.active_view)
#     #     self.page.update()

#     def add_overlay(self, overlay: Any):
#         self._page.overlay.append(overlay)
#         self._page.update()

#     def run_task(self, func):
#         self.page.run_task(func)

#     def change_view(self, view: str):
#         # self.active_view = view
#         print(f"Should set view {view}")
#         self.page.views.clear()
#         self._active_view = view
#         self.page.views.append(self.active_view)
#         self.page.update()

#     def get_view(self, view: str) -> View:
#         v = next(filter(lambda v: v.route == view, self.views), None)
#         if v is None:
#             raise ValueError("Unknown view")
#         return v

#     async def ring_bell(self, *args):
#         print("Ringing bell")
#         bellsound = ft.Audio(src=url,
#                             autoplay=True,
#                             volume=0.5,
#                             balance=0,
#                             on_loaded=lambda _: print("DingDong"))
#         # await self.mqttc.ring_bell()

#     async def show_keypad(self, ce: ft.ControlEvent):
#         self.page.dialog = self.keypad_dlg
#         self.keypad_dlg.open = True
#         self.page.update()

#     async def hide_keypad(self, ce: ft.ControlEvent):
#         self.keypad.clear()
#         self.keypad_dlg.open = False
#         self.page.update()

#     async def validate(self, ce: ft.ControlEvent):
#         print(f"Validating pin: {self.keypad.get_pin()}")
#         await self.hide_keypad()
#         self.page.update()

#     def update_garage(self, message: MQTTMessage):
#         print(message.payload)

#     # def garage_open(self):
#     #     self.mqttc.garage_open()

#     # def garage_close(self):
#     #     self.mqttc.garage_command(GARAGE_COMMAND.CLOSE)

#     # def garage_stop(self):
#     #     self.mqttc.garage_command(GARAGE_COMMAND.STOP)

#     def update_mode(self, message: MQTTMessage):
#         print(message.payload)

#     def update_state(self, message: MQTTMessage):
#         print(message.payload)

#     def update_bell(self, message: MQTTMessage):
#         print(message.payload)


async def main(page: ft.Page):
    async with MqttClient(logger=_LOGGER) as mqttc:
        # mqttc =
        await mqttc.connect()
        # mqttc._message_handle = message_handle
        # page.adaptive = True
        #
        # async def listen(client: Client):
        #     async for message in client.messages:
        #         print(message.payload)

        # async with  Client(hostname=MqttSettings.host,
        #                   port=MqttSettings.port,
        #                   username=MqttSettings.username,
        #                   password=MqttSettings.password,
        #                 #   transport="websockets"
        #                   ) as c:
        #     # Make client globally available
        #     client = c
        #     # Listen for MQTT messages in (unawaited) asyncio task
        #     await client.subscribe("humidity/#")
        #     loop = asyncio.get_event_loop()
        #     task = loop.create_task(listen(client))
        #     yield

        # background_tasks = set()

        # await mqttc.subscribe(GATE.STATE.TOPIC)
        # await mqttc.subscribe(BELL.TOPIC)

        # loop = asyncio.get_event_loop()
        # task = loop.create_task(listen(mqttc))
        # background_tasks.add(task)
        # task.add_done_callback(background_tasks.remove)

        # bellsound = ft.Audio(
        #     src=BELL_WAV,
        #     # autoplay=True,
        #     volume=0.5,
        #     balance=0,
        #     on_loaded=lambda _: print("wav rdy"),
        # )
        # page.overlay.append(bellsound)

        # async def ring_bell(*args):
        #     _LOGGER.debug("Ringing bell")
        #     bellsound.play()
        #     # async with mqttc:
        #     await mqttc.ring_bell()
        #     # page.update()

        # page.add(Home(ring_bell=ring_bell))

        # page.title = "Doorbell"
        # page.padding = 0
        # page.window.width = Size.width
        # page.window.height = Size.height
        # page.window.resizable = False
        # page.theme = Theme(font_family="Verdana")
        # page.theme.page_transitions.windows = "cupertino"
        # page.fonts = {"Pacifico": "/Pacifico-Regular.ttf"}
        # page.bgcolor = colors.BLUE_GREY_200

    # mqttc = MqttClient(logger=_LOGGER)
    # await mqttc.connect()

    # interval = 5  # Seconds
    # while True:
    #     try:
    #         async with MqttClient(logger=_LOGGER) as mqttc:
    #             # await client.subscribe("humidity/#")
    #             # async for message in client.messages:
    #             #     print(message.payload)

    #             print(mqttc)
    #             # async for message in client.messages:
    #             #     print(message.payload)
    #             await page_runner(page, mqttc)
    #             yield
    #     except MQTTConnectError:
    #         print(f"Connection lost; Reconnecting in {interval} seconds ...")
    #         await asyncio.sleep(interval)

    # async with Client(hostname=MqttSettings.host,
    #                   port=MqttSettings.port,
    #                   username=MqttSettings.username,
    #                   password=MqttSettings.password,
    #                 #   transport="websockets"
    #                   ) as client:
    #     print(client)
    #     # async for message in client.messages:
    #     #     print(message.payload)
    #     await page_runner(page, client)
