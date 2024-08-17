import logging
import requests
from telethon.tl.types import Message, MessageEntityUrl
from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.Module
class AutoShortenerMod(loader.Module):
    """Automatically shortens URLs in your messages, which are larger than the specified threshold"""

    strings = {
        "name": "AutoShortener",
        "state": "🔗 <b>Automatic URL shortener is now {}</b>",
        "no_args": "🔗 <b>No link to shorten</b>",
        "on": "on",
        "off": "off",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "threshold",
                80,
                lambda: "URLs larger than this value will be automatically shortened",
                validator=loader.validators.Integer(minimum=50),
            ),
            loader.ConfigValue(
                "auto_engine",
                "bot1",  # Default engine for shortening URLs
                lambda: "Engine to auto-shorten URLs with",
                validator=loader.validators.Choice(["bot1"]),
            ),
        )

    async def autosurlcmd(self, message: Message):
        """Toggle automatic URL shortener"""
        state = not self.get("state", False)
        self.set("state", state)
        await utils.answer(
            message, self.strings("state").format("on" if state else "off")
        )

    async def surlcmd(self, message: Message):
        """[url] - Shorten URL"""
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
            surl = await self.shorten(url)
            if not just_url:
                text = text.replace(url, surl)
            else:
                text += f"{surl} | "
        await utils.answer(message, text.strip(" | "))

    @staticmethod
    async def shorten(url) -> str:
        r = await utils.run_sync(
            requests.post,
            "https://bot1.org/api",  # Use your API endpoint
            json={"url": url},  # Send the URL as JSON
            headers={"Content-Type": "application/json"},
        )

        response_data = r.json()
        return response_data.get("url", url)  # Return the shortened URL or the original if something goes wrong

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
                url, await self.shorten(url)
            )

        await message.edit(text)
