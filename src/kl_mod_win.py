# !/usr/bin/python3
# -*- coding: UTF-8 -*-

# Замечание: в pyhook есть баг, из-за которого данная программа валится, если на передний план выходит приложение с кириллицей в заголовке, поэтому в коде на C pyHook необходимо закомментировать случаи присваивания win_name и пересобрать библиотеку.

from pyHook import HookManager
# Если нужно делать вывод в консоль
import pythoncom
import threading

globs = {'HotkeyCaught':False,'hits':0,'Verbose':False}
lock = threading.Lock()

def print_v(*args):
	if globs['Verbose']:
		print(*args)

def toggle_hotkey(SetBool=True):
	globs['HotkeyCaught'] = SetBool
	globs['hits'] += 1
	print_v('Hotkey has been detected and flag has been changed to %s (%d hits in total)!' % (str(globs['HotkeyCaught']),globs['hits']))

class KeyListener(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.finished = threading.Event()
		# Переменные должны быть инициализированы до вызова HookManager
		self.pressed = []
		self.listeners = {}
		# Иногда по непонятной причине символы выходят в верхнем регистре, но мы их приводим в нижний регистр в классе, поэтому здесь достаточно указать 'c'
		self.addKeyListener("Lcontrol+c+c",toggle_hotkey)
		self.addKeyListener("Rcontrol+c+c",toggle_hotkey)
		self.addKeyListener("Lcontrol+Insert+Insert",toggle_hotkey)
		self.addKeyListener("Rcontrol+Insert+Insert",toggle_hotkey)
		self.restart()
	#--------------------------------------------------------------------------
	def cancel(self):
		self.hm.UnhookKeyboard()
		self.finished.set()
	#--------------------------------------------------------------------------
	def restart(self):
		lock.acquire()
		self.hm = HookManager()
		self.hm.KeyDown = self.press
		self.hm.KeyUp = self.release
		self.hm.HookKeyboard()
		lock.release()
	#--------------------------------------------------------------------------
	def press(self,event):
		character = str(event.Key)
		if character:
			if len(character) == 1:
				character = character.lower()
			print_v('Key released: %s' % str(character))
			if len(self.pressed) == 3:
				self.pressed = []
			if character == 'Lcontrol' or character == 'Rcontrol':
				if len(self.pressed) > 0:
					self.pressed = []
				self.pressed.append(character)
			elif character == 'c' or character == 'C' or character == 'Insert':
				if len(self.pressed) > 0:
					if self.pressed[0] == 'Lcontrol' or self.pressed[0] == 'Rcontrol':
						self.pressed.append(character)
			action = self.listeners.get(tuple(self.pressed), False)
			print_v('Current action: ' + str(tuple(self.pressed)))
			if action:
				action()
		# Без этого получаем ошибку (an integer is required)
		return True
	#--------------------------------------------------------------------------
	def release(self,event):
		"""must be called whenever a key release event has occurred."""
		character = str(event.Key)
		if character:
			if len(character) == 1:
				character = character.lower()
			print_v('Key released: %s' % str(character))
			# Не засчитывает отпущенный Control
			# Кириллическую 'с' распознает как латинскую
			if character != 'c' and character != 'C' and character != 'Insert':
				self.pressed = []
		# Без этого получаем ошибку (an integer is required)
		return True
	#-------------------------------------------------------------------
	def addKeyListener(self, hotkeys, callable):
		keys = tuple(hotkeys.split("+"))
		print_v("Added new keylistener for :" + str(keys))
		self.listeners[keys] = callable

def result():
	if globs['HotkeyCaught']:
		print_v('Hotkey has been caught!')
		globs['HotkeyCaught'] = False
		return True
	else:
		return False

'''
	Linux: Control_L, Control_R
	Windows: Lcontrol, Rcontrol
'''

def wait_example():
	from time import sleep
	while not result():
		# Нельзя делать одновременно pythoncom.PumpMessages() и pythoncom.PumpWaitingMessages() - они оба создают циклы
		# Без этого result вообще почему-то не работает (видимо, здесь есть какой-то цикл, который необходим). Если же создать поток, он не сможет обнаружить globs['HotkeyCaught'].
		pythoncom.PumpWaitingMessages()
		# Если поставить слишком большой интервал, например, 1, то вообще ничего не получим!
		sleep(0.1)
	keylistener.cancel()
	
def wait_cycle():
	from time import sleep, time
	print_v('You have 5 seconds only...')
	timeout = time() + 5
	while timeout > time():
		pythoncom.PumpWaitingMessages()
	keylistener.cancel()
	
keylistener = KeyListener()
# Лучше это делать в 2 строчки, иначе можем получать ошибки
keylistener.start()

if __name__ == '__main__':
	wait_example()
