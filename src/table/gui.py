#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtWidgets import QTableView, QStyleOptionViewItem, QAbstractItemView,\
                            QStyledItemDelegate, QApplication, QStyle
from PyQt6.QtCore import pyqtSignal, Qt, QSize, QAbstractTableModel, QVariant,\
                         QPointF, QModelIndex
from PyQt6.QtGui import QTextCursor, QTextDocument, QAbstractTextDocumentLayout,\
                        QColor, QPen, QPainter

from skl_shared.localize import _
from skl_shared.message.controller import rep, Message
from config import CONFIG

WIDE_ROW_COLOR = '#CCCCCC'
WIDE_ROW_LEN = 70
''' Putting this in TableDelegate does not work (probably because
    table.gui.TableDelegate.paint is called after table.controller.Table.select),
    but for some reason the global list works. Paint processes only a visible
    screen area, so WIDE_ROWS will be constantly updated.
'''
WIDE_ROWS = []


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
    
    def update(self, rowno, colno, code):
        # We need to update underlying data, not only blocks
        self.arraydata[rowno][colno] = code
        index_ = self.index(rowno, colno)
        # Since we update a single cell, indexes are the same
        self.dataChanged.emit(index_, index_, [Qt.ItemDataRole.DisplayRole])



class TableDelegate(QStyledItemDelegate):
    sig_select = pyqtSignal(str, bool)
    # akej74, https://stackoverflow.com/questions/35397943/how-to-make-a-fast-qtableview-with-html-formatted-and-clickable-cells
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mclast_block_no = None
        self.mcindex = None
        self.mcdoc = QTextDocument()
        self.mcpen_border = QPen(QColor(CONFIG.new['rows']['border']['color']), 2)
        self.mcpen_row = QPen(QColor(WIDE_ROW_COLOR), 2)
        self.mcpen_row.setStyle(Qt.PenStyle.DotLine)
        self.mccursor = QTextCursor(self.mcdoc)
        self.mcstyle = QApplication.style()
    
    def mcget_block(self, point: QPointF):
        f = '[MClient] table.gui.TableDelegate.mcget_block'
        # Return block.no for the link under point, or None
        href = self.mcdoc.documentLayout().anchorAt(point)
        if not href.startswith("block#"):
            # Occurs too often
            return
        return href.removeprefix("block#")
    
    def mcset_line_spacing(self):
        f = '[MClient] table.gui.TableDelegate.mcset_line_spacing'
        block = self.mcdoc.firstBlock()
        if not block.isValid():
            rep.wrong_input(f)
            return
        format_ = block.blockFormat()
        format_.setLineHeight(19, 2)
        self.mccursor.setBlockFormat(format_)
    
    def _set_up_doc(self, option: QStyleOptionViewItem, index: QModelIndex):
        options = QStyleOptionViewItem(option)
        self.initStyleOption(options, index)
        style = options.widget.style() if options.widget else self.mcstyle
        self.mcdoc.setHtml(options.text)
        options.text = ''
        textRect = style.subElementRect(QStyle.SubElement.SE_ItemViewItemText, options)
        # Enable text wrapping
        self.mcdoc.setTextWidth(textRect.width())
        return(options, style, textRect)
    
    def _mcdraw_row(self, index, painter, option):
        ''' Cell calculated height can exceed max allowed row height, but
            the cell can still remain visible because there is spacing between
            cells (the hard-coded value is 19). '''
        if self.mcdoc.documentLayout().documentSize().height() <= CONFIG.new['rows']['height'] + 19:
            return
        # Must be index, not self.mcindex
        if index and not index in WIDE_ROWS:
            WIDE_ROWS.append(index)
        painter.setPen(self.mcpen_row)
        # Avoid intersecting cell borders and artifacts as the result
        x1, y1, x2, y2 = option.rect.getCoords()
        painter.drawLine(x1 + 5, y2 - 1, x1 + WIDE_ROW_LEN, y2 - 1)
    
    def _mcdraw_frame(self, index, painter, option):
        f = '[MClient] table.gui.TableDelegate._mcdraw_frame'
        if self.mcindex is None:
            mes = _('Index must be set externally!')
            Message(f, mes).show_error()
            return
        if CONFIG.new['BlockMode'] or index != self.mcindex:
            return
        painter.setPen(self.mcpen_border)
        x1, y1, x2, y2 = option.rect.getCoords()
        # +/-1 to avoid intersecting cell borders and artifacts as the result
        option.rect.setCoords(x1 + 1, y1 + 1, x2 - 1, y2 - 1)
        painter.drawRect(option.rect)
    
    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        f = '[MClient] table.gui.TableDelegate.paint'
        options, style, textRect = self._set_up_doc(option, index)
        self.mcset_line_spacing()
        style.drawControl(QStyle.ControlElement.CE_ItemViewItem, options, painter)
        self._mcdraw_frame(index, painter, option)
        self._mcdraw_row(index, painter, option)
        painter.save()
        painter.translate(textRect.topLeft())
        # Hide too long text; do not allow cells to overlap
        painter.setClipRect(textRect.translated(-textRect.topLeft()))
        ctx = QAbstractTextDocumentLayout.PaintContext()
        self.mcdoc.documentLayout().draw(painter, ctx)
        painter.restore()
    
    def editorEvent(self, event, model, option: QStyleOptionViewItem, index: QModelIndex):
        self._set_up_doc(option, index)
        if event.type() == event.Type.MouseMove:
            ''' Mouse position is in viewport coordinates; the document starts
                at the cell's top-left corner. '''
            point = event.position() - QPointF(option.rect.topLeft())
            block_no = self.mcget_block(point)
            if not block_no in (self.mclast_block_no, None):
                self.mclast_block_no = block_no
                self.sig_select.emit(block_no, True)
            elif event.type() == event.Type.Leave:
                self.mclast_block_no = None
        return False
    
    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex):
        self._set_up_doc(option, index)
        # 'float' is possible but not allowed
        return QSize(int(self.mcdoc.idealWidth()), int(self.mcdoc.size().height()))



class Table(QTableView):
    
    sig_rmb = pyqtSignal()
    sig_mmb = pyqtSignal()
    sig_popup = pyqtSignal()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reset_delegate()
        self.set_gui()
    
    def reset_delegate(self):
        WIDE_ROWS.clear()
        self.delegate = TableDelegate()
    
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
        return self.delegate.mcindex
    
    def set_index(self, index_):
        self.delegate.mcindex = index_
    
    def set_cur_index(self, index_):
        self.setCurrentIndex(index_)
        self.delegate.mcindex = index_
    
    def get_cur_index(self):
        return self.currentIndex()
    
    def get_cur_cell(self):
        index_ = self.currentIndex()
        return(index_.row(), index_.column())
    
    def get_cell(self):
        return(self.delegate.mcindex.row(), self.delegate.mcindex.column())
    
    def get_height(self):
        ''' #NOTE: Run only after events since Qt returns dummy geometry values
            right after startup. This is claimed to be fixed by showing the
            window, but I have not managed this yet. '''
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
        self.delegate.mcindex = self.get_cur_index()
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
    
    def resize_to_contents(self):
        self.resizeRowsToContents()
