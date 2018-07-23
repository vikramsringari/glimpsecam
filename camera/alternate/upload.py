print('Initializing...')

import pyinotify
import tinys3
from threading import Thread
import config

# Run common init functions
config.common_init()

# Init S3
# TODO: Why tls=True?
print('Attempting S3 connection...')
s3_connection = tinys3.Connection(
    config.S3_ACCESS, config.S3_SECRET,
    tls=True, endpoint=config.S3_ENDPOINT
)
print('    Done.')

# Init pyinotify
watchman = pyinotify.WatchManager()

# pyinotify class to watch for arbitrary FS events
class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CLOSE_WRITE(self, event):
    	def __upload():
    		filename = os.path.basename(event.pathname)
    		print('{} closed writing, uploading...'.format(filename))

    		# Upload via the S3 s3_connection
    		with open(event.pathname, 'rb') as f:
    			s3_connection.upload(filename, f, config.S3_BUCKET)

    		print('    Done.')

    	# Run on a separate thread
    	Thread(target=__upload, args=[]).start()

# Create the pyinotify event handler
# We are only watching for IN_CLOSE_WRITE because that means that it is safe
# to upload the file we are watching
handler = EventHandler()
notifier = pyinotify.Notifier(watchman, handler)
wdd = watchman.add_watch(config.OUTPUT, pyinotify.IN_CLOSE_WRITE, rec=True)

# Main loop: wait to be notified of IN_CLOSE_WRITE
notifier.loop()