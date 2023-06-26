#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

from . import gui as gi


class Popup:
    
    def __init__(self):
        self.Shown = False
        self.gui = gi.Popup()
        self.set_gui()
    
    def adjust_position(self, x, y):
        self.gui.move(x, y)
    
    def toggle(self):
        if self.Shown:
            self.close()
        else:
            self.show()
    
    def fill(self, text):
        self.gui.fill(text)
    
    def set_title(self, title=_('Full cell text')):
        self.gui.set_title(title)
    
    def set_gui(self):
        self.set_bindings()
        self.set_title()
    
    def show(self):
        self.Shown = True
        self.gui.show()
    
    def close(self):
        self.Shown = False
        self.gui.close()
    
    def set_bindings(self):
        self.gui.bind('Esc', self.close)
        self.gui.bind(sh.lg.globs['str']['bind_toggle_popup'], self.toggle)
