# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 11:45:42 2018

@author: Caihao.Cui
"""
from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import time
import json
import os
import web3
import time
import board
import neopixel
from threading import Thread
from web3.auto import w3
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

# get the webcam:
cap = cv2.VideoCapture(-1)

cap.set(3,1024)
cap.set(4,768)
#160.0 x 120.0
#176.0 x 144.0
#320.0 x 240.0
#352.0 x 288.0
#640.0 x 480.0
#1024.0 x 768.0
#1280.0 x 1024.0

# cap.set(cv2.CAP_PROP_FPS,30)
time.sleep(2)


class MyThread(Thread):
    def run(self):
        ret, frame = cap.read()

addresses = {}
threads = []


## neopixel
# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 24

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False,
                           pixel_order=ORDER)

def decode(im) :
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)
    return decodedObjects


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
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


def scanned(wait):
    pixels.fill((0, 255, 0))
    pixels.show()
    time.sleep(wait)
    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(1)

def pulse_color(color, pix):
    pix.fill(color)
    pix.show()


white = (0,0,0)
ret, frame = cap.read()
while(cap.isOpened()):
    # Capture frame-by-frame
    thread = MyThread()
    thread.start()
    threads.append(thread)
    # ret, frame = cap.read()
    # Our operations on the frame come here
    im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    print(cap.get(5))
    decodedObjects = decode(im)
    white = ((white[0]+10) %255, (white[1]+10) %255, (white[2]+10) %255)


    # pixels.fill(white)
    # pixels.show()

    for decodedObject in decodedObjects:
        my_json = decodedObject.data.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        if data["id"] not in addresses.keys():
            scanned(1)
            print('Type : ', decodedObject.type)
            addresses[data["id"]]= True
            rainbow_cycle(.005)


    # Display the resulting frame
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key & 0xFF == ord('s'): # wait for 's' key to save
        cv2.imwrite('Capture.png', frame)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
