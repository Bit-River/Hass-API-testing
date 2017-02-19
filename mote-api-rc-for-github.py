#!/usr/bin/env python

from colorsys import hsv_to_rgb, rgb_to_hsv
from sys import exit
import time
import random
#import MoteEffects

try:
    from flask import Flask, jsonify, make_response, abort, request
except ImportError:
    exit("This script requires the flask module\nInstall with: sudo pip install flask")

from mote import Mote


## Create app, Mote instance
app = Flask(__name__)
mote = Mote()

## Optional Security Measure to Restrict IP access
# @app.before_request
# def limit_remote_addr():
#     if request.remote_addr != 'Allowed IP':
#         abort(403)  # Forbidden


## Configure Mote channels for 4x 16 pixel strips
mote.configure_channel(1, 16, False)
mote.configure_channel(2, 16, False)
mote.configure_channel(3, 16, False)
mote.configure_channel(4, 16, False)

# Define baseurl and current API version
baseurl = "/mote/api/"
version = "v1.0"

## Default status to initialise with - all channels off, white, full brightness
status = {'state': {1: 0, 2: 0, 3: 0, 4: 0},
          'colour': {1: [255, 255, 255], 2: [255, 255, 255], 3: [255, 255, 255], 4: [255, 255, 255]},
          'brightness': {1: 255, 2: 255, 3: 255, 4: 255}
         }


## Converts a hex colour like FF0000 to an RGB colour like 255, 0, 0 (red)
def hex_to_rgb(value):
    value = value.lstrip('#')
    length = len(value)
    return tuple(int(value[i:i + length / 3], 16) for i in range(0, length, length / 3))

## Turns Mote on, with the currently set colours and states for each channel
def mote_on(status):
    for chan in range(4):
        r, g, b = status['colour'][chan + 1]
        for pixel in range(16):
            if not status['state'][chan + 1] == 0:
                mote.set_pixel(chan + 1, pixel, r, g, b)
            else:
                mote.set_pixel(chan + 1, pixel, 0, 0, 0)
    mote.show()
    return True

## Turns Mote off
def mote_off(status):
    for chan in range(1,5,1):
        if status['state'][chan] == 0:
            for pixel in range(16):
                    mote.set_pixel(chan, pixel, 0, 0, 0)
    mote.show()
    return True


## Mote Effect - Larson Loop
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
## colour - Light Effect Colour in hex
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
def larson(ch_selection,direction,colour,pause_time,persist,loop):
    r, g, b = hex_to_rgb(colour)
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
            if persist == 0:
                mote.clear()

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
            if persist == 0:
                mote.clear()


## Larson Swipe Call, Mote Sticks Changed Sequentially
## Altered Meaning to ch_selection, Stick Order is used
## '4300' - The 4th Stick, and then the 3rd
##
def larson_sequence(ch_sequence,direction,colour,pause_time,persist,loop):
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
            larson(ch_selection,direction,colour,pause_time,persist,1)


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


## Returns, in JSON, the state of the given channel, or all channels
@app.route(baseurl + version + '/channel/<string:channel>/state', methods=['GET'])
def get_state(channel):
    global status
    for chan in range(1, 5):
        for pixel in range(16):
            if mote.get_pixel(chan, pixel) != (0, 0, 0):
                status['state'][chan] = 1
            else:
                status['state'][chan] = 0
        col = mote.get_pixel(chan, 0)
        br = rgb_to_hsv(*col)[2]
        status['colour'][chan] = list(col)
        status['brightness'][chan] = br
    if channel == 'all':
        return jsonify(status)
    else:
        channel_status = {}
        for k in status:
            channel_status[k] = {int(channel): status[k][int(channel)]}
        return jsonify(channel_status)


## Sets all channels, or a given channel, "on" or "off"
@app.route(baseurl + version + '/channel/<string:channel>/state/<string:st>', methods=['GET'])
def set_state(channel, st):
    global status
    if st == 'on':
        if channel == 'all':
            for chan in range(1, 5):
                status['state'][chan] = 1
        else:
            status['state'][int(channel)] = 1
        mote_on(status)
    elif st == 'off':
        if channel == 'all':
            for chan in range(1, 5):
                status['state'][chan] = 0
        else:
            status['state'][int(channel)] = 0
        mote_off(status)
    return jsonify(status)


