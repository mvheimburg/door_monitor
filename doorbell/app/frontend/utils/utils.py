from subprocess import call
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivy.clock import Clock

# from const import NoneType


def hide_widget(wid, dohide=True):
    """
    Hides a kivy widget.

    Stores relevant size attributes in 'saved_attrs' before disabling/minimizing widget. 
    If dohide=False these saved attributes are reset to original values to reveal the widget.

    Args:
        wid:      Referance to widget that should be hidden or revealed.
        dohide:   True for hide and False for reveal. Defaults to True.

    """
    if hasattr(wid, 'saved_attrs'):
        if not dohide:
            print("SHOW")
            wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
            del wid.saved_attrs
    elif dohide:
        print("DOHIDE")
        wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
        wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True



def show_pop_up(title, text):
    
    pop_up = MDDialog(
        title=title,
        text=text,
        radius=[20, 7, 20, 7],
    )
    
    pop_up.open()



class Timer():
    def __init__(self, callback: callable, time: int) -> None:
        super().__init__()
        self._callback = callback
        self._time_max = time
        self._time_count = time
        self._timer = None
        self._running = False

    @property
    def running(self):
        return self._running

    def reset(self):
        self._time_count = self._time_max

    def start(self):
        print(f"start timer")
        print(f"type(self._timer): {type(self._timer)}")
        if self._timer is None:
            if not self._running:
                self._time_count = self._time_max
                self._timer = Clock.schedule_interval(self.tic, 1)
                self._running = True

    def stop(self):
        print(f"stop timer")
        print(f"type(self._timer): {type(self._timer)}")
        if self._timer is not None:
            if self._running:
                self._timer.cancel()
                self._timer = None
                self._running = False

    def tic(self, dt):
        if self._time_count <= 0:
            print(f"timer finished")
            self.stop()
            self._callback()
        else:
            self._time_count -= 1