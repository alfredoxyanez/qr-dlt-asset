import board
import neopixel
import time



pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 24

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False,
                           pixel_order=ORDER)
def circle(delay, to_color, from_color= (0,0,0)):
    n = num_pixels
    for i in range(num_pixels):
        for j in range(n):
            if j == n-1:
                pixels[j] = to_color
            elif j >0:
                pixels[j] = to_color
                pixels[j-1] = from_color
            else:
                pixels[j] = to_color
            pixels.show()
            time.sleep(delay)
        n = n-1
    time.sleep(1)
    pixels.fill(from_color)

circle(.01,(255,0,0))
