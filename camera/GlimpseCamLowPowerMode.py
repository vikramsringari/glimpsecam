#!/usr/bin/env python

import time, datetime, os, glob, socket, tinys3, threading, socket
from shutil import copyfile
import RPi.GPIO as GPIO
import subprocess as sub

access = ''
secret = ''

held = False
prevState = False

conn = tinys3.Connection(access, secret, tls=True, default_bucket = 'pi-1')

copyfile('/home/pi/newFiles.txt','/home/pi/FilesToUpload.txt')
with open('/home/pi/FilesToUpload.txt') as f:
	content = [x.strip() for x in f]
	open('/home/pi/newFiles.txt', 'w').close()

class NoWiFiException(Exception):
	pass

def __upload(file):
	type = file[-4:]
	filename = os.path.basename(file)
	with open(file, 'rb') as f:
		try:
			if sub.check_output(['hostname','-I']).isspace():
				raise NoWiFiException()
			conn.upload(socket.gethostname() + '/' + ('images' if (type == '.jpg') else 'videos') + '/' + filename, f)
			print 'successful upload'
		except:
			with open('/home/pi/newFiles.txt','a') as newfile:
				newfile.write(file+'\n')
			print 'wrote '+file+' to newFiles.txt'

#Motor vibrates for 3 seconds upon entering LPM
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(5, GPIO.OUT)
GPIO.output(5, GPIO.HIGH)
time.sleep(3)
GPIO.output(5, GPIO.LOW)

#Waiting for button hold
while True:
	currentState = not GPIO.input(12)
	if (currentState and not prevState):
		held = True
		endtime = time.time() + 5
		time.sleep(0.01)
		while time.time() < endtime:
			if (not currentState):
				held = False
			currentState = not GPIO.input(12)
		if held: #Exits LPM
			GPIO.output(5, GPIO.HIGH)
			time.sleep(1)
			GPIO.output(5, GPIO.LOW)
			GPIO.cleanup()
			sub.call('python ./glimpsecam/camera/GlimpseCam.py &', shell=True)
			sub.call('pkill -f ./glimpsecam/camera/GlimpseCamLowPowerMode.py', shell=True)
	time.sleep(0.01)
	prevState = currentState
	if content:
		threading.Thread(target=__upload, args=[content.pop(0)]).start()
	#INSERT BACKLOG UPLOADING HERE LATER

