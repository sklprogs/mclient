#!/usr/bin/python3
# -*- coding: UTF-8 -*-

class KeyListener:
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.status = 0

    def check(self):
        pass
    
    def run(self):
        pass

    def cancel(self):
        pass
    
    def start(self):
        pass


keylistener = KeyListener()
keylistener.start()