## Sets the brightness for a channel or all channels, by converting to HSV,
## modifying the V, and then converting back to RGB, and setting that colour
@app.route(baseurl + version + '/channel/<string:channel>/brightness/<string:br>', methods=['GET'])
def set_brightness(channel, br):
    global status
    if channel == 'all':
        for ch in status['colour']:
            c = status['colour'][ch]
            r, g, b = c
            h, s, v = rgb_to_hsv(r, g, b)
            v = int(br) / 100.0
            r, g, b = [int(c * 255) for c in hsv_to_rgb(h, s, v)]
            status['colour'][ch] = [r, g, b]
        if not all(status['state'].values()) == 0:
            mote_on(status)
    else:
        c = status['colour'][int(channel)]
        r, g, b = c
        h, s, v = rgb_to_hsv(r, g, b)
        v = int(br) / 100.0
        r, g, b = [int(c * 255) for c in hsv_to_rgb(h, s, v)]
        status['colour'][int(channel)] = [r, g, b]
        if not status['state'][int(channel)] == 0:
            mote_on(status)
    return jsonify(status)


## Returns the currently set colours for a specific channel or all channels
@app.route(baseurl + version + '/channel/<string:channel>/colour', methods=['GET'])
def get_colour(channel):
    global status
    if channel == 'all':
        return jsonify(status['colour'])
    else:
        return jsonify({channel: status['colour'][int(channel)]})

## Sets a colour for a specific channel or all channels
@app.route(baseurl + version + '/channel/<string:channel>/colour/<string:c>', methods=['GET'])
def set_colour(channel, c):
    global status
    if channel == 'all':
        for ch in status['colour']:
            status['colour'][ch] = hex_to_rgb(c)
        if not all(status['state'].values()) == 0:
            mote_on(status)
    else:
        status['colour'][int(channel)] = hex_to_rgb(c)
        if not status['state'][int(channel)] == 0:
            mote_on(status)
    return jsonify(status)


## General Larson Loop Call, All Motes Sticks Changed at the Same time
## e.g. /larsonloop/1004/1/00ff00/0.1/0/7
@app.route(baseurl + version + '/larsonloop/<string:ch_selection>/<int:direction>/<string:colour>/<float:pause_time>/<int:persist>/<int:repeat>', methods=['GET'])
def larsonloop(ch_selection,direction,colour,pause_time,persist,repeat):
    larson(ch_selection,direction,colour,pause_time,persist,repeat)
    get_state('all')
    return jsonify(status)


@app.route(baseurl + version + '/larsonloop_rgb/<string:ch_selection>/<int:direction>/<int:r>/<int:g>/<int:b>/<float:pause_time>/<int:persist>/<int:repeat>', methods=['GET'])
def larsonloop_rgb(ch_selection,direction,r,g,b,pause_time,persist,repeat):
    larson_rgb(ch_selection,direction,r,g,b,pause_time,persist,repeat)
    get_state('all')
    return jsonify(status)

## Larson Swipe Call, Mote Sticks Changed Sequentially
## Altered Meaning to ch_selection, Stick Order is used
## '4300' - The 4th Stick, and then the 3rd
## e.g. /larsonloop/1300/1/00ff00/0.1/0/2
@app.route(baseurl + version + '/larsonswipe/<string:ch_sequence>/<int:direction>/<string:colour>/<float:pause_time>/<int:persist>/<int:repeat>', methods=['GET'])
def larsonswipe(ch_sequence,direction,colour,pause_time,persist,repeat):
    larson_sequence(ch_sequence,direction,colour,pause_time,persist,repeat)
    get_state('all')
    return jsonify(status)

@app.route(baseurl + version + '/larsonswipe_rgb/<string:ch_sequence>/<int:direction>/<int:r>/<int:g>/<int:b>/<float:pause_time>/<int:persist>/<int:repeat>', methods=['GET'])
def larsonswipe_rgb(ch_sequence,direction,r,g,b,pause_time,persist,repeat):
    larson_sequence_rgb(ch_sequence,direction,r,g,b,pause_time,persist,repeat)
    get_state('all')
    return jsonify(status)

