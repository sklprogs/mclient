#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.shared as sh
from . import gui as gi


class UpdateSettingsUI:
    
    def __init__(self):
        self.gui = objs.get_settings_ui()
    
    def update_style_area(self):
        self.gui.opt_scm.set(sh.lg.globs['str']['style'])
        self.gui.opt_cl1.set(sh.lg.globs['str']['col1_type'])
        self.gui.opt_cl2.set(sh.lg.globs['str']['col2_type'])
        self.gui.opt_cl3.set(sh.lg.globs['str']['col3_type'])
        self.gui.opt_cl4.set(sh.lg.globs['str']['col4_type'])
    
    def update_speech_area(self):
        self.gui.opt_sp1.set(sh.lg.globs['str']['speech1'])
        self.gui.opt_sp2.set(sh.lg.globs['str']['speech2'])
        self.gui.opt_sp3.set(sh.lg.globs['str']['speech3'])
        self.gui.opt_sp4.set(sh.lg.globs['str']['speech4'])
        self.gui.opt_sp5.set(sh.lg.globs['str']['speech5'])
        self.gui.opt_sp6.set(sh.lg.globs['str']['speech6'])
        self.gui.opt_sp7.set(sh.lg.globs['str']['speech7'])
    
    def update_checkboxes(self):
        self.gui.cbx_no1.set(sh.lg.globs['bool']['SortByColumns'])
        self.gui.cbx_no2.set(sh.lg.globs['bool']['AlphabetizeTerms'])
        self.gui.cbx_no3.set(sh.lg.globs['bool']['BlockSubjects'])
        self.gui.cbx_no4.set(sh.lg.globs['bool']['PrioritizeSubjects'])
        self.gui.cbx_no5.set(sh.lg.globs['bool']['VerticalView'])
        self.gui.cbx_no6.set(sh.lg.globs['bool']['ShortSubjects'])
        self.gui.cbx_no7.set(sh.lg.globs['bool']['ShortSpeech'])
        self.gui.cbx_no8.set(sh.lg.globs['bool']['ShowUserNames'])
        self.gui.cbx_no9.set(sh.lg.globs['bool']['SelectTermsOnly'])
        self.gui.cbx_no10.set(sh.lg.globs['bool']['Iconify'])
        self.gui.cbx_no11.set(sh.lg.globs['bool']['Autocompletion'])
        self.gui.cbx_no12.set(sh.lg.globs['bool']['Autoswap'])
        self.gui.cbx_no13.set(sh.lg.globs['bool']['PhraseCount'])
        self.gui.cbx_no14.set(sh.lg.globs['bool']['AdjustByWidth'])
    
    def update_col_widths(self):
        self.gui.ent_fcw.reset()
        self.gui.ent_fcw.insert(sh.lg.globs['int']['fixed_col_width'])
        self.gui.ent_tcw.reset()
        self.gui.ent_tcw.insert(sh.lg.globs['int']['term_col_width'])
    
    def run(self):
        self.update_style_area()
        self.update_speech_area()
        self.update_checkboxes()
        self.update_col_widths()



