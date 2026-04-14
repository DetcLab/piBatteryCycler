import board
import busio

from .bq25157 import BQ25157
from .ads1115 import ADC
from .mcp4725 import DAC

ADDR_BQ = 0x6a
ADDR_ADC = 0x48
ADDR_DAC = 0x60

i2c = busio.I2C(board.SCL, board.SDA)

class BatteryCycler:
    def __init__(self):
        self.charger = BQ25157(i2c, ADDR_BQ)
        self.meter = ADC(i2c, ADDR_ADC)
        self.load = DAC(i2c, ADDR_DAC)