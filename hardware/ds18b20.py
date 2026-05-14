from glob import glob


class DS18B20:
    def __init__(self):
        return
    
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
        