import threading

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.uix.textinput import TextInput

from AI import FiberPhotometryModel
from Utils import FiberPhotometry
from MouseIO import load, save, batch_load, batch_save
import pandas as pd
import numpy as np
import os, sys
from kivy.resources import resource_add_path, resource_find

class Menu(GridLayout):
    def switch(self, page, *args):
        print(page)
        app = App.get_running_app()
        sm = app.sm
        sm.switch_to(sm.get_screen(page))

    def load_file(self):
        app = App.get_running_app()

        box_layout = BoxLayout(orientation="vertical")
        path = TextInput(multiline=False, hint_text="Path")
        load_button = Button(text='Load File')

        popup = Popup(auto_dismiss=True,
                      size_hint=(None, None),
                      size=(600, 200),
                      title="Load File"
                      )

        load_button.bind(on_press=lambda x: app.set_data(load(path.text)))
        load_button.bind(on_press=popup.dismiss)

        box_layout.add_widget(path)
        box_layout.add_widget(load_button)

        popup.add_widget(box_layout)
        return popup

    def batch_load_file(self):
        app = App.get_running_app()

        box_layout = BoxLayout(orientation="vertical")
        path = TextInput(multiline=False, hint_text="Path")
        load_button = Button(text='Batch Load File')

        popup = Popup(auto_dismiss=True,
                      size_hint=(None, None),
                      size=(600, 200),
                      title="Batch Load File"
                      )

        load_button.bind(on_press=lambda x: app.set_data(batch_load(path.text)))
        load_button.bind(on_press=popup.dismiss)

        box_layout.add_widget(path)
        box_layout.add_widget(load_button)

        popup.add_widget(box_layout)
        return popup

    def load_from_tdt_file(self):
        app = App.get_running_app()

        box_layout = BoxLayout(orientation="vertical")
        path = TextInput(multiline=False, hint_text="Path")
        load_button = Button(text='Load From TDT File')

        popup = Popup(auto_dismiss=True,
                      size_hint=(None, None),
                      size=(600, 200),
                      title="Load From TDT File"
                      )

        load_button.bind(on_press=lambda x: app.set_data(load(path.text)))
        load_button.bind(on_press=popup.dismiss)

        box_layout.add_widget(path)
        box_layout.add_widget(load_button)

        popup.add_widget(box_layout)
        return popup

    def batch_load_from_tdt_file(self):
        app = App.get_running_app()

        box_layout = BoxLayout(orientation="vertical")
        path = TextInput(multiline=False, hint_text="Path")
        load_button = Button(text='Batch Load From TDT File')

        popup = Popup(auto_dismiss=True,
                      size_hint=(None, None),
                      size=(600, 200),
                      title="Batch Load From TDT File"
                      )

        load_button.bind(on_press=lambda x: app.set_data(batch_load(path.text)))
        load_button.bind(on_press=popup.dismiss)

        box_layout.add_widget(path)
        box_layout.add_widget(load_button)

        popup.add_widget(box_layout)
        return popup

    def batch_save_file(self):
        app = App.get_running_app()

        box_layout = BoxLayout(orientation="vertical")
        path = TextInput(multiline=False, hint_text="Path")
        load_button = Button(text='Batch Save File')

        popup = Popup(auto_dismiss=True,
                      size_hint=(None, None),
                      size=(600, 200),
                      title="Batch Save File"
                      )

        load_button.bind(on_press=lambda x: app.data.append(batch_save(app.data, path.text)))
        load_button.bind(on_press=popup.dismiss)

        box_layout.add_widget(path)
        box_layout.add_widget(load_button)

        popup.add_widget(box_layout)
        return popup

    def build_menu(self):
        app = App.get_running_app()
        sm = app.sm
        layout = GridLayout(rows=1)

        toolbar_dropdown = DropDown()

        load_btn = Button(text="Load File", size_hint_y=None, height=44)
        file_popup = self.load_file()
        load_btn.bind(on_release=file_popup.open)

        batch_load_btn = Button(text="Batch Load File", size_hint_y=None, height=44)
        batch_file_popup = self.batch_load_file()
        batch_load_btn.bind(on_release=batch_file_popup.open)

        load_from_tdt_btn = Button(text="Load From TDT File", size_hint_y=None, height=44)
        file_from_tdt_popup = self.load_from_tdt_file()
        load_from_tdt_btn.bind(on_release=file_from_tdt_popup.open)

        batch_load_from_tdt_btn = Button(text="Batch Load From TDT File", size_hint_y=None, height=44)
        batch_load_from_tdt_file_popup = self.batch_load_from_tdt_file()
        batch_load_from_tdt_btn.bind(on_release=batch_load_from_tdt_file_popup.open)

        batch_save_btn = Button(text="Batch Save File", size_hint_y=None, height=44)
        batch_save_file_popup = self.batch_save_file()
        batch_save_btn.bind(on_release=batch_save_file_popup.open)

        tool_button = Button(text="File")
        toolbar_dropdown.add_widget(load_btn)
        toolbar_dropdown.add_widget(batch_load_btn)
        toolbar_dropdown.add_widget(load_from_tdt_btn)
        toolbar_dropdown.add_widget(batch_load_from_tdt_btn)
        toolbar_dropdown.add_widget(batch_save_btn)
        tool_button.bind(on_release=toolbar_dropdown.open)

        for name in sm.screen_names:
            button = Button(
                text=name,
                size_hint_y=None,
                height=44
            )
            print(name)
            button.bind(on_release=lambda button: self.switch(button.text))
            layout.add_widget(button)

        layout.add_widget(tool_button)

        self.add_widget(layout)


