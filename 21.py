
import logging

import requests
from telethon.tl.types import Message, MessageEntityUrl

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class AutoShortenerMod(loader.Module):
    """Automatically shortens urls in your messages, which are larger than specified threshold"""

    strings = {
        "name": "AutoShortener",
        "state": "🔗 <b>Auotmatic url shortener is now {}</b>",
        "no_args": "🔗 <b>No link to shorten</b>",
        "on": "on",
        "off": "off",
    }

    strings_ru = {
        "state": "🔗 <b>Автоматический сократитель ссылок теперь {}</b>",
        "no_args": "🔗 <b>Не указана ссылка для сокращения</b>",
        "_cmd_doc_autosurl": "Включить\\выключить автоматическое сокращение ссылок",
        "_cmd_doc_surl": "[ссылка] [движок]- Сократить ссылку",
        "_cls_doc": (
            "Автоматически сокращает ссылки в твоих сообщениях, если они длиннее"
            " значения в конфиге"
        ),
        "on": "включен",
        "off": "выключен",
    }

    strings_de = {
        "state": "🔗 <b>Automatisches URL-Kürzen ist jetzt {}</b>",
        "no_args": "🔗 <b>Kein Link zum Kürzen</b>",
        "_cmd_doc_autosurl": (
            "Aktivieren\\Deaktivieren Sie das automatische Kürzen von URLs"
        ),
        "_cmd_doc_surl": "[URL] [Engine] - URL kürzen",
        "_cls_doc": (
            "Kürzt automatisch URLs in Ihren Nachrichten, wenn sie länger sind als"
            " Wert in der Konfiguration"
        ),
        "on": "Aktiviert",
        "off": "Deaktiviert",
    }

    strings_tr = {
        "state": "🔗 <b>Otomatik URL kısaltıcı şimdi {}</b>",
        "no_args": "🔗 <b>Kısaltılacak URL yok</b>",
        "_cmd_doc_autosurl": (
            "URL'leri otomatik olarak kısaltmayı etkinleştirin\\devre dışı bırakın"
        ),
        "_cmd_doc_surl": "[URL] [motor] - URL kısalt",
        "_cls_doc": (
            "URL'leri, yapılandırmanın değerinden daha uzun olduğunda mesajlarınızda"
            " otomatik olarak kısaltır"
        ),
        "on": "açık",
        "off": "kapalı",
    }

    strings_hi = {
        "state": "🔗 <b>ऑटो यूआरएल शॉर्टनर अब {} है</b>",
        "no_args": "🔗 <b>संक्षिप्त करने के लिए कोई लिंक नहीं</b>",
        "_cmd_doc_autosurl": "URL को स्वचालित रूप से छोटा करना चालू\\बंद करें",
        "_cmd_doc_surl": "[URL] [Engine] - URL को छोटा करें",
        "_cls_doc": (
            "अपने संदेशों में यूआरएल को छोटा करता है, जब वे विन्यास में निर्दिष्ट मान से अधिक होते हैं"
        ),
        "on": "चालू",
        "off": "बंद",
    }

    strings_uz = {
        "state": "🔗 <b>URL avtomatik qisqartiruvchisi hozir {}</b>",
        "no_args": "🔗 <b>Qisqartiladigan URL yo'q</b>",
        "_cmd_doc_autosurl": "URL'ni avtomatik ravishda qisqartishni yoqish\\o'chirish",
        "_cmd_doc_surl": "[URL] [mashina] - URL'ni qisqartirish",
        "_cls_doc": (
            "So'rovlarizdagi URL'ni konfiguratsiyadagi qiymatdan katta bo'lganda"
            " avtomatik ravishda qisqartadi"
        ),
        "on": "yoqilgan",
        "off": "o'chirilgan",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "threshold",
                80,
                lambda: "Urls larger than this value will be automatically shortened",
                validator=loader.validators.Integer(minimum=50),
            ),
            loader.ConfigValue(
                "auto_engine",
                "owo",
                lambda: "Engine to auto-shorten urls with",
                validator=loader.validators.Choice(["owo", "gg", "gay"]),
            ),
        )

    async def autosurlcmd(self, message: Message):
        """Toggle automatic url shortener"""
        state = not self.get("state", False)
        self.set("state", state)
        await utils.answer(
            message, self.strings("state").format("on" if state else "off")
        )

    async def surlcmd(self, message: Message):
        """[url] [engine]- Shorten url"""
        if (
            not getattr(message, "raw_text", False)
            or not getattr(message, "entities", False)
            or not message.entities
            or not any(
                isinstance(entity, MessageEntityUrl) for entity in message.entities
            )
        ):
            reply = await message.get_reply_message()
            if (
                not reply
                or not getattr(reply, "raw_text", False)
                or not getattr(reply, "entities", False)
                or not reply.entities
                or not any(
                    isinstance(entity, MessageEntityUrl) for entity in reply.entities
                )
            ):
                await utils.answer(message, self.strings("no_args"))
                return

            txt = reply.raw_text
            text = reply.text
            entities = reply.entities
            just_url = False
        else:
            txt = message.raw_text
            text = message.text
            entities = message.entities
            just_url = True

        urls = [
            txt[entity.offset : entity.offset + entity.length] for entity in entities
        ]

        if just_url:
            text = ""

        for url in urls:
            surl = await self.shorten(
                url, txt.split()[-1] if len(txt.split()) > 1 else None
            )
            if not just_url:
                text = text.replace(url, surl)
            else:
                text += f"{surl} | "

        await utils.answer(message, text.strip(" | "))

    @staticmethod
    async def shorten(url, engine=None) -> str:
        if not engine or engine == "gg":
            r = await utils.run_sync(
                requests.post,
                "https://bot1.org/api",  # Changed API endpoint
                json={"url": url},  # Send the URL as JSON
                headers={"Content-Type": "application/json"},
            )
 
            response_data = r.json()
            return response_data.get("bot", url)  # Return the shortened URL or the original if something goes wrongelif engine in ["owo", "gay"]:
            r = await utils.run_sync(
                requests.post,
                "https://owo.vc/generate",
                json={
                    "link": url,
                    "generator": engine,
                    "preventScrape": True,
                    "owoify": True,
                },
                headers={"User-Agent": "https://mods.hikariatama.ru/view/surl.py"},
            )

            logger.debug(r.json())

            return"https://" + r.json()["result"]


    async def watcher(self, message: Message):
        if (
            not getattr(message, "text", False)
            or not getattr(message, "out", False)
            or not getattr(message, "entities", False)
            or not message.entities
            or not any(
                isinstance(entity, MessageEntityUrl) for entity in message.entities
            )
            or not self.get("state", False)
            or message.raw_text.lower().startswith(self.get_prefix())
        ):
            return

        entities = message.entities
        urls = list(
            filter(
                lambda x: len(x) > int(self.config["threshold"]),
                [
                    message.raw_text[entity.offset : entity.offset + entity.length]
                    for entity in entities
                ],
            )
        )

        if not urls:
            return

        text = message.text

        for url in urls:
            text = text.replace(
                url, await self.shorten(url, self.config["auto_engine"])
            )

        await message.edit(text)