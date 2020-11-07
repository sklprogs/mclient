#!/usr/bin/python3
# -*- coding: UTF-8 -*-

''' There was a bug in 'pyhook' which crashed the program if a focus 
    was set on a program having Cyrillic symbols in its title. We
    needed to comment out assigning 'win_name' in pyHook's C code and
    recompile the library. 'pyWinhook' does not have such bug.
'''

from pyWinhook import HookManager
# If we need to output to console
import pythoncom
import threading



class KeyListener(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.finished = threading.Event()
        # Variables must be initialized before calling 'HookManager'
        self.pressed = []
        self.listeners = {}
        self.status = 0
        ''' Sometimes symbols are uppercased by an unknown reason,
            however, we lowercase them, therefore it is sufficient
            to have 'c' here.
        '''
        self.addKeyListener ('Lcontrol+c+c'
                            ,lambda:keylistener.set_status(status=1)
                            )
        self.addKeyListener ('Rcontrol+c+c'
                            ,lambda:keylistener.set_status(status=1)
                            )
        self.addKeyListener ('Lcontrol+Insert+Insert'
                            ,lambda:keylistener.set_status(status=1)
                            )
        self.addKeyListener ('Rcontrol+Insert+Insert'
                            ,lambda:keylistener.set_status(status=1)
                            )
        self.addKeyListener ('Lmenu+Oem_3'
                            ,lambda:keylistener.set_status(status=2)
                            )
        self.addKeyListener ('Rmenu+Oem_3'
                            ,lambda:keylistener.set_status(status=2)
                            )
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
            print_v('Key released: {}'.format(character))
            if len(self.pressed) == 2:
                if self.pressed[1] == 'Oem_3':
                    self.pressed = []
            elif len(self.pressed) == 3:
                self.pressed = []
            if character in ('Lcontrol','Rcontrol','Lmenu','Rmenu'):
                self.pressed = [character]
            elif character in ('c','C','Insert','Oem_3'):
                if len(self.pressed) > 0:
                    if self.pressed[0] in ('Lcontrol','Rcontrol','Lmenu'
                                          ,'Rmenu'
                                          ):
                        self.pressed.append(character)
            action = self.listeners.get(tuple(self.pressed), False)
            print_v('Current action: {}'.format(self.pressed))
            if action:
                action()
        # We receive an error without this (an integer is required)
        return True

    def release(self,event):
        """must be called whenever a key release event has occurred."""
        character = str(event.Key)
        if character:
            if len(character) == 1:
                character = character.lower()
            print_v('Key released: %s' % str(character))
            # A released Control key is not taken into account
            # A cyrillic 'с' symbol is recognized as Latin 'c'
            if not character in ('c','C','Insert','Oem_3'):
                self.pressed = []
        # We receive an error without this (an integer is required)
        return True

    def addKeyListener(self, hotkeys, callable):
        keys = tuple(hotkeys.split('+'))
        print_v('Added new keylistener for: {}'.format(keys))
        self.listeners[keys] = callable
        
    def set_status(self,status=0):
        self.status = status
        print_v('Setting status to {}!'.format(self.status))
        
    # Returns 0..2
    def check(self):
        if self.status:
            print_v('Hotkey has been caught!')
            status = self.status
            self.status = 0
            return status

''' Linux: Control_L, Control_R
    Windows: Lcontrol, Rcontrol
'''

def print_v(*args):
    if Verbose:
        print(*args)

def wait_example():
    from time import sleep
    while not keylistener.check():
        ''' Do not call 'pythoncom.PumpMessages()' and
            'pythoncom.PumpWaitingMessages()' simultaneously - they both
            create loops.
            Without this the result does not work for some reason
            (probably, a loop of some kind is required there).
            If we create a thread, it will not find
            flags['HotkeyCaught'].
        '''
        pythoncom.PumpWaitingMessages()
        ''' If we set a too large interval, e.g., 1, we will have
            no result at all!
        '''
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
# It is better to do this in 2 lines, otherwise, we can receive errors
keylistener.start()

if __name__ == '__main__':
    wait_example()
