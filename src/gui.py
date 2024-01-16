#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt6
import PyQt6.QtWidgets

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import welcome.gui

sh.gi.ICON = sh.objs.get_pdir().add('..', 'resources', 'mclient.png')
WIDE_ROW_COLOR = '#CCCCCC'
WIDE_ROW_LEN = 70


class FontLimits:
    
    def __init__(self):
        pass
    
    def get_font(self, family, size, weight, italic):
        return PyQt6.QtGui.QFont (family
                                 ,pointSize = size
                                 ,weight = weight
                                 ,italic = italic
                                 )
    
    def get_space(self, text, qfont):
        qrect = PyQt6.QtGui.QFontMetrics(qfont).boundingRect(text)
        return qrect.width() * qrect.height()



class Entry(sh.Entry):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gui = MinEntry()
        self.widget = self.gui.widget
        self.parent = None



class MinEntry(sh.gi.Entry):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def set_gui(self):
        self.widget = MinEntryCore()



class MinEntryCore(PyQt6.QtWidgets.QLineEdit):
    
    sig_ctrl_e = PyQt6.QtCore.pyqtSignal()
    sig_ctrl_home = PyQt6.QtCore.pyqtSignal()
    sig_ctrl_end = PyQt6.QtCore.pyqtSignal()
    sig_ctrl_space = PyQt6.QtCore.pyqtSignal()
    sig_left_arrow = PyQt6.QtCore.pyqtSignal()
    sig_right_arrow = PyQt6.QtCore.pyqtSignal()
    sig_home = PyQt6.QtCore.pyqtSignal()
    sig_end = PyQt6.QtCore.pyqtSignal()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def keyPressEvent(self, event):
        key = event.key()
        modifiers = event.modifiers()
        ''' Internal Ctrl+ bindings are not needed, so they are ignored. Other
            bindings (such as Home, End, Left and Right) must be preserved.
        '''
        if modifiers & PyQt6.QtCore.Qt.KeyboardModifier.ControlModifier:
            if key == PyQt6.QtCore.Qt.Key.Key_Home:
                self.sig_ctrl_home.emit()
                return
            if key == PyQt6.QtCore.Qt.Key.Key_End:
                self.sig_ctrl_end.emit()
                return
            if key == PyQt6.QtCore.Qt.Key.Key_E:
                self.sig_ctrl_e.emit()
                return
            if key == PyQt6.QtCore.Qt.Key.Key_Space:
                self.sig_ctrl_space.emit()
                return
        elif key == PyQt6.QtCore.Qt.Key.Key_Left:
            self.sig_left_arrow.emit()
        elif key == PyQt6.QtCore.Qt.Key.Key_Right:
            self.sig_right_arrow.emit()
        elif key == PyQt6.QtCore.Qt.Key.Key_Home:
            self.sig_home.emit()
        elif key == PyQt6.QtCore.Qt.Key.Key_End:
            self.sig_end.emit()
        return super().keyPressEvent(event)



class TableModel(PyQt6.QtCore.QAbstractTableModel):
    
    def __init__(self, datain, parent=None, *args):
        PyQt6.QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        if not self.arraydata:
            return 0
        return len(self.arraydata[0])

    def data(self, index, role):
        f = '[MClient] gui.TableModel.data'
        if not index.isValid():
            return PyQt6.QtCore.QVariant()
        if role == PyQt6.QtCore.Qt.ItemDataRole.DisplayRole:
            try:
                return PyQt6.QtCore.QVariant(self.arraydata[index.row()][index.column()])
            except Exception:
                mes = _('List out of bounds at row #{}, column #{}!')
                mes = mes.format(index.row(), index.column())
                sh.objs.get_mes(f, mes, True).show_warning()
                return PyQt6.QtCore.QVariant()
    
    def update(self, index_):
        self.dataChanged.emit(index_, index_)



