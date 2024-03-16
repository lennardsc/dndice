import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from collections import defaultdict

class RollAnalysis:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)

    def highest_lowest_median_by_day(self):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT timestamp, roll_result FROM dice_rolls''')
        rolls = cursor.fetchall()

        rolls_by_day = defaultdict(list)
        for timestamp, result in rolls:
            day = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').date()
            rolls_by_day[day].append(result)

        days = []
        highest = []
        lowest = []
        median = []
        for day, rolls in rolls_by_day.items():
            days.append(day)
            highest.append(max(rolls))
            lowest.append(min(rolls))
            median.append(np.median(rolls))

        plt.figure(figsize=(10, 6))
        plt.plot(days, highest, label='Highest')
        plt.plot(days, lowest, label='Lowest')
        plt.plot(days, median, label='Median')
        plt.xlabel('Date')
        plt.ylabel('Result')
        plt.title('Highest, Lowest, and Median Rolls by Day')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def count_median_1_by_day(self):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT timestamp, roll_result FROM dice_rolls WHERE roll_result = 1''')
        rolls_1 = cursor.fetchall()

        rolls_by_day = defaultdict(list)
        for timestamp, result in rolls_1:
            day = datetime.strptime(timestamp, '%Y-%m-%d').date()
            rolls_by_day[day].append(result)

        days = []
        count = []
        median = []
        for day, rolls in rolls_by_day.items():
            days.append(day)
            count.append(len(rolls))
            median.append(np.median(rolls))

        plt.figure(figsize=(10, 6))
        plt.bar(days, count, label='Count')
        plt.plot(days, median, color='red', marker='o', label='Median')
        plt.xlabel('Date')
        plt.ylabel('Count')
        plt.title('Count of Rolls with Result 1 and Median by Day')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def count_20_by_day(self):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT timestamp, roll_result FROM dice_rolls WHERE roll_result = 20''')
        rolls_20 = cursor.fetchall()

        rolls_by_day = defaultdict(list)
        for timestamp, result in rolls_20:
            day = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').date()
            rolls_by_day[day].append(result)

        days = []
        count = []
        for day, rolls in rolls_by_day.items():
            days.append(day)
            count.append(len(rolls))

        plt.figure(figsize=(10, 6))
        plt.bar(days, count)
        plt.xlabel('Date')
        plt.ylabel('Count')
        plt.title('Count of Rolls with Result 20 by Day')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def close_connection(self):
        self.conn.close()
