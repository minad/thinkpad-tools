from Util import slurp

posFile = '/sys/devices/platform/hdaps/position'
calibrateFile = '/sys/devices/platform/hdaps/calibrate'

class HDAPS:
	def __readPos(self, file):
		l = slurp(file)
		return [int(x) for x in l[1:-2].split(',')]

	def position(self):
		return self.__readPos(posFile)

	def center(self):
		return self.__readPos(calibrateFile)

