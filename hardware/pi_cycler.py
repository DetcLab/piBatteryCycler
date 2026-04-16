import board
import busio
import time

from .bq25157 import BQ25157
from .ads1115 import ADC
from .mcp4725 import DAC
from .led_soc import LedSoc

ADDR_BQ = 0x6a
ADDR_ADC = 0x48
ADDR_DAC = 0x60

i2c = busio.I2C(board.SCL, board.SDA)
              
class Ciclador:
    def __init__(self):
        self.bq25 = BQ25157(i2c, ADDR_BQ)
        self.adc = ADC(i2c, ADDR_ADC)
        self.load = DAC(i2c, ADDR_DAC)    
        self.led = LedSoc(0.1)
        self.config_cargador = self.bq25.config
        self.config_carga = self.load.config
     

    def configura_defecto(sefl):
        pass

    def graba_param_cargador(self):
        self.bq25.write_config()
        return self.config_cargador
    
    def graba_param_carga(self):
        self.load.write_config(self.config_carga.iload)
        return self.config_carga
    
    def lee_registros(self):
        return self.bq25.read_bytes_raw()
    
    def reset(self):
        self.bq25.reset()
        return self.config_cargador




























    def modo(self, modo=""): # modo carga | descarga | reposo
        
        if modo == "reposo":
            self.bq25.enable_charger(False)
            self.load.enable_load(False)
            self.led.soc_green()
            return "reposo"
        
        elif modo == "carga":
            self.load.enable_load(False)
            time.sleep(1)
            self.bq25.enable_lowchg(False)
            self.bq25.enable_charger(True)
            self.led.soc_blue()
            return "carga"
        
        elif modo == "descarga":
            self.bq25.enable_charger(False)
            time.sleep(1)
            self.load.enable_load(True)
            self.led.soc_red()
            return "descarga"

        else:
            return False
   




 
    
    def tension(self):
        tension = self.adc.get_voltage()
        return tension
    
    def temperatura(self):
        temperatura = self.adc.get_temperature()
        return temperatura

    def intensidad(self):
        intensidad = self.adc.get_current()
        return intensidad