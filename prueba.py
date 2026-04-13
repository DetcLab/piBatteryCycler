from hardware import BatteryCycler

bc = BatteryCycler()

print(f"{bc.charger.lee(0x01):08b}")
bc.charger.escribe(0x01, 0xFF)
print(f"{bc.charger.lee(0x01):08b}")