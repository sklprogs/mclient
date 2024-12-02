#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QVBoxLayout
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedLayout
from PyQt6.QtGui import QShortcut, QKeySequence, QCursor
from PyQt6.QtCore import pyqtSignal, QEvent, Qt

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message, rep
from skl_shared_qt.graphics.root.controller import ROOT
from skl_shared_qt.graphics.icon.controller import ICON
from skl_shared_qt.graphics.entry.controller import Entry as shEntry
from skl_shared_qt.graphics.option_menu.controller import OptionMenu
#TODO: Delete
from skl_shared_qt.graphics.entry.gui import Entry as shguiEntry
from skl_shared_qt.graphics.button.controller import Button
from skl_shared_qt.paths import PDIR

from welcome.gui import WELCOME
from table.controller import Table
from table.gui import TABLE

ICON.set(PDIR.add('..', 'resources', 'mclient.png'))


class Entry(shEntry):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gui = MinEntry()
        self.widget = self.gui.widget
        self.parent = None



class MinEntry(shguiEntry):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def set_gui(self):
        self.widget = MinEntryCore()



class MinEntryCore(QLineEdit):
    
    sig_ctrl_e = pyqtSignal()
    sig_ctrl_home = pyqtSignal()
    sig_ctrl_end = pyqtSignal()
    sig_ctrl_space = pyqtSignal()
    sig_left_arrow = pyqtSignal()
    sig_right_arrow = pyqtSignal()
    sig_home = pyqtSignal()
    sig_end = pyqtSignal()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def keyPressEvent(self, event):
        key = event.key()
        modifiers = event.modifiers()
        ''' Internal Ctrl+ bindings are not needed, so they are ignored. Other
            bindings (such as Home, End, Left and Right) must be preserved.
        '''
        if modifiers & Qt.KeyboardModifier.ControlModifier:
            if key == Qt.Key.Key_Home:
                self.sig_ctrl_home.emit()
                return
            if key == Qt.Key.Key_End:
                self.sig_ctrl_end.emit()
                return
            if key == Qt.Key.Key_E:
                self.sig_ctrl_e.emit()
                return
            if key == Qt.Key.Key_Space:
                self.sig_ctrl_space.emit()
                return
        elif key == Qt.Key.Key_Left:
            self.sig_left_arrow.emit()
        elif key == Qt.Key.Key_Right:
            self.sig_right_arrow.emit()
        elif key == Qt.Key.Key_Home:
            self.sig_home.emit()
        elif key == Qt.Key.Key_End:
            self.sig_end.emit()
        return super().keyPressEvent(event)



