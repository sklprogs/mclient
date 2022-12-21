#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt5.QtWidgets

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

from . import logic as lg
from . import gui as gi


class TableModel(gi.TableModel):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Welcome:
    
    def __init__(self):
        self.logic = lg.Welcome()
        self.set_gui()
    
    def set_gui(self):
        self.gui = gi.App()
        self.set_bindings()
    
    def set_font(self,text):
        return self.logic.set_font(text)
    
    def set_head(self):
        self.logic.set_head()
    
    def set_tail(self):
        self.logic.set_tail()
    
    def set_model(self,model):
        self.gui.set_model(model)
    
    def close(self):
        self.gui.close()
    
    def show(self):
        self.gui.show()
    
    def set_bindings(self):
        self.gui.bind('Ctrl+Q',self.close)
        self.gui.bind('Esc',self.close)
    
    def set_spans(self):
        for i in range(10):
            self.gui.set_span(i,0,1,lg.COLNUM)
    
    def set_col_widths(self):
        for i in range(lg.COLNUM):
            self.gui.set_col_width(i,166)
    
    def resize_rows(self):
        ''' This strange workaround allows to avoid too much space caused by
            spanning rows and resizing them to contents. I have also tried the
            following to no avail:
            vheader = self.verticalHeader()
            vheader.setSectionResizeMode(vheader.ResizeToContents)
            and
            vheader.setSectionResizeMode(vheader.Stretch)
            The first one doesn't work and the second one does not make row
            borders fully visible.
            https://stackoverflow.com/questions/52166539/qtablewidget-respect-span-when-sizing-to-contents
        '''
        self.gui.hide_rows((0,1,2,3,4,5,6,7,8,9))
        self.gui.resize_rows()
        self.gui.show_rows((0,1,2,3,4,5,6,7,8,9))
    
    def reset(self):
        self.fill()
        self.set_spans()
        self.set_col_widths()
        self.resize_rows()
    
    def fill(self):
        model = gi.TableModel(self.logic.run())
        self.gui.set_model(model)
