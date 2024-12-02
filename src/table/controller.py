#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message, rep
from skl_shared_qt.time import Timer
from skl_shared_qt.graphics.clipboard.controller import CLIPBOARD

from popup.controller import Popup
from config import CONFIG
from articles import ARTICLES
from table.gui import TABLE, DELEGATE, TableModel
from table.logic import Table as lgTable
from search.controller import Search
from font_limits.controller import FontLimits


class Table:

    def __init__(self):
        self.set_values()
        self.logic = lgTable([], [])
        self.gui = TABLE
        self.search = Search()
        self.popup = Popup()
        self.set_gui()
    
    def _get_page_row(self, page):
        for rowno in self.coords2:
            if self.coords2[rowno] == page:
                return rowno
    
    def go_page_up(self):
        f = '[MClient] table.controller.Table.go_page_up'
        if not self.coords2:
            self.set_coords()
        if not self.coords2:
            rep.empty(f)
            return
        rowno, colno = self.get_cell()
        cur_page = self.coords2[rowno]
        if cur_page < 0:
            mes = '{} >= 0'.format(cur_page)
            rep.condition(f, mes)
            return
        if cur_page == 0:
            rep.lazy(f)
            return
        rowno = self._get_page_row(cur_page-1)
        if rowno is None:
            rep.empty(f)
            return
        self.select(rowno, colno)
    
    def go_page_down(self):
        f = '[MClient] table.controller.Table.go_page_down'
        if not self.coords2:
            self.set_coords()
        if not self.coords2:
            rep.empty(f)
            return
        rowno, colno = self.get_cell()
        cur_page = self.coords2[rowno]
        max_page = self.coords2[max(self.coords2.keys())]
        if cur_page > max_page:
            mes = f'{max_page} >= {cur_page}'
            rep.condition(f, mes)
            return
        if cur_page == max_page:
            rep.lazy(f)
            return
        rowno = self._get_page_row(cur_page+1)
        if rowno is None:
            rep.empty(f)
            return
        self.select(rowno, colno)
    
    def show_popup(self):
        f = '[MClient] table.controller.Table.show_popup'
        text = self.get_cell_code()
        if not text:
            rep.empty(f)
            return
        rowno, colno = self.get_cell()
        max_width = objs.get_app().get_width()
        width = TABLE.get_col_width(colno)
        height = TABLE.get_row_height(rowno)
        win_y = objs.app.gui.get_y()
        x1 = TABLE.get_cell_x(colno) + objs.app.gui.get_x()
        if CONFIG.new['popup']['center']:
            y1 = TABLE.get_cell_y(rowno) + win_y - height / 2
            if y1 < win_y:
                y1 = win_y
        else:
            # The value is picked up by the trial-and-error method
            y1 = TABLE.get_cell_y(rowno) + win_y - height + 10
        x2 = x1 + width
        y2 = y1 + height
        self.popup.fill(text)
        self.popup.adjust_position(x1, width, y1, height, max_width
                                  ,CONFIG.new['popup']['center'])
        self.popup.show()
    
    def go_next_section(self, no):
        rowno, colno = self.get_cell()
        rowno, colno = self.logic.get_next_row_by_col(rowno, colno, no)
        self.select(rowno, colno)
    
    def go_prev_section(self, no):
        rowno, colno = self.get_cell()
        rowno, colno = self.logic.get_prev_row_by_col(rowno, colno, no)
        self.select(rowno, colno)
    
    def close_search_next(self):
        self.search.close()
        self.reset_search()
        rowno, colno = self.search.search_next()
        self.select(rowno, colno)
    
    def reset_search(self):
        rowno, colno = self.get_cell()
        self.search.reset(self.logic.plain, rowno, colno)
    
    def search_next(self):
        self.reset_search()
        rowno, colno = self.search.search_next()
        self.select(rowno, colno)
    
    def search_prev(self):
        self.reset_search()
        rowno, colno = self.search.search_prev()
        self.select(rowno, colno)
    
    def set_values(self):
        self.model = None
        self.coords = {}
        self.old_rowno = -1
        self.old_colno = -1
    
    def go_end(self):
        rowno, colno = self.logic.get_end()
        self.select(rowno, colno)
    
    def go_start(self):
        rowno, colno = self.logic.get_start()
        self.select(rowno, colno)
    
    def go_first_term(self):
        f = '[MClient] table.controller.Table.go_first_term'
        cell = self.logic.get_first_term()
        if not cell:
            rep.empty(f)
            self.go_start()
            return
        rowno, colno = cell[0], cell[1]
        self.select(rowno, colno)
    
    def go_down(self):
        ''' #NOTE: This should run only after an event since Qt returns dummy
            geometry values right after startup.
        '''
        rowno, colno = self.get_cell()
        rowno, colno = self.logic.get_next_row(rowno, colno)
        self.select(rowno, colno)
    
    def select(self, rowno, colno, Mouse=False):
        f = '[MClient] table.controller.Table.select'
        if Mouse and self.search.Shown:
            return
        if rowno == self.old_rowno and colno == self.old_colno:
            return
        if not self.logic.plain:
            rep.empty(f)
            return
        if rowno >= len(self.logic.plain) \
        or colno >= len(self.logic.plain[rowno]):
            rep.wrong_input(f, (rowno, colno,))
            return
        if not self.logic.plain[rowno][colno].strip():
            return
        self.old_rowno = rowno
        self.old_colno = colno
        self.model.update(TABLE.get_index())
        new_index = self.model.index(rowno, colno)
        if Mouse:
            TABLE.set_index(new_index)
        else:
            TABLE.set_cur_index(new_index)
        self.model.update(new_index)
        if not Mouse:
            self.scroll_top()
        if Mouse:
            if new_index in DELEGATE.long:
                self.show_popup()
            else:
                self.popup.close()
        ARTICLES.set_bookmark(rowno, colno)
    
    def go_up(self):
        rowno, colno = self.get_cell()
        rowno, colno = self.logic.get_prev_row(rowno, colno)
        self.select(rowno, colno)
    
    def go_line_start(self):
        rowno, colno = self.get_cell()
        rowno, colno = self.logic.get_line_start(rowno)
        self.select(rowno, colno)
    
    def go_line_end(self):
        rowno, colno = self.get_cell()
        rowno, colno = self.logic.get_line_end(rowno)
        self.select(rowno, colno)
    
    def go_left(self):
        rowno, colno = self.get_cell()
        rowno, colno = self.logic.get_prev_col(rowno, colno)
        self.select(rowno, colno)
    
    def go_right(self):
        rowno, colno = self.get_cell()
        rowno, colno = self.logic.get_next_col(rowno, colno)
        self.select(rowno, colno)
    
    def scroll_top(self):
        f = '[MClient] table.controller.Table.scroll_top'
        if not self.coords or not self.model:
            rep.empty(f)
            return
        rowno, colno = TABLE.get_cell()
        if rowno == -1 or colno == -1:
            mes = _('No cell is selected!')
            Message(f, mes).show_warning()
            return
        index_ = self.model.index(self.coords[rowno], colno)
        TABLE.scroll2index(index_)
    
    def get_cell(self):
        f = '[MClient] table.controller.Table.get_cell'
        try:
            return TABLE.get_cell()
        except Exception as e:
            rep.third_party(f, e)
            return(0, 0)
    
    def get_cell_text(self):
        f = '[MClient] table.controller.Table.get_cell_text'
        if not self.logic.plain:
            rep.empty(f)
            return ''
        rowno, colno = self.get_cell()
        try:
            return self.logic.plain[rowno][colno]
        except IndexError:
            rep.wrong_input()
        return ''
    
    def get_cell_code(self):
        f = '[MClient] table.controller.Table.get_cell_code'
        if not self.logic.code:
            rep.empty(f)
            return ''
        rowno, colno = self.get_cell()
        try:
            return self.logic.code[rowno][colno]
        except IndexError:
            rep.wrong_input()
        return ''
    
    def copy_cell(self):
        f = '[MClient] table.controller.Table.copy_cell'
        if not ARTICLES.get_len():
            # Do not warn when there are no articles yet
            rep.lazy(f)
            return
        text = self.get_cell_text()
        if text:
            CLIPBOARD.copy(text)
            return True
    
    def set_row_height(self, height=42):
        for no in range(self.logic.rownum):
            TABLE.set_row_height(no, height)
    
    def set_col_width(self):
        # For some reason, this works only after filling cells
        for no in range(self.logic.colnum):
            if no in self.logic.empty_cols:
                #TODO: Check this for articles prepared for printing
                width = 0
            elif no == 0:
                #TODO: Constant widths should depend on types
                width = 123
            elif no == 1:
                width = CONFIG.new['columns']['fixed']['width']
            elif no in (2, 3):
                width = 80
            else:
                width = CONFIG.new['columns']['terms']['width']
            TABLE.set_col_width(no, width)
    
    def go_bookmark(self):
        bookmark = ARTICLES.get_bookmark()
        if not bookmark:
            self.go_first_term()
            return
        rowno, colno = bookmark[0], bookmark[1]
        if rowno > -1 and colno > -1:
            self.select(rowno, colno)
        else:
            self.go_first_term()
    
    def reset(self, plain, code):
        f = '[MClient] table.controller.Table.reset'
        if not plain or not code:
            rep.empty(f)
            # Keep old article functioning if nothing was found
            return
        # Reset values only if the article is not empty
        self.set_values()
        self.logic.reset(plain, code)
        self.model = TableModel(self.logic.code)
        self.fill()
        self.set_col_width()
        self.set_row_height(CONFIG.new['rows']['height'])
        self.show_borders(False)
        self.set_long()
        ''' Coordinates are recreated each time the app window is resized. Here
            we merely suppress a warning at 'self.go_start'.
        '''
        self.set_coords()
    
    def set_long(self):
        # Takes ~0.56s for 'set' on Intel Atom
        f = '[MClient] table.controller.Table.set_long'
        ilimits = FontLimits(family = CONFIG.new['terms']['font']['family']
                            ,size = CONFIG.new['terms']['font']['size']
                            ,Bold = False
                            ,Italic = False)
        timer = Timer(f)
        timer.start()
        DELEGATE.long = []
        for rowno in range(self.logic.rownum):
            for colno in range(self.logic.colnum):
                ilimits.set_text(self.logic.plain[rowno][colno])
                space = ilimits.get_space()
                index_ = self.model.index(rowno, colno)
                hint_space = CONFIG.new['rows']['height'] * TABLE.get_col_width(colno)
                if space > hint_space:
                    DELEGATE.long.append(index_)
        timer.end()
        mes = _('Number of cells: {}').format(self.logic.rownum*self.logic.colnum)
        Message(f, mes).show_debug()
        mes = _('Number of long cells: {}').format(len(DELEGATE.long))
        Message(f, mes).show_debug()
    
    def set_coords(self, event=None):
        ''' Calculating Y is very fast (~0.05s for 'set' on Intel Atom). We
            need 'event' since this procedure overrides
            TABLE.parent.resizeEvent.
        '''
        f = '[MClient] table.controller.Table.set_coords'
        TABLE.scroll2top()
        #TODO: Get rid of this
        self.coords2 = {}
        height = TABLE.get_height()
        mes = _('Window height: {}').format(height)
        Message(f, mes).show_debug()
        for rowno in range(self.logic.rownum):
            y = TABLE.get_cell_y(rowno) + TABLE.get_row_height(rowno)
            pageno = int(y / height)
            page_y = pageno * height
            page_rowno = TABLE.get_row_by_y(page_y)
            self.coords[rowno] = page_rowno
            self.coords2[rowno] = pageno
    
    def fill(self):
        TABLE.set_model(self.model)
    
    def set_max_row_height(self, height=150):
        TABLE.set_max_row_height(height)
    
    def show_borders(self, Show=False):
        TABLE.show_borders(Show)
    
    def set_gui(self):
        #self.set_max_row_height()
        self.set_bindings()
    
    def set_bindings(self):
        TABLE.sig_select.connect(self.select)
        self.search.gui.ent_src.bind(('Return',), self.close_search_next)
        self.search.gui.btn_srp.set_action(self.search_prev)
        self.search.gui.btn_srn.set_action(self.search_next)
        self.popup.gui.sig_close.connect(self.popup.close)