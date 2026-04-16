# from hardware import Ciclador
# import time


# c = Ciclador()


# print(c.lee_param_cargador())

# for reg in c.lee_registros().items():
#      print(reg)

# #c.config_cargador.isafe = 1250
# #c.config_cargador.vsafe = 4.2
# c.config_cargador.ichg = 750
# c.config_cargador.ilimit = 000


# print("\n")
# print(c.graba_param_cargador())

# for reg in c.lee_registros().items():
#      print(reg)


# print(c.modo("descarga"))















# import board
# import busio
# import time
# from hardware.bq25157 import BQ25157

# ADDR_BQ = 0x6a


# i2c = busio.I2C(board.SCL, board.SDA)

# bq = BQ25157(i2c, ADDR_BQ)

# bq.reset()

# print(bq.read_config())
# for reg in bq.read_bytes_raw().items():
#      print(reg)



# bq.config.ichg = 1250
# bq.config.lowchg = False
# bq.config.ilimit = 500
# bq.config.iterm = 250
# bq.write_config()



# print("\n")
# print(bq.read_config())
# for reg in bq.read_bytes_raw().items():
#      print(reg)

# bq.reset()

# print("\n")
# print(bq.read_config())
# for reg in bq.read_bytes_raw().items():
#      print(reg)





























from hardware import Ciclador
import time 

c = Ciclador()

c.config_carga.iload=1005
c.graba_param_carga()

c.config_cargador.ichg = 650
c.config_cargador.ilimit = 000
c.config_cargador.vreg = 4.20
c.config_cargador.lowchg = False
c.graba_param_cargador()

print(c.lee_param_cargador())
for reg in c.lee_registros().items():
     print(reg)

print(c.modo("reposo"))

c.bq25.reset()

print(c.lee_param_cargador())
for reg in c.lee_registros().items():
     print(reg)

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
