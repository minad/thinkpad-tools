from Daemon import Daemon
from Rotater import Rotater
from HDAPS import HDAPS
import time

pidFile = '/tmp/hdaps-rotater.pid'
tilt = 20

class HDAPSRotater(Daemon, Rotater):
	hdaps = HDAPS()

	def __init__(self):
		Daemon.__init__(self, pidFile)
		Rotater.__init__(self)

	def run(self):
		centerX, centerY = self.hdaps.center()
		rot = self.getRotation()
		while True:
			time.sleep(0.5)
			x, y = self.hdaps.position()
			dx = x - centerX
			dy = y - centerY
			newrot = rot
			if abs(dx) - abs(dy) > tilt:
				if dx > tilt:
					newrot = 'right'
				elif dx < -tilt: 
					newrot = 'left'
			elif abs(dy) - abs(dx) > tilt:
				if dy > tilt:
					newrot = 'inverted'
				elif dy < -tilt: 
					newrot = 'normal'
			if rot != newrot:
				self.setRotation(newrot)
				rot = newrot

