#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.shared as sh
from . import gui as gi


class ThirdParties:
    
    def __init__(self):
        file = sh.objs.get_pdir().add ('..','resources'
                                      ,'third parties.txt'
                                      )
        self.text = sh.ReadTextFile(file).get()
        self.gui = None
    
    def get_gui(self):
        if self.gui is None:
            self.set_gui()
        return self.gui
    
    def set_gui(self):
        self.gui = gi.ThirdParties()
        self.gui.obj.insert(text=self.text)
        self.gui.obj.disable()
    
    def show(self,event=None):
        self.get_gui().show()

    def close(self,event=None):
        self.get_gui().close()
