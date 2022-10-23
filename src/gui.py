#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt5
import PyQt5.QtWidgets

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class TableModel(PyQt5.QtCore.QAbstractTableModel):
    
    def __init__(self,datain,parent=None,*args):
        PyQt5.QtCore.QAbstractTableModel.__init__(self,parent,*args)
        self.arraydata = datain

    def rowCount(self,parent):
        return len(self.arraydata)

    def columnCount(self,parent):
        return len(self.arraydata[0])

    def data(self,index,role):
        f = '[MClientQt] gui.TableModel.data'
        if not index.isValid():
            return PyQt5.QtCore.QVariant()
        if role == PyQt5.QtCore.Qt.DisplayRole:
            try:
                return PyQt5.QtCore.QVariant(self.arraydata[index.row()][index.column()])
            except Exception as e:
                mes = _('List out of bounds at row #{}, column #{}!')
                mes = mes.format(index.row(),index.column())
                sh.objs.get_mes(f,mes,True).show_warning()
                return PyQt5.QtCore.QVariant()
    
    def update(self,index_):
        self.dataChanged.emit(index_,index_)



class TableDelegate(PyQt5.QtWidgets.QStyledItemDelegate):
    # akej74, https://stackoverflow.com/questions/35397943/how-to-make-a-fast-qtableview-with-html-formatted-and-clickable-cells
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.index = None
    
    def set_line_spacing(self,doc):
        f = '[MClient] gui.TableDelegate.set_line_spacing'
        cursor = PyQt5.QtGui.QTextCursor(doc)
        block = doc.firstBlock()
        if not block.isValid():
            mes = _('Wrong input data!')
            sh.objs.get_mes(f,mes,True).show_debug()
            return
        format_ = block.blockFormat()
        format_.setLineHeight(19,2)
        cursor.setBlockFormat(format_)
    
    def paint(self,painter,option,index):
        f = '[MClientQt] gui.TableDelegate.paint'
        # index:   PyQt5.QtCore.QModelIndex
        # painter: PyQt5.QtGui.QPainter
        # option:  PyQt5.QtWidgets.QStyleOptionViewItem
        options = PyQt5.QtWidgets.QStyleOptionViewItem(option)
        self.initStyleOption(options,index)
        
        if options.widget:
            style = options.widget.style()
        else:
            style = PyQt5.QtWidgets.QApplication.style()
        
        doc = PyQt5.QtGui.QTextDocument()
        doc.setHtml(options.text)
        options.text = ''
        
        self.set_line_spacing(doc)
        
        # This enables text wrapping in the delegate
        doc.setTextWidth(options.rect.width())
        
        style.drawControl(PyQt5.QtWidgets.QStyle.CE_ItemViewItem,options,painter)
        ctx = PyQt5.QtGui.QAbstractTextDocumentLayout.PaintContext()
        
        textRect = style.subElementRect(PyQt5.QtWidgets.QStyle.SE_ItemViewItemText,options)
        
        if self.index is None:
            mes = _('Index must be set externally!')
            sh.objs.get_mes(f,mes,True).show_error()
        elif index == self.index:
            color = PyQt5.QtGui.QColor('red')
            pen = PyQt5.QtGui.QPen(color,2)
            painter.setPen(pen)
            # Avoid intersecting cell borders and artifacts as the result
            x1, y1, x2, y2 = option.rect.getCoords()
            option.rect.setCoords(x1+1,y1+1,x2-1,y2-1)
            painter.drawRect(option.rect)
        
        painter.save()
    
        painter.translate(textRect.topLeft())
        # Hide too long text; do not allow cells to overlap
        painter.setClipRect(textRect.translated(-textRect.topLeft()))
        doc.documentLayout().draw(painter,ctx)
    
        painter.restore()
    
    def sizeHint(self,option,index):
        options = PyQt5.QtWidgets.QStyleOptionViewItem(option)
        self.initStyleOption(options,index)
        
        doc = PyQt5.QtGui.QTextDocument()
        doc.setHtml(options.text)
        doc.setTextWidth(options.rect.width())
        
        return PyQt5.QtCore.QSize(doc.idealWidth(),doc.size().height())



