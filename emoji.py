from .. import loader, utils
from telethon.tl.types import Message

@loader.tds
class EmojiCommandMod(loader.Module):
    """Sends a specific emoji on command"""
    strings = {
        "name": "EmojiCommand",
        "emoji_sent": "<b>Emoji sent successfully!</b>",
        "emoji_error": "<b>Error sending emoji:</b> {}",
    }

    @loader.command(ru_doc="Отправить заданный emoji")
    async def emojicmd(self, message: Message):
        try:
            emoji = "<emoji document_id=5456130795603244190>🍪</emoji>"
            await message.respond(emoji, parse_mode='html')
            await message.respond(self.strings("emoji_sent"))
        except Exception as e:
            await message.respond(self.strings("emoji_error").format(str(e)))

    async def client_ready(self, client, db):
        self.client = client
