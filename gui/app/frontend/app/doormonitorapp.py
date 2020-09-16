# from kivy.core.window import Window

from os import path
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.utils import get_color_from_hex

from kivymd.app import MDApp
# from kivymd.theming import ThemeManager


from frontend.theming import ThemeManager
from frontend.app.gui import  GUI
from definitions import ROOT_DIR


from kivy.config import Config
        

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.write()

# from kivy.atlas import Atlas

# familyatlaspath = path.join(ROOT_DIR + '/frontend/assets/familie/familieatlas.atlas')
# atlas  = Atlas(familyatlaspath)

class DoorMonitorApp(MDApp):
    """
    Frontend for CatchScanner configuration

    """
    access_level = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__()

        
        self.azure = get_color_from_hex('#f0ffff')

        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.accent_palette = "Yellow"
        self.theme_cls.accent_palette_hue = "500"
        self.theme_cls.theme_style = "Dark"

        self.worker = kwargs.get('worker', None)

        # NavigationDrawer
        self.gui = GUI(**kwargs)

        # Window.borderless = True
        # Window.fullscreen = True


    def screen_change(self, name, sub_in=None):
        """
        Screen change request.

        Forward request to main_panel holding the screen manager.


        Args:
            name_screen: Requested new sreen name

        """

        self.gui.screen_change(name=name, sub_in=sub_in)


    def try_pin(self, pin):
        """"
        Log in.

        Log in to sw with user and password. Hardcoded for now. Should interact with DB.

        Args:
            user:       Username
            password:   Password

        """
        success = False
        success = self.server.authenticate_pin(pin)


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