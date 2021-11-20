#!/usr/anaconda3/envs/grasp_svr/bin/python python3
# -*- coding: utf-8 -*-
__author__ = 'mvheimburg'


from os import path
from functools import partial

from kivy.lang import Builder
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout

from kivy.properties import VariableListProperty, ObjectProperty, BoundedNumericProperty, ListProperty, StringProperty, NumericProperty
from kivymd.toast import toast
from kivy.clock import Clock
from kivy.animation import Animation

from frontend.framework.content import ContentBase


from const import(
     LOGIN_TIMOUT
    ,PIN_SIZE
)

LOAD_FILE = 'login.kv'
FILE_PATH = path.abspath(path.join(path.dirname(__file__), LOAD_FILE))
print(FILE_PATH)
Builder.load_file(FILE_PATH)


# class KeypadButton(MDButton):
dist_var = 20
opacity_fac = 9


class PinIcon(MDIcon):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_font_size=35
        self.opacity = opacity_fac


class NumericButton(MDIconButton):

    number = NumericProperty(99)
    action = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_font_size=60
        self.opacity = opacity_fac

    def on_number(self, *args):
        print(f"this text = {self.number}")
        self.icon= f"numeric-{self.number}-circle-outline"
        




class KeyPad(MDGridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.size_hint= None, None
        # self.width= 480
        # self.height= 380
        self.adaptive_size = True

        # self.valign = "center"
        self.padding = dist_var
        self.spacing = [dist_var,dist_var]

        self.cols = 3
        self.rows = 4



class ActionPad(MDGridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint= None, None
        self.width= 240
        self.height= 380

        self.valign = "center"
        self.padding = dist_var
        self.spacing = [dist_var,dist_var]

        self.cols = 1
        self.rows = 3



class Login(ContentBase):
    controller = ObjectProperty()
    current_pin = VariableListProperty([0])
    icon_list=ListProperty(["checkbox-blank-circle-outline"]*4)
    current_pin_idx = BoundedNumericProperty(-1, min=-1, max=PIN_SIZE-1)

    entry_object = BoundedNumericProperty(5, min=0, max=5)
    entry = None
    timeout_object = BoundedNumericProperty(LOGIN_TIMOUT, min=0, max=LOGIN_TIMOUT)
    timeout = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controller = kwargs.pop('controller', None)
        # self.opacity = 0.01
        self.opacity = 0.1


    def on_touch_down(self, touch):
        
        # if self.collide_point(touch):
        if self.collide_point(touch.x, touch.y):
            print("reset login timer")
            self.timeout_object = LOGIN_TIMOUT
        return super().on_touch_down(touch)


    def enter(self):
        self.reset_pin()
        self.timeout_object = LOGIN_TIMOUT
        self.timeout = Clock.schedule_interval(self.tic_timeout, 1)
        self.entry_object = 2
        self.entry = Clock.schedule_interval(self.tic_entry, 0.1)
    

    def leave(self):
        if self.timeout is not None:
            self.timeout.cancel()
            self.timeout=None

        if self.entry is not None:
            self.entry.cancel()
            self.entry=None

    def tic_timeout(self, dt):
        if self.timeout_object > 0:
            self.timeout_object -= 1

    def tic_entry(self, dt):
        if self.entry_object > 0:
            self.entry_object -= 1

        elif self.entry_object == 0:
            if self.entry is not None:
                self.entry.cancel()
                self.entry=None


    def on_timeout_object(self, *args):
        if self.timeout_object == 0:
            self.app.start_log_out_timer()
            self.controller.hide_login()



    def number_input(self, input):
        if not self.entry_object > 0:
            try:
                self.current_pin_idx +=1
            except ValueError as v:
                toast("Kun 4 siffer i pin")
            finally:
                self.current_pin[self.current_pin_idx]=int(input)
                self.icon_list[self.current_pin_idx]="checkbox-blank-circle"

            if self.current_pin_idx == PIN_SIZE-1:
                pin=f"{self.current_pin[0]}{self.current_pin[1]}{self.current_pin[2]}{self.current_pin[3]}"
                self.app.try_login(pin=pin)



    def action_input(self, input):
        if input == 'cancel':
            self.controller.hide_login()

        elif input == 'clear':
            self.reset_pin()

    
    def reset_pin(self):
            self.current_pin_idx = -1
            self.current_pin=[0]*PIN_SIZE
            self.icon_list=["checkbox-blank-circle-outline"]*PIN_SIZE


    def login_failed(self):
        self.action_input('clear')
        toast('Ingen bruker matcher PIN kode')


    def wobble(self):
        anim = Animation(pos=(80, 10))
        anim &= Animation(size=(800, 800), duration=2.)
        anim.start(self)