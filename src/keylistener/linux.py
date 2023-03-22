#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import signal
import Xlib
import Xlib.X
import Xlib.XK
import Xlib.display
import threading


class KeyListener(threading.Thread):
    ''' Determine if hotkeys are pressed (globally in the system)
        Usage: keylistener = KeyListener()
        Initially: keylistener.addKeyListener("L_CTRL+L_SHIFT+y",callable)
        Note that it is necessary to bind all possible combinations because
        an order of key presses can be different, for example,
        "L_CTRL+y+L_SHIFT"
        Now: keylistener.addKeyListener("Control_L+c+c",callable)
    '''
    def __init__(self):
        threading.Thread.__init__(self)
        self.finished = threading.Event()
        self.contextEventMask = [Xlib.X.KeyPress,Xlib.X.MotionNotify]
        # Give these some initial values
        # Hook to our display.
        self.local_dpy = Xlib.display.Display()
        self.record_dpy = Xlib.display.Display()
        self.pressed = []
        self.listeners = {}
        self.character = None
        ''' 0: Nothing caught; 1: Read buffer and call main module;
            2: Call main module
        '''
        self.status = 0
        
    def lookup_keysym(self,keysym):
        ''' Need the following because XK.keysym_to_string() only does
            printable chars rather than being the correct inverse of
            XK.string_to_keysym().
        '''
        for name in dir(Xlib.XK):
            if name.startswith("XK_") and getattr(Xlib.XK,name) == keysym:
                return name.lstrip("XK_")
        return '[%d]' % keysym

    def processevents(self,reply):
        if reply.category != Xlib.ext.record.FromServer:
            return
        if reply.client_swapped:
            com.print_v('* received swapped protocol data, cowardly ignored')
            return
        # I added 'str', since we receive an error without it
        if not len(str(reply.data)) or ord(str(reply.data[0])) < 2:
            # Not an event
            return
        data = reply.data
        while len(data):
            event, data = Xlib.protocol.rq.EventField(None).parse_binary_value(data,self.record_dpy.display,None,None)
            keycode = event.detail
            keysym = self.local_dpy.keycode_to_keysym(event.detail,0)
            self.character = self.lookup_keysym(keysym)
            if self.character:
                if event.type == Xlib.X.KeyPress:
                    self.press()
                elif event.type == Xlib.X.KeyRelease:
                    self.release()

    def run(self):
        # Check if the extension is present
        if not self.record_dpy.has_extension('RECORD'):
            com.com.print_v('RECORD extension not found')
            sys.exit(1)
        r = self.record_dpy.record_get_version(0,0)
        mes = 'RECORD extension version {}.{}'.format (r.major_version
                                                      ,r.minor_version
                                                      )
        com.print_v(mes)
        # Create a recording context; we only want key events
        self.ctx = self.record_dpy.record_create_context (
                0
               ,[Xlib.ext.record.AllClients]
               ,[{
                  'core_requests'   : (0, 0)
                 ,'core_replies'    : (0, 0)
                 ,'ext_requests'    : (0, 0, 0, 0)
                 ,'ext_replies'     : (0, 0, 0, 0)
                 ,'delivered_events': (0, 0)
                 # (X.KeyPress, X.ButtonPress)
                 ,'device_events'   : tuple(self.contextEventMask)
                 ,'errors'          : (0, 0)
                 ,'client_started'  : False
                 ,'client_died'     : False
                 ,
                 }
                ]
                                                         )

        ''' Enable the context; this only returns after a call to
            record_disable_context, while calling the callback function in the
            meantime.
        '''
        self.record_dpy.record_enable_context(self.ctx,self.processevents)
        # Finally free the context
        self.record_dpy.record_free_context(self.ctx)

    def cancel(self):
        self.finished.set()
        self.local_dpy.record_disable_context(self.ctx)
        self.local_dpy.flush()

    def append(self):
        if len(self.pressed) > 0:
            if self.pressed[0] in ('Control_L','Control_R','Alt_L','Alt_R'):
                self.pressed.append(self.character)
    
    def press(self):
        if len(self.pressed) == 2:
            if self.pressed[1] == 'grave':
                self.pressed = []
        elif len(self.pressed) == 3:
            self.pressed = []
        if self.character in ('Control_L','Control_R','Alt_L','Alt_R'):
            self.pressed = [self.character]
        elif self.character in ('c','Insert','grave'):
            self.append()
        action = self.listeners.get(tuple(self.pressed), False)
        com.print_v('Current action:', str(tuple(self.pressed)))
        if action:
            action()

    def release(self):
        # Must be called whenever a key release event has occurred.
        # A released Control key is not taken into account
        # A cyrillic 'с' symbol is recognized as Latin 'c'
        if not self.character in ('c','Insert','grave'):
            self.pressed = []

    def add_listener(self,hotkeys,callable):
        keys = tuple(hotkeys.split('+'))
        com.print_v('Added new keylistener for :',str(keys))
        self.listeners[keys] = callable
        
    def check(self): # Returns 0..2
        if self.status:
            com.print_v('Hotkey has been caught!')
            status = self.status
            self.status = 0
            return status
            
    def set_status(self,status=0):
        self.status = status
        com.print_v('Setting status to %d!' % self.status)
    
    def set_bindings(self):
        self.add_listener ('Control_L+c+c'
                         ,lambda:self.set_status(status=1)
                         )
        self.add_listener ('Control_R+c+c'
                         ,lambda:self.set_status(status=1)
                         )
        self.add_listener ('Control_L+Insert+Insert'
                          ,lambda:self.set_status(status=1)
                          )
        self.add_listener ('Control_R+Insert+Insert'
                          ,lambda:self.set_status(status=1)
                          )
        self.add_listener ('Alt_L+grave'
                          ,lambda:self.set_status(status=2)
                          )
        self.add_listener ('Alt_R+grave'
                          ,lambda:self.set_status(status=2)
                          )



class Commands:
    
    def __init__(self):
        self.Verbose = False
        self.supress_ctrl_c()
    
    def supress_ctrl_c(self):
        # Do not quit when Control-c is pressed
        signal.signal(signal.SIGINT,self.catch_control_c)
    
    def print_v(self,*args):
        if self.Verbose:
            print(*args)

    def catch_control_c(self,*args):
        pass
    
    def start(self):
        objs.get_listener().set_bindings()
        objs.listener.start()



class Objects:
    
    def __init__(self):
        self.listener = None
    
    def get_listener(self):
        if self.listener is None:
            self.listener = KeyListener()
        return self.listener


objs = Objects()
com = Commands()
