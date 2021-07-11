"""

"""

class IrrigationModel:
    """Irrigation model class

    Must provide one flow rate value and one area value. 
    For flow rate you must provide one of:
        1. liters
        2. us_gallons
    and you must provide the time in seconds. 

    For instance, if you fill a 5 US gallon bucket from your irrigation system 
    in 90 seconds, provide: 
        us_gallons=5, seconds=90

    If you know your flow rate (e.g., 1.2 liters per second), provide:
        liters=1.2, seconds=1

    If both liters AND US gallons are provided, liters are used.

    Provide the area of your garden in square feet or meters:
        1. area_square_meters
        2. area_square_feet
    """

    def __init__(self, liters=None,
                       us_gallons=None,
                       seconds=None,
                       area_square_meters=None,
                       area_square_feet=None
                       ):
        assert liters or us_gallons, \
               "Provide one of liters or us_gallons to calculate flow rate"

        assert seconds, "Provide a time in seconds to calculate flow rate"

        assert area_square_meters or \
               area_square_feet, \
               "Provide one area value"
        
        # Conversions
        L_PER_USGAL = 3.78541 # Liters per US Gallon
        FT_PER_M = 3.28084    # feet per meter

        # Convert given flow rate to liters per second, with priority order
        if liters and seconds:
            self.flow_rate_liters_per_second = liters / seconds
        elif us_gallons and seconds:
            self.flow_rate_liters_per_second = us_gallons * L_PER_USGAL / seconds

        # convert given area to square meters
        self.area_square_meters = area_square_meters or \
                                  area_square_feet / FT_PER_M**2


    def millimeters_to_seconds(self, mm):
        """Convert millimeters of rainfall (uniform depth of water) to seconds of irrigation
           Inputs: 
               mm - millimeters of rainfall (uniform depth of water to be applied)

           Returns:
               Number of seconds to activate the irrigation system

        """
        #   depth (m)  x area (m^2)              x Liters/m^3  / Liters/second    [final units are seconds]
        t = (mm/1000)  * self.area_square_meters * 1000        / self.flow_rate_liters_per_second

        return round(t, 1)


# Example usage
if __name__ == "__main__":
    i = IrrigationModel(us_gallons=40.3,
                        seconds=60*60,
                        area_square_feet=70)
    print(i.millimeters_to_seconds(6))



