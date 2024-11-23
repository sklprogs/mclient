#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtWidgets import QVBoxLayout, QTableView, QAbstractItemView
from PyQt6.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem, QStyle
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QShortcut, QKeySequence, QAbstractTextDocumentLayout
from PyQt6.QtGui import QTextDocument
from PyQt6.QtCore import Qt, QAbstractTableModel, QVariant, QSize

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
        if not index.isValid():
            return QVariant()
        if role == Qt.ItemDataRole.DisplayRole:
            try:
                return QVariant(self.arraydata[index.row()][index.column()])
            except Exception:
                # We will have this exception regularly for merged cells
                return QVariant()



class TableDelegate(QStyledItemDelegate):
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
        # option:  QStyleOptionViewItem
        options = QStyleOptionViewItem(option)
        self.initStyleOption(options, index)
        
        if options.widget:
            style = options.widget.style()
        else:
            style = QApplication.style()
        
        doc = QTextDocument()
        doc.setHtml(options.text)
        options.text = ''
        
        # This enables text wrapping in the delegate
        doc.setTextWidth(options.rect.width())
        
        style.drawControl(QStyle.ControlElement.CE_ItemViewItem, options, painter)
        ctx = QAbstractTextDocumentLayout.PaintContext()
        
        textRect = style.subElementRect(QStyle.SubElement.SE_ItemViewItemText, options)
        
        painter.save()
    
        painter.translate(textRect.topLeft())
        # Hide too long text; do not allow cells to overlap
        painter.setClipRect(textRect.translated(-textRect.topLeft()))
        doc.documentLayout().draw(painter, ctx)
    
        painter.restore()
    
    def sizeHint(self, option, index):
        options = QStyleOptionViewItem(option)
        self.initStyleOption(options, index)
        
        doc = QTextDocument()
        doc.setHtml(options.text)
        doc.setTextWidth(options.rect.width())
        # We have 'float' at input which will crash Qt
        return QSize(int(doc.idealWidth()), int(doc.size().height()))



class Welcome(QWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_gui()
    
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
            QShortcut(QKeySequence(hotkey), self).activated.connect(action)
    
    def centralize(self):
        self.move(ROOT.get_root().primaryScreen().geometry().center() - self.rect().center())
    
    def set_gui(self):
        self.layout_ = QVBoxLayout()
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.table = Table()
        self.layout_.addWidget(self.table)
        self.setLayout(self.layout_)



class Table(QTableView):
    
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
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
    
    def resize_rows(self):
        self.resizeRowsToContents()
    
    def set_col_width(self, no, width):
        self.setColumnWidth(no, width)
    
    def set_model(self, model):
        self.setModel(model)
    
    def show_borders(self, Show=False):
        self.setShowGrid(Show)


WELCOME = Welcome()
