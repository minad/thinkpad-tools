import time

class Sensor:
	def __init__(self, name, min, max):
		self.__name = name
		self.__min  = min
		self.__max  = max
		self.__temp = None
		self.__time = 0
		self.__interval = None

	def temp(self):
		return self.__temp

	def min(self):
		return self.__min
	
	def max(self):
		return self.__max

	def name(self):
		return self.__name

	def isValid(self):
		return self.__temp != None

	def update(self):
		if self.__interval:
			if time.time() - self.__time > self.__interval:
				self.__temp  = self.read()
				self.__time = time.time()
		else:
			self.__temp  = self.read()

	def setInterval(self, i):
		self.__interval = i

