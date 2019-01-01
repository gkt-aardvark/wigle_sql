```# wigle_sql
Just some simple utilities to pull data from wigle sqlite databases

These two utilities do the following:

wigle_pull.py:	- performs a SQL query on as many wiglewifi databases you have in the specified folder.
				- I have many phones that I use to wardrive, so I end up with many databases.
				- This outputs the results to the file you specify in the code in TSV format.

wigle_sql.py: 
			- performs a SQL query on a running Android phone with Wigle Wardriving installed.
			- just change the SQL query to change output
			- need sqlite3 binary (link in script)
			- need adb in your path (link in script)
			- stages a sql command file in /data/local/tmp and queries the /sdcard/wiglewifi/wiglewifi.sqlite db
			- outputs the results to a csv, also in /data/local/tmp
			- pulls that file to local system with adb pull
			- deletes the output.csv from /data/local/tmp```
