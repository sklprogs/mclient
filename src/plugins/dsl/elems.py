#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import copy

from skl_shared.localize import _
from skl_shared.message.controller import rep
from skl_shared.list import List
from skl_shared.logic import Text, punc_array
from skl_shared.table import Table

from instance import Block, Cell

SPEECH_ABBR = ('гл.', 'нареч.', 'нар.', 'прил.', 'сокр.', 'сущ.')
SUBJ_ABBR = ('амер.', 'бирж.', 'банк.', 'вчт.', 'геогр.', 'карт.', 'марк.'
            ,'мор.', 'общ.', 'разг.', 'стат.', 'торг.', 'уст.', 'хир.', 'эл.')


class Elems:

    def __init__(self, blocks, Debug=False):
        f = '[MClient] plugins.dsl.elems.Elems.__init__'
        self.cells = []
        self.art_subj = {}
        self.fixed_urls = {'subj':{}, 'wform':{}, 'phsubj':{}}
        self.Parallel = False
        self.Separate = False
        self.blocks = blocks
        self.Debug = Debug
        if self.blocks:
            self.Success = True
        else:
            self.Success = False
            rep.empty(f)
    
    def set_cells(self):
        f = '[MClient] plugins.dsl.elems.Elems.set_cells'
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
    
    def _is_block_fixed(self, block):
        return block.type in ('subj', 'wform', 'speech', 'transc', 'phsubj')
    
    def _get_fixed_block(self, cell):
        for block in cell.blocks:
            if block.Fixed:
                return block
    
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
    
    def set_fixed_blocks(self):
        for block in self.blocks:
            block.Fixed = self._is_block_fixed(block)
    
    def renumber(self):
        for i in range(len(self.cells)):
            self.cells[i].no = i
    
    def unite_brackets(self):
        ''' Combine a cell with a preceding or following bracket such that the
            user would not see '()' when the cell is ignored/blocked.
        '''
        f = '[MClient] plugins.dsl.elems.Elems.unite_brackets'
        count = 0
        for cell in self.cells:
            i = 2
            while i < len(cell.blocks):
                if cell.blocks[i-2].text.strip() == '(' \
                and cell.blocks[i].text.strip() == ')':
                    count += 1
                    ''' Add brackets to text of a cell (usually of the 'user'
                        type), not vice versa, to preserve its type.
                    '''
                    cell.blocks[i-1].text = cell.blocks[i-2].text \
                                          + cell.blocks[i-1].text \
                                          + cell.blocks[i].text
                    del cell.blocks[i]
                    del cell.blocks[i-2]
                    i -= 2
                i += 1
        rep.matches(f, count)
    
    def set_text(self):
        for cell in self.cells:
            fragms = [block.text for block in cell.blocks]
            cell.text = List(fragms).space_items().strip()
            # 'phsubj' text may have multiple spaces for some reason
            cell.text = Text(cell.text).delete_duplicate_spaces()
    
    def set_fixed_cells(self):
        for cell in self.cells:
            cell.fixed_block = self._get_fixed_block(cell)
    
    def set_row_nos(self):
        # Run this before deleting fixed types
        f = '[MClient] plugins.dsl.elems.Elems.set_row_nos'
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
        f = '[MClient] plugins.dsl.elems.Elems.delete_fixed'
        count = 0
        i = 0
        while i < len(self.cells):
            if self.cells[i].fixed_block:
                count += 1
                del self.cells[i]
                i -= 1
            i += 1
        rep.matches(f, count)
    
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
    
    def fix_transc(self):
        f = '[MClient] plugins.dsl.elems.Elems.fix_transc'
        if len(self.blocks) < 3:
            return
        count = 0
        i = 2
        while i < len(self.blocks):
            if self.blocks[i].type == 'comment' \
            and self.blocks[i].text == r'\]' \
            and self.blocks[i-1].type == 'transc' \
            and self.blocks[i-2].type == 'comment' \
            and self.blocks[i-2].text == r'\[':
                self.blocks[i-2].type = 'transc'
                self.blocks[i-2].cellno = self.blocks[i].cellno
                self.blocks[i-2].text = '['
                self.blocks[i].type = 'transc'
                self.blocks[i].text = ']'
            i += 1
    
    def delete_numeration(self):
        f = '[MClient] plugins.dsl.elems.Elems.delete_numeration'
        old_len = len(self.blocks)
        self.blocks = [block for block in self.blocks \
                      if not re.match(r'\d+\)[\s]{0,1}', block.text)]
        count = old_len - len(self.blocks)
        rep.matches(f, count)
    
    def set_speech(self):
        f = '[MClient] plugins.dsl.elems.Elems.set_speech'
        count = 0
        for block in self.blocks:
            if block.text in SPEECH_ABBR:
                count += 1
                block.type = 'speech'
                block.speech = block.text
                block.Fixed = True
        rep.matches(f, count)
    
    def set_subjects(self):
        f = '[MClient] plugins.dsl.elems.Elems.set_subjects'
        count = 0
        for block in self.blocks:
            if block.text in SUBJ_ABBR:
                count += 1
                block.type = 'subj'
                block.subj = block.text
                block.Fixed = True
        rep.matches(f, count)

    def fix_cellnos(self):
        #NOTE: We assume that adjacent fixed blocks have a different type
        f = '[MClient] plugins.dsl.elems.Elems.fix_cellnos'
        count = 0
        for block in self.blocks:
            if block.Fixed:
                count += 1
                block.cellno += 0.01
        rep.matches(f, count)
    
    def run(self):
        f = '[MClient] plugins.dsl.elems.Elems.run'
        if not self.Success:
            rep.cancel(f)
            return []
        self.delete_numeration()
        self.fix_transc()
        self.set_speech()
        self.set_subjects()
        self.fix_cellnos()
        self.fill()
        self.set_fixed_blocks()
        self.set_cells()
        self.set_text()
        self.set_fixed_cells()
        self.set_row_nos()
        self.unite_brackets()
        self.fill_fixed()
        self.delete_fixed()
        self.renumber()
        return self.cells
    
    def _debug_cells(self, maxrow=30, maxrows=0):
        f = '[MClient] plugins.dsl.elems.Elems._debug_cells'
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
        mes = [f'{f}:']
        sub = _('Cells:')
        mes.append(sub)
        sub = Table(headers = headers
                   ,iterable = (subj, wform, speech, transc, rownos, nos, types
                               ,texts, urls)
                   ,maxrow = maxrow, maxrows = maxrows).run()
        mes.append(sub)
        return '\n'.join(mes)
    
    def _debug_blocks(self, maxrow=70, maxrows=1000):
        f = '[MClient] plugins.dsl.elems.Elems.debug'
        headers = ('NO', 'SUBJ', 'SUBJF', 'WFORM', 'SPEECH', 'TRANSC', 'TYPE'
                  ,'TEXT')
        rows = []
        for i in range(len(self.blocks)):
            rows.append([i + 1, self.blocks[i].subj, self.blocks[i].subjf
                       ,self.blocks[i].wform, self.blocks[i].speech
                       ,self.blocks[i].transc, self.blocks[i].type
                       ,self.blocks[i].text])
        mes = [f'{f}:']
        sub = _('Blocks:')
        mes.append(sub)
        sub = Table(headers = headers, iterable = rows, maxrow = maxrow
                   ,maxrows = maxrows, Transpose = True, encloser = '"').run()
        mes.append(sub)
        mes.append('')
        return '\n'.join(mes)
    
    def debug(self, maxrow=50, maxrows=1000):
        f = '[MClient] plugins.dsl.elems.Elems.debug'
        if not self.blocks:
            rep.lazy(f)
            return
        report = [self._debug_blocks(maxrow, maxrows)
                 ,self._debug_cells(maxrow, maxrows)]
        report = [item for item in report if item]
        return '\n\n'.join(report)
    
    def fill(self):
        subj = wform = speech = transc = ''
        
        # Find first non-empty values and set them as default
        for block in self.blocks:
            if block.type == 'subj':
                subj = block.text
                break
        for block in self.blocks:
            if block.type == 'wform':
                wform = block.text
                break
        for block in self.blocks:
            if block.type == 'speech':
                speech = block.text
                break
        for block in self.blocks:
            if block.type == 'transc':
                transc = block.text
                break
        
        for block in self.blocks:
            if block.type == 'subj':
                subj = block.text
            elif block.type == 'wform':
                wform = block.text
            elif block.type == 'speech':
                speech = block.text
            elif block.type == 'transc':
                transc = block.text
                ''' #TODO: Is there a difference if we use both term/phrase
                    here or the term only?
                '''
            block.subj = block.subjf = subj.strip()
            block.wform = wform
            block.speech = speech
            block.transc = transc
