#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
from datetime import datetime
from time import sleep
import subprocess as sub
import os
import glob
import pexpect

GPIO.setmode(GPIO.BCM)
#GPIO.setup(26, GPIO.OUT)
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)

currentState = False
prevState = False
picture = True
countP = 0
countV = 0
shutdown = False


child = pexpect.spawn('sudo bluetoothctl')
time.sleep(1)
child.sendline('power on')
time.sleep(1)
child.sendline('discoverable on')
time.sleep(1)
child.sendline('pairable on')
time.sleep(1)
child.sendline('agent NoInputNoOutput')
time.sleep(1)
child.sendline('default-agent')
sleep(1)

sub.call(['cd pikrellcam'],shell=True)
sub.call(['pikrellcam &'],shell=True)
sub.call(['cd'],shell=True)

device = sub.check_output('hcitool con',shell=True)
device = device[20:37]
while not device:
        device = sub.check_output('hcitool con',shell=True)
        device = device[20:37]
#print 'ready'
while True:
	currentState = not GPIO.input(14)
	if (currentState and not prevState):
		#print('single press, waiting for double')
		picture = True
		time.sleep(0.1)
		endtime = time.time() + 1
		while time.time() < endtime:
                    prevState = currentState
		    currentState = not GPIO.input(14)
		    if (currentState and not prevState):
		    	#print('double press')
		    	picture = False
		    	time.sleep(0.01)
			break
		    prevState = currentState
		    time.sleep(0.01)
		if picture:
			sub.call(['echo "still" > /home/pi/pikrellcam/www/FIFO'],shell=True)
			time.sleep(1)
			list_of_stills = glob.glob('/home/pi/pikrellcam/www/media/stills/*')
			filename = max(list_of_stills, key=os.path.getctime)
			time.sleep(1)
                        sub.call(['blueman-sendto --device='+device+' '+filename], shell=True)
                        countP += 1
                        #print filename
		else:
                        sub.call(['echo "record on 5 5" > /home/pi/pikrellcam/www/FIFO'],shell=True)
                        time.sleep(7)
			time.sleep(1)
			list_of_videos = glob.glob('/home/pi/pikrellcam/www/media/videos/*')
			filename = max(list_of_videos, key=os.path.getctime)
			time.sleep(1)
                        sub.call(['blueman-sendto --device='+device+' '+filename], shell=True)
			#print filename
	time.sleep(0.1)
	prevState = currentState
