from hardware import BatteryCycler

bc = BatteryCycler()

print(f"{bc.charge.lee(0x01):08b}")
bc.charge.escribe(0x01, 0xFF)
print(f"{bc.charge.lee(0x01):08b}")
