#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt5.QtWidgets
import PyQt5.QtGui

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class TableModel(PyQt5.QtCore.QAbstractTableModel):
    
    def __init__(self, data, parent=None, *args):
        PyQt5.QtCore.QAbstractTableModel.__init__(self,parent,*args)
        self.items = data
        self.headers = [_('#'), _('Source'), _('Source language')
                       ,_('Target language'), _('Request')
                       ]
    
    def get_header(self,colno):
        f = '[MClientQt] history.gui.TableModel.get_header'
        try:
            return self.headers[colno]
        except IndexError:
            mes = _('Wrong input data: "{}"!').format(colno)
            sh.objs.get_mes(f,mes,True).show_warning()
            return _('Header')
    
    def rowCount(self, parent):
        return len(self.items)

    def columnCount(self, parent):
        return len(self.items[0])

    def data(self, index, role):
        f = '[MClientQt] history.gui.TableModel.data'
        if not index.isValid():
            return PyQt5.QtCore.QVariant()
        if role == PyQt5.QtCore.Qt.DisplayRole:
            try:
                return PyQt5.QtCore.QVariant(self.items[index.row()][index.column()])
            except Exception:
                mes = _('List out of bounds at row #{}, column #{}!')
                mes = mes.format(index.row(),index.column())
                sh.objs.get_mes(f,mes,True).show_warning()
                return PyQt5.QtCore.QVariant()
    
    def update(self):
        self.layoutChanged.emit()
    
    def headerData(self, column, orientation, role=PyQt5.QtCore.Qt.DisplayRole):
        if column == 0 and role == PyQt5.QtCore.Qt.TextAlignmentRole:
            return PyQt5.QtCore.Qt.AlignCenter
        if role != PyQt5.QtCore.Qt.DisplayRole:
            return PyQt5.QtCore.QVariant()
        if orientation == PyQt5.QtCore.Qt.Horizontal:
            return PyQt5.QtCore.QVariant(self.get_header(column))



class History(PyQt5.QtWidgets.QWidget):
    
    sig_close = PyQt5.QtCore.pyqtSignal()
    sig_go = PyQt5.QtCore.pyqtSignal(int)
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_gui()
    
    def set_index(self,index_):
        self.history.setCurrentIndex(index_)
    
    def get_row(self):
        return self.history.selectionModel().currentIndex().row()
    
    def clear_selection(self):
        self.history.selectionModel().clearSelection()
    
    def select_row(self, index_):
        mode = PyQt5.QtCore.QItemSelectionModel.Select | PyQt5.QtCore.QItemSelectionModel.Rows
        self.history.selectionModel().select(index_, mode)
    
    def get_model(self):
        return self.history.model()
    
    def set_model(self,model):
        self.history.setModel(model)
    
    def reset(self):
        self.history.clear()
    
    def closeEvent(self, event):
        self.sig_close.emit()
        return super().closeEvent(event)
    
    def set_title(self, title):
        self.setWindowTitle(title)
    
    def centralize(self):
        self.move(sh.objs.get_root().desktop().screen().rect().center() - self.rect().center())
    
    def bind(self,hotkey,action):
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence(hotkey), self).activated.connect(action)
    
    def set_icon(self):
        # Does not accent None
        self.setWindowIcon(sh.gi.objs.get_icon())
    
    def set_col_width(self):
        ''' 42 is the minimal column width to store 2-digit numbers. 3-digit
            numbers require more space; however,
            1) too wide ID column with a lot of empty space looks ugly;
            2) IDs > 99 are not always reached;
            3) the user can manually increase/decrease the column width.
        '''
        self.history.header().resizeSection(0, 42)
    
    def set_gui(self):
        self.layout_ = PyQt5.QtWidgets.QVBoxLayout(self)
        self.history = PyQt5.QtWidgets.QTreeView()
        self.layout_.addWidget(self.history)
        self.setLayout(self.layout_)
        self.set_icon()
        self.resize(600,300)


if __name__ == '__main__':
    sh.com.start()
    headers = [_('#'), _('Source language'), _('Target language')
              ,_('Request')
              ]
    table = [['1',_('Russian'), _('English'), 'start']
            ,['2',_('Russian'), _('English'), 'hello']
            ,['3',_('English'), _('Russian'), 'bye']
            ]
    model = TableModel(table)
    model.headers = headers
    ihis = History()
    ihis.set_model(model)
    ihis.show()
    row = ['0', _('Arabic'), _('French'), _('test')]
    table.insert(0,row)
    model.update()
    sh.com.end()
