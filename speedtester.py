#!/usr/bin/python
import os
import requests
import pickle
import matplotlib.dates
from matplotlib import pyplot as plt
from matplotlib import style
from crontab import CronTab
from SpeedTest import *

style.use('ggplot')

def main():
    path = os.path.abspath(__file__)
    makeCron(path)

    if checkIP():
        test = SpeedTest()
        test.runTest()
        test.logData(path)

''' Creates a Cron job for the program if needed '''
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
    job.setall('* 0 * * *')
    cron.write()

''' Gets the IP address for speed monitoring
    Sets the address if not exists'''
def getIP():
    # open and read stored address data
    try:
        addr_file = open('address.obj', 'r')
        address = pickle.load(addr_file)
    # else create new address file
    except IOError:
        address = requests.request('GET', 'http://myip.dnsomatic.com').text
        addr_file = open('address.obj', 'w')
        pickle.dump(address, addr_file)

    return address

''' Checks the users IP address to determine
    if the speed test should be run '''
def checkIP():
        current_ip = requests.request('GET', 'http://myip.dnsomatic.com').text
        test_ip = getIP()

        if current_ip == test_ip:
            return True
        else:
            return False


''' Clear all data from database '''
def clearData(path):
    dir_path = path[:-7]
    conn = lite.connect(dir_path + 'test.db')

    with conn:
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS Tests')

''' Plot data '''
def plotData(path):
    dir_path = path[:-7]
    conn = lite.connect(dir_path + 'test.db')
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
