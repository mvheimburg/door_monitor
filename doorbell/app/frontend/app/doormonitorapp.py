from __future__ import unicode_literals

from os import path
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, DictProperty
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivymd.uix.screen import MDScreen
from kivy.utils import get_color_from_hex


from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivy.network.urlrequest import UrlRequest
import urllib
from jsonsempai import magic

from kivy.lang import Builder
from kivy.clock import Clock

from time import sleep

import paho.mqtt.client as mqtt
import urllib.parse

from kivy.properties import BoundedNumericProperty

from models import MQTTConfig, DoorsConfig
from models.memory import DoorState, GarageState
from kelvin import kelvin_rgb_to_kivy

from const import(
     ACCESS_TIMEOUT
    ,DOORLOCK_COMMAND_PAYLOAD
    ,DOORLOCK_STATUS_PAYLOAD
    ,BELL_COMMAND_PAYLOAD
    ,GARAGE_COMMAND_PAYLOAD
    ,GARAGE_STATUS_PAYLOAD
    ,MODE_COMMAND_PAYLOAD
)

from frontend.app import config

LOAD_FILE = 'doormonitor.kv'
FILE_PATH = path.abspath(path.join(path.dirname(__file__), LOAD_FILE))
Builder.load_file(FILE_PATH)


