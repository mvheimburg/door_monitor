from os import path

from jsonsempai import magic

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp


from frontend.theming import ThemableBehavior
from frontend.framework.screen import RootScreen

### Import config.jason
from frontend.app import config

LOAD_FILE = 'gui.kv'
FILE_PATH = path.abspath(path.join(path.dirname(__file__), LOAD_FILE))
Builder.load_file(FILE_PATH)



class GUI(Screen):
    """ 
    Catch Scanner main panel.

    Main panel holds screen manager and bottombar.

    """
    
    
    def __init__(self, **kwargs):
        super().__init__()
        self.app = MDApp.get_running_app()

        for screen in config.screens:
            print(f"Config access level = {config.screens[screen]['access_level']}")
            print(f"App access level = {self.app.access_level}")
            if config.screens[screen]['access_level'] == self.app.access_level:
               

                if "import" in config.screens[screen]:
                    print(f"Screen accepted = {screen}")
                    exec(config.screens[screen]["import"])
                    config.screens[screen]["object"] = RootScreen(name=screen, content=eval(config.screens[screen]["content"])(**kwargs))
                    self.ids.sm.add_widget(config.screens[screen]["object"])
            

        self.change_screen(self.ids['sm'].screen_names[0])
        
    def next_screen(self):
        self.change_screen(self.ids['sm'].next())


    def prev_screen(self):
        self.change_screen(self.ids['sm'].previous())


    def change_screen(self, screen_name):

        print(f"entering screen {screen_name}")

        # if screen_name == self.ids['sm'].screen_names[0]:
        #     self.logger.debug(f"screen is first")
        #     self.ids['sm'].current_screen.content.is_first()

        # else:
        #     self.logger.debug(f"screen is inbetween")
        #     # self.ids['sm'].current_screen.content.override_allow_prev(True)

        # if screen_name == self.ids['sm'].screen_names[-1]:
        #     self.logger.debug(f"screen is last")
        #     self.ids['sm'].current_screen.content.is_last()

        self.ids['sm'].current = screen_name