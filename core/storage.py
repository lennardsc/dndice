import sqlite3
from datetime import datetime

class DiceRollStorage:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS dim_date (
                                    date_id INTEGER PRIMARY KEY,
                                    date TEXT
                                )''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS dim_result (
                                    result_id INTEGER PRIMARY KEY,
                                    result INTEGER
                                )''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS fact_rolls (
                                    roll_id INTEGER PRIMARY KEY,
                                    date_id INTEGER,
                                    result_id INTEGER,
                                    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
                                    FOREIGN KEY (result_id) REFERENCES dim_result(result_id)
                                )''')

    def insert_roll(self, date, result):
        date_id = self._get_or_insert_date(date)
        result_id = self._get_or_insert_result(result)
        with self.conn:
            self.conn.execute('''INSERT INTO fact_rolls (date_id, result_id)
                                VALUES (?, ?)''', (date_id, result_id))

    def _get_or_insert_date(self, date):
        with self.conn:
            cursor = self.conn.execute('''SELECT date_id FROM dim_date WHERE date = ?''', (date,))
            date_id = cursor.fetchone()
            if date_id is not None:
                return date_id[0]
            else:
                cursor = self.conn.execute('''INSERT INTO dim_date (date) VALUES (?)''', (date,))
                return cursor.lastrowid

    def _get_or_insert_result(self, result):
        with self.conn:
            cursor = self.conn.execute('''SELECT result_id FROM dim_result WHERE result = ?''', (result,))
            result_id = cursor.fetchone()
            if result_id is not None:
                return result_id[0]
            else:
                cursor = self.conn.execute('''INSERT INTO dim_result (result) VALUES (?)''', (result,))
                return cursor.lastrowid

    def get_roll_stats_by_day(self, result=None):
        query = '''SELECT d.date, COUNT(*) AS count, AVG(r.result) AS median
            FROM dim_date d
            JOIN fact_rolls fr ON d.date_id = fr.date_id
            JOIN dim_result r ON fr.result_id = r.result_id
            {}
            GROUP BY d.date'''.format('WHERE r.result = ?' if result is not None else '')

        if result is not None:
            with self.conn:
                cursor = self.conn.execute(query, (result,))
        else:
            with self.conn:
                cursor = self.conn.execute(query)

        return cursor.fetchall()


    def close_connection(self):
        self.conn.close()
