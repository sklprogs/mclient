#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import rep, Message
from skl_shared.logic import Text
from config import CONFIG


class Table:
    ''' To keep the current article functioning if nothing was found, we do not
        use 'Success' or call 'reset' before filling.
    '''
    def __init__(self, blocks=[]):
        self.BlockMode = False
        self.set_values()
        if blocks:
            self.reset(blocks)
    
    def set_values(self):
        self.rownum = 0
        self.colnum = 0
        ''' This is a constant value and should be manually changed only when
            new fixed types are introduced.
        '''
        self.fixed_num = 6
        self.blocks = []
        self.up = []
        self.down = []
        self.left = []
        self.right = []
        self.block = None
    
    def reset(self, blocks):
        self.set_values()
        self.blocks = blocks
        self.set_size()
        self.set_navigation()
        #TODO: Implement bookmarks and set the block
        self.set_first_term()
    
    def get_cell_code(self):
        code = [block.code for block in self.blocks \
               if block.cellno == self.block.cellno]
        return ''.join(code)
    
    def _add_row(self, text, row):
        new_row = []
        for block in row:
            itext = Text(block.cell_text)
            itext.delete_duplicate_line_breaks()
            itext.delete_line_breaks()
            itext.tabs2spaces()
            itext.delete_duplicate_spaces()
            cell_text = itext.text
            if cell_text:
                if block.colno == 0:
                    new_row.append('\n' + cell_text)
                else:
                    new_row.append(cell_text)
            else:
                new_row.append(f'({block.rowno},{block.colno})')
        if new_row:
            text.append('; '.join(new_row))
        return text
    
    def get_text(self):
        text = []
        row = []
        rowno = cellno = -1
        for block in self.blocks:
            if cellno == block.cellno:
                continue
            cellno = block.cellno
            if rowno == block.rowno:
                row.append(block)
            else:
                rowno = block.rowno
                text = self._add_row(text, row)
                row = [block]
        text = self._add_row(text, row)
        return '\n'.join(text).strip()
    
    def _get_page_block(self, colno, row_min, row_max):
        for block in self.blocks:
            if block.colno == colno and block.rowno >= row_min \
            and block.rowno <= row_max and block.text.strip() \
            and not block.Ignore:
                return block
    
    def get_page_block(self, colno, row_min, row_max):
        f = '[MClient] table.logic.Table.get_page_block'
        if row_min == -1 or row_max == -1:
            rep.cancel(f)
            return
        if colno < 0 or colno >= self.colnum:
            mes = f'0 <= {colno} < {self.colnum}'
            rep.condition(f, mes)
            return
        if row_min < 0 or row_min >= self.rownum:
            mes = f'0 <= {row_min} < {self.rownum}'
            rep.condition(f, mes)
            return
        if row_max < 0 or row_max >= self.rownum:
            mes = f'0 <= {row_max} < {self.rownum}'
            rep.condition(f, mes)
            return
        block = self._get_page_block(colno, row_min, row_max)
        if block:
            return block
        for block in self.blocks:
            if block.rowno >= row_min and block.colno >= colno \
            and block.text.strip() and not block.Ignore:
                return block
    
    def check_block(self):
        f = '[MClient] table.logic.Table.check_block'
        if self.block:
            return self.block
        rep.empty(f)
    
    def set_first_term(self):
        for block in self.blocks:
            if block.type == 'term' and block.text.strip() and not block.Ignore:
                self.block = block
                return
    
    def set_start(self):
        f = '[MClient] table.logic.Table.set_start'
        for block in self.blocks:
            if block.text.strip() and not block.Ignore:
                self.block = block
                # Start has been reached - for Search
                return True
    
    def set_end(self):
        f = '[MClient] table.logic.Table.set_end'
        for block in self.blocks[::-1]:
            if block.text.strip() and not block.Ignore:
                self.block = block
                # End has been reached - for Search
                return True
    
    def set_size(self):
        f = '[MClient] table.logic.Table.set_size'
        if not self.blocks:
            rep.empty(f)
            return
        ''' No need to take into account IGNORE here. If blocks are ignored,
            CODE is not assigned. Empty columns have zero width.
        '''
        rownos = [block.rowno for block in self.blocks]
        colnos = [block.colno for block in self.blocks]
        # Row and column numbers start from 0, so we need +1 to get len
        self.rownum = max(rownos) + 1
        self.colnum = max(colnos) + 1
        mes = _('Table size: {}×{}').format(self.rownum, self.colnum)
        Message(f, mes).show_debug()
    
    def get_phsubj(self):
        f = '[MClient] table.logic.Table.get_phsubj'
        for block in self.blocks:
            if block.type == 'phsubj':
                return block
    
    def set_col(self, colno):
        ''' We need to return even empty blocks here. If empty fixed blocks are
            not allowed, rewrite this code.
        '''
        f = '[MClient] table.logic.Table.set_col'
        if not self.check_block():
            rep.cancel(f)
            return
        if colno < 0 or colno >= self.colnum:
            mes = f'0 <= {colno} < {self.colnum}'
            rep.condition(f, mes)
            return
        for block in self.blocks:
            if block.rowno == self.block.rowno and block.colno == colno:
                self.block = block
                return True
    
    def set_navigation(self):
        self.up = sorted(self.blocks, key=lambda block: (-block.colno, -block.rowno))
        self.down = sorted(self.blocks, key=lambda block: (block.colno, block.rowno))
        self.right = sorted(self.blocks, key=lambda block: (block.rowno, block.colno))
        self.left = sorted(self.blocks, key=lambda block: (-block.rowno, -block.colno))
    
    def set_next_cell(self, lst, ref_block=None):
        f = '[MClient] table.logic.Table.set_next_cell'
        if not ref_block:
            ref_block = self.block
        if not ref_block or not lst:
            rep.empty(f)
            return
        try:
            pos = lst.index(ref_block)
        except ValueError:
            return
        try:
            block = lst[pos + 1]
        except IndexError:
            return
        if not block:
            rep.empty(f)
            return
        Empty = block.Ignore or not block.text.strip()
        SameCell = ref_block.cellno == block.cellno and not CONFIG.new['BlockMode']
        if Empty or SameCell:
            self.set_next_cell(lst, block)
        self.block = block
        return True
    
    def set_up(self):
        if not self.set_next_cell(self.up):
            self.set_end()
    
    def set_down(self):
        if not self.set_next_cell(self.down):
            self.set_start()
    
    def set_right(self):
        f = '[MClient] table.logic.Table.set_right'
        if not self.check_block():
            rep.empty(f)
            return
        if not self.set_next_cell(self.right):
            self.set_start()
    
    def set_left(self):
        f = '[MClient] table.logic.Table.set_left'
        if not self.check_block():
            rep.empty(f)
            return
        if not self.set_next_cell(self.left):
            self.set_end()
    
    def set_next_section(self, colno):
        if self.set_col(colno):
            self.set_down()
    
    def set_prev_section(self, colno):
        if self.set_col(colno):
            self.set_up()
    
    def set_line_start(self):
        f = '[MClient] table.logic.Table.set_line_start'
        if not self.check_block():
            rep.empty(f)
            return
        for block in self.blocks:
            if block.rowno == self.block.rowno and block.colno >= self.fixed_num \
            and block.text.strip() and not block.Ignore:
                self.block = block
                return
    
    def set_line_end(self):
        f = '[MClient] table.logic.Table.set_line_end'
        if not self.check_block():
            rep.empty(f)
            return
        for block in self.blocks[::-1]:
            if block.rowno == self.block.rowno and block.text.strip() and not block.Ignore:
                self.block = block
                return
