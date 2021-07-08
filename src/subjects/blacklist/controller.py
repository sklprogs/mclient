#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.shared as sh

from . import gui as gi


class Blacklist:
    
    def __init__ (self,lst1=[],lst2=[],art_subjects=[]
                 ,majors=[],func_group=None
                 ):
        self.func_group = func_group
        self.gui = None
        self.Colorize2 = True
        self.lst1 = []
        self.lst2 = []
        self.art_subjects = []
        self.copy1 = []
        self.copy2 = []
        self.copy_art = []
        self.majors = []
        if lst1:
            self.reset(lst1,lst2,art_subjects,majors)
    
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
        f = '[MClient] subjects.blacklist.controller.Blacklist._get_index'
        try:
            return items.index(item)
        except ValueError:
            mes = _('Wrong input data: "{}"!').format(item)
            sh.objs.get_mes(f,mes).show_error()
    
    def unblock_group(self,event=None):
        f = '[MClient] subjects.blacklist.controller.Blacklist.unblock_group'
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
                self.unblock()
            else:
                sh.com.rep_lazy(f)
        else:
            mes = _('An external function is not set!')
            sh.objs.get_mes(f,mes,True).show_error()
    
    def block_group(self,event=None):
        f = '[MClient] subjects.blacklist.controller.Blacklist.block_group'
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
                self.block()
            else:
                sh.com.rep_lazy(f)
        else:
            mes = _('An external function is not set!')
            sh.objs.get_mes(f,mes,True).show_error()
    
    def _get_cuts1(self):
        f = '[MClient] subjects.blacklist.controller.Blacklist._get_cuts1'
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
    
    def select_mult1(self,indexes):
        f = '[MClient] subjects.blacklist.controller.Blacklist.select_mult1'
        if indexes:
            try:
                self.get_gui().select_mult1(indexes)
            except Exception as e:
                mes = _('Operation has failed!\nDetails: {}').format(e)
                sh.objs.get_mes(f,mes).show_warning()
        else:
            sh.com.rep_empty(f)
    
    def select_mult2(self,indexes):
        f = '[MClient] subjects.blacklist.controller.Blacklist.select_mult2'
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
        f = '[MClient] subjects.blacklist.controller.Blacklist.colorize2'
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
        f = '[MClient] subjects.blacklist.controller.Blacklist.reset'
        # Convert tuples to lists at input in order to modify them
        if lst1:
            self.lst1 = list(lst1)
            self.copy1 = list(self.lst1)
        if lst2:
            self.lst2 = list(lst2)
            self.copy2 = list(self.lst2)
        if art_subjects:
            self.art_subjects = list(art_subjects)
            self.copy_art = list(self.art_subjects)
        if majors:
            self.majors = majors
        self.fill()
    
    def get_gui(self):
        if self.gui is None:
            self.set_gui()
        return self.gui
    
    def set_gui(self):
        self.gui = gi.Blacklist()
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
    
    def block(self,event=None):
        f = '[MClient] subjects.blacklist.controller.Blacklist.block'
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
    
    def unblock(self,event=None):
        f = '[MClient] subjects.blacklist.controller.Blacklist.unblock'
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
        f = '[MClient] subjects.blacklist.controller.Blacklist.set_bindings'
        if self.gui is None:
            sh.com.rep_empty(f)
            return
        sh.com.bind (obj = self.gui.parent
                    ,bindings = ('<Escape>','<Control-w>','<Control-q>')
                    ,action = self.close
                    )
        sh.com.bind (obj = self.gui.lbl_blk
                    ,bindings = '<ButtonRelease-1>'
                    ,action = self.gui.cbx_blk.toggle
                    )
        self.gui.btn_all.action = self.set_all
        self.gui.btn_art.action = self.set_article
        self.gui.btn_clr.action = self.clear_sel
        self.gui.btn_cls.action = self.close
        self.gui.btn_grb.action = self.block_group
        self.gui.btn_gru.action = self.unblock_group
        self.gui.btn_lft.action = self.block
        self.gui.btn_mjr.action = self.set_major
        self.gui.btn_rht.action = self.unblock
        self.gui.btn_rld.action = self.reload
        self.gui.widget.protocol("WM_DELETE_WINDOW",self.close)
