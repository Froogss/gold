from discord.ext import commands
import logging
import os
import __main__
import json

from .EventRunner import EventRunner


class BlueBot(commands.Bot):

    def __init__(self, command_prefix=None):
        self.load_config()
        super().__init__(command_prefix=command_prefix)
        self.event_runner = EventRunner.EventRunner(self)
        


    async def on_ready(self):
        print("ready")
        self.load_starting_commands()
        for com in self.commands:
            print(com)

    def load_config(self):
        print('/'.join(os.path.abspath(__main__.__file__).split(r'/')[:-1]))
        with open('/'.join(os.path.abspath(__main__.__file__).split(r'/')[:-1]) + "/config.json", "r") as file:
            self.cfg = json.loads(file.read())

    def load_starting_commands(self):
        for cog in self.cfg["starting_commands"]:
            print(cog)
            self.load_extension(f"{cog}")
            print(f"loaded {cog}")
            logging.info("successfully loaded extension {}".format(cog))
