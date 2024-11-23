#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from welcome.gui import WELCOME as guiWelcome, TableModel as guiTableModel
from welcome.logic import Welcome as lgWelcome, COLNUM


#TODO: Do we need this?
class TableModel(guiTableModel):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Welcome:
    
    def __init__(self, desc='Product Current Version'):
        self.gui = guiWelcome
        self.logic = lgWelcome()
        self.logic.desc = desc
    
    def hide_rows(self, rownos):
        self.gui.hide_rows(rownos)
    
    def show_rows(self, rownos):
        self.gui.show_rows(rownos)
    
    def set_font(self, text):
        return self.logic.set_font(text)
    
    def set_head(self):
        self.logic.set_head()
    
    def set_tail(self):
        self.logic.set_tail()
    
    def set_model(self, model):
        self.gui.set_model(model)
    
    def set_spans(self):
        for i in range(10):
            self.gui.set_span(i, 0, 1, COLNUM)
    
    def set_col_widths(self):
        for i in range(COLNUM):
            self.gui.set_col_width(i, 166)
    
    def resize_rows(self):
        ''' Create the table and fill the model before resizing rows, otherwise
            the latter will not work as expected and can cause segfaults.
            This strange workaround allows to avoid too much space caused by
            spanning rows and resizing them to contents.
            https://stackoverflow.com/questions/52166539/qtablewidget-respect-span-when-sizing-to-contents
        '''
        self.set_col_widths()
        self.set_spans()
        self.hide_rows((0, 1, 2, 3, 4, 5, 6, 7, 8))
        self.gui.resize_rows()
        self.show_rows((0, 1, 2, 3, 4, 5, 6, 7, 8))
    
    def reset(self):
        #self.set_col_widths()
        self.fill()
    
    def fill(self):
        model = guiTableModel(self.logic.run())
        self.gui.set_model(model)
