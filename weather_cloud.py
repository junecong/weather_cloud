#Hello, this is a script to get the weather at my house and and change my Lifex bulb to tell it to me in the morning.

#import schedule to schedule lights everyday at 7am-9am
import sys
import schedule 
#import for lifx lightbulb settings
import time
import requests 
#import for weather json parsing
import json
import urllib2 

token = "YOUR TOKEN HERE" 
headers = {
    "Authorization": "Bearer %s" % token,
}

rain = False
degree = 0

def get_weather_for_the_day():
	f = urllib2.urlopen('URL FOR WEATHER CALL HERE')
	json_string = f.read()
	parsed_json = json.loads(json_string)
	degree = parsed_json['currently']['apparentTemperature']
	degree = float(degree)
	rainfall = parsed_json['daily']['data'][0]['precipProbability']
	rainfall = float(rainfall)
	if rainfall > 0:
		rain = True
	print "Current temperature is: %s" % (degree)
	print "Will it rain? %s" % (rain)
	f.close()
	return degree

def color_based_on_weather(degree, rain):
	if rain:
		print "Pink and %s" % (degree)
		color = 'pink'
	else:
	    if degree >= 80:
	    	print "Red and %s" % (degree)
	        color = 'red'
	    elif degree >= 70:
	    	print "orange and %s" % (degree)
	        color = 'orange'
	    elif degree >= 63:
	    	print "white and %s" % (degree)
	        color = 'white'
	    elif degree >= 55:
	    	print "blue and %s" % (degree)
	        color = 'blue'
	    else:
	    	print "purple and %s" % (degree)
	        color = 'purple'
	    return color
	return color

def on():
	print("Let there be light")
	degree = get_weather_for_the_day()
	color = color_based_on_weather(degree, rain)

	#Lastly, you want to set the color and pass it to the bulb
	payload = {
	    "power": "on",
	    "color": color,
	    "brightness": 1.0,
	    "duration": 10,
	}
	response = requests.put('https://api.lifx.com/v1/lights/all/state', data=payload, headers=headers)
	
def off():
	payload = {
	    "power": "off",
	}


#Set the bulb to do this every day at 7:00am
schedule.every().day.at("13:20").do(on)
#Set the bulb to turn off every day at 9:00am
schedule.every().day.at("13:22").do(off)

while True:
    schedule.run_pending()
    time.sleep(1)

# Test module
# while True:
# on()

