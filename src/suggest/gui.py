#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtWidgets import QWidget, QVariant, QListView, QVBoxLayout
from PyQt6.QtCore import QAbstractTableModel, Qt, QVariant, pyqtSignal
from PyQt6.QtCore import QItemSelectionModel
from PyQt6.QtGui import QShortcut, QKeySequence


class TableModel(QAbstractTableModel):
	def __init__(self, items, parent=None, *args):
		QAbstractTableModel.__init__(self, parent, *args)
		self.items = items

	def rowCount(self, parent):
		return len(self.items)

	def columnCount(self, parent):
		return 1

	def data(self, index, role):
		if not index.isValid():
			return QVariant()
		elif role != Qt.ItemDataRole.DisplayRole:
			return QVariant()
		try:
			return QVariant(self.items[index.row()])
		except:
			return QVariant()



class View(QListView):
    
    sig_click = pyqtSignal()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def mouseReleaseEvent(self, event):
        ''' Using 'mouseReleaseEvent' instead of 'mousePressEvent' allows us to
            automatically select the required row before performing an action.
        '''
        if event.button() == Qt.MouseButton.LeftButton:
            self.sig_click.emit()
        super().mouseReleaseEvent(event)



class Suggest(QWidget):
    
    sig_load = pyqtSignal(str)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_gui()
    
    def load(self):
        self.sig_load.emit(self.get())
    
    def get(self):
        return self.model.items[self.get_row()]
    
    def get_index(self):
        return self.view.selectionModel().currentIndex()
    
    def set_geometry(self, x, y, width, height):
        self.setGeometry(x, y, width, height)
    
    def get_height(self):
        return self.height()
    
    def set_gui(self):
        self.layout_ = QVBoxLayout()
        self.view = View()
        self.view.sig_click.connect(self.load)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.addWidget(self.view)
        self.setLayout(self.layout_)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
    
    def fill(self, lst):
        self.model = TableModel(lst)
        self.view.setModel(self.model)
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            QShortcut(QKeySequence(hotkey), self).activated.connect(action)
    
    def set_index(self, index_):
        self.view.setCurrentIndex(index_)
    
    def get_row(self):
        return self.get_index().row()
    
    def clear_selection(self):
        self.view.selectionModel().clearSelection()
    
    def select_row(self, index_):
        mode = QItemSelectionModel.SelectionFlag.Select | QItemSelectionModel.SelectionFlag.Rows
        self.view.selectionModel().select(index_, mode)
    
    def set_width(self, width):
        self.setFixedWidth(width)
