import datetime
class Event:
    def __init__(self, ctx, name, message, minutes, *mentions):
        self.event_call_time = datetime.datetime.now()+datetime.timedelta(minutes=minutes)
        self.name = name
        self.channel = ctx.channel
        self.mentions = mentions
        repeat = []

    async def call(self, bot):
        message = "{} {}".format(message, " ".join(["<@!{}>".format(mention) for mention in mentions]))
        await bot.send_message(self.channel, message)