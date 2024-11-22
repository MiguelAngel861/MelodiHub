import sqlite3

#cursor de tabla sqlite
conn = sqlite3.connect('repify.db')
cursor = conn.cursor()
#creando tabla
cursor.execute('''
               CREATE TABLE IF NOT EXISTS cancion (
               id INTEGER PRIMARY KEY,
               nombre TEXT NOT NULL, 
               fecha TEXT,
               album TEXT

               )

               ''')
conn.commit()

conn.close()