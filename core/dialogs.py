from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from kivy.app import App
from ui import ui_metrics as metrics
from kivy.uix.textinput import TextInput

from kivy.factory import Factory


class DialogManager:

    @staticmethod
    def show_message(title, message):

        metrics = App.get_running_app().metrics

        layout = BoxLayout(
            orientation="vertical",
            spacing=metrics.Spacing.POPUP,
            padding=metrics.Padding.POPUP
        )

        layout.add_widget(
            Label(text=message)
        )

        ok_btn = Button(
            text="OK",
            background_normal="",
            background_down="",
            background_color=metrics.Color.PRIMARY,
            size_hint_y=None,
            height=metrics.Size.POPUP_BUTTON_HEIGHT
        )

        layout.add_widget(ok_btn)

        popup = Popup(
            title=title,
            content=layout,
            size_hint=metrics.Size.POPUP_SMALL
        )

        ok_btn.bind(on_press=popup.dismiss)

        popup.open()
    
    @staticmethod
    def confirm(
    title,
    message,
    yes_callback
    ):
        metrics = App.get_running_app().metrics

        layout = BoxLayout(
        orientation ="vertical",
        spacing = metrics.Spacing.POPUP,
        padding = metrics.Padding.POPUP   
        )
        
        layout.add_widget(
        Label(text=message))
        
        buttons = BoxLayout(
        spacing = metrics.Spacing.NORMAL)
        
        yes_btn = Button(
            text="Yes",
            background_normal="",
            background_color=metrics.Color.SUCCESS
        )
        
        no_btn = Button(
            text="Cancel",
            background_normal="",
            background_color=metrics.Color.DANGER
        )
        
        buttons.add_widget(
        yes_btn)
        
        buttons.add_widget(
        no_btn)
        
        layout.add_widget(buttons)
        
        popup=Popup(
        title=title,
        content=layout,
        size_hint=metrics.Size.POPUP_MEDIUM
        )
        
        yes_btn.bind(
            on_press=lambda x: (
            yes_callback(),
            popup.dismiss()
            )
        )
        
        no_btn.bind(on_press=popup.dismiss)
        
        popup.open()

    @staticmethod
    def text_input_popup(
        title,
        text="",
        hint_text="",
        button_text="Save",
        callback=None,
    ):
        metrics = App.get_running_app().metrics

        layout = BoxLayout(
            orientation="vertical",
            spacing=metrics.Spacing.POPUP,
            padding=metrics.Padding.POPUP,
        )

        text_input = Factory.AppTextInput(
            text=text,
            hint_text=hint_text,
        )

        save_btn = Factory.AppPrimaryButton(
            text=button_text,
            height=metrics.Size.POPUP_BUTTON_HEIGHT,
        )

        layout.add_widget(text_input)
        layout.add_widget(save_btn)

        popup = Popup(
            title=title,
            content=layout,
            size_hint=metrics.Size.POPUP_SMALL,
        )

        if callback:
            save_btn.bind(
                on_press=lambda *_: callback(
                    text_input.text,
                    popup,
                )
            )

        return popup

    @staticmethod
    def create_popup(title, content, size_hint=None):

        metrics = App.get_running_app().metrics

        return Popup(
            title=title,
            content=content,
            size_hint=size_hint or metrics.Size.POPUP_MEDIUM,
        )