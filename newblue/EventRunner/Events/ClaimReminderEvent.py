import json
import datetime
from .. import Reminder


class ClaimReminder(Reminder):
    def __init__(self):
        super().__init__("Claim Reminder", True, 60)
        with open('opts.json') as file:
            data = json.loads(file)[self.name]['claim_start']
            self.claim_Start = datetime.time(hour=data[:2])
        cur_time = datetime.datetime.now()

        if cur_time.minute < self.call_time.minute -1:
            hour = str(cur_time.hour).zfill(2)
            minute = str(self.claim_start.minute).zfill(2)
            self.call_time = datetime.time.fromisoformat(f"{hour}:{minute}:00")

        else:
            hour = str(cur_time.hour+1).zfill(2)
            minute = str(self.claim_start.minute).zfill(2)
            self.call_time = datetime.time.fromisoformat(f"{hour}:{minute}:00")


    def call(self, bot):
        cur_time = datetime.datetime.now()
        #due to the event scheduler, this event will always be called at the right time
        #if the current hour can't be divided by 3
        remainder = cur_time.hour if cur_time.hour in [0,1,2] else cur_time.hour%3
        
        if remainder == 0:
            #the hour is a multiple of 3 and the claim will reset
            await (bot.get_channel(self.channel_id).send(f"Full claim/roll reset in 2 minutes! <@&{self.role_ids['roll']}> <@&{self.role_ids['claim']}>"))
        else:
            await (bot.get_channel(self.channel_id).send(f"Roll reset in 2 minutes! <@&{self.role_ids['roll']}>"))
        self.call_time = self.call_time + dateime.timedelta(hours=1)

            