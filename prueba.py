from hardware import BatteryCycler
import time 

bc = BatteryCycler()


print(bc.charger.set_ilimit(550))
print(bc.charger.set_vlow(3.8))
print(bc.charger.set_vreg(4.20))
print(bc.charger.set_ichg(650))
print(bc.charger.set_iterm(200))
print(bc.charger.set_vdpm(4.20))
print(bc.charger.set_safety(4.20, 950))
print(bc.charger.enable_charger(True))
print(bc.charger.enable_iterm(False))
print(bc.charger.enable_lowchg(False))
for reg in bc.charger.get_bytes_raw().items():
    print(reg)

#print(bc.charger.reset())

print(bc.charger.get_status())
print(bc.charger.get_config())

print(f"{bc.meter.get_current():.3f} Amperios")
print(f"{bc.meter.get_voltage():.2f} Voltios")
print(f"{bc.meter.get_temperature():.1f} ºC")

bc.load.set_iload(1000)
bc.load.rele(False)