import adafruit_ina219

########################################################################
########################################################################
# Clase INA219
########################################################################
########################################################################
class INA219:
    def __init__(self, i2c="", addr=""):
        self._sensor = adafruit_ina219.INA219(i2c, addr) 

########################################################################
# Metodo: Externo
# Función: Lee el valor y sentido de la intensidad
# Retorna:  Intensidad
########################################################################
    def get_current(self):  
        current = self._sensor.current / 1000
        return current

########################################################################
# Metodo: Externo
# Función: Lee el valor de la tesnion en la bateria
# Retorna:  Tension
########################################################################  
    def get_voltage(self):     
        voltage = self._sensor.bus_voltage
        return voltage

########################################################################
# Metodo: Externo
# Función: Lee el valor de la tension en el shunt
# Retorna:  Tension 
########################################################################
    def get_shunt_voltage(self):     
        shut_voltage = self._sensor.shunt_voltage / 1000
        return shut_voltage