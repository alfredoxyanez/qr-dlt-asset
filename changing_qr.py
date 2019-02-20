import json
import time
import psutil
import qrcode
from tkinter import *
from datetime import datetime

def changing_qr():
    """Generates QR code that changes in respect to time.

    Args:


    Returns:
        type: Description of returned object.

    """
    img = qrcode.make("start")
    while True:
        random_data = str(datetime.utcnow())

        js  = json.dumps(random_data)
        img = qrcode.make(js)

        img.show()
        time.sleep(5)

        # main = Tk()
        # camelot = Canvas(main, width = 400, height = 300)
        # camelot.grid(row = 0, column = 0, rowspan = 11, columnspan = 3)
        #
        # camelot.create_image(0, 0, anchor = NW, image = img)






if __name__ == "__main__":
    changing_qr()
