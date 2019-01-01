#!/usr/bin/env python3

#get all wigle dbs in the selected path
#run the DB_QUERY on all of them
#create csv of output
#adds oui vendor, human time, and a link to google maps of lat/long

import sqlite3
import os
import csv
import sys
from datetime import datetime

#constants... change as required or input from command line
DB_QUERY = ('SELECT bssid,ssid,capabilities,lasttime,bestlevel,bestlat,bestlon FROM network WHERE bssid LIKE "a0:63:91%";')
F_OUT = 'some_netgear.tsv'
BASE_PATH = '.'
VENDOR_CONN = sqlite3.Connection('macvendors.db')
VENDOR_CUR = VENDOR_CONN.cursor()

def get_db_list(BASE_PATH):

	'''get all wigle dbs in the designated path'''
	
	db_list = [
		os.path.abspath(x)
		for x in os.listdir(BASE_PATH) 
		if x.startswith('wiglewifi') and x.endswith('.sqlite')
	]
	return db_list

def enrich_dev(device):
	
	'''get the mac vendor, a human time, and generate a maps.google.com link'''
	
	oui = device[0].replace(':', '').replace('-', '').upper()[0:6]
	VENDOR_CUR.execute('SELECT vendor FROM macvendors WHERE mac=="{}";'.format(oui))
	match = VENDOR_CUR.fetchone()
	if match == None:
		vendor = 'Not Found'
	else:
		vendor = match[0]
		
	#the base link is just a maps.google.com thing...
	#the =HYPERLINK thing will tell excel to treat it as a URL for your clicking pleasure
	gmaps_link = '=HYPERLINK("https://www.google.com/maps/search/{},{}")'.format(device[5], device[6])
	
	#turns out python3 throws an error if the timestamp is 0, which occurs a lot in wigle db
	try:
		date_stamp = str(datetime.fromtimestamp(int(device[3]) / 1000))
	except OSError:
		date_stamp = 'Invalid'
		
	return vendor, gmaps_link, date_stamp
	
def main():
	
	#check to see if python version is 3 or not, exit if not
	if not (sys.version.startswith('3')):
		print ('Sorry, only compatible with Python 3')
		sys.exit()
	
	devices = []
	
	#get all wigle dbs in the give BASE_PATH
	db_list = get_db_list(BASE_PATH)
	
	#Run the queries for every db
	for wigle_db in db_list:
		conn = sqlite3.Connection(wigle_db)
		cur = conn.cursor()
		cur.execute(DB_QUERY)
		results = cur.fetchall()
		conn.close()
		for dev in results:
			#this bit is unwieldy, but I need them re-ordered
			enrichment = enrich_dev(dev) #get vendor, date from timestamp and maps.google.com link
			enriched_dev = (dev[0], enrichment[0], dev[1], dev[2], dev[3], enrichment[2], dev[4], dev[5], dev[6], enrichment[1])
			if enriched_dev not in devices:
				devices.append(enriched_dev)
				
	
	#spew to tsv file, with utf-16 encoding (needed for wigle db), quoting all entries, etc...
	with open(F_OUT, 'w', encoding='utf-16', newline='') as f:
		writer = csv.writer(f, dialect='excel', quoting=csv.QUOTE_ALL, delimiter='\t')
		writer.writerow(('MAC', 'Vendor', 'Name', 'Capabilities', 'Last Time', 'Last Date', 'Best RSSI', 'Best Lat', 'Best Long', 'Google Maps'))
		writer.writerows(devices)
	VENDOR_CONN.close()

if __name__ == '__main__':
	main()
			