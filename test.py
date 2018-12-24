import sqlite3
db = sqlite3.connect('test.db')

cursor = db.cursor()

cursor.execute("""drop table waifuClaims""")
cursor.execute("""CREATE TABLE waifuClaims (
                  user_id string, waifu_name string, date datetime)""")
print(cursor.fetchall())
db.close()
