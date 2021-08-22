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
    
    def update_table_width(self):
        self.gui.ent_tab.reset()
        self.gui.ent_tab.insert(sh.lg.globs['int']['table_width'])
        if sh.lg.globs['int']['table_width'] == 100:
            self.gui.cbx_no15.disable()
        else:
            self.gui.cbx_no15.enable()
    
    def run(self):
        self.update_style_area()
        self.update_speech_area()
        self.update_checkboxes()
        self.update_table_width()



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
    
    def export_table_width(self):
        f = '[MClient] settings.controller.ExportSettingsUI.export_table_width'
        if objs.settings_ui.cbx_no15.get():
            width = objs.settings_ui.ent_tab.get()
            width = sh.Input(f,width).get_integer()
            if not 60 <= width <= 100:
                mes = _('Wrong input data: "{}"!').format(width)
                sh.objs.get_mes(f,mes,True).show_warning()
                width = 100
            sh.lg.globs['int']['table_width'] = width
    
    def run(self):
        f = '[MClient] settings.controller.ExportSettingsUI.run'
        # 'objs.get_settings_ui' may not be used as often
        if objs.settings is None or objs.settings.gui is None:
            sh.com.rep_lazy(f)
        else:
            self.export_style_area()
            self.export_speech_area()
            self.export_checkboxes()
            self.export_table_width()



class Settings:

    def __init__(self):
        self.gui = None
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
    
    def set_bindings(self):
        self.get_gui().btn_apl.action = self.apply
        sh.com.bind (obj = self.gui
                    ,bindings = [sh.lg.globs['str']['bind_settings']
                                ,sh.lg.globs['str']['bind_settings_alt']
                                ]
                    ,action = self.toggle
                    )
        sh.com.bind (obj = self.gui.ent_tab
                    ,bindings = ('<Return>','<KP_Enter>')
                    ,action = self.apply
                    )

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