
class Event:
    def __init__(self, ctx, name, message, *mentions):
        self.name = name
        self.channel = ctx.channel
        self.mentions = mentions
        repeat = []

    async def call(self, bot):
        message = "{} {}".format(message, " ".join(["<@!{}>".format(mention) for mention in mentions]))
        await bot.send_message(self.channel, message)