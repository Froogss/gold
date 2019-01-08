from discord.ext import commands

class Cog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def md(self, ctx, id=None):
        if id is None:
            id = ctx.message.author.id

        self.bot.cursor.execute("""select * from waifuClaims where user_id = ? order by date""", [id])
        
        stats = [f"{item[1]}: {str(item[2])[:-7]}\n" for item in self.bot.cursor.fetchall()]
        cur_len = 0
        temp = []
        for stat in stats:
            if (cur_len + len(stat)) > 2000:
                await ctx.channel.send("".join(temp))
                temp = [stat]
                await asyncio.sleep(1)

            else:
                temp.append(stat)

        await ctx.channel.send("".join(temp))

def setup(bot):
    bot.add_cog(Cog(bot))