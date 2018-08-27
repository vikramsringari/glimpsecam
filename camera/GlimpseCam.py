#!/usr/bin/env python

import time, datetime, os, glob, socket
import RPi.GPIO as GPIO
import subprocess as sub

currentState = False
prevState = False
picture = True
filename = "file.wav"
held = False

sub.call('python /home/pi/glimpsecam/camera/uploadFile.py &',shell=True)
sub.call('/home/pi/pikrellcam/pikrellcam &',shell=True)
time.sleep(3)

#BOOT TEST GOES HERE

#print ("running camera test")
#sub.call('echo "still" > /home/pi/pikrellcam/www/FIFO',shell=True)
#time.sleep(1)
#filename = rF.rename('/home/pi/pikrellcam/www/media/stills', 0)
#time.sleep(30)
#filepath = 's3://pi-1/' + socket.gethostname() + '/images/' + filename
#try:
#	sub.check_output(['aws', 's3', 'ls', filepath], shell=True)
#except:
#	print 'image file was not uploaded correctly'
	#INSERT HAPTIC FEEDBACK HERE

#IF IT REACHES HERE IT PASSED CAMERA
#print ("running video test")
#sub.call('echo "record on 5 5" > /home/pi/pikrellcam/www/FIFO',shell=True)
#time.sleep(10)
#filename = rF.rename('/home/pi/pikrellcam/www/media/videos', 0)
#time.sleep(60)
#filepath = 's3://pi-1/' + socket.gethostname() + '/videos/' + filename
#try:
#	sub.check_output(['aws', 's3', 'ls', filepath], shell=True)
#except:
#	print 'video file was not uploaded correctly'
	#INSERT HAPTIC FEEDBACK HERE

#BACK TO RUNNING
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(5, GPIO.OUT)
GPIO.output(5, GPIO.HIGH)
time.sleep(0.5)
GPIO.output(5, GPIO.LOW)
time.sleep(0.5)
GPIO.output(5, GPIO.HIGH)
time.sleep(0.5)
GPIO.output(5, GPIO.LOW)

while True:
	currentState = not GPIO.input(12)
	if (currentState and not prevState):
		held = True
		picture = True
		time.sleep(0.01)
		endtime = time.time() + 1
		while time.time() < endtime:
			if (not currentState):
				held = False
			prevState = currentState
			currentState = not GPIO.input(12)
			if (currentState and not prevState):
				picture = False
				time.sleep(0.01)
				break
			prevState = currentState
			time.sleep(0.01)
		if held:
			endtime = time.time() + 4
			while time.time() < endtime:
				if (not currentState):
					held = False
			if held:
				GPIO.cleanup()
				#sub.call("kill $(ps | grep bash | awk '{print $1}')",shell=True)
				sub.call('python ./glimpsecam/camera/GlimpseCamLowPowerMode.py &', shell=True)
				sub.call('pkill -f ./pikrellcam/pikrellcam', shell=True)
				sub.call('pkill -f ./glimpsecam/camera/uploadFile.py', shell=True)
				sub.call('pkill -f ./glimpsecam/camera/GlimpseCam.py', shell=True)
		if picture:
			sub.call('echo "still" > /home/pi/pikrellcam/www/FIFO', shell=True)
			GPIO.output(5, GPIO.HIGH)
			time.sleep(0.5)
			GPIO.output(5, GPIO.LOW)
			time.sleep(1)
		else:
			sub.call('echo "record on 5 5" > /home/pi/pikrellcam/www/FIFO', shell=True)
			GPIO.output(5, GPIO.HIGH)
			time.sleep(0.25)
			GPIO.output(5, GPIO.LOW)
			time.sleep(0.25)
			GPIO.output(5, GPIO.HIGH)
			time.sleep(0.25)
			GPIO.output(5, GPIO.LOW)
			time.sleep(10)
	time.sleep(0.01)
	prevState = currentState
