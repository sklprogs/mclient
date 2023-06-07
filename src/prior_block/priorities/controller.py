#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
#import skl_shared_qt.shared as sh

from . import gui as gi


class Priorities:
    
    def __init__(self):
        self.Shown = False
        self.dic1 = {}
        self.dic2 = {}
        self.set_gui()
    
    def fill(self):
        self.fill1()
        self.fill2()
    
    def fill1(self):
        self.gui.fill1(self.dic1, _('In use'))
    
    def fill2(self):
        self.gui.fill2(self.dic2, _('Available'))
    
    def unprioritize_group(self):
        f = '[MClient] prior_block.priorities.controller.Priorities.unprioritize_group'
        print(f)
    
    def prioritize_group(self):
        f = '[MClient] prior_block.priorities.controller.Priorities.prioritize_group'
        print(f)
    
    def move_top(self):
        f = '[MClient] prior_block.priorities.controller.Priorities.move_top'
        print(f)
    
    def set_gui(self):
        self.gui = gi.Priorities()
        self.set_bindings()
    
    def move_bottom(self):
        f = '[MClient] prior_block.priorities.controller.Priorities.move_bottom'
        print(f)
    
    def increase(self):
        f = '[MClient] prior_block.priorities.controller.Priorities.increase'
        print(f)
        print(self.gui.get_index())
        print(self.gui.get_row())
    
    def decrease(self):
        f = '[MClient] prior_block.priorities.controller.Priorities.decrease'
        print(f)
    
    def prioritize(self):
        f = '[MClientQt] prior_block.priorities.controller.Priorities.prioritize'
        print(f)
    
    def unprioritize(self, event=None):
        f = '[MClient] prior_block.priorities.controller.Priorities.unprioritize'
        print(f)
    
    def show(self):
        self.Shown = True
        self.gui.show()
        self.gui.resize(800, 450)
        self.gui.centralize()
    
    def close(self):
        self.Shown = False
        self.gui.close()
    
    def toggle(self):
        if self.Shown:
            self.close()
        else:
            self.show()
    
    def reload(self):
        f = '[MClientQt] prior_block.priorities.controller.Priorities.reload'
        print(f)
    
    def set_bindings(self):
        self.gui.bind('Esc', self.close)
        self.gui.btn_btm.set_action(self.move_bottom)
        self.gui.btn_dwn.set_action(self.decrease)
        self.gui.btn_lft.set_action(self.prioritize)
        self.gui.btn_rht.set_action(self.unprioritize)
        self.gui.btn_top.set_action(self.move_top)
        self.gui.btn_up1.set_action(self.increase)
