import board
import busio
import time

from .bq25157 import BQ25157
from .ina219 import INA219
from .mcp4725 import DAC
from .led_soc import LedSoc
from .ds18b20 import DS18B20

########################################################################
# Direcciones I2C dispositivos e inicializacion de este
########################################################################
ADDR_BQ  = 0x6a # Dirección I2C cargador
ADDR_DAC = 0x60 # Direccíon I2C convertidor DAC
ADDR_INA = 0x40 # Dirección I2C INA219

i2c = busio.I2C(board.SCL, board.SDA)

########################################################################
########################################################################
# Clase Ciclador
########################################################################
########################################################################
class Ciclador:
    def __init__(self):
        self.bq25 = BQ25157(i2c, ADDR_BQ)
        self.ina = INA219(i2c, ADDR_INA)
        self.load = DAC(i2c, ADDR_DAC)    
        self.led = LedSoc(0.1)
        self.config_cargador = self.bq25.config
        self.config_cargador_defecto = self.bq25.config_default
        self.config_carga = self.load.config
        self.temp = DS18B20()

########################################################################
# Metodo: Externo 
# Función: Graba los parametros pasados para el cargador
# Retorna:  Los parametros configurados
########################################################################   
    def graba_param_cargador(self):
        self.bq25.write_config()
        return self.config_cargador

########################################################################
# Metodo: Externo 
# Función: Graba los parametros pasados para la carga electronica
# Retorna:  Los parametros configurados
######################################################################## 
    def graba_param_carga(self):
        self.load.write_config()
        return self.config_carga

########################################################################
# Metodo: Externo 
# Función: Lee los registros del bq24157
# Retorna:  Devuelve la configuracion de los registros
######################################################################## 
    def lee_registros(self):
        return self.bq25.read_bytes_raw()

########################################################################
# Metodo: Externo 
# Función: Resetea los registros del bq24157
# Retorna:  Devuelve la configuracion despues del reseteo
######################################################################## 
    def reset(self):
        self.bq25.reset()
        return self.config_cargador

########################################################################
# Metodo: Externo 
# Función: Devuelve las opciones preestablecidad de V_reg
# Retorna:  Opciones de tensión
######################################################################## 
    def opciones_vreg(self):
        opciones = self.bq25.config_vreg()
        return opciones

########################################################################
# Metodo: Externo 
# Función: Devuelve las opciones preestablecidad de Intensidad de carga
# Retorna:  Opciones
########################################################################   
    def opciones_ichg(self):
        opciones = self.bq25.config_ichg()
        return opciones

########################################################################
# Metodo: Externo 
# Función: Devuelve las opciones preestablecidad de Tension corte
# Retorna:  Opciones
######################################################################## 
    def opciones_voff(self):
        opciones = self.load.config_voff()
        return opciones

########################################################################
# Metodo: Externo 
# Función: Devuelve las opciones preestablecidad de Intensidad de descarga
# Retorna:  Opciones
######################################################################## 
    def opciones_iload(self):
        opciones = self.load.config_iload()
        return opciones

########################################################################
# Metodo: Externo 
# Función: Establece el modo del ciclador
# Recibe: "reposo" - "carga" - "descarga"
# Retorna:  Opcion escogida
######################################################################## 
    def modo(self, modo=""): # modo carga | descarga | reposo
        
        if modo == "paro":
            self.bq25.enable_charger(False)
            self.load.enable_load(False)
            self.led.soc_green()
            return "paro"
        
        elif modo == "carga":
            self.load.enable_load(False)
            time.sleep(1)
            self.bq25.enable_lowchg(False)
            self.bq25.enable_charger(True)
            self.bq25.enable_iterm(True)
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
   
########################################################################
# Metodo: Externo 
# Función: Lee el valor de tension de la bateria
# Retorna:  Tension leida
########################################################################  
    def tension(self):
        tension = self.ina.get_voltage()
        return tension

########################################################################
# Metodo: Externo 
# Función: Lee el valor de intensidad de carga (+) descarga (-)
# Retorna:  Intensidad leida
########################################################################  
    def intensidad(self):
        intensidad = self.ina.get_current()
        return intensidad

########################################################################
# Metodo: Externo 
# Función: Lee el valor de temperatura de la bateria
# Retorna:  Temperatura leida
########################################################################  
    def temperatura(self):
        temperatura = self.temp.get_temperature()
        return temperatura