class Table(PyQt5.QtWidgets.QTableView):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.select = None
        self.click_left = None
        self.click_right = None
        self.click_middle = None
        self.click_left_arrow = None
        self.click_right_arrow = None
        self.set_gui()
    
    def get_cell_hint(self,index_):
        option = PyQt5.QtWidgets.QStyleOptionViewItem()
        return self.delegate.sizeHint(option,index_).height()
    
    def scroll2index(self,index_):
        self.scrollTo(index_,PyQt5.QtWidgets.QAbstractItemView.PositionAtTop)
    
    def get_col_by_x(self,x):
        return self.columnAt(x)
    
    def get_row_by_y(self,y):
        return self.rowAt(y)
    
    def get_row_hint(self,rowno):
        return self.sizeHintForRow(rowno)
    
    def get_row_height(self,rowno):
        return self.rowHeight(rowno)
    
    def get_row_y(self,rowno):
        return self.rowViewportPosition(rowno)
    
    def get_row(self,index_):
        return index_.row()
    
    def get_column(self,index_):
        return index_.column()
    
    def set_index(self,index_):
        self.setCurrentIndex(index_)
        self.delegate.index = index_
    
    def get_index(self):
        return self.currentIndex()
    
    def get_cell(self):
        index_ = self.currentIndex()
        return(index_.row(),index_.column())
    
    def get_height(self):
        return self.height()
    
    def get_cell_x(self,colno):
        return self.columnViewportPosition(colno)
    
    def get_cell_y(self,rowno):
        return self.rowViewportPosition(rowno)
    
    def set_model(self,mymodel):
        # Do not overwrite built-in 'model'
        self.mymodel = mymodel
        self.setModel(mymodel)
    
    def _use_mouse(self,event):
        pos = event.pos()
        rowno = self.rowAt(pos.y())
        colno = self.columnAt(pos.x())
        index_ = self.mymodel.index(rowno,colno)
        self.set_index(index_)
    
    def _report_external(self):
        f = '[MClientQt] gui.Table._report_external'
        mes = _('An external function is required!')
        sh.objs.get_mes(f,mes,True).show_error()
    
    def eventFilter(self,widget,event):
        ''' #NOTE: Return True for matches only, otherwise the app will freeze!
            Qt accepts boolean at output, but not NoneType.
        '''
        type_ = event.type()
        if type_ == PyQt5.QtCore.QEvent.MouseMove:
            if not self.select:
                self._report_external()
                return False
            self._use_mouse(event)
            return True
        elif type_ == PyQt5.QtCore.QEvent.MouseButtonPress:
            button = event.button()
            if button == PyQt5.QtCore.Qt.LeftButton:
                if self.click_left:
                    self._use_mouse(event)
                    self.click_left()
                else:
                    self._report_external()
                return True
            elif button == PyQt5.QtCore.Qt.RightButton:
                if self.click_right:
                    self._use_mouse(event)
                    self.click_right()
                else:
                    self._report_external()
                return True
            elif button == PyQt5.QtCore.Qt.MiddleButton:
                if self.click_middle:
                    self._use_mouse(event)
                    self.click_middle()
                else:
                    self._report_external()
                return True
            elif button == PyQt5.QtCore.Qt.Qt_Left:
                if self.click_left_arrow:
                    self.click_left_arrow()
                else:
                    self._report_external()
                return True
            elif button == PyQt5.QtCore.Qt.Qt_Right:
                if self.click_right_arrow:
                    self.click_right_arrow()
                else:
                    self._report_external()
                return True
        return False
    
    def set_col_width(self,no,width):
        self.setColumnWidth(no,width)
    
    def set_row_height(self,no,height):
        self.setRowHeight(no,height)
    
    def set_max_row_height(self,height):
        self.vheader.setMaximumSectionSize(height)
    
    def set_gui(self):
        self.delegate = TableDelegate()
        self.setItemDelegate(self.delegate)
        self.hheader = self.horizontalHeader()
        self.vheader = self.verticalHeader()
        self.hheader.setVisible(False)
        self.vheader.setVisible(False)
        self.setStyleSheet('QTableView { selection-background-color: white; }')
    
    def show_borders(self,Show=False):
        self.setShowGrid(Show)
    
    def clear(self):
        pass



class App(PyQt5.QtWidgets.QMainWindow):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    
    def get_height(self):
        return self.height()
    
    def get_width(self):
        return self.width()
    
    def minimize(self):
        self.showMinimized()
    
    def show(self):
        self.showMaximized()
    
    def set_title(self,title):
        self.setWindowTitle(title)
    
    def set_layout(self):
        self.parent = PyQt5.QtWidgets.QWidget()
        self.layout = PyQt5.QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
    
    def add_widgets(self):
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.panel,1)
        self.parent.setLayout(self.layout)
    
    def set_gui(self,table=None,panel=None):
        self.set_layout()
        if table:
            self.table = table
        else:
            self.table = Table()
        if panel:
            self.panel = panel
        else:
            self.panel = Panel()
        self.add_widgets()
        self.setCentralWidget(self.parent)
    
    def bind(self,hotkey,action):
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence(hotkey),self).activated.connect(action)



