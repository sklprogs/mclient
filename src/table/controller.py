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
from search.controller import Search
from columns import COL_WIDTH
import format as fm


class Table:

    def __init__(self):
        self.set_values()
        self.logic = lgTable([])
        self.gui = guiTable()
        self.search = Search()
        self.set_gui()
    
    def set_values(self):
        self.model = None
        self.coords = {}
        self.old_rowno = -1
        self.old_colno = -1
    
    def _check_cell(self, cell):
        f = '[MClient] table.controller.Table._check_cell'
        if not cell:
            rep.empty(f)
            return
        if len(cell) != 2:
            mes = f'{len(cell)} == 2'
            rep.condition(f, mes)
            return
    
    def get_cell_x(self, colno):
        return self.gui.get_cell_x(colno)
    
    def get_cell_y(self, rowno):
        return self.gui.get_cell_y(rowno)
    
    def go_start(self):
        block = self.logic.get_start()
        self.select(block)
    
    def go_end(self):
        block = self.logic.get_end()
        self.select(block)
    
    def search_prev(self):
        self.reset_search()
        block = self.search.search_prev()
        self.select(block)
    
    def search_next(self):
        self.reset_search(True)
        block = self.search.search_next()
        self.select(block)
    
    def reset_search(self, Forward=False):
        block = self.get_selected_block(Forward)
        self.search.reset(self.logic.blocks, block)
    
    def close_search_next(self):
        self.search.close()
        self.reset_search(True)
        block = self.search.search_next()
        self.select(block)
    
    def go_prev_section(self, colno):
        f = '[MClient] table.controller.Table.go_prev_section'
        if colno < 0 or colno >= self.logic.colnum:
            mes = f'0 <= {colno} < {self.logic.colnum}'
            rep.condition(f, mes)
            return
        block = self.get_selected_block()
        block = self.logic.get_prev_section(block, colno)
        self.select(block)
    
    def go_next_section(self, colno):
        f = '[MClient] table.controller.Table.go_next_section'
        if colno < 0 or colno >= self.logic.colnum:
            mes = f'0 <= {colno} < {self.logic.colnum}'
            rep.condition(f, mes)
            return
        block = self.get_selected_block(True)
        block = self.logic.get_next_section(block, colno)
        self.select(block)
    
    def get_block(self, rowno, colno, Forward=False):
        f = '[MClient] table.controller.Table.get_block'
        if not self.logic.check_nos(rowno, colno):
            rep.cancel(f)
            return
        if Forward:
            for block in self.logic.blocks:
                if block.colno == colno and block.rowno == rowno:
                    return block
        else:
            for block in self.logic.blocks[::-1]:
                if block.colno == colno and block.rowno == rowno:
                    return block
    
    def get_selected_block(self, Forward=False):
        f = '[MClient] table.controller.Table.get_selected_block'
        cell = self.get_cell()
        if not cell:
            rep.empty(f)
            return
        if len(cell) != 2:
            mes = f'{len(cell)} == 2'
            rep.condition(f, mes)
            return
        return self.get_block(cell[0], cell[1], Forward)
    
    def get_cell(self):
        # Get rowno and colno
        f = '[MClient] table.controller.Table.get_cell'
        try:
            return self.gui.get_cell()
        except Exception as e:
            rep.third_party(f, e)
    
    def go_right(self):
        block = self.logic.get_right(self.get_selected_block(True))
        self.select(block)
    
    def go_left(self):
        block = self.logic.get_left(self.get_selected_block())
        self.select(block)
    
    def go_up(self):
        block = self.logic.get_up(self.get_selected_block())
        self.select(block)
    
    def go_down(self):
        ''' #NOTE: This should run only after an event since Qt returns dummy
            geometry values right after startup.
        '''
        block = self.logic.get_down(self.get_selected_block(True))
        self.select(block)
    
    def select_with_mouse(self, rowno, colno):
        f = '[MClient] table.controller.Table.select_with_mouse'
        if self.search.Shown:
            return
        if rowno < 0 or rowno >= self.logic.rownum:
            mes = f'0 <= {rowno} < {self.logic.rownum}'
            rep.condition(f, mes, False)
            return
        if colno < 0 or colno >= self.logic.colnum:
            mes = f'0 <= {colno} < {self.logic.colnum}'
            rep.condition(f, mes, False)
            return
        if rowno == self.old_rowno and colno == self.old_colno:
            return
        self.old_rowno = rowno
        self.old_colno = colno
        self.model.update(self.gui.get_index())
        new_index = self.model.index(rowno, colno)
        self.gui.set_index(new_index)
        self.model.update(new_index)
        if new_index in self.gui.delegate.long:
            self.show_popup()
        else:
            POPUP.close()
        ARTICLES.set_bookmark(rowno, colno)
    
    def select(self, block):
        f = '[MClient] table.controller.Table.select'
        if not self.logic.check_block(block):
            rep.cancel(f)
            return
        rowno, colno = block.rowno, block.colno
        if self.search.Shown:
            return
        if rowno == self.old_rowno and colno == self.old_colno:
            return
        self.old_rowno = rowno
        self.old_colno = colno
        self.model.update(self.gui.get_index())
        new_index = self.model.index(rowno, colno)
        self.gui.set_cur_index(new_index)
        self.model.update(new_index)
        self.scroll_top()
        ARTICLES.set_bookmark(rowno, colno)
    
    def go_line_start(self):
        block = self.get_selected_block()
        block = self.logic.get_line_start(block)
        self.select(block)
    
    def go_line_end(self):
        block = self.get_selected_block(True)
        block = self.logic.get_line_end(block)
        self.select(block)
    
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
        if not self.coords2:
            self.set_coords()
        if not self.coords2:
            rep.empty(f)
            return
        cell = self.get_cell()
        if not cell:
            rep.empty(f)
            return
        rowno, colno = cell[0], cell[1]
        try:
            cur_page = self.coords2[rowno]
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
        row_min, row_max = self._get_page_limits(cur_page + delta)
        block = self.logic.get_page_block(colno, row_min, row_max)
        self.select(block)
    
    def scroll_top(self):
        f = '[MClient] table.controller.Table.scroll_top'
        if not self.coords or not self.model:
            rep.empty(f)
            return
        rowno, colno = self.gui.get_cell()
        if rowno == -1 or colno == -1:
            mes = _('No cell is selected!')
            Message(f, mes).show_warning()
            return
        index_ = self.model.index(self.coords[rowno], colno)
        self.gui.scroll2index(index_)
    
    def _get_cell_text(self, block):
        cellno = block.cellno
        fragms = [block.text for block in self.logic.blocks \
                 if block.cellno == cellno]
        return List(fragms).space_items()
    
    def get_cell_text(self):
        f = '[MClient] table.controller.Table.get_cell_text'
        block = self.get_selected_block()
        if not block:
            rep.empty(f)
            return ''
        return self._get_cell_text(block)
    
    def get_cell_code(self):
        f = '[MClient] table.controller.Table.get_cell_code'
        block = self.get_selected_block()
        if not block:
            rep.empty(f)
            return ''
        cellno = block.cellno
        code = [block.code for block in self.logic.blocks \
               if block.cellno == cellno]
        return ''.join(code)
    
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
        block = self.logic.get_first_term()
        if not block:
            rep.empty(f)
            return
        self.select(block)
    
    def go_bookmark(self):
        f = '[MClient] table.controller.Table.go_bookmark'
        bookmark = ARTICLES.get_bookmark()
        if not bookmark:
            self.go_first_term()
            return
        if len(bookmark) != 2:
            mes = f'{len(bookmark)} == 2'
            rep.condition(f, mes)
            return
        rowno, colno = bookmark[0], bookmark[1]
        # There are no bookmarks or they were deleted
        if rowno == -1 or colno == -1:
            self.go_first_term()
            return
        block = self.get_block(rowno, colno)
        if not block:
            rep.empty(f)
            return
        self.select(block)
    
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
            try:
                code[block.rowno][block.colno] += block.code
            except IndexError:
                mes = _('List out of bounds at row #{}, column #{}!')
                mes = mes.format(rowno, colno)
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
    
    def set_gui(self):
        #self.set_max_row_height()
        self.set_bindings()
    
    def set_bindings(self):
        self.gui.sig_select.connect(self.select_with_mouse)
        self.search.gui.ent_src.bind(('Return',), self.close_search_next)
        self.search.gui.btn_srp.set_action(self.search_prev)
        self.search.gui.btn_srn.set_action(self.search_next)



