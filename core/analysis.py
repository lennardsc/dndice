import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from collections import defaultdict
from storage import DiceRollStorage

class RollAnalysis:
    def __init__(self, db_file):
        self.storage = DiceRollStorage(db_file)

    def plot_roll_stats_by_day(self, rolls, label, y_label, title):
        try:
            rolls_by_day = defaultdict(list)
            for timestamp, result in rolls:
                day = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').date()
                rolls_by_day[day].append(result)

            days = []
            values = []
            for day, rolls in rolls_by_day.items():
                days.append(day)
                values.append(np.median(rolls))

            plt.figure(figsize=(10, 6))
            plt.bar(days, values, label=label)
            plt.xlabel('Date')
            plt.ylabel(y_label)
            plt.title(title)
            plt.xticks(rotation=45)
            plt.legend()
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"An error occurred: {e}")

    def highest_lowest_median_by_day(self):
        rolls = self.storage.get_roll_stats_by_day()
        self.plot_roll_stats_by_day(rolls, 'Median', 'Result', 'Highest, Lowest, and Median Rolls by Day')

    def count_median_1_by_day(self):
        rolls = self.storage.get_roll_stats_by_day(result=1)
        self.plot_roll_stats_by_day(rolls, 'Count', 'Count', 'Count of Rolls with Result 1 by Day')

    def count_20_by_day(self):
        rolls = self.storage.get_roll_stats_by_day(result=20)
        self.plot_roll_stats_by_day(rolls, 'Count', 'Count', 'Count of Rolls with Result 20 by Day')

    def close_connection(self):
        self.storage.close_connection()
