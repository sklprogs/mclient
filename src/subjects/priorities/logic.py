#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class Priorities:
    
    def __init__(self):
        self.dic1 = {}
        self.dic2 = {}
    
    def reset(self,dic1,dic2):
        self.dic1 = dic1
        self.dic2 = dic2
    
    def delete1(self):
        f = '[MClientQt] subjects.priorities.logic.Priorities.delete1'
        try:
            del self.dic1[self.pos1]
            return True
        except IndexError:
            mes = _('Wrong input data: "{}"!').format(self.pos1)
            sh.objs.get_mes(f,mes).show_error()
    
    def move_up(self):
        if not self.delete1():
            return
        if self.pos1 == 0:
            return
        del self.dic1[self.pos1]
        self.pos1 -= 1
