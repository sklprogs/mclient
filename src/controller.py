#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import sqlite3
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication,QMainWindow,QGridLayout \
                           ,QWidget,QTableWidget,QTableWidgetItem \
                           ,QHeaderView,QShortcut
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QKeySequence
from skl_shared.localize import _
import skl_shared.shared as sh


class Cell:
    
    def __init__(self,text,rowno,colno,cellno):
        self.text = text
        self.rowno = rowno
        self.colno = colno
        self.cellno = cellno



class DB:
    
    def __init__(self):
        self.set_values()
        self.db = sqlite3.connect(self.path)
        self.dbc = self.db.cursor()
    
    def set_values(self):
        self.artid = 0
        self.Selectable = True
        self.path = '/home/pete/tmp/set.db'
    
    def fetch(self):
        query = 'select TYPE,TEXT,ROWNO,COLNO,CELLNO from BLOCKS \
                 where BLOCK = 0 and IGNORE = 0 order by CELLNO,NO'
        self.dbc.execute(query,)
        return self.dbc.fetchall()
    
    def close(self):
        f = 'controller.DB.close'
        mes = _('Close "{}"').format(self.path)
        sh.objs.get_mes(f,mes,True).show_info()
        self.dbc.close()
    
    def get_max_col_no(self):
        ''' This is a less advanced alternative to 'self.get_max_col'
            for cases when positions are not set yet.
        '''
        f = 'controller.DB.get_max_col_no'
        query = 'select COLNO from BLOCKS where BLOCK = 0 and \
                        IGNORE = 0 order by COLNO desc'
        self.dbc.execute(query,)
        col_no = self.dbc.fetchone()
        if col_no:
            return col_no[0]
    
    def get_max_row_no(self):
        f = 'controller.DB.get_max_row_no'
        query = 'select ROWNO from BLOCKS where BLOCK = 0 \
                 and IGNORE = 0 order by ROWNO desc'
        self.dbc.execute(query,)
        result = self.dbc.fetchone()
        if result:
            return result[0]



class Cells:
    
    def __init__(self):
        self.cells = []
    
    def _get(self,cellno):
        for i in range(len(self.cells)):
            if self.cells[i].cellno == cellno:
                return i
    
    def reset(self,data):
        f = 'controller.Cells.reset'
        if not data:
            sh.com.rep_empty(f)
            return
        for block in data:
            text, rowno, colno, cellno = block[1], block[2], block[3], block[4]
            i = self._get(cellno)
            if i is None:
                self.cells.append(Cell(text,rowno,colno,cellno))
            else:
                self.cells[i].text += text
    
    def debug(self):
        f = 'controller.Cells.debug'
        if not data:
            sh.com.rep_empty(f)
            return
        texts = []
        rownos = []
        colnos = []
        cellnos = []
        for cell in self.cells:
            texts.append(cell.text)
            rownos.append(cell.rowno)
            colnos.append(cell.colno)
            cellnos.append(cell.cellno)
        headers = (_('TEXT'),_('ROW #'),_('COLUMN #'),_('CELL #'))
        iterable = [texts,rownos,colnos,cellnos]
        mes = sh.FastTable (headers = headers
                           ,iterable = iterable
                           ,maxrows = 1000
                           ,maxrow = 40
                           ).run()
        sh.com.run_fast_debug(f,mes)



class Table(QMainWindow):
    
    def __init__(self):
        QMainWindow.__init__(self)
        self.set_values()
    
    def set_values(self):
        self.cells = []
        self.rowno = 0
        self.colno = 0
    
    def set_gui(self):
        f = 'controller.Table.set_gui'
        self.setWindowTitle('MClientQT')
        center = QWidget(self)
        self.setCentralWidget(center)
        self.layout = QGridLayout()
        center.setLayout(self.layout)
        self.table = QTableWidget(self)
        mes = _('Table sizes: {}x{}').format(self.rowno,self.colno)
        sh.objs.get_mes(f,mes,True).show_debug()
        self.table.setRowCount(self.rowno)
        self.table.setColumnCount(self.colno)
        self.hheader = self.table.horizontalHeader()
        #self.hheader.defaultSectionSize = 20
        self.vheader = self.table.verticalHeader()
        self.set_bindings()
    
    def set_bindings(self):
        QShortcut(QKeySequence('Ctrl+Q'),self).activated.connect(self.close)
        QShortcut(QKeySequence('Esc'),self).activated.connect(self.close)
    
    def reset(self,cells,rowno,colno):
        f = 'controller.Commands.reset'
        if not cells or not rowno or not colno:
            sh.com.rep_empty(f)
            return
        self.cells = cells
        self.rowno = rowno
        self.colno = colno
    
    def fill(self):
        f = 'controller.Commands.fill'
        timer = sh.Timer(f)
        timer.start()
        for cell in self.cells:
            table_item = QTableWidgetItem(cell.text)
            self.table.setItem(cell.rowno,cell.colno,table_item)
            table_item.setTextAlignment(QtCore.Qt.AlignTop)
            if 0 <= cell.colno < 4:
                table_item.setTextAlignment(QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.table,0,0)
        #self.hheader.setSectionResizeMode(0,QHeaderView.Interactive)
        #self.hheader.setSectionResizeMode(1,QHeaderView.Interactive)
        self.table.setColumnWidth(0,150)
        self.table.setColumnWidth(1,100)
        self.table.setColumnWidth(2,50)
        self.table.setColumnWidth(3,50)
        #self.table.resizeColumnToContents(2)
        #self.table.resizeColumnToContents(3)
        self.hheader.setSectionResizeMode(4,QHeaderView.Stretch)
        self.hheader.setSectionResizeMode(5,QHeaderView.Stretch)
        self.hheader.setSectionResizeMode(6,QHeaderView.Stretch)
        self.hheader.setSectionResizeMode(7,QHeaderView.Stretch)
        self.vheader.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.vheader.setMaximumSectionSize(50)
        timer.end()



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


com = Commands()


if __name__ == '__main__':
    f = 'controller.__main__'
    app = QApplication(sys.argv)
    db = DB()
    data = db.fetch()
    rowno = db.get_max_row_no()
    colno = db.get_max_col_no()
    if rowno is not None:
        rowno += 1
    if colno is not None:
        colno += 1
    icells = Cells()
    icells.reset(data)
    #icells.debug()
    #com.debug_memory(data)
    itable = Table()
    itable.reset(icells.cells,rowno,colno)
    itable.set_gui()
    itable.fill()
    #itable.show()
    itable.showMaximized()
    sys.exit(app.exec())
    db.close()
