import logging
import requests
from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class URLShortenerMod(loader.Module):
    """Shortens URLs using bot1 with the .surl command"""

    strings = {
        "name": "URLShortener",
        "no_args": "🔗 <b>Please provide a URL to shorten</b>",
        "shortened": "🔗 <b>Shortened URL:</b> <code>{}</code>",
        "error": "🚫 <b>Error shortening URL:</b> <code>{}</code>",
    }

    async def surlcmd(self, message):
        """Shorten a URL using bot1"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_args"])
            return

        try:
            logger.info(f"Attempting to shorten URL: {args.strip()}")
            r = requests.post(
                "https://bot1.org/api",  # bot1 API endpoint
                json={"url": args.strip()},
                headers={"Content-Type": "application/json"},
            )
            response_data = r.json()
            shortened_url = response_data.get("url", "Error")
            logger.info(f"Shortened URL: {shortened_url}")
            await utils.answer(message, self.strings["shortened"].format(shortened_url))
        except Exception as e:
            logger.error(f"Error shortening URL: {str(e)}")
            await utils.answer(message, self.strings["error"].format(str(e)))
