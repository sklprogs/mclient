#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.shared as sh

PRODUCT = 'MClient'
ICON = sh.objs.get_pdir().add('..','resources','icon_64x64_mclient.gif')


class Settings:

    def __init__(self):
        self.set_values()
        self.set_gui()

    def set_values(self):
        self.items = (_('Subjects')
                     ,_('Word forms')
                     ,_('Transcription')
                     ,_('Parts of speech')
                     ,_('Do not set')
                     )
        self.scitems = (PRODUCT
                       ,_('Multitran')
                       ,_('Cut to the chase')
                       ,_('Clearness')
                       ,_('Custom')
                       )
        self.spitems = (_('Noun'),_('Verb'),_('Adjective')
                       ,_('Abbreviation'),_('Adverb'),_('Preposition')
                       ,_('Pronoun')
                       )
        self.allowed = []
        self.spallow = []

    def update_col1(self):
        f = '[MClient] settings.gui.Settings.update_col1'
        if self.opt_cl1.choice != _('Do not set'):
            if self.opt_cl1.choice in self.allowed:
                self.allowed.remove(self.opt_cl1.choice)
            elif _('Subjects') in self.allowed:
                self.opt_cl1.set(_('Subjects'))
                self.allowed.remove(_('Subjects'))
            elif self.allowed:
                self.opt_cl1.set(self.allowed[0])
                self.allowed.remove(self.allowed[0])
            else:
                mes = _('Empty input is not allowed!')
                sh.objs.get_mes(f,mes).show_error()

    def update_col2(self):
        f = '[MClient] settings.gui.Settings.update_col2'
        if self.opt_cl2.choice != _('Do not set'):
            if self.opt_cl2.choice in self.allowed:
                self.allowed.remove(self.opt_cl2.choice)
            elif _('Word forms') in self.allowed:
                self.opt_cl2.set(_('Word forms'))
                self.allowed.remove(_('Word forms'))
            elif self.allowed:
                self.opt_cl2.set(self.allowed[0])
                self.allowed.remove(self.allowed[0])
            else:
                mes = _('Empty input is not allowed!')
                sh.objs.get_mes(f,mes).show_error()

    def update_col3(self):
        f = '[MClient] settings.gui.Settings.update_col3'
        if self.opt_cl3.choice != _('Do not set'):
            if self.opt_cl3.choice in self.allowed:
                self.allowed.remove(self.opt_cl3.choice)
            elif _('Parts of speech') in self.allowed:
                self.opt_cl3.set(_('Parts of speech'))
                self.allowed.remove(_('Parts of speech'))
            elif self.allowed:
                self.opt_cl3.set(self.allowed[0])
                self.allowed.remove(self.allowed[0])
            else:
                mes = _('Empty input is not allowed!')
                sh.objs.get_mes(f,mes).show_error()

    def update_col4(self):
        f = '[MClient] settings.gui.Settings.update_col4'
        if self.opt_cl4.choice != _('Do not set'):
            if self.opt_cl4.choice in self.allowed:
                self.allowed.remove(self.opt_cl4.choice)
            elif _('Transcription') in self.allowed:
                self.opt_cl4.set(_('Transcription'))
                self.allowed.remove(_('Transcription'))
            elif self.allowed:
                self.opt_cl4.set(self.allowed[0])
                self.allowed.remove(self.allowed[0])
            else:
                mes = _('Empty input is not allowed!')
                sh.objs.get_mes(f,mes).show_error()

    def update_sc(self,event=None):
        cond11 = self.opt_cl1.choice == _('Subjects')
        cond12 = self.opt_cl1.choice == _('Word forms')
        cond13 = self.opt_cl1.choice == _('Parts of speech')
        cond21 = self.opt_cl2.choice == _('Word forms')
        cond22 = self.opt_cl2.choice == _('Transcription')
        cond31 = self.opt_cl3.choice == _('Transcription')
        cond32 = self.opt_cl3.choice == _('Parts of speech')
        cond33 = self.opt_cl3.choice == _('Do not set')
        cond41 = self.opt_cl4.choice == _('Parts of speech')
        cond42 = self.opt_cl4.choice == _('Subjects')
        cond43 = self.opt_cl4.choice == _('Do not set')

        if cond11 and cond21 and cond31 and cond41:
            self.opt_scm.set(PRODUCT)
        elif cond12 and cond22 and cond32 and cond42:
            self.opt_scm.set(_('Multitran'))
        elif cond13 and cond21 and cond31 and cond42:
            self.opt_scm.set(_('Cut to the chase'))
        elif cond13 and cond21 and cond33 and cond43:
            self.opt_scm.set(_('Clearness'))
        else:
            self.opt_scm.set(_('Custom'))

    def update_by_sc(self,event=None):
        f = '[MClient] settings.gui.Settings.update_by_sc'
        if self.opt_scm.choice == PRODUCT:
            self.opt_cl1.set(_('Subjects'))
            self.opt_cl2.set(_('Word forms'))
            self.opt_cl3.set(_('Transcription'))
            self.opt_cl4.set(_('Parts of speech'))
        elif self.opt_scm.choice == _('Multitran'):
            self.opt_cl1.set(_('Word forms'))
            self.opt_cl2.set(_('Transcription'))
            self.opt_cl3.set(_('Parts of speech'))
            self.opt_cl4.set(_('Subjects'))
        elif self.opt_scm.choice == _('Cut to the chase'):
            self.opt_cl1.set(_('Parts of speech'))
            self.opt_cl2.set(_('Word forms'))
            self.opt_cl3.set(_('Transcription'))
            self.opt_cl4.set(_('Subjects'))
        elif self.opt_scm.choice == _('Clearness'):
            self.opt_cl1.set(_('Parts of speech'))
            self.opt_cl2.set(_('Word forms'))
            self.opt_cl3.set(_('Do not set'))
            self.opt_cl4.set(_('Do not set'))
        elif self.opt_scm.choice == _('Custom'):
            pass
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(self.opt_scm.choice,self.scitems)
            sh.objs.get_mes(f,mes).show_error()

    def update_by_col1(self,event=None):
        self.allowed = list(self.items)
        self.update_col1()
        self.update_col2()
        self.update_col3()
        self.update_col4()
        self.update_sc()

    def update_by_col2(self,event=None):
        self.allowed = list(self.items)
        self.update_col2()
        self.update_col1()
        self.update_col3()
        self.update_col4()
        self.update_sc()

    def update_by_col3(self,event=None):
        self.allowed = list(self.items)
        self.update_col3()
        self.update_col1()
        self.update_col2()
        self.update_col4()
        self.update_sc()

    def update_by_col4(self,event=None):
        self.allowed = list(self.items)
        self.update_col4()
        self.update_col1()
        self.update_col2()
        self.update_col3()
        self.update_sc()
        
    def update_by_sp1(self,event=None):
        self.spallow = list(self.spitems)
        self.update_sp1()
        self.update_sp2()
        self.update_sp3()
        self.update_sp4()
        self.update_sp5()
        self.update_sp6()
        self.update_sp7()
        
    def update_by_sp2(self,event=None):
        self.spallow = list(self.spitems)
        self.update_sp2()
        self.update_sp1()
        self.update_sp3()
        self.update_sp4()
        self.update_sp5()
        self.update_sp6()
        self.update_sp7()
        
    def update_by_sp3(self,event=None):
        self.spallow = list(self.spitems)
        self.update_sp3()
        self.update_sp1()
        self.update_sp2()
        self.update_sp4()
        self.update_sp5()
        self.update_sp6()
        self.update_sp7()
        
    def update_by_sp4(self,event=None):
        self.spallow = list(self.spitems)
        self.update_sp4()
        self.update_sp1()
        self.update_sp2()
        self.update_sp3()
        self.update_sp5()
        self.update_sp6()
        self.update_sp7()
        
    def update_by_sp5(self,event=None):
        self.spallow = list(self.spitems)
        self.update_sp5()
        self.update_sp1()
        self.update_sp2()
        self.update_sp3()
        self.update_sp4()
        self.update_sp6()
        self.update_sp7()
        
    def update_by_sp6(self,event=None):
        self.spallow = list(self.spitems)
        self.update_sp6()
        self.update_sp1()
        self.update_sp2()
        self.update_sp3()
        self.update_sp4()
        self.update_sp5()
        self.update_sp7()
        
    def update_by_sp7(self,event=None):
        self.spallow = list(self.spitems)
        self.update_sp7()
        self.update_sp1()
        self.update_sp2()
        self.update_sp3()
        self.update_sp4()
        self.update_sp5()
        self.update_sp6()

    def set_gui(self):
        self.parent = sh.Top (AutoCr = True
                             ,title = _('View Settings')
                             ,icon = ICON
                             )
        self.widget = self.parent.widget
        self.set_frames()
        self.set_cboxes()
        self.set_labels()
        self.set_columns()
        self.set_buttons()
        self.set_bindings()

    def block_settings(self,event=None):
        f = '[MClient] settings.gui.Settings.block_settings'
        mes = _('Not implemented yet!')
        sh.objs.get_mes(f,mes).show_info()

    def get_priority_settings(self,event=None):
        f = '[MClient] settings.gui.Settings.get_priority_settings'
        mes = _('Not implemented yet!')
        sh.objs.get_mes(f,mes).show_info()

    def set_dep(self,event=None):
        if self.cbx_no14.get():
            self.cbx_no15.set_state(True)
        else:
            self.cbx_no15.set_state(False)
    
    def set_cboxes(self):
        self.cbx_no1 = sh.CheckBox (parent = self.frm_cb1
                                   ,side = 'left'
                                   )
        self.cbx_no2 = sh.CheckBox (parent = self.frm_cb2
                                   ,side = 'left'
                                   )
        self.cbx_no3 = sh.CheckBox (parent = self.frm_cb3
                                   ,side = 'left'
                                   )
        self.cbx_no4 = sh.CheckBox (parent = self.frm_cb4
                                   ,side = 'left'
                                   )
        self.cbx_no5 = sh.CheckBox (parent = self.frm_cb5
                                   ,side = 'left'
                                   )
        self.cbx_no6 = sh.CheckBox (parent = self.frm_cb6
                                   ,side = 'left'
                                   )
        self.cbx_no7 = sh.CheckBox (parent = self.frm_cb7
                                   ,side = 'left'
                                   )
        self.cbx_no8 = sh.CheckBox (parent = self.frm_cb8
                                   ,side = 'left'
                                   )
        self.cbx_no9 = sh.CheckBox (parent = self.frm_cb9
                                   ,side = 'left'
                                   )
        self.cbx_no10 = sh.CheckBox (parent = self.frm_cb10
                                    ,side = 'left'
                                    )
        self.cbx_no11 = sh.CheckBox (parent = self.frm_cb11
                                    ,side = 'left'
                                    )
        self.cbx_no12 = sh.CheckBox (parent = self.frm_cb12
                                    ,side = 'left'
                                    )
        self.cbx_no13 = sh.CheckBox (parent = self.frm_cb13
                                    ,side = 'left'
                                    )
        self.cbx_no14 = sh.CheckBox (parent = self.frm_cb14
                                    ,side = 'left'
                                    ,action = self.set_dep
                                    )
        self.lbl_spc = sh.Label (parent = self.frm_cb15
                                ,side = 'left'
                                ,text = ''
                                ,width = 2
                                )
        self.cbx_no15 = sh.CheckBox (parent = self.frm_cb15
                                    ,side = 'left'
                                    )

    def reset(self,event=None):
        self.opt_scm.set(PRODUCT)
        self.opt_cl1.set(_('Subjects'))
        self.opt_cl2.set(_('Word forms'))
        self.opt_cl3.set(_('Parts of speech'))
        self.opt_cl4.set(_('Transcription'))
        self.opt_sp1.set(_('Noun'))
        self.opt_sp2.set(_('Verb'))
        self.opt_sp3.set(_('Adjective'))
        self.opt_sp4.set(_('Abbreviation'))
        self.opt_sp5.set(_('Adverb'))
        self.opt_sp6.set(_('Preposition'))
        self.opt_sp7.set(_('Pronoun'))
        self.cbx_no1.enable()
        self.cbx_no2.enable()
        self.cbx_no3.enable()
        self.cbx_no4.enable()
        self.cbx_no5.disable()
        self.cbx_no6.disable()
        self.cbx_no7.disable()
        self.cbx_no8.enable()
        self.cbx_no9.enable()
        self.cbx_no10.enable()
        self.cbx_no11.enable()
        self.cbx_no12.disable()
        self.cbx_no13.enable()
        self.cbx_no14.enable()

    def set_buttons(self):
        sh.Button (parent = self.frm_btn
                  ,action = self.reset
                  ,hint = _('Reset settings')
                  ,text = _('Reset')
                  ,side = 'left'
                  )

        self.btn_apl = sh.Button (parent = self.frm_btn
                                 ,hint = _('Apply settings')
                                 ,text = _('Apply')
                                 ,side = 'right'
                                 )

    def set_frames(self):
        self.frm_col = sh.Frame (parent = self.parent
                                ,expand = True
                                ,fill = 'both'
                                )
        self.frm_spc = sh.Frame (parent = self.parent
                                ,expand = True
                                ,fill = 'both'
                                )
        self.frm_scm = sh.Frame (parent = self.frm_col
                                ,side = 'left'
                                ,expand = False
                                ,fill = 'both'
                                )
        self.frm_cl1 = sh.Frame (parent = self.frm_col
                                ,side = 'left'
                                ,expand = False
                                ,fill = 'both'
                                )
        self.frm_cl2 = sh.Frame (parent = self.frm_col
                                ,side = 'left'
                                ,expand = False
                                ,fill = 'both'
                                )
        self.frm_cl3 = sh.Frame (parent = self.frm_col
                                ,expand = False
                                ,side = 'left'
                                ,fill = 'both'
                                )
        self.frm_cl4 = sh.Frame (parent = self.frm_col
                                ,side = 'left'
                                ,expand = False
                                ,fill = 'both'
                                )
        self.frm_sp1 = sh.Frame (parent = self.frm_spc
                                ,side = 'left'
                                ,expand = False
                                ,fill = 'both'
                                )
        self.frm_sp2 = sh.Frame (parent = self.frm_spc
                                ,side = 'left'
                                ,expand = False
                                ,fill = 'both'
                                )
        self.frm_sp3 = sh.Frame (parent = self.frm_spc
                                ,side = 'left'
                                ,expand = False
                                ,fill = 'both'
                                )
        self.frm_sp4 = sh.Frame (parent = self.frm_spc
                                ,side = 'left'
                                ,expand = False
                                ,fill = 'both'
                                )
        self.frm_sp5 = sh.Frame (parent = self.frm_spc
                                ,side = 'left'
                                ,expand = False
                                ,fill = 'both'
                                )
        self.frm_sp6 = sh.Frame (parent = self.frm_spc
                                ,side = 'left'
                                ,expand = False
                                ,fill = 'both'
                                )
        self.frm_sp7 = sh.Frame (parent = self.frm_spc
                                ,side = 'left'
                                ,expand = False
                                ,fill = 'both'
                                )
        self.frm_cb1 = sh.Frame (parent = self.parent
                                ,expand = False
                                ,fill = 'x'
                                )
        self.frm_cb2 = sh.Frame (parent = self.parent
                                ,expand = False
                                ,fill = 'x'
                                )
        self.frm_cb3 = sh.Frame (parent = self.parent
                                ,expand = False
                                ,fill = 'x'
                                )
        self.frm_cb4 = sh.Frame (parent = self.parent
                                ,expand = False
                                ,fill = 'x'
                                )
        self.frm_cb5 = sh.Frame (parent = self.parent
                                ,expand = False
                                ,fill = 'x'
                                )
        self.frm_cb6 = sh.Frame (parent = self.parent
                                ,expand = False
                                ,fill = 'x'
                                )
        self.frm_cb7 = sh.Frame (parent = self.parent
                                ,expand = False
                                ,fill = 'x'
                                )
        self.frm_cb8 = sh.Frame (parent = self.parent
                                ,expand = False
                                ,fill = 'x'
                                )
        self.frm_cb9 = sh.Frame (parent = self.parent
                                ,expand = False
                                ,fill = 'x'
                                )
        self.frm_cb10 = sh.Frame (parent = self.parent
                                 ,expand = False
                                 ,fill = 'x'
                                 )
        self.frm_cb11 = sh.Frame (parent = self.parent
                                 ,expand = False
                                 ,fill = 'x'
                                 )
        self.frm_cb12 = sh.Frame (parent = self.parent
                                 ,expand = False
                                 ,fill = 'x'
                                 )
        self.frm_cb13 = sh.Frame (parent = self.parent
                                 ,expand = False
                                 ,fill = 'x'
                                 )
        self.frm_cb14 = sh.Frame (parent = self.parent
                                 ,expand = False
                                 ,fill = 'x'
                                 )
        self.frm_cb15 = sh.Frame (parent = self.parent
                                 ,expand = False
                                 ,fill = 'x'
                                 )
        self.frm_btn = sh.Frame (parent = self.parent
                                ,expand = False
                                ,fill = 'x'
                                ,side = 'bottom'
                                )

    def set_labels(self):
        ''' Other possible color schemes:
            font = 'Sans 9 italic', fg = 'khaki4'
        '''
        sh.Label (parent = self.frm_scm
                 ,text = _('Style:')
                 ,font = 'Sans 9'
                 ,side = 'top'
                 ,fill = 'both'
                 ,expand = True
                 ,fg = 'PaleTurquoise1'
                 ,bg = 'RoyalBlue3'
                 )
        sh.Label (parent = self.frm_cl1
                 ,text = _('Column') + ' 1:'
                 ,font = 'Sans 9'
                 ,side = 'top'
                 ,fill = 'both'
                 ,expand = True
                 ,fg = 'PaleTurquoise1'
                 ,bg = 'RoyalBlue3'
                 )
        sh.Label (parent = self.frm_cl2
                 ,text = _('Column') + ' 2:'
                 ,font = 'Sans 9'
                 ,side = 'top'
                 ,fill = 'both'
                 ,expand = True
                 ,fg = 'PaleTurquoise1'
                 ,bg = 'RoyalBlue3'
                 )
        sh.Label (parent = self.frm_cl3
                 ,text = _('Column') + ' 3:'
                 ,font = 'Sans 9'
                 ,side = 'top'
                 ,fill = 'both'
                 ,expand = True
                 ,fg = 'PaleTurquoise1'
                 ,bg = 'RoyalBlue3'
                 )
        sh.Label (parent = self.frm_cl4
                 ,text = _('Column') + ' 4:'
                 ,font = 'Sans 9'
                 ,side = 'top'
                 ,fill = 'both'
                 ,expand = True
                 ,fg = 'PaleTurquoise1'
                 ,bg = 'RoyalBlue3'
                 )
        self.lbl_no1 = sh.Label (parent = self.frm_cb1
                                ,text = _('Sort by each column (if it is set, except for transcription) and order parts of speech')
                                ,side = 'left'
                                )
        self.lbl_no2 = sh.Label (parent = self.frm_cb2
                                ,text = _('Alphabetize terms')
                                ,side = 'left'
                                )
        self.lbl_no3 = sh.Label (parent = self.frm_cb3
                                ,text = _('Block subjects from blacklist')
                                ,side = 'left'
                                )
        self.lbl_no4 = sh.Label (parent = self.frm_cb4
                                ,text = _('Prioritize subjects')
                                ,side = 'left'
                                )
        self.lbl_no5 = sh.Label (parent = self.frm_cb5
                                ,text = _('Vertical view')
                                ,side = 'left'
                                )
        self.lbl_no6 = sh.Label (parent = self.frm_cb6
                                ,text = _('Shorten subject titles')
                                ,side = 'left'
                                )
        self.lbl_no7 = sh.Label (parent = self.frm_cb7
                                ,text = _('Shorten parts of speech')
                                ,side = 'left'
                                )
        self.lbl_no8 = sh.Label (parent = self.frm_cb8
                                ,text = _('Show user names')
                                ,side = 'left'
                                )
        self.lbl_no9 = sh.Label (parent = self.frm_cb9
                                ,text = _('Select terms only')
                                ,side = 'left'
                                )
        self.lbl_no10 = sh.Label (parent = self.frm_cb10
                                 ,text = _('Iconify the program window after copying')
                                 ,side = 'left'
                                 )
        self.lbl_no11 = sh.Label (parent = self.frm_cb11
                                 ,text = _('Show suggestions on input')
                                 ,side = 'left'
                                 )
        self.lbl_no12 = sh.Label (parent = self.frm_cb12
                                 ,text = _('Autoswap Russian and the other language if appropriate')
                                 ,side = 'left'
                                 )
        self.lbl_no13 = sh.Label (parent = self.frm_cb13
                                 ,text = _('Show a phrase count')
                                 ,side = 'left'
                                 )
        self.lbl_no14 = sh.Label (parent = self.frm_cb14
                                 ,text = _('Adjust columns by width')
                                 ,side = 'left'
                                 )
        self.lbl_no15 = sh.Label (parent = self.frm_cb15
                                 ,text = _('Use a custom table width:')
                                 ,side = 'left'
                                 )
        self.ent_tab = sh.Entry (parent = self.frm_cb15
                                ,side = 'left'
                                ,width = 3
                                )
        self.lbl_prc = sh.Label (parent = self.frm_cb15
                                 ,text = '%'
                                 ,side = 'left'
                                 )
        sh.Label (parent = self.frm_sp1
                 ,text = _('Part of speech') + ' 1:'
                 ,font = 'Sans 8'
                 ,side = 'top'
                 ,fill = 'both'
                 ,expand = True
                 ,fg = 'PaleTurquoise1'
                 ,bg = 'RoyalBlue3'
                 )
        sh.Label (parent = self.frm_sp2
                 ,text = _('Part of speech') + ' 2:'
                 ,font = 'Sans 8'
                 ,side = 'top'
                 ,fill = 'both'
                 ,expand = True
                 ,fg = 'PaleTurquoise1'
                 ,bg = 'RoyalBlue3'
                 )
        sh.Label (parent = self.frm_sp3
                 ,text = _('Part of speech') + ' 3:'
                 ,font = 'Sans 8'
                 ,side = 'top'
                 ,fill = 'both'
                 ,expand = True
                 ,fg = 'PaleTurquoise1'
                 ,bg = 'RoyalBlue3'
                 )
        sh.Label (parent = self.frm_sp4
                 ,text = _('Part of speech') + ' 4:'
                 ,font = 'Sans 8'
                 ,side = 'top'
                 ,fill = 'both'
                 ,expand = True
                 ,fg = 'PaleTurquoise1'
                 ,bg = 'RoyalBlue3'
                 )
        sh.Label (parent = self.frm_sp5
                 ,text = _('Part of speech') + ' 5:'
                 ,font = 'Sans 8'
                 ,side = 'top'
                 ,fill = 'both'
                 ,expand = True
                 ,fg = 'PaleTurquoise1'
                 ,bg = 'RoyalBlue3'
                 )
        sh.Label (parent = self.frm_sp6
                 ,text = _('Part of speech') + ' 6:'
                 ,font = 'Sans 8'
                 ,side = 'top'
                 ,fill = 'both'
                 ,expand = True
                 ,fg = 'PaleTurquoise1'
                 ,bg = 'RoyalBlue3'
                 )
        sh.Label (parent = self.frm_sp7
                 ,text = _('Part of speech') + ' 7:'
                 ,font = 'Sans 8'
                 ,side = 'top'
                 ,fill = 'both'
                 ,expand = True
                 ,fg = 'PaleTurquoise1'
                 ,bg = 'RoyalBlue3'
                 )
                 
    def set_columns(self):
        self.opt_scm = sh.OptionMenu (parent = self.frm_scm
                                     ,items = self.scitems
                                     ,side = 'bottom'
                                     ,action = self.update_by_sc
                                     ,default = PRODUCT
                                     )
        self.opt_cl1 = sh.OptionMenu (parent = self.frm_cl1
                                     ,items = self.items
                                     ,side = 'bottom'
                                     ,action = self.update_by_col1
                                     ,default = _('Subjects')
                                     )
        self.opt_cl2 = sh.OptionMenu (parent = self.frm_cl2
                                     ,items = self.items
                                     ,side = 'bottom'
                                     ,action = self.update_by_col2
                                     ,default = _('Word forms')
                                     )
        self.opt_cl3 = sh.OptionMenu (parent = self.frm_cl3
                                     ,items = self.items
                                     ,side = 'bottom'
                                     ,action = self.update_by_col3
                                     ,default = _('Transcription')
                                     )
        self.opt_cl4 = sh.OptionMenu (parent = self.frm_cl4
                                     ,items = self.items
                                     ,side = 'bottom'
                                     ,action = self.update_by_col4
                                     ,default = _('Parts of speech')
                                     )
        self.opt_sp1 = sh.OptionMenu (parent = self.frm_sp1
                                     ,items = self.spitems
                                     ,side = 'bottom'
                                     ,action = self.update_by_sp1
                                     ,default = self.spitems[0]
                                     )
        self.opt_sp2 = sh.OptionMenu (parent = self.frm_sp2
                                     ,items = self.spitems
                                     ,side = 'bottom'
                                     ,action = self.update_by_sp2
                                     ,default = self.spitems[1]
                                     )
        self.opt_sp3 = sh.OptionMenu (parent = self.frm_sp3
                                     ,items = self.spitems
                                     ,side = 'bottom'
                                     ,action = self.update_by_sp3
                                     ,default = self.spitems[2]
                                     )
        self.opt_sp4 = sh.OptionMenu (parent = self.frm_sp4
                                     ,items = self.spitems
                                     ,side = 'bottom'
                                     ,action = self.update_by_sp4
                                     ,default = self.spitems[3]
                                     )
        self.opt_sp5 = sh.OptionMenu (parent = self.frm_sp5
                                     ,items = self.spitems
                                     ,side = 'bottom'
                                     ,action = self.update_by_sp5
                                     ,default = self.spitems[4]
                                     )
        self.opt_sp6 = sh.OptionMenu (parent = self.frm_sp6
                                     ,items = self.spitems
                                     ,side = 'bottom'
                                     ,action = self.update_by_sp6
                                     ,default = self.spitems[5]
                                     )
        self.opt_sp7 = sh.OptionMenu (parent = self.frm_sp7
                                     ,items = self.spitems
                                     ,side = 'bottom'
                                     ,action = self.update_by_sp7
                                     ,default = self.spitems[6]
                                     )

    def set_bindings(self):
        sh.com.bind (obj = self.lbl_no1
                    ,bindings = '<Button-1>'
                    ,action = self.cbx_no1.toggle
                    )
        sh.com.bind (obj = self.lbl_no2
                    ,bindings = '<Button-1>'
                    ,action = self.cbx_no2.toggle
                    )
        sh.com.bind (obj = self.lbl_no3
                    ,bindings = '<Button-1>'
                    ,action = self.cbx_no3.toggle
                    )
        sh.com.bind (obj = self.lbl_no4
                    ,bindings = '<Button-1>'
                    ,action = self.cbx_no4.toggle
                    )
        sh.com.bind (obj = self.lbl_no5
                    ,bindings = '<Button-1>'
                    ,action = self.cbx_no5.toggle
                    )
        sh.com.bind (obj = self.lbl_no6
                    ,bindings = '<Button-1>'
                    ,action = self.cbx_no6.toggle
                    )
        sh.com.bind (obj = self.lbl_no7
                    ,bindings = '<Button-1>'
                    ,action = self.cbx_no7.toggle
                    )
        sh.com.bind (obj = self.lbl_no8
                    ,bindings = '<Button-1>'
                    ,action = self.cbx_no8.toggle
                    )
        sh.com.bind (obj = self.lbl_no9
                    ,bindings = '<Button-1>'
                    ,action = self.cbx_no9.toggle
                    )
        sh.com.bind (obj = self.lbl_no10
                    ,bindings = '<Button-1>'
                    ,action = self.cbx_no10.toggle
                    )
        sh.com.bind (obj = self.lbl_no11
                    ,bindings = '<Button-1>'
                    ,action = self.cbx_no11.toggle
                    )
        sh.com.bind (obj = self.lbl_no12
                    ,bindings = '<Button-1>'
                    ,action = self.cbx_no12.toggle
                    )
        sh.com.bind (obj = self.lbl_no13
                    ,bindings = '<Button-1>'
                    ,action = self.cbx_no13.toggle
                    )
        sh.com.bind (obj = self.lbl_no14
                    ,bindings = '<Button-1>'
                    ,action = self.click_label14
                    )
        sh.com.bind (obj = self.lbl_spc
                    ,bindings = '<Button-1>'
                    ,action = self.cbx_no15.toggle
                    )
        sh.com.bind (obj = self.lbl_no15
                    ,bindings = '<Button-1>'
                    ,action = self.cbx_no15.toggle
                    )
        sh.com.bind (obj = self.lbl_prc
                    ,bindings = '<Button-1>'
                    ,action = self.cbx_no15.toggle
                    )

    def click_label14(self,event=None):
        self.cbx_no14.toggle()
        self.set_dep()
    
    def show(self,event=None):
        self.parent.show()

    def close(self,event=None):
        self.parent.close()

    def update_sp1(self):
        f = '[MClient] settings.gui.Settings.update_sp1'
        if self.opt_sp1.choice in self.spallow:
            self.spallow.remove(self.opt_sp1.choice)
        elif _('Noun') in self.spallow:
            self.opt_sp1.set(_('Noun'))
            self.spallow.remove(_('Noun'))
        elif self.spallow:
            self.opt_sp1.set(self.spallow[0])
            self.spallow.remove(self.spallow[0])
        else:
            mes = _('Empty input is not allowed!')
            sh.objs.get_mes(f,mes).show_error()
    
    def update_sp2(self):
        f = '[MClient] settings.gui.Settings.update_sp2'
        if self.opt_sp2.choice in self.spallow:
            self.spallow.remove(self.opt_sp2.choice)
        elif _('Verb') in self.spallow:
            self.opt_sp2.set(_('Verb'))
            self.spallow.remove(_('Verb'))
        elif self.spallow:
            self.opt_sp2.set(self.spallow[0])
            self.spallow.remove(self.spallow[0])
        else:
            mes = _('Empty input is not allowed!')
            sh.objs.get_mes(f,mes).show_error()
                       
    def update_sp3(self):
        f = '[MClient] settings.gui.Settings.update_sp3'
        if self.opt_sp3.choice in self.spallow:
            self.spallow.remove(self.opt_sp3.choice)
        elif _('Adjective') in self.spallow:
            self.opt_sp3.set(_('Adjective'))
            self.spallow.remove(_('Adjective'))
        elif self.spallow:
            self.opt_sp3.set(self.spallow[0])
            self.spallow.remove(self.spallow[0])
        else:
            mes = _('Empty input is not allowed!')
            sh.objs.get_mes(f,mes).show_error()
                       
    def update_sp4(self):
        f = '[MClient] settings.gui.Settings.update_sp4'
        if self.opt_sp4.choice in self.spallow:
            self.spallow.remove(self.opt_sp4.choice)
        elif _('Abbreviation') in self.spallow:
            self.opt_sp4.set(_('Abbreviation'))
            self.spallow.remove(_('Abbreviation'))
        elif self.spallow:
            self.opt_sp4.set(self.spallow[0])
            self.spallow.remove(self.spallow[0])
        else:
            mes = _('Empty input is not allowed!')
            sh.objs.get_mes(f,mes).show_error()
                       
    def update_sp5(self):
        f = '[MClient] settings.gui.Settings.update_sp5'
        if self.opt_sp5.choice in self.spallow:
            self.spallow.remove(self.opt_sp5.choice)
        elif _('Adverb') in self.spallow:
            self.opt_sp5.set(_('Adverb'))
            self.spallow.remove(_('Adverb'))
        elif self.spallow:
            self.opt_sp5.set(self.spallow[0])
            self.spallow.remove(self.spallow[0])
        else:
            mes = _('Empty input is not allowed!')
            sh.objs.get_mes(f,mes).show_error()
                       
    def update_sp6(self):
        f = '[MClient] settings.gui.Settings.update_sp6'
        if self.opt_sp6.choice in self.spallow:
            self.spallow.remove(self.opt_sp6.choice)
        elif _('Preposition') in self.spallow:
            self.opt_sp6.set(_('Preposition'))
            self.spallow.remove(_('Preposition'))
        elif self.spallow:
            self.opt_sp6.set(self.spallow[0])
            self.spallow.remove(self.spallow[0])
        else:
            mes = _('Empty input is not allowed!')
            sh.objs.get_mes(f,mes).show_error()
                       
    def update_sp7(self):
        f = '[MClient] settings.gui.Settings.update_sp7'
        if self.opt_sp7.choice in self.spallow:
            self.spallow.remove(self.opt_sp7.choice)
        elif _('Pronoun') in self.spallow:
            self.opt_sp7.set(_('Pronoun'))
            self.spallow.remove(_('Pronoun'))
        elif self.spallow:
            self.opt_sp7.set(self.spallow[0])
            self.spallow.remove(self.spallow[0])
        else:
            mes = _('Empty input is not allowed!')
            sh.objs.get_mes(f,mes).show_error()


if __name__ == '__main__':
    Settings().show()