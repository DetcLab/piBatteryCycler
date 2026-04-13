###########################################################################################
# Direcciones de registro del BQ25175
# El registro 06H solo puede escribirse una sola vez
###########################################################################################
ADDR_BQ25157 = 0x6a  # Dirección I2C integrado

REG_STATUS   = 0x00  # Registro de Estado y Control
REG_CONTROL  = 0x01  # Registro de Control de Carga
REG_VOLTAGE  = 0x02  # Registro de Control de Voltaje de Batería
REG_VENDOR   = 0x03  # Registro de Vendedor/Revisión (Solo lectura)
REG_CHARGE   = 0x04  # Registro de Terminación y Corriente de Carga
REG_SPECIAL  = 0x05  # Registro de Voltaje Especial y Estado de Pines
REG_SAFETY   = 0x06  # Registro de Límites de Seguridad (Escritura prioritaria)

########################################################################
# Registro: 01H | Bits: B7-B6
# Configura: Límite de Corriente de Entrada (ILIMIT)
# Valor por Defecto: 100 mA 
########################################################################
ILIMIT_VAL = {
    100:   0b00, # USB Host (100 mA) 
    500:   0b01, # USB Host (500 mA) 
    800:   0b10, # USB Host/Charger (800 mA) 
    000:   0b11  # Sin límite de entrada
}

########################################################################
# Registro: 01H | Bits: B5-B4
# Configura: Umbral de Voltaje de Batería Débil (VLOW)
# Valor por Defecto: 3.7V
########################################################################
VLOW_VAL = {
    3.4: 0b00, 
    3.5: 0b01, 
    3.6: 0b10, 
    3.7: 0b11  
}

########################################################################
# Registro: 02H | Bits: B7-B2
# Configura: Voltaje de Regulación de la Batería (VREG)
# Rango: 3.50V a 4.44V en pasos de 20mV
# Valor por Defecto: 3.54V
########################################################################
VREG_VAL = {
    3.50: 0b000000, 3.52: 0b000001, 3.54: 0b000010, 3.56: 0b000011,
    3.58: 0b000100, 3.60: 0b000101, 3.62: 0b000110, 3.64: 0b000111,
    3.66: 0b001000, 3.68: 0b001001, 3.70: 0b001010, 3.72: 0b001011,
    3.74: 0b001100, 3.76: 0b001101, 3.78: 0b001110, 3.80: 0b001111,
    3.82: 0b010000, 3.84: 0b010001, 3.86: 0b010010, 3.88: 0b010011,
    3.90: 0b010100, 3.92: 0b010101, 3.94: 0b010110, 3.96: 0b010111,
    3.98: 0b011000, 4.00: 0b011001, 4.02: 0b011010, 4.04: 0b011011,
    4.06: 0b011100, 4.08: 0b011101, 4.10: 0b011110, 4.12: 0b011111,
    4.14: 0b100000, 4.16: 0b100001, 4.18: 0b100010, 4.20: 0b100011,
    4.22: 0b100100, 4.24: 0b100101, 4.26: 0b100110, 4.28: 0b100111,
    4.30: 0b101000, 4.32: 0b101001, 4.34: 0b101010, 4.36: 0b101011,
    4.38: 0b101100, 4.40: 0b101101, 4.42: 0b101110, 4.44: 0b101111 
}

########################################################################
# Registro: 04H | Bits: B6-B4
# Configura: Corriente de Carga Rápida (ICHG)
# Basado en Rsns = 68 mΩ (Offset 550mA, pasos de 100mA)
# Valor por Defecto: 550mA
########################################################################
ICHG_VAL = {
    550:  0b000, 
    650:  0b001, 
    750:  0b010, 
    850:  0b011, 
    950:  0b100, 
    1050: 0b101, 
    1150: 0b110, 
    1250: 0b111  
}

