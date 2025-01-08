#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import rep

from config import CONFIG
from popup.gui import Popup as guiPopup, HEIGHT, WIDTH


class Attach:
    
    def __init__(self, x1, width, y1, height, max_width, Center=False):
        self.px1 = self.px2 = self.py1 = self.py2 = 0
        self.x1 = x1
        self.y1 = y1
        self.width = width
        self.height = height
        self.max_width = max_width
        self.Center = Center
    
    def align_y(self):
        # Align widgets such that their top borders coincide
        self.py1 = self.y1 + int((HEIGHT - self.height) / 2)
        if self.py1 < 0:
            self.py1 = self.y1
    
    def center_y(self):
        # Align widgets such that center axes of cell and popup coincide
        self.py1 = self.y1
    
    def set_coords(self):
        self.x2 = self.x1 + self.width
        self.y2 = self.y1 + self.height
        if self.Center:
            self.center_y()
        else:
            self.align_y()
        self.py2 = self.py1 + HEIGHT
        self.px1 = self.x2
        self.px2 = self.px1 + WIDTH
    
    def adjust_y(self):
        if self.py1 < 0:
            self.py1 = 0
            self.py2 = HEIGHT
    
    def adjust_x(self):
        if self.px2 > self.max_width:
            self.px1 = self.x1 - WIDTH
            self.px2 = self.x1
            if self.px1 < 0:
                self.px1 = 0
                self.px2 = WIDTH
    
    def run(self):
        self.set_coords()
        self.adjust_x()
        self.adjust_y()
        return(int(self.px1), int(self.px2), int(self.py1), int(self.py2))



class Popup:
    
    def __init__(self):
        self.Shown = False
        self.gui = guiPopup()
        self.set_gui()
    
    def adjust_position(self, x1, width, y1, height, max_width, Center=False):
        px1, px2, py1, py2 = Attach(x1, width, y1, height, max_width, Center).run()
        self.gui.move(px1, py1)
    
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
        f = '[MClient] popup.controller.Popup.set_bindings'
        self.gui.bind(('Esc',), self.close)
        if not CONFIG.Success:
            rep.cancel(f)
            return
        self.gui.bind(CONFIG.new['actions']['toggle_popup']['hotkeys']
                     ,self.toggle)


POPUP = Popup()
