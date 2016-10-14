#Script to get the weather and change my Lifex bulb to tell it to me in the morning.

import sys
import schedule #import schedule to schedule lights everyday at 7am-9am
import time
import requests #import for lifx lightbulb settings
import json

#defining variables
color = "white" #color I want the bulb to change to
degree = 0
rain = False
url = "http://www.google.com"

# Colors
# Purple - hue:295 saturation:1.0 brightness:1 kelvin:3500
# Blue - hue:240 saturation:1.0 brightness:1
# Warm white - kelvin:2700 brightness: 1
# Orange - hue:45 saturation:1.0 brightness:1
# Red - hue:0 saturation:1.0 brightness:1

token = "c7aeb493236f5c7938012b106609337b890480da42325bc6bf828c3f8cb89799"

headers = {
    "Authorization": "Bearer %s" % token,
}








def get_weather_for_the_day(url):
	"""Return what the weather will be like for the day"""
	pass

def color_based_on_weather(degree):
    if degree >= 80:
        color = 'red'
    elif degree >= 70:
        color = 'orange'
    elif degree >= 63:
        color = 'white'
    elif degree >= 55:
        color = 'blue'
    else:
        color = 'purple'
    return color




#main function that runs in the morning
def on():
	print("Let there be light")
    # degree = get_weather_for_the_day(url)
	color = color_based_on_weather(degree)

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
schedule.every().day.at("7:00").do(on)
#Set the bulb to turn off every day at 9:00am
schedule.every().day.at("9:00").do(off)


while True:
    schedule.run_pending()
    time.sleep(1)




