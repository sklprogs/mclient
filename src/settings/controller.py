#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt5.QtWidgets

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

from . import gui as gi


class Load:
    
    def __init__(self):
        self.gui = objs.get_settings().gui
    
    def load_style_area(self):
        self.gui.opt_stl.set(sh.lg.globs['str']['style'])
        self.gui.opt_cl1.set(sh.lg.globs['str']['col1_type'])
        self.gui.opt_cl2.set(sh.lg.globs['str']['col2_type'])
        self.gui.opt_cl3.set(sh.lg.globs['str']['col3_type'])
        self.gui.opt_cl4.set(sh.lg.globs['str']['col4_type'])
    
    def load_speech_area(self):
        self.gui.opt_sp1.set(sh.lg.globs['str']['speech1'])
        self.gui.opt_sp2.set(sh.lg.globs['str']['speech2'])
        self.gui.opt_sp3.set(sh.lg.globs['str']['speech3'])
        self.gui.opt_sp4.set(sh.lg.globs['str']['speech4'])
        self.gui.opt_sp5.set(sh.lg.globs['str']['speech5'])
        self.gui.opt_sp6.set(sh.lg.globs['str']['speech6'])
        self.gui.opt_sp7.set(sh.lg.globs['str']['speech7'])
    
    def load_checkboxes(self):
        self.gui.cbx_no1.set(sh.lg.globs['bool']['SortByColumns'])
        self.gui.cbx_no2.set(sh.lg.globs['bool']['ShortSubjects'])
        self.gui.cbx_no3.set(sh.lg.globs['bool']['ShortSpeech'])
        self.gui.cbx_no4.set(sh.lg.globs['bool']['ShowUserNames'])
        self.gui.cbx_no5.set(sh.lg.globs['bool']['Iconify'])
        self.gui.cbx_no6.set(sh.lg.globs['bool']['Autocompletion'])
        self.gui.cbx_no7.set(sh.lg.globs['bool']['Autoswap'])
        self.gui.cbx_no8.set(sh.lg.globs['bool']['PhraseCount'])
        self.gui.cbx_no9.set(sh.lg.globs['bool']['AdjustByWidth'])
    
    def load_col_widths(self):
        self.gui.ent_num.reset()
        self.gui.ent_fix.reset()
        self.gui.ent_trm.reset()
        self.gui.ent_num.insert(sh.lg.globs['int']['colnum'])
        self.gui.ent_fix.insert(sh.lg.globs['int']['fixed_col_width'])
        self.gui.ent_trm.insert(sh.lg.globs['int']['term_col_width'])
    
    def run(self):
        self.load_style_area()
        self.load_speech_area()
        self.load_checkboxes()
        self.load_col_widths()



class Save:
    
    def __init__(self):
        self.gui = objs.get_settings().gui
    
    def save_speech_area(self):
        sh.lg.globs['str']['speech1'] = self.gui.opt_sp1.get()
        sh.lg.globs['str']['speech2'] = self.gui.opt_sp2.get()
        sh.lg.globs['str']['speech3'] = self.gui.opt_sp3.get()
        sh.lg.globs['str']['speech4'] = self.gui.opt_sp4.get()
        sh.lg.globs['str']['speech5'] = self.gui.opt_sp5.get()
        sh.lg.globs['str']['speech6'] = self.gui.opt_sp6.get()
        sh.lg.globs['str']['speech7'] = self.gui.opt_sp7.get()
    
    def save_style_area(self):
        sh.lg.globs['str']['style'] = self.gui.opt_stl.get()
        sh.lg.globs['str']['col1_type'] = self.gui.opt_cl1.get()
        sh.lg.globs['str']['col2_type'] = self.gui.opt_cl2.get()
        sh.lg.globs['str']['col3_type'] = self.gui.opt_cl3.get()
        sh.lg.globs['str']['col4_type'] = self.gui.opt_cl4.get()
    
    def save_checkboxes(self):
        sh.lg.globs['bool']['SortByColumns'] = self.gui.cbx_no1.get()
        sh.lg.globs['bool']['ShortSubjects'] = self.gui.cbx_no2.get()
        sh.lg.globs['bool']['ShortSpeech'] = self.gui.cbx_no3.get()
        sh.lg.globs['bool']['ShowUserNames'] = self.gui.cbx_no4.get()
        sh.lg.globs['bool']['Iconify'] = self.gui.cbx_no5.get()
        sh.lg.globs['bool']['Autocompletion'] = self.gui.cbx_no6.get()
        sh.lg.globs['bool']['Autoswap'] = self.gui.cbx_no7.get()
        sh.lg.globs['bool']['PhraseCount'] = self.gui.cbx_no8.get()
        sh.lg.globs['bool']['AdjustByWidth'] = self.gui.cbx_no9.get()
    
    def _report_wrong_range(self,f,start,end):
        mes = _('A value of this field should be within the range of {}-{}!')
        mes = mes.format(start,end)
        sh.objs.get_mes(f,mes).show_warning()
    
    def save_col_num(self):
        f = '[MClientQt] settings.controller.Save.save_col_num'
        ''' #TODO: Do we need this?
        if not sh.lg.globs['bool']['AdjustByWidth']:
            sh.com.rep_lazy(f)
            return
        '''
        col_num = self.gui.ent_num.get()
        col_num = sh.Input(f,col_num).get_integer()
        if not 0 < col_num <= 10:
            self._report_wrong_range(f,1,10)
            col_num = 5
            self.gui.ent_num.reset()
            self.gui.ent_num.insert(col_num)
        sh.lg.globs['int']['colnum'] = col_num
    
    def save_fixed_col_width(self):
        f = '[MClientQt] settings.controller.Save.save_fixed_col_width'
        width = self.gui.ent_fix.get()
        width = sh.Input(f,width).get_integer()
        if not 50 <= width <= 512:
            self._report_wrong_range(f,50,512)
            width = 63
            self.gui.ent_fix.reset()
            self.gui.ent_fix.insert(width)
        sh.lg.globs['int']['fixed_col_width'] = width
    
    def save_term_col_width(self):
        f = '[MClientQt] settings.controller.Save.save_term_col_width'
        width = self.gui.ent_trm.get()
        width = sh.Input(f,width).get_integer()
        if not 50 <= width <= 512:
            self._report_wrong_range(f,50,512)
            width = 157
            self.gui.ent_trm.reset()
            self.gui.ent_trm.insert(width)
        sh.lg.globs['int']['term_col_width'] = width
    
    def run(self):
        self.save_style_area()
        self.save_speech_area()
        self.save_checkboxes()
        self.save_fixed_col_width()
        self.save_term_col_width()
        self.save_col_num()



class Settings:
    
    def __init__(self):
        self.Shown = False
        self.set_gui()
    
    def set_gui(self):
        self.gui = gi.Settings()
        self.set_title()
        self.set_bindings()
    
    def set_bindings(self):
        self.gui.bind('Ctrl+Q',self.close)
        self.gui.bind('Esc',self.close)
    
    def show(self):
        self.Shown = True
        Load().run()
        self.gui.show()
        self.gui.centralize()
    
    def close(self):
        self.Shown = False
        self.gui.close()
    
    def set_title(self,title=_('Settings')):
        self.gui.set_title(title)
    
    def toggle(self):
        if self.Shown:
            self.close()
        else:
            self.show()



class Objects:
    
    def __init__(self):
        self.settings = None
    
    def get_settings(self):
        if self.settings is None:
            self.settings = Settings()
        return self.settings


objs = Objects()
