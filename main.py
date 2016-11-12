#!/usr/bin/python
import os
import matplotlib.dates
from matplotlib import pyplot as plt
from matplotlib import style
from crontab import CronTab
from SpeedTest import *

style.use('ggplot')

def main():
    path = os.path.abspath(__file__)
    makeCron(path)

    test = SpeedTest()
    test.runTest()
    test.logData(path)


''' Creates a cron job to schedule program if needed '''
def makeCron(path):
    speedtest_ID = "id: SpeedTester"
    cron = CronTab(user=True)

    #does cron job already exist?
    for job in cron:
        if job.comment == speedtest_ID:
            return


    #make cron job if not exist
    dir_path = path[:-7]
    job = cron.new(command= "python %s\n" % path)
    job.set_comment(speedtest_ID)
    job.setall('* * * * *')
    cron.write()



''' Clear all data from database '''
def clearData(path):
    dir_path = path[:-7]
    conn = lite.connect(path + 'test.db')

    with conn:
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS Tests')

''' Plot data '''
def plotData(path):
    dir_path = path[:-7]
    conn = lite.connect(path + 'test.db')
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Tests")
        rows = cursor.fetchall()

        # populate arrays
        dates = []
        downs = []
        ups = []
        for row in rows:
            dates.append(row[0])
            downs.append(row[2])
            ups.append(row[3])

        #formatting
        dates = matplotlib.dates.datestr2num(dates)
        dates = matplotlib.dates.num2date(dates)
        fig, ax = plt.subplots(1)
        formatter = matplotlib.dates.DateFormatter('%Y-%m-%d %H:%M')
        ax.xaxis.set_major_formatter(formatter)
        fig.autofmt_xdate()

        plt.plot(dates, downs, 'ro', label="Down Speed")
        plt.axhline(y=150, color='r', linestyle='-', label='Down Target') # down speed target
        plt.plot(dates, ups, 'bo', label="Down Speed")
        plt.axhline(y=10, color='b', linestyle='-', label='Up Target') # up speed target

        plt.title('Download/Upload Speed')
        plt.xlabel('Date/Time')
        plt.ylabel('Mbit/s')

        plt.subplots_adjust(right=.75)
        plt.legend(bbox_to_anchor=(1,1), loc=2)

        plt.show()

if __name__ == "__main__":
    main()
