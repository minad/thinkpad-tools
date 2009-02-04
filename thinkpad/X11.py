from Util import runCmd
import re, os, pwd

def foreachDisplay(cb, *args):
	for (user, display) in __getDisplays():
		__runCallback(cb, args, user, display)

def __getDisplays():
	who = runCmd('/usr/bin/who -s')
	l = filter(lambda s: re.search('^[^\s]+\s+(:[\.\d]+)', s), who)
	return map(lambda x: (re.split('\s+', x)[0], re.split('\s+', x)[1]), l)

def __runCallback(cb, args, user, display):
	pw = pwd.getpwnam(user)
	home = pw.pw_dir
	xauth = '%s/.Xauthority' % home
	if os.access(xauth, os.R_OK):
		oldEnviron = os.environ
		os.environ['DISPLAY'] = display
		os.environ['XAUTHORITY'] = xauth
		cb(*(args + (pw.pw_uid, display)))
		os.environ = oldEnviron