class TableProxy(QWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_gui()
    
    def set_gui(self):
        self.layout_ = QVBoxLayout()
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.addWidget(TABLE)
        self.setLayout(self.layout_)



class ArticleProxy(QWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active = WELCOME
        self.set_gui()
    
    def set_gui(self):
        self.layout_ = QStackedLayout()
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.addWidget(WELCOME)
        self.table = TableProxy()
        self.layout_.addWidget(self.table)
        self.setLayout(self.layout_)
    
    def is_welcome(self):
        return self.active == WELCOME
    
    def go_welcome(self):
        f = '[MClient] gui.ArticleProxy.go_welcome'
        if self.is_welcome():
            rep.lazy(f)
            return
        width = self.table.width()
        height = self.table.height()
        self.table.hide()
        self.active = WELCOME
        self.active.show()
        self.active.resize(width, height)
    
    def go_article(self):
        f = '[MClient] gui.ArticleProxy.go_article'
        if self.active == self.table:
            rep.lazy(f)
            return
        width = WELCOME.width()
        height = WELCOME.height()
        WELCOME.hide()
        self.active = self.table
        self.active.show()
        self.active.resize(width, height)



class App(QMainWindow):
    
    sig_close = pyqtSignal()
    sig_pgdn = pyqtSignal()
    sig_pgup = pyqtSignal()
    
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
        self.setWindowState(self.windowState() & ~Qt.WindowState.WindowMinimized | Qt.WindowState.WindowActive)
        self.activateWindow()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageUp:
            self.sig_pgup.emit()
        elif event.key() == Qt.Key.Key_PageDown:
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
        self.parent = QWidget()
        self.layout_ = QVBoxLayout()
        self.layout_.setContentsMargins(0, 0, 0, 0)
    
    def add_widgets(self):
        self.layout_.addWidget(objs.get_article_proxy())
        self.layout_.addWidget(objs.get_panel(), 1)
        self.parent.setLayout(self.layout_)
    
    def set_icon(self):
        # Does not accent None
        self.setWindowIcon(ICON.get())
    
    def set_gui(self):
        self.set_layout()
        self.add_widgets()
        self.setCentralWidget(self.parent)
        self.set_icon()
        self.set_styles()
    
    def set_styles(self):
        # Windows creates an irritating blue halo at the bottom of QLineEdit
        self.setStyleSheet('QLineEdit {qproperty-frame: false; border: 1px solid gray;}')
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            QShortcut(QKeySequence(hotkey), self).activated.connect(action)



class MinPanel(QWidget):

    sig_hover = pyqtSignal(QEvent)
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setMouseTracking(True)
    
    def mouseMoveEvent(self, event):
        self.sig_hover.emit(event)
        return super().mouseMoveEvent(event)



class Panel(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_values()
        self.set_gui()
    
    def set_values(self):
        self.delta = 0
        self.offset = 45
        self.pos = 0
        self.max_opt_width = 110
        self.icn_al0 = PDIR.add('..', 'resources', 'buttons'
                               ,'alphabet_off.png')
        self.icn_al1 = PDIR.add('..', 'resources', 'buttons'
                               ,'alphabet_on.png')
        self.icn_bl0 = PDIR.add('..', 'resources', 'buttons', 'block_off.png')
        self.icn_bl1 = PDIR.add('..', 'resources', 'buttons', 'block_on.png')
        self.icn_clr = PDIR.add('..', 'resources', 'buttons'
                               ,'clear_search_field.png')
        self.icn_def = PDIR.add('..', 'resources', 'buttons', 'define.png')
        self.icn_bk0 = PDIR.add('..', 'resources', 'buttons'
                               ,'go_back_off.png')
        self.icn_bk1 = PDIR.add('..', 'resources', 'buttons', 'go_back.png')
        self.icn_fw0 = PDIR.add('..', 'resources', 'buttons'
                               ,'go_next_off.png')
        self.icn_fw1 = PDIR.add('..', 'resources', 'buttons', 'go_next.png')
        self.icn_ret = PDIR.add('..', 'resources', 'buttons', 'go_search.png')
        self.icn_brw = PDIR.add('..', 'resources', 'buttons'
                               ,'open_in_browser.png')
        self.icn_ins = PDIR.add('..', 'resources', 'buttons', 'paste.png')
        self.icn_prn = PDIR.add('..', 'resources', 'buttons', 'print.png')
        self.icn_pr0 = PDIR.add('..', 'resources', 'buttons'
                               ,'priority_off.png')
        self.icn_pr1 = PDIR.add('..', 'resources', 'buttons'
                               ,'priority_on.png')
        self.icn_qit = PDIR.add('..', 'resources', 'buttons', 'quit_now.png')
        self.icn_rld = PDIR.add('..', 'resources', 'buttons', 'reload.png')
        self.icn_rp0 = PDIR.add('..', 'resources', 'buttons'
                               ,'repeat_sign_off.png')
        self.icn_rp1 = PDIR.add('..', 'resources', 'buttons'
                               ,'repeat_sign.png')
        self.icn_r20 = PDIR.add('..', 'resources', 'buttons'
                               ,'repeat_sign2_off.png')
        self.icn_r21 = PDIR.add('..', 'resources', 'buttons'
                               ,'repeat_sign2.png')
        self.icn_sav = PDIR.add('..', 'resources', 'buttons'
                               ,'save_article.png')
        self.icn_src = PDIR.add('..', 'resources', 'buttons'
                               ,'search_article.png')
        self.icn_set = PDIR.add('..', 'resources', 'buttons','settings.png')
        self.icn_abt = PDIR.add('..', 'resources', 'buttons', 'show_about.png')
        self.icn_sym = PDIR.add('..', 'resources', 'buttons'
                               ,'spec_symbol.png')
        self.icn_hst = PDIR.add('..', 'resources', 'buttons'
                               ,'toggle_history.png')
        self.icn_cp0 = PDIR.add('..', 'resources', 'buttons'
                               ,'watch_clipboard_off.png')
        self.icn_cp1 = PDIR.add('..', 'resources', 'buttons'
                               ,'watch_clipboard_on.png')
        self.icn_swp = PDIR.add('..', 'resources', 'buttons', 'swap_langs.png')
    
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
        x = QCursor().pos().x() - geom.left()
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
        self.layout_ = QHBoxLayout()
        self.layout_.setContentsMargins(4, 4, 4, 4)
        self.ent_src = Entry()
        self.ent_src.set_min_width(96)
        # A button for newbies, substitutes Enter in search_field
        self.btn_trn = Button(hint = _('Translate'), inactive = self.icn_ret
                             ,active = self.icn_ret)
        # A button to clear the search field
        self.btn_clr = Button(hint = _('Clear search field')
                             ,inactive = self.icn_clr, active = self.icn_clr)
        # A button to insert text into the search field
        self.btn_ins = Button(hint = _('Paste text from clipboard')
                             ,inactive = self.icn_ins, active = self.icn_ins)
        # A button to insert a current search
        self.btn_rp1 = Button(hint = _('Paste current request')
                             ,inactive = self.icn_rp0, active = self.icn_rp1)
        # A button to insert a previous search
        self.btn_rp2 = Button(hint = _('Paste previous request')
                             ,inactive = self.icn_r20, active = self.icn_r21)
        # A button to insert special symbols
        self.btn_sym = Button(inactive = self.icn_sym, active = self.icn_sym)
        # Drop-down list with dictionary sources
        self.opt_src = OptionMenu()
        # Drop-down lists with languages
        self.opt_lg1 = OptionMenu()
        self.btn_swp = Button(inactive = self.icn_swp, active = self.icn_swp)
        self.opt_lg2 = OptionMenu()
        self.opt_col = OptionMenu(range(1, 11), 5)
        # A settings button
        self.btn_set = Button(inactive = self.icn_set, active = self.icn_set)
        # A button to toggle subject blocking
        self.btn_blk = Button(inactive = self.icn_bl0, active = self.icn_bl1)
        # A button to toggle subject prioritization
        self.btn_pri = Button(inactive = self.icn_pr0, active = self.icn_pr1)
        # A button to toggle subject alphabetization
        self.btn_alp = Button(inactive = self.icn_al0, active = self.icn_al1)
        # A button to move to the previous article
        self.btn_prv = Button(inactive = self.icn_bk0, active = self.icn_bk1)
        # A button to move to the next article
        self.btn_nxt = Button(inactive = self.icn_fw0, active = self.icn_fw1)
        # A button to toggle and clear history
        self.btn_hst = Button(inactive = self.icn_hst, active = self.icn_hst)
        # A button to reload the article
        self.btn_rld = Button(inactive = self.icn_rld, active = self.icn_rld)
        # A button to search within the article
        self.btn_ser = Button(inactive = self.icn_src, active = self.icn_src)
        # A button to save the article
        self.btn_sav = Button(inactive = self.icn_sav, active = self.icn_sav)
        # A button to open the current article in a browser
        self.btn_brw = Button(inactive = self.icn_brw, active = self.icn_brw)
        # A button to print the article
        self.btn_prn = Button(inactive = self.icn_prn, active = self.icn_prn)
        # A button to define a term
        self.btn_def = Button(inactive = self.icn_def, active = self.icn_def)
        # A button to toggle capturing Ctrl-c-c and Ctrl-Ins-Ins
        self.btn_cap = Button(hint = _('Capture Ctrl-c-c and Ctrl-Ins-Ins')
                             ,inactive = self.icn_cp0, active = self.icn_cp1)
        # A button to show info about the program
        self.btn_abt = Button(inactive = self.icn_abt, active = self.icn_abt)
        # A button to quit the program
        self.btn_qit = Button(inactive = self.icn_qit, active = self.icn_qit)
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


objs = Objects()


if __name__ == '__main__':
    import sys
    exe = QApplication(sys.argv)
    app = App()
    app.set_gui()
    
    data = [['hel<b>L</b>o', 'I Am Here', 'Hello there!']
           ,['distinct', 'creation', 'suffering']
           ,['tree', 'as;f,d', 'sdafsdfasdfasdfsdfsdfsd']]
    
    mymodel = TableModel(data)
    app.table.setModel(mymodel)
    app.show()
    sys.exit(exe.exec_())