########################################################################
# Registro: 04H | Bits: B2-B0
# Configura: Corriente de Terminación de Carga (ITERM)
# Basado en Rsns = 68 mΩ (Offset 50mA, pasos de 50mA)
# Valor por Defecto: 100mA
########################################################################
ITERM_VAL = {
    50:  0b000,
    100: 0b001, 
    150: 0b010, 
    200: 0b011, 
    250: 0b100, 
    300: 0b101, 
    350: 0b110, 
    400: 0b111 
}

########################################################################
# Registro: 05H | Bits: B2-B0
# Configura: Voltaje de Gestión de Potencia Dinámica (VIN_DPM)
# Rango: 4.20V a 4.76V en pasos de 80mV
# Valor por Defecto: 4.52V
########################################################################
VDPM_VAL = {
    4.20: 0b000, 
    4.28: 0b001,
    4.36: 0b010, 
    4.44: 0b011,
    4.52: 0b100,
    4.60: 0b101,
    4.68: 0b110,
    4.76: 0b111 
}

########################################################################
# Registro: 06H | Bits: B3-B0
# Configura: Límite de Voltaje de Seguridad (VSAFE)
# Rango: 4.20V a 4.44V en pasos de 20mV
# Valor por Defecto: 4.2V
########################################################################
VSAFE_VAL = {
    4.20: 0b0000, 4.22: 0b0001, 4.24: 0b0010, 4.26: 0b0011,
    4.28: 0b0100, 4.30: 0b0101, 4.32: 0b0110, 4.34: 0b0111,
    4.36: 0b1000, 4.38: 0b1001, 4.40: 0b1010, 4.42: 0b1011,
    4.44: 0b1100
}

########################################################################
# Registro: 06H | Bits: B7-B4
# Configura: Límite de Corriente de Seguridad (ISAFE)
# Basado en Rsns = 68 mΩ (Offset 550mA, pasos aprox. 100mA Max 1250mA)
#Valor por Defecto: 550mA
########################################################################
ISAFE_VAL = {
    550:  0b0000,
    650:  0b0001,
    750:  0b0010,
    850:  0b0011,
    950:  0b0100,
    1050: 0b0101,
    1150: 0b0110,
    1250: 0b0111
}

########################################################################
########################################################################
# Clase BQ25175
########################################################################
########################################################################
class BQ25157:
    def __init__(self, i2c="", addr=ADDR_BQ25157):
        self._i2c = i2c  
        self._addr = addr
        self._flag_safe = False  # Bandera escritura registro 06H
        self._ilimit = 100 # Intensidad limite de entrada 100mA 
        self._vlow = 3.70 
        self._vreg = 3.54
        self._ichg = 550
        self._iterm = 100
        self._vdpm = 4.52
        self._vsafe = 4.20
        self._isafe = 550

########################################################################
# Metodo: Interno 
# Función: Bloquea el puerto I2C para escribir o leer en el
# Retorna:  
########################################################################
    def _lock(self):
        while not self._i2c.try_lock():
            pass

########################################################################
# Metodo: Interno 
# Función: Desbloquea el puerto I2C una vez terminada lectura/escritura
# Retorna: 
########################################################################
    def _unlock(self):
        self._i2c.unlock()

########################################################################
# Metodo interno 
# Función: Escribe en el registro el dato recibido 
# Retorna: False (error) True (OK)
########################################################################
    def _write_byte(self, register, value):
        self._lock()
        
        try:
            self._i2c.writeto(self._addr, bytes([register, value]))
            return True
        
        except:
            return False
        
        finally:
            self._unlock()

########################################################################
# Metodo: Interno 
# Función: Lee el valor del registro recibido 
# Retorna: Byte leido, False (error)
########################################################################
    def _read_byte(self, register):
        buffer = bytearray(1)

        self._lock()
        try:
            self._i2c.writeto_then_readfrom(self._addr, 
                            bytes([register]), buffer)
        
        except:
            return False
            
        finally:
            self._unlock()

        return buffer[0]

########################################################################
# Metodo: Externo 
# Función: Configura el valor ILIMIT 
# Retorna: True (OK), False (error)
########################################################################    
