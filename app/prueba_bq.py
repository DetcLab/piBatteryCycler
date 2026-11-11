import board
import busio
import time

from firmware.bq25157 import BQ25157


ADDR_BQ  = 0x6a # Dirección I2C cargador

i2c = busio.I2C(board.SCL, board.SDA)

bq = BQ25157(i2c, ADDR_BQ)

bq.set_ilimit(0)
bq.set_vlow(3.7)
bq.set_ichg(550)
bq.enable_lowchg(False)
bq.set_vreg(4.2)
bq.enable_iterm(False)


print(bq.read_config())

print(bq.enable_charger(True))
print(bq.read_bytes_raw())

time.sleep(0.1)

print(bq.status())



