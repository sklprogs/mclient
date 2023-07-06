#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt5
import PyQt5.QtWidgets


class TableModel(PyQt5.QtCore.QAbstractTableModel):
	def __init__(self, items, parent=None, *args):
		PyQt5.QtCore.QAbstractTableModel.__init__(self, parent, *args)
		self.items = items

	def rowCount(self, parent):
		return len(self.items)

	def columnCount(self, parent):
		return 1

	def data(self, index, role):
		if not index.isValid():
			return PyQt5.QtWidgets.QVariant()
		elif role != PyQt5.QtCore.Qt.DisplayRole:
			return PyQt5.QtCore.QVariant()
		try:
			return PyQt5.QtCore.QVariant(self.items[index.row()])
		except:
			return PyQt5.QtCore.QVariant()



class View(PyQt5.QtWidgets.QListView):
    
    sig_click = PyQt5.QtCore.pyqtSignal()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def mousePressEvent(self, event):
        if event.button() == PyQt5.QtCore.Qt.LeftButton:
            self.sig_click.emit()
        super().mousePressEvent(event)



class Suggest(PyQt5.QtWidgets.QWidget):
    
    sig_load = PyQt5.QtCore.pyqtSignal(str)
    
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
        self.layout_ = PyQt5.QtWidgets.QVBoxLayout()
        self.view = View()
        self.view.sig_click.connect(self.load)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.addWidget(self.view)
        self.setLayout(self.layout_)
        self.setWindowFlags(self.windowFlags() | PyQt5.QtCore.Qt.FramelessWindowHint)
    
    def fill(self, lst):
        self.model = TableModel(lst)
        self.view.setModel(self.model)
    
    def bind(self, hotkey, action):
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence(hotkey), self).activated.connect(action)
    
    def set_index(self, index_):
        self.view.setCurrentIndex(index_)
    
    def get_row(self):
        return self.get_index().row()
    
    def clear_selection(self):
        self.view.selectionModel().clearSelection()
    
    def select_row(self, index_):
        mode = PyQt5.QtCore.QItemSelectionModel.Select | PyQt5.QtCore.QItemSelectionModel.Rows
        self.view.selectionModel().select(index_, mode)
    
    def set_width(self, width):
        self.setFixedWidth(width)
