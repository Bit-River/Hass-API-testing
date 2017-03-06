#!/usr/bin/env python
from flask import Flask, jsonify, make_response, abort, request
from energenie import switch_on, switch_off

app = Flask(__name__)

global ener_one_status
global ener_two_status


## Optional Security Measure to restrict API to IP
#@app.before_request
#def limit_remote_addr():
#    if request.remote_addr != 'allowed IP address':
#        abort(403)  # Forbidden

@app.route('/api/lamp/<int:lamp>/<int:toggle>', methods=['GET'])
def lamp(lamp,toggle):
    global ener_one_status
    global ener_two_status

    if lamp == 1 and toggle == 1:
            switch_on(1)
            ener_one_status = 1
    elif lamp == 1 and toggle == 0:
            switch_off(1)
            ener_one_status = 0
    elif lamp == 2 and toggle == 1:
            switch_on(2)
            ener_two_status = 1
    elif lamp == 2 and toggle == 0:
            switch_off(2)
            ener_two_status = 0
    elif lamp == 3 and toggle == 1:
            switch_on(1)
            switch_on(2)
            ener_one_status = 1
            ener_two_status = 1
    elif lamp == 3 and toggle == 0:
            switch_off(1)
            switch_off(2)
            ener_one_status = 0
            ener_two_status = 0
    return ("Ener One: " + str(ener_one_status) + ", Ener Two: " + str(ener_two_status))

@app.route('/api/ener_lamp/<int:lamp_choice>', methods=['GET'])
def ener_status(lamp_choice):
    global ener_one_status
    global ener_two_status

    if lamp_choice == 1:
            return (str(ener_one_status))
    elif lamp_choice == 2:
            return (str(ener_two_status))
    elif lamp_choice == 3 and ener_one_status == 1 and ener_two_status == 1:
            return ("1")
    else:
            return ("0")

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
