#Script to get the weather and change my Lifex bulb to tell it to me in the morning.

import sys
import schedule #import schedule to schedule lights everyday at 7am-9am
import time
import requests #import for lifx lightbulb settings
import json
import urllib2 #import for weather json parsing

color = "white" #color I want the bulb to change to
degree = 0 #what the weather feels like at the moment, not actual temperature
rain = False #will it rain today?
rainfall = 0



headers = {
    "Authorization": "Bearer %s" % token,
}

def get_weather_for_the_day():
	f = urllib2.urlopen('http://api.wunderground.com/api/7d7772c918e39295/conditions/q/CA/San_Francisco.json')
	json_string = f.read()
	parsed_json = json.loads(json_string)
	degree = parsed_json['current_observation']['feelslike_f']
	degree = float(degree)
	rainfall = parsed_json['current_observation']['precip_today_string']
	rainfall = float(rainfall[0:4])
	if rainfall > 0:
		rain = True
	print "Current temperature is: %s" % (degree)
	print "Will it rain? %s" % (rainfall)
	f.close()
	return degree

def color_based_on_weather(degree):
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

def on():
	print("Let there be light")
	degree = get_weather_for_the_day()
	color = color_based_on_weather(degree)

	#Lastly, you want to set the color and pass it to the bulb
	payload = {
	    "power": "on",
	    "color": color,
	    "brightness": 1.0,
	    "duration": 10,
	}
	response = requests.put('https://api.lifx.com/v1/lights/all/state', data=payload, headers=headers)
	
	# if rain == True:
	# 	data = {
	#     "period": 2,
	#     "color": "pink",
	# 	}
	# 	response = requests.post('https://api.lifx.com/v1/lights/all/effects/breathe', data=data, headers=headers)

def off():
	payload = {
	    "power": "off",
	}

# #Set the bulb to do this every day at 7:00am
# schedule.every().day.at("0:25").do(on)
# #Set the bulb to turn off every day at 9:00am
# schedule.every().day.at("9:00").do(off)


# while True:
#     schedule.run_pending()
#     time.sleep(1)


while True:
    on()

