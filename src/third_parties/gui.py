#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.shared as sh

ICON = sh.objs.get_pdir().add('..','resources','icon_64x64_mclient.gif')


class ThirdParties:
    
    def __init__(self):
        self.set_gui()
        
    def set_bindings(self):
        sh.com.bind (obj = self.obj
                    ,bindings = ('<Escape>','<Control-q>','<Control-w>')
                    ,action = self.close
                    )
    
    def set_gui(self):
        title = _('Third parties') + ':'
        self.obj = sh.TextBoxRO (title = title
                                ,icon = ICON
                                )
        self.parent = self.obj.parent
        sh.Geometry(self.parent).set('800x600')
        self.set_bindings()
        self.obj.focus()
    
    def show(self,event=None):
        self.obj.show()
    
    def close(self,event=None):
        self.obj.close()
