from discord.ext import commands

class Cog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def create_event(self, ctx, *message):
        message = " ".join(message)
        split = [item for item in message.split(",")]
        print(split)
        name = split[0]
        event_message = split[1]
        minutes = int(split[2])
        mentions = split[3].split(" ")
        self.bot.event_runner.events.append(Event(ctx, name, event_message, minutes,  mentions))


def setup(bot):
    bot.add_cog(Cog(bot))
