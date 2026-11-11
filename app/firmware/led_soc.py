import board
import neopixel
import time

# Configuración
LED_COUNT = 10
LED_PIN = board.D18   # GPIO18
BRIGHTNESS = 0.1


class LedSoc:
    def __init__(self, bright=BRIGHTNESS):
        self.pixels = neopixel.NeoPixel(
                                        LED_PIN,
                                        LED_COUNT,
                                        brightness=bright,
                                        auto_write=False,
                                        pixel_order=neopixel.RGB
                                       )
    def soc_red(self):
        for i in range(LED_COUNT):
            self.pixels[i] = (255, 0, 0)
            time.sleep(0.1)
            self.pixels.show()
        return

    def soc_green(self):
        for i in range(LED_COUNT):
            self.pixels[i] = (0, 255, 0)
            time.sleep(0.1)
            self.pixels.show()
        return
    
    def soc_blue(self):
        for i in range(LED_COUNT):
            self.pixels[i] = (0, 0, 255)
            time.sleep(0.1)
            self.pixels.show()
        return
    
    def soc_off(self):
        for i in range(LED_COUNT):
            self.pixels[i] = (0, 0, 0)
            time.sleep(0.1)
            self.pixels.show()
        return


