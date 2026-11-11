import adafruit_ina219


class INA219:
    def __init__(self, i2c="", addr=""):
        self._sensor = adafruit_ina219.INA219(i2c, addr) 
  
    def get_current(self):  
        current = self._sensor.current / 1000
        return current
    
    def get_voltage(self):     
        voltage = self._sensor.bus_voltage
        return voltage
    
    def get_shunt_voltage(self):     
        shut_voltage = self._sensor.shunt_voltage / 1000
        return shut_voltage