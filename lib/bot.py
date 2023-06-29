import logging
from typing import Any, Coroutine
from discord import Intents, TextChannel
from discord.ext import commands
from discord.message import Message
from pydantic import Field

from .utils import generate_extensions_list

from .models import JsonModel, conf_dir

RAT = "rat"


class RatConfigs(JsonModel):
    path = conf_dir / "main.json"

    default_prefix: str = "r."
    """command prefix"""
    description: str = "Rat Bot. Welcome to Rat Bot."
    enabled_extensions: set[str] = Field(
        default_factory=lambda: set(generate_extensions_list())
    )
    debug: bool = False

    def list_exts(self) -> str:
        return "`" + "`, `".join(self.enabled_extensions) + "`"


class RatBot(commands.Bot):
    conf: RatConfigs

    def __init__(self, conf: RatConfigs) -> None:
        super().__init__(
            command_prefix=conf.default_prefix,
            intents=Intents.all(),
            description=conf.description,
        )
        self.conf = conf

    async def setup_hook(self) -> None:
        logging.info("Loading enabled extensions...")
        for ext in self.conf.enabled_extensions:
            try:
                await self.load_extension(ext)
            except Exception as exc:
                logging.exception(f"An error occurred while loading extension: {ext}")
            else:
                logging.info(f"Loaded extension: {ext}")
        logging.info("Done loading extensions!")

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


class RatCog(commands.Cog):
    bot: RatBot
    conf: RatConfigs

    @classmethod
    async def basic_setup(cls, bot: RatBot):
        await bot.add_cog(cls(bot))

    def setup_hook(self) -> Coroutine[Any, Any, None]:
        """Override this method to do more setup on ready. Unlike
        creating an on_ready event, this method is only called once."""
        raise NotImplementedError

    def __init__(self, bot: RatBot):
        self.bot = bot
        self.conf = bot.conf

        if type(self).setup_hook is not RatCog.setup_hook:

            async def f():
                await self.bot.wait_until_ready()
                await self.setup_hook()

            bot.loop.create_task(f())


RatContext = commands.Context[RatBot]
