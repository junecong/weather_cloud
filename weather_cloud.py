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
#import to print time
import time

token = "YOUR TOKEN HERE" 
headers = {
    "Authorization": "Bearer %s" % token,
}

rain = False
degree = 0

def get_weather_for_the_day():
	f = urllib2.urlopen('WEATHER URL HERE')
	json_string = f.read()
	parsed_json = json.loads(json_string)
	degree = parsed_json['currently']['apparentTemperature']
	degree = float(degree)
	rainfall = parsed_json['daily']['data'][0]['precipProbability']
	rainfall = float(rainfall)
	if rainfall > 0:
		rain = True
	f.close()
	return degree, rain

def color_based_on_weather(degree, rain):
    if degree >= 80:
        color = 'red'
    elif degree >= 70:
        color = 'orange'
    elif degree >= 60:
        color = 'white'
    elif degree >= 53:
        color = 'blue'
    else:
        color = 'purple'
    print(degree)
    print(color)
    return color

def on():
	print "Turning on - " + time.strftime("%Y-%m-%d %H:%M")
	degree, rain = get_weather_for_the_day()
	color = color_based_on_weather(degree, rain)

	payload = {
	    "power": "on",
	    "color": color,
	    "brightness": 1.0,
	    "duration": 10,
	}
	response = requests.put('https://api.lifx.com/v1/lights/all/state', data=payload, headers=headers)

	if(rain):
		print "Raining today"
		for x in range(0, 94):
			data = {
			    "period": 4,
			    "cycles": 15,
			    "color": "hue:300 saturation:1.0 brightness:0.3",
			}
			response = requests.post('https://api.lifx.com/v1/lights/all/effects/breathe', data=data, headers=headers)
			time.sleep(60)
	
def off():
	print "Turning off - " + time.strftime("%Y-%m-%d %H:%M")
	print "\n"
	response = requests.post('https://api.lifx.com/v1/lights/all/toggle', headers=headers)

schedule.every().day.at("6:50").do(on)
schedule.every().day.at("8:25").do(off)

while True:
    schedule.run_pending()
    time.sleep(1)


