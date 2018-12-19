import time
import datetime

class EventRunner:
    def __init__(self, bot, poll_period=10):
        self.bot = bot
        self.poll_period = poll_period
        self.fired_events = []
        self. events = []

    async def runner():
        while True:
            next_poll = datetime.datetime.now() + datetime.timedelta(minutes=self.poll_period)
            for i in events:
                if i.fired == False and i.event_call_time <= next_poll:
                    fired_events.append( [ (next_poll-i.event_call_time).total_seconds(), i] )
                    i.fired = True

    async def run_delayed(self, delay, event):
        await asyncio.sleep(delay)
        await event.call()