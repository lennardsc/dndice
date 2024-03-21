import duckdb
from datetime import datetime

class DiceRollStorage:
    def __init__(self, db_file):
        self.conn = duckdb.connect(db_file)
        self.create_tables()

    def create_tables(self):
        with self.conn.cursor() as cursor:
            cursor.execute('''CREATE TABLE IF NOT EXISTS dim_date (
                                date_id INTEGER PRIMARY KEY,
                                date TEXT
                            )''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS dim_result (
                                result_id INTEGER PRIMARY KEY,
                                result INTEGER
                            )''')
            cursor.execute('''CREATE SEQUENCE IF NOT EXISTS roll_id_seq''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS fact_rolls (
                            roll_id INTEGER PRIMARY KEY,
                            date_id INTEGER,
                            result_id INTEGER,
                            FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
                            FOREIGN KEY (result_id) REFERENCES dim_result(result_id)
                        )''')



    def insert_roll(self, date, result):
        date_id = self._get_or_insert_date(date)
        result_id = self._get_or_insert_result(result)
        with self.conn.cursor() as cursor:
            cursor.execute('''INSERT INTO fact_rolls (roll_id, date_id, result_id) VALUES (NEXTVAL('roll_id_seq'), ?, ?)''', (date_id, result_id))



    def _get_or_insert_date(self, date):
        with self.conn.cursor() as cursor:
            try:
                cursor.execute('''INSERT INTO dim_date (date) VALUES (?)''', (date,))
                return cursor.lastrowid
            except duckdb.ConstraintException:
                # Handle constraint violation here (e.g., log an error message, retry insertion)
                return None

    def _get_or_insert_result(self, result):
        with self.conn.cursor() as cursor:
            try:
                cursor.execute('''INSERT INTO dim_result (result) VALUES (?)''', (result,))
                return cursor.lastrowid  # Use lastrowid to get the auto-generated primary key
            except duckdb.ConstraintException:
                # Handle constraint violation here (e.g., log an error message, retry insertion)
                return None


    def get_roll_stats_by_day(self, result=None):
        with self.conn.cursor() as cursor:
            if result is not None:
                query = '''SELECT d.date, COUNT(*) AS count, AVG(r.result) AS median
                    FROM dim_date d
                    JOIN fact_rolls fr ON d.date_id = fr.date_id
                    JOIN dim_result r ON fr.result_id = r.result_id
                    WHERE r.result = ?
                    GROUP BY d.date'''
                cursor.execute(query, (result,))
            else:
                query = '''SELECT d.date, COUNT(*) AS count, AVG(r.result) AS median
                    FROM dim_date d
                    JOIN fact_rolls fr ON d.date_id = fr.date_id
                    JOIN dim_result r ON fr.result_id = r.result_id
                    GROUP BY d.date'''
                cursor.execute(query)

            return cursor.fetchall()
    def close_connection(self):
        self.conn.close()  # Close the connection
