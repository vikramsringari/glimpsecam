import tinys3, socket, pyinotify, os, time, threading, subprocess
import imageEnhance as iE

access = ''
secret = ''

with open("./glimpsecam/camera/numFile.txt") as numFile:
	int_list = [int(i) for i in numFile.readline().split()]

conn = tinys3.Connection(access, secret, tls=True, default_bucket='pi-1')

watchman = pyinotify.WatchManager()

mask = pyinotify.IN_MOVED_TO | pyinotify.IN_CREATE

class NoWiFiException(Exception):
	pass

class EventHandler(pyinotify.ProcessEvent):
	def process_IN_MOVED_TO(self, event):
		def __upload():
			type = event.pathname[-4:]
			filename = os.path.basename(event.pathname)
			with open(event.pathname, 'rb') as f:
				try:
					if subprocess.check_output(['hostname','-I']).isspace():
						raise NoWiFiException
					conn.upload(socket.gethostname() + '/' + ('images' if (type == '.jpg') else 'videos') + '/' + filename, f)
					print 'success'
				except:
					with open('/home/pi/newFiles.txt','a') as file:
						file.write(event.pathname+'\n')
					print 'failure'
		threading.Thread(target=__upload, args=[]).start()

	def process_IN_CREATE(self, event):
		type = event.pathname[-4:]
		path = os.path.dirname(event.pathname)
		if type == '.jpg':
			#print 'image was created: ', event.pathname
			time.sleep(1)
			iE.simpleImageEnhance(event.pathname, event.pathname)
			#print 'image was enhanced: ', event.pathname
			filename = os.path.basename(event.pathname)
			time.sleep(1)
			os.rename(event.pathname, path + '/%05d' % int_list[0] + filename)
			int_list[0] -= 1
		elif type == '.mp4':
			#print 'video was created: ', event.pathname
			time.sleep(10)
			filename = os.path.basename(event.pathname)
			time.sleep(1)
			os.rename(event.pathname, path + '/%05d' % int_list[1] + filename)
			int_list[1] -= 1
		time.sleep(0.01)
		with open('./glimpsecam/camera/numFile.txt','w') as numFile:
			numFile.write(str(int_list[0]) + ' ' + str(int_list[1]))

handler = EventHandler()
notifier = pyinotify.Notifier(watchman, handler)
wdd = watchman.add_watch('pikrellcam/media/videos', mask, rec=True)
wss = watchman.add_watch('pikrellcam/media/stills', mask, rec=True)

notifier.loop()
