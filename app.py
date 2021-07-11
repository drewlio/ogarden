"""Garden watering application

This application appropriately waters a garden. Data is collected from:
    * Weather forecast from online sources
    * Soil moisture sensor measurements

For each watering session, weather and soil conditons are applied to a 
mathematical soil model to determine the additional water needed.

The amount of additional water is applied to an irrigation model to determine
the duration of watering session.

Water is applied by actuating a solenoid valve for the appropriate amount
of time.

Watering is repeated on a schedule. Soil moisture readings are collected 
continuously.
"""

from weather import NationalWeatherService
from soil_moisture_sensor import SoilMoistureSensor
import soil
from irrigation_model import IrrigationModel
from valve import Valve
from log import Log

from pprint import pprint
import json


# Set up objects
weather = NationalWeatherService(latitude=39.2155,
                                 longitude=-76.8542, 
                                 user_agent="Drew's Garden awilso29@jhu.edu");
sensor = SoilMoistureSensor(debug=15000)

# My system filled 5 US gallons in 27.5 min from 18 emitters. This works out to
# be 5gal/27.5min*(60min/hour)/18emitters=0.606 GPH per emitter. (The package
# says they are 0.65 GPH, only 6.8% difference from what I measured.)
#
# My system has 62 emitters.
# 5gal/27.5min/(60sec/min)/18emitters*62emitters*3.875L/gal = 0.0404L/sec
#
# Maybe I could just use the rate from the package:
# (0.65gal/h)*62emitters=40.3gal/hour
irrigation = IrrigationModel(us_gallons=40.3, seconds=60*60, area_square_feet=70)
valve = Valve()
log = Log('log.db')


# Perform the watering
conditions = {**weather.fetch(), **sensor.measure()} # get weather and soil conditions
water = soil.calculate(**conditions) # determine how much watering is needed
duration = irrigation.millimeters_to_seconds(water) # determine how long to irrigate
valve.timer(duration) # turn on the irrigation for a specified period of time


results = {**conditions,
           "water_amount": water,
           "valve_duration": duration}

pprint(results)

# Log the results
log.add(results)


