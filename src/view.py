#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import copy

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.list import List
from skl_shared.table import Table

from config import CONFIG
from format import Block as fmBlock
from subjects import SUBJECTS
from articles import ARTICLES
from columns import COL_WIDTH



class Phrases:
    
    def __init__(self, blocks):
        self.sourcepr = -1
        self.dic = ''
        self.subjpr = -1
        self.wform = ''
        self.speechpr = -1
        self.transc = ''
        self.cellno = -1
        self.phname = _('Phrases')
        self.blocks = blocks
        
    def ignore_phcount(self):
        f = '[MClient] view.Phrases.ignore_phcount'
        if CONFIG.new['PhraseCount']:
            rep.lazy(f)
            return
        count = 0
        for block in self.blocks:
            if block.type == 'phcount':
                count += 1
                block.Ignore = True
        rep.matches(f, count)
    
    def set_sourcepr(self):
        f = '[MClient] view.Phrases.set_sourcepr'
        sourcepr = [block.sourcepr for block in self.blocks]
        if not sourcepr:
            rep.lazy(f)
            return
        self.sourcepr = max(sourcepr) + 1
        mes = f'"{self.sourcepr}"'
        Message(f, mes).show_debug()
    
    def set_subjpr(self):
        f = '[MClient] view.Phrases.set_subjpr'
        subjpr = [block.subjpr for block in self.blocks]
        if not subjpr:
            rep.lazy(f)
            return
        self.subjpr = max(subjpr) + 1
        mes = f'"{self.subjpr}"'
        Message(f, mes).show_debug()
    
    def set_dic(self):
        f = '[MClient] view.Phrases.set_dic'
        for block in self.blocks[::-1]:
            if block.dic and not block.type in ('phsubj', 'phrase', 'phcount'
                                               ,'comment'):
                self.dic = block.dic
                mes = f'"{self.dic}"'
                Message(f, mes).show_debug()
                return
    
    def set_wform(self):
        f = '[MClient] view.Phrases.set_wform'
        for block in self.blocks[::-1]:
            if block.wform and not block.type in ('phsubj', 'phrase', 'phcount'
                                                 ,'comment'):
                self.wform = block.wform
                mes = f'"{self.wform}"'
                Message(f, mes).show_debug()
                return
    
    def set_speechpr(self):
        f = '[MClient] view.Phrases.set_speechpr'
        speechpr = [block.speechpr for block in self.blocks]
        if not speechpr:
            rep.lazy(f)
            return
        self.speechpr = max(speechpr) + 1
        mes = f'"{self.speechpr}"'
        Message(f, mes).show_debug()
    
    def set_transc(self):
        f = '[MClient] view.Phrases.set_transc'
        for block in self.blocks[::-1]:
            if block.transc and not block.type in ('phsubj', 'phrase', 'phcount'
                                                  ,'comment'):
                self.transc = block.transc
                mes = f'"{self.transc}"'
                Message(f, mes).show_debug()
                return
    
    def set_cellno(self):
        f = '[MClient] view.Phrases.set_cellno'
        cellnos = [block.cellno for block in self.blocks]
        if not cellnos:
            rep.lazy(f)
            return
        self.cellno = max(cellnos) + 1
        mes = f'"{self.cellno}"'
        Message(f, mes).show_debug()
    
    def reassign(self):
        ''' - phsubj is set to an incorrect row without this.
            - Phrases may have synonyms attached to them and formatted as
              comments, so moving by cellno is more precise.
        '''
        f = '[MClient] view.Phrases.reassign'
        cellnos = [block.cellno for block in self.blocks \
                  if block.type == 'phrase']
        if not cellnos:
            rep.lazy(f)
            return
        phrases = [block for block in self.blocks if block.cellno in cellnos]
        for block in phrases:
            block.cellno = self.cellno
            block.sourcepr = self.sourcepr
            block.dic = self.dic
            block.subjpr = self.subjpr
            block.wform = self.wform
            block.speechpr = self.speechpr
            block.transc = self.transc
            block.cellno = self.cellno
            block.subj = block.subjf = self.phname
            
    def run(self):
        # At this point, blocks may have identical cellno
        self.set_sourcepr()
        self.set_dic()
        self.set_subjpr()
        self.set_wform()
        self.set_speechpr()
        self.set_transc()
        self.set_cellno()
        self.ignore_phcount()
        self.reassign()
        return self.blocks



