#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.shared as sh


class Suggest:
    #TODO: make this widget reusable
    def __init__(self):
        self.parent = None
        
    def set_bindings(self):
        sh.com.bind (obj = self.parent
                    ,bindings = '<Escape>'
                    ,action = self.close
                    )
        
    def show(self,lst=['a','b','c'],action=None):
        if not self.parent:
            self.parent = sh.Top(Lock=False)
            self.parent.widget.wm_overrideredirect(1)
            self.lbox = sh.ListBox (parent = self.parent
                                   ,lst = lst
                                   ,action = action
                                   )
            self.set_bindings()
                               
    def close(self):
        if self.parent:
            self.parent.kill()
            self.parent = None