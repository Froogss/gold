import sys

import discord
from discord.ext import commands


class CommandErrorHandler:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command,'on_error'):
            return

        ignored = (commands.CommandNotFound, commands.UserInputError)
        error = getattr(error, 'original', error)
        print(error)
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.NotOwner):
            await ctx.channel.send("`Error: You are not an owner`")


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
