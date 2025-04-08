from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from threading import Thread

# Импорт ваших модулей
from features.internet import InternetManager
from features.sms import SMSHandler

Builder.load_file('main.kv')

class RootWidget(BoxLayout):
    pass

class ModemControlApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return RootWidget()

    def show_loading(self):
        self.root.ids.progress.value = 50

    def hide_loading(self):
        self.root.ids.progress.value = 0

    def update_label(self, text):
        self.root.ids.status_label.text = text

    # Асинхронные операции
    def check_internet_status(self, *args):
        def task():
            try:
                self.show_loading()
                modem = InternetManager()
                status = modem.get_status()
                Clock.schedule_once(lambda dt: self.update_label(
                    f"[b]Статус интернета:[/b]\n{'ВКЛ' if status else 'ВЫКЛ'}"
                ))
            except Exception as e:
                Clock.schedule_once(lambda dt: self.update_label(f"[Ошибка] {str(e)}"))
            finally:
                self.hide_loading()

        Thread(target=task).start()

    def toggle_internet(self, *args):
        def task():
            try:
                self.show_loading()
                modem = InternetManager()
                current_status = modem.get_status()
                modem.toggle(not current_status)
                Clock.schedule_once(lambda dt: self.update_label(
                    f"[b]Интернет {'ВКЛЮЧЕН' if not current_status else 'ВЫКЛЮЧЕН'}[/b]"
                ))
            except Exception as e:
                Clock.schedule_once(lambda dt: self.update_label(f"[Ошибка] {str(e)}"))
            finally:
                self.hide_loading()

        Thread(target=task).start()

    def show_last_sms(self, *args):
        def task():
            try:
                self.show_loading()
                sms = SMSHandler()
                last = sms.get_last_sms()
                
                if last["status"] == "success":
                    text = (
                        f"[b]Последнее SMS:[/b]\n"
                        f"Дата: {last['date']}\n"
                        f"Отправитель: {last['sender']}\n"
                        f"Текст: {last['text']}"
                    )
                else:
                    text = f"[Ошибка] {last['message']}"
                
                Clock.schedule_once(lambda dt: self.update_label(text))
            except Exception as e:
                Clock.schedule_once(lambda dt: self.update_label(f"[Ошибка] {str(e)}"))
            finally:
                self.hide_loading()

        Thread(target=task).start()

if __name__ == '__main__':
    ModemControlApp().run()
