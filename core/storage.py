import sqlite3
from datetime import datetime

class DiceRollStorage:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS dice_rolls (
                            id INTEGER PRIMARY KEY,
                            roll_text TEXT,
                            roll_result INTEGER,
                            timestamp TEXT
                        )''')
        self.conn.commit()

    def insert_roll(self, roll_text, roll_result):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO dice_rolls (roll_text, roll_result, timestamp)
                        VALUES (?, ?, ?)''', (roll_text, roll_result, timestamp))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
