#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtWidgets import QWidget, QTreeView, QVBoxLayout
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtCore import QAbstractTableModel, QVariant, Qt, pyqtSignal
from PyQt6.QtCore import QItemSelectionModel

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message
from skl_shared_qt.graphics.root.controller import ROOT
from skl_shared_qt.graphics.file_dialog.controller import FILE_DIALOG


class TableModel(QAbstractTableModel):
    
    def __init__(self, data=[], parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        if not data:
            data = [_('Save the current view as a web-page (*.htm)')
                   ,_('Save the original article as a web-page (*.htm)')
                   ,_('Save the article as plain text in UTF-8 (*.txt)')
                   ,_('Copy the code of the article to clipboard')
                   ,_('Copy the text of the article to clipboard')]
        self.items = data
    
    def rowCount(self, parent):
        return len(self.items)

    def columnCount(self, parent):
        return 1

    def data(self, index, role):
        f = '[MClient] save.gui.TableModel.data'
        if not index.isValid():
            return QVariant()
        if role == Qt.ItemDataRole.DisplayRole:
            try:
                return QVariant(self.items[index.row()])
            except Exception:
                mes = _('List out of bounds at row #{}, column #{}!')
                mes = mes.format(index.row(), index.column())
                Message(f, mes).show_warning()
                return QVariant()
    
    def update(self):
        self.layoutChanged.emit()



class Save(QWidget):
    
    sig_close = pyqtSignal()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_gui()
    
    def set_model(self, model):
        self.save.setModel(model)
    
    def set_index(self, index_):
        self.save.setCurrentIndex(index_)
    
    def get_row(self):
        return self.save.selectionModel().currentIndex().row()
    
    def clear_selection(self):
        self.save.selectionModel().clearSelection()
    
    def select_row(self, index_):
        mode = QItemSelectionModel.SelectionFlag.Select | QItemSelectionModel.SelectionFlag.Rows
        self.save.selectionModel().select(index_, mode)
    
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
    
    def get_font_size(self):
        size = self.font().pointSize()
        # We will get -1 if the font size was specified in pixels
        if size > 0:
            return size
    
    def set_font_size(self, size):
        qfont = self.font()
        qfont.setPointSize(size)
        self.setFont(qfont)
    
    def set_gui(self):
        self.save = QTreeView()
        self.save.header().hide()
        self.save.setIndentation(5)
        self.layout_ = QVBoxLayout()
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.addWidget(self.save)
        self.setLayout(self.layout_)
        self.ask = FILE_DIALOG
        self.resize(550, 115)
