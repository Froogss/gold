from discord.ext import commands
from newblue.EventRunner.Event import Event
import inspect
import discord
import re
import datetime

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
        mentions = split[3].split(" ")
        self.bot.event_runner.events.append(Event(ctx, name, event_message, minutes,  mentions))

    @commands.command(pass_context=True)
    async def list_events(self, ctx):
        await ctx.channel.send(", ".join([f"{event.name}: {event.event_call_time}" for event in self.bot.event_runner.events]))

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def test(self, ctx):
        await ctx.channel.send("yep")

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
    @commands.command(pass_context=True)
    @commands.is_owner()
    async def get_old_claims(self, ctx):
        after = datetime.datetime.now() - datetime.timedelta(weeks=24)
        for channel in ctx.message.guild.channels:
            if type(channel) != discord.TextChannel:
                continue
            print("getting claims")
            async for message in channel.history(limit=None, after=after):
                #print(message.content)
                res = re.search(r". (.*) and (.*) are now married! .", message.content)
                if res:
                    print(res.group(2))
                    self.bot.cursor.execute("""INSERT INTO waifuClaims values (?, ?, ?)""", [message.author.id, res.group(2), message.created_at])
            self.bot.conn.commit()

    @commands.command(pass_context=True)
    async def md(self, ctx, id=None):
        if id is None:
            id = ctx.message.author.id

        self.bot.cursor.execute("""select * from waifuClaims where user_id = ?""", [id])
        await ctx.channel.send(self.bot.cursor.fetchall())

def setup(bot):
    bot.add_cog(Cog(bot))
