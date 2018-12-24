import datetime
class Event:
    def __init__(self, ctx, name, message, minutes, mentions):
        self.event_call_time = datetime.datetime.now()+datetime.timedelta(minutes=minutes)
        self.name = name
        self.message = message
        self.channel = ctx.message.channel
        self.mentions = mentions
        repeat = []
        self.fired = False

    async def call(self):
        mentions = ["<@!{}>".format(mention) for mention in self.mentions]
        message = "{} {}".format(self.message, " ".join(mentions))
        await self.channel.send(message)
