#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.shared as sh

from . import gui as gi


class Priorities:
    
    def __init__(self,lst1=[],lst2=[],lst3=[],majors=[],func_group=None):
        self.func_group = func_group
        self.gui = None
        self.lst1 = []
        self.lst2 = []
        self.lst3 = []
        self.copy1 = []
        self.copy2 = []
        self.copy3 = []
        self.majors = []
        if lst1:
            self.reset(lst1,lst2,lst3,majors)
    
    def get_checkbox(self):
        return self.gui.get_checkbox()
    
    def set_checkbox(self,Active=False):
        self.gui.set_checkbox(Active)
    
    def set_all(self,event=None):
        self.lst2 = list(self.copy2)
        self.get_gui().reset2(self.lst2)
        self.colorize2()
    
    def set_article(self,event=None):
        self.lst2 = list(self.copy3)
        self.get_gui().reset2(self.lst2)
        self.colorize2()
    
    def _get_index(self,items,item):
        f = '[MClient] priorities.controller.Priorities._get_index'
        try:
            return items.index(item)
        except ValueError:
            mes = _('Wrong input data: "{}"!').format(item)
            sh.objs.get_mes(f,mes).show_error()
    
    def move_group(self,event=None):
        f = '[MClient] priorities.controller.Priorities.move_group'
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
                indexes = []
                for item in items:
                    index_ = self._get_index(self.lst2,item)
                    if index_:
                        indexes.append(index_)
                    else:
                        sh.com.rep_empty(f)
                self.select_mult2(indexes)
                self.prioritize()
            else:
                sh.com.rep_lazy(f)
        else:
            mes = _('An external function is not set!')
            sh.objs.get_mes(f,mes,True).show_error()
    
    def _get_cuts1(self):
        f = '[MClient] priorities.controller.Priorities._get_cuts1'
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
        f = '[MClient] priorities.controller.Priorities.move_top'
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
            self.fill()
            self.select_mult1(moved)
        else:
            sh.com.rep_empty(f)
    
    def select_mult1(self,indexes):
        f = '[MClient] priorities.controller.Priorities.select_mult1'
        if indexes:
            try:
                self.get_gui().select_mult1(indexes)
            except Exception as e:
                mes = _('Operation has failed!\nDetails: {}').format(e)
                sh.objs.get_mes(f,mes).show_warning()
        else:
            sh.com.rep_empty(f)
    
    def select_mult2(self,indexes):
        f = '[MClient] priorities.controller.Priorities.select_mult2'
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
        for i in range(len(self.lst2)):
            if self.lst2[i] in self.majors:
                self.gui.colorize2(i)
    
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
    
    def reset(self,lst1=[],lst2=[],lst3=[],majors=[]):
        f = '[MClient] priorities.controller.Priorities.reset'
        # Convert tuples to lists at input in order to modify them
        if lst1:
            self.lst1 = list(lst1)
            self.copy1 = list(self.lst1)
        if lst2:
            self.lst2 = list(lst2)
            self.copy2 = list(self.lst2)
        if lst3:
            self.lst3 = list(lst3)
            self.copy3 = list(self.lst3)
        if majors:
            self.majors = majors
        self.fill()
    
    def get_gui(self):
        if self.gui is None:
            self.set_gui()
        return self.gui
    
    def set_gui(self):
        self.gui = gi.Priorities()
        self.set_bindings()
    
    def fill(self):
        self.get_gui().reset1(self.lst1)
        self.gui.reset2(self.lst2)
        self.colorize2()
    
    def reload(self,event=None):
        self.lst1 = list(self.copy1)
        self.lst2 = list(self.copy2)
        self.lst3 = list(self.copy3)
        self.fill()
    
    def move_bottom(self,event=None):
        f = '[MClient] priorities.controller.Priorities.move_bottom'
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
            self.fill()
            self.select_mult1(moved)
        else:
            sh.com.rep_empty(f)
    
    def increase(self,event=None):
        f = '[MClient] priorities.controller.Priorities.increase'
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
            self.fill()
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
        f = '[MClient] priorities.controller.Priorities.decrease'
        result = self._get_cuts1()
        if result:
            cuts, cutsi = result[0], result[1]
            for i in range(len(cuts)):
                index_ = cutsi[i][0]
                index_ += 1
                paste = cuts[i][::-1]
                for j in range(len(paste)):
                    self.lst1.insert(index_,paste[j])
            self.fill()
            for cuti in cutsi:
                moved = []
                for index_ in cuti:
                    moved.append(index_+1)
                self.select_mult1(moved)
        else:
            sh.com.rep_empty(f)
    
    def prioritize(self,event=None):
        f = '[MClient] priorities.controller.Priorities.prioritize'
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
        f = '[MClient] priorities.controller.Priorities.unprioritize'
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
    
    def show(self,event=None):
        self.get_gui().show()
    
    def close(self,event=None):
        self.get_gui().close()
    
    def set_bindings(self):
        f = '[MClient] priorities.controller.Priorities.set_bindings'
        if self.gui is None:
            sh.com.rep_empty(f)
            return
        sh.com.bind (obj = self.gui.parent
                    ,bindings = ('<Escape>','<Control-w>','<Control-q>')
                    ,action = self.close
                    )
        sh.com.bind (obj = self.gui.lbl_pri
                    ,bindings = '<ButtonRelease-1>'
                    ,action = self.gui.cbx_pri.toggle
                    )
        self.gui.btn_all.action = self.set_all
        self.gui.btn_art.action = self.set_article
        self.gui.btn_btm.action = self.move_bottom
        self.gui.btn_clr.action = self.clear_sel
        self.gui.btn_cls.action = self.close
        self.gui.btn_dwn.action = self.decrease
        self.gui.btn_grp.action = self.move_group
        self.gui.btn_lft.action = self.prioritize
        self.gui.btn_rht.action = self.unprioritize
        self.gui.btn_rld.action = self.reload
        self.gui.btn_top.action = self.move_top
        self.gui.btn_up1.action = self.increase
        self.gui.widget.protocol("WM_DELETE_WINDOW",self.close)