class ExportSettingsUI:
    
    def export_speech_area(self):
        sh.lg.globs['str']['speech1'] = objs.get_settings_ui().opt_sp1.choice
        sh.lg.globs['str']['speech2'] = objs.settings_ui.opt_sp2.choice
        sh.lg.globs['str']['speech3'] = objs.settings_ui.opt_sp3.choice
        sh.lg.globs['str']['speech4'] = objs.settings_ui.opt_sp4.choice
        sh.lg.globs['str']['speech5'] = objs.settings_ui.opt_sp5.choice
        sh.lg.globs['str']['speech6'] = objs.settings_ui.opt_sp6.choice
        sh.lg.globs['str']['speech7'] = objs.settings_ui.opt_sp7.choice
    
    def export_style_area(self):
        sh.lg.globs['str']['style'] = objs.get_settings_ui().opt_scm.choice
        sh.lg.globs['str']['col1_type'] = objs.settings_ui.opt_cl1.choice
        sh.lg.globs['str']['col2_type'] = objs.settings_ui.opt_cl2.choice
        sh.lg.globs['str']['col3_type'] = objs.settings_ui.opt_cl3.choice
        sh.lg.globs['str']['col4_type'] = objs.settings_ui.opt_cl4.choice
    
    def export_checkboxes(self):
        sh.lg.globs['bool']['SortByColumns'] = objs.get_settings_ui().cbx_no1.get()
        sh.lg.globs['bool']['AlphabetizeTerms'] = objs.settings_ui.cbx_no2.get()
        sh.lg.globs['bool']['BlockSubjects'] = objs.settings_ui.cbx_no3.get()
        sh.lg.globs['bool']['PrioritizeSubjects'] = objs.settings_ui.cbx_no4.get()
        sh.lg.globs['bool']['VerticalView'] = objs.settings_ui.cbx_no5.get()
        sh.lg.globs['bool']['ShortSubjects'] = objs.settings_ui.cbx_no6.get()
        sh.lg.globs['bool']['ShortSpeech'] = objs.settings_ui.cbx_no7.get()
        sh.lg.globs['bool']['ShowUserNames'] = objs.settings_ui.cbx_no8.get()
        sh.lg.globs['bool']['SelectTermsOnly'] = objs.settings_ui.cbx_no9.get()
        sh.lg.globs['bool']['Iconify'] = objs.settings_ui.cbx_no10.get()
        sh.lg.globs['bool']['Autocompletion'] = objs.settings_ui.cbx_no11.get()
        sh.lg.globs['bool']['Autoswap'] = objs.settings_ui.cbx_no12.get()
        sh.lg.globs['bool']['PhraseCount'] = objs.settings_ui.cbx_no13.get()
        sh.lg.globs['bool']['AdjustByWidth'] = objs.settings_ui.cbx_no14.get()
    
    def _report_wrong_range(self,f):
        mes = _('A value of this field should be within the range of {}-{}!')
        mes = mes.format(50,512)
        sh.objs.get_mes(f,mes).show_warning()
    
    def export_fixed_col_width(self):
        f = '[MClient] settings.controller.ExportSettingsUI.export_fixed_col_width'
        width = objs.get_settings_ui().ent_fcw.get()
        width = sh.Input(f,width).get_integer()
        if not 50 <= width <= 512:
            self._report_wrong_range(f)
            width = 63
            objs.settings_ui.ent_fcw.reset()
            objs.settings_ui.ent_fcw.insert(width)
        sh.lg.globs['int']['fixed_col_width'] = width
    
    def export_term_col_width(self):
        f = '[MClient] settings.controller.ExportSettingsUI.export_term_col_width'
        width = objs.get_settings_ui().ent_tcw.get()
        width = sh.Input(f,width).get_integer()
        if not 50 <= width <= 512:
            self._report_wrong_range(f)
            width = 157
            objs.settings_ui.ent_tcw.reset()
            objs.settings_ui.ent_tcw.insert(width)
        sh.lg.globs['int']['term_col_width'] = width
    
    def run(self):
        f = '[MClient] settings.controller.ExportSettingsUI.run'
        # 'objs.get_settings_ui' may not be used so often
        if objs.settings is None or objs.settings.gui is None:
            sh.com.rep_lazy(f)
        else:
            self.export_style_area()
            self.export_speech_area()
            self.export_checkboxes()
            self.export_fixed_col_width()
            self.export_term_col_width()



