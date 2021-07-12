from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard


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


# def show_input_dialog(**kwargs):

#     title = kwargs.get('text', None)
#     hint_text = kwargs.get('hint_text', None)
#     callback = kwargs.get('callback', None)

#     content = InputCard()

#     input_dialog = MDDialog(
#             title=title,
#             text=hint_text,
#             content_cls=content,
#             buttons=[
#                     MDFlatButton(
#                         text="CANCEL",
#                         text_color=self.app.theme_cls.primary_color,
#                     ),
#                     MDFlatButton(
#                         text="ACCEPT",
#                         text_color=self.app.theme_cls.primary_color,
#                     ),
#                 ],
#     )
#     input_dialog.open()