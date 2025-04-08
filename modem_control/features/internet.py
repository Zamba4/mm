# features/internet.py
from core.modem_api import ModemAPI

class InternetManager(ModemAPI):
    def get_status(self) -> bool:
        """Проверка статуса интернета"""
        root = self.make_request("GET", "/api/dialup/mobile-dataswitch")
        dataswitch = root.find(".//dataswitch")
        return dataswitch.text == "1"

    def toggle(self, enable: bool):
        """Включение/выключение интернета"""
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
        <request>
            <dataswitch>{1 if enable else 0}</dataswitch>
        </request>"""
        self.make_request("POST", "/api/dialup/mobile-dataswitch", data=xml)
        print("Статус изменён!")
