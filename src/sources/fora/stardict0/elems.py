#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import rep, Message
from skl_shared.list import List
from skl_shared.table import Table

from instance import Block, Cell, is_block_fixed

COM = ('мн') # '{{мн}}' that can be treated as comments


class Elems:
    
    def __init__(self, text, search, dic):
        self.blocks = []
        self.cells = []
        self.Parallel = False
        self.Separate = False
        self.text = text
        self.search = search
        self.dic = dic
    
    def set_blocks(self):
        lines = self.text.splitlines()
        for i in range(len(lines)):
            block = Block()
            block.text = lines[i]
            block.type = 'term'
            block.cellno = i + 2
            self.blocks.append(block)
    
    def set_cells(self):
        f = '[MClient] sources.fora.stardict0.elems.Elems.set_cells'
        if not self.blocks:
            rep.empty(f)
            return
        if len(self.blocks) < 2:
            mes = f'{len(self.blocks)} >= 2'
            rep.condition(f, mes)
            return
        cell = Cell()
        cell.blocks.append(self.blocks[0])
        i = 1
        while i < len(self.blocks):
            if self.blocks[i-1].cellno == self.blocks[i].cellno:
                cell.blocks.append(self.blocks[i])
            else:
                if cell.blocks:
                    self.cells.append(cell)
                cell = Cell()
                cell.blocks.append(self.blocks[i])
            i += 1
        if cell.blocks:
            self.cells.append(cell)
    
    def set_text(self):
        for cell in self.cells:
            fragms = [block.text for block in cell.blocks]
            cell.text = List(fragms).space_items().strip()
    
    def _get_fixed_block(self, cell):
        for block in cell.blocks:
            if is_block_fixed(block):
                return block
    
    def set_fixed_cells(self):
        for cell in self.cells:
            cell.fixed_block = self._get_fixed_block(cell)
    
    def set_row_nos(self):
        # Run this before deleting fixed types
        f = '[MClient] sources.fora.stardict0.elems.Elems.set_row_nos'
        count = 0
        if self.cells:
            count += 1
            self.cells[0].rowno = 0
        rowno = 0
        i = 1
        while i < len(self.cells):
            if not self.cells[i-1].fixed_block and self.cells[i].fixed_block:
                count += 1
                rowno += 1
            self.cells[i].rowno = rowno
            i += 1
        rep.matches(f, count)
    
    def _get_last_subj(self):
        for cell in self.cells[::-1]:
            if cell.fixed_block and cell.fixed_block.type in ('subj', 'phsubj'):
                return cell.text
    
    def _get_last_wform(self):
        for cell in self.cells[::-1]:
            if cell.fixed_block and cell.fixed_block.type == 'wform':
                return cell.text
    
    def _get_last_speech(self):
        for cell in self.cells[::-1]:
            if cell.fixed_block and cell.fixed_block.type == 'speech':
                return cell.text
    
    def _get_last_transc(self):
        for cell in self.cells[::-1]:
            if cell.fixed_block and cell.fixed_block.type == 'transc':
                return cell.text
    
    def _get_prev_subj(self, i):
        while i >= 0:
            if self.cells[i].fixed_block \
            and self.cells[i].fixed_block.type in ('subj', 'phsubj'):
                return self.cells[i].text
            i -= 1
        return ''
    
    def _get_prev_wform(self, i):
        while i >= 0:
            if self.cells[i].fixed_block \
            and self.cells[i].fixed_block.type == 'wform':
                return self.cells[i].text
            i -= 1
        return ''
    
    def _get_prev_speech(self, i):
        while i >= 0:
            if self.cells[i].fixed_block \
            and self.cells[i].fixed_block.type == 'speech':
                return self.cells[i].text
            i -= 1
        return ''
    
    def _get_prev_transc(self, i):
        while i >= 0:
            if self.cells[i].fixed_block \
            and self.cells[i].fixed_block.type == 'transc':
                return self.cells[i].text
            i -= 1
        return ''
    
    def fill_fixed(self):
        subj = self._get_last_subj()
        wform = self._get_last_wform()
        transc = self._get_last_transc()
        speech = self._get_last_speech()
        i = len(self.cells) - 1
        while i >= 0:
            if not self.cells[i].fixed_block:
                subj = self._get_prev_subj(i)
                wform = self._get_prev_wform(i)
                speech = self._get_prev_speech(i)
                transc = self._get_prev_transc(i)
            self.cells[i].subj = subj
            self.cells[i].wform = wform
            self.cells[i].speech = speech
            self.cells[i].transc = transc
            i -= 1
    
    def delete_fixed(self):
        f = '[MClient] sources.fora.stardict0.elems.Elems.delete_fixed'
        count = 0
        i = 0
        while i < len(self.cells):
            if self.cells[i].fixed_block:
                count += 1
                del self.cells[i]
                i -= 1
            i += 1
        rep.matches(f, count)
    
    def renumber(self):
        for i in range(len(self.cells)):
            self.cells[i].no = i
    
    def debug(self):
        report = [self._debug_blocks(), self._debug_cells()]
        report = [item for item in report if item]
        return '\n\n'.join(report)
    
    def _debug_blocks(self, maxrow=30, maxrows=0):
        f = '[MClient] sources.fora.stardict0.elems.Elems._debug_blocks'
        headers = (_('CELL #'), _('TYPES'), _('TEXT'), 'SUBJ', 'SUBJF', 'URL')
        nos = []
        types = []
        texts = []
        subj = []
        subjf = []
        urls = []
        for block in self.blocks:
            nos.append(block.cellno)
            types.append(block.type)
            texts.append(f'"{block.text}"')
            subj.append(block.subj)
            subjf.append(block.subjf)
            urls.append(block.url)
        mes = Table(headers = headers
                   ,iterable = (nos, types, texts, subj, subjf, urls)
                   ,maxrow = maxrow, maxrows = maxrows).run()
        return f'{f}:\n{mes}'
    
    def _debug_cells(self, maxrow=30, maxrows=0):
        f = '[MClient] sources.fora.stardict0.elems.Elems._debug_cells'
        headers = ('SUBJ', 'WFORM', 'SPEECH', 'TRANSC', _('ROW #'), _('CELL #')
                  ,_('TYPES'), _('TEXT'), 'URL')
        subj = []
        wform = []
        speech = []
        transc = []
        rownos = []
        nos = []
        types = []
        texts = []
        urls = []
        for cell in self.cells:
            subj.append(cell.subj)
            wform.append(cell.wform)
            speech.append(cell.speech)
            transc.append(cell.transc)
            rownos.append(cell.rowno)
            nos.append(cell.no)
            texts.append(f'"{cell.text}"')
            cell_types = [block.type for block in cell.blocks]
            types.append(', '.join(cell_types))
            urls.append(cell.url)
        mes = Table(headers = headers
                   ,iterable = (subj, wform, speech, transc, rownos, nos, types
                               ,texts, urls)
                   ,maxrow = maxrow, maxrows = maxrows).run()
        return f'{f}:\n{mes}'
    
    def add_subj(self):
        block = Block()
        block.cellno = 0
        block.text = self.dic
        block.type = 'subj'
        self.blocks.append(block)
    
    def add_wform(self):
        block = Block()
        block.cellno = 1
        block.text = self.search
        block.type = 'wform'
        self.blocks.append(block)
    
    def run(self):
        f = '[MClient] sources.fora.stardict0.elems.Elems.run'
        if not self.text or not self.search or not self.dic:
            rep.cancel(f)
            return []
        self.add_subj()
        self.add_wform()
        self.set_blocks()
        self.set_cells()
        self.set_text()
        self.set_fixed_cells()
        self.set_row_nos()
        self.fill_fixed()
        self.delete_fixed()
        self.renumber()
        return self.cells

