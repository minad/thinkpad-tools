AVERAGE_LEN = 30

class FanScheduler:
	def __init__(self, min, max, sensors):
		self.__sensors  = sensors
		self.__min = min
		self.__max = max
		self.__level = max
		self.__list = []

	def update(self):
		maxLevel = self.__min
		maxSensor = None
		for s in self.__sensors:
			s.update()
			if s.isValid():
				if s.temp() <= s.min():
					level = self.__min
				elif s.temp() >= s.max():
					level = self.__max
				else:
					level = (s.temp() - s.min()) / (s.max() - s.min()) * (self.__max - self.__min) + self.__min
				if level > maxLevel:
					maxSensor = s.name()
					maxLevel = level
		print '%s: %d' % (maxSensor, maxLevel)
		self.__list.append(maxLevel)
		if len(self.__list) > AVERAGE_LEN:
			self.__list.pop(0)
		sum = 0
		div = 0
		for i in range(len(self.__list)):
			div += i+1
			sum += (i+1) * self.__list[i]
		self.__level = sum / div

	def level(self):
		return self.__level

