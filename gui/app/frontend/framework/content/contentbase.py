#!/usr/anaconda3/envs/grasp_svr/bin/python python3
# -*- coding: utf-8 -*-
__author__ = 'sintefocean'


from os import path
from threading import Event

from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.properties import BooleanProperty

from frontend.theming import ThemableBehavior


LOAD_FILE = 'contentbase.kv'
FILE_PATH = path.abspath(path.join(path.dirname(__file__), LOAD_FILE))
Builder.load_file(FILE_PATH)


class ContentBase(ThemableBehavior, BoxLayout):

    _content_active = BooleanProperty(False)

    def __init__(self, sub=None, **kwargs):
        super().__init__(**kwargs)
        self.server = kwargs.get('server', None)

        if sub is not None:
            self.sub = sub
            self._add_sub_content(**kwargs)

        self.init_complete = Event()


    def _add_sub_content(self, **kwargs):
        if self.sub is not None:
            for content in self.sub:
                if "import" in self.sub[content]:
                    exec(self.sub[content]["import"])
                    
                kwargs.update({'name':content}) 
                self.sub[content]["object"] = eval(self.sub[content]["content"])(**kwargs)
                self.ids['sub_content'].add_widget(self.sub[content]['object'])


    def enter(self):
        self._content_active = True

        if hasattr(self, '_enter'):
            self._enter()


    def leave(self):
        self._content_active = False

        if hasattr(self, '_leave'):
            self._leave()


    def refresh(self):
        if hasattr(self, '_refresh'):
            self._refresh()