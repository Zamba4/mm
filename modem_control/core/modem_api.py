# core/modem_api.py
import requests
import xml.etree.ElementTree as ET

class ModemAPI:
    def __init__(self, ip: str = "192.168.8.1"):
        self.ip = ip
        self.session = requests.Session()
        self.token = None
        self.session_id = None
        
    def auth(self):
        """Получение токена и сессии"""
        try:
            response = self.session.get(f"http://{self.ip}/api/webserver/SesTokInfo")
            response.raise_for_status()
            root = ET.fromstring(response.text)
            
            # Получаем токен
            tok_element = root.find(".//TokInfo")
            if tok_element is None:
                raise ValueError("Не найден токен авторизации")
            self.token = tok_element.text
            
            # Получаем SessionID
            ses_element = root.find(".//SesInfo")
            if ses_element is None:
                raise ValueError("Не найден SessionID")
            self.session_id = ses_element.text.split("SessionID=")[1].split(";")[0]
            
        except Exception as e:
            print(f"Ошибка авторизации: {str(e)}")
            raise

    def make_request(self, method: str, endpoint: str, data: str = None):
        """Универсальный метод для запросов"""
        try:
            if not self.token:
                self.auth()
                
            headers = {
                "__RequestVerificationToken": self.token,
                "Cookie": f"SessionID={self.session_id}",
                "Content-Type": "text/xml" if method == "POST" else ""
            }
            
            response = self.session.request(
                method,
                f"http://{self.ip}{endpoint}",
                headers=headers,
                data=data
            )
            response.raise_for_status()
            return ET.fromstring(response.text)
            
        except Exception as e:
            print(f"Ошибка запроса: {str(e)}")
            raise
