from discord.ext import commands

class Cog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def load_extension(self, ctx, name):
        try:
            self.bot.load_extension(name)

        except ImportError as e:
            await self.bot.say("Extension {} could not be loaded")

def setup(bot):
    bot.add_cog(Cog(bot))
