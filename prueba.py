from hardware.bq25157 import BQ25157

import board
import busio
import time


ADDR_BQ = 0x6a


i2c = busio.I2C(board.SCL, board.SDA)

bq = BQ25157(i2c, ADDR_BQ)

bq.reset()

print(bq.read_config())
for reg in bq.read_bytes_raw().items():
     print(reg)



bq.config.ichg = 1250
bq.config.lowchg = False
bq.config.ilimit = 500
bq.config.iterm = 250
bq.write_config()



print("\n")
print(bq.read_config())
for reg in bq.read_bytes_raw().items():
     print(reg)

bq.reset()

print("\n")
print(bq.read_config())
for reg in bq.read_bytes_raw().items():
     print(reg)





























# from hardware import Ciclador
# import time 

# c = Ciclador()

# c.config_load.iload=1005
# c.config_carga()

# c.config_charge.ichg = 650
# c.config_charge.ilimit = 000
# c.config_charge.vreg = 4.20
# c.config_charge.lowchg = False

# # c.bq25.set_ichg(650)
# # c.bq25.set_ilimit(000)
# # c.bq25.set_vreg(4.20)
# # c.bq25.enable_lowchg(False)

# print(c.modo("reposo"))

# while 1:
#     print(f"{c.intensidad():.2f} Amperios")
#     print(f"{c.tension():.2f} Voltios")
#     print(f"{c.temperatura():.1f} ºC")

#     time.sleep(2)
#print(f"{c.adc.get_current():.3f}")

# print(bc.charger.set_ilimit(550))
# print(bc.charger.set_vlow(3.8))
# print(bc.charger.set_vreg(4.20))
# print(bc.charger.set_ichg(650))
# print(bc.charger.set_iterm(200))
# print(bc.charger.set_vdpm(4.20))
# print(bc.charger.set_safety(4.20, 950))
# print(bc.charger.enable_iterm(False))
# print(bc.charger.enable_lowchg(False))

# print(bc.charger.enable_charger(True))



# for reg in bc.charger.get_bytes_raw().items():
#     print(reg)

# #print(bc.charger.reset())

# print(bc.charger.get_status())
# print(bc.charger.get_config())



# bc.load.set_iload(1000)
# bc.load.rele(False)
