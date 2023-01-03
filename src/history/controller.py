#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

from . import gui as gi


class TableModel(gi.TableModel):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class History:
    
    def __init__(self):
        self.Shown = False
        self.no = 0
        self.gui = gi.History()
        self.set_title()
        self.set_bindings()
    
    def set_model(self,model):
        self.gui.set_model(model)
    
    def add_row(self,lang1,lang2,search):
        self.no += 1
        row = [str(self.no),lang1,lang2,search]
        model = self.gui.get_model()
        model.items.insert(0,row)
        model.update()
    
    def set_title(self,title=_('History')):
        self.gui.set_title(title)
    
    def set_bindings(self):
        self.gui.bind('Esc',self.close)
    
    def show(self):
        self.Shown = True
        self.gui.show()
        self.gui.centralize()
    
    def close(self):
        self.Shown = False
        self.gui.close()
    
    def toggle(self):
        if self.Shown:
            self.close()
        else:
            self.show()
