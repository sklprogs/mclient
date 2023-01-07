#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt5.QtWidgets
import PyQt5.QtGui

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class TableModel(PyQt5.QtCore.QAbstractTableModel):
    
    def __init__(self,data=[],parent=None,*args):
        PyQt5.QtCore.QAbstractTableModel.__init__(self,parent,*args)
        if not data:
            data = [_('Save the current view as a web-page (*.htm)')
                   ,_('Save the original article as a web-page (*.htm)')
                   ,_('Save the article as plain text in UTF-8 (*.txt)')
                   ,_('Copy the code of the article to clipboard')
                   ,_('Copy the text of the article to clipboard')
                   ]
        self.items = data
    
    def rowCount(self,parent):
        return len(self.items)

    def columnCount(self,parent):
        return 1

    def data(self,index,role):
        f = '[MClientQt] save.gui.TableModel.data'
        if not index.isValid():
            return PyQt5.QtCore.QVariant()
        if role == PyQt5.QtCore.Qt.DisplayRole:
            try:
                return PyQt5.QtCore.QVariant(self.items[index.row()])
            except Exception as e:
                mes = _('List out of bounds at row #{}, column #{}!')
                mes = mes.format(index.row(),index.column())
                sh.objs.get_mes(f,mes,True).show_warning()
                return PyQt5.QtCore.QVariant()
    
    def update(self):
        self.layoutChanged.emit()



class Save(PyQt5.QtWidgets.QWidget):
    
    sig_close = PyQt5.QtCore.pyqtSignal()
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_gui()
    
    def set_model(self,model):
        self.save.setModel(model)
    
    def set_index(self,index_):
        self.save.setCurrentIndex(index_)
    
    def get_row(self):
        return self.save.selectionModel().currentIndex().row()
    
    def clear_selection(self):
        self.save.selectionModel().clearSelection()
    
    def select_row(self,index_):
        mode = PyQt5.QtCore.QItemSelectionModel.Select | PyQt5.QtCore.QItemSelectionModel.Rows
        self.save.selectionModel().select(index_,mode)
    
    def set_icon(self,qicon):
        # Does not accent None
        self.setWindowIcon(qicon)
    
    def closeEvent(self,event):
        self.sig_close.emit()
        return super().closeEvent(event)
    
    def set_title(self,title):
        self.setWindowTitle(title)
    
    def centralize(self):
        self.move(sh.objs.get_root().desktop().screen().rect().center() - self.rect().center())
    
    def bind(self,hotkey,action):
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence(hotkey),self).activated.connect(action)
    
    def set_gui(self):
        self.save = PyQt5.QtWidgets.QTreeView()
        self.layout_ = PyQt5.QtWidgets.QVBoxLayout()
        self.layout_.addWidget(self.save)
        self.setLayout(self.layout_)


if __name__ == '__main__':
    sh.com.start()
    model = TableModel()
    isave = Save()
    isave.set_model(model)
    isave.show()
    sh.com.end()