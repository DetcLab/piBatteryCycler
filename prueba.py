from hardware import Ciclador
import time 

c = Ciclador()


c.config_carga.iload = 250
print(c.graba_param_carga())

c.config_cargador.ichg = 565
c.config_cargador.ilimit = 000
c.config_cargador.vreg = 4.20
c.config_cargador.lowchg = False
print(c.graba_param_cargador())


# for reg in c.lee_registros().items():
#      print(reg)

print(c.modo("reposo"))


# print(c.lee_param_cargador())
# for reg in c.lee_registros().items():
#      print(reg)

while 1:
    print(f"{c.intensidad():.3f} Amperios")
    print(f"{c.tension():.2f} Voltios")
    print(f"{c.temperatura():.1f} ºC")

    time.sleep(2)