class Panel(PyQt5.QtWidgets.QWidget):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_values()
        self.set_gui()
    
    def set_values(self):
        self.delta = 0
        self.offset = 10
        self.pos = 0
        self.icn_al0 = sh.objs.get_pdir().add ('..','resources'
                                              ,'buttons'
                                              ,'alphabet_off.png'
                                              )
        self.icn_al1 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'alphabet_on.png'
                                        )
        self.icn_bl0 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'block_off.png'
                                        )
        self.icn_bl1 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'block_on.png'
                                        )
        self.icn_clr = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'clear_search_field.png'
                                        )
        self.icn_def = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'define.png'
                                        )
        self.icn_bk0 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'go_back_off.png'
                                        )
        self.icn_bk1 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'go_back.png'
                                        )
        self.icn_fw0 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'go_forward_off.png'
                                        )
        self.icn_fw1 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'go_forward.png'
                                        )
        self.icn_ret = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'go_search.png'
                                        )
        self.icn_brw = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'open_in_browser.png'
                                        )
        self.icn_ins = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'paste.png'
                                        )
        self.icn_prn = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'print.png'
                                        )
        self.icn_pr0 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'priority_off.png'
                                        )
        self.icn_pr1 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'priority_on.png'
                                        )
        self.icn_qit = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'quit_now.png'
                                        )
        self.icn_rld = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'reload.png'
                                        )
        self.icn_rp0 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'repeat_sign_off.png'
                                        )
        self.icn_rp1 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'repeat_sign.png'
                                        )
        self.icn_r20 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'repeat_sign2_off.png'
                                        )
        self.icn_r21 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'repeat_sign2.png'
                                        )
        self.icn_sav = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'save_article.png'
                                        )
        self.icn_src = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'search_article.png'
                                        )
        self.icn_set = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'settings.png'
                                        )
        self.icn_abt = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'show_about.png'
                                        )
        self.icn_sym = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'spec_symbol.png'
                                        )
        self.icn_hst = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'toggle_history.png'
                                        )
        self.icn_hor = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'toggle_view_hor.png'
                                        )
        self.icn_ver = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'toggle_view_ver.png'
                                        )
        self.icn_cp0 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'watch_clipboard_off.png'
                                        )
        self.icn_cp1 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'watch_clipboard_on.png'
                                        )
        self.icn_swp = sh.objs.pdir.add ('..','resources','buttons'
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
            self.panel.move(self.pos,0)
    
    def slide_right(self):
        if self.panel.x() + self.offset <= 0:
            self.pos += self.offset
            self.panel.move(self.pos,0)
    
    def trigger_hover(self,event):
        ''' We should not use event.x since this returns x relative to the
            widget that caused the event, and this widget will be any we have
            mouse over.
        '''
        self.set_delta()
        geom = self.geometry()
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
        self.setMaximumHeight(44)
        self.panel = PyQt5.QtWidgets.QWidget(self)
        self.layout = PyQt5.QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(4,4,4,4)
        self.ent_src = sh.Entry()
        self.ent_src.set_min_width(105)
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
        self.btn_sym = sh.Button (hint = _('Paste a special symbol')
                                 ,inactive = self.icn_sym
                                 ,active = self.icn_sym
                                 )
        # Drop-down list with dictionary sources
        self.opt_src = sh.OptionMenu()
        # Drop-down lists with languages
        self.opt_lg1 = sh.OptionMenu()
        self.btn_swp = sh.Button (hint = _('Swap source and target languages')
                                 ,inactive = self.icn_swp
                                 ,active = self.icn_swp
                                 )
        self.opt_lg2 = sh.OptionMenu()
        self.opt_col = sh.OptionMenu()
        # A settings button
        self.btn_set = sh.Button (hint = _('Tune up view settings')
                                 ,inactive = self.icn_set
                                 ,active = self.icn_set
                                 )
        # A button to toggle subject blocking
        self.btn_blk = sh.Button (hint = _('Configure blacklisting')
                                 ,inactive = self.icn_bl0
                                 ,active = self.icn_bl1
                                 )
        # A button to toggle subject prioritization
        self.btn_pri = sh.Button (hint = _('Configure prioritization')
                                 ,inactive = self.icn_pr0
                                 ,active = self.icn_pr1
                                 )
        # A button to toggle subject alphabetization
        self.btn_alp = sh.Button (hint = _('Toggle alphabetizing')
                                 ,inactive = self.icn_al0
                                 ,active = self.icn_al1
                                 )
        # A button to change the article view
        self.btn_viw = sh.Button (hint = _('Toggle the article view mode')
                                 ,inactive = self.icn_ver
                                 ,active = self.icn_hor
                                 )
        # A button to move to the previous article
        self.btn_prv = sh.Button (hint = _('Go to the preceding article')
                                 ,inactive = self.icn_bk0
                                 ,active = self.icn_bk1
                                 )
        # A button to move to the next article
        self.btn_nxt = sh.Button (hint = _('Go to the following article')
                                 ,inactive = self.icn_fw0
                                 ,active = self.icn_fw1
                                 )
        # A button to toggle and clear history
        self.btn_hst = sh.Button (hint = _('Toggle history')
                                 ,inactive = self.icn_hst
                                 ,active = self.icn_hst
                                 )
        # A button to reload the article
        self.btn_rld = sh.Button (hint = _('Reload the article')
                                 ,inactive = self.icn_rld
                                 ,active = self.icn_rld
                                 )
        # A button to search within the article
        self.btn_ser = sh.Button (hint = _('Find in the current article')
                                 ,inactive = self.icn_src
                                 ,active = self.icn_src
                                 )
        # A button to save the article
        self.btn_sav = sh.Button (hint = _('Save the current article')
                                 ,inactive = self.icn_sav
                                 ,active = self.icn_sav
                                 )
        # A button to open the current article in a browser
        self.btn_brw = sh.Button (hint = _('Open the current article in a browser')
                                 ,inactive = self.icn_brw
                                 ,active = self.icn_brw
                                 )
        # A button to print the article
        self.btn_prn = sh.Button (hint = _('Create a print-ready preview')
                                 ,inactive = self.icn_prn
                                 ,active = self.icn_prn
                                 )
        # A button to define a term
        self.btn_def = sh.Button (hint = _('Define the current term')
                                 ,inactive = self.icn_def
                                 ,active = self.icn_def
                                 )
        # A button to toggle capturing Ctrl-c-c and Ctrl-Ins-Ins
        self.btn_cap = sh.Button (hint = _('Capture Ctrl-c-c and Ctrl-Ins-Ins')
                                 ,inactive = self.icn_cp0
                                 ,active = self.icn_cp1
                                 )
        # A button to show info about the program
        self.btn_abt = sh.Button (hint = _('View About')
                                 ,inactive = self.icn_abt
                                 ,active = self.icn_abt
                                 )
        # A button to quit the program
        self.btn_qit = sh.Button (hint = _('Quit the program')
                                 ,action = self.close
                                 ,inactive = self.icn_qit
                                 ,active = self.icn_qit
                                 )
        self.layout.addWidget(self.ent_src.widget)
        self.layout.addWidget(self.btn_trn.widget)
        self.layout.addWidget(self.btn_clr.widget)
        self.layout.addWidget(self.btn_ins.widget)
        self.layout.addWidget(self.btn_rp1.widget)
        self.layout.addWidget(self.btn_rp2.widget)
        self.layout.addWidget(self.btn_sym.widget)
        self.layout.addWidget(self.opt_src.widget)
        self.layout.addWidget(self.opt_lg1.widget)
        self.layout.addWidget(self.btn_swp.widget)
        self.layout.addWidget(self.opt_lg2.widget)
        self.layout.addWidget(self.opt_col.widget)
        self.layout.addWidget(self.btn_set.widget)
        self.layout.addWidget(self.btn_blk.widget)
        self.layout.addWidget(self.btn_pri.widget)
        self.layout.addWidget(self.btn_alp.widget)
        self.layout.addWidget(self.btn_viw.widget)
        self.layout.addWidget(self.btn_prv.widget)
        self.layout.addWidget(self.btn_nxt.widget)
        self.layout.addWidget(self.btn_hst.widget)
        self.layout.addWidget(self.btn_rld.widget)
        self.layout.addWidget(self.btn_ser.widget)
        self.layout.addWidget(self.btn_sav.widget)
        self.layout.addWidget(self.btn_brw.widget)
        self.layout.addWidget(self.btn_prn.widget)
        self.layout.addWidget(self.btn_def.widget)
        self.layout.addWidget(self.btn_cap.widget)
        self.layout.addWidget(self.btn_abt.widget)
        self.layout.addWidget(self.btn_qit.widget)
        self.panel.setLayout(self.layout)
    
    def set_gui(self):
        self.set_widgets()
        self.set_hint_bg()
        self.show()

    @PyQt5.QtCore.pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')


if __name__ == '__main__':
    import sys
    exe = PyQt5.QtWidgets.QApplication(sys.argv)
    app = App()
    app.set_gui()
    
    data = [['hel<b>L</b>o','I Am Here','Hello there!']
           ,['distinct','creation','suffering']
           ,['tree','as;f,d','sdafsdfasdfasdfsdfsdfsd']
           ]
    
    mymodel = TableModel(data)
    app.table.setModel(mymodel)
    app.show()
    sys.exit(exe.exec_())
