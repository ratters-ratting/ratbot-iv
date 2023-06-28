from discord import Intents, TextChannel
from discord.ext import commands
from discord.message import Message

from .models import JsonModel, conf_dir

RAT = "rat"


class RatConfigs(JsonModel):
    path = conf_dir / "main.json"
    default_prefix: str = "r."
    description: str = "Rat Bot. Welcome to Rat Bot."


class RatBot(commands.Bot):
    conf: RatConfigs

    def __init__(self, conf: RatConfigs) -> None:
        super().__init__(
            command_prefix=conf.default_prefix,
            intents=Intents.all(),
            description=conf.description,
        )
        self.conf = conf

    async def on_message(self, message: Message) -> None:
        """handles 'rat' replying and the contexts in which commands can be invoked"""

        # rat channels
        if isinstance(message.channel, TextChannel) and message.channel.name == RAT:
            if message.content == RAT:
                await message.channel.send(RAT)
            else:
                await message.delete()
            return

        # do not reply to bots
        if message.author.bot:
            return

        if message.content.lower().startswith(RAT):
            await message.channel.send(RAT)

        await self.process_commands(message)
