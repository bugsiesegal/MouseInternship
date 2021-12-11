from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from functools import partial
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.factory import Factory
from kivy.uix.textinput import TextInput
import re


class Menu(GridLayout):
    def switch(self, page, *args):
        app = App.get_running_app()
        sm = app.sm
        sm.switch_to(page)
    def build_menu(self):
        app = App.get_running_app()
        sm = app.sm
        for name in sm.screen_names:
            print(name)
            button = Button(
                text=name
            )
            screen = sm.get_screen(name)
            button.bind(on_press=partial(self.switch, screen))
            self.add_widget(button)


class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
        self.menu = Menu(
            size_hint=(1, 0.05),
            pos_hint={'center_x': .5, 'center_y': .975}
        )
        self.add_widget(self.menu)

    def build_menu(self):
        self.menu.build_menu()


class AnalysisScreen(BaseScreen):
    pass

class AIScreen(BaseScreen):
    pass

class BrainwaveAnalysisApp(App):
    def build(self):
        self.sm = ScreenManager(transition=FadeTransition())
        analysisscreen = AnalysisScreen(name="Analysis")
        self.sm.add_widget(analysisscreen)
        aiscreen = AIScreen(name="AI")
        self.sm.add_widget(aiscreen)
        analysisscreen.build_menu()
        aiscreen.build_menu()
        return self.sm


if __name__ == "__main__":
    BrainwaveAnalysisApp().run()
