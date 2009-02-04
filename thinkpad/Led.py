from Util import burp
import os

class Led:
	def __init__(self, id):
		self.__id = id
		self.__accessible = os.access('/proc/acpi/ibm/led', os.W_OK)

	def on(self):
		self.__set('on')

	def off(self):
		self.__set('off')

	def blink(self):
		self.__set(n, 'blink')

	def __set(self, mode):
		if self.__accessible:
			burp('/proc/acpi/ibm/led', '%d  %s' % (self.__id, mode))

