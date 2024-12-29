#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message, rep
from skl_shared_qt.graphics.clipboard.controller import CLIPBOARD
from skl_shared_qt.list import List

from config import CONFIG
from manager import PLUGINS
from articles import ARTICLES
from table.controller import TABLE
from format import Block


class BlockMode:
    
    def __init__(self):
        self.cell = None
        self.blockno = -1
    
    def copy_block(self):
        f = '[MClient] block_mode.BlockMode.copy_block'
        if not self.cell or not self.cell.blocks:
            rep.empty(f)
            return
        try:
            CLIPBOARD.copy(self.cell.blocks[self.blockno].text.strip())
            return True
        except IndexError:
            mes = _('Wrong input data: "{}"!').format(self.blockno)
            Message(f, mes, True).show_warning()
    
    def select_next(self):
        f = '[MClient] block_mode.BlockMode.select_next'
        self.enable()
        if not self.cell or not self.cell.blocks:
            rep.empty(f)
            return
        self.blockno += 1
        if self.blockno == len(self.cell.blocks):
            self.blockno = 0
        self.set_cell()
        self.select()
    
    def select_prev(self):
        f = '[MClient] block_mode.BlockMode.select_prev'
        self.enable()
        if not self.cell or not self.cell.blocks:
            rep.empty(f)
            return
        self.blockno -= 1
        if self.blockno < 0:
            self.blockno = len(self.cell.blocks) - 1
        self.set_cell()
        self.select()
    
    def toggle(self):
        if self.blockno == -1:
            self.enable()
        else:
            self.disable()
    
    def disable(self):
        f = '[MClient] block_mode.BlockMode.disable'
        self.blockno = -1
        mes = _('Disable block mode')
        Message(f, mes).show_info()
        self.set_cell()
        self.select()
    
    def enable(self):
        f = '[MClient] block_mode.BlockMode.enable'
        if self.blockno > -1:
            rep.lazy(f)
            return
        self.blockno = 0
        mes = _('Enable block mode')
        Message(f, mes).show_info()
        self.set_cell()
        self.select()
    
    def set_cell(self):
        f = '[MClient] block_mode.BlockMode.set_cell'
        tuple_ = TABLE.get_cell()
        if not tuple_:
            rep.empty(f)
            return
        rowno, colno = tuple_[0], tuple_[1]
        mes = _('Row #{}. Column #{}').format(rowno, colno)
        Message(f, mes).show_debug()
        cells = ARTICLES.get_table()
        if not cells:
            rep.empty(f)
            return
        try:
            self.cell = cells[rowno][colno]
        except (KeyError, IndexError):
            mes = _('Wrong input data!')
            Message(f, mes, True).show_warning()
            return
    
    def select(self):
        f = '[MClient] block_mode.BlockMode.select'
        if not self.cell:
            rep.empty(f)
            return
        try:
            block = self.cell.blocks[self.blockno]
        except IndexError:
            mes = _('Wrong input data: "{}"!').format(self.blockno)
            Message(f, mes).show_warning()
            return
        code = []
        for i in range(len(self.cell.blocks)):
            code.append(Block(self.cell.blocks[i], self.cell.colno, i==self.blockno).run())
        self.cell.code = List(code).space_items()
        TABLE.logic.code[self.cell.rowno][self.cell.colno] = self.cell.code
        TABLE.reset(TABLE.logic.plain, TABLE.logic.code)
        TABLE.select(self.cell.rowno, self.cell.colno)


BLOCK_MODE = BlockMode()