class TableDelegate(PyQt6.QtWidgets.QStyledItemDelegate):
    # akej74, https://stackoverflow.com/questions/35397943/how-to-make-a-fast-qtableview-with-html-formatted-and-clickable-cells
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.index = None
        self.long = []
    
    def set_line_spacing(self, doc):
        f = '[MClient] gui.TableDelegate.set_line_spacing'
        cursor = PyQt6.QtGui.QTextCursor(doc)
        block = doc.firstBlock()
        if not block.isValid():
            mes = _('Wrong input data!')
            sh.objs.get_mes(f, mes, True).show_debug()
            return
        format_ = block.blockFormat()
        format_.setLineHeight(19, 2)
        cursor.setBlockFormat(format_)
    
    def paint(self, painter, option, index):
        f = '[MClient] gui.TableDelegate.paint'
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
        
        self.set_line_spacing(doc)
        
        # This enables text wrapping in the delegate
        doc.setTextWidth(options.rect.width())
        
        style.drawControl(PyQt6.QtWidgets.QStyle.ControlElement.CE_ItemViewItem, options, painter)
        ctx = PyQt6.QtGui.QAbstractTextDocumentLayout.PaintContext()
        
        textRect = style.subElementRect(PyQt6.QtWidgets.QStyle.SubElement.SE_ItemViewItemText, options)
        
        if self.index is None:
            mes = _('Index must be set externally!')
            sh.objs.get_mes(f, mes, True).show_error()
        elif index == self.index:
            color = PyQt6.QtGui.QColor('red')
            pen = PyQt6.QtGui.QPen(color, 2)
            painter.setPen(pen)
            # Avoid intersecting cell borders and artifacts as the result
            x1, y1, x2, y2 = option.rect.getCoords()
            option.rect.setCoords(x1 + 1, y1 + 1, x2 - 1, y2 - 1)
            painter.drawRect(option.rect)
        
        if self.long and index in self.long:
            color = PyQt6.QtGui.QColor(WIDE_ROW_COLOR)
            pen = PyQt6.QtGui.QPen(color, 2)
            pen.setStyle(PyQt6.QtCore.Qt.PenStyle.DotLine)
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
        options = PyQt6.QtWidgets.QStyleOptionViewItem(option)
        self.initStyleOption(options, index)
        
        doc = PyQt6.QtGui.QTextDocument()
        doc.setHtml(options.text)
        doc.setTextWidth(options.rect.width())
        
        return PyQt6.QtCore.QSize(doc.idealWidth(), doc.size().height())



