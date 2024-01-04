from .. import loader, utils
from telethon.tl.types import Message
import asyncio
import time

@loader.tds
class MyBroadcasterMod(loader.Module):
    """Custom message broadcaster"""
    strings = {
        "name": "MyBroadcaster",
        "success": "<b>Сообщение отправлено успешно!</b>",
        "error": "<b>Ошибка при отправке сообщения:</b> {}",
        "broadcast_on": "<b>Рассылка включена.</b>",
        "broadcast_off": "<b>Рассылка выключена.</b>"
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
                "ЗАЕБАЛСЯ ИСКАТЬ НЕ ДОРОГОЙ НО КАЧЕСТВЕННЫЙ ДИЗАЙН ❓\n\n"
                "Рады вам представить — MORIA DESIGN, лучший дизайн за лучшие цены во всем рынке,\n"
                "средний чек — 250-500₽\n\n"
                "Делаем:\n"
                "⚙️- Аватарки\n"
                "👍- Рекламные баннеры\n"  
                "👌- Оформление тем\n"
                "🌐- Анимированные работы\n\n"
                "Портфолио: @moriadesign\n"
                "(https://t.me/+wn_45A9wkbViMmFi)Связь: @imfckngmoriarty\n"
                "Гарант: @zelenka_guarantor_robot"
            )
            await self.client.send_file('zelenka_services', image_url, caption=message_text)
            await self.client.send_message('gdfgdfgdf235453', self.strings("success"))
            return True
        except Exception as e:
            await self.client.send_message('gdfgdfgdf235453', self.strings("error").format(str(e)))
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
                if await self.send_message():
                    last_sent_time = current_time
            await asyncio.sleep(max(0, interval - (time.time() - last_sent_time)))

    @loader.command(ru_doc="Остановить рассылку сообщений")
    async def stopbroadcastcmd(self, message: Message):
        self.broadcast_enabled = False
        await self.client.send_message(message.peer_id, self.strings("broadcast_off"))
