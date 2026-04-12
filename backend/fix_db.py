import sqlite3

db = sqlite3.connect('./data/webui.db')
cursor = db.cursor()
cursor.execute("DELETE FROM config WHERE id = 'rag.template';")
db.commit()
db.close()
print("rag.template deleted from config table.")
