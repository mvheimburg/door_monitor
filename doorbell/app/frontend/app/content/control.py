#!/usr/anaconda3/envs/grasp_svr/bin/python python3
# -*- coding: utf-8 -*-
__author__ = 'mvheimburg'


from os import path

# from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.carousel import MDCarousel
from kivy.uix.image import Image
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.card import MDCard

from kivymd.uix.behaviors import TouchBehavior
from kivy.properties import ObjectProperty, BooleanProperty, DictProperty, StringProperty, BoundedNumericProperty, NumericProperty
from kivy.clock import Clock

from frontend.framework.screen import ScreenBehaviour
from kivymd.uix.screen import MDScreen

from models.memory import DoorState, GarageState

from frontend.utils import hide_widget

from const import (
     CONTROL_TIMEOUT
    ,SCREEN_WIDTH
    ,SCREEN_HEIGHT
    ,LEFT_BOX_WIDTH
    ,RIGHT_BOX_WIDTH
)

LOAD_FILE = 'control.kv'
FILE_PATH = path.abspath(path.join(path.dirname(__file__), LOAD_FILE))
print(FILE_PATH)
Builder.load_file(FILE_PATH)


class DoorCard(MDCard):
    door_id=StringProperty("")
    controller = ObjectProperty(None)
    name=StringProperty("")
    label=BooleanProperty(True)
    size_fac=NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def on_label(self, *args):    
        if not self.label:
            hide_widget(self.ids.doorlabel)
            
    
    def on_size_fac(self, *args):
        self.ids.doorbutt.user_font_size *= self.size_fac
        self.ids.doorlabel.user_font_size *= self.size_fac

        
    def update_state(self, state):
        self.ids.doorbutt.locked = state
        


class DoorButton(MDIconButton):
    locked = BooleanProperty(None)
    locked_icon = "door-closed-lock"
    unlocked_icon = "door-closed"


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon = "lock-question"
        self.user_font_size=60

    
    def on_locked(self, *args):
        if self.locked:
            self.icon = self.locked_icon
        else:
            self.icon = self.unlocked_icon
        

# class DoorControlScreen(MDScreen):

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.register_event_type('on_arrow_next')
#         self.register_event_type('on_arrow_prev')

    
#     def update_state(self, state):
#         self.ids.butt.locked = state
 
#     def on_arrow_next(self):
#         pass

#     def on_arrow_prev(self):
#         pass

#     def arrow_next(self, *args):
#         print("self.dispatch('on_arrow_next')")
#         self.dispatch('on_arrow_next')

#     def arrow_prev(self, *args):
#         self.dispatch('on_arrow_prev')



class Control(ScreenBehaviour):

    # door_states = ObjectProperty(None)
    # door_states= DictProperty()
    garage_state=ObjectProperty()
    timer_object = BoundedNumericProperty(5, min=0, max=CONTROL_TIMEOUT)
    timer = None

    def __init__(self, **kwargs):
        
        super().__init__(**kwargs)
        # self.door_screens = {}

        # for door in self.app.doors_config.doors:
            # self.door_states.update({door.name:DoorState(locked=True)})
            
            # door_screen = DoorControlScreen(name = door.name)
            # door_screen.fbind("on_arrow_next",self.next_screen)
            # door_screen.fbind("on_arrow_prev",self.prev_screen)
            # self.door_screens.update({door.name:door_screen})
            # print(f"adding door screen {door.name}")
            # self.ids.door_sm.add_widget(door_screen)


        self.garage_state = GarageState()
        print('Importing Control')
        # print(f'{self.fakker}')
        # self.door_states = self.app.door_states


    def on_touch_down(self, touch):
        
        # if self.collide_point(touch):
        if self.collide_point(touch.x, touch.y):
            print("reset timer")
            self.timer_object = CONTROL_TIMEOUT
        return super().on_touch_down(touch)

    def _enter(self):
        self.timer_object = CONTROL_TIMEOUT
        self.timer = Clock.schedule_interval(self.tic, 1)
    
    def _leave(self):
        self.timer.cancel()

    def tic(self, dt):
        self.timer_object -= 1

    def on_timer_object(self, *args):
        if self.timer_object == 0:
            self.app.start_log_out_timer()
            self.app.change_screen("DoorBell")


    def on_door_states(self, *args):
        print("CONTROL: ON DOOR STATES")        
        
    def update_door_states(self, door: str, state: bool):
        # self.door_states.update({door:DoorState(locked=state)})
        # self.door_screens[door].update_state(state)
        print(self.ids)
        self.ids[door].update_state(state)
        
    
    def next_screen(self, *args):
        print("next_screen")
        self.ids.door_sm.current = self.ids.door_sm.next()

    def prev_screen(self, *args):
        print("prev_screen")
        self.ids.door_sm.current = self.ids.door_sm.previous()

    def get_door_name(self, door_id):
        return self.app.get_door_name(door_id)