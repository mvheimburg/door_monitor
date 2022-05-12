# from __future__ import unicode_literals

# from os import path
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, DictProperty
from kivy.uix.screenmanager import ScreenManager, NoTransition
# from kivymd.uix.screen import MDScreen
from kivy.utils import get_color_from_hex
from rpi_backlight import Backlight

from kivymd.app import MDApp
from kivymd.theming import ThemeManager
# from kivy.network.urlrequest import UrlRequest
from kivymd.toast import toast
# import urllib
from jsonsempai import magic
from typing import Dict

# from kivy.lang import Builder
# from kivy.clock import Clock

# from time import sleep

import paho.mqtt.client as mqtt
# import urllib.parse
# import websockets

# from kivy.properties import BoundedNumericProperty

from models import MQTTConfig, DoorsConfig, AccessModel
# from models.memory import DoorState, GarageState
from kelvin import kelvin_rgb_to_kivy

from const import(
     SCREEN_TIMER
    ,LOGOUT_TIMER
    ,BELL_COMMAND_PAYLOAD
    ,GARAGE_COMMAND_PAYLOAD
    ,MODE_COMMAND_PAYLOAD
    ,MQTT_BROKER
    ,MQTT_CLIENT_ID
    ,MQTT_PASSWORD
    ,MQTT_PORT
    ,MQTT_USERNAME
    
)

# from kivy.support import install_twisted_reactor

# install_twisted_reactor()

# from twisted.web import server, resource
# from twisted.internet import reactor, endpoints
# from twisted.internet import defer
# from twisted.web import xmlrpc
# # xmlrpc.XMLRPC(allowNone=True)

from frontend.app import config
from frontend.app.api import try_login, detected_beacon, lock_door, unlock_door

# LOAD_FILE = 'doormonitor.kv'
# FILE_PATH = path.abspath(path.join(path.dirname(__file__), LOAD_FILE))
# Builder.load_file(FILE_PATH)


from models import MQTTConfig, APIConfig, Door, DoorsConfig, MqttStringConfig, AccessModel
from const import LoginState
from frontend.utils import Timer
# from const import NoneType




from kivy.support import install_twisted_reactor

install_twisted_reactor()

from twisted.web import server, resource
from twisted.internet import reactor, endpoints
from twisted.internet import defer
from twisted.web import xmlrpc
class WebServerResource(xmlrpc.XMLRPC):

    def __init__(self, app):
        self.allowNone = True
        super().__init__()
        self.app = app

    # def xmlrpc_echo(self, *args):
    #     print(args)
    #     return args

    # def xmlrpc_echo2(self, x):
    #     print(x)
    #     return x

    # def xmlrpc_presence_out_of_bounds(self, am:dict):
    #     am=AccessModel(**am)
    #     self.app.presence_out_of_bounds(am)
    #     return True

    def xmlrpc_presence_detected(self, am:Dict):
        # am=AccessModel(**am, login_state = LoginState.PRESENCE_IN)
        self.app.presence_detected(am)
        return True

# from fastapi import Depends, FastAPI, Body
# import uvicorn

# def create_app(frontend) -> FastAPI:
#     print("Starting FastAPI!")

#     app = FastAPI()


#     @app.get("/test/")
#     async def test():
#         return "test"

#     @app.put("/presence_detected/")
#     async def presence_detected(am:Dict=Body(...)):
#         # global frontend
#         # am=AccessModel(**am, login_state = LoginState.PRESENCE_IN)
#         print(am)
#         frontend.presence_detected(am)
#         return True

#     uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")


