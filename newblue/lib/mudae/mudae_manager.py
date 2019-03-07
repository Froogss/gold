import re

import discord


class MudaeManager:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        self.mudae_ids = ["432610292342587392", "522749851922989068"]
        self.check_existing_tables()

    def determine_message_type(self, message):
        if str(message.author.id) in self.mudae_ids and len(message.embeds) == 1:
            embed = message.embeds[0]
            if message.author != discord.Embed.Empty \
                    and embed.footer.text == discord.Embed.Empty \
                    and embed.image.url != discord.Embed.Empty \
                    and embed.title == discord.Embed.Empty \
                    and embed.thumbnail.url == discord.Embed.Empty \
                    and "\n" not in embed.description \
                    and "\n" not in message.author.name:  # we have ourself a roll result
                print("yes")
                self.process_roll_result(message)

            # print(f"title: {embed.title}")
            # print(f"thimbnail: {embed.thumbnail}")
            # print(f"desc: {embed.description}")
            # print(f"footer: {embed.footer}")
            # print(f"image: {embed.image}")
            # print(f"url: {embed.url}")
            # print(f"prov: {embed.provider}")
            # print(f"author: {embed.author}")

    def process_roll_result(self, message):
        cursor = self.db.cursor()
        cursor.execute("""INSERT INTO rollResults values (?, ?, ?)""",
                       [message.embeds[0].author.name.strip('*'), str(message.guild.id), message.created_at])
        print(f'Added {message.embeds[0].author.name.strip("*")} to database')
        self.db.commit()

    def check_existing_tables(self):
        cursor = self.db.cursor()
        query_str = """SELECT name FROM sqlite_master WHERE type='table' AND name='{}';"""

        if len(cursor.execute(query_str.format('claims')).fetchall()) < 1:
            cursor.execute(
                """CREATE TABLE claims (userId varchar(20), guildId varchar(20), waifuName string, createdAt datetime)""")
            self.db.commit()

        if len(cursor.execute(query_str.format('rollResults')).fetchall()) < 1:
            cursor.execute("""CREATE TABLE rollResults (waifuName string, guildId varchar(20), createdAt datetime)""")
            self.db.commit()

    def process_claim_message(self, message):
        cursor = self.db.cursor()
        res = re.search(r". (.*) and (.*) are now married! .", message.content)
        print(res.group(1).strip('*'))
        users = [user for user in message.guild.members if user.name == res.group(1).strip('*')]
        if len(users) != 1:
            # TODO log that multiple users were found
            return
        user_id = users[0].id
        print("adding")
        cursor.execute("""INSERT INTO claims values (?, ?, ?, ?) """,
                       [user_id, message.guild.id, res.group(2).strip('*'), message.created_at])
        self.db.commit()
