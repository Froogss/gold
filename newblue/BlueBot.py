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
        self.load_starting_commands()
        for com in self.commands:
            print(com)

    async def on_message(self, message):
        await self.process_commands(message)
        if str(message.author.id) in ["143092974316683264", "4326102922342587392", "522749851922989068"]:
            split_message = message.content.split(" ")
            if False:
                match = re.search(r'. (.*) and (.*) are now married! .', message.content)
                user_id = str(message.author.id)
                character_name =  match.group(2)

                self.cursor.execute("""INSERT INTO waifuClaims values (?, ?, ?)""", [user_id, character_name, message.created_at])
                self.conn.commit()
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
