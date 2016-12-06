#! /usr/bin/python
import os
import sys
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

    #handle arguments
    args = sys.argv[1:]
    for arg in args:
        if arg == "-c":
            clearData(path)
        elif arg == "-p":
            plotData(path)
        elif arg == "-ip":
            setIP(path)
        elif arg == "-td":
            down_target = float(raw_input("Enter download target speed: "))
            setTargets(path, down=down_target, up=None)
        elif arg == "-tu":
            up_target = float(raw_input("Enter upload target speed: "))
            setTargets(path, down=None, up=up_target)
        elif arg == "-min" or arg == "-hour" or arg == "-day" or arg == "-reboot":
            setCron(arg)
        elif arg == "-run":
            #run test
            if checkIP(path):
                print("Testing . . .")
                test = SpeedTest()
                test.runTest()
                test.logData(path)
                print('Complete')
        else:
            print("Error: enter valid arguments")
            print("-c to clear database")
            print("-p to plot data")
            print("-min to track minutely data")
            print("-hour to track hourly data")
            print("-day to track daily data")
            print("-reboot to track data upon boot")
            print("-ip to set IP address to current")
            print("-td to enter download target speed")
            print("-tu to enter upload target speed")
            print("-run to run test")


''' Alters the current cron job to desired frequency'''
def setCron(arg):
    speedtest_ID = "id: SpeedTester"
    cron = CronTab(user=True)

    for job in cron:
        if job.comment == speedtest_ID:
            if arg == "-min":
                job.setall('* * * * *')
            elif arg == "-hour":
                job.setall('@hourly')
            elif arg == "-day":
                job.setall('@daily')
            elif arg == "-reboot":
                job.setall('@reboot')
            cron.write()


''' Creates a Cron job for the program if needed '''
def makeCron(path):
    speedtest_ID = "id: SpeedTester"
    cron = CronTab(user=True)

    #does cron job already exist?
    for job in cron:
        if job.comment == speedtest_ID:
            return


    #make cron job if not exist
    dir_path = path[:-14]
    job = cron.new(command= "python %s + -run\n" % path)
    job.set_comment(speedtest_ID)
    job.setall('0 * * * *')
    cron.write()

''' Sets the IP address to the current IP '''
def setIP(path):
    dir_path = path[:-14]
    address = requests.request('GET', 'http://myip.dnsomatic.com').text
    addr_file = open(dir_path + 'address.obj', 'w')
    pickle.dump(address, addr_file)

    return address

''' Gets the IP address for speed monitoring
    Sets the address if not exists'''
def getIP(path):
    dir_path = path[:-14]
    # open and read stored address data
    try:
        addr_file = open(dir_path + 'address.obj', 'r')
        address = pickle.load(addr_file)
    # else create new address file
    except IOError:
        address = setIP(path)

    return address

''' Checks the users IP address to determine
    if the speed test should be run '''
def checkIP(path):
        current_ip = requests.request('GET', 'http://myip.dnsomatic.com').text
        test_ip = getIP(path)

        if current_ip == test_ip:
            return True
        else:
            return False

''' Set download/upload target speeds '''
def setTargets(path, down=None, up=None):
        dir_path = path[:-14]

        if down is not None:
            down_file = open(dir_path + 'down.obj', 'w')
            pickle.dump(down, down_file)
        if up is not None:
            up_file = open(dir_path + 'up.obj', 'w')
            pickle.dump(up, up_file)

''' return download/upload target speeds '''
def getTargets(path):
    dir_path = path[:-14]
    down_file = open(dir_path + 'down.obj', 'r')
    up_file = open(dir_path + 'up.obj', 'r')

    down_target = pickle.load(down_file)
    up_target = pickle.load(up_file)

    return (down_target, up_target)

''' Clear all data from database '''
def clearData(path):
    dir_path = path[:-14]
    conn = lite.connect(dir_path + 'test.db')

    with conn:
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS Tests')

''' Plot data '''
def plotData(path):
    dir_path = path[:-14]
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
        plt.plot(dates, ups, 'bo', label="Up Speed")

        # attempt to load and graph target lines
        try:
            down_target, up_target = getTargets(path)
            plt.axhline(y=down_target, color='r', linestyle='-', label='Down Target') # down speed target
            plt.axhline(y=up_target, color='b', linestyle='-', label='Up Target') # up speed target
        except:
            print("error")
            pass

        plt.title('Download/Upload Speed')
        plt.xlabel('Date/Time')
        plt.ylabel('Mbit/s')

        plt.subplots_adjust(right=.75)
        plt.legend(bbox_to_anchor=(1,1), loc=2)

        plt.show()

if __name__ == "__main__":
    main()
