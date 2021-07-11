"""Simple mathematical model of soil moisture

Determines how much soil should we watered right now, given:
    - time in the season
    - weather forecast over the next number of hours
    - input from soil moisture sensor(s)

Returns
    - depth of water to apply uniformly to soil
"""

DEBUG = True

from datetime import datetime

SEASON_START_MONTH_DAY = (5, 11) # month and day of start of growing season (last frost)

# Model parameters
BASE_WATER_AMOUNT = 2.0   # session watering before adjustments (mm)
PRECIPITATION_K = 1       # scaling factor for accounting for forecasted rainfall

HUMIDITY_NOMINAL = 50     # nominal value which would require no correction (percent)
HUMIDITY_K = 0.1          # scaling factor

SKYCOVER_NOMINAL = 50     # nominal value which would require no correction (percent)
SKYCOVER_K = 0.1          # scaling factor

TEMPERATURE_NOMINAL = 20  # nominal value which would require no correction (C)
TEMPERATURE_K = 0.4       # scaling factor

WIND_NOMINAL = 7          # nominal value which would require no correction (km/h)
WIND_K = 0.1              # scaling factor

SENSOR_NOMINAL = 50       # nominal value which would require no correction (percent)
SENSOR_K = 1.0            # scaling factor

SEASON_K = 0.0016         # scaling factor


def calculate(ave_probability_of_precipitation = 0,
              ave_relative_humidity = HUMIDITY_NOMINAL,
              ave_sky_cover = SKYCOVER_NOMINAL,
              ave_temperature = TEMPERATURE_NOMINAL,
              ave_wind_gust = WIND_NOMINAL,
              ave_wind_speed = WIND_NOMINAL,
              total_precipitation = 0,
              sensor_value = SENSOR_NOMINAL,
              sensor_min = 0,
              sensor_max = 100,
              season_start = datetime(datetime.now().year, *SEASON_START_MONTH_DAY)):

    water = BASE_WATER_AMOUNT 
    if DEBUG: print(f"{water} from base amount")

    # reduce watering if soil moisture sensor indicates soil is already above nominal wetness 
    water -= (sensor_value - SENSOR_NOMINAL)/SENSOR_NOMINAL * SENSOR_K * BASE_WATER_AMOUNT
    if DEBUG: print(f"{water} after correcting for soil moisture sensor")

    # reduce watering when precipitation is in the forecast
    water -= total_precipitation * PRECIPITATION_K
    if DEBUG: print(f"{water} after correcting for precip")

    # reduce watering in high humidity
    water -= (ave_relative_humidity - HUMIDITY_NOMINAL)/HUMIDITY_NOMINAL * HUMIDITY_K * BASE_WATER_AMOUNT
    if DEBUG: print(f"{water} after correcting for humidity")

    # reduce watering for cloudy days
    water -= (ave_sky_cover - SKYCOVER_NOMINAL)/SKYCOVER_NOMINAL * SKYCOVER_K * BASE_WATER_AMOUNT
    if DEBUG: print(f"{water} after correcting for skycover")

    # increase watering on hot days
    water += (ave_temperature - TEMPERATURE_NOMINAL)/TEMPERATURE_NOMINAL * TEMPERATURE_K * BASE_WATER_AMOUNT
    if DEBUG: print(f"{water} after correcting for temperature")

    # increase watering on windy days
    wind = (ave_wind_speed + ave_wind_gust) / 2
    water += (wind - WIND_NOMINAL)/WIND_NOMINAL * WIND_K * BASE_WATER_AMOUNT
    if DEBUG: print(f"{water} after correcting for wind")

    # increase watering as the season progresses (and plants grow)
    water += (datetime.now() - season_start).days * SEASON_K * BASE_WATER_AMOUNT
    if DEBUG: print(f"{water} after correcting for season")

    # Clamp lower limit at zero just in case a correction made it go negative
    water = 0 if water<0 else water

    return round(water, 2)



if __name__ == "__main__":
    print(calculate())
