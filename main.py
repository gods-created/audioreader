from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from services import (
    enable_task as enable_task_service, 
    disable_task as disable_task_service
)
from multiprocessing import Process, freeze_support
from dotenv import load_dotenv

class AudioReaderApp(App):
    def enable_task(self, *args, **kwargs) -> None:
        if not hasattr(self, 'process') or self.process is None:
            self.process = Process(
                name='enable_task_service',
                target=enable_task_service
            )
            self.process.start()

            self.label.text = 'Task on'

    def disable_task(self, *args, **kwargs) -> None:
        if hasattr(self, 'process') and not self.process is None:
            disable_task_service(self.process)
            self.process = None
            self.label.text = 'Task off'

    def build(self):
        btn_enable = Button(
            text='Enable',
            on_press=self.enable_task
        )
        btn_disable = Button(
            text='Disable', 
            on_press=self.disable_task
        )

        btn_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(0.5, None),
            spacing=20
        )
        btn_layout.add_widget(btn_enable)
        btn_layout.add_widget(btn_disable)

        self.label = Label(
            text='Task off',
            font_size=80,
            size_hint=(None, None),
            size=(400, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.6}
        )

        root = FloatLayout()
        root.add_widget(self.label)
        root.add_widget(btn_layout)

        btn_layout.pos_hint = {'center_x': 0.5, 'y': 0.1}

        return root

if __name__ == '__main__':
    freeze_support()
    load_dotenv()
    AudioReaderApp().run()

# pyinstaller --one-file --console main.py