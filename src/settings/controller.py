#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt5.QtWidgets

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

from . import gui as gi


class Settings:
    
    def __init__(self):
        self.Shown = False
        self.set_gui()
    
    def set_gui(self):
        self.gui = gi.Settings()
        self.set_title()
        self.set_bindings()
    
    def set_bindings(self):
        self.gui.bind('Ctrl+Q',self.close)
        self.gui.bind('Esc',self.close)
    
    def show(self):
        self.Shown = True
        self.gui.show()
        self.gui.centralize()
    
    def close(self):
        self.Shown = False
        self.gui.close()
    
    def set_title(self,title=_('Settings')):
        self.gui.set_title(title)
    
    def toggle(self):
        if self.Shown:
            self.close()
        else:
            self.show()


if __name__ == '__main__':
    f = '__main__'
    sh.com.start()
    app = Settings()
    app.show()
    sh.com.end()
