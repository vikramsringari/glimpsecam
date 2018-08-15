#!/usr/bin/env python

import time, datetime, os, glob, socket
import RPi.GPIO as GPIO
import subprocess as sub
import imageEnhance as iE
import renameFile as rF


held = False
currentState = False
prevState = False
picture = True
filename = "file.wav"
held = False

with open("./glimpsecam/camera/numFile.txt") as numFile:
	int_list = [int(i) for i in numFile.readline().split()]

sub.call('kill -- -1',shell=True)
sub.call('/home/pi/pikrellcam/pikrellcam &',shell=True)

#BOOT TEST GOES HERE
print ("running camera test")
sub.call('echo "still" > /home/pi/pikrellcam/www/FIFO',shell=True)
time.sleep(1)
filename = rF.rename('/home/pi/pikrellcam/www/media/stills', 0)
time.sleep(30)
filepath = 's3://pi-1/' + socket.gethostname() + '/images/' + filename
sub.call('aws s3 ls ' + filepath,shell=True)
if [[ $? -ne 0 ]]:
	echo "image file was not uploaded correctly"
	#INSERT HAPTIC FEEDBACK HERE
#IT IF REACHES HERE IT PASSED CAMERA
print ("running video test")
sub.call('echo "record on 5 5" > /home/pi/pikrellcam/www/FIFO',shell=True)
time.sleep(10)
filename = rF.rename('/home/pi/pikrellcam/www/media/videos', 0)
time.sleep(60)
filepath = 's3://pi-1/' + socket.gethostname() + '/videos/' + filename
sub.call('aws s3 ls ' + filepath,shell=True')
if [[ $? -ne 0 ]]:
	echo "video file was not uploaded correctly"
	#INSERT HAPTIC FEEDBACK HERE

#BACK TO RUNNING
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
<<<<<<< HEAD
		if held:
=======
		if (held):
>>>>>>> 13b5bb0a2ef0570c2f67e532c015816847b6eb2e
			endtime = time.time() + 4
			while time.time() < endtime:
				if (not currentState):
					held = False
<<<<<<< HEAD
			if held:
				GPIO.cleanup()
				sub.call('python ./glimpsecam/camera/GlimpseCamLowPowerMode.py &', shell=True)
				sub.call('pkill -f ./pikrellcam/pikrellcam', shell=True)
				sub.call('sudo ifconfig wlan0 down', shell=True)
				sub.call('pkill -f ./glimpsecam/camera/GlimpseCam.py', shell=True)
=======
			if (held):
				sub.call('GlimpseCamLowPowerMode.py',shell=True)
>>>>>>> 13b5bb0a2ef0570c2f67e532c015816847b6eb2e
		if picture:
			sub.call('echo "still" > /home/pi/pikrellcam/www/FIFO')
			time.sleep(1)
			filename = rF.rename('/home/pi/pikrellcam/www/media/stills',int_list[0])
			iE.simpleImageEnhance(filename, filename)
			int_list[0] -= 1
			time.sleep(0.01)
		else:
			sub.call('echo "record on 5 5" > /home/pi/pikrellcam/www/FIFO')
			time.sleep(10)
			filename = rF.rename('/home/pi/pikrellcam/www/media/videos',int_list[1])
			int_list[1] -= 1
			time.sleep(0.01)
		Upath = socket.gethostname() + '/' + ('images' if picture else 'videos') + '/'
		with open("UploadTimes.txt","a") as file:
			start_time = time.time()
			sub.call('aws s3 cp ' + filename + ' s3://pi-1/' + Upath)
			file.write("AWS : "+("Picture" if picture else "Video")+" uploaded in %s seconds on " % (time.time() - start_time) + time.strftime("%Y/%m/%d at %H:%M\n"))
			start_time = time.time()
			sub.call('/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload ' + filename + ' /' + Upath)
			file.write("DB  : "+("Picture" if picture else "Video")+" uplaoded in %s seconds on " % (time.time() - start_time) + time.strftime("%Y/%m/%d at %H:%M\n"))
		with open("./glimpsecam/camera/numFile.txt","w") as numFile:
			numFile.write(str(int_list[0]) + ' ' + str(int_list[1]))
	time.sleep(0.01)
	prevState = currentState
	
	
	
finally:                   # this block will run no matter how the program exits  
    GPIO.cleanup()  
