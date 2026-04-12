import board
import busio
from .bq25157 import BQ25157

i2c = busio.I2C(board.SCL, board.SDA)

class BatteryCycler:
    def __init__(self):
        self.charger = BQ25157(i2c)
        self.meter = "ADC(i2c)"
        self.load = "DAC(i2c)"