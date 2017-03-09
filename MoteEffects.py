from mote import Mote
import time
import random
from colorsys import hsv_to_rgb, rgb_to_hsv

mote = Mote()

## Configure Mote channels for 4x 16 pixel strips
mote.configure_channel(1, 16, False)
mote.configure_channel(2, 16, False)
mote.configure_channel(3, 16, False)
mote.configure_channel(4, 16, False)

## Mote Effect - Larson rgb
##
## ch_selection - Mote Stick Channel Selection:
## '1234' - All Four Channels Selected
## '1204' - Channels 1, 2, and 4 Selected
## '0230' - Channels 2 and 3 Selected
##
## direction - Light Effect Direction
## 0 = Effect moves from End to USB port
## 1 = Effect moves from USB port to End
##
## Light Effect Colour in r,g,b, there are api calls for Hex
##
## pause_time - Light Effect Pause in Seconds (typical value 0.1)
##
## persist - Light Change Persistence
## 0 = Colour Change is Not Persistent, effect is a moving led light
## 1 = Colour Change is Persistent, effect is a growing wash of colour
##
## loop - Number of Loops
## 1 = Run Once (no repeat)
## 2 = Run Twice
## and so on ...
##
## Larson Sequence Call, Mote Sticks Changed Sequentially
##
## Altered Meaning to ch_selection, Stick Order is used
## '4300' - The 4th Stick, and then the 3rd
## e.g. /larsonloop/1300/1/00ff00/0.1/0/2

def larson_rgb(ch_selection,direction,r,g,b,pause_time,persist,loop):
    start = 0
    end = 16

    if direction == 0:
        start = 15
        end = -1
        direction = -1

    for i in range(loop):

        for i in range(start,end,direction):

            for c in range(4):
                if ch_selection[c] not in "0":
                    mote.set_pixel(int(ch_selection[c]),i,r,g,b)

            mote.show()
            time.sleep(pause_time)

            for c in range(4):
                if ch_selection[c] not in "0" and persist == 0:
                    mote.clear(int(c+1))

def larson_sequence_rgb(ch_sequence,direction,r,g,b,pause_time,persist,loop):
    ch_selection = "0000"
    for i in range(loop):

        for c in range(4):
            if int(ch_sequence[c]) == 1:
                ch_selection = "1000"
            elif int(ch_sequence[c]) == 2:
                ch_selection = "0200"
            elif int(ch_sequence[c]) == 3:
                ch_selection = "0030"
            elif int(ch_sequence[c]) == 4:
                ch_selection = "0004"
            elif int(ch_sequence[c]) == 0:
                ch_selection = "0000"
            larson_rgb(ch_selection,direction,r,g,b,pause_time,persist,1)

def rainbow(ch_selection):
    h = time.time() * 50
    for channel in range(0,16,1):

        for i in range(15,-1,-1):
            hue = (h + (channel * 64) + (i * 2)) % 360
            r, g, b = [int(c * 255) for c in hsv_to_rgb(hue/360.0, 1.0, 1.0)]

            for c in range(4):
                if ch_selection[c] not in "0":
                    mote.set_pixel(int(ch_selection[c]),i,r,g,b)

            mote.show()
            time.sleep(0.07)

def tiedye(ch_selection):
    for dye in range(8):

        for i in range (16):
            h = time.time() * 50

            for channel in range(30):

                for pixel in range(16):
                    hue = (h + (channel * 64) + (pixel * 4)) % 360
                    r, g, b = [int(c * 255) for c in hsv_to_rgb(hue/360.0, hue/180, hue/90)]

                    for c in range(4):
                        if ch_selection[c] not in "0":
                            mote.set_pixel(int(ch_selection[c]),i,r,g,b)

            mote.show()
            time.sleep(random.uniform(0.01,0.12))



def mote_single_led_rgb(ch_selection,led_number,r,g,b):
    for c in range(4):
        if int(ch_selection[c]) != 0:
            mote.set_pixel(int(ch_selection[c]),led_number,r,g,b)
            mote.show()