class View:
    # Order blocks as specified by the user
    def __init__(self, blocks):
        self.Success = True
        self.blocks = blocks
        # Must be recreated for each article loading/reloading
        self.fixed_cols = COL_WIDTH.get_fixed_types()
    
    def check(self):
        f = '[MClient] view.View.check'
        if not self.blocks:
            self.Success = False
            rep.empty(f)
    
    def sort(self):
        f = '[MClient] view.View.sort'
        if not self.Success:
            rep.cancel(f)
            return
        if not CONFIG.new['OrderCells']:
            rep.empty(f)
            return
        #if CONFIG.new['AlphabetizeTerms'] and not ARTICLES.is_parallel() \
        #and not ARTICLES.is_separate():
            self.blocks.sort(key=lambda b: (b.col1, b.col2, b.col3, b.col4, b.col5, b.col6, b.cellno, b.no))
    
    '''
    def _get_fixed(self, block):
        f = '[MClient] view.View._get_fixed'
        iblock = Block()
        iblock.type = block.type
        iblock.Delete = True
        if block.type in ('phsubj', 'phrase', 'phcount'):
            iblock.subjpr = block.subjpr
            iblock.speechpr = block.speechpr
            if block.type == 'subj':
                if CONFIG.new['ShortSubjects']:
                    iblock.text = block.subj
                else:
                    iblock.text = block.subjf
            return iblock
        iblock.source = block.source
        iblock.dic = block.dic
        iblock.subj = block.subj
        iblock.subjf = block.subjf
        iblock.subjpr = block.subjpr
        iblock.wform = block.wform
        iblock.transc = block.transc
        iblock.speech = block.speech
        iblock.speechpr = block.speechpr
    '''
    
    '''
    def _create_fixed(self, block):
        f = '[MClient] view.View._create_fixed'
        iblock = Block()
        iblock.type = block.type
        iblock.Delete = True
        if block.type in ('phsubj', 'phrase', 'phcount'):
            iblock.subjpr = block.subjpr
            iblock.speechpr = block.speechpr
            if block.type == 'subj':
                iblock.text = block.subj
            return iblock
        iblock.source = block.source
        iblock.dic = block.dic
        iblock.subj = block.subj
        iblock.subjpr = block.subjpr
        iblock.wform = block.wform
        iblock.transc = block.transc
        iblock.speech = block.speech
        iblock.speechpr = block.speechpr
        if block.type == 'source':
            iblock.text = block.source
        elif block.type == 'dic':
            iblock.text = block.dic
        elif block.type == 'subj':
            iblock.text = block.subj
        elif block.type == 'wform':
            iblock.text = block.wform
        elif block.type == 'transc':
            iblock.text = block.transc
        elif block.type == 'speech':
            iblock.text = block.speech
        elif not block.type:
            # Empty types are actually allowed since we can have empty columns
            pass
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(block.type, 'source, dic, subj, wform, transc, speech, or empty')
            Message(f, mes, True).show_error()
        return iblock
    '''
    
    def restore_fixed(self):
        f = '[MClient] view.View.restore_fixed'
        if not self.Success:
            rep.cancel(f)
            return
        count = 0
        i = 1
        while i < len(self.blocks):
            if self.blocks[i-1].rowno != self.blocks[i].rowno:
                rowno = self.blocks[i].rowno
                for type_ in self.fixed_cols:
                    count += 1
                    block = self._create_fixed(i, type_, rowno)
                    self.blocks.insert(i, block)
                    i += 1
            i += 1
        rep.matches(f, count)
    
    def restore_first(self):
        # Add fixed cells for the very first row
        f = '[MClient] view.View.restore_first'
        if not self.Success:
            rep.cancel(f)
            return
        count = 0
        rowno = self.cells[0].rowno
        for type_ in self.fixed_cols[::-1]:
            count += 1
            cell = self._create_fixed(0, type_, rowno)
            self.cells.insert(0, cell)
        rep.matches(f, count)
    
    def debug(self, maxrow=35):
        f = '[MClient] view.View.debug'
        if not self.Success:
            rep.cancel(f)
            return
        headers = (_('ROW #'), _('CELL #'), _('TEXT'), _('TYPES'), 'URL', 'COL1'
                  ,'COL2', 'COL3', 'COL4', 'COL5', 'COL6')
        rowno = []
        no = []
        text = []
        types = []
        url = []
        col1 = []
        col2 = []
        col3 = []
        col4 = []
        col5 = []
        col6 = []
        for cell in self.cells:
            rowno.append(cell.rowno)
            no.append(cell.no)
            text.append(cell.text)
            url.append(cell.url)
            col1.append(cell.col1)
            col2.append(cell.col2)
            col3.append(cell.col3)
            col4.append(cell.col4)
            col5.append(cell.col5)
            col6.append(cell.col6)
            cell_types = []
            for block in cell.blocks:
                cell_types.append(block.type)
            types.append(', '.join(cell_types))
        iterable = [rowno, no, text, types, url, col1, col2, col3, col4, col5
                   ,col6]
        return Table(headers=headers, iterable=iterable, maxrow=maxrow).run()
    
    def _renumber_cell_nos(self):
        for i in range(len(self.cells)):
            self.cells[i].no = i
    
    def _renumber_row_nos(self):
        # Actually, we do this for prettier debug output
        rownos = [0]
        rowno = 0
        i = 1
        while i < len(self.cells):
            if self.cells[i-1].rowno != self.cells[i].rowno:
                rowno += 1
            rownos.append(rowno)
            i += 1
        i = 0
        while i < len(self.cells):
            self.cells[i].rowno = rownos[i]
            i += 1
    
    def renumber(self):
        f = '[MClient] view.View.renumber'
        if not self.Success:
            rep.cancel(f)
            return
        self._renumber_cell_nos()
        self._renumber_row_nos()
    
    def clear_duplicates(self):
        f = '[MClient] view.View.clear_duplicates'
        if not self.Success:
            rep.cancel(f)
            return
        source = dic = subj = wform = transc = speech = ''
        for cell in self.cells:
            if not cell.fixed_block:
               continue
            if cell.fixed_block.type == 'source':
                if cell.text == source:
                    cell.text = cell.fixed_block.text = ''
                else:
                    source = cell.source
            elif cell.fixed_block.type == 'dic':
                if cell.text == dic:
                    cell.text = cell.fixed_block.text = ''
                else:
                    dic = cell.dic
            elif cell.fixed_block.type == 'subj':
                if cell.text == subj or (not subj and not cell.subj):
                    cell.text = cell.fixed_block.text = ''
                else:
                    subj = cell.subj
            elif cell.fixed_block.type == 'wform':
                if cell.text == wform:
                    cell.text = cell.fixed_block.text = ''
                else:
                    wform = cell.wform
            elif cell.fixed_block.type == 'transc':
                if cell.text == transc:
                    cell.text = cell.fixed_block.text = ''
                else:
                    transc = cell.transc
            elif cell.fixed_block.type == 'speech':
                if cell.text == speech:
                    cell.text = cell.fixed_block.text = ''
                else:
                    speech = cell.speech
    
    def fill_cols(self):
        f = '[MClient] view.View.fill_cols'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.fixed_cols:
            rep.lazy(f)
            return
        ''' Word forms must be case-sensitive; otherwise, they can be ordered
            like AST - ast - AST, etc.
        '''
        for block in self.blocks:
            for i in range(len(self.fixed_cols)):
                match i:
                    case 0:
                        match self.fixed_cols[i]:
                            case 'source':
                                block.col1 = block.sourcepr
                            case 'dic':
                                block.col1 = block.dic.lower()
                            case 'subj':
                                block.col1 = block.subjpr
                            case 'wform':
                                block.col1 = block.wform
                            case 'speech':
                                block.col1 = block.speechpr
                            case 'transc':
                                block.col1 = block.transc
                    case 1:
                        match self.fixed_cols[i]:
                            case 'source':
                                block.col2 = block.sourcepr
                            case 'dic':
                                block.col2 = block.dic.lower()
                            case 'subj':
                                block.col2 = block.subjpr
                            case 'wform':
                                block.col2 = block.wform
                            case 'speech':
                                block.col2 = block.speechpr
                            case 'transc':
                                block.col2 = block.transc
                    case 2:
                        match self.fixed_cols[i]:
                            case 'source':
                                block.col3 = block.sourcepr
                            case 'dic':
                                block.col3 = block.dic.lower()
                            case 'subj':
                                block.col3 = block.subjpr
                            case 'wform':
                                block.col3 = block.wform
                            case 'speech':
                                block.col3 = block.speechpr
                            case 'transc':
                                block.col3 = block.transc
                    case 3:
                        match self.fixed_cols[i]:
                            case 'source':
                                block.col4 = block.sourcepr
                            case 'dic':
                                block.col4 = block.dic.lower()
                            case 'subj':
                                block.col4 = block.subjpr
                            case 'wform':
                                block.col4 = block.wform
                            case 'speech':
                                block.col4 = block.speechpr
                            case 'transc':
                                block.col4 = block.transc
                    case 4:
                        match self.fixed_cols[i]:
                            case 'source':
                                block.col5 = block.sourcepr
                            case 'dic':
                                block.col5 = block.dic.lower()
                            case 'subj':
                                block.col5 = block.subjpr
                            case 'wform':
                                block.col5 = block.wform
                            case 'speech':
                                block.col5 = block.speechpr
                            case 'transc':
                                block.col5 = block.transc
                    case 5:
                        match self.fixed_cols[i]:
                            case 'source':
                                block.col6 = block.sourcepr
                            case 'dic':
                                block.col6 = block.dic.lower()
                            case 'subj':
                                block.col6 = block.subjpr
                            case 'wform':
                                block.col6 = block.wform
                            case 'speech':
                                block.col6 = block.speechpr
                            case 'transc':
                                block.col6 = block.transc
    
    def run(self):
        self.check()
        self.fill_cols()
        self.sort()
        #self.restore_fixed()
        #self.restore_first()
        #self.clear_duplicates()
        #self.renumber()
        return self.blocks



