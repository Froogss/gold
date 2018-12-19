import logging
from newblue.BlueBot import BlueBot


bot = BlueBot(command_prefix="[")
logging.basicConfig(filename='example.log', level=logging.INFO, format=bot.cfg["logging"]["format"], datefmt=bot.cfg["logging"]["datefmt"])

bot.run(bot.cfg["Tokens"]["NewBlue"])

