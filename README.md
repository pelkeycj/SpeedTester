**SpeedTester**
================

A python application to monitor network speeds
------------------

SpeedTester tests and logs network speeds at set intervals.
Network speeds are only tested for the desired IP.

Arguments include:
- "-c" to clear database of all entries
- "-p" to generate a plot of upload/download speeds
- "-ip" to reset the tracked IP address to the current IP
- "-m" to set cron interval to minutely
- "-h" to set cron interval to hourly
- "-d" to set cron interval to daily
