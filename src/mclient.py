#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import sqlite3

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import logic as lg
import gui as gi

DEBUG = False


class Table:

    def __init__(self):
        self.set_values()
        self.logic = lg.Table()
        self.gui = gi.Table()
        self.set_gui()
    
    def set_values(self):
        self.coords = {}
        self.row_height = 42
    
    def go_url(self):
        #TODO: implement
        pass
    
    def go_keyboard(self):
        #TODO: implement
        self.go_url()
    
    def go(self,Mouse=False):
        # Process either the search string or the URL
        if Mouse:
            self.go_url()
        else:
            self.go_keyboard()
    
    def go_end(self):
        rowno, colno = self.logic.get_end()
        self.select(rowno,colno)
    
    def go_start(self):
        rowno, colno = self.logic.get_start()
        self.select(rowno,colno)
    
    def go_down(self):
        ''' #NOTE: This should run only after the event since Qt returns dummy
            geometry values right after startup.
        '''
        rowno, colno = self.get_cell()
        rowno, colno = self.logic.get_next_row(rowno,colno)
        self.select(rowno,colno)
        self.scroll_top()
    
    def select(self,rowno,colno,Mouse=False):
        self.model.update(self.gui.get_index())
        new_index = self.model.index(rowno,colno)
        if Mouse:
            self.gui.set_index(new_index)
        else:
            self.gui.set_cur_index(new_index)
        self.model.update(new_index)
    
    def go_up(self):
        rowno, colno = self.get_cell()
        rowno, colno = self.logic.get_prev_row(rowno,colno)
        self.select(rowno,colno)
    
    def go_left(self):
        rowno, colno = self.get_cell()
        rowno, colno = self.logic.get_prev_col(rowno,colno)
        self.select(rowno,colno)
    
    def go_right(self):
        rowno, colno = self.get_cell()
        rowno, colno = self.logic.get_next_col(rowno,colno)
        self.select(rowno,colno)
    
    def scroll_top(self):
        f = '[MClientQt] mclient.Table.scroll_top'
        if not self.coords:
            sh.com.rep_empty(f)
            return
        rowno, colno = self.gui.get_cell()
        index_ = self.model.index(self.coords[rowno],colno)
        self.gui.scroll2index(index_)
    
    def go_cell(self):
        print('go_cell')
    
    def get_cell(self):
        f = '[MClientQt] mclient.Table.get_cell'
        try:
            return self.gui.get_cell()
        except Exception as e:
            sh.com.rep_third_party(f,e)
            return(0,0)
    
    def copy_cell(self):
        f = '[MClientQt] mclient.Table.copy_cell'
        rowno, colno = self.gui.get_cell()
        mes = '"' + self.plain[rowno][colno] + '"'
        sh.objs.get_mes(f,mes,True).show_debug()
    
    def clear(self):
        self.gui.clear()
    
    def set_row_height(self,height=42):
        for no in range(self.logic.rownum):
            self.gui.set_row_height(no,height)
    
    def set_col_width(self):
        # For some reason, this works only after filling cells
        f = '[MClientQt] mclient.Table.set_col_width'
        mes = _('Number of columns: {}').format(self.logic.colnum)
        sh.objs.get_mes(f,mes,True).show_debug()
        #TODO: Rework, number of fixed columns can be different
        for no in range(self.logic.colnum):
            if no == 0:
                width = 140
            elif no == 1:
                width = sh.lg.globs['int']['fixed_col_width']
            elif no in (2,3):
                width = 63
            else:
                width = sh.lg.globs['int']['term_col_width']
            self.gui.set_col_width(no,width)
    
    def reset(self,cells):
        f = '[MClientQt] mclient.Table.reset'
        if not cells:
            sh.com.rep_empty(f)
            return
        self.clear()
        self.logic.reset(cells)
        self.model = gi.TableModel(self.logic.table)
        self.fill()
        self.set_col_width()
        self.set_row_height(self.row_height)
        self.show_borders(False)
        #self.set_long()
        self.go_start()
    
    def set_long(self):
        ''' This is slow ('set' on Intel Atom without debugging: ~2.68s with
            default sizeHint and ~5.57s with custom sizeHint.
        '''
        f = '[MClient] mclient.Table.set_long'
        timer = sh.Timer(f)
        timer.start()
        self.gui.delegate.long = []
        for rowno in range(self.logic.rownum):
            for colno in range(self.logic.colnum):
                index_ = self.model.index(rowno,colno)
                height = self.gui.get_cell_hint(index_)
                #mes = 'Row #{}. Column #{}. Size hint: {}'
                #mes = mes.format(rowno,colno,height)
                #sh.objs.get_mes(f,mes,True).show_debug()
                #if height > self.row_height:
                if height > 380:
                    self.gui.delegate.long.append(index_)
        timer.end()
        mes = _('Number of cells: {}').format(self.logic.rownum*self.logic.colnum)
        sh.objs.get_mes(f,mes,True).show_debug()
        mes = _('Number of long cells: {}').format(len(self.gui.delegate.long))
        sh.objs.get_mes(f,mes,True).show_debug()
    
    def set_coords(self,event=None):
        f = '[MClientQt] mclient.Table.set_coords'
        ''' Calculating Y is very fast (~0.05s for 'set' on Intel Atom). We
            need None since this procedure overrides
            self.gui.parent.resizeEvent.
        '''
        height = self.gui.get_height()
        mes = _('Window height: {}').format(height)
        sh.objs.get_mes(f,mes,True).show_debug()
        for rowno in range(self.logic.rownum):
            y = self.gui.get_cell_y(rowno) + self.gui.get_row_height(rowno)
            pageno = int(y / height)
            page_y = pageno * height
            page_rowno = self.gui.get_row_by_y(page_y)
            self.coords[rowno] = page_rowno
    
    def fill(self):
        f = '[MClientQt] mclient.Table.fill'
        timer = sh.Timer(f)
        timer.start()
        self.gui.set_model(self.model)
        timer.end()
    
    def set_max_row_height(self,height=150):
        self.gui.set_max_row_height(height)
    
    def set_max_col_width(self):
        constraints = []
        for cell in self.logic.cells:
            #TODO: elaborate
            if cell.no < 5:
                value = 63
            else:
                value = 221
            constraints.append(self.gui.get_constraint(value))
        self.gui.set_max_col_width(constraints)
    
    def show_borders(self,Show=False):
        self.gui.show_borders(Show)
    
    def set_gui(self):
        self.gui.click_right = self.copy_cell
        self.gui.click_left_arrow = self.go_left
        self.gui.click_right_arrow = self.go_right
        self.gui.select = self.select
        self.gui.clicked.connect(self.go_cell)
        #self.set_max_row_height()



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
        query = 'select NO,ROWNO,COLNO,TEXT,COLOR,FAMILY,SIZE,BOLD,ITALIC \
                 from FONTS order by NO'
        self.dbc.execute(query,)
        return self.dbc.fetchall()
    
    def close(self):
        f = '[MClient] mclient.DB.close'
        mes = _('Close "{}"').format(self.path)
        #sh.objs.get_mes(f,mes,True).show_info()
        print(mes)
        self.dbc.close()
    
    def get_max_col_no(self):
        ''' This is a less advanced alternative to 'self.get_max_col'
            for cases when positions are not set yet.
        '''
        f = '[MClient] mclient.DB.get_max_col_no'
        query = 'select COLNO from FONTS order by COLNO desc'
        self.dbc.execute(query,)
        col_no = self.dbc.fetchone()
        if col_no:
            return col_no[0]
    
    def get_max_row_no(self):
        f = '[MClient] mclient.DB.get_max_row_no'
        query = 'select ROWNO from FONTS order by ROWNO desc'
        self.dbc.execute(query,)
        result = self.dbc.fetchone()
        if result:
            return result[0]



