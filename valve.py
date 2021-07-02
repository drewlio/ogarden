import gpiozero
from gpiozero.pins.mock import MockFactory
from datetime import datetime
from time import sleep


class Valve:
    """Solenoid valve controlled through relay board

    Valve is wired with "high side switching" and "low side switching". 
    That is, both 24VAC lines are switched on/off with one relay each.

    Control lines are active-low pull-downs.

    Inputs:
     relay1_pin:     Default 17
     relay2_pin:     Default 27
     active_high:    Default: False. Pulling line low energizes the relay.
     mock_on_fail:   Default: True. If GPIO pins don't exist, automatically mock.
     debug:          Default: False. Outputs debugging messages.

    All timing delays are blocking.

    """


    def __init__(self, 
                 relay1_pin=17, 
                 relay2_pin=27, 
                 active_high=False,
                 mock_on_fail=True,
                 debug=False):
        self.debug = debug
        try:
            self.relay1 = gpiozero.DigitalOutputDevice(relay1_pin, active_high=active_high)
            self.relay2 = gpiozero.DigitalOutputDevice(relay2_pin, active_high=active_high)
        except:
            if self.debug: print(f"{datetime.now()} | GPIO error. Trying mock pin factory.")
            gpiozero.Device.pin_factory = MockFactory()
            self.relay1 = gpiozero.DigitalOutputDevice(relay1_pin, active_high=active_high)
            self.relay2 = gpiozero.DigitalOutputDevice(relay2_pin, active_high=active_high)


    def off(self):
        """Immediately turns the valve off.
        """
        self.__off()


    def on(self, duration=None):
        """Immediately turns the valve on.
        
        duration:   Leaves valve on and exits if duration is unspecified or None.
                    Otherwise, blocks for duration seconds and then turns off the valve.
        """
        self.__on()

        if duration is not None:
            if self.debug: print(f"{datetime.now()} | Watering for {duration} seconds")
            sleep(duration)
            self.off()


    def __off(self):
        if self.debug: print(f"{datetime.now()} | Turning the valve off")
        self.relay1.off()
        self.relay2.off()


    def __on(self):
        if self.debug: print(f"{datetime.now()} | Turning the valve on")
        self.relay1.on()
        self.relay2.on()

    def timer(self, duration):
        """Convenience function for readability"""
        self.on(duration=duration)        


if __name__ == "__main__":
    v = Valve(debug=True)
    v.on(duration=20*60)
