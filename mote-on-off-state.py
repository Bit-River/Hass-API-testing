#!/usr/bin/python3
from requests import get
response = get('http://[ MOTE IP ]:5000/mote/api/v1.0/channel/all/state')
active = response.json()['state']
if (active['1'] == 1 or active['2'] == 1 or active ['3'] or active ['4']):
    print ('on')
else:
    print ('off')
