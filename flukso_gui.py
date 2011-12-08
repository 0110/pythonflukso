#!/usr/bin/env python

# Features
# - Display the actual power consuption
# - Display the actual weather (according to google)
#
# Requirements:
# - python ;-)
# - gtkpy
# - pango (if not already installed with gtkpy)
# - http://code.google.com/p/python-weather-api/


import urllib2
import simplejson
import datetime
import time
import pywapi
import string
import pygtk
pygtk.require('2.0')
import gtk, gobject, pango


class FluksoGUI:
	
	# Layout:
	# +----------------------------------+
	# |               Time               |
	# |              Weather             |
	# |         power consumption        |
	# +----------------------------------+
	def __init__(self, timeout_power, timeout_weather):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("destroy", self.destroy)
		self.window.set_size_request(800,600);
		self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(0,0,0))
#		self.window.fullscreen()
		
		self.label = gtk.Label('time label')
		self.label.set_use_markup(True)
		self.label.modify_font(pango.FontDescription("sans 20"))
		self.label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color(65535,65535,65535))

		self.weather = gtk.Label('Weather')
		self.weather.set_use_markup(True)
		self.weather.modify_font(pango.FontDescription("sans 20"))
		self.weather.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color(0,65535,0))

		self.power = gtk.Label('Power')
		self.power.set_use_markup(True)
		self.power.modify_font(pango.FontDescription("sans 50"))
		self.power.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color(65535,65535,65535))

		vbox = gtk.VBox()
	
		vbox.pack_start(self.label)
		vbox.pack_start(self.weather)
		vbox.pack_start(self.power)		

		self.window.add(vbox)
		self.window.show_all()
		gobject.timeout_add_seconds(timeout_power, self.update_power)
		gobject.timeout_add_seconds(timeout_weather, self.update_weather)

	def destroy(self, widget, data=None):
		gtk.main_quit()
	
	def update_weather(self):
		# Here the weather location has to be inserted
		google_result = pywapi.get_weather_from_google('68199','DE')
		weather = "Heute " + google_result['current_conditions']['condition'] + " bei " + google_result['current_conditions']['temp_c'] + " C\n" + google_result['current_conditions']['wind_condition'] + "\nin " + google_result['forecast_information']['city'] + "."
		self.weather.set_text(weather)

	def update_power(self):
		self.label.set_text(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
		try:
			dummy = int(self.getCurrentPower())
			power = "%d Watt" % self.getCurrentPower()
		except:
			power = "Data missing\n(Network error?)"
		self.power.set_text(power)
		return True
			
	def main(self):
		gtk.main()

	def getCurrentPower(self):
	        sensor_id = '437728cc335cf14021957af9552835a5'
	        url = ''.join([
        	        'http://192.168.255.1:8080',
                	'/sensor/%s' % sensor_id,
			'?unit=watt&interval=minute&version=1.0',
			])
		try:
			json = urllib2.urlopen(url).read()
			pydata = simplejson.loads(json)
			current_power = pydata[-1][1]
			return current_power
		except Exception:
			return "ERROR: Data missing"

if __name__ == "__main__":
	print "Starting GUI..."
#	update the energie every two seconds, the weather will be updated once an hour
	base = FluksoGUI(2,3600)
#	initial update
	base.update_power()
	base.update_weather()
	base.main()