## Cylon (aka Larson Scanner), e.g. /cylon/0230/1/f0ff00/0.1/1/3
@app.route(baseurl + version + '/cylon/<string:ch_selection>/<int:direction>/<string:colour>/<float:pause_time>/<int:persist>/<int:repeat>', methods=['GET'])
def cylon(ch_selection,direction,colour,pause_time,persist,repeat):
    for i in range(repeat):
        larson(ch_selection,direction,colour,pause_time,0,1)
        larson(ch_selection,1 - direction,colour,pause_time,0,1)
    get_state('all')
    return jsonify(status)

@app.route(baseurl + version + '/cylon_rgb/<string:ch_selection>/<int:direction>/<int:r>/<int:g>/<int:b>/<float:pause_time>/<int:persist>/<int:repeat>', methods=['GET'])
def cylon_rgb(ch_selection,direction,r,g,b,pause_time,persist,repeat):
    for i in range(repeat):
        larson_rgb(ch_selection,direction,r,g,b,pause_time,0,1)
        larson_rgb(ch_selection,1 - direction,r,g,b,pause_time,0,1)
    get_state('all')
    return jsonify(status)

## Bounce Colour Wash, e.g. /bouncewash/1234/1/f0ffff/0.1/1/4
@app.route(baseurl + version + '/bouncewash/<string:ch_selection>/<int:direction>/<string:colour>/<float:pause_time>/<int:persist>/<int:repeat>', methods=['GET'])
def bouncewash(ch_selection,direction,colour,pause_time,persist,repeat):
    for i in range(repeat):
        larson(ch_selection,1 - direction,colour,pause_time,0,1)
        larson(ch_selection,direction,colour,pause_time,1,1)
    get_state('all')
    return jsonify(status)

@app.route(baseurl + version + '/bouncewash_rgb/<string:ch_selection>/<int:direction>/<int:r>/<int:g>/<int:b>/<float:pause_time>/<int:persist>/<int:repeat>', methods=['GET'])
def bouncewash_rgb(ch_selection,direction,r,g,b,pause_time,persist,repeat):
    for i in range(repeat):
        larson_rgb(ch_selection,1 - direction,r,g,b,pause_time,0,1)
        larson_rgb(ch_selection,direction,r,g,b,pause_time,1,1)
    get_state('all')
    return jsonify(status)


## Rainbow / Spectrum
@app.route(baseurl + version + '/rainbow', methods=['GET'])
def rainbow():
    global colour
    h = time.time() * 50
    for channel in range(0,16,1):

        for i in range(15,-1,-1):
            hue = (h + (channel * 64) + (i * 2)) % 360
            r, g, b = [int(c * 255) for c in hsv_to_rgb(hue/360.0, 1.0, 1.0)]
            mote.set_pixel(1, i, r, g, b)
            mote.set_pixel(2, i, r, g, b)
            mote.set_pixel(3, i, r, g, b)
            mote.set_pixel(4, i, r, g, b)

            mote.show()
            time.sleep(0.07)

    get_state('all')
    return jsonify(status)

## Tiedye Effect (needs work, too much purple & white)
@app.route(baseurl + version + '/tiedye', methods=['GET'])
def tiedye():
    global colour
    for i in range (120):
        h = time.time() * 150

        for channel in range(10):

            for pixel in range(16):
                hue = (h + (channel * 64) + (pixel * 4)) % 360
                r, g, b = [int(c * 255) for c in hsv_to_rgb(hue/360.0, hue/180, hue/90)]
                mote.set_pixel(1, pixel, r, g, b)
                mote.set_pixel(2, pixel, r, g, b)
                mote.set_pixel(3, pixel, r, g, b)
                mote.set_pixel(4, pixel, r, g, b)

        mote.show()
        time.sleep(random.uniform(0.01,0.12))

    get_state('all')
    return jsonify(status)


## Returns the current API version to the requester
@app.route(baseurl, methods=['GET'])
def get_version():
    return jsonify({'mote-api-version': version})

## Catches page not found errors, returns 404
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    mote_off(status)
    app.run(host='0.0.0.0', debug=True)
