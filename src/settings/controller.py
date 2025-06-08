#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message
from skl_shared.logic import Input

from config import CONFIG
from settings.gui import Settings as guiSettings


class Load:
    
    def load_style_area(self):
        SETTINGS.gui.opt_stl.set(CONFIG.new['style'])
        SETTINGS.gui.opt_cl1.set(CONFIG.new['columns']['1']['type'])
        SETTINGS.gui.opt_cl2.set(CONFIG.new['columns']['2']['type'])
        SETTINGS.gui.opt_cl3.set(CONFIG.new['columns']['3']['type'])
        SETTINGS.gui.opt_cl4.set(CONFIG.new['columns']['4']['type'])
    
    def load_speech_area(self):
        SETTINGS.gui.opt_sp1.set(CONFIG.new['speech1'])
        SETTINGS.gui.opt_sp2.set(CONFIG.new['speech2'])
        SETTINGS.gui.opt_sp3.set(CONFIG.new['speech3'])
        SETTINGS.gui.opt_sp4.set(CONFIG.new['speech4'])
        SETTINGS.gui.opt_sp5.set(CONFIG.new['speech5'])
        SETTINGS.gui.opt_sp6.set(CONFIG.new['speech6'])
        SETTINGS.gui.opt_sp7.set(CONFIG.new['speech7'])
    
    def load_checkboxes(self):
        SETTINGS.gui.cbx_no1.set(CONFIG.new['SortByColumns'])
        SETTINGS.gui.cbx_no2.set(CONFIG.new['ShortSubjects'])
        SETTINGS.gui.cbx_no3.set(CONFIG.new['ShortSpeech'])
        SETTINGS.gui.cbx_no4.set(CONFIG.new['ShowUserNames'])
        SETTINGS.gui.cbx_no5.set(CONFIG.new['Iconify'])
        SETTINGS.gui.cbx_no6.set(CONFIG.new['Autoswap'])
        SETTINGS.gui.cbx_no7.set(CONFIG.new['PhraseCount'])
        if CONFIG.new['rows']['height'] == 0:
            SETTINGS.gui.cbx_no8.enable()
        else:
            SETTINGS.gui.cbx_no8.disable()
    
    def load_col_widths(self):
        SETTINGS.gui.ent_num.reset()
        SETTINGS.gui.ent_fix.reset()
        SETTINGS.gui.ent_trm.reset()
        SETTINGS.gui.ent_num.insert(CONFIG.new['columns']['num'])
        SETTINGS.gui.ent_fix.insert(CONFIG.new['columns']['fixed']['width'])
        SETTINGS.gui.ent_trm.insert(CONFIG.new['columns']['terms']['width'])
    
    def run(self):
        self.load_style_area()
        self.load_speech_area()
        self.load_checkboxes()
        self.load_col_widths()



class Save:
    
    def save_speech_area(self):
        CONFIG.new['speech1'] = SETTINGS.gui.opt_sp1.get()
        CONFIG.new['speech2'] = SETTINGS.gui.opt_sp2.get()
        CONFIG.new['speech3'] = SETTINGS.gui.opt_sp3.get()
        CONFIG.new['speech4'] = SETTINGS.gui.opt_sp4.get()
        CONFIG.new['speech5'] = SETTINGS.gui.opt_sp5.get()
        CONFIG.new['speech6'] = SETTINGS.gui.opt_sp6.get()
        CONFIG.new['speech7'] = SETTINGS.gui.opt_sp7.get()
    
    def save_style_area(self):
        CONFIG.new['style'] = SETTINGS.gui.opt_stl.get()
        CONFIG.new['columns']['1']['type'] = SETTINGS.gui.opt_cl1.get()
        CONFIG.new['columns']['2']['type'] = SETTINGS.gui.opt_cl2.get()
        CONFIG.new['columns']['3']['type'] = SETTINGS.gui.opt_cl3.get()
        CONFIG.new['columns']['4']['type'] = SETTINGS.gui.opt_cl4.get()
    
    def save_checkboxes(self):
        CONFIG.new['SortByColumns'] = SETTINGS.gui.cbx_no1.get()
        CONFIG.new['ShortSubjects'] = SETTINGS.gui.cbx_no2.get()
        CONFIG.new['ShortSpeech'] = SETTINGS.gui.cbx_no3.get()
        CONFIG.new['ShowUserNames'] = SETTINGS.gui.cbx_no4.get()
        CONFIG.new['Iconify'] = SETTINGS.gui.cbx_no5.get()
        CONFIG.new['Autoswap'] = SETTINGS.gui.cbx_no6.get()
        CONFIG.new['PhraseCount'] = SETTINGS.gui.cbx_no7.get()
        if SETTINGS.gui.cbx_no8.get():
            CONFIG.new['rows']['height'] = 0
        elif CONFIG.new['rows']['height'] == 0:
            CONFIG.new['rows']['height'] = 42
    
    def _report_wrong_range(self, f, start, end):
        mes = _('A value of this field should be within the range of {}-{}!')
        mes = mes.format(start, end)
        Message(f, mes, True).show_warning()
    
    def save_col_num(self):
        f = '[MClient] settings.controller.Save.save_col_num'
        col_num = SETTINGS.gui.ent_num.get()
        col_num = Input(f, col_num).get_integer()
        if not 0 < col_num <= 10:
            self._report_wrong_range(f, 1, 10)
            col_num = 5
            SETTINGS.gui.ent_num.reset()
            SETTINGS.gui.ent_num.insert(col_num)
        CONFIG.new['columns']['num'] = col_num
    
    def save_fixed_col_width(self):
        f = '[MClient] settings.controller.Save.save_fixed_col_width'
        width = SETTINGS.gui.ent_fix.get()
        width = Input(f, width).get_integer()
        if not 50 <= width <= 512:
            self._report_wrong_range(f, 50, 512)
            width = 63
            SETTINGS.gui.ent_fix.reset()
            SETTINGS.gui.ent_fix.insert(width)
        CONFIG.new['columns']['fixed']['width'] = width
    
    def save_term_col_width(self):
        f = '[MClient] settings.controller.Save.save_term_col_width'
        width = SETTINGS.gui.ent_trm.get()
        width = Input(f, width).get_integer()
        if not 50 <= width <= 512:
            self._report_wrong_range(f, 50, 512)
            width = 157
            SETTINGS.gui.ent_trm.reset()
            SETTINGS.gui.ent_trm.insert(width)
        CONFIG.new['columns']['terms']['width'] = width
    
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


SETTINGS = Settings()
SAVE_SETTINGS = Save()
