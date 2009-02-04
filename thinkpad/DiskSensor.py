import re
from Util import runCmd
from Sensor import Sensor

class DiskSensor(Sensor):
	def __init__(self, disk, min, max):
		Sensor.__init__(self, 'Disk %s' % disk, min, max)
		self.__disk = disk
		self.__time = -1
		self.setInterval(300)

	def read(self):
		l = runCmd('hddtemp %s' % self.__disk)
		for x in l:
			m = re.match('[^:]+:[^:]+:\s+(\d+)\s+C', x)
			if m: return float(m.group(1))
		return None


