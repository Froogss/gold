import time
import datetime
import asyncio

class EventRunner:
    def __init__(self, bot, poll_period=1):
        self.bot = bot
        self.poll_period = poll_period
        self.fired_events = []
        self.events = []
        asyncio.ensure_future(self.runner())

    async def runner(self):
        while True:
            next_poll = datetime.datetime.now() + datetime.timedelta(minutes=self.poll_period)
            for i in events:
                if i.fired == False and i.event_call_time <= next_poll:
                    fired_events.append( [ (next_poll-i.event_call_time).total_seconds(), i] )
                    i.fired = True

            await asyncio.sleep(poll_period*60)

    async def run_delayed(self, delay, event):
        await asyncio.sleep(delay)
        await event.call()
