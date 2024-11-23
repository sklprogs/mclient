#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTreeView
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtCore import QAbstractTableModel, QVariant, Qt, pyqtSignal
from PyQt6.QtCore import QItemSelectionModel

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message, rep
from skl_shared_qt.graphics.root.controller import ROOT


class TableModel(QAbstractTableModel):
    
    def __init__(self, data, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.items = data
        self.headers = [_('#'), _('Source'), _('Source language')
                       ,_('Target language'), _('Request')]
    
    def get_header(self, colno):
        f = '[MClient] history.gui.TableModel.get_header'
        try:
            return self.headers[colno]
        except IndexError:
            rep.wrong_input(f, colno)
            return _('Header')
    
    def rowCount(self, parent):
        return len(self.items)

    def columnCount(self, parent):
        return len(self.items[0])

    def data(self, index, role):
        f = '[MClient] history.gui.TableModel.data'
        if not index.isValid():
            return QVariant()
        if role == Qt.ItemDataRole.DisplayRole:
            try:
                return QVariant(self.items[index.row()][index.column()])
            except Exception:
                mes = _('List out of bounds at row #{}, column #{}!')
                mes = mes.format(index.row(), index.column())
                Message(f, mes).show_warning()
                return QVariant()
    
    def update(self):
        self.layoutChanged.emit()
    
    def headerData(self, column, orientation, role=Qt.ItemDataRole.DisplayRole):
        if column == 0 and role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter
        if role != Qt.ItemDataRole.DisplayRole:
            return QVariant()
        if orientation == Qt.Orientation.Horizontal:
            return QVariant(self.get_header(column))



class History(QWidget):
    
    sig_close = pyqtSignal()
    sig_go = pyqtSignal(int)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_gui()
    
    def set_index(self, index_):
        self.history.setCurrentIndex(index_)
    
    def get_row(self):
        return self.history.selectionModel().currentIndex().row()
    
    def clear_selection(self):
        self.history.selectionModel().clearSelection()
    
    def select_row(self, index_):
        mode = QItemSelectionModel.SelectionFlag.Select | QItemSelectionModel.SelectionFlag.Rows
        self.history.selectionModel().select(index_, mode)
    
    def get_model(self):
        return self.history.model()
    
    def set_model(self, model):
        self.history.setModel(model)
    
    def reset(self):
        self.history.clear()
    
    def closeEvent(self, event):
        self.sig_close.emit()
        return super().closeEvent(event)
    
    def set_title(self, title):
        self.setWindowTitle(title)
    
    def centralize(self):
        self.move(ROOT.get_root().primaryScreen().geometry().center() - self.rect().center())
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            QShortcut(QKeySequence(hotkey), self).activated.connect(action)
    
    def set_col_width(self):
        ''' 42 is the minimal column width to store 2-digit numbers. 3-digit
            numbers require more space; however,
            1) too wide ID column with a lot of empty space looks ugly;
            2) IDs > 99 are not always reached;
            3) the user can manually increase/decrease the column width.
        '''
        self.history.header().resizeSection(0, 42)
    
    def set_gui(self):
        self.layout_ = QVBoxLayout(self)
        self.history = QTreeView()
        self.layout_.addWidget(self.history)
        self.setLayout(self.layout_)
        self.resize(600, 300)


if __name__ == '__main__':
    headers = [_('#'), _('Source language'), _('Target language')
              ,_('Request')]
    table = [['1', _('Russian'), _('English'), 'start']
            ,['2', _('Russian'), _('English'), 'hello']
            ,['3', _('English'), _('Russian'), 'bye']]
    model = TableModel(table)
    model.headers = headers
    ihis = History()
    ihis.set_model(model)
    ihis.show()
    row = ['0', _('Arabic'), _('French'), _('test')]
    table.insert(0, row)
    model.update()
    ROOT.end()
