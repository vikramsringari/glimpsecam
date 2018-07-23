import os
import errno
import config

# Common init functions to all files
def common_init():
	# Ensure output directory exists (config.OUTPUT)
	try:
		os.makedirs(config.OUTPUT)
	except OSError as e:
		if e.errno == errno.EEXIST and os.path.isdir(config.OUTPUT):
			pass
		else:
			raise

# Returns current time in milliseconds
def time_ms():
	return time.time() * 1000