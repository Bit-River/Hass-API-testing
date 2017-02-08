from colorsys import hsv_to_rgb, rgb_to_hsv
from mote import Mote
from flask import Flask, jsonify, make_response
import time
import random

app = Flask(__name__)
mote = Mote()

mote.configure_channel(1, 16, True)
mote.configure_channel(2, 16, True)

#colour = 'FF9900'
#status = 1

global colour
global status

colour = 'FF9900'
status = 1

for channel in range(2):
    for pixel in range(16):
        if mote.get_pixel(channel + 1, pixel) != (0, 0, 0):
                status = 1
        elif mote.get_pixel(channel + 1, pixel) == (0, 0, 0):
                status = 0
#        return status


def hex_to_rgb(value):
    value = value.lstrip('#')
    length = len(value)
    return tuple(int(value[i:i + length / 3], 16) for i in range(0, length, length / 3))

def mote_on(c):
#    mote.clear()
    mote.show()
    r, g, b = hex_to_rgb(c)
    for channel in range(2):
        for pixel in range(16):
            mote.set_pixel(channel + 1, pixel, r, g, b)
    mote.show()
    return True

def mote_off():
    mote.clear()
    mote.show()
    return True

def get_status():
#    global status
    for channel in range(2):
        for pixel in range(16):
            if mote.get_pixel(channel + 1, pixel) != (0, 0, 0):
                status = 1
            elif mote.get_pixel(channel + 1, pixel) == (0, 0, 0):
                status = 0
    return status


@app.route('/mote/api/v1.0/<string:st>', methods=['GET'])
def set_status(st):
    global status, colour
    if st == 'on':
        status = 1
        mote_on(colour)
    elif st == 'off':
        status = 0
        mote_off()
    elif st == 'status':
        status = get_status()
    return jsonify({'status': status, 'colour': colour})

@app.route('/mote/api/v1.0/set', methods=['GET'])
def get_colour():
    global colour
    return jsonify({'status': status, 'colour': colour})

@app.route('/mote/api/v1.0/set/<string:c>', methods=['GET'])
def set_colour(c):
    global status, colour
    colour = c
    if status == 0:
        mote_on(colour)
        mote.show()
        status = 1
    elif status == 1:
        mote_on(colour)
        mote.show()
        status = 1
    return jsonify({'status': status, 'colour': colour})

@app.route('/mote/api/v1.0/lamp', methods=['GET'])
def get_state():
    global state
    if status == 1:
        state = 1
    elif status == 0:
        state = 0
    return jsonify(state)

@app.route('/mote/api/v1.0/cylon', methods=['GET'])
def cylon():


    for cy in range (1):

        for i in range(0,16,1):
            mote.clear()
            mote.set_pixel(1,i,250,0,0)
            mote.show()
            time.sleep(0.1)

        for i in range(15,-1,-1):
            mote.set_pixel(2,i,250,0,0)
            mote.show()
            time.sleep(0.1)
            mote.clear()

        for i in range(0,16,1):
            mote.set_pixel(2,i,250,0,0)
            mote.show()
            time.sleep(0.1)
            mote.clear()

        for i in range(15,-1,-1):
            mote.set_pixel(1,i,250,0,0)
            mote.show()
            time.sleep(0.1)
            mote.clear()

    for i in range(0,16,1):
        mote.set_pixel(2,i,255,153,0)
        mote.show()
        time.sleep(0.1)

    for i in range(15,-1,-1):
        mote.set_pixel(1,i,255,153,0)
        mote.show()
        time.sleep(0.1)

    state = 1
    status = get_status()
    return ()

    

@app.route('/mote/api/v1.0/cylon2', methods=['GET'])
def cylon2():

    for cylon_double in range (2):

        for i in range(0,16,1):
            mote.set_pixel(1,i,250,0,0)
            mote.set_pixel(2,i,250,0,0)
            mote.show()
            time.sleep(0.1)
            mote.clear()

        for i in range(15,-1,-1):

            mote.set_pixel(1,i,250,0,0)
            mote.set_pixel(2,i,250,0,0)
            mote.show()
            time.sleep(0.1)
            mote.clear()

    time.sleep(0.01)

    for i in range(0,16,1):
            mote.clear()
            mote.set_pixel(1,i,255,153,0)
            mote.set_pixel(2,i,255,153,0)
            mote.show()
            time.sleep(0.1)

    for i in range(15,-1,-1):
            mote.set_pixel(1,i,255,153,0)
            mote.set_pixel(2,i,255,153,0)
            mote.show()
            time.sleep(0.1)

    state = 1
    status = get_status()
    return ()

@app.route('/mote/api/v1.0/yelon', methods=['GET'])
def yelon():

    for i in range(15,-1,-1):
        mote.clear()
        mote.set_pixel(1,i,200,102,0)
        mote.set_pixel(2,i,200,102,0)
        mote.show()
        time.sleep(0.08)

    for i in range(0,16,1):
        mote.set_pixel(1,i,200,102,0)
        mote.set_pixel(2,i,200,102,0)
        mote.show()
        time.sleep(0.1)


    state = 1
    status = get_status()
    return ()

@app.route('/mote/api/v1.0/yeloff', methods=['GET'])
def yeloff():

    for i in range(0,16,1):
        mote.set_pixel(1,i,0,0,0)
        mote.show()
        time.sleep(0.1)

    for i in range(15,-1,-1):
        mote.set_pixel(2,i,0,0,0)
        mote.show()
        time.sleep(0.1)

    state = 0
    status = get_status()
    return ()


@app.route('/mote/api/v1.0/rainbow', methods=['GET'])
def rainbow():

    h = time.time() * 50

    for channel in range(0,16,1):

        for i in range(15,-1,-1):
            hue = (h + (channel * 64) + (i * 2)) % 360
            r, g, b = [int(c * 255) for c in hsv_to_rgb(hue/360.0, 1.0, 1.0)]
            mote.set_pixel(1, i, r, g, b)
            mote.set_pixel(2, i, r, g, b)
            mote.show()
            time.sleep(0.07)

    for i in range(0,16,1):
        mote.set_pixel(1,i,255,153,0)
        mote.set_pixel(2,i,255,153,0)
        mote.show()
        time.sleep(0.1)

    for i in range(15,-1,-1):
        mote.set_pixel(1,i,255,153,0)
        mote.set_pixel(2,i,255,153,0)
        mote.show()
        time.sleep(0.1)

    state = 1
    status = get_status()
    return ()


@app.route('/mote/api/v1.0/tiedye', methods=['GET'])
def tiedye():

    mote.clear()

    for i in range (60):

        h = time.time() * 50

        for channel in range(3):

            for pixel in range(16):

                hue = (h + (channel * 64) + (pixel * 4)) % 360
                r, g, b = [int(c * 255) for c in hsv_to_rgb(hue/360.0, hue/180, hue/90)]
                mote.set_pixel(1, pixel, r, g, b)
                mote.set_pixel(2, pixel, r, g, b)

        mote.show()
        time.sleep(random.uniform(0.080,0.12))

    for pixel in range(16):
            mote.set_pixel(1, pixel, 235, 153, 0)
            mote.set_pixel(2, pixel, 235, 153, 0)
            mote.show()
            time.sleep(0.1)

            mote.set_pixel(1, pixel, 255, 153, 0)
            mote.set_pixel(2, pixel, 255, 153, 0)
            mote.show()
            time.sleep(0.1)

    state = 1
    status = get_status()
    return ()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    mote_off()
    app.run(host='0.0.0.0', debug=True)
