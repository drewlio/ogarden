"""Soil moisture sensor

Usage:



Configuring I2C permissions on non-Raspberry Pis:
    1. Create a group for i2c permissions: "sudo groupadd i2c"
    2. Change ownership of i2c devices: "sudo chown :i2c /dev/i2c-*"
    3. Change permissions of i2c devices: "sudo chmod g+rw /dev/i2c-*"
    4. Add yourself to the i2c group: "sudo usermod -aG i2c <username>"
    5. Make it persistent across reboots with:
          $ sudo -s
          # echo 'KERNEL=="i2c-[0-9]*", GROUP="i2c"' >> /etc/udev/rules.d/10-local_i2c_group.rules

Installing SMBus2 Python Library:
    sudo pip3 install smbus2
"""

import smbus2
import warnings
from time import sleep
from pprint import pprint


class SoilMoistureSensor:
    """Soil moisture sensor class

    Keyword arguments:
    address: Hexadecimal or decimal sensor I2C address
    port:    Which SMBus/I2C port to access
    dry:     Set point for dry soil (take measurement in air)
    wet:     Set point for wet soil (take measurement in water)
    debug:   None or value. If value, SMBus errors are supressed and a mock
             response of value is returned.
    """


    def __init__(self, address=0x10, port=1, dry=11000, wet=22000, debug=None):
        """Create soil moisture sensor object
        """
        self.address = address
        self.port = port
        self.dry = dry
        self.wet = wet
        self.debug = debug

        self.response = []
        self.raw = 0
        self.percent = 0

        self.bus = smbus2.SMBus(self.port)
        sleep(0.1) # this resolves a race condition when immediately measuring


    def measure(self):
        """Perform the measurment and process the data"""

        try:
            # Read 2 bytes, starting at offset 0, from address
            self.response = self.bus.read_i2c_block_data(self.address, 0, 2)
        except:
            if self.debug:
                # If debug exists, we will pretend this came from the sensor
                # and ignore any SMBus communication errors.
                # Convert the debug value from int to array of 2 bytes.
                self.response = self.debug.to_bytes(2, 'big', signed=False)
            else:
                # If an error occured and we're not in debug mode, raise error
                raise Exception("I2C sensor error")


        # Shift high byte left 8 bits, add to low byte
        self.raw = (self.response[0]<<8) + self.response[1]

        self.calculate()

        return {"sensor_value": self.percent}


    def calculate(self):
        """Calculate values based off existing raw measurement

           This is used by measure() and would otherwise only be useful
           when experimenting with dry/wet set points and want to 
           recalculate percent moisture with existing raw measurement.
        """
        # Map the raw value to a percentage in the range of dry->wet
        #    "raw-dry" is how far into the range the measurment is...
        #    divided by the whole range...
        #    times 100 to make it a percentage
        self.percent = (self.raw - self.dry) / (self.wet - self.dry) * 100

        # Clamp the min and max values to 0% and 100%
        # This is in case dry/wet are too high/low
        self.percent = 0. if self.percent < 0 else self.percent
        self.percent = 100. if self.percent > 100 else self.percent

        # Round the floating point number
        self.percent = round(self.percent, 2)


    def __str__(self):
        """Output a summary when you print the sensor object"""
        return f"Address {hex(self.address)} ({self.address}) | " + \
               f"Percent {self.percent}% | " + \
               f"Raw {self.raw} | " + \
               f"Dry {self.dry} | " + \
               f"Wet {self.wet}" 


if __name__ == "__main__":
    sensor = SoilMoistureSensor(debug=15000)
    sensor.measure()
    print(sensor)


