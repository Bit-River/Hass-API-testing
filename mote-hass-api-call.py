#!/usr/bin/python3
from requests import get
import os

response = get('http://[Home Assistant IP]:8123/api/states/input_slider.mote_value_red')
r = int(float(response.json()['state']))

response = get('http://[Home Assistant IP]:8123/api/states/input_slider.mote_value_green')
g = int(float(response.json()['state']))

response = get('http://[Home Assistant IP]:8123/api/states/input_slider.mote_value_blue')
b = int(float(response.json()['state']))


response = get('http://[Home Assistant IP]:8123/api/states/input_select.mote_value_persistence')
persist = str(response.json()['state'])
if persist == "Clears as it Moves":
    persist = 0
else:
    persist = 1


response = get('http://[Home Assistant IP]:8123/api/states/input_select.mote_light_direction')
direction = str(response.json()['state'])
if direction == "To End":
    direction = 1
else:
    direction = 0


response = get('http://[Home Assistant IP]:8123/api/states/input_boolean.mote_channel_1')
channel_1 = str(response.json()['state'])
if channel_1 == "on":
    channel_1 = 1
else:
    channel_1 = 0


response = get('http://[Home Assistant IP]:8123/api/states/input_boolean.mote_channel_2')
channel_2 = str(response.json()['state'])
if channel_2 == "on":
    channel_2 = 2
else:
    channel_2 = 0



response = get('http://[Home Assistant IP]:8123/api/states/input_boolean.mote_channel_3')
channel_3 = str(response.json()['state'])
if channel_3 == "on":
    channel_3 = 3
else:
    channel_3 = 0


response = get('http://[Home Assistant IP]:8123/api/states/input_boolean.mote_channel_4')
channel_4 = str(response.json()['state'])
if channel_4 == "on":
    channel_4 = 4
else:
    channel_4 = 0


response = get('http://[Home Assistant IP]:8123/api/states/input_select.mote_device_choice')
device = str(response.json()['state'])
if device == "Stereo":
    device = "http://[mote lights IP #1]:5000/mote/api/v1.0"
elif device == "Square Circle":
    device = "http://[mote lights IP #2]:5000/mote/api/v1.0"
elif device == "Ceramic Oval":
    device = "http://[mote lights IP #3]:5000/mote/api/v1.0"


response = get('http://[Home Assistant IP]:8123/api/states/input_slider.mote_value_pause_time')
pause_time = float(response.json()['state'])


response = get('http://[Home Assistant IP]:8123/api/states/input_slider.mote_value_loop_repeats')
loop_repeats = int(float(response.json()['state']))


#response = get('http://192.168.178.40:8123/api/states/input_select.mote_effect_larson_type')
#larson_type = str(response.json()['state'])


response = get('http://[Home Assistant IP]:8123/api/states/input_select.mote_effect_classes')
mote_effect_classes = str(response.json()['state'])
if mote_effect_classes == "Larson Loop":
    mote_effect_classes = "larsonloop_rgb"
elif mote_effect_classes == "Larson Swipe":
    mote_effect_classes = "larsonswipe_rgb"
elif mote_effect_classes == "Cylon":
    mote_effect_classes = "cylon_rgb"
elif mote_effect_classes == "Bouncewash":
    mote_effect_classes = "bouncewash_rgb"
elif mote_effect_classes == "Rainbow":
    mote_effect_classes = "rainbow"
elif mote_effect_classes == "Tie dye":
    mote_effect_classes ="tiedye"


mote_stick_settings = str(channel_1) + str(channel_2) + str(channel_3) + str(channel_4)
break_slash = "/"
print (mote_effect_classes)
if mote_effect_classes == "rainbow" or mote_effect_classes == "tiedye":
    curl_string_sequence_join = (device, mote_effect_classes)
else:
    curl_string_sequence_join = (device, mote_effect_classes, str(mote_stick_settings), str(direction), str(r), str(g), str(b), str(pause_time), str(persist), str(loop_repeats))

#print "curl -s " + break_slash.join( curl_string_sequence_join )

os.system("curl -s " + break_slash.join( curl_string_sequence_join ))



#print(curl_string_sequence)



##
