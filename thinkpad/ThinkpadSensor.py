from Util import slurp
from Sensor import Sensor

class ThinkpadSensor(Sensor):
	def __init__(self, name, id, min, max):
		Sensor.__init__(self, name, min, max)
		self.__id = id
	
	def read(self):
		try:
			return float(slurp('/sys/devices/platform/thinkpad_hwmon/temp%d_input' % self.__id)) / 1000
		except IOError:
			return None