class Wrap2:
    
    def __init__(self, blocks):
        self.Success = True
        self.blocks = blocks
        self.rowno = -1
        self.colno = 0
    
    def _set_text_by_type(self, block, column):
        match column.type:
            case 'source':
                block.text = block.source
            case 'dic':
                block.text = block.dic
            case 'subj':
                if CONFIG.new['ShortSubjects']:
                    block.text = block.subj
                else:
                    block.text = block.subjf
            case 'wform':
                block.text = block.wform
            case 'speech':
                if CONFIG.new['ShortSpeech']:
                    block.text = block.speech
                else:
                    block.text = block.speechf
            case 'transc':
                block.text = block.transc
            # Column types are read from config, so '' means column is not set
            case '':
                block.text = ''
            case other if True:
                mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
                mes = mes.format(other, 'source, dic, subj, wform, speech or transc')
                Message(f, mes, True).show_error()
        return block
    
    def _create_block(self, block, column, Empty=False):
        f = '[MClient] view.View._create_block'
        if not block or not column:
            rep.empty(f)
            return block
        block = copy.deepcopy(block)
        block.Delete = True
        if Empty:
            block.text = ''
        else:
            block = self._set_text_by_type(block, column)
        block.type = column.type
        block.no = block.no - 1 + float(f'.{column.no + 1}')
        block.cellno = block.cellno - 1 + float(f'.{column.no + 1}')
        block.rowno = self.rowno
        block.colno = self.colno
        self.colno += 1
        return block
    
    def _create_row(self, block, Empty=False):
        row = []
        self.rowno += 1
        self.colno = 0
        for column in COL_WIDTH.columns[:COL_WIDTH.fixed_num]:
            row.append(self._create_block(block, column, Empty))
        return row
    
    def wrap(self):
        collimit = COL_WIDTH.fixed_num + COL_WIDTH.term_num
        new_blocks = []
        source = dic = subj = wform = speech = transc = ''
        cellno = 0
        for block in self.blocks:
            if (source, dic, subj, wform, speech, transc) != (block.source
               ,block.dic, block.subj, block.wform, block.speech, block.transc):
                # Required in both if and elif; otherwise, expect bugs
                cellno = block.cellno
                new_blocks += self._create_row(block)
                source = block.source
                dic = block.dic
                subj = block.subj
                wform = block.wform
                speech = block.speech
                transc = block.transc
            elif block.cellno != cellno:
                cellno = block.cellno
                if self.colno + 1 == collimit:
                    new_blocks += self._create_row(block, True)
                else:
                    self.colno += 1
            new_blocks.append(block)
            new_blocks[-1].rowno = self.rowno
            new_blocks[-1].colno = self.colno
        self.blocks = new_blocks
    
    def run(self):
        self.wrap()
        return self.blocks



