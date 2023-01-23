#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt5
import PyQt5.QtWidgets

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

icn_btm = sh.objs.get_pdir().add('..','resources','buttons','bottom.png')
icn_clr = sh.objs.pdir.add('..','resources','buttons','clear_selection.png')
icn_dwn = sh.objs.pdir.add('..','resources','buttons','down.png')
icn_grp = sh.objs.pdir.add('..','resources','buttons','double_back.png')
icn_gru = sh.objs.pdir.add('..','resources','buttons','double_forward.png')
icn_lft = sh.objs.pdir.add('..','resources','buttons','go_back.png')
icn_rht = sh.objs.pdir.add('..','resources','buttons','go_forward.png')
icn_rld = sh.objs.pdir.add('..','resources','buttons','reload.png')
icn_top = sh.objs.pdir.add('..','resources','buttons','top.png')
icn_up1 = sh.objs.pdir.add('..','resources','buttons','up.png')


class Priorities(PyQt5.QtWidgets.QWidget):
    
    sig_close = PyQt5.QtCore.pyqtSignal()
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_gui()
    
    def set_icon(self):
        # Does not accent None
        self.setWindowIcon(sh.gi.objs.get_icon())
    
    def closeEvent(self,event):
        self.sig_close.emit()
        return super().closeEvent(event)
    
    def set_title(self,title):
        self.setWindowTitle(title)
    
    def centralize(self):
        self.move(sh.objs.get_root().desktop().screen().rect().center() - self.rect().center())
    
    def bind(self,hotkey,action):
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence(hotkey),self).activated.connect(action)
    
    def get_checkbox(self):
        return self.cbx_pri.get()
    
    def set_checkbox(self,Active=False):
        self.cbx_pri.set(Active)
    
    def set_prioritize(self):
        self.cbx_pri = sh.CheckBox (parent = self.frm_bm2
                                   ,side = 'left'
                                   )
        self.lbl_pri = sh.Label (parent = self.frm_bm2
                                ,text = _('Prioritize subjects')
                                ,side = 'left'
                                )
    
    def set_scrolly(self):
        sh.Scrollbar (parent = self.frm_vr1
                     ,scroll = self.lbx_lft
                     )
        sh.Scrollbar (parent = self.frm_vr2
                     ,scroll = self.lbx_rht
                     )
    
    def select_mult1(self,indexes):
        self.lbx_lft.select_mult(indexes)
    
    def select_mult2(self,indexes):
        self.lbx_rht.select_mult(indexes)
    
    def colorize1(self,i,bg='cyan'):
        self.lbx_lft.widget.itemconfig(i,{'bg':bg})
    
    def colorize2(self,i,bg='cyan'):
        self.lbx_rht.widget.itemconfig(i,{'bg':bg})
    
    def get_index_mult1(self):
        return self.lbx_lft.get_index_mult()
    
    def get_index_mult2(self):
        return self.lbx_rht.get_index_mult()
    
    def get_sel1(self):
        return self.lbx_lft.get()
    
    def get_sel2(self):
        return self.lbx_rht.get()
    
    def clear_sel1(self):
        self.lbx_lft.clear_sel()
    
    def clear_sel2(self):
        self.lbx_rht.clear_sel()
    
    def reset1(self,lst=[]):
        self.lbx_lft.reset(lst)
        self.clear_sel1()
    
    def reset2(self,lst=[]):
        self.lbx_rht.reset(lst)
        self.clear_sel2()
    
    def get1(self):
        return self.lbx_lft.lst
    
    def get2(self):
        return self.lbx_rht.lst
    
    def set_frames(self):
        self.frm_top = sh.Frame (parent = self.parent
                                ,side = 'top'
                                )
        self.frm_btm = sh.Frame (parent = self.parent
                                ,side = 'bottom'
                                ,expand = False
                                )
        self.frm_bm1 = sh.Frame (parent = self.frm_btm
                                ,side = 'left'
                                )
        self.frm_bm2 = sh.Frame (parent = self.frm_btm
                                ,side = 'left'
                                )
        self.frm_bm3 = sh.Frame (parent = self.frm_btm
                                ,side = 'right'
                                ,expand = False
                                )
        self.frm_lft = sh.Frame (parent = self.frm_top
                                ,side = 'left'
                                ,propag = False
                                ,width = 350
                                )
        self.frm_vr1 = sh.Frame (parent = self.frm_top
                                ,side = 'left'
                                ,expand = False
                                ,fill = 'y'
                                )
        self.frm_cnt = sh.Frame (parent = self.frm_top
                                ,side = 'left'
                                ,expand = False
                                )
        self.frm_rht = sh.Frame (parent = self.frm_top
                                ,side = 'left'
                                ,propag = False
                                ,width = 350
                                )
        self.frm_vr2 = sh.Frame (parent = self.frm_top
                                ,expand = False
                                ,fill = 'y'
                                ,side = 'left'
                                )
        self.frm_bt1 = sh.Frame (parent = self.frm_cnt
                                ,side = 'top'
                                )
        self.frm_bt2 = sh.Frame (parent = self.frm_cnt
                                ,side = 'top'
                                ,expand = False
                                )
        self.frm_bt3 = sh.Frame (parent = self.frm_cnt
                                ,side = 'bottom'
                                )
    
    def set_listboxes(self):
        self.lbx_lft = sh.ListBox (parent = self.frm_lft
                                  ,Multiple = True
                                  )
        self.lbx_rht = sh.ListBox (parent = self.frm_rht
                                  ,Multiple = True
                                  )
    
    def set_buttons(self):
        self.btn_lft = sh.Button (hint = _('Prioritize selection on the right')
                                 ,inactive = icn_lft
                                 ,active = icn_lft
                                 )
        self.btn_rht = sh.Button (hint = _('Unprioritize selection on the left')
                                 ,inactive = icn_rht
                                 ,active = icn_rht
                                 )
        self.btn_grp = sh.Button (hint = _('Prioritize related subjects')
                                 ,inactive = icn_grp
                                 ,active = icn_grp
                                 )
        self.btn_gru = sh.Button (hint = _('Unprioritize related subjects')
                                 ,inactive = icn_gru
                                 ,active = icn_gru
                                 )
        self.btn_up1 = sh.Button (hint = _('Increase priority')
                                 ,inactive = icn_up1
                                 ,active = icn_up1
                                 )
        self.btn_dwn = sh.Button (hint = _('Decrease priority')
                                 ,inactive = icn_dwn
                                 ,active = icn_dwn
                                 )
        self.btn_top = sh.Button (hint = _('Move to the top')
                                 ,inactive = icn_top
                                 ,active = icn_top
                                 )
        self.btn_btm = sh.Button (hint = _('Move to the bottom')
                                 ,inactive = icn_btm
                                 ,active = icn_btm
                                 )
        self.btn_clr = sh.Button (hint = _('Clear selection in both panes')
                                 ,inactive = icn_clr
                                 ,active = icn_clr
                                 )
        self.btn_rld = sh.Button (hint = _('Reload settings')
                                 ,inactive = icn_rld
                                 ,active = icn_rld
                                 )
        '''
        self.btn_cls = sh.Button (text = _('Close')
                                 ,hint = _('Close this window')
                                 )
        self.btn_all = sh.Button (text = _('All')
                                 ,hint = _('Show all subjects')
                                 )
        self.btn_mjr = sh.Button (text = _('Main')
                                 ,hint = _('Show main subjects')
                                 )
        self.btn_art = sh.Button (text = _('From the article')
                                 ,hint = _('Show subjects from the current article')
                                 )
        '''
    
    def set_widgets(self):
        self.layout_ = PyQt5.QtWidgets.QGridLayout()
        self.lbx_lft = PyQt5.QtWidgets.QTreeView()
        self.lbx_rht = PyQt5.QtWidgets.QTreeView()
        self.prm_btn = PyQt5.QtWidgets.QWidget()
        self.lay_btn = PyQt5.QtWidgets.QVBoxLayout()
        self.set_buttons()
    
    def add_widgets(self):
        self.layout_.addWidget(self.lbx_lft,0,0)
        self.layout_.addWidget(self.prm_btn,0,1)
        self.layout_.addWidget(self.lbx_rht,0,2)
        self.add_buttons()
        self.prm_btn.setLayout(self.lay_btn)
        self.setLayout(self.layout_)
    
    def add_buttons(self):
        self.lay_btn.addWidget(self.btn_lft.widget)
        self.lay_btn.addWidget(self.btn_rht.widget)
        self.lay_btn.addWidget(self.btn_grp.widget)
        self.lay_btn.addWidget(self.btn_gru.widget)
        self.lay_btn.addWidget(self.btn_up1.widget)
        self.lay_btn.addWidget(self.btn_dwn.widget)
        self.lay_btn.addWidget(self.btn_top.widget)
        self.lay_btn.addWidget(self.btn_btm.widget)
        self.lay_btn.addWidget(self.btn_clr.widget)
        self.lay_btn.addWidget(self.btn_rld.widget)
        '''
        self.lay_btn.addWidget(self.btn_cls.widget)
        self.lay_btn.addWidget(self.btn_all.widget)
        self.lay_btn.addWidget(self.btn_mjr.widget)
        self.lay_btn.addWidget(self.btn_art.widget)
        '''
    
    def set_gui(self):
        self.set_title(_('Subject prioritization'))
        self.set_icon()
        self.set_widgets()
        self.add_widgets()
        self.customize()
    
    def customize(self):
        self.layout_.setContentsMargins(0,0,0,0)
        self.lay_btn.setContentsMargins(4,4,4,4)


if __name__ == '__main__':
    f = '[MClient] subjects.priorities.gui.__main__'
    sh.com.start()
    iprior = Priorities()
    iprior.show()
    iprior.resize(800,450)
    iprior.centralize()
    sh.com.end()