class Table(PyQt6.QtWidgets.QTableView):
    
    sig_select = PyQt6.QtCore.pyqtSignal(int, int, bool)
    sig_rmb = PyQt6.QtCore.pyqtSignal()
    sig_mmb = PyQt6.QtCore.pyqtSignal()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        option = PyQt6.QtWidgets.QStyleOptionViewItem()
        return self.delegate.sizeHint(option, index_).height()
    
    def get_cell_space(self, index_):
        option = PyQt6.QtWidgets.QStyleOptionViewItem()
        hint = self.delegate.sizeHint(option, index_)
        return hint.width() * hint.height()
    
    def scroll2index(self, index_):
        self.scrollTo(index_, PyQt6.QtWidgets.QAbstractItemView.ScrollHint.PositionAtTop)
    
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
        if button == PyQt6.QtCore.Qt.MouseButton.RightButton:
            self.sig_rmb.emit()
        elif button == PyQt6.QtCore.Qt.MouseButton.MiddleButton:
            self.sig_mmb.emit()
        super().mousePressEvent(event)
    
    def set_col_width(self, no, width):
        self.setColumnWidth(no, width)
    
    def set_row_height(self, no, height):
        self.setRowHeight(no, height)
    
    def set_max_row_height(self, height):
        self.vheader.setMaximumSectionSize(height)
    
    def set_gui(self):
        self.delegate = TableDelegate()
        self.delegate.index = self.get_cur_index()
        self.setItemDelegate(self.delegate)
        self.hheader = self.horizontalHeader()
        self.vheader = self.verticalHeader()
        self.hheader.setVisible(False)
        self.vheader.setVisible(False)
        # Do not allow Qt to colorize cell background
        self.setFocusPolicy(PyQt6.QtCore.Qt.FocusPolicy.NoFocus)
        self.setSelectionMode(PyQt6.QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.setMouseTracking(True)
    
    def show_borders(self, Show=False):
        self.setShowGrid(Show)



class TableProxy(PyQt6.QtWidgets.QWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_gui()
    
    def set_gui(self):
        self.layout_ = PyQt6.QtWidgets.QVBoxLayout()
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.addWidget(objs.get_table())
        self.setLayout(self.layout_)



class ArticleProxy(PyQt6.QtWidgets.QWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active = welcome.gui.objs.get_welcome()
        self.set_gui()
    
    def set_gui(self):
        self.layout_ = PyQt6.QtWidgets.QStackedLayout()
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.addWidget(welcome.gui.objs.get_welcome())
        self.table = TableProxy()
        self.layout_.addWidget(self.table)
        self.setLayout(self.layout_)
    
    def is_welcome(self):
        return self.active == welcome.gui.objs.get_welcome()
    
    def go_welcome(self):
        f = '[MClient] gui.ArticleProxy.go_welcome'
        if self.is_welcome():
            sh.com.rep_lazy(f)
            return
        width = self.table.width()
        height = self.table.height()
        self.table.hide()
        self.active = welcome.gui.objs.get_welcome()
        self.active.show()
        self.active.resize(width, height)
    
    def go_article(self):
        f = '[MClient] gui.ArticleProxy.go_article'
        if self.active == self.table:
            sh.com.rep_lazy(f)
            return
        width = welcome.gui.objs.get_welcome().width()
        height = welcome.gui.objs.welcome.height()
        welcome.gui.objs.welcome.hide()
        self.active = self.table
        self.active.show()
        self.active.resize(width, height)



class App(PyQt6.QtWidgets.QMainWindow):
    
    sig_close = PyQt6.QtCore.pyqtSignal()
    sig_pgdn = PyQt6.QtCore.pyqtSignal()
    sig_pgup = PyQt6.QtCore.pyqtSignal()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_gui()
    
    def get_x(self):
        return self.pos().x()
    
    def get_y(self):
        return self.pos().y()
    
    def activate(self):
        ''' Remove minimized status and restore window with keeping maximized
            or normal state. Works on Linux and Windows 10, but not 11.
        '''
        self.setWindowState(self.windowState() & ~PyQt6.QtCore.Qt.WindowState.WindowMinimized | PyQt6.QtCore.Qt.WindowState.WindowActive)
        self.activateWindow()
    
    def keyPressEvent(self, event):
        if event.key() == PyQt6.QtCore.Qt.Key.Key_PageUp:
            self.sig_pgup.emit()
        elif event.key() == PyQt6.QtCore.Qt.Key.Key_PageDown:
            self.sig_pgdn.emit()
        return super().keyPressEvent(event)
    
    def closeEvent(self, event):
        self.sig_close.emit()
        return super().closeEvent(event)
    
    def get_width(self):
        return self.width()
    
    def get_height(self):
        return self.height()
    
    def minimize(self):
        self.showMinimized()
    
    def show(self):
        self.showMaximized()
    
    def set_title(self, title):
        self.setWindowTitle(title)
    
    def set_layout(self):
        self.parent = PyQt6.QtWidgets.QWidget()
        self.layout_ = PyQt6.QtWidgets.QVBoxLayout()
        self.layout_.setContentsMargins(0, 0, 0, 0)
    
    def add_widgets(self):
        self.layout_.addWidget(objs.get_article_proxy())
        self.layout_.addWidget(objs.get_panel(), 1)
        self.parent.setLayout(self.layout_)
    
    def set_icon(self):
        # Does not accent None
        self.setWindowIcon(sh.gi.objs.get_icon())
    
    def set_gui(self):
        self.set_layout()
        self.add_widgets()
        self.setCentralWidget(self.parent)
        self.set_icon()
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            PyQt6.QtGui.QShortcut(PyQt6.QtGui.QKeySequence(hotkey), self).activated.connect(action)



class MinPanel(PyQt6.QtWidgets.QWidget):

    sig_hover = PyQt6.QtCore.pyqtSignal(PyQt6.QtCore.QEvent)
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setMouseTracking(True)
    
    def mouseMoveEvent(self, event):
        self.sig_hover.emit(event)
        return super().mouseMoveEvent(event)



class Panel(PyQt6.QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_values()
        self.set_gui()
    
    def set_values(self):
        self.delta = 0
        self.offset = 45
        self.pos = 0
        self.max_opt_width = 110
        self.icn_al0 = sh.objs.get_pdir().add ('..', 'resources', 'buttons'
                                              ,'alphabet_off.png'
                                              )
        self.icn_al1 = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'alphabet_on.png'
                                        )
        self.icn_bl0 = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'block_off.png'
                                        )
        self.icn_bl1 = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'block_on.png'
                                        )
        self.icn_clr = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'clear_search_field.png'
                                        )
        self.icn_def = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'define.png'
                                        )
        self.icn_bk0 = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'go_back_off.png'
                                        )
        self.icn_bk1 = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'go_back.png'
                                        )
        self.icn_fw0 = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'go_next_off.png'
                                        )
        self.icn_fw1 = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'go_next.png'
                                        )
        self.icn_ret = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'go_search.png'
                                        )
        self.icn_brw = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'open_in_browser.png'
                                        )
        self.icn_ins = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'paste.png'
                                        )
        self.icn_prn = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'print.png'
                                        )
        self.icn_pr0 = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'priority_off.png'
                                        )
        self.icn_pr1 = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'priority_on.png'
                                        )
        self.icn_qit = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'quit_now.png'
                                        )
        self.icn_rld = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'reload.png'
                                        )
        self.icn_rp0 = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'repeat_sign_off.png'
                                        )
        self.icn_rp1 = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'repeat_sign.png'
                                        )
        self.icn_r20 = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'repeat_sign2_off.png'
                                        )
        self.icn_r21 = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'repeat_sign2.png'
                                        )
        self.icn_sav = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'save_article.png'
                                        )
        self.icn_src = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'search_article.png'
                                        )
        self.icn_set = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'settings.png'
                                        )
        self.icn_abt = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'show_about.png'
                                        )
        self.icn_sym = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'spec_symbol.png'
                                        )
        self.icn_hst = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'toggle_history.png'
                                        )
        self.icn_cp0 = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'watch_clipboard_off.png'
                                        )
        self.icn_cp1 = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'watch_clipboard_on.png'
                                        )
        self.icn_swp = sh.objs.pdir.add ('..', 'resources', 'buttons'
                                        ,'swap_langs.png'
                                        )
    
    def set_delta(self):
        ''' Set a delta value between a label size and a main widget size. This
            should be called only after the widget is drawn, otherwise, Qt will
            return bogus geometry of 640x480.
            #TODO (?): do not update each time on hovering, update only when
            the window size is changed.
        '''
        self.delta = self.width() - self.panel.width()
    
    def slide_left(self):
        if self.panel.x() - self.offset >= self.delta:
            self.pos -= self.offset
            self.panel.move(self.pos, 0)
    
    def slide_right(self):
        if self.panel.x() + self.offset <= 0:
            self.pos += self.offset
            self.panel.move(self.pos, 0)
    
    def trigger_hover(self, event):
        ''' We should not use event.x since this returns x relative to the
            widget that caused the event, and this widget will be any we have
            mouse over.
        '''
        self.set_delta()
        geom = self.geometry()
        x = PyQt6.QtGui.QCursor().pos().x() - geom.left()
        width = geom.width()
        if 0 <= x <= 30:
            self.slide_right()
        elif width - 30 <= x <= width:
            self.slide_left()
    
    def set_hint_bg(self):
        self.setStyleSheet('QPushButton:hover {background-color: white} QToolTip {background-color: #ffffe0}')
    
    def set_widgets(self):
        self.setMaximumHeight(44)
        self.panel = MinPanel(self)
        self.layout_ = PyQt6.QtWidgets.QHBoxLayout()
        self.layout_.setContentsMargins(4, 4, 4, 4)
        self.ent_src = Entry()
        self.ent_src.set_min_width(96)
        # A button for newbies, substitutes Enter in search_field
        self.btn_trn = sh.Button (hint = _('Translate')
                                 ,inactive = self.icn_ret
                                 ,active = self.icn_ret
                                 )
        # A button to clear the search field
        self.btn_clr = sh.Button (hint = _('Clear search field')
                                 ,inactive = self.icn_clr
                                 ,active = self.icn_clr
                                 )
        # A button to insert text into the search field
        self.btn_ins = sh.Button (hint = _('Paste text from clipboard')
                                 ,inactive = self.icn_ins
                                 ,active = self.icn_ins
                                 )
        # A button to insert a current search
        self.btn_rp1 = sh.Button (hint = _('Paste current request')
                                 ,inactive = self.icn_rp0
                                 ,active = self.icn_rp1
                                 )
        # A button to insert a previous search
        self.btn_rp2 = sh.Button (hint = _('Paste previous request')
                                 ,inactive = self.icn_r20
                                 ,active = self.icn_r21
                                 )
        # A button to insert special symbols
        self.btn_sym = sh.Button (inactive = self.icn_sym
                                 ,active = self.icn_sym
                                 )
        # Drop-down list with dictionary sources
        self.opt_src = sh.OptionMenu()
        # Drop-down lists with languages
        self.opt_lg1 = sh.OptionMenu()
        self.btn_swp = sh.Button (inactive = self.icn_swp
                                 ,active = self.icn_swp
                                 )
        self.opt_lg2 = sh.OptionMenu()
        self.opt_col = sh.OptionMenu(range(1, 11), 5)
        # A settings button
        self.btn_set = sh.Button (inactive = self.icn_set
                                 ,active = self.icn_set
                                 )
        # A button to toggle subject blocking
        self.btn_blk = sh.Button (inactive = self.icn_bl0
                                 ,active = self.icn_bl1
                                 )
        # A button to toggle subject prioritization
        self.btn_pri = sh.Button (inactive = self.icn_pr0
                                 ,active = self.icn_pr1
                                 )
        # A button to toggle subject alphabetization
        self.btn_alp = sh.Button (inactive = self.icn_al0
                                 ,active = self.icn_al1
                                 )
        # A button to move to the previous article
        self.btn_prv = sh.Button (inactive = self.icn_bk0
                                 ,active = self.icn_bk1
                                 )
        # A button to move to the next article
        self.btn_nxt = sh.Button (inactive = self.icn_fw0
                                 ,active = self.icn_fw1
                                 )
        # A button to toggle and clear history
        self.btn_hst = sh.Button (inactive = self.icn_hst
                                 ,active = self.icn_hst
                                 )
        # A button to reload the article
        self.btn_rld = sh.Button (inactive = self.icn_rld
                                 ,active = self.icn_rld
                                 )
        # A button to search within the article
        self.btn_ser = sh.Button (inactive = self.icn_src
                                 ,active = self.icn_src
                                 )
        # A button to save the article
        self.btn_sav = sh.Button (inactive = self.icn_sav
                                 ,active = self.icn_sav
                                 )
        # A button to open the current article in a browser
        self.btn_brw = sh.Button (inactive = self.icn_brw
                                 ,active = self.icn_brw
                                 )
        # A button to print the article
        self.btn_prn = sh.Button (inactive = self.icn_prn
                                 ,active = self.icn_prn
                                 )
        # A button to define a term
        self.btn_def = sh.Button (inactive = self.icn_def
                                 ,active = self.icn_def
                                 )
        # A button to toggle capturing Ctrl-c-c and Ctrl-Ins-Ins
        self.btn_cap = sh.Button (hint = _('Capture Ctrl-c-c and Ctrl-Ins-Ins')
                                 ,inactive = self.icn_cp0
                                 ,active = self.icn_cp1
                                 )
        # A button to show info about the program
        self.btn_abt = sh.Button (inactive = self.icn_abt
                                 ,active = self.icn_abt
                                 )
        # A button to quit the program
        self.btn_qit = sh.Button (inactive = self.icn_qit
                                 ,active = self.icn_qit
                                 )
        self.layout_.addWidget(self.ent_src.widget)
        self.layout_.addWidget(self.btn_trn.widget)
        self.layout_.addWidget(self.btn_clr.widget)
        self.layout_.addWidget(self.btn_ins.widget)
        self.layout_.addWidget(self.btn_rp1.widget)
        self.layout_.addWidget(self.btn_rp2.widget)
        self.layout_.addWidget(self.btn_sym.widget)
        self.layout_.addWidget(self.opt_src.widget)
        self.layout_.addWidget(self.opt_lg1.widget)
        self.layout_.addWidget(self.btn_swp.widget)
        self.layout_.addWidget(self.opt_lg2.widget)
        self.layout_.addWidget(self.opt_col.widget)
        self.layout_.addWidget(self.btn_set.widget)
        self.layout_.addWidget(self.btn_blk.widget)
        self.layout_.addWidget(self.btn_pri.widget)
        self.layout_.addWidget(self.btn_alp.widget)
        self.layout_.addWidget(self.btn_prv.widget)
        self.layout_.addWidget(self.btn_nxt.widget)
        self.layout_.addWidget(self.btn_hst.widget)
        self.layout_.addWidget(self.btn_rld.widget)
        self.layout_.addWidget(self.btn_ser.widget)
        self.layout_.addWidget(self.btn_sav.widget)
        self.layout_.addWidget(self.btn_brw.widget)
        self.layout_.addWidget(self.btn_prn.widget)
        self.layout_.addWidget(self.btn_def.widget)
        self.layout_.addWidget(self.btn_cap.widget)
        self.layout_.addWidget(self.btn_abt.widget)
        self.layout_.addWidget(self.btn_qit.widget)
        self.panel.setLayout(self.layout_)
    
    def set_bindings(self):
        self.panel.sig_hover.connect(self.trigger_hover)
    
    def set_max_opt_width(self):
        self.opt_src.widget.setMaximumWidth(self.max_opt_width)
        self.opt_lg1.widget.setMaximumWidth(self.max_opt_width)
        self.opt_lg2.widget.setMaximumWidth(self.max_opt_width)
        self.opt_col.widget.setMaximumWidth(self.max_opt_width)
    
    def set_gui(self):
        self.set_widgets()
        self.set_hint_bg()
        self.set_max_opt_width()
        self.set_bindings()



