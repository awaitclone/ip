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
        "error": "<b>Ошибка при отправке сообщения:</b> {}"
    }

    async def client_ready(self, client, db):
        self.client = client

    async def send_message(self):
        try:
            image_url = 'https://i.imgur.com/iOYNbtV.png'  # URL изображения
            message_text = (
                "Тут текст\n\n"
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
            await self.client.send_message('kgfdgkdfgk324', self.strings("success"))
        except Exception as e:
            await self.client.send_message('kgfdgkdfgk324', self.strings("error").format(str(e)))

    @loader.command(ru_doc="Запустить рассылку сообщений")
    async def mybroadcastcmd(self, message: Message):
        """Run the broadcaster"""
        interval = 3605  # Интервал в секундах между сообщениями
        last_sent_time = 0
        while True:
            try:
                current_time = time.time()
                if current_time - last_sent_time >= interval:
                    await self.send_message()
                await asyncio.sleep(max(0, interval - (current_time - last_sent_time)))
            except Exception as e:
                await self.client.send_message('kgfdgkdfgk324', self.strings("error").format(str(e)))
                last_sent_time = time.time()
                await asyncio.sleep(max(0, interval - (current_time - last_sent_time)))
