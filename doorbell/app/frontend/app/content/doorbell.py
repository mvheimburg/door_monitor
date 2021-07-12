#!/usr/anaconda3/envs/grasp_svr/bin/python python3
# -*- coding: utf-8 -*-
__author__ = 'mvheimburg'


from os import path

from kivy.lang import Builder
from kivymd.uix.carousel import MDCarousel
from kivy.uix.image import Image, AsyncImage
from kivy.clock import Clock


from kivymd.uix.behaviors import TouchBehavior
from kivy.properties import ObjectProperty

from frontend.framework.screen import ScreenBehaviour
from frontend.app.content.login import Login
from frontend.utils import hide_widget


from const import (
     SCREEN_WIDTH
    ,SCREEN_HEIGHT
    ,LEFT_BOX_WIDTH
    ,RIGHT_BOX_WIDTH
)

LOAD_FILE = 'doorbell.kv'
FILE_PATH = path.abspath(path.join(path.dirname(__file__), LOAD_FILE))
print(FILE_PATH)
Builder.load_file(FILE_PATH)




image_list = [
     'atlas://frontend/assets/familie/familieatlas/1'
    ,'atlas://frontend/assets/familie/familieatlas/2'
    ,'atlas://frontend/assets/familie/familieatlas/3']

class CarouselWithDoubleTap(MDCarousel, TouchBehavior):
    controller = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        for im in image_list:
            print(f"adding image: {im}")
            # add=Image(source=im, nocache=True)
            add=Image(source=im)
            # add.reload()
            self.add_widget(add)
        
        Clock.schedule_interval(self.next_image, 60)


    def on_double_tap(self, *args):
        print('doubltap')
        self.controller.carousel_double_tap()
    

    def next_image(self, dt):
        self.load_next()




class DoorBell(ScreenBehaviour):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print('Importing DoorBell')

        self.login_wid = Login(controller=self)
        #     controller: doorbell)
        # self.hide_login()
        
    def carousel_double_tap(self):
        if self.app.access_level > 0:
            print(f'access_level {self.app.access_level}')
            self.app.change_screen('Control')
        else:
            self.show_login()

    
    def hide_login(self, *args):
        # self.ids.bellbox.opacity = 1
        self.opacity = 1
        print('hide_login!!')

        self.ids.loginbox.remove_widget(self.login_wid)
        self.login_wid.leave()
        hide_widget(self.ids.bellbutton, dohide=False)


    def show_login(self):
        print('show_login!!')
        # self.ids.bellbox.opacity = 0.15
        self.opacity = 0.15
        # hide_widget(self.ids.loginbox, dohide=False)
        self.ids.loginbox.add_widget(self.login_wid)
        self.login_wid.enter()
        hide_widget(self.ids.bellbutton)


    def login_feedback(self, success):
        if success:
            self.hide_login()
        else:
            self.login_wid.login_failed()
