from glob import glob

########################################################################
########################################################################
# Clase DS18B20
########################################################################
########################################################################
class DS18B20:
    def __init__(self):
        return

########################################################################
# Metodo: Externo
# Función: Busca id sensor instalado y devuelve temperatura
# Retorna:  Temperatura en ªC
########################################################################  
    def get_temperature(self):
        try:            
            base = glob('/sys/bus/w1/devices/28-*')[0]
            with open(base + '/w1_slave') as f:
                 lines = f.readlines()
            temp_line = lines[1]
            temp = float(temp_line.split('t=')[1]) / 1000
            return temp
        
        except:
            return False
