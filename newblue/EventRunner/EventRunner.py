import time
import datetime
import asyncio

class EventRunner:
    def __init__(self, bot, poll_period=1):
        self.bot = bot
        self.poll_period = poll_period
        self.fired_events = []
        self.events = []
        self.a = asyncio.ensure_future(self.runner())

    async def runner(self):
        await self.bot.wait_until_ready()
        while True:
            print("polling")
            next_poll = datetime.datetime.now() + datetime.timedelta(minutes=self.poll_period)
            for i in self.events:
                #if the event would be called between this poll and next
                if i.fired == False and i.event_call_time <= next_poll:
                    time_until_event_time = (i.event_call_time - datetime.datetime.now()).total_seconds

                    asyncio.ensure_future(self.run_delayed(time_until_event_time, i))
                    i.fired = True
            print("sleeping")
            await asyncio.sleep(int(self.poll_period * 30))
            print("unsleeping")
            

    async def run_delayed(self, delay, event):
        print(f"Running delayed event {event.name}")
        await asyncio.sleep(5)
        print("calling event")
        await event.call()
        if event.repeating:
            event.fired = False

        else:
            self.events.remove(event)
