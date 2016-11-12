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
        try:
            self.results = os.popen("/usr/local/bin/speedtest-cli --simple --secure").read().split()
        except:
            return
        if 'Cannot' not in self.results:
            self.ping = float(self.results[1])
            self.down = float(self.results[4])
            self.up = float(self.results[7])

    ''' Log data in sqlite database '''
    def logData(self, path):
        dir_path = path[:-7]
        conn = lite.connect(dir_path + 'test.db')
        os.popen("echo 'connecting' >> ~/Documents/scripts/SpeedTester/debugger.txt")
        with conn:
            os.popen("echo 'connected!!' >> ~/Documents/scripts/SpeedTester/debugger.txt")
            cursor = conn.cursor()

            cursor.execute("CREATE TABLE IF NOT EXISTS Tests(Timestamp TEXT, Ping REAL, Down REAL, Up REAL)")
            cursor.execute("INSERT INTO Tests(Timestamp, Ping, Down, Up) VALUES(?,?,?,?)",
                            (self.timestamp, self.ping, self.down, self.up))
