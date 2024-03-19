import sqlite3
from datetime import datetime

class DiceRollStorage:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            # Create dimensions
            self.conn.execute('''CREATE TABLE IF NOT EXISTS dice_types (
                                    id INTEGER PRIMARY KEY,
                                    num_dice INTEGER,
                                    num_sides INTEGER
                                )''')
            # Create fact table
            self.conn.execute('''CREATE TABLE IF NOT EXISTS roll_results (
                                    id INTEGER PRIMARY KEY,
                                    dice_type_id INTEGER,
                                    result INTEGER,
                                    timestamp TEXT,
                                    FOREIGN KEY (dice_type_id) REFERENCES dice_types(id)
                                )''')

    def insert_roll(self, num_dice, num_sides, result):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with self.conn:
            # Insert into dimensions and get the id
            dice_type_id = self.insert_or_get_dice_type_id(num_dice, num_sides)
            # Insert into fact table
            self.conn.execute('''INSERT INTO roll_results (dice_type_id, result, timestamp)
                                VALUES (?, ?, ?)''', (dice_type_id, result, timestamp))

    def insert_or_get_dice_type_id(self, num_dice, num_sides):
        # Check if the dice type already exists
        cursor = self.conn.execute('''SELECT id FROM dice_types WHERE num_dice=? AND num_sides=?''', (num_dice, num_sides))
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            # Insert and return the id
            cursor = self.conn.execute('''INSERT INTO dice_types (num_dice, num_sides) VALUES (?, ?)''', (num_dice, num_sides))
            return cursor.lastrowid

    def close_connection(self):
        self.conn.close()
