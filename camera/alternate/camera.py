# Print something since gpiozero takes so long to init..
print('Initializing...')

import config
import time
import random
import string
from threading import Thread
from picamera import PiCamera, PiCameraCircularIO
from gpiozero import Button

# Run common init functions
config.common_init()

# Init ends here
print('    Done.')

# Singleton class instances
button_handler = None
camera_handler = None

# Makes a randomized and timestamped filename
# Contains the specified string and uses the extension
def make_filename(name, ext, prefix_dir='./'):
	# Ensure the directory ends with a path separator
	if prefix_dir[-1] != '/':
		prefix_dir += '/'

	# Random 8 characters
	randstr = ''.join(
		random.choice(string.ascii_uppercase + string.digits)
		for _ in range(8)
	)

	return '{}{}_{}_{}.{}'.format(
		prefix_dir, time.strftime('%Y%m%d%H%M%S'),
		randstr, name, ext
	)

# TODO: Document
class CameraHandler():
	# Retroactive recording timing
	# (m, n) => m seconds before and n seconds after
	retroactive_time = (10, 2)

	def __init__(self):
		# TODO: Make resolution configurable
		# Initialize the camera
		self.camera = PiCamera()
		self.camera.resolution = (1280, 720)

		# Record to a circular stream for retroactive recording
		self.stream = PiCameraCircularIO(
			self.camera,
			seconds=sum(CameraHandler.retroactive_time)
		)

		# Start recording
		self.camera.start_recording(self.stream, format='h264')

	# Captures a picture on another thread and writes it to OUTPUT
	def picture(self):
		# Capture on another thread
		def __capture(camera, output):
			print('Picture -> ' + output)
			camera.capture(output)

		Thread(
			target=__capture,
			args=[self.camera, make_filename('out', 'jpg', config.OUTPUT)]
		).start()

	# Captures a video on another thread and writes it to OUTPUT
	# Waits for retroactive_time[1] seconds after call to write video out
	def video(self):
		# Record and write on another thread
		def __capture(camera, stream, output):
			wait = CameraHandler.retroactive_time[1]
			
			print('Video -> waiting extra ' + str(wait) + ' seconds')
			camera.wait_recording(wait)
			print('    Writing to ' + output)

			# Specify seconds because there could be more in the buffer
			stream.copy_to(
				output,	seconds=sum(CameraHandler.retroactive_time)
			)

		Thread(
			target=__capture,
			args=[self.camera, self.stream, make_filename('out', 'h264', config.OUTPUT)]
		).start()

# Keeps track of current button presses, time between, etc.
class ButtonHandler():
	# Maximum ms distance detected as double click
	double_time_ms = 225

	def __init__(self, pin):
		# FIFO stack of last presses, maintained to ~16 elements
		self.pstack = []

		# Button on specified GPIO pin
		self.button = Button(pin)

		# Boolean state of the last time the button was polled
		self.last_state = False

	# Logs a single button press
	def press(self):
		# Push this press onto the stack
		self.pstack.append(time_ms())

		# Trim the stack
		if len(self.pstack) > 16:
			del self.pstack[:(len(self.pstack) - 16)]

		# Detect double presses
		if (len(self.pstack) >= 2 and
			(self.pstack[-1] - self.pstack[-2]) <= ButtonHandler.double_time_ms):
			
			# Remove both from the stack
			del self.pstack[(len(self.pstack) - 2):]

			# Capture a video
			camera_handler.video()

	# Handles a poll
	def handle(self, state):
		# Handle state change as press
		if state != self.last_state and state:
			self.press()

		# Detect a single press that was not a double click
		if (len(self.pstack) > 0 and
			time_ms() - self.pstack[-1] > ButtonHandler.double_time_ms):
			
			# Remove from the stack
			del self.pstack[-1]

			# Capture a picture
			camera_handler.picture()

		self.last_state = state


# Initialize global handlers
button_handler = ButtonHandler(2)
camera_handler = CameraHandler()

# Main loop/spin
while True:
	button_handler.handle(button_handler.button.is_pressed)
	time.sleep(0.01)