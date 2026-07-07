import sqlite3
conn = sqlite3.connect('state.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in c.fetchall()]
print('\n'.join(tables[:50]))
conn.close()
