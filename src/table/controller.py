#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.time import Timer
from skl_shared.graphics.clipboard.controller import CLIPBOARD
from skl_shared.list import List, get_text_table

from popup.controller import POPUP
from config import CONFIG
from articles import ARTICLES
from table.gui import Table as guiTable, TableModel
from table.logic import Table as lgTable
from columns import COL_WIDTH
import format as fm


class Table:

    def __init__(self):
        self.set_values()
        self.logic = lgTable([])
        self.gui = guiTable()
    
    def set_values(self):
        #TODO: Set in default config
        #CONFIG.new['BlockMode'] = False
        CONFIG.new['BlockMode'] = True
        self.model = None
        self.coords = {}
    
    def toggle_mode(self):
        f = '[MClient] table.controller.Table.toggle_mode'
        if CONFIG.new['BlockMode']:
            Message(f, _('Disable block mode')).show_info()
        else:
            Message(f, _('Enable block mode')).show_info()
        CONFIG.new['BlockMode'] = not CONFIG.new['BlockMode']
        self.update_cell(CONFIG.new['BlockMode'])
    
    def get_text(self):
        return self.logic.get_text()
    
    def get_cell_x(self, colno):
        return self.gui.get_cell_x(colno)
    
    def get_cell_y(self, rowno):
        return self.gui.get_cell_y(rowno)
    
    def go_start(self):
        self.update_cell()
        self.logic.set_start()
        self.select()
    
    def go_end(self):
        self.update_cell()
        self.logic.set_end()
        self.select()
    
    def go_prev_section(self, colno):
        f = '[MClient] table.controller.Table.go_prev_section'
        if colno < 0 or colno >= self.logic.colnum:
            mes = f'0 <= {colno} < {self.logic.colnum}'
            rep.condition(f, mes)
            return
        self.update_cell()
        self.logic.set_prev_section(colno)
        self.select()
    
    def go_next_section(self, colno):
        f = '[MClient] table.controller.Table.go_next_section'
        if colno < 0 or colno >= self.logic.colnum:
            mes = f'0 <= {colno} < {self.logic.colnum}'
            rep.condition(f, mes)
            return
        self.update_cell()
        self.logic.set_next_section(colno)
        self.select()
    
    def get_block(self, rowno, colno, Forward=False):
        if Forward:
            for block in self.logic.blocks:
                if block.colno == colno and block.rowno == rowno:
                    return block
        else:
            for block in self.logic.blocks[::-1]:
                if block.colno == colno and block.rowno == rowno:
                    return block
    
    def get_cell(self):
        # Get rowno and colno
        f = '[MClient] table.controller.Table.get_cell'
        try:
            return self.gui.get_cell()
        except Exception as e:
            rep.third_party(f, e)
        
    def get_cell_code(self):
        return self.logic.get_cell_code()
    
    def go_right(self):
        self.update_cell()
        self.logic.set_right()
        self.select()
    
    def go_left(self):
        self.update_cell()
        self.logic.set_left()
        self.select()
    
    def go_up(self):
        self.update_cell()
        self.logic.set_up()
        self.select()
    
    def go_down(self):
        ''' #NOTE: This should run only after an event since Qt returns dummy
            geometry values right after startup.
        '''
        self.update_cell()
        self.logic.set_down()
        self.select()
    
    def _get_block(self, block_no):
        for block in self.logic.blocks:
            if block.no == block_no:
                return block
    
    def select_with_mouse(self, block_no_str):
        f = '[MClient] table.controller.Table.select_with_mouse'
        if block_no_str is None:
            rep.empty(f)
            return
        ''' Do not impose a float with skl_shared.logic.Input.get_float because
            self.logic.block should not be overridden on failure.
        '''
        try:
            block_no = float(block_no_str)
        except ValueError:
            rep.wrong_input(f, Graphical=False)
            return
        self.update_cell()
        block = self._get_block(block_no)
        if not block:
            rep.empty(f)
            return
        self.logic.block = block
        self.select()
    
    def update_cell(self, Select=False):
        f = '[MClient] table.controller.Table.update_cell'
        if not self.logic.check_block():
            rep.cancel(f)
            return
        self.logic.block = fm.Block(self.logic.block, Select).run()
        self.model.update(self.logic.block.rowno, self.logic.block.colno, self.logic.get_cell_code())
        
    def select(self):
        f = '[MClient] table.controller.Table.select'
        if not self.logic.check_block():
            rep.cancel(f)
            return
        self.update_cell(CONFIG.new['BlockMode'])
        self.scroll_top()
        #ARTICLES.set_bookmark(self.logic.block)
    
    def go_line_start(self):
        self.update_cell()
        self.logic.set_line_start()
        self.select()
    
    def go_line_end(self):
        self.update_cell()
        self.logic.set_line_end()
        self.select()
    
    def get_row_height(self, rowno):
        return self.gui.get_row_height(rowno)
    
    def get_col_width(self, colno):
        return self.gui.get_col_width(colno)
    
    def show_popup(self):
        self.gui.show_popup()
    
    def _get_page_limits(self, page):
        f = '[MClient] table.controller.Table._get_page_limits'
        min_ = -1
        max_ = -1
        rownos = []
        for rowno in self.coords2:
            if self.coords2[rowno] == page:
                rownos.append(rowno)
        if not rownos:
            mes = _('Page: {}. Minimal row no: {}. Maximal row no: {}')
            mes = mes.format(page, min_, max_)
            Message(f, mes).show_debug()
            return(min_, max_)
        min_, max_ = min(rownos), max(rownos)
        mes = _('Page: {}. Minimal row no: {}. Maximal row no: {}')
        mes = mes.format(page, min_, max_)
        Message(f, mes).show_debug()
        return(min_, max_)
    
    def go_page(self, Forward=False):
        f = '[MClient] table.controller.Table.go_page'
        if not self.logic.check_block():
            rep.empty(f)
            return
        if not self.coords2:
            self.set_coords()
        if not self.coords2:
            rep.empty(f)
            return
        try:
            cur_page = self.coords2[self.logic.block.rowno]
            max_page = self.coords2[max(self.coords2.keys())]
        except KeyError:
            rep.wrong_input(f, Graphical=False)
            return
        if cur_page > max_page:
            mes = f'{max_page} >= {cur_page}'
            rep.condition(f, mes)
            return
        if Forward:
            if cur_page == max_page:
                rep.lazy(f)
                return
        elif cur_page == 0:
            rep.lazy(f)
            return
        if Forward:
            delta = 1
        else:
            delta = -1
        self.update_cell()
        row_min, row_max = self._get_page_limits(cur_page + delta)
        block = self.logic.get_page_block(self.logic.block.colno, row_min, row_max)
        if block:
            self.logic.block = block
        self.select()
    
    def scroll_top(self):
        f = '[MClient] table.controller.Table.scroll_top'
        if not self.coords or not self.model or not self.logic.check_block():
            rep.empty(f)
            return
        index_ = self.model.index(self.coords[self.logic.block.rowno]
                                 ,self.logic.block.colno)
        self.gui.scroll2index(index_)
    
    def get_cell_text(self):
        f = '[MClient] table.controller.Table.get_cell_text'
        if not self.logic.check_block():
            rep.empty(f)
            return ''
        return self.logic.block.cell_text
    
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
            self.gui.set_row_height(no, height)
    
    def _is_col_empty(self, colno):
        for block in self.logic.blocks:
            if block.colno == colno and block.text.strip():
                return False
        return True
    
    def set_col_width(self):
        # For some reason, this works only after filling cells
        for colno in range(self.logic.colnum):
            if self._is_col_empty(colno):
                width = 0
            else:
                width = COL_WIDTH.get_width(colno)
            self.gui.set_col_width(colno, width)
    
    def go_first_term(self):
        f = '[MClient] table.controller.Table.go_first_term'
        self.update_cell()
        self.logic.set_first_term()
        self.select()
    
    def go_bookmark(self):
        f = '[MClient] table.controller.Table.go_bookmark'
        block = ARTICLES.get_bookmark()
        if not block:
            self.go_first_term()
            return
        self.update_cell()
        self.logic.block = block
        self.select()
    
    def select_row_height(self):
        if CONFIG.new['rows']['height']:
            self.set_row_height(CONFIG.new['rows']['height'])
        else:
            self.gui.resize_to_contents()
    
    def get_code_table(self):
        f = '[MClient] table.controller.Table.get_code_table'
        code = get_text_table(self.logic.rownum, self.logic.colnum)
        if not code:
            rep.empty(f)
            return []
        for block in self.logic.blocks:
            if block.Ignore or block.Block:
                continue
            try:
                code[block.rowno][block.colno] += block.code
            except IndexError:
                mes = _('List out of bounds at row #{}, column #{}!')
                mes = mes.format(block.rowno, block.colno)
                Message(f, mes).show_warning()
                return []
        return code
    
    def reset(self, blocks):
        f = '[MClient] table.controller.Table.reset'
        if not blocks:
            rep.empty(f)
            # Keep old article functioning if nothing was found
            return
        # Reset values only if the article is not empty
        self.set_values()
        self.logic.reset(blocks)
        self.model = TableModel(self.get_code_table())
        self.fill()
        self.set_col_width()
        self.select_row_height()
        self.show_borders(False)
        ''' Coordinates are recreated each time the app window is resized. Here
            we merely suppress a warning at 'self.go_start'.
        '''
        self.set_coords()
        self.go_bookmark()
    
    def set_coords(self, event=None):
        ''' Calculating Y is very fast (~0.05s for 'set' on Intel Atom). We
            need 'event' since this procedure overrides
            self.gui.parent.resizeEvent.
        '''
        f = '[MClient] table.controller.Table.set_coords'
        self.gui.scroll2top()
        #TODO: Get rid of this
        self.coords2 = {}
        height = self.gui.get_height()
        mes = _('Window height: {}').format(height)
        Message(f, mes).show_debug()
        for rowno in range(self.logic.rownum):
            y = self.gui.get_cell_y(rowno) + self.gui.get_row_height(rowno)
            pageno = int(y / height)
            page_y = pageno * height
            page_rowno = self.gui.get_row_by_y(page_y)
            self.coords[rowno] = page_rowno
            self.coords2[rowno] = pageno
    
    def fill(self):
        self.gui.set_model(self.model)
    
    def set_max_row_height(self, height=150):
        self.gui.set_max_row_height(height)
    
    def show_borders(self, Show=False):
        self.gui.show_borders(Show)


TABLE = Table()
