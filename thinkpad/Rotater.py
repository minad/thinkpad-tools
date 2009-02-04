import os, re
from Util import runCmd
from Wacom import Wacom
from Util import runCmd, findCmd

class Rotater:
	def __init__(self):
		self.__wacom = Wacom()
		self.__xrandr = findCmd('xrandr')

	def getRotation(self):
		l = runCmd(self.__xrandr)
		l = [x for x in l if re.search(r'(LVDS|default) connected', x)][0]
		l = l.split(' ')[3]
		l = re.sub(r'\(', '', l)
		return l.strip()
		
	def setRotation(self, o):
		runCmd("%s --output LVDS --rotate %s" % (self.__xrandr, o))
		self.__wacom.setRotation(o)
		self.__updateArrowKeys(o)
	
	def __updateArrowKeys(self, o):
		# Keycodes to use for each rotation
		# 104 = pgup, 109 = pgdn, 105 = left, 106 = right, 103 = up, 108 = down
		keyCodes = {
			    'normal':   {'up': 103, 'dn': 108, 'lt': 105, 'rt': 106},
			    'right':    {'up': 105, 'dn': 106, 'lt': 108, 'rt': 103},
			    'inverted': {'up': 108, 'dn': 103, 'lt': 106, 'rt': 105},
			    'left':     {'up': 106, 'dn': 105, 'lt': 103, 'rt': 108}
			  }

		# Keyboard scan codes for arrow keys (you probably don't need to change these)
		scanCodes = {'up': 0x71, 'dn': 0x6f, 'lt': 0x6e, 'rt': 0x6d}

		for sc in scanCodes.keys():
			os.system('setkeycodes %x %d 2> /dev/null' % (scanCodes[sc], keyCodes[o][sc]))

