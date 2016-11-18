# !/usr/bin/python3
# -*- coding: UTF-8 -*-

# Замечание: в pyhook есть баг, из-за которого данная программа валится, если на передний план выходит приложение с кириллицей в заголовке, поэтому в коде на C pyHook необходимо закомментировать случаи присваивания win_name и пересобрать библиотеку.

from pyHook import HookManager
# Если нужно делать вывод в консоль
import pythoncom
import threading



class KeyListener(threading.Thread):
	
	def __init__(self):
		threading.Thread.__init__(self)
		self.finished = threading.Event()
		# Переменные должны быть инициализированы до вызова HookManager
		self.pressed = []
		self.listeners = {}
		self.status = 0
		# Иногда по непонятной причине символы выходят в верхнем регистре, но мы их приводим в нижний регистр в классе, поэтому здесь достаточно указать 'c'
		self.addKeyListener("Lcontrol+c+c",lambda: keylistener.set_status(status=1))
		self.addKeyListener("Rcontrol+c+c",lambda: keylistener.set_status(status=1))
		self.addKeyListener("Lcontrol+Insert+Insert",lambda: keylistener.set_status(status=1))
		self.addKeyListener("Rcontrol+Insert+Insert",lambda: keylistener.set_status(status=1))
		self.addKeyListener("Lmenu+Oem_3",lambda: keylistener.set_status(status=2))
		self.addKeyListener("Rmenu+Oem_3",lambda: keylistener.set_status(status=2))
		self.restart()

	def cancel(self):
		self.hm.UnhookKeyboard()
		self.finished.set()

	def restart(self):
		lock.acquire()
		self.hm = HookManager()
		self.hm.KeyDown = self.press
		self.hm.KeyUp = self.release
		self.hm.HookKeyboard()
		lock.release()

	def press(self,event):
		character = str(event.Key)
		if character:
			if len(character) == 1:
				character = character.lower()
			print_v('Key released: %s' % str(character))
			if len(self.pressed) == 2:
				if self.pressed[1] == 'Oem_3':
					self.pressed = []
			elif len(self.pressed) == 3:
				self.pressed = []
			if character == 'Lcontrol' or character == 'Rcontrol' or character == 'Lmenu' or character == 'Rmenu':
				self.pressed = [character]
			elif character == 'c' or character == 'C' or character == 'Insert' or character == 'Oem_3':
				if len(self.pressed) > 0:
					if self.pressed[0] == 'Lcontrol' or self.pressed[0] == 'Rcontrol' or self.pressed[0] == 'Lmenu' or self.pressed[0] == 'Rmenu':
						self.pressed.append(character)
			action = self.listeners.get(tuple(self.pressed), False)
			print_v('Current action: ' + str(tuple(self.pressed)))
			if action:
				action()
		# Без этого получаем ошибку (an integer is required)
		return True

	def release(self,event):
		"""must be called whenever a key release event has occurred."""
		character = str(event.Key)
		if character:
			if len(character) == 1:
				character = character.lower()
			print_v('Key released: %s' % str(character))
			# Не засчитывает отпущенный Control
			# Кириллическую 'с' распознает как латинскую
			if character != 'c' and character != 'C' and character != 'Insert' and character != 'Oem_3':
				self.pressed = []
		# Без этого получаем ошибку (an integer is required)
		return True

	def addKeyListener(self, hotkeys, callable):
		keys = tuple(hotkeys.split("+"))
		print_v("Added new keylistener for :" + str(keys))
		self.listeners[keys] = callable
		
	def set_status(self,status=0):
		self.status = status
		print_v('Setting status to %d!' % self.status)
		
	def check(self): # Returns 0..2
		if self.status:
			print_v('Hotkey has been caught!')
			status = self.status
			self.status = 0
			return status

'''
	Linux: Control_L, Control_R
	Windows: Lcontrol, Rcontrol
'''

def print_v(*args):
	if Verbose:
		print(*args)

def wait_example():
	from time import sleep
	while not keylistener.check():
		# Нельзя делать одновременно pythoncom.PumpMessages() и pythoncom.PumpWaitingMessages() - они оба создают циклы
		# Без этого result вообще почему-то не работает (видимо, здесь есть какой-то цикл, который необходим). Если же создать поток, он не сможет обнаружить flags['HotkeyCaught'].
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
	
lock = threading.Lock()
Verbose = False
keylistener = KeyListener()
# Лучше это делать в 2 строчки, иначе можем получать ошибки
keylistener.start()

if __name__ == '__main__':
	wait_example()
