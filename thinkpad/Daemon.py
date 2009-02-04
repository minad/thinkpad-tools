import os, sys, atexit, signal, errno
from Util import burp, slurp

class Daemon:
	def __init__(self, pidFile):
		self.__pidFile = pidFile

	def start(self):
		if self.running():
			return
		try:
			if os.fork() > 0: os._exit(0)
		except OSError, error:
			sys.stderr.write("fork #1 failed: %d (%s)\n" % (error.errno, error.strerror))
			os._exit(1)
		
		os.chdir('/')
		os.setsid()
		os.umask(0)
		
		try:
			pid = os.fork()
			if pid > 0:
				return
		except OSError, error:
			sys.stderr.write("fork #2 failed: %d (%s)\n" % (error.errno, error.strerror))
			os._exit(1)
		
		atexit.register(os.unlink, self.__pidFile)
		burp(self.__pidFile, '%d' % os.getpid())
		self.run()
		os.unlink(self.__pidFile)
		os._exit(0)

	def stop(self):
		if os.path.exists(self.__pidFile):
			try:
				os.kill(int(slurp(self.__pidFile)), signal.SIGTERM)
			except OSError, error:
				if error.errno == errno.ESRCH:
					sys.stderr.write("Removing stale pid file\n")
					os.unlink(self.__pidFile)
				else:
					sys.stderr.write("Failed to kill daemon: %d (%s)\n" % (error.errno, error.strerror));
					sys.exit(1)
	
	def running(self):
		if os.path.exists(self.__pidFile):
			try:
				os.kill(int(slurp(self.__pidFile)), 0)
				return True
			except OSError, error:
				return False
		return False