class DoorMonitorApp(MDApp):
    """
    Frontend for CatchScanner configuration

    """
    # connection = ObjectProperty()
    current_user = ObjectProperty(AccessModel())
    gui = ObjectProperty()
    _mqttc = mqtt.Client

    def __init__(self, cfg: dict) -> None:
        super().__init__()

        door_list = []
        for door, d_cfg in  cfg['doors'].items():
            print(f"new_door: {door}")
            new_door = Door(id=door, name=d_cfg['name'])
            # new_door.set_relay()
            door_list.append(new_door)
            
        self.doors_config = DoorsConfig(doors=door_list)
        self.bell_config = MqttStringConfig(**cfg['bell'])
        self.garage_config = MqttStringConfig(**cfg['garage'])
        self.mode_config = MqttStringConfig(**cfg['mode'])
        self.state_config = MqttStringConfig(**cfg['state'])

        print(cfg['garage'])

        self.kelvin = kelvin_rgb_to_kivy()
        self.azure = get_color_from_hex('#f0ffff')

        self.theme_cls = ThemeManager()
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.accent_palette = "Yellow"
        self.theme_cls.accent_palette_hue = "500"
        self.theme_cls.theme_style = "Light"

        self.backlight = Backlight()

        
        ## GUI ##
        self.gui = ScreenManager(transition=NoTransition())
        try:
            self.screens= config.screens
        except AttributeError:
            self.screens = None
        else:
            for screen in self.screens:
                print(f'New screen: {screen}')
                try:
                    import_statemet = self.screens[screen]["import"]+' as NewScreen'
                    print(import_statemet)
                    exec(import_statemet)
                except Exception as e:
                    print(e)
                else:
                    screen_kwargs = {}
                    screen_kwargs.update({'name':screen})
                    print(f'SCREEN NAME IS: {screen}')
                    print(f'with kwargs: {screen_kwargs}')
                    self.screens[screen]["object"]=eval('NewScreen')(**screen_kwargs)
                    self.gui.add_widget(self.screens[screen]["object"])
            

        self.change_screen(self.gui.screen_names[0])

        self.screen_timer = Timer(callback=self.screen_time_out ,time=SCREEN_TIMER)
        self.log_out_timer = Timer(callback= self.log_out ,time=LOGOUT_TIMER)


    # def presence_out_of_bounds(self, am:AccessModel):
    #     print(f"USER OUT OF BOUNDS {am}")
    

    def presence_detected(self, am:dict):
        am=AccessModel(**am, login_state = LoginState.PRESENCE_IN)
        print(f"presence_detected: {am}")
        # if self.current_user != am.name:
        print(f"self.current_user: {self.current_user }")
        if self.current_user.login_state == LoginState.OUT:
            # if self.current_user != am:
            print("Setting new user")
            self.current_user = am
        elif self.current_user.name == am.name:
            self.extend_screen_timer()

    
    def on_current_user(self, instance, value):
        print(value)
        try:
            if value.access_level>0:
                if value.name is not None:
                    user = str(value.name)
                    print(f"Current user is {user}")
                    toast(f"Velkommen {user}")
                else:
                    print(f"Login user is {None}")

                self.change_screen('Control')
                self.screens['DoorBell']["object"].login_feedback(True)
        except Exception as e:
            print(e)


    def get_door_name(self, door_nr, *args):
        print(door_nr)
        door = self.doors_config.get_name_by_nr(door_nr)
        if door is not None:
            return door.name
        else:
            return ""

    def get_door_id(self, door_nr, *args):
        print(door_nr)
        door = self.doors_config.get_id_by_nr(door_nr)
        if door is not None:
            return door.name
        else:
            return ""
    

    @property
    def access_level(self):
        return self.current_user.access_level


    # def on_door_states(self, *args):
    #     print("on_door_states")


    def on_start(self):
        self.make_client()
        

    def next_screen(self):
        self.gui.next_screen()

    def prev_screen(self):
        self.gui.prev_screen()

    def on_enter_view(self, *args):
        pass


    def build(self):
        """
        Kivy build.

        Function to return Kivy Layout from App class.


        Returns:
            Widget containing GUI

        """
        reactor.listenTCP(80, server.Site(WebServerResource(self)))
        # create_app(self)
        return self.gui



    def login_from_pin(self, result):
        print(f"login response: {result}")
        print(f"self.current_user: {self.current_user}")
        if self.current_user.login_state == LoginState.OUT:
            self.current_user = AccessModel(access_level=result, login_state = LoginState.PIN_IN)
                # if result > 0:
                #     self.change_screen('Control')
                #     self.screens['DoorBell']["object"].login_feedback(True)
                # else:
                #     print("Login failed")
                #     self.screens['DoorBell']["object"].login_feedback(False)



    def log_out(self, *args):
        print(f"Log out, user {self.current_user.name}")
        self.current_user = AccessModel(access_level=0, login_state = LoginState.OUT)
        print(f"Logged out, user {self.current_user}")
        if self.screen_timer.running:
            self.screen_timer.stop()
        if self.log_out_timer.running:
            self.log_out_timer.stop()

        
    def extend_log_out_timer(self):
        self.log_out_timer.reset()


    def start_screen_timer(self):
        self.screen_timer.start()


    def screen_time_out(self):
        self.change_screen('DoorBell')
        if self.current_user.login_state == LoginState.PIN_IN:
            # self.start_log_out_timer()
            self.log_out_timer.start()
        else:
            self.log_out()


    def extend_screen_timer(self):
        self.screen_timer.reset()


    #### MQTT STUFF ####
    def make_client(self):
        # parameters = {'self': self}
        self._mqttc = mqtt.Client(MQTT_CLIENT_ID)
        # self._mqttc = mqtt.Client(MQTT_CLIENT_ID, userdata = parameters)
        self._mqttc.on_message = self.mqtt_on_message
        self._mqttc.on_connect = self.mqtt_on_connect
        self._mqttc.on_publish = self.mqtt_on_publish
        self._mqttc.on_subscribe = self.mqtt_on_subscribe
        # self._mqttc.on_disconnect = self.mqtt_on_disconnect

        self.mqttc_connect_to_broker()



    def mqtt_on_connect(self, mqttc, obj, flags, rc):
        print("rc: "+str(rc))
        print(f"flag: {flags}")
        self.mqttc_subscribe()
        self.mqttc_run()
        


    def mqtt_on_message(self, mqttc, obj, msg):
        print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
        topic = msg.topic
        payload = msg.payload.decode("utf-8") 

        # door = self.doors_config.get_by_state_topic(topic)
        # if door is not None:
        #     print(f"state received")
        #     if payload == DOORLOCK_STATE.LOCKED:
        #         door.state="LOCKED"
        #         self.screens['Control']["object"].update_door_states(door.door_id,True)
                
        #     elif payload == DOORLOCK_STATE.UNLOCKED:
        #         door.state="UNLOCKED"
        #         self.screens['Control']["object"].update_door_states(door.door_id, False)
         
        if topic == self.mode_config.command_topic:
            print(f"mode received: {payload}")
            self.mode_config.state = payload


    def mqtt_on_publish(self, mqttc, obj, mid):
        print("mid: "+str(mid))

    def mqtt_on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def mqtt_on_log(self, mqttc, obj, level, string):
        print(string)

    def tls_set(self):
        #TODO: sett ssl and cert for encrypt
        pass

    def mqttc_connect_to_broker(self):
        print(f"connecting to broker {MQTT_BROKER} as {MQTT_CLIENT_ID}")
        # broker_parsed = urllib.parse.urlparse(MQTT_BROKER)
        self._mqttc.username_pw_set(MQTT_USERNAME, password=MQTT_PASSWORD)
        self._mqttc.connect(MQTT_BROKER, port=MQTT_PORT, keepalive=60)


    def mqttc_subscribe(self):
        # for door in self.doors_config.doors:
        #     print(f"Subscribing: {door.topic.state}")
        #     self._mqttc.subscribe(door.topic.state, qos=1)
        self._mqttc.subscribe(self.mode_config.command_topic, qos=0)
        self._mqttc.subscribe(self.state_config.command_topic, qos=0)

    def mqttc_run(self):     
        self._mqttc.loop_start()

    def ring_bell(self):
        print('ringing that bell')
        print(f'self.mode_config.state: {self.mode_config.state}')
        self._mqttc.publish(self.bell_config.command_topic, payload=BELL_COMMAND_PAYLOAD.DO)
        if self.mode_config.state == MODE_COMMAND_PAYLOAD.NORMAL:
            pass
        elif self.mode_config.state == MODE_COMMAND_PAYLOAD.HALLOWEEN:
           self.change_screen('Scary')




    def toggle_state(self, *args):
        print(f"Toggle state: {args}")
  
        
    def garage_open(self, *args):
        self.garage_command(GARAGE_COMMAND_PAYLOAD.OPEN)

    def garage_close(self, *args):
        self.garage_command(GARAGE_COMMAND_PAYLOAD.CLOSE)

    def garage_stop(self, *args):
        self.garage_command(GARAGE_COMMAND_PAYLOAD.STOP)

    def garage_command(self, command):
        self._mqttc.publish(self.garage_config.command_topic, payload=command)

    def next_screen(self):
        self.change_screen(self.gui.next())

    def prev_screen(self):
        self.change_screen(self.gui.previous())

    def change_screen(self, screen_name):
        if screen_name == 'Control':
            self.start_screen_timer()
        self.gui.current = screen_name


    # def mqtt_on_disconnect(self, client, userdata, rc):
    #     if rc != 0:
    #         print("Unexpected disconnection.")

            # self.mqttc_connect_to_broker()
            # # self.mqttc_subscribe()
            # self.mqttc_run()
