#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtWidgets import QTableView, QStyleOptionViewItem, QAbstractItemView
from PyQt6.QtWidgets import QStyledItemDelegate, QApplication, QStyle
from PyQt6.QtCore import pyqtSignal, Qt, QSize, QAbstractTableModel, QVariant
from PyQt6.QtGui import QTextCursor, QTextDocument, QAbstractTextDocumentLayout
from PyQt6.QtGui import QColor, QPen

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import rep, Message

WIDE_ROW_COLOR = '#CCCCCC'
WIDE_ROW_LEN = 70


class TableModel(QAbstractTableModel):
    
    def __init__(self, datain, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        if not self.arraydata:
            return 0
        return len(self.arraydata[0])

    def data(self, index, role):
        f = '[MClient] table.gui.TableModel.data'
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
    
    def update(self, index_):
        self.dataChanged.emit(index_, index_)



class TableDelegate(QStyledItemDelegate):
    # akej74, https://stackoverflow.com/questions/35397943/how-to-make-a-fast-qtableview-with-html-formatted-and-clickable-cells
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.index = None
        self.long = []
    
    def set_line_spacing(self, doc):
        f = '[MClient] table.gui.TableDelegate.set_line_spacing'
        cursor = QTextCursor(doc)
        block = doc.firstBlock()
        if not block.isValid():
            rep.wrong_input(f)
            return
        format_ = block.blockFormat()
        format_.setLineHeight(19, 2)
        cursor.setBlockFormat(format_)
    
    def paint(self, painter, option, index):
        f = '[MClient] table.gui.TableDelegate.paint'
        # index:   PyQt6.QtCore.QModelIndex
        # painter: PyQt6.QtGui.QPainter
        # option:  PyQt6.QtWidgets.QStyleOptionViewItem
        options = QStyleOptionViewItem(option)
        self.initStyleOption(options, index)
        
        if options.widget:
            style = options.widget.style()
        else:
            style = QApplication.style()
        
        doc = QTextDocument()
        doc.setHtml(options.text)
        options.text = ''
        
        self.set_line_spacing(doc)
        
        # This enables text wrapping in the delegate
        doc.setTextWidth(options.rect.width())
        
        style.drawControl(QStyle.ControlElement.CE_ItemViewItem, options, painter)
        ctx = QAbstractTextDocumentLayout.PaintContext()
        
        textRect = style.subElementRect(QStyle.SubElement.SE_ItemViewItemText, options)
        
        if self.index is None:
            mes = _('Index must be set externally!')
            Message(f, mes).show_error()
        elif index == self.index:
            color = QColor('red')
            pen = QPen(color, 2)
            painter.setPen(pen)
            # Avoid intersecting cell borders and artifacts as the result
            x1, y1, x2, y2 = option.rect.getCoords()
            option.rect.setCoords(x1 + 1, y1 + 1, x2 - 1, y2 - 1)
            painter.drawRect(option.rect)
        
        if self.long and index in self.long:
            color = QColor(WIDE_ROW_COLOR)
            pen = QPen(color, 2)
            pen.setStyle(Qt.PenStyle.DotLine)
            painter.setPen(pen)
            # Avoid intersecting cell borders and artifacts as the result
            x1, y1, x2, y2 = option.rect.getCoords()
            painter.drawLine(x1 + 5, y2 - 1, x1 + WIDE_ROW_LEN, y2 - 1)
        
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
        
        return QSize(doc.idealWidth(), doc.size().height())



class Table(QTableView):
    
    sig_select = pyqtSignal(int, int, bool)
    sig_rmb = pyqtSignal()
    sig_mmb = pyqtSignal()
    sig_popup = pyqtSignal()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.delegate = TableDelegate()
        # Do not override internal 'x' and 'y'
        self.x_ = 0
        self.y_ = 0
        self.set_gui()
    
    def _use_mouse(self, event):
        pos = event.position().toPoint()
        self.x_ = pos.x()
        self.y_ = pos.y()
        rowno = self.rowAt(self.y_)
        colno = self.columnAt(self.x_)
        self.sig_select.emit(rowno, colno, True)
    
    def mouseMoveEvent(self, event):
        self._use_mouse(event)
        return super().mouseMoveEvent(event)
    
    def get_col_width(self, colno):
        return self.columnWidth(colno)
    
    def get_row_height(self, rowno):
        return self.rowHeight(rowno)
    
    def get_cell_hint(self, index_):
        option = QStyleOptionViewItem()
        return self.delegate.sizeHint(option, index_).height()
    
    def get_cell_space(self, index_):
        option = QStyleOptionViewItem()
        hint = self.delegate.sizeHint(option, index_)
        return hint.width() * hint.height()
    
    def scroll2index(self, index_):
        self.scrollTo(index_, QAbstractItemView.ScrollHint.PositionAtTop)
    
    def scroll2top(self):
        self.scrollToTop()
    
    def get_row_by_y(self, y):
        return self.rowAt(y)
    
    def get_row_hint(self, rowno):
        return self.sizeHintForRow(rowno)
    
    def get_row_y(self, rowno):
        return self.rowViewportPosition(rowno)
    
    def get_row(self, index_):
        return index_.row()
    
    def get_column(self, index_):
        return index_.column()
    
    def get_index(self):
        return self.delegate.index
    
    def set_index(self, index_):
        self.delegate.index = index_
    
    def set_cur_index(self, index_):
        self.setCurrentIndex(index_)
        self.delegate.index = index_
    
    def get_cur_index(self):
        return self.currentIndex()
    
    def get_cur_cell(self):
        index_ = self.currentIndex()
        return(index_.row(), index_.column())
    
    def get_cell(self):
        return(self.delegate.index.row(), self.delegate.index.column())
    
    def get_height(self):
        ''' #NOTE: Run only after events since Qt returns dummy geometry values
            right after startup. This is claimed to be fixed by showing the
            window, but I have not managed this yet.
        '''
        return self.height()
    
    def get_cell_x(self, colno):
        return self.columnViewportPosition(colno)
    
    def get_cell_y(self, rowno):
        return self.rowViewportPosition(rowno)
    
    def set_model(self, model):
        self.setModel(model)
    
    def mousePressEvent(self, event):
        button = event.button()
        if button == Qt.MouseButton.RightButton:
            self.sig_rmb.emit()
        elif button == Qt.MouseButton.MiddleButton:
            self.sig_mmb.emit()
        super().mousePressEvent(event)
    
    def set_col_width(self, no, width):
        self.setColumnWidth(no, width)
    
    def set_row_height(self, no, height):
        self.setRowHeight(no, height)
    
    def set_max_row_height(self, height):
        self.vheader.setMaximumSectionSize(height)
    
    def set_gui(self):
        self.delegate.index = self.get_cur_index()
        self.setItemDelegate(self.delegate)
        self.hheader = self.horizontalHeader()
        self.vheader = self.verticalHeader()
        self.hheader.setVisible(False)
        self.vheader.setVisible(False)
        # Do not allow Qt to colorize cell background
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.setMouseTracking(True)
    
    def show_borders(self, Show=False):
        self.setShowGrid(Show)
    
    def show_popup(self):
        self.sig_popup.emit()
