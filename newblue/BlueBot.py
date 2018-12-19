from discord.ext import commands
import logging
import os
import __main__
import json

from EventRunner import EventRunner


class BlueBot(commands.Bot):

    def __init__(self, command_prefix=None):
        self.load_config()
        super().__init__(command_prefix=command_prefix)
        self.event_runner = EventRunner(self)
        


    async def on_ready(self):
        print("ready")
        for com in self.commands:
            print(com.cog_name)

    def load_config(self):
        print('/'.join(os.path.abspath(__main__.__file__).split(r'/')[:-1]))
        with open('/'.join(os.path.abspath(__main__.__file__).split(r'/')[:-1]) + "/config.json", "r") as file:
            self.cfg = json.loads(file.read())

    def load_starting_commands():
        for cog in self.cfg["starting_commands"]:
            try:
                self.load_extension(cog)
                logging.info("successfully loaded extension {}".format(cog))

            except ImportError as e:
                logging.error("Failed to load extension {}".format(cog))
