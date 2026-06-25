from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout



class DialogManager:

    @staticmethod
    def show_message(
        title,
        message
    ):
        Popup(
            title=title,
            content=Label(
                text=message
            ),
            size_hint=(.8,.3)
        ).open()
    
    @staticmethod
    def confirm(
    title,
    message,
    yes_callback
    ):
        layout = BoxLayout(
        orientation ="vertical",
        spacing = 10,
        padding = 10   
        )
        
        layout.add_widget(
        Label(text=message))
        
        buttons = BoxLayout(
        spacing = 10)
        
        yes_btn = Button(
        text="yes")
        
        no_btn = Button(
        text="No")
        
        buttons.add_widget(
        yes_btn)
        
        buttons.add_widget(
        no_btn)
        
        layout.add_widget(buttons)
        
        popup=Popup(
        title=title,
        content=layout,
        size_hint=(.8,.4))
        
        yes_btn.bind(
            on_press=lambda x: (
            yes_callback(),
            popup.dismiss()
            )
        )
        
        no_btn.bind(on_press=popup.dismiss)
        
        popup.open()