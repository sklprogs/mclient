#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt5.QtWidgets

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

PRODUCT = 'MClient'


class Settings(PyQt5.QtWidgets.QWidget):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_values()
        self.set_gui()
    
    def set_values(self):
        self.items = (_('Subjects')
                     ,_('Word forms')
                     ,_('Transcription')
                     ,_('Parts of speech')
                     ,_('Do not set')
                     )
        self.stitems = (PRODUCT
                       ,_('Multitran')
                       ,_('Cut to the chase')
                       ,_('Clearness')
                       ,_('Custom')
                       )
        self.spitems = (_('Noun'),_('Verb'),_('Adjective')
                       ,_('Abbreviation'),_('Adverb')
                       ,_('Preposition'),_('Pronoun')
                       )
    
    def centralize(self):
        self.move(sh.objs.get_root().desktop().screen().rect().center() - self.rect().center())
    
    def set_labels(self):
        self.lbl_stl = sh.Label(_('Style:'))
        mes = _('Column {}:')
        self.lbl_cl1 = sh.Label(mes.format(1))
        self.lbl_cl2 = sh.Label(mes.format(2))
        self.lbl_cl3 = sh.Label(mes.format(3))
        self.lbl_cl4 = sh.Label(mes.format(4))
        mes = _('Part of speech {}:')
        self.lbl_sp1 = sh.Label(mes.format(1))
        self.lbl_sp2 = sh.Label(mes.format(2))
        self.lbl_sp3 = sh.Label(mes.format(3))
        self.lbl_sp4 = sh.Label(mes.format(4))
        self.lbl_sp5 = sh.Label(mes.format(5))
        self.lbl_sp6 = sh.Label(mes.format(6))
        self.lbl_sp7 = sh.Label(mes.format(7))
    
    def set_menus(self):
        self.opt_stl = sh.OptionMenu(self.stitems,PRODUCT)
        self.opt_cl1 = sh.OptionMenu(self.items,_('Subjects'))
        self.opt_cl2 = sh.OptionMenu(self.items,_('Word forms'))
        self.opt_cl3 = sh.OptionMenu(self.items,_('Transcription'))
        self.opt_cl4 = sh.OptionMenu(self.items,_('Parts of speech'))
        self.opt_sp1 = sh.OptionMenu(self.spitems,_('Noun'))
        self.opt_sp2 = sh.OptionMenu(self.spitems,_('Verb'))
        self.opt_sp3 = sh.OptionMenu(self.spitems,_('Adjective'))
        self.opt_sp4 = sh.OptionMenu(self.spitems,_('Abbreviation'))
        self.opt_sp5 = sh.OptionMenu(self.spitems,_('Adverb'))
        self.opt_sp6 = sh.OptionMenu(self.spitems,_('Preposition'))
        self.opt_sp7 = sh.OptionMenu(self.spitems,_('Pronoun'))
    
    def set_layouts(self):
        self.lay_prm = PyQt5.QtWidgets.QVBoxLayout(self)
        self.lay_col = PyQt5.QtWidgets.QGridLayout()
        self.lay_psp = PyQt5.QtWidgets.QGridLayout()
        self.lay_cbx = PyQt5.QtWidgets.QVBoxLayout()
        self.lay_sug = PyQt5.QtWidgets.QHBoxLayout()
        self.lay_btn = PyQt5.QtWidgets.QHBoxLayout()
        self.lay_prm.addLayout(self.lay_col)
        self.lay_prm.addLayout(self.lay_psp)
        self.lay_prm.addLayout(self.lay_cbx)
        self.lay_prm.addLayout(self.lay_sug)
        self.lay_prm.addLayout(self.lay_btn)
    
    def set_checkboxes(self):
        self.cbx_op1 = sh.CheckBox(_('Sort by each column (if it is set, except for transcription) and order parts of speech'))
        self.cbx_op2 = sh.CheckBox(_('Shorten subject titles'))
        self.cbx_op3 = sh.CheckBox(_('Shorten parts of speech'))
        self.cbx_op4 = sh.CheckBox(_('Show user names'))
        self.cbx_op5 = sh.CheckBox(_('Iconify the program window after copying'))
        self.cbx_op6 = sh.CheckBox(_('Show suggestions on input'))
        self.cbx_op7 = sh.CheckBox(_('Autoswap Russian and the other language if appropriate'))
        self.cbx_op8 = sh.CheckBox(_('Show a phrase count'))
        self.cbx_op9 = sh.CheckBox(_('Adjust columns by width'))
    
    def set_bg(self):
        self.bg_col = PyQt5.QtWidgets.QWidget()
        # Cannot reuse the same widget
        self.bg_psp = PyQt5.QtWidgets.QWidget()
        self.lay_col.addWidget(self.bg_col,0,0,1,5)
        self.lay_psp.addWidget(self.bg_psp,0,0,1,7)
    
    def set_suggest(self):
        self.lbl_num = sh.Label(_('Preferred number of columns:'))
        self.ent_num = sh.Entry()
        self.lbl_fix = sh.Label(_('Fixed column width:'))
        self.ent_fix = sh.Entry()
        self.lbl_trm = sh.Label(_('Term column width:'))
        self.ent_trm = sh.Entry()
        self.btn_sug = sh.Button(_('Suggest'))
    
    def _add_columns(self):
        self.lay_col.addWidget(self.lbl_stl.widget,0,0,PyQt5.QtCore.Qt.AlignCenter)
        self.lay_col.addWidget(self.lbl_cl1.widget,0,1,PyQt5.QtCore.Qt.AlignCenter)
        self.lay_col.addWidget(self.lbl_cl2.widget,0,2,PyQt5.QtCore.Qt.AlignCenter)
        self.lay_col.addWidget(self.lbl_cl3.widget,0,3,PyQt5.QtCore.Qt.AlignCenter)
        self.lay_col.addWidget(self.lbl_cl4.widget,0,4,PyQt5.QtCore.Qt.AlignCenter)
        self.lay_col.addWidget(self.opt_stl.widget,1,0)
        self.lay_col.addWidget(self.opt_cl1.widget,1,1)
        self.lay_col.addWidget(self.opt_cl2.widget,1,2)
        self.lay_col.addWidget(self.opt_cl3.widget,1,3)
        self.lay_col.addWidget(self.opt_cl4.widget,1,4)
    
    def _add_speech(self):
        self.lay_psp.addWidget(self.lbl_sp1.widget,0,0,PyQt5.QtCore.Qt.AlignCenter)
        self.lay_psp.addWidget(self.lbl_sp2.widget,0,1,PyQt5.QtCore.Qt.AlignCenter)
        self.lay_psp.addWidget(self.lbl_sp3.widget,0,2,PyQt5.QtCore.Qt.AlignCenter)
        self.lay_psp.addWidget(self.lbl_sp4.widget,0,3,PyQt5.QtCore.Qt.AlignCenter)
        self.lay_psp.addWidget(self.lbl_sp5.widget,0,4,PyQt5.QtCore.Qt.AlignCenter)
        self.lay_psp.addWidget(self.lbl_sp6.widget,0,5,PyQt5.QtCore.Qt.AlignCenter)
        self.lay_psp.addWidget(self.lbl_sp7.widget,0,6,PyQt5.QtCore.Qt.AlignCenter)
        self.lay_psp.addWidget(self.opt_sp1.widget,1,0)
        self.lay_psp.addWidget(self.opt_sp2.widget,1,1)
        self.lay_psp.addWidget(self.opt_sp3.widget,1,2)
        self.lay_psp.addWidget(self.opt_sp4.widget,1,3)
        self.lay_psp.addWidget(self.opt_sp5.widget,1,4)
        self.lay_psp.addWidget(self.opt_sp6.widget,1,5)
        self.lay_psp.addWidget(self.opt_sp7.widget,1,6)
    
    def _add_checkboxes(self):
        self.lay_cbx.addWidget(self.cbx_op1.widget)
        self.lay_cbx.addWidget(self.cbx_op2.widget)
        self.lay_cbx.addWidget(self.cbx_op3.widget)
        self.lay_cbx.addWidget(self.cbx_op4.widget)
        self.lay_cbx.addWidget(self.cbx_op5.widget)
        self.lay_cbx.addWidget(self.cbx_op6.widget)
        self.lay_cbx.addWidget(self.cbx_op7.widget)
        self.lay_cbx.addWidget(self.cbx_op8.widget)
        self.lay_cbx.addWidget(self.cbx_op9.widget)
    
    def _add_suggest(self):
        self.lay_sug.addWidget(self.lbl_num.widget)
        self.lay_sug.addWidget(self.ent_num.widget)
        self.lay_sug.addWidget(self.lbl_fix.widget)
        self.lay_sug.addWidget(self.ent_fix.widget)
        self.lay_sug.addWidget(self.lbl_trm.widget)
        self.lay_sug.addWidget(self.ent_trm.widget)
        self.lay_sug.addWidget(self.btn_sug.widget)
    
    def _add_buttons(self):
        self.lay_btn.addWidget(self.btn_res.widget)
        ''' This value is picked up manually and depends on the window width.
            However, we can set a value surpassing the window width.
        '''
        self.lay_btn.insertSpacing(1,650)
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
        
        # 9 -> 11
        self.cbx_op1.change_font_size(2)
        self.cbx_op2.change_font_size(2)
        self.cbx_op3.change_font_size(2)
        self.cbx_op4.change_font_size(2)
        self.cbx_op5.change_font_size(2)
        self.cbx_op6.change_font_size(2)
        self.cbx_op7.change_font_size(2)
        self.cbx_op8.change_font_size(2)
        self.cbx_op9.change_font_size(2)
        
        self.opt_stl.change_font_size(1)
        self.opt_cl1.change_font_size(1)
        self.opt_cl2.change_font_size(1)
        self.opt_cl3.change_font_size(1)
        self.opt_cl4.change_font_size(1)
        self.opt_sp1.change_font_size(1)
        self.opt_sp2.change_font_size(1)
        self.opt_sp3.change_font_size(1)
        self.opt_sp4.change_font_size(1)
        self.opt_sp5.change_font_size(1)
        self.opt_sp6.change_font_size(1)
        self.opt_sp7.change_font_size(1)
    
    def set_buttons(self):
        self.btn_res = sh.Button(_('Reset'))
        self.btn_apl = sh.Button(_('Apply'))
    
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
    
    def set_title(self,title):
        self.setWindowTitle(title)
    
    def bind(self,hotkey,action):
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence(hotkey),self).activated.connect(action)


if __name__ == '__main__':
    f = '__main__'
    sh.com.start()
    app = Settings()
    app.show()
    sh.com.end()
