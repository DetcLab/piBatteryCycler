from hardware import BatteryCycler
import time 

bc = BatteryCycler()

print(bc.charger.set_ilimit(800))
print(bc.charger.set_vlow(3.7))
print(bc.charger.set_vreg(4.44))
print(bc.charger.set_ichg(850))
print(bc.charger.set_iterm(100))
print(bc.charger.set_vdpm(4.44))
print(bc.charger.set_safety(4.20, 950))
print(bc.charger.enable_charger(False))
print(bc.charger.enable_iterm(False))
print(bc.charger.enable_lowchg(False))
print(bc.charger.get_bytes_raw())
print(bc.charger.get_status())
print(bc.charger.reset())
print(bc.charger.get_bytes_raw())