class DoorMonitorApp(MDApp):
    """
    Frontend for CatchScanner configuration

    """
    connection = ObjectProperty()
    _access_level = NumericProperty(0)
    gui = ObjectProperty()
    api_response = ObjectProperty()

    timer_cnt = BoundedNumericProperty(5, min=0, max=ACCESS_TIMEOUT)
    timer = None
    _mqttc = mqtt.Client

    def __init__(self, mqtt_config, doors_config, bell_config, garage_config, api_config, mode_config):
        super().__init__()

        self.kelvin = kelvin_rgb_to_kivy()
        self.azure = get_color_from_hex('#f0ffff')

        self.theme_cls = ThemeManager()
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.accent_palette = "Yellow"
        self.theme_cls.accent_palette_hue = "500"
        self.theme_cls.theme_style = "Light"

        self.api_config = api_config
        self.mqtt_config = mqtt_config
        self.doors_config = doors_config
        self.bell_config = bell_config
        self.garage_config = garage_config
        self.mode_config = mode_config


        
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
                    # screen_kwargs.update({'controller':self})
                    # screen_kwargs.update({'sub':self.screens[screen].get("sub", None)})
                    # screen_kwargs.update({'memory':kwargs.get(screen,None)})

                    print(f'SCREEN NAME IS: {screen}')
                    print(f'with kwargs: {screen_kwargs}')

                    self.screens[screen]["object"]=eval('NewScreen')(**screen_kwargs)

                    self.gui.add_widget(self.screens[screen]["object"])
            

        self.change_screen(self.gui.screen_names[0])


    def get_door_name(self, door_id, *args):
        print(door_id)
        door = self.doors_config.get_by_id(door_id)
        if door is not None:
            return door.name
        else:
            return ""

    @property
    def access_level(self):
        print(f"current access level: {self._access_level}")
        return self._access_level

    def on_door_states(self, *args):
        print("on_door_states")

    def on_start(self):
        self.make_client()
        


    # def try_pin(self, pin):
    #     """"
    #     Log in.

    #     Log in to sw with user and password. Hardcoded for now. Should interact with DB.

    #     Args:
    #         user:       Username
    #         password:   Password

    #     """
    #     success = False
    #     success = self.api.authenticate_pin(pin)


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
        return self.gui



    def try_login_response(self, *args):
        
        if self.api_response:
            # for key, value in self.api_response.resp_headers.items():
            #     print('{}: {}'.format(key, value))
            print(self.api_response.result)
            try:
                access_level = int(self.api_response.result)
            except Exception as e:
                print(e)
            else:
                self.set_access_level(access_level)

                if self._access_level > 0:
                    self.change_screen('Control')
                    self.screens['DoorBell']["object"].login_feedback(True)
                else:
                    print("Login failed")
                    self.screens['DoorBell']["object"].login_feedback(False)


    def log_out(self, *args):
        self._access_level = 0
        self.change_screen("DoorBell")
        print(f"Log out, access level is: {self._access_level}")

    def set_access_level(self, level):
        self._access_level = level
        print(f"access level is: {self._access_level}")
        

    def start_log_out_timer(self):
        if self._access_level > 0:
            print(f"access timeout set")
            # self.acccess_timeout = Clock.schedule_once(self.acccess_timeout, ACCESS_TIMEOUT)
            self.timer_cnt = ACCESS_TIMEOUT
            self.timer = Clock.schedule_interval(self.tic, 1)
    

    def cancel_log_out_timer(self):
        self.timer.cancel()


    def tic(self, dt):
        self.timer_cnt -= 1


    def on_timer_cnt(self, *args):
        if self.timer_cnt == 0:
            self.cancel_log_out_timer()
            self.log_out()


    def extend_log_out_timer(self):
        self.timer_cnt = ACCESS_TIMEOUT


    # def acccess_timeout(self, dt):
    #     self.log_out()
    #     print(f"access level timeout")
    #     self.acccess_timeout.cancel()
            


    def try_login(self, pin, *args):
        req = f"{self.api_config.url}/get_access_level_by_pin/{pin}"
        print(f"making request: {req}")
        self.api_response = UrlRequest(req, on_success=self.try_login_response)
        # self.change_screen('Control')



    #### MQTT STUFF ####
    def make_client(self):
        # parameters = {'self': self}
        self._mqttc = mqtt.Client(self.mqtt_config.client_id)
        # self._mqttc = mqtt.Client(self.mqtt_config.client_id, userdata = parameters)
        self._mqttc.on_message = self.mqtt_on_message
        self._mqttc.on_connect = self.mqtt_on_connect
        self._mqttc.on_publish = self.mqtt_on_publish
        self._mqttc.on_subscribe = self.mqtt_on_subscribe
        self.mqttc_connect_to_broker()
        self.mqttc_subscribe()
        self.mqttc_run()


    def mqtt_on_connect(self, mqttc, obj, flags, rc):
        print("rc: "+str(rc))
        print(f"flag: {flags}")


    def mqtt_on_message(self, mqttc, obj, msg):
        print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
        topic = msg.topic
        payload = msg.payload.decode("utf-8") 

        door = self.doors_config.get_by_state_topic(topic)
        if door is not None:
            print(f"state received")
            if payload == DOORLOCK_STATUS_PAYLOAD.LOCKED:
                door.state="LOCKED"
                self.screens['Control']["object"].update_door_states(door.door_id,True)
                
            elif payload == DOORLOCK_STATUS_PAYLOAD.UNLOCKED:
                door.state="UNLOCKED"
                self.screens['Control']["object"].update_door_states(door.door_id, False)
         
        elif topic == self.mode_config.command_topic:
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
        print(f"connecting to broker {self.mqtt_config.broker} as {self.mqtt_config.client_id}")
        # broker_parsed = urllib.parse.urlparse(self.mqtt_config.broker)
        self._mqttc.username_pw_set(self.mqtt_config.username, password=self.mqtt_config.password)
        self._mqttc.connect(self.mqtt_config.broker, port=self.mqtt_config.port, keepalive=60)


    def mqttc_subscribe(self):
        for door in self.doors_config.doors:
            self._mqttc.subscribe(door.state_topic, qos=0)
        self._mqttc.subscribe(self.mode_config.command_topic, qos=0)

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



    def toggle_door(self, door, locked, *args):
        if locked:
            
            for d in self.doors_config.doors:
                if d.name == door:
                    print(f"mqtt unlock door {door}")
                    self._mqttc.publish(d.command_topic, payload= DOORLOCK_COMMAND_PAYLOAD.UNLOCK)
        else:
            for d in self.doors_config.doors:
                if d.name == door:
                    print(f"mqtt lock door {door}")
                    self._mqttc.publish(d.command_topic, payload= DOORLOCK_COMMAND_PAYLOAD.LOCK)
        
        
    def garage_open(self, *args):
         self._mqttc.publish(self.garage_config.command_topic, payload= GARAGE_COMMAND_PAYLOAD.OPEN)

    def garage_close(self, *args):
         self._mqttc.publish(self.garage_config.command_topic, payload= GARAGE_COMMAND_PAYLOAD.CLOSE)

    def garage_stop(self, *args):
         self._mqttc.publish(self.garage_config.command_topic, payload= GARAGE_COMMAND_PAYLOAD.STOP)


    def next_screen(self):
        self.change_screen(self.gui.next())


    def prev_screen(self):
        self.change_screen(self.gui.previous())


    def change_screen(self, screen_name):

        print(f"entering screen {screen_name}")

        # if screen_name == self.ids['sm'].screen_names[0]:
        #     print(f"screen is first")
        #     self.ids['sm'].current_screen.content.is_first()

        # else:
        #     print(f"screen is inbetween")
        #     # self.ids['sm'].current_screen.content.override_allow_prev(True)

        # if screen_name == self.ids['sm'].screen_names[-1]:
        #     print(f"screen is last")
        #     self.ids['sm'].current_screen.content.is_last()

        self.gui.current = screen_name