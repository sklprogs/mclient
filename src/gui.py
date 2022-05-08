#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import PyQt5
import PyQt5.QtWidgets

from skl_shared.localize import _
import skl_shared.shared as sh


class Button:
    
    def __init__ (self,parent,text='',action=None,width=36
                 ,height=36,movex=4,movey=4,hint='',active=''
                 ,inactive=''
                 ):
        self.Status = False
        self.parent = parent
        self.text = text
        self.action = action
        self.width = width
        self.height = height
        self.movex = movex
        self.movey = movey
        self.hint = hint
        self.active = active
        self.icon = self.inactive = inactive
        self.set_gui()
    
    def activate(self):
        if not self.Status:
            self.Status = True
            self.icon = self.active
            self.set_icon()

    def inactivate(self):
        if self.Status:
            self.Status = False
            self.icon = self.inactive
            self.set_icon()
    
    def set_hint(self):
        if self.hint:
            self.widget.setToolTip(self.hint)
    
    def resize(self):
        self.widget.resize(self.width,self.height)
    
    def move(self):
        self.widget.move(self.movex,self.movey)
    
    def set_icon(self):
        ''' Setting a button image with
            button.setStyleSheet('image: url({})'.format(path)) causes
            tooltip glitches.
        '''
        if self.icon:
            self.widget.setIcon(PyQt5.QtGui.QIcon(self.icon))
    
    def set_size(self):
        if self.width and self.height:
            self.widget.setIconSize(PyQt5.QtCore.QSize(self.width,self.height))
    
    def set_border(self):
        if self.icon:
            self.widget.setStyleSheet('border: 0px')
    
    def set_action(self):
        if self.action:
            self.widget.clicked.connect(self.action)
    
    def set_gui(self):
        self.widget = PyQt5.QtWidgets.QPushButton(self.text,self.parent)
        self.resize()
        self.move()
        self.set_icon()
        self.set_size()
        self.set_border()
        self.set_hint()
        self.set_action()



class App(PyQt5.QtWidgets.QWidget):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_gui()
    
    def show(self):
        self.showMaximized()
    
    def set_title(self,title):
        self.setWindowTitle(title)
    
    def set_gui(self):
        self.layout = PyQt5.QtWidgets.QVBoxLayout()
        self.table = Table()
        self.panel = Panel()
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.panel)
        self.setLayout(self.layout)
    
    def bind(self,hotkey,action):
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence(hotkey),self).activated.connect(action)



class Table(PyQt5.QtWidgets.QWidget):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_gui()
    
    def set_cell_bg(self,cell,bg):
        # 'cell' is QTableWidgetItem
        cell.setBackground(PyQt5.QtGui.QBrush(PyQt5.QtGui.QColor(bg)))
    
    def get_cell(self,rowno,colno):
        return self.table.item(rowno,colno)
    
    def enter_cell(self,action):
        self.table.cellEntered.connect(action)
    
    def set_family(self,ifont,family):
        ifont.setFamily(family)
    
    def get_new_cell(self,text):
        return PyQt5.QtWidgets.QTableWidgetItem(text)
    
    def set_font(self,widget,ifont):
        widget.setFont(ifont)
    
    def align_top(self,widget):
        widget.setTextAlignment(PyQt5.QtCore.Qt.AlignTop)
    
    def get_term_cell(self,text):
        cell = self.get_new_cell(text)
        self.set_font(cell,objs.get_term_font())
        self.set_family(objs.term_font,'Serif')
        self.align_top(cell)
        return cell
    
    def set_col_width(self,no,width):
        self.table.setColumnWidth(no,width)
    
    def set_row_width(self,no,width):
        self.table.setRowWidth(no,width)
    
    def set_row_num(self,num):
        self.table.setRowCount(num)
    
    def set_col_num(self,num):
        self.table.setColumnCount(num)
    
    def show_grid(self,Show=True):
        self.table.setShowGrid(Show)
    
    def set_max_row_height(self,height):
        self.vheader.setMaximumSectionSize(height)
    
    def resize_fixed(self):
        # A temporary solution
        self.vheader.setSectionResizeMode(PyQt5.QtWidgets.QHeaderView.ResizeToContents)
    
    def hide_x_header(self):
        self.hheader.hide()
    
    def hide_y_header(self):
        self.vheader.hide()
    
    def set_gui(self):
        self.layout = PyQt5.QtWidgets.QGridLayout()
        self.setLayout(self.layout)
        self.table = PyQt5.QtWidgets.QTableWidget(self)
        self.hheader = self.table.horizontalHeader()
        self.vheader = self.table.verticalHeader()
        # This is required to activate mouse hovering
        self.table.setMouseTracking(True)
    
    def clear(self,event=None):
        self.table.clear()
    
    def set_cell(self,cell,rowno,colno):
        self.table.setItem(rowno,colno,cell)
    
    def add_layout(self):
        self.layout.addWidget(self.table,0,0)



