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
irrigation = IrrigationModel(us_gallons=5, seconds=90, area_square_feet=70)
valve = Valve()
log = Log('log.db')


# Perform the watering
conditions = {**weather.fetch(), **sensor.measure()} # get weather and soil conditions
water = soil.calculate(**conditions) # determine how much watering is needed
duration = irrigation.millimeters_to_seconds(water) # determine how long to irrigate
valve.timer(duration) # turn on the irrigation for a specified period of time


# Log the results
log.add({**conditions,
         "water_amount": water,
         "valve_duration": duration})


