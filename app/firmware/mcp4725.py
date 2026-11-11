import adafruit_mcp4725

###########################################################################################
# Ajuste del perfil de configuración por defecto 
# al crear la clase
###########################################################################################
ILOAD = 150
VOFF  = 3.20

########################################################################
# Valores de intensidad de descarga predefinidos
########################################################################
ILOAD_VAL = [50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,
             1000,1050,1100,1150,1200,1250,1300,1350,1400,1450,1500,1550,1600,1650,1700,
             1750,1800,1850,1900,1950,2000]

########################################################################
# Valores de tensión de corte predefinidos
########################################################################
VOFF_VAL = [2.80,2.90,3.00,3.10,3.20,3.40,3.50]

########################################################################
# Clase Configuracion parametros carga electronica
########################################################################
class ConfigLoad:
    def __init__(self, iload, voff):
        self.iload = iload
        self.voff  = voff
        
    def __repr__(self):
        return f"{self.__class__.__name__} | (ILOAD: {self.iload}, (VOFF: {self.voff}))"

########################################################################
########################################################################
# Clase MCP4725
########################################################################
########################################################################
class DAC:
    def __init__(self, i2c="", addr=""):
        self._dac = adafruit_mcp4725.MCP4725(i2c, address=addr)
        self.config = ConfigLoad(iload = ILOAD, voff = VOFF)
    
########################################################################
# Metodo:  Externo
# Función: Graba los parametros por defecto de la carga electronica
# Retorna: Valor configurado
########################################################################
    def write_config(self):
        if self.config.iload > 2000:
            self.config.iload = 2000

        elif self.config.iload < 0:
            self.config.iload = 0
        return self.config.iload

########################################################################
# Metodo:  Externo
# Función: Habillita la carga electronica
# Retorna: Valor calculado a cargar en el DAC
########################################################################
    def enable_load(self, value):
        if value:
            out = int((self.config.iload * 4095) / 2000)
	        
        else:
            out = 0
        
        self._dac.raw_value = out

        return out

########################################################################
# Metodo: Externo 
# Función: Envia opciones ILOAD
# Retorna: Lista con opciones 
########################################################################  
    def config_iload(self):
        return ILOAD_VAL

########################################################################
# Metodo: Externo 
# Función: Envia opciones V-OFF
# Retorna: Lista con opciones 
########################################################################  
    def config_voff(self):
        return VOFF_VAL
