from typing import Any, NoReturn, Coroutine, Callable, Self
# import asyncio
import logging
# from gmqtt import Client

import paho.mqtt.client as mqtt
from paho.mqtt import MQTTException
from types import TracebackType

from doorbell.mqtt.mqttconst import BELL, GATE
from doorbell.mqtt.config import MqttSettings


class MqttClient:
    def __init__(
        self,
        message_handle: Callable | None = None,
        settings: MqttSettings = MqttSettings(),
        logger: logging.Logger | None = None,
    ):
        self._settings = settings
        self._message_handle = message_handle
        self._logger = logger or logging.Logger(__name__)
        # self._background_tasks: set[asyncio.Task[Any]] = set()

        # self._client = Client(client_id=settings.client_id, logger=logger)
        # self._client.set_auth_credentials(
        #     self._settings.username, self._settings.password
        # )
        # self._client.on_message = self._on_message
        # self._client.on_connect = self._on_connect
        self._client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        # self._client.host = self._settings.host
        # self._client.port = self._settings.port
        self._client.username = self._settings.username
        self._client.password = self._settings.password
        self._client.on_message = self.on_message
        self._client.on_connect = self.on_connect
        self._client.on_subscribe = self.on_subscribe
        # Uncomment to enable debug messages
        # self._client.on_log = on_log
        self._client.connect("mqtt.eclipseprojects.io", 1883, 60)
        self._client.subscribe("$SYS/#")



    # def __aenter__(self) -> Self:
    #     # self.connect()
    #     return self

    # def __aexit__(self,
    #     exc_type: type[BaseException] | None,
    #     exc: BaseException | None,
    #     tb: TracebackType | None,
    # ) -> None:
    #     try:
    #         self._client.disconnect()
    #     except Exception as e:
    #          print(str(e))
    #     else:
    #         print(
    #             "Could not gracefully disconnect. Forcing disconnection.")

    def connect(self):
        """Connecting to broker"""
        print(f"Connecting to host={self._settings.host}, port={self._settings.port}")
        self._client.connect(
            host=self._settings.host, port=self._settings.port
        )
        print("Connected to broker")

    # def _on_connect(self, client: Client, flags: int, rc: int, properties: Any) -> None:
    #     self._sub_all()

    # def _on_message(
    #     self, client: Client, topic: str, payload: bytes, qos: int, properties: Any
    # ) -> Any:
        

    def _sub_all(self):
        self._client.subscribe(GATE.STATE.TOPIC, qos=0)
        self._client.subscribe(BELL.TOPIC, qos=0)

    def ring_bell(self):
        print('ringing that bell')
        self._publish(BELL.TOPIC, payload=BELL.PAYLOAD)

    def _garage_command(self, command: str):
        self._publish(GATE.CMD.TOPIC, payload=command)

    def garage_open(self):
        self._garage_command(GATE.CMD.PAYLOAD.OPEN)

    def _publish(self, topic: str, payload: str):
        print('ringing that bell')
        if not self._client.is_connected:
            self._client.reconnect()
        self._client.publish(topic, payload=payload)


    def on_connect(self, mqttc, obj, flags, reason_code, properties):
        print("reason_code: " + str(reason_code))


    def on_message(self, mqttc, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        if self._message_handle is not None:
            self._message_handle(msg.topic, msg.payload)

    def on_subscribe(self, mqttc, obj, mid, reason_code_list, properties):
        print("Subscribed: " + str(mid) + " " + str(reason_code_list))


    def on_log(self, mqttc, obj, level, string):
        print(string)

