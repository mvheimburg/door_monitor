# -*- coding: utf-8 -*-
__author__ = 'sintefocean'


from threading import Event
from os import path 

from kivymd.app import MDApp
from kivy.properties import BooleanProperty, ObjectProperty
# from kivy.uix.screenmanager import Screen
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.metrics import dp

from kivymd.theming import ThemableBehavior

from const import (
     SCREEN_WIDTH
    ,SCREEN_HEIGHT
    ,LEFT_BOX_WIDTH
    ,RIGHT_BOX_WIDTH
)

# LOAD_FILE = 'screenbehaviour.kv'
# FILE_PATH = path.abspath(path.join(path.dirname(__file__), LOAD_FILE))
# Builder.load_file(FILE_PATH)

class ScreenBehaviour(MDScreen, ThemableBehavior):
    SCREEN_WIDTH = SCREEN_WIDTH
    SCREEN_HEIGHT = SCREEN_HEIGHT
    LEFT_BOX_WIDTH = LEFT_BOX_WIDTH
    RIGHT_BOX_WIDTH = RIGHT_BOX_WIDTH

    def __init__(self, **kwargs):
        self.size_hint= None, None
        self.width= SCREEN_WIDTH
        self.height= SCREEN_HEIGHT

        # self.sub = kwargs.pop('sub', None)
        # # self.controller = kwargs.pop('controller', None)

        # self.memory=kwargs.pop('memory', None)
        self.content_active = False
        super().__init__(**kwargs)

        self.app = MDApp.get_running_app()

        # if self.sub is not None:
        #     self._add_sub_content()

        # self.init_complete = Event()

    # def _add_sub_content(self):
    #     for item in self.sub['items']:
    #         try:
    #             import_statemet = self.sub['items'][item]["import"]+' as Item'
    #             print(import_statemet)
    #             exec(import_statemet)
    #         except Exception as e:
    #             print(e)
    #         else:
    #             kwargs = {}
    #             kwargs.update({'name':item})
    #             # kwargs.update({'sub':self.sub['items'][item].get("sub", None)})
    #             self.sub['items'][item]["object"]=eval('Item')(**kwargs)
    #             # self.screens[screen]["object"]=eval('Content')(**kwargs)
    #             self.ids.sub_content.add_widget(self.sub['items'][item]["object"])
         

    def on_enter(self):
        print(f"entering screen: {self.__class__}, with name {self.name}")
        self.content_active = True
        try:
            self._enter()
        except AttributeError as e:
            print(e)


    def on_leave(self):
        print(f"leaving screen: {self.__class__}, with name {self.name}")
        self.content_active = False
        try:
            self._leave()
        except AttributeError as e:
            print(e)


    # def change_sub_screen(self, name):
    #     self.content.change_screen(name)


    # def state_changed(self, state):
    #     try:
    #         self._state_changed(state)
    #     except AttributeError as e:
    #         print(e)


    # def on_memory(self):
    #     print("on_memory")