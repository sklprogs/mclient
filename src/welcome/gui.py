#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt6.QtWidgets

#from skl_shared_qt.localize import _
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
        if not index.isValid():
            return PyQt6.QtCore.QVariant()
        if role == PyQt6.QtCore.Qt.ItemDataRole.DisplayRole:
            try:
                return PyQt6.QtCore.QVariant(self.arraydata[index.row()][index.column()])
            except Exception:
                # We will have this exception regularly for merged cells
                return PyQt6.QtCore.QVariant()



class TableDelegate(PyQt6.QtWidgets.QStyledItemDelegate):
    ''' akej74, https://stackoverflow.com/questions/35397943/how-to-make-a-fast-qtableview-with-html-formatted-and-clickable-cells
        #NOTE: Do not set a default font here since Welcome has rows with
        different fonts and wrong sizeHint will be returned causing rows not to
        be fully visible.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def paint(self, painter, option, index):
        # index:   PyQt6.QtCore.QModelIndex
        # painter: PyQt6.QtGui.QPainter
        # option:  PyQt6.QtWidgets.QStyleOptionViewItem
        options = PyQt6.QtWidgets.QStyleOptionViewItem(option)
        self.initStyleOption(options, index)
        
        if options.widget:
            style = options.widget.style()
        else:
            style = PyQt6.QtWidgets.QApplication.style()
        
        doc = PyQt6.QtGui.QTextDocument()
        doc.setHtml(options.text)
        options.text = ''
        
        # This enables text wrapping in the delegate
        doc.setTextWidth(options.rect.width())
        
        style.drawControl(PyQt6.QtWidgets.QStyle.ControlElement.CE_ItemViewItem, options, painter)
        ctx = PyQt6.QtGui.QAbstractTextDocumentLayout.PaintContext()
        
        textRect = style.subElementRect(PyQt6.QtWidgets.QStyle.SubElement.SE_ItemViewItemText, options)
        
        painter.save()
    
        painter.translate(textRect.topLeft())
        # Hide too long text; do not allow cells to overlap
        painter.setClipRect(textRect.translated(-textRect.topLeft()))
        doc.documentLayout().draw(painter, ctx)
    
        painter.restore()
    
    def sizeHint(self, option, index):
        options = PyQt6.QtWidgets.QStyleOptionViewItem(option)
        self.initStyleOption(options, index)
        
        doc = PyQt6.QtGui.QTextDocument()
        doc.setHtml(options.text)
        doc.setTextWidth(options.rect.width())
        
        return PyQt6.QtCore.QSize(doc.idealWidth(), doc.size().height())



class Welcome(PyQt6.QtWidgets.QWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_gui()
    
    def set_icon(self):
        # Does not accent None
        self.setWindowIcon(sh.gi.objs.get_icon())
    
    def show_rows(self, rownos):
        for rowno in rownos:
            self.table.show_row(rowno)
    
    def hide_rows(self, rownos):
        for rowno in rownos:
            self.table.hide_row(rowno)
    
    def resize_rows(self):
        self.table.resize_rows()
    
    def set_col_width(self, no, width):
        self.table.set_col_width(no, width)
    
    def set_span(self, rowno, colno, rowspan, colspan):
        self.table.set_span(rowno, colno, rowspan, colspan)
    
    def set_model(self, model):
        self.table.set_model(model)
    
    def show(self):
        self.showMaximized()
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            PyQt6.QtGui.QShortcut(PyQt6.QtGui.QKeySequence(hotkey), self).activated.connect(action)
    
    def centralize(self):
        self.move(sh.objs.get_root().primaryScreen().geometry().center() - self.rect().center())
    
    def set_gui(self):
        self.layout_ = PyQt6.QtWidgets.QVBoxLayout()
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.table = Table()
        self.layout_.addWidget(self.table)
        self.setLayout(self.layout_)



class Table(PyQt6.QtWidgets.QTableView):
    
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
        self.setFocusPolicy(PyQt6.QtCore.Qt.FocusPolicy.NoFocus)
        self.setSelectionMode(PyQt6.QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
    
    def resize_rows(self):
        self.resizeRowsToContents()
    
    def set_col_width(self, no, width):
        self.setColumnWidth(no, width)
    
    def set_model(self, model):
        self.setModel(model)
    
    def show_borders(self, Show=False):
        self.setShowGrid(Show)



class Objects:
    
    def __init__(self):
        self.welcome = None
    
    def get_welcome(self):
        if self.welcome is None:
            self.welcome = Welcome()
        return self.welcome


objs = Objects()
