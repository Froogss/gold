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
        name = split[0]
        event_message = split[1]
        mentions = split[2:]
        bot.event_runner.events.append(Event(ctx, name, event_message, mentions))

    @commands.command()
    async def list_events(self, ctx):
        bot.say(", ".join([f"{event.name}: {event.event_call_time}" for event in bot.event_runner.events]))


def setup(bot):
    bot.add_cog(Cog(bot))
