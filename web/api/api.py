import sys
import time
from flask import Flask, request
from dotenv import dotenv_values
import random
from collections import OrderedDict

# Location of project root
PROJECT_ROOT = "../.."

# Add the directory containing the Python application modules to the path
sys.path.append(PROJECT_ROOT)

# remaining imports now that we can reach our project modules
from soil_moisture_sensor import SoilMoistureSensor
from log import Log
from valve import Valve


# load .env configuration from project root
config = dotenv_values(PROJECT_ROOT + "/.env")


# define Flask server object
app = Flask(__name__, static_folder="../build", static_url_path="/")


# define Ogarden objects
sensor = SoilMoistureSensor(debug=15000)
log = Log(PROJECT_ROOT + "/" + config['LOG'])
valve = Valve()


# define routes (API endpoints)
@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/time')
def api_time():
    return {'time': time.time()}


@app.route('/api/sensor')
def api_sensor():
    return sensor.measure()


@app.route('/api/random')
def api_random():
    digits = int(request.args.get('round') or 2)
    return {'random': str(round(100 * random.random(), digits))}


@app.route('/api/log')
def api_log():
    """Returns the log as a JSON object, limited by limit parameter
    (e.g. http://localhost/api/log?limit=50)
    """
    num = int(request.args.get('limit') or 60)

    # the log returns a list of JSON objects, but must be a single JSON object 
    lst = log.tail(num)

    # create OrderedDict to preserve time order of elements
    # since each log entry must have a top-level key in the wrapper JSON object
    # that will be the isodatetime value, which also remains inside the object
    od = OrderedDict()
    for d in lst:
        od[d['isodatetime']] = d

    return od 


@app.route('/api/valve/on')
def api_valve_on():
    valve.on()
    return {'isValveOn': True}


@app.route('/api/valve/off')
def api_valve_off():
    valve.off()
    return {'isValveOn': False}


@app.route('/api/valve')
def api_valve_status():
    return {'isValveOn': True} if valve.status() else {'isValveOn': False}

