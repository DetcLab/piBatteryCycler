import adafruit_mcp4725

#################### QUITAR EN PRODUCCION ###########
import RPi.GPIO as GPIO

RELE = 17  # GPIO17

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELE, GPIO.OUT)
#######################################################

class DAC:
    def __init__(self, i2c="", addr=""):
        self._dac = adafruit_mcp4725.MCP4725(i2c, address=addr)

    def set_iload(self, iload):
        out = int((iload * 4095) / 2000)
        self._dac.raw_value = out
        return
 
 
 ######### QUITAR EN PRODUCCION ########################   
    def rele(self, value):
        if value:
            GPIO.output(RELE, GPIO.HIGH)
        else:
            GPIO.output(RELE, GPIO.LOW)

        return
#########################################################