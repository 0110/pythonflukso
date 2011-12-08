#!/usr/bin/env python

import urllib2
import simplejson
#import datetime
#import time
#import pprint

sensor_id = '437728cc335cf14021957af9552835a5'

url = ''.join([
	'http://flukso:8080',
	'/sensor/%s' % sensor_id,
	'?unit=watt&interval=minute&version=1.0',
	])
try:
	json = urllib2.urlopen(url).read()
	pydata = simplejson.loads(json)
	current_power = pydata[-1][1]
	print current_power
except Exception:
	print "ERROR"

#print datetime.datetime.fromtimestamp(int(pydata[-1][0])).strftime("%Y-%m-%d %H:%M:%S"), "Watt", pydata[-1][1]

#print pydata.[0]
