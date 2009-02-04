from Util import runCmd, findCmd
import os

wacomButton = 'Button2'
wacomRotations= { 'normal': '0', 'left': '2', 'right': '1', 'inverted': '3' }

class Wacom:
	def __init__(self):
		self.__xsetwacom = findCmd('xsetwacom')
		self.__devices   = self.__findDevices()

	def __findDevices(self):
		dev = runCmd("%s list dev | awk {'print $1'}" % self.__xsetwacom)
		return map(lambda s: s.strip(), dev)
   
	def setRotation(self, o):
		for d in self.__devices:
			runCmd("%s set %s Rotate %s" % (self.__xsetwacom, d, wacomRotations[o]))

	def getPenButton(self):
		return runCmd('%s get %s %s' % (self.__xsetwacom, self.__devices[0], wacomButton))[0].strip()
		
	def setPenButton(self, b):
		for d in self.__devices:
			os.system('%s set %s %s %s' % (self.__xsetwacom, d, wacomButton, b))

