#!/usr/bin/env python
from flask import Flask, jsonify, make_response
import subprocess, shlex

subprocess.Popen(["/home/pi/screen_on.sh"], stdout=subprocess.PIPE)

subprocess.Popen(["/home/pi/restart_browser.sh"], stdout=subprocess.PIPE)

app = Flask(__name__)

global status

def gather_status:

    args = shlex.split('export\ DISPLAY=:0\ &&\ xset\ -q\ |\ grep\ "Monitor\ is"\ |\ cut\ -c14-17')

    p = subprocess.Popen(args,shell=True, stdout=subprocess.PIPE)

    status = p.communicate()

    return status



@app.route('/api/get_status', methods=['GET'])
def get_status():

    gather_status()



@app.route('/api/screen_off', methods=['GET'])
def screen_off():

    args = shlex.split('xset\ dpms\ force\ off')

    subprocess.Popen(args,shell=True, stdout=subprocess.PIPE)

    gather_status()



@app.route('/api/screen_on', methods=['GET'])
def screen_on():

    args = shlex.split('xset\ dpms\ force\ on')

    subprocess.Popen(args,shell=True, stdout=subprocess.PIPE)

    gather_status()



@app.route('/api/restart_browser', methods=['GET'])
def restart_browser():

    p = subprocess.Popen(["/home/pi/screen_status.sh"], stdout=subprocess.PIPE)

    subprocess.Popen(["/home/pi/restart_browser.sh"], stdout=subprocess.PIPE)

    return p.communicate()



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
