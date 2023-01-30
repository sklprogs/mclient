#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

from . import gui as gi


class Priorities:
    
    def __init__ (self,lst1=[],lst2=[],art_subjects=[]
                 ,majors=[],func_group=None
                 ):
        self.func_group = func_group
        self.Shown = False
        self.Colorize2 = True
        self.lst1 = []
        self.lst2 = []
        self.art_subjects = []
        self.copy1 = []
        self.copy2 = []
        self.copy_art = []
        self.majors = []
        self.set_gui()
        '''
        #cur
        if lst1:
            self.reset(lst1,lst2,art_subjects,majors)
        '''
    
    def get_checkbox(self):
        return self.gui.get_checkbox()
    
    def set_checkbox(self,Active=False):
        self.gui.set_checkbox(Active)
    
    def set_all(self,event=None):
        self.Colorize2 = True
        self.lst2 = list(self.copy2)
        self.get_gui().reset2(self.lst2)
        self.colorize2()
    
    def set_article(self,event=None):
        self.Colorize2 = True
        self.lst2 = list(self.copy_art)
        self.get_gui().reset2(self.lst2)
        self.colorize2()
    
    def set_major(self,event=None):
        self.Colorize2 = False
        self.lst2 = list(self.majors)
        self.get_gui().reset2(self.lst2)
    
    def _get_index(self,items,item):
        f = '[MClient] subjects.priorities.controller.Priorities._get_index'
        try:
            return items.index(item)
        except ValueError:
            mes = _('Wrong input data: "{}"!').format(item)
            sh.objs.get_mes(f,mes).show_error()
    
    def unprioritize_group(self,event=None):
        f = '[MClient] subjects.priorities.controller.Priorities.unprioritize_group'
        if self.func_group:
            items = []
            sel1 = self.get_sel1()
            if sel1:
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
            else:
                sh.com.rep_lazy(f)
        else:
            mes = _('An external function is not set!')
            sh.objs.get_mes(f,mes,True).show_error()
    
    def prioritize_group(self,event=None):
        f = '[MClient] subjects.priorities.controller.Priorities.prioritize_group'
        if self.func_group:
            items = []
            sel2 = self.get_sel2()
            if sel2:
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
            else:
                sh.com.rep_lazy(f)
        else:
            mes = _('An external function is not set!')
            sh.objs.get_mes(f,mes,True).show_error()
    
    def _get_cuts1(self):
        f = '[MClient] subjects.priorities.controller.Priorities._get_cuts1'
        indexes = self.get_gui().get_index_mult1()
        if indexes:
            cutsi = sh.List(indexes).split_by_gaps()
            if cutsi:
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
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.rep_lazy(f)
    
    def move_top(self,event=None):
        f = '[MClient] subjects.priorities.controller.Priorities.move_top'
        result = self._get_cuts1()
        if result:
            cuts, cutsi = result[0], result[1]
            cuts = cuts[::-1]
            count = 0
            for row in cuts:
                row = row[::-1]
                for item in row:
                    count += 1
                    self.lst1.insert(0,item)
            moved = [i for i in range(count)]
            self.get_gui().reset1(self.lst1)
            self.select_mult1(moved)
        else:
            sh.com.rep_empty(f)
    
    def select_mult1(self,indexes):
        f = '[MClient] subjects.priorities.controller.Priorities.select_mult1'
        if indexes:
            try:
                self.get_gui().select_mult1(indexes)
            except Exception as e:
                mes = _('Operation has failed!\nDetails: {}').format(e)
                sh.objs.get_mes(f,mes).show_warning()
        else:
            sh.com.rep_empty(f)
    
    def select_mult2(self,indexes):
        f = '[MClient] subjects.priorities.controller.Priorities.select_mult2'
        if indexes:
            try:
                self.get_gui().select_mult2(indexes)
            except Exception as e:
                mes = _('Operation has failed!\nDetails: {}').format(e)
                sh.objs.get_mes(f,mes).show_warning()
        else:
            sh.com.rep_empty(f)
    
    def colorize1(self):
        for i in range(len(self.lst1)):
            if self.lst1[i] in self.majors:
                self.gui.colorize1(i)
    
    def colorize2(self):
        f = '[MClient] subjects.priorities.controller.Priorities.colorize2'
        if self.Colorize2:
            for i in range(len(self.lst2)):
                if self.lst2[i] in self.majors:
                    self.gui.colorize2(i)
        else:
            sh.com.rep_lazy(f)
    
    def clear_sel(self,event=None):
        self.clear_sel1()
        self.clear_sel2()
    
    def clear_sel1(self):
        self.get_gui().clear_sel1()
    
    def clear_sel2(self):
        self.get_gui().clear_sel2()
    
    def get_sel1(self,event=None):
        return self.get_gui().get_sel1()
    
    def get_sel2(self,event=None):
        return self.get_gui().get_sel2()
    
    def get1(self,event=None):
        return self.get_gui().get1()
    
    def get2(self,event=None):
        return self.get_gui().get2()
    
    def reset(self,lst1=[],lst2=[],art_subjects=[],majors=[]):
        f = '[MClient] subjects.priorities.controller.Priorities.reset'
        # Convert tuples to lists at input in order to modify them
        if lst1:
            self.lst1 = list(lst1)
            self.copy1 = list(self.lst1)
        if lst2:
            self.lst2 = list(lst2)
            self.copy2 = list(self.lst2)
        if art_subjects:
            self.art_subjects = list(art_subjects)
            self.copy_art = list(art_subjects)
        if majors:
            self.majors = majors
        self.fill()
    
    def set_gui(self):
        self.gui = gi.Priorities()
        self.set_bindings()
    
    def fill(self):
        ''' #NOTE: Since a list of all subjects can be very long,
            use this code only where necessary. Only affected panes
            should be reset.
        '''
        self.get_gui().reset1(self.lst1)
        self.gui.reset2(self.lst2)
        self.colorize2()
    
    def reload(self,event=None):
        self.Colorize2 = True
        self.lst1 = list(self.copy1)
        self.lst2 = list(self.copy2)
        self.art_subjects = list(self.copy_art)
        self.fill()
    
    def move_bottom(self,event=None):
        f = '[MClient] subjects.priorities.controller.Priorities.move_bottom'
        result = self._get_cuts1()
        if result:
            cuts, cutsi = result[0], result[1]
            selection = []
            for row in cuts:
                for item in row:
                    selection.append(item)
            index1 = len(self.lst1)
            index2 = index1 + len(selection)
            self.lst1 += selection
            moved = [i for i in range(index1,index2)]
            self.get_gui().reset1(self.lst1)
            self.select_mult1(moved)
        else:
            sh.com.rep_empty(f)
    
    def increase(self,event=None):
        f = '[MClient] subjects.priorities.controller.Priorities.increase'
        result = self._get_cuts1()
        if result:
            cuts, cutsi = result[0], result[1]
            for i in range(len(cuts)):
                index_ = cutsi[i][0]
                if index_ > 0:
                    index_ -= 1
                paste = cuts[i][::-1]
                for j in range(len(paste)):
                    self.lst1.insert(index_,paste[j])
            self.get_gui().reset1(self.lst1)
            for cuti in cutsi:
                moved = []
                for index_ in cuti:
                    if index_ > 0:
                        moved.append(index_-1)
                    else:
                        moved.append(index_)
                self.select_mult1(moved)
        else:
            sh.com.rep_empty(f)
    
    def decrease(self,event=None):
        f = '[MClient] subjects.priorities.controller.Priorities.decrease'
        result = self._get_cuts1()
        if result:
            cuts, cutsi = result[0], result[1]
            for i in range(len(cuts)):
                index_ = cutsi[i][0]
                index_ += 1
                paste = cuts[i][::-1]
                for j in range(len(paste)):
                    self.lst1.insert(index_,paste[j])
            self.get_gui().reset1(self.lst1)
            for cuti in cutsi:
                moved = []
                for index_ in cuti:
                    moved.append(index_+1)
                self.select_mult1(moved)
        else:
            sh.com.rep_empty(f)
    
    def prioritize(self,event=None):
        f = '[MClient] subjects.priorities.controller.Priorities.prioritize'
        sel2 = self.get_sel2()
        if sel2:
            sel2 = [item for item in sel2 if not item in self.lst1]
            self.lst1 += sel2
            self.lst2 = [item for item in self.lst2 if not item in sel2]
            self.get_gui().reset1(self.lst1)
            self.gui.reset2(self.lst2)
            self.colorize2()
            index1 = len(self.lst1) - len(sel2)
            index2 = len(self.lst1)
            indexes = [i for i in range(index1,index2+1)]
            self.select_mult1(indexes)
        else:
            sh.com.rep_empty(f)
    
    def unprioritize(self,event=None):
        f = '[MClient] subjects.priorities.controller.Priorities.unprioritize'
        sel1 = self.get_sel1()
        if sel1:
            add = [item for item in sel1 if not item in self.lst2]
            self.lst2 += add
            self.lst1 = [item for item in self.lst1 if not item in sel1]
            self.get_gui().reset1(self.lst1)
            self.gui.reset2(self.lst2)
            self.colorize2()
            index1 = len(self.lst2) - len(add)
            index2 = len(self.lst2)
            indexes = [i for i in range(index1,index2+1)]
            self.select_mult2(indexes)
        else:
            sh.com.rep_empty(f)
    
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
