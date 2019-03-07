from discord.ext import commands


class Cog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reload_extensions(self):
        for name in self.extenions:
            self.unload_extension(name)
            try:
                self.bot.load_extension(name)

            except ImportError as e:
                await self.bot.say("Failed to reload extension {}")

def setup(bot):
    bot.add_cog(Cog(bot))
