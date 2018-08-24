import time, datetime, os, glob, socket
import RPi.GPIO as GPIO
import subprocess as sub

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(5, GPIO.OUT)
GPIO.output(5, GPIO.HIGH)
time.sleep(3)
GPIO.output(5, GPIO.LOW)

held = False
prevState = False

print 'you made it'

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
		if held:
			GPIO.output(5, GPIO.HIGH)
			time.sleep(1)
			GPIO.output(5, GPIO.LOW)
			GPIO.cleanup()
			sub.call('python ./glimpsecam/camera/GlimpseCam.py &', shell=True)
			sub.call('pkill -f ./glimpsecam/camera/GlimpseCamLowPowerMode.py', shell=True)
	time.sleep(0.01)
	prevState = currentState
	#INSERT BACKLOG UPLOADING HERE LATER
