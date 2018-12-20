from discord.ext import commands
from newblue.EventRunner.Event import Event

class Cog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def load_extension(self, ctx, name):
        try:
            self.bot.load_extension(name)

        except ImportError as e:
            await self.bot.say("Extension {} could not be loaded")
    
    @commands.command(pass_context=True)
    async def create_event(self, ctx, *message):
        message = " ".join(message)
        split = [item for item in message.split(",")]
        print(split)
        name = split[0]
        event_message = split[1]
        minutes = int(split[2])
        mentions = split[3:]
        self.bot.event_runner.events.append(Event(ctx, name, event_message, minutes,  mentions))

    @commands.command(pass_context=True)
    async def list_events(self, ctx):
        await self.bot.send_message(ctx.message.channel, ", ".join([f"{event.name}: {event.event_call_time}" for event in self.bot.event_runner.events]))


def setup(bot):
    bot.add_cog(Cog(bot))
