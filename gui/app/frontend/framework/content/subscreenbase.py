from threading import Event
from os import path

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import BooleanProperty

from frontend.framework.screen.screenbehaviour import ScreenBehaviour

LOAD_FILE = 'subscreenbase.kv'
FILE_PATH = path.abspath(path.join(path.dirname(__file__), LOAD_FILE))
Builder.load_file(FILE_PATH)

class SubScreenBase(ScreenBehaviour):

    screen_active = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
