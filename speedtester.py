'''
Test internet speed every hour, log results
'''

from SpeedTest import *

def main():
    test = SpeedTest()
    test.runTest()
    print(test.down)



if __name__ == "__main__":
    main()
