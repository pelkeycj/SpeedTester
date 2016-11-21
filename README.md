**SpeedTester**
================

A python application to monitor network speeds
------------------

SpeedTester tests and logs network speeds at set intervals.
Network speeds are only tested for the desired IP.

Arguments include:
- "-run" to run run a speedtest and log results
- "-c" to clear database of all entries
- "-td" to set the target download speed
- "-tu" to set the target upload speed
- "-p" to generate a plot of upload/download speeds
- "-ip" to reset the tracked IP address to the current IP
- "-min" to set cron interval to minutely
- "-hour" to set cron interval to hourly
- "-day" to set cron interval to daily
- "-reboot" to set cron interval to every reboot

It is recommended to create an alias in the ~/.bashrc file containing the command and full path to run speedtester.py
