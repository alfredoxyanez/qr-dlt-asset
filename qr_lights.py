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
from web3.auto import w3
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

# get the webcam:
cap = cv2.VideoCapture(0)

cap.set(3,640)
cap.set(4,480)
#160.0 x 120.0
#176.0 x 144.0
#320.0 x 240.0
#352.0 x 288.0
#640.0 x 480.0
#1024.0 x 768.0
#1280.0 x 1024.0
time.sleep(2)

addresses = {}


#Load parameters
path = os.path.join(os.path.dirname(__file__),'parameters.json' )
with open(path) as f:
    parameters = json.load(f)

## Smart COntract Variables

#address
sc_address = Web3.toChecksumAddress(parameters["CONTRACT_ADDRESS"])
sc_abi = parameters["ABI"]


#Web 3 Set UP
w3 = Web3(HTTPProvider(parameters["INFURA_LINK"]))
w3.middleware_stack.inject(geth_poa_middleware, layer=0)

# Make default account
private_key = parameters["PRIVATE_KEY"]
w3.eth.defaultAccount = w3.eth.account.privateKeyToAccount(private_key)

# Get Initial Nonce
nonce = int(w3.eth.getTransactionCount(w3.eth.defaultAccount.address))



#Location of QR Scanner
LOCATION = "Narnia"


#Make instance of Smart Contract
asset_contract = w3.eth.contract(
    address=sc_address,
    abi=sc_abi
)

## neopixel
# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 24

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.RGB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False,
                           pixel_order=ORDER)



def check_in(id, nonce, location):
    """Short summary.

    Args:
        id (type): Description of parameter `id`.
        nonce (type): Description of parameter `nonce`.
        location (type): Description of parameter `location`.

    Returns:
        type: Description of returned object.

    """
    print("Sending transaction")
    deploy_txn = asset_contract.functions.checkIn(id, location, w3.eth.defaultAccount.address ).buildTransaction({
    'nonce': nonce,
    'gas': 2000000,
    'gasPrice': 2345678976543,
    })
    signed = w3.eth.account.signTransaction(deploy_txn, private_key)
    txn_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    return nonce +1

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

def white_cycle(wait):
    brightness = (0,0,0)
    for i in range(num_pixels):
        pixels[i] = brightness
    pixels.show()
    for _ in range(4):
        for i in range(num_pixels):
            brightness = ((brightness[0]+63) %255, (brightness[1]+63) %255, (brightness[2]+63) %255)
            pixels[i] = brightness
        pixels.show()
        time.sleep(wait)

def scanned(wait):
    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(wait)
    pixels.fill((0, 255, 0))
    pixels.show()
    time.sleep(wait)
    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(1)





font = cv2.FONT_HERSHEY_SIMPLEX
white = (0,0,0)
while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    decodedObjects = decode(im)
    white = ((white[0]+1) %255, (white[1]+1) %255, (white[2]+1) %255)
    pixels.fill(white)
    pixels.show()

    for decodedObject in decodedObjects:
        points = decodedObject.polygon

        # If the points do not form a quad, find convex hull
        if len(points) > 4 :
          hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
          hull = list(map(tuple, np.squeeze(hull)))
        else :
          hull = points;

        # Number of points in the convex hull
        n = len(hull)
        # Draw the convext hull
        for j in range(0,n):
          cv2.line(frame, hull[j], hull[ (j+1) % n], (255,0,0), 3)

        x = decodedObject.rect.left
        y = decodedObject.rect.top



        my_json = decodedObject.data.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        if data["id"] not in addresses.keys():
            scanned(.5)
            print('Type : ', decodedObject.type)
            addresses[data["id"]]= True
            rainbow_cycle(.001)
            # n = check_in(data["id"], nonce, LOCATION)
            # nonce = n


        barCode = str(decodedObject.data)
        cv2.putText(frame, barCode, (x, y), font, 1, (0,255,255), 2, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key & 0xFF == ord('s'): # wait for 's' key to save
        cv2.imwrite('Capture.png', frame)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
