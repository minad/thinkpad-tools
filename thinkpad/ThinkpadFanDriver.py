from FanDriver import FanDriver
from Util import slurp, burp
import os

class ThinkpadFanDriver(FanDriver):
	def __init__(self):
		FanDriver.__init__(self, 0, 255)
		if not os.access('/sys/devices/platform/thinkpad_hwmon/pwm1', os.W_OK):
			raise SystemError()

  	def driverStart(self):
		self.__setWatchdog(8)
		self.__setMode(1)

	def driverStop(self):
		self.__setMode(2)
		self.__setWatchdog(0)

	def driverSetLevel(self, level):
		burp('/sys/devices/platform/thinkpad_hwmon/pwm1', '%d' % level)

	def driverLevel(self):
		return slurp('/sys/devices/platform/thinkpad_hwmon/pwm1')
	
	def __setWatchdog(self, time):
		burp('/sys/bus/platform/drivers/thinkpad_hwmon/fan_watchdog', '%d' % time)
  
	def __setMode(self, mode):
		if mode in [1, 2]: # Manual, auto
			print 'Fan mode %d' % mode
			burp('/sys/devices/platform/thinkpad_hwmon/pwm1_enable', '%d' % mode)
 
