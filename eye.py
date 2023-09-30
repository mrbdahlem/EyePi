#
# eye.py -- Spooky blinking eye
# Based on sample code by Tod Kurt - todbot.com
#

import random
import time
import board
import busio
import displayio
import adafruit_imageload
import gc9a01

# display settings
WIDTH = 240
HEIGHT = 240
ROTATION = 180
FLIPPED = random.choice([True, False])

# map the eye position to file names
# prepare image with ImageMagick like:
# convert input.jpg -resize 240x240 -type palette BMP3:output.bmp
img_filenames = {
    "closed": "/images/closedsm.bmp",
    "open": "/images/open.bmp" ,
    "right": "/images/rightsm.bmp",
    "left": "/images/leftsm.bmp"
    }

# Release any resources currently in use for the displays
displayio.release_displays()

# attempt to auto-detect board type
import os
board_type = os.uname().machine
if 'EyePi' in board_type:
    # Raspberry Pi Pico pinout, one possibility, at "southwest" of board
    tft_clk = board.GP18 # must be a SPI CLK
    tft_mosi= board.GP19 # must be a SPI TX
    tft_rst = board.GP20
    tft_dc  = board.GP16
    tft_cs  = board.GP17
    tft_bl  = board.GP21
    spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)
    baudrate = 62500000
elif 'Pico' in board_type:
    # Raspberry Pi Pico pinout, one possibility, at "southwest" of board
    tft_clk = board.GP10 # must be a SPI CLK
    tft_mosi= board.GP11 # must be a SPI TX
    tft_rst = board.GP12
    tft_dc  = board.GP8
    tft_cs  = board.GP9
    tft_bl  = board.GP13
    spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)
    baudrate = 62500000
else:
    print("ERROR: Unknown board!")
    
# Make the displayio SPI bus and the GC9A01 display
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst, baudrate=baudrate)
display = gc9a01.GC9A01(display_bus, width=WIDTH, height=HEIGHT, rotation=ROTATION, backlight_pin=tft_bl, auto_refresh=True, brightness=1.0) #  

def blink(group):
    # display the closed eye
    main.append(closed_eye)
    # display.refresh()

    # wait a random fraction of a second before removing the closed eye
    time.sleep(random.random())
    main.pop()
    # display.refresh()

openPic = adafruit_imageload.load(img_filenames["open"])
closedPic = adafruit_imageload.load(img_filenames["closed"])

# Get the image and pallet from the closed eye and prepare to display when blinking
closed_bitmap, closed_palette = closedPic
closed_palette.make_transparent(254)
closed_eye = displayio.TileGrid(closed_bitmap, pixel_shader=closed_palette, x=int((WIDTH-closed_bitmap.width)/2), y=int((HEIGHT-closed_bitmap.height)/2))
closed_eye.flip_x = FLIPPED

# Make the main display context to show the default (open) eye
main = displayio.Group()
display.show(main)

# display the opened eye
open_bitmap, open_palette = openPic
open_eye = displayio.TileGrid(open_bitmap, pixel_shader=open_palette)
open_eye.flip_x = FLIPPED
main.append(open_eye)

# Blink randomly
while True:
    blink(main);
    time.sleep((random.random() * 8) + 2)
    
main.pop()  # remove image
