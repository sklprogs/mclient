#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt5
import PyQt5.QtWidgets

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class TableModel(PyQt5.QtCore.QAbstractTableModel):
    
    def __init__(self,datain,parent=None,*args):
        PyQt5.QtCore.QAbstractTableModel.__init__(self,parent,*args)
        self.arraydata = datain
    
    def rowCount(self,parent):
        return len(self.arraydata)

    def columnCount(self,parent):
        return len(self.arraydata[0])

    def data(self,index,role):
        f = '[MClientQt] symbols.gui.TableModel.data'
        if not index.isValid():
            return PyQt5.QtCore.QVariant()
        if role == PyQt5.QtCore.Qt.DisplayRole:
            try:
                return PyQt5.QtCore.QVariant(self.arraydata[index.row()][index.column()])
            except Exception as e:
                mes = _('List out of bounds at row #{}, column #{}!')
                mes = mes.format(index.row(),index.column())
                sh.objs.get_mes(f,mes,True).show_warning()
                return PyQt5.QtCore.QVariant()



class Table(PyQt5.QtWidgets.QTableView):
    
    right_mouse = PyQt5.QtCore.pyqtSignal()
    space = PyQt5.QtCore.pyqtSignal()
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    
    def mousePressEvent(self,event):
        button = event.button()
        if button == PyQt5.QtCore.Qt.RightButton:
            self.right_mouse.emit()
        super().mousePressEvent(event)
    
    def keyPressEvent(self,event):
        if event.key() == PyQt5.QtCore.Qt.Key_Space:
            self.space.emit()
        return super().keyPressEvent(event)



class Symbols(PyQt5.QtWidgets.QWidget):
    
    return_ = PyQt5.QtCore.pyqtSignal()
    ctrl_return = PyQt5.QtCore.pyqtSignal()
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_gui()
    
    def set_gui(self):
        self.layout_ = PyQt5.QtWidgets.QVBoxLayout()
        self.layout_.setContentsMargins(5,5,5,5)
        self.table = Table()
        self.layout_.addWidget(self.table)
        self.setLayout(self.layout_)
    
    def keyPressEvent(self,event):
        key = event.key()
        modifiers = event.modifiers()
        if key in (PyQt5.QtCore.Qt.Key_Return,PyQt5.QtCore.Qt.Key_Enter):
            if modifiers & PyQt5.QtCore.Qt.ControlModifier:
                self.ctrl_return.emit()
            else:
                self.return_.emit()
        return super().keyPressEvent(event)
    
    def resize_to_contents(self):
        self.table.resizeColumnsToContents()
    
    def set_size(self):
        self.resize(300,400)
    
    def set_model(self,model):
        self.table.setModel(model)
    
    def set_title(self,title):
        self.setWindowTitle(title)
    
    def centralize(self):
        self.move(sh.objs.get_root().desktop().screen().rect().center() - self.rect().center())
    
    def bind(self,hotkey,action):
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence(hotkey),self).activated.connect(action)
