import gtk, os, sys, signal
from xml.sax import ContentHandler, make_parser
from thinkpad.Util import getPids

class Launcher(ContentHandler):
	window = None
	box = []
	button = None
	command = ""

	def __init__(self):
		signal.signal(signal.SIGTERM, gtk.main_quit)

		pids = getPids('tabletLauncher')
		if len(pids) > 1:
			for pid in pids:
				if pid != os.getpid():
					os.kill(pid, signal.SIGTERM)
			sys.exit(0)

		if os.path.exists("/etc/tablet-launcher/gtkrc"):
			gtk.rc_parse("/etc/tablet-launcher/gtkrc")
		parser = make_parser()
		parser.setContentHandler(self)
		parser.parse("/etc/tablet-launcher/commands.xml")

	def startElement(self, name, attrs):
		if name == "window":
			self.window = gtk.Window(gtk.WINDOW_POPUP)
			self.window.set_title(attrs["title"])
			self.window.set_decorated(0)
			self.window.connect("destroy", gtk.main_quit)
			self.window.set_position("center")

			box = gtk.VBox(False, 0)
			box.set_border_width(10)
			self.window.add(box)
			
			self.box.append(box)

			label = gtk.Label()
			label.set_markup("<b>" + attrs["title"] + "</b>")
			box.pack_start(label, True, True, 0)

		elif name == "vbox" or name == "hbox":
			if name == "vbox":
				box = gtk.VBox(False, 3)
			else:
				box = gtk.HBox(True, 3)

			if "title" in attrs.keys():
				frame = gtk.Frame(attrs["title"]);
				frame.set_border_width(2)
				frame.add(box)
				self.box[len(self.box)-1].pack_start(frame, True, True, 0)
			else:
				self.box[len(self.box)-1].pack_start(box, True, True, 0)
			
			self.box.append(box)
		
		elif name == "button":
			self.addButton(attrs["title"])

	def endElement(self, name):
		if name == "window":
			self.addButton("Close")
			self.button.connect("clicked", gtk.main_quit)
			self.window.show_all()
		elif name == "vbox" or name == "hbox":
			self.box.pop()
		elif name == "button":
			cmds = map(lambda s: s.strip(), self.command.split("\n"))
			cmds = filter(lambda s: s != "", cmds)	
			self.button.connect("clicked", self.runCommand, "; ".join(cmds))
			self.button = None
			self.command = ""

	def characters(self, ch):
		if self.button:
			self.command += ch

	def runCommand(self, widget, cmd):
		print cmd
		os.system(cmd + " &")

	def addButton(self, title):
		self.button = gtk.Button(title)
		self.button.set_border_width(2)
		box = self.box[len(self.box)-1]
		box.pack_start(self.button, False, box.__class__ == gtk.HBox, 0)
	
	def main(self):
		gtk.main()