class Search(PyQt6.QtWidgets.QWidget):

    sig_close = PyQt6.QtCore.pyqtSignal()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_gui()
    
    def set_icon(self):
        # Does not accent None
        self.setWindowIcon(sh.gi.objs.get_icon())
    
    def closeEvent(self, event):
        self.sig_close.emit()
        return super().closeEvent(event)
    
    def clear(self):
        self.ent_src.clear()
    
    def set_title(self, title=_('Search:')):
        self.setWindowTitle(title)
    
    def add_widgets(self):
        self.layout_ = PyQt6.QtWidgets.QVBoxLayout()
        self.ent_src = sh.Entry()
        self.cbx_cas = sh.CheckBox(_('Case-sensitive'))
        self.btn_cls = sh.Button(_('Close'))
        self.btn_clr = sh.Button(_('Clear'))
        self.btn_srp = sh.Button(_('Back'))
        self.btn_srn = sh.Button(_('Forward'))
        self.layout_.addWidget(self.ent_src.widget)
        self.layout_.addWidget(self.cbx_cas.widget)
        self.panel = PyQt6.QtWidgets.QWidget()
        self.btn_lay = PyQt6.QtWidgets.QHBoxLayout()
        self.btn_lay.setContentsMargins(4, 4, 4, 4)
        self.btn_lay.addWidget(self.btn_cls.widget)
        self.btn_lay.addWidget(self.btn_clr.widget)
        self.btn_lay.addWidget(self.btn_srp.widget)
        self.btn_lay.addWidget(self.btn_srn.widget)
        self.panel.setLayout(self.btn_lay)
        self.layout_.addWidget(self.panel)
        self.setLayout(self.layout_)
    
    def set_gui(self):
        self.add_widgets()
        self.set_title()
        self.set_icon()
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            PyQt6.QtGui.QShortcut(PyQt6.QtGui.QKeySequence(hotkey), self).activated.connect(action)
    
    def get(self):
        return self.ent_src.get()



class Objects:
    
    def __init__(self):
        self.panel = self.table = self.article_proxy = None
    
    def get_article_proxy(self):
        if self.article_proxy is None:
            self.article_proxy = ArticleProxy()
        return self.article_proxy
    
    def get_panel(self):
        if self.panel is None:
            self.panel = Panel()
        return self.panel
    
    def get_table(self):
        if self.table is None:
            self.table = Table()
        return self.table


objs = Objects()


if __name__ == '__main__':
    '''
    sh.com.start()
    Search().show()
    sh.com.end()
    '''
    import sys
    exe = PyQt6.QtWidgets.QApplication(sys.argv)
    app = App()
    app.set_gui()
    
    data = [['hel<b>L</b>o', 'I Am Here', 'Hello there!']
           ,['distinct', 'creation', 'suffering']
           ,['tree', 'as;f,d', 'sdafsdfasdfasdfsdfsdfsd']
           ]
    
    mymodel = TableModel(data)
    app.table.setModel(mymodel)
    app.show()
    sys.exit(exe.exec_())
