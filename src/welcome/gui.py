#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt5.QtWidgets

#from skl_shared_qt.localize import _
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
        if not index.isValid():
            return PyQt5.QtCore.QVariant()
        if role == PyQt5.QtCore.Qt.DisplayRole:
            try:
                return PyQt5.QtCore.QVariant(self.arraydata[index.row()][index.column()])
            except Exception:
                # We will have this exception regularly for merged cells
                return PyQt5.QtCore.QVariant()



class TableDelegate(PyQt5.QtWidgets.QStyledItemDelegate):
    ''' akej74, https://stackoverflow.com/questions/35397943/how-to-make-a-fast-qtableview-with-html-formatted-and-clickable-cells
        #NOTE: Do not set a default font here since Welcome has rows with
        different fonts and wrong sizeHint will be returned causing rows not to
        be fully visible.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def paint(self, painter, option, index):
        # index:   PyQt5.QtCore.QModelIndex
        # painter: PyQt5.QtGui.QPainter
        # option:  PyQt5.QtWidgets.QStyleOptionViewItem
        options = PyQt5.QtWidgets.QStyleOptionViewItem(option)
        self.initStyleOption(options, index)
        
        if options.widget:
            style = options.widget.style()
        else:
            style = PyQt5.QtWidgets.QApplication.style()
        
        doc = PyQt5.QtGui.QTextDocument()
        doc.setHtml(options.text)
        options.text = ''
        
        # This enables text wrapping in the delegate
        doc.setTextWidth(options.rect.width())
        
        style.drawControl(PyQt5.QtWidgets.QStyle.CE_ItemViewItem, options, painter)
        ctx = PyQt5.QtGui.QAbstractTextDocumentLayout.PaintContext()
        
        textRect = style.subElementRect(PyQt5.QtWidgets.QStyle.SE_ItemViewItemText, options)
        
        painter.save()
    
        painter.translate(textRect.topLeft())
        # Hide too long text; do not allow cells to overlap
        painter.setClipRect(textRect.translated(-textRect.topLeft()))
        doc.documentLayout().draw(painter, ctx)
    
        painter.restore()
    
#    def sizeHint(self, option, index):
#        options = PyQt5.QtWidgets.QStyleOptionViewItem(option)
#        self.initStyleOption(options, index)
#        
#        doc = PyQt5.QtGui.QTextDocument()
#        doc.setHtml(options.text)
#        doc.setTextWidth(options.rect.width())
#        
#        return PyQt5.QtCore.QSize(doc.idealWidth(), doc.size().height())



class App(PyQt5.QtWidgets.QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_gui()
    
    def set_icon(self):
        # Does not accent None
        self.setWindowIcon(sh.gi.objs.get_icon())
    
    def show_rows(self, rownos):
        for rowno in rownos:
            self.welcome.show_row(rowno)
    
    def hide_rows(self, rownos):
        for rowno in rownos:
            self.welcome.hide_row(rowno)
    
    def resize_rows(self):
        self.welcome.resize_rows()
    
    def set_col_width(self, no, width):
        self.welcome.set_col_width(no, width)
    
    def set_span(self, rowno, colno, rowspan, colspan):
        self.welcome.set_span(rowno, colno, rowspan, colspan)
    
    def set_model(self, model):
        self.welcome.set_model(model)
    
    def show(self):
        self.showMaximized()
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence(hotkey), self).activated.connect(action)
    
    def centralize(self):
        self.move(sh.objs.get_root().desktop().screen().rect().center() - self.rect().center())
    
    def set_gui(self):
        self.parent_ = PyQt5.QtWidgets.QWidget()
        self.layout_ = PyQt5.QtWidgets.QVBoxLayout()
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.welcome = Welcome()
        self.layout_.addWidget(self.welcome)
        self.parent_.setLayout(self.layout_)
        self.setCentralWidget(self.parent_)



class Welcome(PyQt5.QtWidgets.QTableView):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_gui()
    
    def show_row(self, rowno):
        self.setRowHidden(rowno, False)
    
    def hide_row(self, rowno):
        self.setRowHidden(rowno, True)
    
    def set_span(self, rowno, colno, rowspan, colspan):
        self.setSpan(rowno, colno, rowspan, colspan)
    
    def set_gui(self):
        self.setItemDelegate(TableDelegate())
        hheader = self.horizontalHeader()
        vheader = self.verticalHeader()
        hheader.setVisible(False)
        vheader.setVisible(False)
        self.show_borders(False)
        # Disable selecting cells
        self.setFocusPolicy(PyQt5.QtCore.Qt.NoFocus)
        self.setSelectionMode(PyQt5.QtWidgets.QAbstractItemView.NoSelection)
    
    def resize_rows(self):
        self.resizeRowsToContents()
    
    def set_col_width(self, no, width):
        self.setColumnWidth(no, width)
    
    def set_model(self, model):
        self.setModel(model)
    
    def show_borders(self, Show=False):
        self.setShowGrid(Show)
