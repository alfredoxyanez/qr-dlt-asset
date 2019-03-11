import time
def clear_lights(pix, color=(0,0,0)):
    pix.fill(color)
    pix.show()

## NeoPixel Functions
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b)


def rainbow_cycle(pix, wait):
    num_pixels = len(pix)
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pix[i] = wheel(pixel_index & 255)
        pix.show()
        time.sleep(wait)

def m_rainbow_cycle(pix, wait, times):
    for _ in range(times):
        rainbow_cycle(pix, wait)
    pix.fill((0,0,0))
    pix.show()


def scanning(pix, wait, times):
    for _ in range(times):
        pix.fill((0, 255, 0))
        pix.show()
        time.sleep(wait)
        pix.fill((0, 0, 0))
        pix.show()
        time.sleep(wait)


def scanned(pix, wait, times):
    for _ in range(times):
        pix.fill((255, 75, 0))
        pix.show()
        time.sleep(wait)
        pix.fill((0, 0, 0))
        pix.show()
        time.sleep(wait)

def circle(pix, delay, to_color, from_color= (0,0,0)):
    num_pixels = len(pix)
    n = num_pixels
    for i in range(num_pixels):
        for j in range(n):
            if j == n-1:
                pix[j] = to_color
            elif j >0:
                pix[j] = to_color
                pix[j-1] = from_color
            else:
                pix[j] = to_color
            pix.show()
            time.sleep(delay)
        n = n-1
    time.sleep(.5)
    pix.fill(from_color)
    pix.show()