class BlockMode:
    
    def __init__(self):
        self.block = None
    
    def is_active(self):
        return self.block
    
    def enable(self):
        f = '[MClient] table.controller.BlockMode.enable'
        Message(f, _('Enable block mode')).show_info()
        self.set_block(True)
        self.update()
    
    def disable(self):
        f = '[MClient] table.controller.BlockMode.disable'
        Message(f, _('Disable block mode')).show_info()
        self.update(True)
        self.block = None
    
    def toggle(self):
        if self.block:
            self.disable()
        else:
            self.enable()
    
    def go_up(self):
        self.reset_block_code(True)
        self.set_block()
        self.set_up()
        self.update()
    
    def get_down(self):
        f = '[MClient] table.controller.BlockMode.get_down'
        if not self.block:
            rep.empty(f)
            return
        for block in TABLE.logic.blocks:
            if block.cellno == self.block.cellno and block.no > self.block.no \
            and block.text.strip() and not block.Ignore:
                return block
    
    def set_down(self):
        f = '[MClient] table.controller.BlockMode.set_down'
        ''' Although this class should work OK with 'self.block' being None, do
            not assign all attempts to get next block rightaway to self.block,
            because a) 'TABLE.logic.get_down' does not accept None;
            b) if 'self.block' is None, it is determined by the current
            selection, i.e. the current cell, and you will not be able to go to
            the next cell in this mode.
        '''
        block = self.get_down()
        if block:
            self.block = block
            mes = _('Go to the same-cell block "{}"').format(self.block.text)
            Message(f, mes).show_debug()
            return
        block = TABLE.logic.get_down(self.block)
        if block:
            self.block = block
            mes = _('Go to the other-cell block "{}"').format(self.block.text)
            Message(f, mes).show_debug()
    
    def get_up(self):
        f = '[MClient] table.controller.BlockMode.get_up'
        if not self.block:
            rep.empty(f)
            return
        for block in TABLE.logic.blocks[::-1]:
            if block.cellno == self.block.cellno and block.no < self.block.no \
            and block.text.strip() and not block.Ignore:
                return block
    
    def set_up(self):
        f = '[MClient] table.controller.BlockMode.set_up'
        block = self.get_up()
        if block:
            self.block = block
            mes = _('Go to the same-cell block "{}"').format(self.block.text)
            Message(f, mes).show_debug()
            return
        block = TABLE.logic.get_up(self.block)
        if block:
            self.block = block
            mes = _('Go to the other-cell block "{}"').format(self.block.text)
            Message(f, mes).show_debug()
    
    def set_block(self, Forward=False):
        f = '[MClient] table.controller.BlockMode.set_block'
        ''' Do not reassign the current block if it is already set; otherwise,
            the current block is set according to the selected cell, i.e. to
            block #0, and doing 'go_down' or 'go_right' won't be able to go past
            block #1.
        '''
        if self.block:
            rep.lazy(f)
            return
        self.block = TABLE.get_selected_block(Forward)
    
    def go_down(self):
        self.reset_block_code(True)
        self.set_block(True)
        self.set_down()
        self.update()
    
    def go_left(self):
        self.update()
    
    def go_right(self):
        self.update(True)
    
    def reset_block_code(self, Reset=False):
        f = '[MClient] table.controller.BlockMode.reset_block_code'
        if not self.block:
            rep.lazy(f)
            return
        # Reset reverts current block to old formatting thus unselecting it
        fm.Block(self.block, not Reset).run()
    
    def update(self, Reset=False):
        f = '[MClient] table.controller.BlockMode.update'
        if not self.block:
            rep.lazy(f)
            return
        self.reset_block_code(Reset)
        #TODO: This is probably slower than it should be
        TABLE.reset(TABLE.logic.blocks)
        TABLE.select(self.block)


TABLE = Table()
BLOCK_MODE = BlockMode()