class Settings:

    def __init__(self):
        self.gui = None
        self.get_win_width = None
        self.Active = False
    
    def toggle(self,event=None):
        if self.Active:
            self.close()
        else:
            self.show()
    
    def get_gui(self):
        if self.gui is None:
            self.set_gui()
        return self.gui
    
    def set_gui(self):
        self.gui = gi.Settings()
        self.set_bindings()

    def show(self,event=None):
        self.Active = True
        self.get_gui()
        UpdateSettingsUI().run()
        self.gui.show()
    
    def close(self,event=None):
        self.Active = False
        self.get_gui().close()

    def apply(self,event=None):
        f = '[MClient] settings.controller.Settings.apply'
        mes = _('This procedure should be overridden')
        sh.objs.get_mes(f,mes,True).show_error()
    
    def _set_col_num(self,window_width):
        if window_width <= 1024:
            return 3
        else:
            return 5
    
    def get_table_width(self):
        f = '[MClient] settings.controller.Settings.get_table_width'
        if self.get_win_width:
            return self.get_win_width()
        else:
            mes = _('An external function is not set!')
            sh.objs.get_mes(f,mes,True).show_error()
            return 1050
    
    def suggest_col_widths(self,event=None):
        f = '[MClient] settings.controller.Settings.suggest_col_widths'
        table_width = self.get_table_width()
        col_num = self.get_gui().ent_num.get()
        if not col_num:
            col_num = self._set_col_num(table_width)
        col_num = sh.Input(f,col_num).get_integer()
        if not 0 < col_num <= 10:
            mes = _('A value of this field should be within the range of {}-{}!')
            mes = mes.format(1,10)
            sh.objs.get_mes(f,mes).show_warning()
            col_num = self._set_col_num(table_width)
        
        ''' How we got this formula. The recommended fixed column width
            is 63 (provided that there are 4 fixed columns). This value
            does not depend on a screen size (but is font-dependent).
            63 * 4 = 252. 79.77% is the recommended value of
            a calculated term column width. We need this to be less than
            100% since a width of columns in HTML cannot be less than
            the text width, and we may have pretty long lines sometimes.
        '''
        term_width = 0.7977 * ((table_width - 252) / col_num)
        # Values in pixels must be integer
        term_width = int(term_width)
        
        mes = _('Table width: {}').format(table_width)
        sh.objs.get_mes(f,mes,True).show_debug()
        mes = _('Term column width: {}').format(term_width)
        sh.objs.get_mes(f,mes,True).show_debug()
        
        self.gui.ent_num.reset()
        self.gui.ent_num.insert(col_num)
        self.gui.ent_fcw.reset()
        self.gui.ent_fcw.insert(63)
        self.gui.ent_tcw.reset()
        self.gui.ent_tcw.insert(term_width)
    
    def set_bindings(self):
        f = '[MClient] settings.controller.Settings.set_bindings'
        if self.gui is None:
            sh.com.rep_empty(f)
            return
        sh.com.bind (obj = self.gui
                    ,bindings = [sh.lg.globs['str']['bind_settings']
                                ,sh.lg.globs['str']['bind_settings_alt']
                                ]
                    ,action = self.toggle
                    )
        sh.com.bind (obj = self.gui.ent_fcw
                    ,bindings = ('<Return>','<KP_Enter>')
                    ,action = self.apply
                    )
        sh.com.bind (obj = self.gui.ent_tcw
                    ,bindings = ('<Return>','<KP_Enter>')
                    ,action = self.apply
                    )
        sh.com.bind (obj = self.gui
                    ,bindings = ('<Escape>','<Control-q>','<Control-w>')
                    ,action = self.close
                    )
        self.gui.btn_apl.action = self.apply
        self.gui.btn_sug.action = self.suggest_col_widths
        self.gui.widget.protocol('WM_DELETE_WINDOW',self.close)

    def get_speech_prior(self):
        return (sh.lg.globs['str']['speech1']
               ,sh.lg.globs['str']['speech2']
               ,sh.lg.globs['str']['speech3']
               ,sh.lg.globs['str']['speech4']
               ,sh.lg.globs['str']['speech5']
               ,sh.lg.globs['str']['speech6']
               ,sh.lg.globs['str']['speech7']
               )



class Objects:
    
    def __init__(self):
        self.settings = self.settings_ui = None
        self.cols = ()
    
    def get_settings(self):
        if self.settings is None:
            self.settings = Settings()
        return self.settings
    
    def get_settings_ui(self):
        if self.settings_ui is None:
            self.settings_ui = self.get_settings().get_gui()
        return self.settings_ui


objs = Objects()
