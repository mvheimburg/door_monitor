from os import path
from threading import Thread
import random
import time

from kivy.clock import Clock

from frontend.framework.screen import ScreenBehaviour
from kivy.uix.image import Image

from kivy.lang import Builder


LOAD_FILE = 'scary.kv'
FILE_PATH = path.abspath(path.join(path.dirname(__file__), LOAD_FILE))
print(FILE_PATH)
Builder.load_file(FILE_PATH)


class Scary(ScreenBehaviour):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print('Importing Scary')
        self.scary_image = Image(source='frontend/assets/halloween/jackolantern.png')
        self.add_widget(self.scary_image)
        self.show_img(False)


    def _enter(self):
        self.show_img(False)
        Clock.schedule_once(self.go_back, 10)
        self.cycle = 1
        self.t = Thread(target=self.cycle_img, args=())
        self.t.start()

    def _leave(self):
        self.cycle = 0
        self.t.join()
        self.show_img(False)


    def cycle_img(self):
        print("Adding scary image")
        show=False
        time.sleep(2)
        Clock.schedule_once(self.stop_cycle, 3)
        while self.cycle:
            pause = random.randint(1, 5) / 30
            self.show_img(show)
            show = not show
            time.sleep(pause)
        self.show_img()


    def stop_cycle(self,dt):
        self.cycle = 0

    def show_img(self, show:bool=True):
        if show:
            self.scary_image.opacity = 1
        else:
            self.scary_image.opacity = 0

    def go_back(self, dt):
        self.app.change_screen('DoorBell')