import requests
import re
from datetime import datetime, timedelta, timezone
from pprint import pprint 

class NationalWeatherService:
    """Summarize data from NWS API
    
    This module retrieves the API URL for your LONGITUDE and LATITUDE, then fetches
    weather information and returns a dictionary containing summarized weather
    data for the specified number of hours.

    Required:
        latitude - Degrees of latitude as a float (e.g., 38.8894)
        longitude - Degrees of longitude as a float (e.g., -77.0352)
        user_agent - Requirement of National Weather Service. String which uniquely
                     identifies your application and contains contact information.

    Optional:
        forecast_hours - Period of future time over which to summarize conditions.
                         For twice-daily watering, 12 hours is reasonable.
        api_server - Defaults to primary NWS server.
    
    NWS API documentation can be located at: 
    https://www.weather.gov/documentation/services-web-api
    """

    def __init__(self, latitude=38.8894,
                       longitude=-77.0352,
                       user_agent="myweatherapp.com, contact@myweatherapp.com",
                       forecast_hours=12,
                       api_server="https://api.weather.gov",
                       debug=False):

        self.latitude = latitude
        self.longitude = longitude
        self.forecast_hours = forecast_hours # Number of hours to summarize forecast
        self.api_server= api_server
        self.debug = debug

        # The NWS requests a unique string in the 'User-Agent' header
        self.headers = {'User-Agent': user_agent}


        # Get API endpoint for my longitude and latitude
# TODO: this sometimes returns a response such as below. Maybe add a retry on
# error or on 'status':500
#{
#    'correlationId': '494c5834',
#    'title': 'Unexpected Problem', 
#    'type': 'https://api.weather.gov/problems/UnexpectedProblem', 
#    'status': 500, 
#    'detail': 'An unexpected problem has occurred.', 
#    'instance': 'https://api.weather.gov/requests/494c5834'
#}
        r = requests.get(self.api_server + \
                         "/points/"  + \
                         str(self.latitude) + "," + \
                         str(self.longitude), headers=self.headers).json()
        self.api = r['properties']['forecastGridData']


    def fetch(self):
        # Get the forecast for my grid
        r = requests.get(self.api, headers=self.headers).json()
        
        
        # The following properties are useful
        properties = ["probabilityOfPrecipitation",
                      "quantitativePrecipitation", 
                      "relativeHumidity",
                      "skyCover",
                      "temperature",
                      "windSpeed",
                      "windGust"]
        
        
        # Parse the "validTime" string into "time" and "duration" properties
        # to make this easier to deal with than the native format is.
        # Example "validTime" in the response: "2021-05-27T04:00:00+00:00/PT1H"
        # which is the date followed by the string "/PT1H" indicating 1 hour duration.
        for p in properties:
            for v in r['properties'][p]['values']:
                fields = re.split("/", v['validTime'])
                v['time'] = datetime.strptime(fields[0], "%Y-%m-%dT%H:%M:%S%z")
                v['duration'] = int(re.search("[0-9]+", fields[1]).group())
        
        
        # Function to sum the value and duration over upcoming period of time
        # later, if you want the total (ie, for precipitation) just use the sum.
        # or if you want the average you can divide accum_value/accum_duration
        def accumulate_over_period(property, period):
            accum_value = 0
            accum_duration = 0
            accum_value_times_duration = 0
            for v in r['properties'][property]['values']:
                # if the timestamp is between the present time and present+period
                if datetime.now(timezone.utc) <= \
                   v['time'] <= \
                   datetime.now(timezone.utc) + timedelta(hours=period):
                    accum_value += v['value']
                    accum_duration += v['duration']
                    accum_value_times_duration += v['value'] * v['duration']
            return accum_value, accum_duration, accum_value_times_duration
        
        
        # Summarize properties over FORECAST_HOURS
        summary = {}
        
        v, d, vd = accumulate_over_period('probabilityOfPrecipitation', self.forecast_hours)
        summary['ave_probability_of_precipitation'] = 0 if d==0 else round(vd/d, 2)
        
        v, d, vd = accumulate_over_period('quantitativePrecipitation', self.forecast_hours)
        summary['total_precipitation'] = round(v, 2)
        
        v, d, vd = accumulate_over_period('relativeHumidity', self.forecast_hours)
        summary['ave_relative_humidity'] = 0 if d==0 else round(vd/d, 2)
        
        v, d, vd = accumulate_over_period('skyCover', self.forecast_hours)
        summary['ave_sky_cover'] = 0 if d==0 else round(vd/d, 2)
        
        v, d, vd = accumulate_over_period('temperature', self.forecast_hours)
        summary['ave_temperature'] = 0 if d==0 else round(vd/d, 2)
        
        v, d, vd = accumulate_over_period('windSpeed', self.forecast_hours)
        summary['ave_wind_speed'] = 0 if d==0 else round(vd/d, 2)
        
        v, d, vd = accumulate_over_period('windGust', self.forecast_hours)
        summary['ave_wind_gust'] = 0 if d==0 else round(vd/d, 2)
        
        if self.debug: pprint(summary)
    
        return summary


if __name__ == "__main__":
    weather = NationalWeatherService()
    pprint(weather.fetch())
