#!/usr/anaconda3/envs/grasp_svr/bin/python python3
# -*- coding: utf-8 -*-
__author__ = 'sintefocean'


from os import path
from threading import Event

from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from kivymd.app import MDApp



LOAD_FILE = 'screenbehaviour.kv'
FILE_PATH = path.abspath(path.join(path.dirname(__file__), LOAD_FILE))
Builder.load_file(FILE_PATH)


class ScreenBehaviour(Screen):

    screen_active = BooleanProperty(False)
    content = ObjectProperty(None)

    def _add_content(self, new_content):
        self.ids.content_container.add_widget(new_content)


    def __init__(self, name=None, content=None, bottombar_mode=None,):
        super().__init__()
        self.name = name

        if content:
            self.content = content
            self._add_content(self.content)

        self.init_complete = Event()

    def enter(self):
        self.screen_active = True
        if hasattr(self.content, 'enter'):
            self.content.enter()

    def leave(self):
        self.screen_active = False
        if hasattr(self.content, 'leave'):
            self.content.leave()