class App:
    
    def __init__(self):
        self.gui = gi.App()
        self.set_gui()
        self.update_ui()
    
    def clear_search_field(self):
        #TODO: implement
        #objs.get_suggest().get_gui().close()
        self.panel.ent_src.clear()
    
    def reset(self,cells):
        f = '[MClientQt] mclient.App.reset'
        self.table.reset(cells)
    
    def minimize(self):
        self.gui.minimize()
    
    def update_ui(self):
        ''' #TODO: Focusing on the entry will disable left-right arrow keys
            since the table must have a focus for these keys to work. Looks
            like this happen owing to that Qt already has internal left-right
            arrow bindings for the entry, and we need to subclass the entry
            and override these bindings.
        '''
        self.gui.panel.ent_src.focus()
        #TODO: load from logic
        sources = (_('Multitran'),_('Stardict'),'Lingvo (DSL)'
                  ,_('Local MT')
                  )
        self.gui.panel.opt_src.reset(sources)
        self.gui.panel.opt_col.reset((1,2,3,4,5,6,7,8,9,10),4)
        #TODO: load from logic
        langs1 = (_('English'),_('Russian'),_('French'))
        langs2 = (_('Russian'),_('English'),_('French'))
        self.gui.panel.opt_lg1.reset(langs1)
        self.gui.panel.opt_lg2.reset(langs2)
    
    def show(self,event=None):
        self.gui.show()
    
    def close(self,event=None):
        self.gui.close()
    
    def set_bindings(self):
        # Mouse buttons cannot be bound
        self.gui.bind('Ctrl+Q',self.close)
        self.gui.bind('Esc',self.minimize)
        self.gui.bind('Down',self.table.go_down)
        self.gui.bind('Up',self.table.go_up)
        self.gui.bind('Ctrl+Home',self.table.go_start)
        self.gui.bind('Ctrl+End',self.table.go_end)
        self.table.gui.click_middle = self.minimize
        ''' Recalculate pages each time the main window is resized. This allows
            to save resources and avoid getting dummy geometry which will be
            returned before the window is shown.
        '''
        self.gui.parent.resizeEvent = self.table.set_coords
        self.panel.btn_trn.action = self.table.go
        self.panel.btn_clr.action = self.clear_search_field
        self.panel.btn_trn.set_action()
        self.panel.btn_clr.set_action()
    
    def set_title(self,title='MClientQt'):
        self.gui.set_title(title)
    
    def set_gui(self):
        self.table = Table()
        self.panel = gi.Panel()
        self.gui.set_gui(self.table.gui,self.panel)
        self.set_title()
        self.set_bindings()


if __name__ == '__main__':
    f = '[MClient] mclient.__main__'
    sh.com.start()
    lg.objs.get_plugins(Debug=False,maxrows=1000)
    db = DB()
    data = db.fetch()
    blocks = lg.com.set_blocks(data)
    cells = lg.Cells(blocks).run()
    timer = sh.Timer(f + ': Showing GUI')
    timer.start()
    app = App()
    app.panel.ent_src.widget.act_on_ctrl_end = app.table.go_end
    ''' We can get a constant mouse hovering response only if we install
        the filter like this.
    '''
    sh.objs.get_root().installEventFilter(app.gui.table)
    sh.objs.get_root().installEventFilter(app.gui.panel)
    app.reset(cells)
    timer.end()
    app.show()
    db.close()
    sh.com.end()
