import discord
import sqlite3
import re
from discord.ext import commands
import logging
import os
import __main__
import json

from .EventRunner import EventRunner


class BlueBot(commands.Bot):

    def __init__(self, command_prefix=None):
        print(discord.__version__)
        self.load_config()
        super().__init__(command_prefix=command_prefix)
        self.event_runner = EventRunner.EventRunner(self)
        self.conn = sqlite3.connect("test.db")
        self.cursor = self.conn.cursor()


    async def on_ready(self):
        print("ready")
        self.load_base_commands()
        for com in self.commands:
            print(com)

    async def on_message(self, message):
        await self.process_commands(message)
        if str(message.author.id) in ["4326102922342587392", "522749851922989068"]:
            res = re.search(r". .* and (.*) are now married! .")
            if res:
                self.bot.cursor.execute("""INSERT INTO waifuClaims values                                                   (?, ?, ?) """,
                                            str(ctx.message.author.id), res.group(1), ctx.message.created_at)
                self.bot.cursor.commit()

    def load_config(self):
        print('/'.join(os.path.abspath(__main__.__file__).split(r'/')[:-1]))
        with open('/'.join(os.path.abspath(__main__.__file__).split(r'/')[:-1]) + "/config.json", "r") as file:
            self.cfg = json.loads(file.read())

    def load_starting_commands(self):
        # Load each cog from ./Commands/BaseCommands
        for cog_file in [[file[:-3] for file in os.listdir('./Commands/BaseCommands') if file != '__init__.py']]:
            self.load_extension(f"{cog}")
            logging.info("successfully loaded extension {}".format(cog))
