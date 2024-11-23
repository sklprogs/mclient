#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtWidgets import QVBoxLayout, QWidget, QTableView
from PyQt6.QtCore import QVariant, Qt, pyqtSignal, QAbstractTableModel
from PyQt6.QtGui import QShortcut, QKeySequence

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message
from skl_shared_qt.graphics.root.controller import ROOT


class TableModel(QAbstractTableModel):
    
    def __init__(self, datain, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain
    
    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

    def data(self, index, role):
        f = '[MClient] symbols.gui.TableModel.data'
        if not index.isValid():
            return QVariant()
        if role == Qt.ItemDataRole.DisplayRole:
            try:
                return QVariant(self.arraydata[index.row()][index.column()])
            except Exception:
                mes = _('List out of bounds at row #{}, column #{}!')
                mes = mes.format(index.row(), index.column())
                Message(f, mes).show_warning()
                return QVariant()



class Table(QTableView):
    
    sig_rmb = pyqtSignal()
    sig_space = pyqtSignal()
    sig_select = pyqtSignal(int, int)
    
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
        if button == Qt.MouseButton.RightButton:
            self.sig_rmb.emit()
        super().mousePressEvent(event)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            self.sig_space.emit()
        return super().keyPressEvent(event)



class Symbols(QWidget):
    
    sig_return = pyqtSignal()
    sig_ctrl_return = pyqtSignal()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_gui()
    
    def set_gui(self):
        self.layout_ = QVBoxLayout()
        self.layout_.setContentsMargins(5, 5, 5, 5)
        self.table = Table()
        self.layout_.addWidget(self.table)
        self.setLayout(self.layout_)
    
    def keyPressEvent(self, event):
        key = event.key()
        modifiers = event.modifiers()
        if key in (Qt.Key_Return, Qt.Key.Key_Enter):
            if modifiers & Qt.KeyboardModifier.ControlModifier:
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
        self.move(ROOT.get_root().primaryScreen().geometry().center() - self.rect().center())
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            QShortcut(QKeySequence(hotkey), self).activated.connect(action)
