from os import getenv

from dotenv import load_dotenv

from lib import RatBot, RatConfigs

load_dotenv()
token = getenv("RATBOT_TOKEN")

if not token:
    raise RuntimeError("RATBOT_TOKEN environment variable not set!")

conf = RatConfigs.load_or_defaults()
bot = RatBot(conf)
bot.run(token)
