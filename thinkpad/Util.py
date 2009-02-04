import os

def slurp(file):
	f = open(file)
	d = f.read()
	f.close()
	return d
	
def burp(file, data):
	f = open(file, 'w')
	f.write(data)
	f.close()

def runCmd(cmd):
	f = os.popen(cmd)
	l = f.readlines()
	f.close()
	return l
	
def findCmd(cmd):
	for path in [ '/usr/local/sbin/', '/usr/local/bin/', '/usr/sbin/', '/usr/bin/', '/sbin', '/bin' ]:
		if os.path.isfile(path + cmd):
			return path + cmd
	raise Exception('Command %s not found' % cmd)

def getPids(cmd):
	return map(lambda x: int(x.strip().split(' ')[0]), runCmd('ps --no-heading -C %s' % cmd))

