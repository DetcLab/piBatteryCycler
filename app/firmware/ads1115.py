from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15

K_VOLTAGE = 0.4
K_TEMPERATURE = 100

class ADC:
    def __init__(self, i2c="", addr=""):
        self._ads = ADS1115(i2c, address=addr)
        self._chan0 = AnalogIn(self._ads, ads1x15.Pin.A0)
        self._chan1 = AnalogIn(self._ads, ads1x15.Pin.A1)
        self._chan2 = AnalogIn(self._ads, ads1x15.Pin.A2)
        
    def get_current(self):  
        current = self._chan0.voltage
        return current
    
    def get_voltage(self):     
        voltage = (self._chan1.voltage) / K_VOLTAGE
        return voltage
    
    def get_temperature(self):  
        temperature = (self._chan2.voltage) * K_TEMPERATURE
        return temperature