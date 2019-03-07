import asyncio
import json
import logging
import logging
import os
import re
import sqlite3

import __main__
import discord
from discord.ext import commands

from newblue.EventRunner import EventRunner
from newblue.lib.mudae.mudae_manager import MudaeManager


class BlueBot(commands.Bot):

    def __init__(self, command_prefix=None):
        logging.basicConfig(filename='GoldLog.log', level=logging.INFO)
        self.mudae_manager = MudaeManager(self, sqlite3.connect('mudae.db'))
        self.event_runner = EventRunner.EventRunner(self)
        self.dir = os.path.dirname(__file__)
        self.load_config()
        super().__init__(command_prefix=command_prefix)

        self.on_message_commands = []

    async def on_ready(self):
        print("ready")
        self.load_base_commands()
        # asyncio.ensure_future(self.process_old_messages())
        for com in self.commands:
            print(com)

    async def on_message(self, message):
        self.mudae_manager.determine_message_type(message)
        if self.check_gigguk_content(message.content) and not message.author.bot:
            print('true')
            await message.channel.send("Fuck off with your gigguk")
        await self.process_commands(message)

    def load_config(self):
        print('/'.join(os.path.abspath(__main__.__file__).split(r'/')[:-1]))
        with open(f"{self.dir}\\config.json", "r") as file:
            self.cfg = json.loads(file.read())

    def load_base_commands(self):
        # Load each cog from ./Commands/BaseCommands
        for cog_file in [file[:-3] for file in
                         os.listdir(f'{self.dir}\\newblue\\Commands\\BaseCommands'.replace("\\", "/")) if
                         file not in ['__init__.py', '__pycache__']]:
            self.load_extension(f"newblue.Commands.BaseCommands.{cog_file}")
            logging.info("successfully loaded extension {}".format(cog_file))
