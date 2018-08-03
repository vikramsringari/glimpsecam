import glob, os

def rename(path, number):
	list = glob.glob(path + '/*')
	filename = max(list, key=os.path.getctime)
	filepath = os.path.split(filename)
	os.rename(filename, filepath[0] + '/%05d' % number + filepath[1])
	return filepath[0] + '/%05d' % number + filepath[1]
