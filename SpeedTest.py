import os
import datetime
import sqlite3 as lite

class SpeedTest():
    def __init__(self):
        self.ping = 0
        self.down = 0
        self.up = 0
        self.timestamp = datetime.datetime.now()

    ''' Run speedtest '''
    def runTest(self):
        self.results = os.popen("/usr/local/bin/speedtest-cli --simple").read().split()
        if 'Cannot' not in self.results:
            self.ping = float(self.results[1])
            self.down = float(self.results[4])
            self.up = float(self.results[7])

    ''' Log data in sqlite database '''
    def logData(self):
        conn = lite.connect('test.db')
        with conn:
            cursor = conn.cursor()

            cursor.execute("CREATE TABLE IF NOT EXISTS Tests(Timestamp INT, Ping REAL, Down REAL, Up REAL)")
            cursor.execute("INSERT INTO Tests(Timestamp, Ping, Up, Down) VALUES(?,?,?,?)",
                            (self.timestamp, self.ping, self.down, self.up))
