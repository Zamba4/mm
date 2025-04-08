# features/sms.py
from core.modem_api import ModemAPI
import html
import xml.etree.ElementTree as ET

class SMSHandler(ModemAPI):
    def get_last_sms(self) -> dict:
        """Получение последнего SMS с исправлением кодировки"""
        try:
            self.auth()  # Обновляем токен и сессию

            # XML-запрос как в оригинальном скрипте
            xml_request = """<?xml version="1.0" encoding="UTF-8"?>
            <request>
                <PageIndex>1</PageIndex>
                <ReadCount>3</ReadCount>
                <BoxType>1</BoxType>
                <SortType>0</SortType>
                <Ascending>0</Ascending>
                <UnreadPreferred>1</UnreadPreferred>
            </request>"""

            headers = {
                "__RequestVerificationToken": self.token,
                "Cookie": f"SessionID={self.session_id}",
                "Content-Type": "text/xml"
            }
            
            response = self.session.post(
                f"http://{self.ip}/api/sms/sms-list",
                headers=headers,
                data=xml_request,
                timeout=10
            )
            response.raise_for_status()

            # Декодируем контент и обрабатываем HTML-сущности
            decoded_content = response.content.decode('utf-8')
            decoded_content = html.unescape(decoded_content)
            
            root = ET.fromstring(decoded_content)
            messages = root.findall(".//Message")
            
            if not messages:
                return {"status": "error", "message": "Нет сообщений"}
                
            last_msg = messages[0]  # Первое сообщение в списке
            
            # Получаем текст сообщения
            content = last_msg.findtext("Content", "")
            text = html.unescape(content).strip()
            
            return {
                "status": "success",
                "date": last_msg.findtext("Date", "Нет даты"),
                "sender": last_msg.findtext("Phone", "Неизвестный номер"),
                "text": text
            }
            
        except Exception as e:
            return {"status": "error", "message": f"{str(e)}"}
