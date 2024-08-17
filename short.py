import requests
from .. import loader, utils

@loader.tds
class URLShortenerMod(loader.Module):
    """A simple URL shortener using bot1"""

    strings = {
        "name": "URLShortener",
        "no_args": "🔗 <b>Please provide a URL to shorten</b>",
        "shortened": "🔗 <b>Shortened URL:</b> <code>{}</code>",
        "error": "🚫 <b>Error shortening URL:</b> <code>{}</code>",
    }

    async def surlcmd(self, message):
        """[url] - Shorten a URL using bot1"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_args"])
            return

        shortened_url = await self.shorten(args.strip())
        if shortened_url.startswith("http"):
            await utils.answer(message, self.strings["shortened"].format(shortened_url))
        else:
            await utils.answer(message, self.strings["error"].format(shortened_url))

    @staticmethod
    async def shorten(url) -> str:
        try:
            r = requests.post(
                "https://bot1.org/api",  # Replace with the correct API endpoint
                json={"url": url},
                headers={"Content-Type": "application/json"},
            )
            response_data = r.json()
            return response_data.get("url", "Failed to shorten URL")
        except Exception as e:
            return str(e)