class Panel(PyQt5.QtWidgets.QWidget):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_values()
        self.set_gui()
        self.set_delta()
    
    def set_values(self):
        self.offset = 10
        self.pos = 0
        self.icn_al0 = sh.objs.get_pdir().add ('..','resources'
                                              ,'buttons'
                                              ,'alphabet_off.svgz'
                                              )
        self.icn_al1 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'alphabet_on.svgz'
                                        )
        self.icn_bl0 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'block_off.svgz'
                                        )
        self.icn_bl1 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'block_on.svgz'
                                        )
        self.icn_clr = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'clear_search_field.svgz'
                                        )
        self.icn_def = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'define.png'
                                        )
        self.icn_bk0 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'go_back_off.svgz'
                                        )
        self.icn_bk1 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'go_back.svgz'
                                        )
        self.icn_fw0 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'go_forward_off.svgz'
                                        )
        self.icn_fw1 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'go_forward.svgz'
                                        )
        self.icn_ret = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'go_search.svgz'
                                        )
        self.icn_brw = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'open_in_browser.svgz'
                                        )
        self.icn_ins = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'paste.svgz'
                                        )
        self.icn_prn = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'print.svgz'
                                        )
        self.icn_pr0 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'priority_off.svgz'
                                        )
        self.icn_pr1 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'priority_on.png'
                                        )
        self.icn_qit = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'quit_now.svgz'
                                        )
        self.icn_rld = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'reload.svgz'
                                        )
        self.icn_rp0 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'repeat_sign_off.svgz'
                                        )
        self.icn_rp1 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'repeat_sign.svgz'
                                        )
        self.icn_r20 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'repeat_sign2_off.svgz'
                                        )
        self.icn_r21 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'repeat_sign2.svgz'
                                        )
        self.icn_sav = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'save_article.svgz'
                                        )
        self.icn_src = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'search_article.svgz'
                                        )
        self.icn_set = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'settings.svgz'
                                        )
        self.icn_abt = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'show_about.svgz'
                                        )
        self.icn_sym = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'spec_symbol.svgz'
                                        )
        self.icn_hst = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'toggle_history.svgz'
                                        )
        self.icn_hor = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'toggle_view_hor.svgz'
                                        )
        self.icn_ver = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'toggle_view_ver.svgz'
                                        )
        self.icn_cp0 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'watch_clipboard_off.svgz'
                                        )
        self.icn_cp1 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'watch_clipboard_on.svgz'
                                        )
        self.icn_swp = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'swap_langs.svgz'
                                        )
    
    def set_delta(self):
        # Set a delta value between a label size and a main widget size
        self.delta = self.geometry().width() - self.label.geometry().width()
    
    def slide_left(self):
        if self.label.geometry().x() - self.offset >= self.delta:
            self.pos -= self.offset
            self.label.move(self.pos,0)
    
    def slide_right(self):
        if self.label.geometry().x() + self.offset <= 0:
            self.pos += self.offset
            self.label.move(self.pos,0)
    
    def trigger_hover(self,event):
        ''' We shouldn't use event.x since this returns x relative to
            the widget that caused the event, and this is widget will be
            any we have mouse over.
        '''
        geom = self.parent.geometry()
        x = PyQt5.QtGui.QCursor().pos().x() - geom.left()
        width = geom.width()
        if 0 <= x <= 30:
            self.slide_right()
        elif width - 30 <= x <= width:
            self.slide_left()
    
    def eventFilter(self,source,event):
        if event.type() == PyQt5.QtCore.QEvent.MouseMove:
            self.trigger_hover(event)
        return super().eventFilter(source,event)
    
    def set_hint_bg(self):
        self.setStyleSheet('QPushButton:hover {background-color: white} QToolTip {background-color: #ffffe0}')
    
    def set_widgets(self):
        self.label = PyQt5.QtWidgets.QLabel(self)
        # A button for newbies, substitutes Enter in search_field
        self.btn_trn = Button (parent = self.label
                                 ,hint = _('Translate')
                                 ,inactive = self.icn_ret
                                 ,active = self.icn_ret
                                 ,movex = 3
                                 )
        # A button to clear the search field
        self.btn_clr = Button (parent = self.label
                                 ,hint = _('Clear search field')
                                 ,inactive = self.icn_clr
                                 ,active = self.icn_clr
                                 ,movex = 42
                                 )
        # A button to insert text into the search field
        self.btn_ins = Button (parent = self.label
                                 ,hint = _('Paste text from clipboard')
                                 ,inactive = self.icn_ins
                                 ,active = self.icn_ins
                                 ,movex = 81
                                 )
        # A button to insert a current search
        self.btn_rp1 = Button (parent = self.label
                                 ,hint = _('Paste current request')
                                 ,inactive = self.icn_rp0
                                 ,active = self.icn_rp1
                                 ,movex = 120
                                 )
        # A button to insert a previous search
        self.btn_rp2 = Button (parent = self.label
                                 ,hint = _('Paste previous request')
                                 ,inactive = self.icn_r20
                                 ,active = self.icn_r21
                                 ,movex = 159
                                 )
        # A button to insert special symbols
        self.btn_sym = Button (parent = self.label
                                 ,hint = _('Paste a special symbol')
                                 ,inactive = self.icn_sym
                                 ,active = self.icn_sym
                                 ,movex = 198
                                 )
        '''
        self.opt_src = sh.OptionMenu (parent = self.label
                                     ,Combo = True
                                     ,font = 'Sans 11'
                                     )
        '''
        ''' Configure the option menu at the GUI creation time to avoid
            glitches with the search field.
        '''
        '''
        self.opt_src.widget.configure (width = 14
                                      ,font = 'Sans 11'
                                      )
        # Drop-down lists with languages
        self.opt_lg1 = sh.OptionMenu (parent = self.label
                                     ,Combo = True
                                     ,font = 'Sans 11'
                                     )
        '''
        self.btn_swp = Button (parent = self.label
                                 ,hint = _('Swap source and target languages')
                                 ,inactive = self.icn_swp
                                 ,active = self.icn_swp
                                 ,movex = 237
                                 )
        '''
        self.opt_lg2 = sh.OptionMenu (parent = self.label
                                     ,Combo = True
                                     ,font = 'Sans 11'
                                     )
        self.opt_col = sh.OptionMenu (parent = self.label
                                     ,items = (1,2,3,4,5,6,7,8,9,10)
                                     ,default = 4
                                     ,Combo = True
                                     ,font = 'Sans 11'
                                     )
        '''
        ''' The 'height' argument changes a height of the drop-down
            list and not the main widget.
        '''
        '''
        self.opt_lg1.widget.config (width = 11
                                   ,height = 15
                                   )
        self.opt_lg2.widget.config (width = 11
                                   ,height = 15
                                   )
        self.opt_col.widget.config(width=2)
        '''
        # A settings button
        self.btn_set = Button (parent = self.label
                                 ,hint = _('Tune up view settings')
                                 ,inactive = self.icn_set
                                 ,active = self.icn_set
                                 ,movex = 276
                                 )
        # A button to toggle subject blocking
        self.btn_blk = Button (parent = self.label
                                 ,hint = _('Configure blacklisting')
                                 ,inactive = self.icn_bl0
                                 ,active = self.icn_bl1
                                 ,movex = 315
                                 )
        # A button to toggle subject prioritization
        self.btn_pri = Button (parent = self.label
                                 ,hint = _('Configure prioritization')
                                 ,inactive = self.icn_pr0
                                 ,active = self.icn_pr1
                                 ,movex = 354
                                 )
        # A button to toggle subject alphabetization
        self.btn_alp = Button (parent = self.label
                                 ,hint = _('Toggle alphabetizing')
                                 ,inactive = self.icn_al0
                                 ,active = self.icn_al1
                                 ,movex = 393
                                 )
        # A button to change the article view
        self.btn_viw = Button (parent = self.label
                                 ,hint = _('Toggle the article view mode')
                                 ,inactive = self.icn_ver
                                 ,active = self.icn_hor
                                 ,movex = 432
                                 )
        # A button to move to the previous article
        self.btn_prv = Button (parent = self.label
                                 ,hint = _('Go to the preceding article')
                                 ,inactive = self.icn_bk0
                                 ,active = self.icn_bk1
                                 ,movex = 471
                                 )
        # A button to move to the next article
        self.btn_nxt = Button (parent = self.label
                                 ,hint = _('Go to the following article')
                                 ,inactive = self.icn_fw0
                                 ,active = self.icn_fw1
                                 ,movex = 510
                                 )
        # A button to toggle and clear history
        self.btn_hst = Button (parent = self.label
                                 ,hint = _('Toggle history')
                                 ,inactive = self.icn_hst
                                 ,active = self.icn_hst
                                 ,movex = 549
                                 )
        # A button to reload the article
        self.btn_rld = Button (parent = self.label
                                 ,hint = _('Reload the article')
                                 ,inactive = self.icn_rld
                                 ,active = self.icn_rld
                                 ,movex = 588
                                 )
        # A button to search within the article
        self.btn_ser = Button (parent = self.label
                                 ,hint = _('Find in the current article')
                                 ,inactive = self.icn_src
                                 ,active = self.icn_src
                                 ,movex = 627
                                 )
        # A button to save the article
        self.btn_sav = Button (parent = self.label
                                 ,hint = _('Save the current article')
                                 ,inactive = self.icn_sav
                                 ,active = self.icn_sav
                                 ,movex = 666
                                 )
        # A button to open the current article in a browser
        self.btn_brw = Button (parent = self.label
                                 ,hint = _('Open the current article in a browser')
                                 ,inactive = self.icn_brw
                                 ,active = self.icn_brw
                                 ,movex = 705
                                 )
        # A button to print the article
        self.btn_prn = Button (parent = self.label
                                 ,hint = _('Create a print-ready preview')
                                 ,inactive = self.icn_prn
                                 ,active = self.icn_prn
                                 ,movex = 744
                                 )
        # A button to define a term
        self.btn_def = Button (parent = self.label
                                 ,hint = _('Define the current term')
                                 ,inactive = self.icn_def
                                 ,active = self.icn_def
                                 ,movex = 783
                                 )
        # A button to toggle capturing Ctrl-c-c and Ctrl-Ins-Ins
        self.btn_cap = Button (parent = self.label
                                 ,hint = _('Capture Ctrl-c-c and Ctrl-Ins-Ins')
                                 ,inactive = self.icn_cp0
                                 ,active = self.icn_cp1
                                 ,movex = 822
                                 )
        # A button to show info about the program
        self.btn_abt = Button (parent = self.label
                                 ,hint = _('View About')
                                 ,inactive = self.icn_abt
                                 ,active = self.icn_abt
                                 ,movex = 861
                                 )
        # A button to quit the program
        self.btn_qit = Button (parent = self.label
                                 ,hint = _('Quit the program')
                                 ,inactive = self.icn_qit
                                 ,active = self.icn_qit
                                 ,movex = 900
                                 )
    
    def set_gui(self):
        self.set_widgets()
        self.set_hint_bg()

    @PyQt5.QtCore.pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')



