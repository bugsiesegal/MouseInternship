from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.properties import ObjectProperty
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from Utils import FiberPhotometry
from functools import partial


class Menu(GridLayout):
    def switch(self, page, *args):
        print("switch")
        app = App.get_running_app()
        sm = app.sm
        sm.switch_to(page)

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

        load_button.bind(on_press=lambda x: app.data.append(FiberPhotometry.load(path.text)))
        load_button.bind(on_press=lambda x: app.reload())
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

        load_button.bind(on_press=lambda x: app.data.append(FiberPhotometry.batch_load(path.text)))
        load_button.bind(on_press=lambda x: app.reload())
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

        load_button.bind(on_press=lambda x: app.data.append(FiberPhotometry.load_from_tdt(path.text)))
        load_button.bind(on_press=lambda x: app.reload())
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

        load_button.bind(on_press=lambda x: app.data.append(FiberPhotometry.batch_load_from_tdt(path.text)))
        load_button.bind(on_press=lambda x: app.reload())
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

        load_from_tdt_btn = Button(text="Load File", size_hint_y=None, height=44)
        file_from_tdt_popup = self.load_from_tdt_file()
        load_from_tdt_btn.bind(on_release=file_from_tdt_popup.open)

        batch_load_from_tdt_btn = Button(text="Batch Load From TDT File", size_hint_y=None, height=44)
        batch_load_from_tdt_file_popup = self.batch_load_from_tdt_file()
        batch_load_from_tdt_btn.bind(on_release=batch_load_from_tdt_file_popup.open)

        tool_button = Button(text="File")
        toolbar_dropdown.add_widget(load_btn)
        toolbar_dropdown.add_widget(batch_load_btn)
        toolbar_dropdown.add_widget(load_from_tdt_btn)
        toolbar_dropdown.add_widget(batch_load_from_tdt_btn)
        tool_button.bind(on_release=toolbar_dropdown.open)

        menu_dropdown = DropDown()
        for name in sm.screen_names:
            button = Button(
                text=name,
                size_hint_y=None,
                height=44
            )
            screen = sm.get_screen(name)
            button.bind(on_release=lambda button: menu_dropdown.select(screen))
            menu_dropdown.add_widget(button)

        menubutton = Button(text='Pages')
        menubutton.bind(on_release=menu_dropdown.open)
        menu_dropdown.bind(on_select=lambda instance, x: self.switch(x))

        layout.add_widget(tool_button)
        layout.add_widget(menubutton)

        self.add_widget(layout)


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
    graph = ObjectProperty(None)

    def reload(self):
        pass


class AIScreen(BaseScreen):
    pass


class BrainwaveAnalysisApp(App):
    data = []

    def build(self):
        self.sm = ScreenManager(transition=FadeTransition())
        self.analysisscreen = AnalysisScreen(name="Analysis")
        self.sm.add_widget(self.analysisscreen)
        self.aiscreen = AIScreen(name="AI")
        self.sm.add_widget(self.aiscreen)
        self.analysisscreen.build_menu()
        self.aiscreen.build_menu()
        return self.sm

    def reload(self):
        pass


if __name__ == "__main__":
    BrainwaveAnalysisApp().run()
