import logging
from typing import Awaitable, Callable

from discord import TextChannel, Thread, User, VoiceChannel
from discord.ext import commands

from lib import RatCog, RatContext, RatBot, split_string


@commands.is_owner()
class Admin(RatCog):
    """Administrative commands. Only for bot owners"""

    @commands.hybrid_command()  # type: ignore[arg-type]
    async def sync_tree(self, ctx: RatContext):
        """Syncs internally registered commands with Discord"""
        await self.bot.tree.sync()
        logging.info("Synced tree!")
        await ctx.send("synced!", ephemeral=True)

    @commands.hybrid_command()  # type: ignore[arg-type]
    async def echo(
        self,
        ctx: RatContext,
        channel: TextChannel | Thread | VoiceChannel | None = None,
        victim: User | None = None,
        *,
        message: str,
    ):
        """Echos a message into a channel"""
        target = victim or channel or ctx.channel
        await target.send(message)

        if ctx.interaction:
            await ctx.reply("sent!", ephemeral=True)

    @commands.hybrid_group()  # type: ignore[arg-type]
    async def exts(self, ctx: RatContext) -> None:
        raise NotImplementedError

    @exts.command(name="list")  # type: ignore[arg-type]
    async def _list(self, ctx: RatContext) -> None:
        """List currently enabled extensions."""
        await ctx.send("current enabled extensions: `" + self.conf.list_exts())

    async def _exts_subcommand(
        self,
        ctx: RatContext,
        extensions: str,
        *,
        name: str,
        func: Callable[[RatBot, str], Awaitable[None]],
    ) -> None:
        resp = ["```diff"]

        extensions: list[str] = split_string(extensions)
        if not extensions:
            raise SyntaxError("missing argument: extensions")

        total_errors = 0

        for ext in extensions:
            try:
                await func(self.bot, ext)
                resp.append(f"+ {ext}")
            except:
                logging.exception(
                    f"an exception occurred while {name}ing extension: {ext}"
                )
                resp.append(f"- {ext}")
                total_errors += 1

        resp.append("```")

        if total_errors != 0:
            resp.append(
                f"{total_errors} module{'' if total_errors == 1 else 's'} failed to {name}."
                "please check console logs for more information."
            )
        else:
            resp.append(
                f"Successfully reloaded module{'' if total_errors == 1 else 's'}!"
            )

        await ctx.send("\n".join(resp))

    @exts.command()  # type: ignore[arg-type]
    async def reload(self, ctx: RatContext, extensions: str) -> None:
        """Reload given extensions."""
        await self._exts_subcommand(
            ctx, extensions, name="reload", func=RatBot.reload_extension
        )

    @exts.command()  # type: ignore[arg-type]
    async def load(self, ctx: RatContext, extensions: str) -> None:
        """Load given extensions."""
        await self._exts_subcommand(
            ctx, extensions, name="load", func=RatBot.load_extension
        )

    @exts.command()  # type: ignore[arg-type]
    async def unload(self, ctx: RatContext, extensions: str) -> None:
        """Load given extensions."""
        await self._exts_subcommand(
            ctx, extensions, name="unload", func=RatBot.unload_extension
        )


setup = Admin.basic_setup
