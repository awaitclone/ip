from .. import loader, utils
from telethon.tl.types import Message
import asyncio
import time
from telethon.errors import FloodWaitError

@loader.tds
class MyBroadcasterMod(loader.Module):
    """Custom message broadcaster"""
    strings = {
        "name": "MyBroadcaster",
        "success": "<b>Сообщение отправлено успешно!</b>",
        "error": "<b>Ошибка при отправке сообщения:</b> {}",
        "broadcast_on": "<b>Рассылка включена.</b>",
        "broadcast_off": "<b>Рассылка выключена.</b>",
        "wait_error": "<b>Ожидание отправки следующего сообщения...</b>"
    }

    def __init__(self):
        self.broadcast_enabled = False

    async def client_ready(self, client, db):
        self.client = client

    async def send_message(self):
        if not self.broadcast_enabled:
            return False
        try:
            image_url = 'https://i.imgur.com/iOYNbtV.png'
            message_text = (
                "<b>ЗАЕБАЛСЯ ИСКАТЬ </b><b><u>НЕ ДОРОГОЙ</u> НО </b><b><u>КАЧЕСТВЕННЫЙ</u> ДИЗАЙН ❓</b>\n\n"
                "Рады вам представить — <b>MORIA DESIGN</b>, лучший дизайн за лучшие цены во всем рынке,\n"
                "средний чек — <b>250-500₽</b>\n\n"
                "🖌️Делаем:\n"
                "— <b>Аватарки</b>\n"
                "— <b>Рекламные баннеры</b>\n"  
                "— <b>Оформление тем</b>\n"
                "— <b>Анимированные работы</b>\n\n"
                "Портфолио: <a href='https://t.me/+wn_45A9wkbViMmFi'><b>@moriadesign</b></a>\n"
                "Связь: <b>@imfckngmoriarty</b>\n"
                "Гарант: <b>@zelenka_guarantor_robot</b>"
            )
            await self.client.send_file('zelenka_services', image_url, caption=message_text, parse_mode='html')
            await self.client.send_message('gdfgdfgdf235453', self.strings("success"), parse_mode='html')
            return True
        except FloodWaitError as e:
            wait_time = e.seconds
            await self.client.send_message('gdfgdfgdf235453', f"{self.strings('wait_error')} {wait_time} секунд.", parse_mode='html')
            await asyncio.sleep(wait_time)
            return False
        except Exception as e:
            await self.client.send_message('gdfgdfgdf235453', self.strings("error").format(str(e)), parse_mode='html')
            return False

    @loader.command(ru_doc="Запустить рассылку сообщений")
    async def startbroadcastcmd(self, message: Message):
        self.broadcast_enabled = True
        await self.client.send_message(message.peer_id, self.strings("broadcast_on"))
        interval = 3605
        last_sent_time = 0
        while self.broadcast_enabled:
            current_time = time.time()
            if current_time - last_sent_time >= interval:
                await self.send_message()
            last_sent_time = current_time  # Обновляем время после каждой попытки отправки
            await asyncio.sleep(max(0, interval - (time.time() - last_sent_time)))

    @loader.command(ru_doc="Остановить рассылку сообщений")
    async def stopbroadcastcmd(self, message: Message):
        self.broadcast_enabled = False
        await self.client.send_message(message.peer_id, self.strings("broadcast_off"))
