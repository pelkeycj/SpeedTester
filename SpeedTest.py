import os

class SpeedTest():
    def __init__(self):
        self.ping = 0
        self.down = 0
        self.up = 0

    #run speedtest
    def runTest(self):
        self.results = os.popen("/usr/local/bin/speedtest-cli --simple").read().split()
        if 'Cannot' not in self.results:
            self.ping = float(self.results[1])
            self.down = float(self.results[4])
            self.up = float(self.results[7])
