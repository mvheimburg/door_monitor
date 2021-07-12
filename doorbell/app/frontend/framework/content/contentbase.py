#!/usr/anaconda3/envs/grasp_svr/bin/python python3
# -*- coding: utf-8 -*-
__author__ = 'sintefocean'


from os import path
from threading import Event
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout

from kivy.properties import BooleanProperty

from kivymd.theming import ThemableBehavior
# from frontend.theming import ThemableBehavior


from const import (
     SCREEN_WIDTH
    ,SCREEN_HEIGHT
    ,LEFT_BOX_WIDTH
    ,RIGHT_BOX_WIDTH
)

LOAD_FILE = 'contentbase.kv'
FILE_PATH = path.abspath(path.join(path.dirname(__file__), LOAD_FILE))
Builder.load_file(FILE_PATH)


class ContentBase(ThemableBehavior, MDBoxLayout):

    SCREEN_WIDTH = SCREEN_WIDTH
    SCREEN_HEIGHT = SCREEN_HEIGHT
    LEFT_BOX_WIDTH = LEFT_BOX_WIDTH
    RIGHT_BOX_WIDTH = RIGHT_BOX_WIDTH

    _content_active = BooleanProperty(False)

    def __init__(self, sub=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint= None, None
        self.width= SCREEN_WIDTH
        self.height= SCREEN_HEIGHT

        self.app = MDApp.get_running_app()  





    def refresh(self):
        if hasattr(self, '_refresh'):
            self._refresh()