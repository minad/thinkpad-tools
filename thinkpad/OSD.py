from Util import findCmd, getPids
import X11
import os, time, signal

class OSD:

	font    = '-*-lucidatypewriter-*-*-*-*-*-240-*-*-*-*-*-*'
	delay   = 2
	pos     = 'middle'
	align   = 'center'
	color   = 'blue'
	outline = 1
	shadow  = 3
	text    = ''
	barmode = ''
	percentage = 0

	def __init__(self):
		self.__osd_cat = findCmd('osd_cat')

	def show(self):
		pids = getPids('osd_cat')
		X11.foreachDisplay(OSD.__showOSD, self)
		time.sleep(.01)
		for pid in pids:
			os.kill(pid, signal.SIGTERM)

	def __showOSD(self, *foo):
		args = ''
		for arg in ['font', 'delay', 'pos', 'align', 'color', 'outline', 'shadow']:
			args += ' --%s=%s' % (arg, getattr(self, arg))
		if self.barmode == 'slider' or self.barmode == 'percentage':
			args += ' --barmode=%s --percentage=%d --text="%s"' % \
				(self.barmode, int(self.percentage), self.text)
			cmd = '%s %s &' % (self.__osd_cat, args)
		else:
			cmd = 'echo %s | %s %s &' % (self.text, self.__osd_cat, args)
		os.system(cmd)

