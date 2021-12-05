from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager


class Menu(GridLayout):
    pass


class AnalysisScreen(Screen):
    pass


class BrainwaveAnalysisApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(AnalysisScreen(name="Analysis"))
        return sm


if __name__ == "__main__":
    BrainwaveAnalysisApp().run()
