from discord.ext import commands


class Cog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def get_old_claims(self, ctx):
        after = datetime.datetime.now() - datetime.timedelta(weeks=24)
        for channel in ctx.message.guild.channels:
            if type(channel) != discord.TextChannel:
                continue
            print("getting claims")
            async for message in channel.history(limit=None, after=after):
                res = re.search(r". (.*) and (.*) are now married! .", message.content)
                if res:
                    #see if the user still has the same username
                    print(res.group(1).strip('*'))
                    users = [user.id for user in ctx.message.guild.members if user.name == res.group(1).strip('*')]
                    if len(users) == 1:
                        self.bot.cursor.execute("""INSERT INTO waifuClaims values (?, ?, ?)""", [users[0], res.group(2), message.created_at])
            self.bot.conn.commit()

def setup(bot):
    bot.add_cog(Cog(bot))