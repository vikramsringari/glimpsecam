#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import datetime
import subprocess as sub
import os
import glob
import imageEnhance as iE

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)

currentState = False
prevState = False
picture = True
filename = "file.wav"
file = open("UploadTimes.txt","a")

sub.call('/home/pi/pikrellcam/pikrellcam &',shell=True)

while True:
	currentState = not GPIO.input(12)
	if (currentState and not prevState):
		picture = True
		time.sleep(0.01)
		endtime = time.time() + 1
		while time.time() < endtime:
			prevState = currentState
			currentState = not GPIO.input(12)
			if (currentState and not prevState):
				picture = False
				time.sleep(0.01)
				break
			prevState = currentState
			time.sleep(0.01)
		if picture:
			sub.call('echo "still" > /home/pi/pikrellcam/www/FIFO',shell=True)
			time.sleep(1)
			listPictures = glob.glob('/home/pi/pikrellcam/www/media/stills/*')
			filename = max(listPictures, key=os.path.getctime)
			#name = os.path.split(filename)[1]
			iE.simpleImageEnhance(filename, filename)
			#listPictures = glob.glob('/home/pi/pikrellcam/www/media/stills/*')
			#filename = max(listPictures, key=os.path.getctime)
			time.sleep(0.01)
		else:
			sub.call('echo "record on 7 3" > /home/pi/pikrellcam/www/FIFO',shell=True)
			time.sleep(10)
			listVideos = glob.glob('/home/pi/pikrellcam/www/media/videos/*')
			filename = max(listVideos, key=os.path.getctime)
			time.sleep(0.01)
		Upath = "user2/"+("images" if picture else "videos")+"/"
		start_time = time.time()
		sub.call('aws s3 cp ' + filename + ' s3://pi-1/'+Upath,shell=True)
		file.write("AWS : "+("Picture" if picture else "Video")+" uploaded in %s seconds on " % (time.time() - start_time) + time.strftime("%Y/%m/%d at %H:%M\n"))
		start_time = time.time()
		sub.call('/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload ' + filename + ' /'+Upath,shell=True)
		file.write("DB  : "+("Picture" if picture else "Video")+" uplaoded in %s seconds on " % (time.time() - start_time) + time.strftime("%Y/%m/%d at %H:%M\n"))
	time.sleep(0.01)
	prevState = currentState
