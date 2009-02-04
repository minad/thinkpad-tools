class FanDriver:
	__started = False

	def __init__(self, min, max):
		self.__min = min
		self.__max = max
	
	def __del__(self):
		self.__stop()

	def min(self):
		return self.__min

	def max(self):
		return self.__max

	def level(self):
		return self.driverLevel()

	def speed(self):
		return self.driverSpeed()

	def setLevel(self, level):
		self.__start()
		print 'New level: %d' % level
		self.driverSetLevel(level)

  	def __start(self):
		if not self.__started:
			self.driverStart()
			self.__started = True

	def __stop(self):
		if self.__started:
			self.driverStop()
			self.__started = False
