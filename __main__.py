import logging
from os import getenv

from dotenv import load_dotenv

from lib import RatBot, RatConfigs

from discord.utils import setup_logging

load_dotenv()
token = getenv("RATBOT_TOKEN")

if not token:
    raise RuntimeError("RATBOT_TOKEN environment variable not set!")

setup_logging(level=logging.DEBUG)

conf = RatConfigs.load_or_defaults()
bot = RatBot(conf)
bot.run(token)
