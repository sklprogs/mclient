#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message
from skl_shared_qt.logic import Input

import config as cf
from settings.gui import Settings as guiSettings


class Load:
    
    def __init__(self):
        self.gui = objs.get_settings().gui
    
    def load_style_area(self):
        self.gui.opt_stl.set(cf.objs.get_config().new['style'])
        self.gui.opt_cl1.set(cf.objs.config.new['columns']['1']['type'])
        self.gui.opt_cl2.set(cf.objs.config.new['columns']['2']['type'])
        self.gui.opt_cl3.set(cf.objs.config.new['columns']['3']['type'])
        self.gui.opt_cl4.set(cf.objs.config.new['columns']['4']['type'])
    
    def load_speech_area(self):
        self.gui.opt_sp1.set(cf.objs.get_config().new['speech1'])
        self.gui.opt_sp2.set(cf.objs.config.new['speech2'])
        self.gui.opt_sp3.set(cf.objs.config.new['speech3'])
        self.gui.opt_sp4.set(cf.objs.config.new['speech4'])
        self.gui.opt_sp5.set(cf.objs.config.new['speech5'])
        self.gui.opt_sp6.set(cf.objs.config.new['speech6'])
        self.gui.opt_sp7.set(cf.objs.config.new['speech7'])
    
    def load_checkboxes(self):
        self.gui.cbx_no1.set(cf.objs.get_config().new['SortByColumns'])
        self.gui.cbx_no2.set(cf.objs.config.new['ShortSubjects'])
        self.gui.cbx_no3.set(cf.objs.config.new['ShortSpeech'])
        self.gui.cbx_no4.set(cf.objs.config.new['ShowUserNames'])
        self.gui.cbx_no5.set(cf.objs.config.new['Iconify'])
        self.gui.cbx_no6.set(cf.objs.config.new['Autoswap'])
        self.gui.cbx_no7.set(cf.objs.config.new['PhraseCount'])
        if cf.objs.config.new['rows']['height'] == 0:
            self.gui.cbx_no8.enable()
        else:
            self.gui.cbx_no8.disable()
    
    def load_col_widths(self):
        self.gui.ent_num.reset()
        self.gui.ent_fix.reset()
        self.gui.ent_trm.reset()
        self.gui.ent_num.insert(cf.objs.get_config().new['columns']['num'])
        self.gui.ent_fix.insert(cf.objs.config.new['columns']['fixed']['width'])
        self.gui.ent_trm.insert(cf.objs.config.new['columns']['terms']['width'])
    
    def run(self):
        self.load_style_area()
        self.load_speech_area()
        self.load_checkboxes()
        self.load_col_widths()



class Save:
    
    def __init__(self):
        self.gui = objs.get_settings().gui
    
    def save_speech_area(self):
        cf.objs.get_config().new['speech1'] = self.gui.opt_sp1.get()
        cf.objs.config.new['speech2'] = self.gui.opt_sp2.get()
        cf.objs.config.new['speech3'] = self.gui.opt_sp3.get()
        cf.objs.config.new['speech4'] = self.gui.opt_sp4.get()
        cf.objs.config.new['speech5'] = self.gui.opt_sp5.get()
        cf.objs.config.new['speech6'] = self.gui.opt_sp6.get()
        cf.objs.config.new['speech7'] = self.gui.opt_sp7.get()
    
    def save_style_area(self):
        cf.objs.get_config().new['style'] = self.gui.opt_stl.get()
        cf.objs.config.new['columns']['1']['type'] = self.gui.opt_cl1.get()
        cf.objs.config.new['columns']['2']['type'] = self.gui.opt_cl2.get()
        cf.objs.config.new['columns']['3']['type'] = self.gui.opt_cl3.get()
        cf.objs.config.new['columns']['4']['type'] = self.gui.opt_cl4.get()
    
    def save_checkboxes(self):
        cf.objs.get_config().new['SortByColumns'] = self.gui.cbx_no1.get()
        cf.objs.config.new['ShortSubjects'] = self.gui.cbx_no2.get()
        cf.objs.config.new['ShortSpeech'] = self.gui.cbx_no3.get()
        cf.objs.config.new['ShowUserNames'] = self.gui.cbx_no4.get()
        cf.objs.config.new['Iconify'] = self.gui.cbx_no5.get()
        cf.objs.config.new['Autoswap'] = self.gui.cbx_no6.get()
        cf.objs.config.new['PhraseCount'] = self.gui.cbx_no7.get()
        #TODO: Rework
        if self.gui.cbx_no8.get():
            cf.objs.config.new['rows']['height'] = 0
    
    def _report_wrong_range(self, f, start, end):
        mes = _('A value of this field should be within the range of {}-{}!')
        mes = mes.format(start, end)
        Message(f, mes, True).show_warning()
    
    def save_col_num(self):
        f = '[MClient] settings.controller.Save.save_col_num'
        col_num = self.gui.ent_num.get()
        col_num = Input(f, col_num).get_integer()
        if not 0 < col_num <= 10:
            self._report_wrong_range(f, 1, 10)
            col_num = 5
            self.gui.ent_num.reset()
            self.gui.ent_num.insert(col_num)
        cf.objs.get_config().new['columns']['num'] = col_num
    
    def save_fixed_col_width(self):
        f = '[MClient] settings.controller.Save.save_fixed_col_width'
        width = self.gui.ent_fix.get()
        width = Input(f, width).get_integer()
        if not 50 <= width <= 512:
            self._report_wrong_range(f, 50, 512)
            width = 63
            self.gui.ent_fix.reset()
            self.gui.ent_fix.insert(width)
        cf.objs.get_config().new['columns']['fixed']['width'] = width
    
    def save_term_col_width(self):
        f = '[MClient] settings.controller.Save.save_term_col_width'
        width = self.gui.ent_trm.get()
        width = Input(f, width).get_integer()
        if not 50 <= width <= 512:
            self._report_wrong_range(f, 50, 512)
            width = 157
            self.gui.ent_trm.reset()
            self.gui.ent_trm.insert(width)
        cf.objs.get_config().new['columns']['terms']['width'] = width
    
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
        self.gui = guiSettings()
        self.set_title()
        self.set_bindings()
    
    def set_bindings(self):
        self.gui.bind(('Ctrl+Q',), self.close)
        self.gui.bind(('Esc',), self.close)
    
    def show(self):
        self.Shown = True
        Load().run()
        self.gui.show()
        self.gui.centralize()
    
    def close(self):
        self.Shown = False
        self.gui.close()
    
    def set_title(self, title=_('Settings')):
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
