import board
import neopixel
import time

#pixels = neopixel.NeoPixel(board.D5, 10)    # Feather wiring!
pixels = neopixel.NeoPixel(board.D18, 10) # Raspberry Pi wiring!

while 1:

      pixels[1] = (255, 0, 0)
      time.sleep(2)
      pixels[1] = (0,0,0)
      time.sleep(2)