class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.menu = Menu(
            size_hint=(1, 0.05),
            pos_hint={'center_x': .5, 'center_y': .975}
        )
        self.add_widget(self.menu)

    def build_menu(self):
        self.menu.build_menu()


class AnalysisScreen(BaseScreen):
    graph = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def split_data(self, window_size):
        self.app.set_windows(FiberPhotometry.batch_to_window(self.app.data, window_size))
        self.app.window_size = window_size


class AIScreen(BaseScreen):
    def build_ai(self, compression, dropout, learning_rate):
        self.app.model = FiberPhotometryModel(window_size=self.app.window_size, learning_rate=learning_rate)
        self.app.model.build_cnn_model(compression, dropout)

    def train_ai(self, epochs):
        t1 = threading.Thread(target=self.app.model.train, args=(self.app.windows, epochs))
        t1.start()
        t1.join()

    def save_model(self):
        app = App.get_running_app()

        box_layout = BoxLayout(orientation="vertical")
        path = TextInput(multiline=False, hint_text="Path")
        load_button = Button(text='Save Model')

        popup = Popup(auto_dismiss=True,
                      size_hint=(None, None),
                      size=(600, 200),
                      title="Save Model"
                      )

        load_button.bind(on_press=lambda x: app.model.save(path))
        load_button.bind(on_press=popup.dismiss)

        box_layout.add_widget(path)
        box_layout.add_widget(load_button)

        popup.add_widget(box_layout)
        return popup

    def load_model(self):
        app = App.get_running_app()

        box_layout = BoxLayout(orientation="vertical")
        path = TextInput(multiline=False, hint_text="Path")
        load_button = Button(text='Load Model')

        popup = Popup(auto_dismiss=True,
                      size_hint=(None, None),
                      size=(600, 200),
                      title="Load Model"
                      )

        load_button.bind(on_press=lambda x: app.model.load(path))
        load_button.bind(on_press=popup.dismiss)

        box_layout.add_widget(path)
        box_layout.add_widget(load_button)

        popup.add_widget(box_layout)
        return popup

    def predict_behavior(self, path):
        for file_num, windows in enumerate(self.app.windows):
            data = self.app.model.enc_predict(windows.data)
            data.flatten()
            num_samples = len(windows.data)
            times = np.linspace(1, num_samples, num_samples) / windows.frequency
            data = pd.DataFrame([times, data])
            data.to_csv(path+str(file_num)+".csv")




class BrainwaveAnalysisApp(App):
    data = []
    windows = []
    window_size = None
    model = None

    def set_data(self, data):
        self.data = data
        print(self.data)

    def set_windows(self, windows):
        print(windows)
        self.windows = windows

    def build(self):
        self.sm = ScreenManager(transition=FadeTransition())
        self.analysisscreen = AnalysisScreen(name="Analysis")
        self.sm.add_widget(self.analysisscreen)
        self.aiscreen = AIScreen(name="AI")
        self.sm.add_widget(self.aiscreen)

        self.aiscreen.build_menu()
        self.analysisscreen.build_menu()
        return self.sm


if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    BrainwaveAnalysisApp().run()
