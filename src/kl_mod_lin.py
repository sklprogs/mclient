#!/usr/bin/python3

import sys
import signal
from Xlib.display import Display
from Xlib import X, XK
from Xlib.ext import record
from Xlib.protocol import rq
import threading

flags = {'HotkeyCaught':False,'Verbose':False}

def catch_control_c(*args):
	pass
	
signal.signal(signal.SIGINT,catch_control_c) # do not quit when Control-c is pressed

def print_v(*args):
	if flags['Verbose']:
		print(*args)

def toggle_hotkey(SetBool=True):
	flags['HotkeyCaught'] = SetBool



# Определить нажатие горячих клавиш глобально в системе
class KeyListener(threading.Thread):
	''' Использование: 
		keylistener = KeyListener()
		Изначально:
		keylistener.addKeyListener("L_CTRL+L_SHIFT+y", callable)
		Обратить внимание, что необходимо присвоить все возможные комбинации, поскольку порядок нажатия может быть иной, например, "L_CTRL+y+L_SHIFT"
		Теперь:
		keylistener.addKeyListener("Control_L+c+c", callable)
	'''
	def __init__(self):
		threading.Thread.__init__(self)
		self.finished = threading.Event()
		self.contextEventMask = [X.KeyPress,X.MotionNotify]
		# Give these some initial values
		# Hook to our display.
		self.local_dpy = Display()
		self.record_dpy = Display()
		self.pressed = []
		self.listeners = {}

	# need the following because XK.keysym_to_string() only does printable chars
	# rather than being the correct inverse of XK.string_to_keysym()
	def lookup_keysym(self, keysym):
		for name in dir(XK):
			if name.startswith("XK_") and getattr(XK, name) == keysym:
				return name.lstrip("XK_")
		return "[%d]" % keysym

	def processevents(self, reply):
		if reply.category != record.FromServer:
			return
		if reply.client_swapped:
			print_v("* received swapped protocol data, cowardly ignored")
			return
		# Добавил str, иначе получаем ошибку
		if not len(str(reply.data)) or ord(str(reply.data[0])) < 2:
			# not an event
			return
		data = reply.data
		while len(data):
			event, data = rq.EventField(None).parse_binary_value(data, self.record_dpy.display, None, None)
			keycode = event.detail
			keysym = self.local_dpy.keycode_to_keysym(event.detail, 0)
			character = self.lookup_keysym(keysym)
			if character:
				if event.type == X.KeyPress:
					self.press(character)
				elif event.type == X.KeyRelease:
					self.release(character)

	def run(self):
		# Check if the extension is present
		if not self.record_dpy.has_extension("RECORD"):
			print_v("RECORD extension not found")
			sys.exit(1)
		r = self.record_dpy.record_get_version(0, 0)
		print_v("RECORD extension version %d.%d" % (r.major_version, r.minor_version))
		# Create a recording context; we only want key events
		self.ctx = self.record_dpy.record_create_context(
				0,
				[record.AllClients],
				[{
						'core_requests': (0, 0),
						'core_replies': (0, 0),
						'ext_requests': (0, 0, 0, 0),
						'ext_replies': (0, 0, 0, 0),
						'delivered_events': (0, 0),
						'device_events': tuple(self.contextEventMask), #(X.KeyPress, X.ButtonPress),
						'errors': (0, 0),
						'client_started': False,
						'client_died': False,
				}])

		# Enable the context; this only returns after a call to record_disable_context,
		# while calling the callback function in the meantime
		self.record_dpy.record_enable_context(self.ctx, self.processevents)
		# Finally free the context
		self.record_dpy.record_free_context(self.ctx)

	def cancel(self):
		self.finished.set()
		self.local_dpy.record_disable_context(self.ctx)
		self.local_dpy.flush()

	def press(self, character):
		if len(self.pressed) == 3:
			self.pressed = []
		if character == 'Control_L' or character == 'Control_R':
			if len(self.pressed) > 0:
				self.pressed = []
			self.pressed.append(character)
		elif character == 'c' or character == 'Insert':
			if len(self.pressed) > 0:
				if self.pressed[0] == 'Control_L' or self.pressed[0] == 'Control_R':
					self.pressed.append(character)
		action = self.listeners.get(tuple(self.pressed), False)
		print_v('Current action:', str(tuple(self.pressed)))
		if action:
			action()

	def release(self, character):
		"""must be called whenever a key release event has occurred."""
		# Не засчитывает отпущенный Control
		# Кириллическую 'с' распознает как латинскую
		if character != 'c' and character != 'Insert':
			self.pressed = []

	def addKeyListener(self, hotkeys, callable):
		keys = tuple(hotkeys.split("+"))
		print_v("Added new keylistener for :",str(keys))
		self.listeners[keys] = callable



def result():
	if flags['HotkeyCaught']:
		print_v('Hotkey has been caught!')
		flags['HotkeyCaught'] = False
		return True
	else:
		return False
			
def wait_example():
	from time import sleep
	while not result():
		sleep(.5)
	keylistener.cancel()
	
keylistener = KeyListener()
keylistener.addKeyListener("Control_L+c+c",toggle_hotkey)
keylistener.addKeyListener("Control_R+c+c",toggle_hotkey)
keylistener.addKeyListener("Control_L+Insert+Insert",toggle_hotkey)
keylistener.addKeyListener("Control_R+Insert+Insert",toggle_hotkey)
keylistener.start()

if __name__ == '__main__':
	wait_example()