class Commands:
    
    def debug_memory(self,data):
        f = 'controller.Commands.debug_memory'
        if not data:
            sh.com.rep_empty(f)
            return
        #TYPE,TEXT,ROWNO,COLNO,CELLNO
        headers = (_('TYPE'),_('TEXT'),_('ROW #'),_('COLUMN #')
                  ,_('CELL #')
                  )
        mes = sh.FastTable (headers = headers
                           ,iterable = data
                           ,maxrows = 1000
                           ,maxrow = 40
                           ,Transpose = 1
                           ).run()
        sh.com.run_fast_debug(f,mes)



class Objects:
    
    def __init__(self):
        self.term_font = None
    
    def get_term_font(self):
        if self.term_font is None:
            self.term_font = PyQt5.QtGui.QFont()
            self.term_font.setFamily('Serif')
            self.term_font.setPixelSize(16)
        return self.term_font


com = Commands()
objs = Objects()


if __name__ == '__main__':
    f = 'controller.__main__'
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    db = DB()
    data = db.fetch()
    rownum = db.get_max_row_no()
    colnum = db.get_max_col_no()
    if rownum is not None:
        rownum += 1
    if colnum is not None:
        colnum += 1
    icells = Cells()
    icells.reset(data)
    #icells.debug()
    #com.debug_memory(data)
    itable = Table()
    itable.reset(icells.cells,rownum,colnum)
    itable.set_gui()
    itable.fill()
    #itable.show()
    itable.showMaximized()
    sys.exit(app.exec())
    db.close()
