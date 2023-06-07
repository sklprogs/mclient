#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt5
import PyQt5.QtWidgets

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

icn_btm = sh.objs.get_pdir().add('..','resources', 'buttons', 'bottom.png')
icn_dwn = sh.objs.pdir.add('..', 'resources', 'buttons', 'down.png')
icn_lft = sh.objs.pdir.add('..', 'resources', 'buttons', 'go_back.png')
icn_rht = sh.objs.pdir.add('..', 'resources', 'buttons', 'go_next.png')
icn_top = sh.objs.pdir.add('..', 'resources', 'buttons', 'top.png')
icn_up1 = sh.objs.pdir.add('..', 'resources', 'buttons', 'up.png')


class Model(PyQt5.QtGui.QStandardItemModel):
    
    def __init__(self, dic, header='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dic = dic
        self.header = header
        self.Success = True
        self.fill()
    
    def fill(self):
        f = '[MClientQt] subjects.priorities.gui.Model.fill'
        if not self.dic:
            self.Success = False
            sh.com.rep_empty(f)
            return
        self.parse_json()
        self.set_headers()
    
    def _set_item(self, key):
        # Multi-level filling: https://stackoverflow.com/questions/57130400/multi-level-qtreeview-using-dictionaries
        item = PyQt5.QtGui.QStandardItem(str(key))
        self.root.appendRow(item)
        for value in self.dic[key]:
            child = PyQt5.QtGui.QStandardItem(str(value))
            item.appendRow(child)
    
    def parse_json(self):
        f = '[MClientQt] subjects.priorities.gui.Model.parse_json'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.root = self.invisibleRootItem()
        for key in self.dic:
            self._set_item(key)
    
    def set_headers(self):
        f = '[MClientQt] subjects.priorities.gui.Model.set_headers'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.setHorizontalHeaderLabels([self.header])



class Priorities(PyQt5.QtWidgets.QWidget):
    
    sig_close = PyQt5.QtCore.pyqtSignal()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_gui()
    
    def get_index(self):
        return self.lbx_lft.selectionModel().currentIndex()
    
    def get_row(self):
        index_ = self.get_index()
        return(index_.row(), index_.column())
    
    def fill1(self,dic,header):
        model = Model(dic,header)
        self.lbx_lft.setModel(model)
    
    def fill2(self, dic, header):
        model = Model(dic, header)
        self.lbx_rht.setModel(model)
    
    def set_icon(self):
        # Does not accent None
        self.setWindowIcon(sh.gi.objs.get_icon())
    
    def closeEvent(self, event):
        self.sig_close.emit()
        return super().closeEvent(event)
    
    def set_title(self, title):
        self.setWindowTitle(title)
    
    def centralize(self):
        self.move(sh.objs.get_root().desktop().screen().rect().center() - self.rect().center())
    
    def bind(self, hotkey, action):
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence(hotkey), self).activated.connect(action)
    
    def set_buttons(self):
        self.btn_lft = sh.Button (hint = _('Prioritize selection on the right')
                                 ,inactive = icn_lft
                                 ,active = icn_lft
                                 )
        self.btn_rht = sh.Button (hint = _('Unprioritize selection on the left')
                                 ,inactive = icn_rht
                                 ,active = icn_rht
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
        self.btn_res = sh.Button (text = _('Reset')
                                 ,hint = _('Reload subjects')
                                 )
        self.btn_apl = sh.Button (text = _('Apply')
                                 ,hint = _('Save and close')
                                 )
    
    def set_layouts(self):
        self.lay_prm = PyQt5.QtWidgets.QVBoxLayout()
        self.lay_sec = PyQt5.QtWidgets.QGridLayout()
        self.lay_ter = PyQt5.QtWidgets.QGridLayout()
        self.lay_btn = PyQt5.QtWidgets.QVBoxLayout()
        self.lay_rht = PyQt5.QtWidgets.QHBoxLayout()
    
    def set_widgets(self):
        self.lbx_lft = PyQt5.QtWidgets.QTreeView()
        self.lbx_rht = PyQt5.QtWidgets.QTreeView()
        self.prm_sec = PyQt5.QtWidgets.QWidget()
        self.prm_ter = PyQt5.QtWidgets.QWidget()
        self.prm_btn = PyQt5.QtWidgets.QWidget()
        self.prm_rht = PyQt5.QtWidgets.QWidget()
        self.cbx_pri = sh.CheckBox(_('Prioritize subjects'))
        sources = (_('All subjects'), _('Main'), _('From the article'))
        self.opt_src = sh.OptionMenu(sources)
    
    def add_widgets(self):
        self.lay_prm.addWidget(self.prm_sec)
        self.lay_prm.addWidget(self.prm_ter)
        self.lay_sec.addWidget(self.lbx_lft, 0, 0)
        self.lay_sec.addWidget(self.prm_btn, 0, 1)
        self.lay_sec.addWidget(self.lbx_rht, 0, 2)
        self.lay_ter.addWidget(self.btn_res.widget, 0, 1, PyQt5.QtCore.Qt.AlignLeft)
        self.lay_ter.addWidget(self.cbx_pri.widget, 0, 2, PyQt5.QtCore.Qt.AlignCenter)
        self.lay_ter.addWidget(self.prm_rht, 0, 3, PyQt5.QtCore.Qt.AlignRight)
        self.lay_rht.addWidget(self.opt_src.widget)
        self.lay_rht.addWidget(self.btn_apl.widget)
        self.prm_sec.setLayout(self.lay_sec)
        self.prm_btn.setLayout(self.lay_btn)
        self.prm_ter.setLayout(self.lay_ter)
        self.prm_rht.setLayout(self.lay_rht)
        self.setLayout(self.lay_prm)
    
    def add_buttons(self):
        #NOTE: If run directly, this module will not find icons owing to paths
        self.lay_btn.addWidget(self.btn_lft.widget)
        self.lay_btn.addWidget(self.btn_rht.widget)
        self.lay_btn.addWidget(self.btn_up1.widget)
        self.lay_btn.addWidget(self.btn_dwn.widget)
        self.lay_btn.addWidget(self.btn_top.widget)
        self.lay_btn.addWidget(self.btn_btm.widget)
    
    def set_gui(self):
        self.set_title(_('Subject prioritization'))
        self.set_icon()
        self.set_layouts()
        self.set_widgets()
        self.set_buttons()
        self.add_widgets()
        self.add_buttons()
        self.customize()
    
    def customize(self):
        #self.lay_prm.setContentsMargins(0, 0, 0, 0)
        self.lay_sec.setContentsMargins(0, 0, 0, 0)
        self.lay_btn.setContentsMargins(4, 4, 4, 4)
        self.lay_ter.setContentsMargins(2, 4, 2, 0)
        self.lay_rht.setContentsMargins(0, 0, 0, 0)


if __name__ == '__main__':
    f = '[MClient] subjects.priorities.gui.__main__'
    sh.com.start()
    iprior = Priorities()
    iprior.show()
    iprior.resize(800, 450)
    iprior.centralize()
    sh.com.end()
