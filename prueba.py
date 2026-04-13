from hardware import BatteryCycler
import time 

bc = BatteryCycler()

print(bc.charger.set_ilimit(800))
print(bc.charger.set_vlow(3.7))
print(bc.charger.set_vreg(4.44))
print(bc.charger.set_ichg(850))
print(bc.charger.set_iterm(100))
print(bc.charger.set_vdpm(4.44))
print(bc.charger.set_safety(4.38, 950))
    