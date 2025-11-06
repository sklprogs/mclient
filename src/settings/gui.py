#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QGridLayout, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QShortcut, QKeySequence

from skl_shared.localize import _
from skl_shared.graphics.root.controller import ROOT
from skl_shared.graphics.button.controller import Button
from skl_shared.graphics.label.controller import Label
from skl_shared.graphics.entry.controller import Entry
from skl_shared.graphics.checkbox.controller import CheckBox
from skl_shared.graphics.option_menu.controller import OptionMenu

PRODUCT = 'MClient'


class Settings(QWidget):
    
    sig_close = pyqtSignal()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_values()
        self.set_gui()
    
    def set_values(self):
        self.allowed = []
        self.spallow = []
        self.items = (_('Sources'), _('Dictionaries'), _('Subjects')
                     ,_('Word forms'), _('Transcription')
                     ,_('Parts of speech'), _('Do not set'))
        self.stitems = (_('Full'), PRODUCT, _('Multitran')
                       ,_('Cut to the chase'), _('Clearness'), _('Custom'))
        self.spitems = (_('Noun'), _('Verb'), _('Adjective'), _('Abbreviation')
                       ,_('Adverb'), _('Preposition'), _('Pronoun'))

    def update_sp1(self):
        f = '[MClient] settings.gui.Settings.update_sp1'
        if self.opt_sp1.get() in self.spallow:
            self.spallow.remove(self.opt_sp1.get())
        elif _('Noun') in self.spallow:
            self.opt_sp1.set(_('Noun'))
            self.spallow.remove(_('Noun'))
        elif self.spallow:
            self.opt_sp1.set(self.spallow[0])
            self.spallow.remove(self.spallow[0])
        else:
            mes = _('Empty input is not allowed!')
            Message(f, mes, True).show_error()
    
    def update_sp2(self):
        f = '[MClient] settings.gui.Settings.update_sp2'
        if self.opt_sp2.get() in self.spallow:
            self.spallow.remove(self.opt_sp2.get())
        elif _('Verb') in self.spallow:
            self.opt_sp2.set(_('Verb'))
            self.spallow.remove(_('Verb'))
        elif self.spallow:
            self.opt_sp2.set(self.spallow[0])
            self.spallow.remove(self.spallow[0])
        else:
            mes = _('Empty input is not allowed!')
            Message(f, mes, True).show_error()
                       
    def update_sp3(self):
        f = '[MClient] settings.gui.Settings.update_sp3'
        if self.opt_sp3.get() in self.spallow:
            self.spallow.remove(self.opt_sp3.get())
        elif _('Adjective') in self.spallow:
            self.opt_sp3.set(_('Adjective'))
            self.spallow.remove(_('Adjective'))
        elif self.spallow:
            self.opt_sp3.set(self.spallow[0])
            self.spallow.remove(self.spallow[0])
        else:
            mes = _('Empty input is not allowed!')
            Message(f, mes, True).show_error()
                       
    def update_sp4(self):
        f = '[MClient] settings.gui.Settings.update_sp4'
        if self.opt_sp4.get() in self.spallow:
            self.spallow.remove(self.opt_sp4.get())
        elif _('Abbreviation') in self.spallow:
            self.opt_sp4.set(_('Abbreviation'))
            self.spallow.remove(_('Abbreviation'))
        elif self.spallow:
            self.opt_sp4.set(self.spallow[0])
            self.spallow.remove(self.spallow[0])
        else:
            mes = _('Empty input is not allowed!')
            Message(f, mes, True).show_error()
                       
    def update_sp5(self):
        f = '[MClient] settings.gui.Settings.update_sp5'
        if self.opt_sp5.get() in self.spallow:
            self.spallow.remove(self.opt_sp5.get())
        elif _('Adverb') in self.spallow:
            self.opt_sp5.set(_('Adverb'))
            self.spallow.remove(_('Adverb'))
        elif self.spallow:
            self.opt_sp5.set(self.spallow[0])
            self.spallow.remove(self.spallow[0])
        else:
            mes = _('Empty input is not allowed!')
            Message(f, mes, True).show_error()
                       
    def update_sp6(self):
        f = '[MClient] settings.gui.Settings.update_sp6'
        if self.opt_sp6.get() in self.spallow:
            self.spallow.remove(self.opt_sp6.get())
        elif _('Preposition') in self.spallow:
            self.opt_sp6.set(_('Preposition'))
            self.spallow.remove(_('Preposition'))
        elif self.spallow:
            self.opt_sp6.set(self.spallow[0])
            self.spallow.remove(self.spallow[0])
        else:
            mes = _('Empty input is not allowed!')
            Message(f, mes, True).show_error()
                       
    def update_sp7(self):
        f = '[MClient] settings.gui.Settings.update_sp7'
        if self.opt_sp7.get() in self.spallow:
            self.spallow.remove(self.opt_sp7.get())
        elif _('Pronoun') in self.spallow:
            self.opt_sp7.set(_('Pronoun'))
            self.spallow.remove(_('Pronoun'))
        elif self.spallow:
            self.opt_sp7.set(self.spallow[0])
            self.spallow.remove(self.spallow[0])
        else:
            mes = _('Empty input is not allowed!')
            Message(f, mes, True).show_error()
    
    def update_col1(self):
        f = '[MClient] settings.gui.Settings.update_col1'
        if self.opt_cl1.get() == _('Do not set'):
            return
        if self.opt_cl1.get() in self.allowed:
            self.allowed.remove(self.opt_cl1.get())
        elif _('Sources') in self.allowed:
            self.opt_cl1.set(_('Sources'))
            self.allowed.remove(_('Sources'))
        elif self.allowed:
            self.opt_cl1.set(self.allowed[0])
            self.allowed.remove(self.allowed[0])
        else:
            mes = _('Empty input is not allowed!')
            Message(f, mes, True).show_error()
    
    def update_col2(self):
        f = '[MClient] settings.gui.Settings.update_col2'
        if self.opt_cl2.get() == _('Do not set'):
            return
        if self.opt_cl2.get() in self.allowed:
            self.allowed.remove(self.opt_cl2.get())
        elif _('Dictionaries') in self.allowed:
            self.opt_cl2.set(_('Dictionaries'))
            self.allowed.remove(_('Dictionaries'))
        elif self.allowed:
            self.opt_cl2.set(self.allowed[0])
            self.allowed.remove(self.allowed[0])
        else:
            mes = _('Empty input is not allowed!')
            Message(f, mes, True).show_error()
    
    def update_col3(self):
        f = '[MClient] settings.gui.Settings.update_col3'
        if self.opt_cl3.get() == _('Do not set'):
            return
        if self.opt_cl3.get() in self.allowed:
            self.allowed.remove(self.opt_cl3.get())
        elif _('Subjects') in self.allowed:
            self.opt_cl3.set(_('Subjects'))
            self.allowed.remove(_('Subjects'))
        elif self.allowed:
            self.opt_cl3.set(self.allowed[0])
            self.allowed.remove(self.allowed[0])
        else:
            mes = _('Empty input is not allowed!')
            Message(f, mes, True).show_error()

    def update_col4(self):
        f = '[MClient] settings.gui.Settings.update_col4'
        if self.opt_cl4.get() == _('Do not set'):
            return
        if self.opt_cl4.get() in self.allowed:
            self.allowed.remove(self.opt_cl4.get())
        elif _('Word forms') in self.allowed:
            self.opt_cl4.set(_('Word forms'))
            self.allowed.remove(_('Word forms'))
        elif self.allowed:
            self.opt_cl4.set(self.allowed[0])
            self.allowed.remove(self.allowed[0])
        else:
            mes = _('Empty input is not allowed!')
            Message(f, mes, True).show_error()

    def update_col5(self):
        f = '[MClient] settings.gui.Settings.update_col5'
        if self.opt_cl5.get() == _('Do not set'):
            return
        if self.opt_cl5.get() in self.allowed:
            self.allowed.remove(self.opt_cl5.get())
        elif _('Parts of speech') in self.allowed:
            self.opt_cl5.set(_('Parts of speech'))
            self.allowed.remove(_('Parts of speech'))
        elif self.allowed:
            self.opt_cl5.set(self.allowed[0])
            self.allowed.remove(self.allowed[0])
        else:
            mes = _('Empty input is not allowed!')
            Message(f, mes, True).show_error()

    def update_col6(self):
        f = '[MClient] settings.gui.Settings.update_col6'
        if self.opt_cl6.get() == _('Do not set'):
            return
        if self.opt_cl6.get() in self.allowed:
            self.allowed.remove(self.opt_cl6.get())
        elif _('Transcription') in self.allowed:
            self.opt_cl6.set(_('Transcription'))
            self.allowed.remove(_('Transcription'))
        elif self.allowed:
            self.opt_cl6.set(self.allowed[0])
            self.allowed.remove(self.allowed[0])
        else:
            mes = _('Empty input is not allowed!')
            Message(f, mes, True).show_error()

    def update_style(self):
        cond11 = self.opt_cl1.get() == _('Sources')
        cond12 = self.opt_cl1.get() == _('Subjects')
        cond13 = self.opt_cl1.get() == _('Word forms')
        cond14 = self.opt_cl1.get() == _('Parts of speech')
        cond21 = self.opt_cl2.get() == _('Dictionaries')
        cond22 = self.opt_cl2.get() == _('Word forms')
        cond23 = self.opt_cl2.get() == _('Transcription')
        cond31 = self.opt_cl3.get() == _('Subjects')        
        cond32 = self.opt_cl3.get() == _('Transcription')
        cond33 = self.opt_cl3.get() == _('Parts of speech')
        cond34 = self.opt_cl3.get() == _('Do not set')
        cond41 = self.opt_cl4.get() == _('Word forms')
        cond42 = self.opt_cl4.get() == _('Parts of speech')
        cond43 = self.opt_cl4.get() == _('Subjects')
        cond44 = self.opt_cl4.get() == _('Do not set')
        cond51 = self.opt_cl5.get() == _('Transcription')
        cond52 = self.opt_cl5.get() == _('Do not set')
        cond61 = self.opt_cl6.get() == _('Parts of speech')
        cond62 = self.opt_cl6.get() == _('Do not set')
        if cond11 and cond21 and cond31 and cond41 and cond51 and cond61:
            self.opt_stl.set(_('Full'))
        elif cond12 and cond22 and cond32 and cond42 and cond52 and cond62:
            self.opt_stl.set(PRODUCT)
        elif cond13 and cond23 and cond33 and cond43 and cond52 and cond62:
            self.opt_stl.set(_('Multitran'))
        elif cond14 and cond22 and cond32 and cond43 and cond52 and cond62:
            self.opt_stl.set(_('Cut to the chase'))
        elif cond14 and cond22 and cond34 and cond44 and cond52 and cond62:
            self.opt_stl.set(_('Clearness'))
        else:
            self.opt_stl.set(_('Custom'))

    def update_by_st(self, event=None):
        f = '[MClient] settings.gui.Settings.update_by_st'
        if self.opt_stl.get() == _('Full'):
            self.opt_cl1.set(_('Sources'))
            self.opt_cl2.set(_('Dictionaries'))
            self.opt_cl3.set(_('Subjects'))
            self.opt_cl4.set(_('Word forms'))
            self.opt_cl5.set(_('Transcription'))
            self.opt_cl6.set(_('Parts of speech'))
        elif self.opt_stl.get() == PRODUCT:
            self.opt_cl1.set(_('Subjects'))
            self.opt_cl2.set(_('Word forms'))
            self.opt_cl3.set(_('Transcription'))
            self.opt_cl4.set(_('Parts of speech'))
            self.opt_cl5.set(_('Do not set'))
            self.opt_cl6.set(_('Do not set'))
        elif self.opt_stl.get() == _('Multitran'):
            self.opt_cl1.set(_('Word forms'))
            self.opt_cl2.set(_('Transcription'))
            self.opt_cl3.set(_('Parts of speech'))
            self.opt_cl4.set(_('Subjects'))
            self.opt_cl5.set(_('Do not set'))
            self.opt_cl6.set(_('Do not set'))
        elif self.opt_stl.get() == _('Cut to the chase'):
            self.opt_cl1.set(_('Parts of speech'))
            self.opt_cl2.set(_('Word forms'))
            self.opt_cl3.set(_('Transcription'))
            self.opt_cl4.set(_('Subjects'))
            self.opt_cl5.set(_('Do not set'))
            self.opt_cl6.set(_('Do not set'))
        elif self.opt_stl.get() == _('Clearness'):
            self.opt_cl1.set(_('Parts of speech'))
            self.opt_cl2.set(_('Word forms'))
            self.opt_cl3.set(_('Do not set'))
            self.opt_cl4.set(_('Do not set'))
            self.opt_cl5.set(_('Do not set'))
            self.opt_cl6.set(_('Do not set'))
        elif self.opt_stl.get() == _('Custom'):
            pass
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(self.opt_stl.get(), self.stitems)
            Message(f, mes, True).show_error()

    def update_by_col1(self):
        self.allowed = list(self.items)
        self.update_col1()
        self.update_col2()
        self.update_col3()
        self.update_col4()
        self.update_col5()
        self.update_col6()
        self.update_style()

    def update_by_col2(self):
        self.allowed = list(self.items)
        self.update_col2()
        self.update_col1()
        self.update_col3()
        self.update_col4()
        self.update_col5()
        self.update_col6()
        self.update_style()

    def update_by_col3(self):
        self.allowed = list(self.items)
        self.update_col3()
        self.update_col1()
        self.update_col2()
        self.update_col4()
        self.update_col5()
        self.update_col6()
        self.update_style()

    def update_by_col4(self, event=None):
        self.allowed = list(self.items)
        self.update_col4()
        self.update_col1()
        self.update_col2()
        self.update_col3()
        self.update_col5()
        self.update_col6()
        self.update_style()
    
    def update_by_col5(self, event=None):
        self.allowed = list(self.items)
        self.update_col5()
        self.update_col1()
        self.update_col2()
        self.update_col3()
        self.update_col4()
        self.update_col6()
        self.update_style()
    
    def update_by_col6(self, event=None):
        self.allowed = list(self.items)
        self.update_col6()
        self.update_col1()
        self.update_col2()
        self.update_col3()
        self.update_col4()
        self.update_col5()
        self.update_style()
        
    def update_by_sp1(self):
        self.spallow = list(self.spitems)
        self.update_sp1()
        self.update_sp2()
        self.update_sp3()
        self.update_sp4()
        self.update_sp5()
        self.update_sp6()
        self.update_sp7()
        
    def update_by_sp2(self):
        self.spallow = list(self.spitems)
        self.update_sp2()
        self.update_sp1()
        self.update_sp3()
        self.update_sp4()
        self.update_sp5()
        self.update_sp6()
        self.update_sp7()
        
    def update_by_sp3(self):
        self.spallow = list(self.spitems)
        self.update_sp3()
        self.update_sp1()
        self.update_sp2()
        self.update_sp4()
        self.update_sp5()
        self.update_sp6()
        self.update_sp7()
        
    def update_by_sp4(self):
        self.spallow = list(self.spitems)
        self.update_sp4()
        self.update_sp1()
        self.update_sp2()
        self.update_sp3()
        self.update_sp5()
        self.update_sp6()
        self.update_sp7()
        
    def update_by_sp5(self):
        self.spallow = list(self.spitems)
        self.update_sp5()
        self.update_sp1()
        self.update_sp2()
        self.update_sp3()
        self.update_sp4()
        self.update_sp6()
        self.update_sp7()
        
    def update_by_sp6(self):
        self.spallow = list(self.spitems)
        self.update_sp6()
        self.update_sp1()
        self.update_sp2()
        self.update_sp3()
        self.update_sp4()
        self.update_sp5()
        self.update_sp7()
        
    def update_by_sp7(self):
        self.spallow = list(self.spitems)
        self.update_sp7()
        self.update_sp1()
        self.update_sp2()
        self.update_sp3()
        self.update_sp4()
        self.update_sp5()
        self.update_sp6()
    
    def reset(self):
        self.opt_stl.set(PRODUCT)
        self.opt_cl1.set(_('Subjects'))
        self.opt_cl2.set(_('Word forms'))
        self.opt_cl3.set(_('Parts of speech'))
        self.opt_cl4.set(_('Transcription'))
        self.opt_cl5.set(_('Do not set'))
        self.opt_cl6.set(_('Do not set'))
        self.opt_sp1.set(_('Noun'))
        self.opt_sp2.set(_('Verb'))
        self.opt_sp3.set(_('Adjective'))
        self.opt_sp4.set(_('Abbreviation'))
        self.opt_sp5.set(_('Adverb'))
        self.opt_sp6.set(_('Preposition'))
        self.opt_sp7.set(_('Pronoun'))
        self.cbx_no1.enable()
        self.cbx_no2.enable()
        self.cbx_no3.disable()
        self.cbx_no4.disable()
        self.cbx_no5.enable()
        self.cbx_no6.disable()
        self.cbx_no7.enable()
        self.cbx_no8.enable()
    
    def closeEvent(self, event):
        self.sig_close.emit()
        return super().closeEvent(event)
    
    def centralize(self):
        self.move(ROOT.get_root().primaryScreen().geometry().center() - self.rect().center())
    
    def set_labels(self):
        self.lbl_stl = Label(_('Style:'))
        mes = _('Column {}:')
        self.lbl_cl1 = Label(mes.format(1))
        self.lbl_cl2 = Label(mes.format(2))
        self.lbl_cl3 = Label(mes.format(3))
        self.lbl_cl4 = Label(mes.format(4))
        self.lbl_cl5 = Label(mes.format(5))
        self.lbl_cl6 = Label(mes.format(6))
        mes = _('Part of speech {}:')
        self.lbl_sp1 = Label(mes.format(1))
        self.lbl_sp2 = Label(mes.format(2))
        self.lbl_sp3 = Label(mes.format(3))
        self.lbl_sp4 = Label(mes.format(4))
        self.lbl_sp5 = Label(mes.format(5))
        self.lbl_sp6 = Label(mes.format(6))
        self.lbl_sp7 = Label(mes.format(7))
    
    def set_menus(self):
        self.opt_stl = OptionMenu(items = self.stitems, default = PRODUCT
                                 ,action = self.update_by_st)
        self.opt_cl1 = OptionMenu(items = self.items, default = _('Subjects')
                                 ,action = self.update_by_col1)
        self.opt_cl2 = OptionMenu(items = self.items, default = _('Word forms')
                                 ,action = self.update_by_col2)
        self.opt_cl3 = OptionMenu(items = self.items
                                 ,default = _('Transcription')
                                 ,action = self.update_by_col3)
        self.opt_cl4 = OptionMenu(items = self.items
                                 ,default = _('Parts of speech')
                                 ,action = self.update_by_col4)
        self.opt_cl5 = OptionMenu(items = self.items
                                 ,default = _('Do not set')
                                 ,action = self.update_by_col5)
        self.opt_cl6 = OptionMenu(items = self.items
                                 ,default = _('Do not set')
                                 ,action = self.update_by_col6)
        self.opt_sp1 = OptionMenu(items = self.spitems
                                 ,default = _('Noun')
                                 ,action = self.update_by_sp1)
        self.opt_sp2 = OptionMenu(items = self.spitems, default = _('Verb')
                                 ,action = self.update_by_sp2)
        self.opt_sp3 = OptionMenu(items = self.spitems
                                 ,default = _('Adjective')
                                 ,action = self.update_by_sp3)
        self.opt_sp4 = OptionMenu(items = self.spitems
                                 ,default = _('Abbreviation')
                                 ,action = self.update_by_sp4)
        self.opt_sp5 = OptionMenu(items = self.spitems
                                 ,default = _('Adverb')
                                 ,action = self.update_by_sp5)
        self.opt_sp6 = OptionMenu(items = self.spitems
                                 ,default = _('Preposition')
                                 ,action = self.update_by_sp6)
        self.opt_sp7 = OptionMenu(items = self.spitems
                                 ,default = _('Pronoun')
                                 ,action = self.update_by_sp7)
    
    def set_layouts(self):
        self.lay_prm = QVBoxLayout(self)
        self.lay_col = QGridLayout()
        self.lay_psp = QGridLayout()
        self.lay_cbx = QVBoxLayout()
        self.lay_sug = QHBoxLayout()
        self.lay_sgl = QHBoxLayout()
        ''' Position widgets in "Suggest" row correctly for different languages
            irrespectively of label widths.
        '''
        self.fml_sug = QFormLayout()
        self.fml_sug.addRow(self.lay_sgl)
        self.lay_btn = QHBoxLayout()
        self.lay_sug.addLayout(self.fml_sug)
        self.lay_prm.addLayout(self.lay_col)
        self.lay_prm.addLayout(self.lay_psp)
        self.lay_prm.addLayout(self.lay_cbx)
        self.lay_prm.addLayout(self.lay_sug)
        self.lay_prm.addLayout(self.lay_btn)
    
    def set_checkboxes(self):
        self.cbx_no1 = CheckBox(_('Sort by each column (if it is set, except for transcription) and order parts of speech'))
        self.cbx_no2 = CheckBox(_('Shorten subject titles'))
        self.cbx_no3 = CheckBox(_('Shorten parts of speech'))
        self.cbx_no4 = CheckBox(_('Show user names'))
        self.cbx_no5 = CheckBox(_('Iconify the program window after copying'))
        self.cbx_no6 = CheckBox(_('Autoswap Russian and the other language if appropriate'))
        self.cbx_no7 = CheckBox(_('Show a phrase count'))
        self.cbx_no8 = CheckBox(_('Resize rows to contents'))
    
    def set_bg(self):
        self.bg_col = QWidget()
        # Cannot reuse the same widget
        self.bg_psp = QWidget()
        self.lay_col.addWidget(self.bg_col, 0, 0, 1, 7)
        self.lay_psp.addWidget(self.bg_psp, 0, 0, 1, 7)
    
    def set_suggest(self):
        self.lbl_num = Label(_('Preferred number of columns:'))
        self.ent_num = Entry()
        self.lbl_fix = Label(_('Fixed column width:'))
        self.ent_fix = Entry()
        self.lbl_trm = Label(_('Term column width:'))
        self.ent_trm = Entry()
        self.btn_sug = Button(_('Suggest'))
    
    def _add_columns(self):
        self.lay_col.addWidget(self.lbl_stl.widget, 0, 0, Qt.AlignmentFlag.AlignCenter)
        self.lay_col.addWidget(self.lbl_cl1.widget, 0, 1, Qt.AlignmentFlag.AlignCenter)
        self.lay_col.addWidget(self.lbl_cl2.widget, 0, 2, Qt.AlignmentFlag.AlignCenter)
        self.lay_col.addWidget(self.lbl_cl3.widget, 0, 3, Qt.AlignmentFlag.AlignCenter)
        self.lay_col.addWidget(self.lbl_cl4.widget, 0, 4, Qt.AlignmentFlag.AlignCenter)
        self.lay_col.addWidget(self.lbl_cl5.widget, 0, 5, Qt.AlignmentFlag.AlignCenter)
        self.lay_col.addWidget(self.lbl_cl6.widget, 0, 6, Qt.AlignmentFlag.AlignCenter)
        self.lay_col.addWidget(self.opt_stl.widget, 1, 0)
        self.lay_col.addWidget(self.opt_cl1.widget, 1, 1)
        self.lay_col.addWidget(self.opt_cl2.widget, 1, 2)
        self.lay_col.addWidget(self.opt_cl3.widget, 1, 3)
        self.lay_col.addWidget(self.opt_cl4.widget, 1, 4)
        self.lay_col.addWidget(self.opt_cl5.widget, 1, 5)
        self.lay_col.addWidget(self.opt_cl6.widget, 1, 6)
    
    def _add_speech(self):
        self.lay_psp.addWidget(self.lbl_sp1.widget, 0, 0, Qt.AlignmentFlag.AlignCenter)
        self.lay_psp.addWidget(self.lbl_sp2.widget, 0, 1, Qt.AlignmentFlag.AlignCenter)
        self.lay_psp.addWidget(self.lbl_sp3.widget, 0, 2, Qt.AlignmentFlag.AlignCenter)
        self.lay_psp.addWidget(self.lbl_sp4.widget, 0, 3, Qt.AlignmentFlag.AlignCenter)
        self.lay_psp.addWidget(self.lbl_sp5.widget, 0, 4, Qt.AlignmentFlag.AlignCenter)
        self.lay_psp.addWidget(self.lbl_sp6.widget, 0, 5, Qt.AlignmentFlag.AlignCenter)
        self.lay_psp.addWidget(self.lbl_sp7.widget, 0, 6, Qt.AlignmentFlag.AlignCenter)
        self.lay_psp.addWidget(self.opt_sp1.widget, 1, 0)
        self.lay_psp.addWidget(self.opt_sp2.widget, 1, 1)
        self.lay_psp.addWidget(self.opt_sp3.widget, 1, 2)
        self.lay_psp.addWidget(self.opt_sp4.widget, 1, 3)
        self.lay_psp.addWidget(self.opt_sp5.widget, 1, 4)
        self.lay_psp.addWidget(self.opt_sp6.widget, 1, 5)
        self.lay_psp.addWidget(self.opt_sp7.widget, 1, 6)
    
    def _add_checkboxes(self):
        self.lay_cbx.addWidget(self.cbx_no1.widget)
        self.lay_cbx.addWidget(self.cbx_no2.widget)
        self.lay_cbx.addWidget(self.cbx_no3.widget)
        self.lay_cbx.addWidget(self.cbx_no4.widget)
        self.lay_cbx.addWidget(self.cbx_no5.widget)
        self.lay_cbx.addWidget(self.cbx_no6.widget)
        self.lay_cbx.addWidget(self.cbx_no7.widget)
        self.lay_cbx.addWidget(self.cbx_no8.widget)
    
    def _add_suggest(self):
        self.lay_sgl.addWidget(self.lbl_num.widget)
        self.lay_sgl.addWidget(self.ent_num.widget)
        self.lay_sgl.addWidget(self.lbl_fix.widget)
        self.lay_sgl.addWidget(self.ent_fix.widget)
        self.lay_sgl.addWidget(self.lbl_trm.widget)
        self.lay_sgl.addWidget(self.ent_trm.widget)
        self.lay_sug.addWidget(self.btn_sug.widget)
    
    def _add_buttons(self):
        self.lay_btn.addWidget(self.btn_res.widget)
        ''' This value is picked up manually and depends on the window width.
            However, we can set a value surpassing the window width.
        '''
        self.lay_btn.insertSpacing(1, 650)
        self.lay_btn.addWidget(self.btn_apl.widget)
    
    def add_widgets(self):
        self._add_columns()
        self._add_speech()
        self._add_checkboxes()
        self._add_suggest()
        self._add_buttons()
    
    def configure(self):
        self.bg_col.setStyleSheet('background-color: #3a5fcd')
        self.bg_psp.setStyleSheet('background-color: #3a5fcd')
        self.setStyleSheet('QLabel {color: #bbffff}')
        
        self.lbl_num.widget.setStyleSheet('color: black')
        self.lbl_fix.widget.setStyleSheet('color: black')
        self.lbl_trm.widget.setStyleSheet('color: black')
        
        self.ent_num.set_max_width(20)
        self.ent_fix.set_max_width(35)
        self.ent_trm.set_max_width(35)
        
        # 10 -> 11
        # self.cbx_no1.change_font_size(1)
        # self.cbx_no2.change_font_size(1)
        # self.cbx_no3.change_font_size(1)
        # self.cbx_no4.change_font_size(1)
        # self.cbx_no5.change_font_size(1)
        # self.cbx_no6.change_font_size(1)
        # self.cbx_no7.change_font_size(1)
        # self.cbx_no8.change_font_size(1)
        
        # self.opt_stl.change_font_size(1)
        # self.opt_cl1.change_font_size(1)
        # self.opt_cl2.change_font_size(1)
        # self.opt_cl3.change_font_size(1)
        # self.opt_cl4.change_font_size(1)
        # self.opt_sp1.change_font_size(1)
        # self.opt_sp2.change_font_size(1)
        # self.opt_sp3.change_font_size(1)
        # self.opt_sp4.change_font_size(1)
        # self.opt_sp5.change_font_size(1)
        # self.opt_sp6.change_font_size(1)
        # self.opt_sp7.change_font_size(1)
        
        # Prevent layout from taking all available space
        self.lay_sgl.addStretch(0)
    
    def set_buttons(self):
        self.btn_res = Button(text = _('Reset')
                             ,hint = _('Restore recommended settings')
                             ,action = self.reset)
        self.btn_apl = Button(text = _('Apply')
                             ,hint = _('Apply current settings and reload the article'))
    
    def set_gui(self):
        self.set_layouts()
        self.set_menus()
        self.set_labels()
        self.set_bg()
        self.set_checkboxes()
        self.set_suggest()
        self.set_buttons()
        self.add_widgets()
        self.configure()
        # The window width will be larger than 1024px otherwise 
        self.setFixedWidth(800)
    
    def set_title(self, title):
        self.setWindowTitle(title)
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            QShortcut(QKeySequence(hotkey), self).activated.connect(action)
