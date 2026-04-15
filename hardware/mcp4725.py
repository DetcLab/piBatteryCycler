import adafruit_mcp4725
from .class_config import ConfigLoad

class DAC:
    def __init__(self, i2c="", addr=""):
        self._dac = adafruit_mcp4725.MCP4725(i2c, address=addr)
        self._iload = 0

    def set_iload(self, iload):
        if iload > 2000:
            iload = 2000
        elif iload < 0:
            iload = 0
        self._iload = iload  

        return self._iload

    def enable_load(self, value):
        if value:
            out = int((self._iload * 4095) / 2000)

        else:
            out = 0
                
        self._dac.raw_value = out

        return
    
    def get_config(self):
        cfg = ConfigLoad(self._iload)
        return cfg