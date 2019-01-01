#!/usr/bin/env python

#get adb in the platform-tools package for your system
#and it must be in your path
#https://developer.android.com/studio/releases/platform-tools

#or through apt-get
#you also need sqlite3 binary staged in /data/local/tmp
#https://github.com/EXALAB/sqlite3-android/tree/master/binary


from subprocess import call


#create command file and push to device's /data/local/tmp

sql_cmd = "SELECT * FROM network WHERE bssid LIKE 'a0:63:91%';" #a netgear oui
with open('command.sql','w') as f:
	f.write(sql_cmd)
call('adb push command.sql /data/local/tmp/', shell=True)

#run sqlite3 from /data/local/tmp using command.sql as input for command
#sqlite3 command includes headers and csv mode
#then pull the resulting file and delete it from /data/local/tmp
call('adb shell "/data/local/tmp/sqlite3 -header -csv /sdcard/wiglewifi/wiglewifi.sqlite < /data/local/tmp/command.sql > /data/local/tmp/output.csv"', shell=True)
call('adb pull /data/local/tmp/output.csv', shell=True)
call('adb shell rm /data/local/tmp/output.csv', shell=True)