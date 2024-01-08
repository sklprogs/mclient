#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt6
import PyQt6.QtWidgets

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class TableModel(PyQt6.QtCore.QAbstractTableModel):
    
    def __init__(self, datain, parent=None, *args):
        PyQt6.QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain
    
    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

    def data(self, index, role):
        f = '[MClient] symbols.gui.TableModel.data'
        if not index.isValid():
            return PyQt6.QtCore.QVariant()
        if role == PyQt6.QtCore.Qt.ItemDataRole.DisplayRole:
            try:
                return PyQt6.QtCore.QVariant(self.arraydata[index.row()][index.column()])
            except Exception:
                mes = _('List out of bounds at row #{}, column #{}!')
                mes = mes.format(index.row(), index.column())
                sh.objs.get_mes(f, mes, True).show_warning()
                return PyQt6.QtCore.QVariant()



class Table(PyQt6.QtWidgets.QTableView):
    
    sig_rmb = PyQt6.QtCore.pyqtSignal()
    sig_space = PyQt6.QtCore.pyqtSignal()
    sig_select = PyQt6.QtCore.pyqtSignal(int, int)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMouseTracking(True)
    
    def set_cur_index(self, index_):
        self.setCurrentIndex(index_)
    
    def _use_mouse(self, event):
        pos = event.position().toPoint()
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
        if button == PyQt6.QtCore.Qt.MouseButton.RightButton:
            self.sig_rmb.emit()
        super().mousePressEvent(event)
    
    def keyPressEvent(self, event):
        if event.key() == PyQt6.QtCore.Qt.Key.Key_Space:
            self.sig_space.emit()
        return super().keyPressEvent(event)



class Symbols(PyQt6.QtWidgets.QWidget):
    
    sig_return = PyQt6.QtCore.pyqtSignal()
    sig_ctrl_return = PyQt6.QtCore.pyqtSignal()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_gui()
    
    def set_gui(self):
        self.layout_ = PyQt6.QtWidgets.QVBoxLayout()
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
        if key in (PyQt6.QtCore.Qt.Key_Return, PyQt6.QtCore.Qt.Key.Key_Enter):
            if modifiers & PyQt6.QtCore.Qt.KeyboardModifier.ControlModifier:
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
        self.move(sh.objs.get_root().primaryScreen().geometry().center() - self.rect().center())
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            PyQt6.QtGui.QShortcut(PyQt6.QtGui.QKeySequence(hotkey), self).activated.connect(action)
