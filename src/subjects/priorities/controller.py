#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

from . import gui as gi


class Priorities:
    
    def __init__(self):
        self.Shown = False
        self.lst1 = []
        self.lst2 = []
        self.set_gui()
    
    def fill(self):
        self.fill1()
        self.fill2()
    
    def fill1(self):
        self.gui.fill1(self.lst1,_('In use'))
    
    def fill2(self):
        self.gui.fill2(self.lst2,_('Available'))
    
    def get_checkbox(self):
        return self.gui.get_checkbox()
    
    def set_checkbox(self,Active=False):
        self.gui.set_checkbox(Active)
    
    def set_all(self,event=None):
        self.Colorize2 = True
        self.lst2 = list(self.copy2)
        self.gui.reset2(self.lst2)
        self.colorize2()
    
    def set_article(self,event=None):
        self.Colorize2 = True
        self.lst2 = list(self.copy_art)
        self.gui.reset2(self.lst2)
        self.colorize2()
    
    def set_major(self,event=None):
        self.Colorize2 = False
        self.lst2 = list(self.majors)
        self.gui.reset2(self.lst2)
    
    def _get_index(self,items,item):
        f = '[MClient] subjects.priorities.controller.Priorities._get_index'
        try:
            return items.index(item)
        except ValueError:
            mes = _('Wrong input data: "{}"!').format(item)
            sh.objs.get_mes(f,mes).show_error()
    
    def unprioritize_group(self,event=None):
        f = '[MClient] subjects.priorities.controller.Priorities.unprioritize_group'
        if not self.func_group:
            mes = _('An external function is not set!')
            sh.objs.get_mes(f,mes,True).show_error()
            return
        items = []
        sel1 = self.get_sel1()
        if not sel1:
            sh.com.rep_lazy(f)
            return
        for item in sel1:
            group = self.func_group(item)
            if group:
                items += group
            else:
                sh.com.rep_empty(f)
        Add = False
        for item in items:
            if not item in self.lst1:
                Add = True
                self.lst1.append(item)
        if Add:
            self.gui.reset1(self.lst1)
        indexes = []
        for item in items:
            index_ = self._get_index(self.lst1,item)
            if index_ is None:
                sh.com.rep_empty(f)
            else:
                indexes.append(index_)
        self.select_mult1(indexes)
        self.unprioritize()
    
    def prioritize_group(self,event=None):
        f = '[MClient] subjects.priorities.controller.Priorities.prioritize_group'
        if not self.func_group:
            mes = _('An external function is not set!')
            sh.objs.get_mes(f,mes,True).show_error()
            return
        items = []
        sel2 = self.get_sel2()
        if not sel2:
            sh.com.rep_lazy(f)
            return
        for item in sel2:
            group = self.func_group(item)
            if group:
                items += group
            else:
                sh.com.rep_empty(f)
        Add = False
        for item in items:
            if not item in self.lst2:
                Add = True
                self.lst2.append(item)
        if Add:
            self.gui.reset2(self.lst2)
        indexes = []
        for item in items:
            index_ = self._get_index(self.lst2,item)
            if index_ is None:
                sh.com.rep_empty(f)
            else:
                indexes.append(index_)
        self.select_mult2(indexes)
        self.prioritize()
    
    def _get_cuts1(self):
        f = '[MClientQt] subjects.priorities.controller.Priorities._get_cuts1'
        indexes = self.gui.get_index_mult1()
        if not indexes:
            sh.com.rep_lazy(f)
            return
        cutsi = sh.List(indexes).split_by_gaps()
        if not cutsi:
            sh.com.rep_empty(f)
            return
        cuts = []
        for cuti in cutsi:
            cut = []
            for index_ in cuti:
                cut.append(self.lst1[index_])
            cuts.append(cut)
        cutsi = cutsi[::-1]
        for cuti in cutsi:
            cuti = cuti[::-1]
            for i in cuti:
                del self.lst1[i]
        cutsi = cutsi[::-1]
        return(cuts,cutsi)
    
    def move_top(self,event=None):
        f = '[MClient] subjects.priorities.controller.Priorities.move_top'
        result = self._get_cuts1()
        if not result:
            sh.com.rep_empty(f)
            return
        cuts, cutsi = result[0], result[1]
        cuts = cuts[::-1]
        count = 0
        for row in cuts:
            row = row[::-1]
            for item in row:
                count += 1
                self.lst1.insert(0,item)
        moved = [i for i in range(count)]
        self.gui.reset1(self.lst1)
        self.select_mult1(moved)
    
    def select_mult1(self,indexes):
        f = '[MClient] subjects.priorities.controller.Priorities.select_mult1'
        if not indexes:
            sh.com.rep_empty(f)
            return
        try:
            self.gui.select_mult1(indexes)
        except Exception as e:
            mes = _('Operation has failed!\nDetails: {}').format(e)
            sh.objs.get_mes(f,mes).show_warning()
    
    def select_mult2(self,indexes):
        f = '[MClient] subjects.priorities.controller.Priorities.select_mult2'
        if not indexes:
            sh.com.rep_empty(f)
            return
        try:
            self.gui.select_mult2(indexes)
        except Exception as e:
            mes = _('Operation has failed!\nDetails: {}').format(e)
            sh.objs.get_mes(f,mes).show_warning()
    
    def colorize1(self):
        for i in range(len(self.lst1)):
            if self.lst1[i] in self.majors:
                self.gui.colorize1(i)
    
    def colorize2(self):
        f = '[MClient] subjects.priorities.controller.Priorities.colorize2'
        if not self.Colorize2:
            sh.com.rep_lazy(f)
            return
        for i in range(len(self.lst2)):
            if self.lst2[i] in self.majors:
                self.gui.colorize2(i)
    
    def clear_sel(self,event=None):
        self.clear_sel1()
        self.clear_sel2()
    
    def clear_sel1(self):
        self.gui.clear_sel1()
    
    def clear_sel2(self):
        self.gui.clear_sel2()
    
    def get_sel1(self,event=None):
        return self.gui.get_sel1()
    
    def get_sel2(self,event=None):
        return self.gui.get_sel2()
    
    def get1(self,event=None):
        return self.gui.get1()
    
    def get2(self,event=None):
        return self.gui.get2()
    
    def set_gui(self):
        self.gui = gi.Priorities()
        self.set_bindings()
    
    def move_bottom(self,event=None):
        f = '[MClient] subjects.priorities.controller.Priorities.move_bottom'
        result = self._get_cuts1()
        if not result:
            sh.com.rep_empty(f)
            return
        cuts, cutsi = result[0], result[1]
        selection = []
        for row in cuts:
            for item in row:
                selection.append(item)
        index1 = len(self.lst1)
        index2 = index1 + len(selection)
        self.lst1 += selection
        moved = [i for i in range(index1,index2)]
        self.gui.reset1(self.lst1)
        self.select_mult1(moved)
    
    def increase(self,event=None):
        f = '[MClient] subjects.priorities.controller.Priorities.increase'
        result = self._get_cuts1()
        if not result:
            sh.com.rep_empty(f)
            return
        cuts, cutsi = result[0], result[1]
        for i in range(len(cuts)):
            index_ = cutsi[i][0]
            if index_ > 0:
                index_ -= 1
            paste = cuts[i][::-1]
            for j in range(len(paste)):
                self.lst1.insert(index_,paste[j])
        self.gui.reset1(self.lst1)
        for cuti in cutsi:
            moved = []
            for index_ in cuti:
                if index_ > 0:
                    moved.append(index_-1)
                else:
                    moved.append(index_)
            self.select_mult1(moved)
    
    def decrease(self,event=None):
        f = '[MClient] subjects.priorities.controller.Priorities.decrease'
        result = self._get_cuts1()
        if not result:
            sh.com.rep_empty(f)
            return
        cuts, cutsi = result[0], result[1]
        for i in range(len(cuts)):
            index_ = cutsi[i][0]
            index_ += 1
            paste = cuts[i][::-1]
            for j in range(len(paste)):
                self.lst1.insert(index_,paste[j])
        self.gui.reset1(self.lst1)
        for cuti in cutsi:
            moved = []
            for index_ in cuti:
                moved.append(index_+1)
            self.select_mult1(moved)
    
    def prioritize(self,event=None):
        f = '[MClientQt] subjects.priorities.controller.Priorities.prioritize'
        sel2 = self.get_sel2()
        if not sel2:
            sh.com.rep_empty(f)
            return
        sel2 = [item for item in sel2 if not item in self.lst1]
        self.lst1 += sel2
        self.lst2 = [item for item in self.lst2 if not item in sel2]
        self.gui.reset1(self.lst1)
        self.gui.reset2(self.lst2)
        self.colorize2()
        index1 = len(self.lst1) - len(sel2)
        index2 = len(self.lst1)
        indexes = [i for i in range(index1,index2+1)]
        self.select_mult1(indexes)
    
    def unprioritize(self,event=None):
        f = '[MClient] subjects.priorities.controller.Priorities.unprioritize'
        sel1 = self.get_sel1()
        if not sel1:
            sh.com.rep_empty(f)
            return
        add = [item for item in sel1 if not item in self.lst2]
        self.lst2 += add
        self.lst1 = [item for item in self.lst1 if not item in sel1]
        self.gui.reset1(self.lst1)
        self.gui.reset2(self.lst2)
        self.colorize2()
        index1 = len(self.lst2) - len(add)
        index2 = len(self.lst2)
        indexes = [i for i in range(index1,index2+1)]
        self.select_mult2(indexes)
    
    def show(self):
        self.Shown = True
        self.gui.show()
        self.gui.resize(800,450)
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
        f = '[MClientQt] subjects.priorities.controller.Priorities.reload'
        print(f)
    
    def set_bindings(self):
        self.gui.bind('Esc',self.close)
        self.gui.btn_btm.set_action(self.move_bottom)
        self.gui.btn_clr.set_action(self.clear_sel)
        self.gui.btn_dwn.set_action(self.decrease)
        self.gui.btn_grp.set_action(self.prioritize_group)
        self.gui.btn_gru.set_action(self.unprioritize_group)
        self.gui.btn_lft.set_action(self.prioritize)
        self.gui.btn_rht.set_action(self.unprioritize)
        self.gui.btn_rld.set_action(self.reload)
        self.gui.btn_top.set_action(self.move_top)
        self.gui.btn_up1.set_action(self.increase)