class Wrap:
    
    def __init__(self, blocks):
        ''' Since we create even empty columns, the number of fixed cells in
            a row should always be 6 (unless new fixed types are added).
        '''
        self.Success = True
        self.plain = []
        self.code = []
        self.blocks = blocks
        self.fixed_len = COL_WIDTH.fixed_num
        self.collimit = COL_WIDTH.fixed_num + COL_WIDTH.term_num
    
    def clear_single_source(self):
        f = '[MClient] view.Wrap.clear_single_source'
        if not self.Success:
            rep.cancel(f)
            return
        if not CONFIG.new['ClearSingleSource']:
            rep.lazy(f)
            return
        sources = set([block.source for block in self.blocks if block.source])
        if len(sources) == 1:
            for cell in self.cells:
                cell.source = ''
    
    def check(self):
        f = '[MClient] view.Wrap.check'
        if not self.cells:
            self.Success = False
            rep.empty(f)
            return
        if self.collimit <= self.fixed_len:
            self.Success = False
            rep.condition(f, f'{self.collimit} > {self.fixed_len}')
    
    def get_empty_cells(self, delta):
        row = []
        for type_ in range(delta):
            cell = Cell()
            cell.blocks = [Block()]
            row.append(cell)
        return row
    
    def wrap(self):
        f = '[MClient] view.Wrap.wrap'
        if not self.Success:
            rep.cancel(f)
            return
        cells = []
        row = []
        rowno = 0
        for cell in self.cells:
            if len(row) == self.collimit:
                cells.append(row)
                if cell.rowno == rowno:
                    row = self.get_empty_cells(self.fixed_len)
                else:
                    row = []
            elif cell.rowno != rowno:
                row += self.get_empty_cells(self.collimit - len(row))
                cells.append(row)
                row = []
            row.append(cell)
            rowno = cell.rowno
        row += self.get_empty_cells(self.collimit - len(row))
        cells.append(row)
        self.cells = cells
    
    def _get_prev_cell(self, i, j):
        if i >= len(self.cells):
            return
        while j >= 0:
            try:
                return self.cells[i][j]
            except IndexError:
                pass
            j -= 1
    
    def _debug_cells(self, maxrow=60, maxrows=700):
        f = '[MClient] view.Wrap._debug_cells'
        mes = [f'{f}:']
        headers = (_('CELL #'), _('ROW #'), _('COLUMN #'), _('TEXT'), _('CODE')
                  ,'URL')
        no = []
        rowno = []
        colno = []
        text = []
        code = []
        url = []
        for row in self.cells:
            for cell in row:
                no.append(cell.no)
                rowno.append(cell.rowno)
                colno.append(cell.colno)
                text.append(cell.text)
                code.append(cell.code)
                url.append(cell.url)
        iterable = [no, rowno, colno, text, code, url]
        mes += Table(headers=headers, iterable=iterable, maxrow=maxrow
                    ,maxrows=maxrows).run()
        return '\n'.join(mes)
    
    def _debug_plain(self):
        f = '[MClient] view.Wrap._debug_plain'
        mes = [f'{f}:']
        plain = []
        for row in self.cells:
            new_row = []
            for cell in row:
                text = f'({cell.rowno}, {cell.no}): {cell.text}'
                new_row.append(text)
            plain.append(new_row)
        mes.append(str(plain))
        return '\n'.join(mes)
    
    def _debug_code(self):
        f = '[MClient] view.Wrap._debug_code'
        mes = [f'{f}:']
        code = []
        for row in self.cells:
            new_row = []
            for cell in row:
                text = f'({cell.rowno}, {cell.no}): {cell.code}'
                new_row.append(text)
            code.append(new_row)
        mes.append(str(code))
        return '\n'.join(mes)
    
    def debug(self):
        f = '[MClient] view.Wrap.debug'
        if not self.Success:
            rep.cancel(f)
            return
        mes = [self._debug_cells()]
        mes.append(self._debug_plain())
        mes.append(self._debug_code())
        return '\n\n'.join(mes)
    
    def renumber(self):
        f = '[MClient] view.Wrap.renumber'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.cells[0]:
            self.Success = False
            rep.empty(f)
            return
        no = 0
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                self.cells[i][j].no = no
                self.cells[i][j].rowno = i
                self.cells[i][j].colno = j
                no += 1
    
    def format(self):
        # Takes ~0.871s for 'set' on AMD E-300
        f = '[MClient] view.Wrap.format'
        if not self.Success:
            rep.cancel(f)
            return
        for row in self.cells:
            for cell in row:
                cell_code = []
                for block in cell.blocks:
                    cell_code.append(fmBlock(block, cell.colno).run())
                cell.code = List(cell_code).space_items()
    
    def set_plain(self):
        f = '[MClient] view.Wrap.set_plain'
        if not self.Success:
            rep.cancel(f)
            return
        for row in self.cells:
            new_row = []
            for cell in row:
                new_row.append(cell.text)
            self.plain.append(new_row)
    
    def set_code(self):
        f = '[MClient] view.Wrap.set_code'
        if not self.Success:
            rep.cancel(f)
            return
        for row in self.cells:
            new_row = []
            for cell in row:
                new_row.append(cell.code)
            self.code.append(new_row)
    
    def run(self):
        self.check()
        self.wrap()
        self.renumber()
        self.format()
        self.set_plain()
        self.set_code()
        self.clear_single_source()
        return self.cells