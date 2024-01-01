#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt5
import PyQt5.QtWidgets

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class TableModel(PyQt5.QtCore.QAbstractTableModel):
    
    def __init__(self, datain, parent=None, *args):
        PyQt5.QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain
    
    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

    def data(self, index, role):
        f = '[MClient] symbols.gui.TableModel.data'
        if not index.isValid():
            return PyQt5.QtCore.QVariant()
        if role == PyQt5.QtCore.Qt.DisplayRole:
            try:
                return PyQt5.QtCore.QVariant(self.arraydata[index.row()][index.column()])
            except Exception:
                mes = _('List out of bounds at row #{}, column #{}!')
                mes = mes.format(index.row(), index.column())
                sh.objs.get_mes(f, mes, True).show_warning()
                return PyQt5.QtCore.QVariant()



class Table(PyQt5.QtWidgets.QTableView):
    
    sig_rmb = PyQt5.QtCore.pyqtSignal()
    sig_space = PyQt5.QtCore.pyqtSignal()
    sig_select = PyQt5.QtCore.pyqtSignal(int, int)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMouseTracking(True)
    
    def set_cur_index(self, index_):
        self.setCurrentIndex(index_)
    
    def _use_mouse(self, event):
        pos = event.pos()
        rowno = self.rowAt(pos.y())
        colno = self.columnAt(pos.x())
        self.sig_select.emit(rowno, colno)
    
    def mouseMoveEvent(self, event):
        ''' In order to properly process a symbol, its cell should be selected
            ('setCurrentIndex' should be used). Without that, copying a symbol
            with right click will not work as expected.
        '''
        self._use_mouse(event)
        return super().mouseMoveEvent(event)
    
    def get_cur_cell(self):
        index_ = self.currentIndex()
        return(index_.row(), index_.column())
    
    def mousePressEvent(self, event):
        button = event.button()
        if button == PyQt5.QtCore.Qt.RightButton:
            self.sig_rmb.emit()
        super().mousePressEvent(event)
    
    def keyPressEvent(self, event):
        if event.key() == PyQt5.QtCore.Qt.Key_Space:
            self.sig_space.emit()
        return super().keyPressEvent(event)



class Symbols(PyQt5.QtWidgets.QWidget):
    
    sig_return = PyQt5.QtCore.pyqtSignal()
    sig_ctrl_return = PyQt5.QtCore.pyqtSignal()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_gui()
    
    def set_gui(self):
        self.layout_ = PyQt5.QtWidgets.QVBoxLayout()
        self.layout_.setContentsMargins(5, 5, 5, 5)
        self.table = Table()
        self.layout_.addWidget(self.table)
        self.setLayout(self.layout_)
        self.set_icon()
    
    def set_icon(self):
        # Does not accent None
        self.setWindowIcon(sh.gi.objs.get_icon())
    
    def keyPressEvent(self, event):
        key = event.key()
        modifiers = event.modifiers()
        if key in (PyQt5.QtCore.Qt.Key_Return, PyQt5.QtCore.Qt.Key_Enter):
            if modifiers & PyQt5.QtCore.Qt.ControlModifier:
                self.sig_ctrl_return.emit()
            else:
                self.sig_return.emit()
        return super().keyPressEvent(event)
    
    def resize_to_contents(self):
        self.table.resizeColumnsToContents()
    
    def set_size(self):
        self.resize(300, 400)
    
    def set_model(self, model):
        self.table.setModel(model)
    
    def set_title(self, title):
        self.setWindowTitle(title)
    
    def centralize(self):
        self.move(sh.objs.get_root().desktop().screen().rect().center() - self.rect().center())
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence(hotkey), self).activated.connect(action)
