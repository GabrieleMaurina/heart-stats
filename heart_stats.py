import datetime
import json
import re
import pandas


import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_pdf import PdfPages

STATS_RE = re.compile(r'(\d{2,3})\s+(\d{2,3})\s+(\d{2,3})')


def get_stats(text):
    if match := STATS_RE.search(text):
        return {
            'sys': int(match.group(1)),
            'dia': int(match.group(2)),
            'rate': int(match.group(3))
        }
    return None


def load_data():
    with open('result.json') as file:
        messages = json.load(file)['messages']
    data = []
    for message in messages:
        if stats := get_stats(message['text']):
            item = {'date': datetime.datetime.fromisoformat(message['date'])}
            item.update(stats)
            data.append(item)
    return pandas.DataFrame.from_dict(data).sort_values(by='date').reset_index(drop=True)


def create_plot(data):
    with PdfPages('heart_stats.pdf') as pdf:
        fig1 = plt.figure(figsize=(8.5, 11))
        ax1 = fig1.add_subplot(111)
        ax1.scatter(data['date'], data['sys'], label='Systolic', marker='o')
        ax1.scatter(data['date'], data['dia'], label='Diastolic', marker='s')
        ax1.scatter(data['date'], data['rate'], label='Heart Rate', marker='^')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Value')
        ax1.set_title('Stats')
        ax1.grid(True)
        ax1.legend()
        ax1.xaxis.set_major_locator(mdates.DayLocator(interval=3))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax1.set_yticks(range(60, 161, 5))
        pdf.savefig(fig1)
        plt.close(fig1)

        fig2, ax2 = plt.subplots(figsize=(8.5, 11))
        ax2.axis('off')
        table_data = data[['date', 'sys', 'dia', 'rate']].values
        col_labels = ['Date', 'Systolic', 'Diastolic', 'Heart Rate']
        table = ax2.table(
            cellText=table_data,
            colLabels=col_labels,
            loc='center',
            cellLoc='center'
        )
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.3)

        pdf.savefig(fig2)
        plt.close(fig2)

def main():
    data = load_data()
    create_plot(data)


if __name__ == "__main__":
    main()
