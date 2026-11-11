import board
import neopixel
import time

########################################################################
# Configuracion leds WS2812
########################################################################
LED_COUNT = 10
LED_PIN = board.D18   # GPIO18
BRIGHTNESS = 0.1

########################################################################
########################################################################
# Clase LedSoc
########################################################################
########################################################################
class LedSoc:
    def __init__(self, bright=BRIGHTNESS):
        self.pixels = neopixel.NeoPixel(
                                        LED_PIN,
                                        LED_COUNT,
                                        brightness=bright,
                                        auto_write=False,
                                        pixel_order=neopixel.RGB)

########################################################################
# Escalera de color rojo
########################################################################                                       )
    def soc_red(self):
        for i in range(LED_COUNT):
            self.pixels[i] = (255, 0, 0)
            time.sleep(0.1)
            self.pixels.show()
        return

########################################################################
# Escalera de color verde
########################################################################   
    def soc_green(self):
        for i in range(LED_COUNT):
            self.pixels[i] = (0, 255, 0)
            time.sleep(0.1)
            self.pixels.show()
        return

########################################################################
# Escalera de color azul
########################################################################   
    def soc_blue(self):
        for i in range(LED_COUNT):
            self.pixels[i] = (0, 0, 255)
            time.sleep(0.1)
            self.pixels.show()
        return

########################################################################
# Apagado completo
########################################################################   
    def soc_off(self):
        for i in range(LED_COUNT):
            self.pixels[i] = (0, 0, 0)
            time.sleep(0.1)
            self.pixels.show()
        return


