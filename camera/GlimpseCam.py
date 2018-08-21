#!/usr/bin/env python

import time, datetime, os, glob, socket
import RPi.GPIO as GPIO
import subprocess as sub
import imageEnhance as iE
import renameFile as rF

currentState = False
prevState = False
picture = True
filename = "file.wav"
held = False

with open("./glimpsecam/camera/numFile.txt") as numFile:
	int_list = [int(i) for i in numFile.readline().split()]

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
GPIO.setup(5, GPIO.HIGH)
time.sleep(1)
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
				GPIO.output(5, GPIO.HIGH)
				time.sleep(1)
				GPIO.output(5, GPIO.LOW)
				GPIO.cleanup()
				sub.call('python ./glimpsecam/camera/GlimpseCamLowPowerMode.py &', shell=True)
				sub.call('pkill -f ./pikrellcam/pikrellcam', shell=True)
				sub.call('sudo ifconfig wlan0 down', shell=True)
				sub.call('pkill -f ./glimpsecam/camera/GlimpseCam.py', shell=True)
		if picture:
			sub.call('echo "still" > /home/pi/pikrellcam/www/FIFO', shell=True)
			time.sleep(1)
			filename = rF.rename('/home/pi/pikrellcam/www/media/stills',int_list[0])
			iE.simpleImageEnhance(filename, filename)
			int_list[0] -= 1
			time.sleep(0.01)
		else:
			sub.call('echo "record on 5 5" > /home/pi/pikrellcam/www/FIFO', shell=True)
			time.sleep(10)
			filename = rF.rename('/home/pi/pikrellcam/www/media/videos',int_list[1])
			int_list[1] -= 1
			time.sleep(0.01)
		Upath = socket.gethostname() + '/' + ('images' if picture else 'videos') + '/'
		with open("UploadTimes.txt","a") as file:
			start_time = time.time()
			sub.call('aws s3 cp ' + filename + ' s3://pi-1/' + Upath, shell=True)
			file.write("AWS : "+("Picture" if picture else "Video")+" uploaded in %s seconds on " % (time.time() - start_time) + time.strftime("%Y/%m/%d at %H:%M\n"))
			#start_time = time.time()
			#sub.call('/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload ' + filename + ' /' + Upath, sub.call)
			#file.write("DB  : "+("Picture" if picture else "Video")+" uplaoded in %s seconds on " % (time.time() - start_time) + time.strftime("%Y/%m/%d at %H:%M\n"))
		with open("./glimpsecam/camera/numFile.txt","w") as numFile:
			numFile.write(str(int_list[0]) + ' ' + str(int_list[1]))
	time.sleep(0.01)
	prevState = currentState
