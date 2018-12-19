from discord.ext import commands
from Event import Event

class Cog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def load_extension(self, ctx, name):
        try:
            self.bot.load_extension(name)

        except ImportError as e:
            await self.bot.say("Extension {} could not be loaded")
    
    @commands.command()
    async def create_event(self, ctx, *message):
        split = [item.strip(" ") for item in message]
        bot.event_runner.events.append(Event(ctx, split[0], split[1], split[2:]))


def setup(bot):
    bot.add_cog(Cog(bot))
