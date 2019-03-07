from discord.ext import commands

class Cog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def eval(self, ctx, *args):
        message = " ".join(args)
        print(message)
        res = eval(message)
        if inspect.isawaitable(res):
            await ctx.channel.send(await res)

        else:
            await ctx.channel.send(res)

def setup(bot):
    bot.add_cog(Cog(bot))