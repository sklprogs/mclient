#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt5
import PyQt5.QtWidgets


class Table(PyQt5.QtWidgets.QMainWindow):
    
    def __init__(self):
        PyQt5.QtWidgets.QMainWindow.__init__(self)
        self.set_gui()
    
    def set_cell_bg(self,cell,bg):
        # 'cell' is QTableWidgetItem
        cell.setBackground(PyQt5.QtGui.QBrush(PyQt5.QtGui.QColor(bg)))
    
    def get_cell(self,rowno,colno):
        return self.table.item(rowno,colno)
    
    def enter_cell(self,action):
        self.table.cellEntered.connect(action)
    
    def show(self):
        self.showMaximized()
    
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
    
    def set_title(self,title):
        self.setWindowTitle(title)
    
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
        self.qwidget = PyQt5.QtWidgets.QWidget(self)
        self.setCentralWidget(self.qwidget)
        self.layout = PyQt5.QtWidgets.QGridLayout()
        self.qwidget.setLayout(self.layout)
        self.table = PyQt5.QtWidgets.QTableWidget(self)
        self.hheader = self.table.horizontalHeader()
        self.vheader = self.table.verticalHeader()
    
    def bind(self,hotkey,action):
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence(hotkey),self).activated.connect(action)
    
    def clear(self,event=None):
        self.table.clear()
    
    def set_cell(self,cell,rowno,colno):
        self.table.setItem(rowno,colno,cell)
    
    def add_layout(self):
        self.layout.addWidget(self.table,0,0)



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
