# -*- coding: utf-8 -*-
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import time
import json
import os
import time
import busio
import board
import neopixel
import adafruit_bme280
from dlt_helpers import *

# get the webcam:
cap = cv2.VideoCapture(0)

cap.set(3,1024)
cap.set(4,768)

# Address that have been scanned
addresses = {}

## Neopixel Set Up
# Choose an open pin connected to the Data In of the NeoPixel strip
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18
# The number of NeoPixels
num_pixels = 24
# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False,
                           pixel_order=ORDER)

# BME280 Sensor
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c,0x76)

def decode(im) :
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)
    return decodedObjects

clear_lights(pixels,(0,0,0))

#Start Camera Cycle
n = 0
while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    print(cap.get(5))
    decodedObjects = decode(im)


    for decodedObject in decodedObjects:
        my_json = decodedObject.data.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        if data["id"] not in addresses.keys():
            m_rainbow_cycle(pixels, .005,1)
            addresses[data["id"]] = n
            env= get_environment(bme280)
            print(env)
            circle(pixels, .01,(0,255,0))
        elif data["id"] in addresses.keys() :
            print( n , addresses[data["id"]])
            if n - addresses[data["id"]] > 3:
                scanned(pixels, .25, 2)
                clear_lights(pixels,(0,0,0))

        n = n + 1
    # Display the resulting frame
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key & 0xFF == ord('s'): # wait for 's' key to save
        cv2.imwrite('Capture.png', frame)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
