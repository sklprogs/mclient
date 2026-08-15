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
    
    def set_wform(self):
        f = '[MClient] view.Phrases.set_wform'
        wforms = [block.wform for block in self.blocks]
        if not wforms:
            rep.lazy(f)
            return
        self.wform = sorted(wforms)[-1]
        mes = f'"{self.wform}"'
        Message(f, mes).show_debug()
    
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
        transc = [block.transc for block in self.blocks]
        if not transc:
            rep.lazy(f)
            return
        self.transc = sorted(transc)[-1]
        mes = f'"{self.transc}"'
        Message(f, mes).show_debug()
    
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
        ''' Phrases may have number of counts in Multitran ('phcount') and
            synonyms attached to phrases; both are formatted as comments and
            share the same cellno as the parent phrase block, so we need to use
            cellnos.
        '''
        f = '[MClient] view.Phrases.reassign'
        cellnos = [block.cellno for block in self.blocks \
                  if block.type == 'phrase']
        if not cellnos:
            rep.lazy(f)
            return
        start = min(cellnos)
        phrases = [block for block in self.blocks if block.cellno in cellnos]
        for block in phrases:
            block.sourcepr = self.sourcepr
            block.dic = self.dic
            block.subjpr = self.subjpr
            block.wform = self.wform
            block.speechpr = self.speechpr
            block.transc = self.transc
            #block.subj = block.subjf = self.phname
            block.cellno = self.cellno + block.cellno - start
            
    def run(self):
        self.set_sourcepr()
        self.set_subjpr()
        self.set_wform()
        self.set_speechpr()
        self.set_transc()
        self.set_cellno()
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
        return self.blocks



class Phsubj:
    # Fixed blocks are inserted at 'View.Wrap', so do this afterwards
    def __init__(self, blocks, phurl=''):
        self.phname = _('Phrases')
        self.blocks = blocks
        self.phurl = phurl
    
    def _get_last_subj(self, i):
        for block in self.blocks[:i][::-1]:
            if block.type == 'subj' and block.text:
                return block
    
    def _get_first_phrase(self):
        for i in range(len(self.blocks)):
            if self.blocks[i].type == 'phrase' and self.blocks[i].text:
                return i
    
    def set(self):
        f = '[MClient] view.Phsubj.set'
        i = self._get_first_phrase()
        if i is None:
            rep.lazy(f)
            return
        phsubj = self._get_last_subj(i)
        if not phsubj:
            rep.lazy(f)
            return
        mes = _('Reassign block (row #{}, column #{}, cellno: {}, no: {}, subj: "{}", text: "{}")')
        mes = mes.format(phsubj.rowno, phsubj.colno, phsubj.cellno, phsubj.no
                        ,phsubj.subj, phsubj.text)
        Message(f, mes).show_debug()
        phsubj.type = 'phsubj'
        phsubj.subj = _('phr.')
        phsubj.text = phsubj.subjf = self.phname
        #TODO: Implement
        phsubj.url = self.phurl
    
    def run(self):
        self.set()
        return self.blocks



class Wrap:
    
    def __init__(self, blocks):
        self.blocks = blocks
        self.rowno = -1
        self.colno = 0
    
    def _set_text_by_type(self, block, column):
        f = '[MClient] view.Wrap._set_text_by_type'
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
        f = '[MClient] view.Wrap._create_block'
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
                elif block.Ignore:
                    # Do not add empty space - cells can be entirely ignored
                    pass
                else:
                    self.colno += 1
            new_blocks.append(block)
            new_blocks[-1].rowno = self.rowno
            new_blocks[-1].colno = self.colno
        self.blocks = new_blocks
    
    def clear_single_source(self):
        f = '[MClient] view.Wrap.clear_single_source'
        if not CONFIG.new['ClearSingleSource']:
            rep.lazy(f)
            return
        sources = set([block.source for block in self.blocks if block.source])
        if len(sources) != 1:
            rep.lazy(f)
            return
        count = 0
        for block in self.blocks:
            if block.type == 'source':
                count += 1
                block.text = ''
        rep.matches(f, count)
    
    def clear_duplicates(self):
        f = '[MClient] view.Wrap.clear_duplicates'
        source = dic = subj = wform = speech = transc = ''
        for block in self.blocks:
            if block.type == 'source':
                if block.source == source:
                    block.text = ''
                else:
                    source = block.source
            if block.type == 'dic':
                if block.dic == dic:
                    block.text = ''
                else:
                    dic = block.dic
            if block.type == 'subj':
                if block.subj == subj:
                    block.text = ''
                else:
                    subj = block.subj
            if block.type == 'wform':
                if block.wform == wform:
                    block.text = ''
                else:
                    wform = block.wform
            if block.type == 'speech':
                if block.speech == speech:
                    block.text = ''
                else:
                    speech = block.speech
            if block.type == 'transc':
                if block.transc == transc:
                    block.text = ''
                else:
                    transc = block.transc
    
    def format(self):
        self.blocks = [fmBlock(block).run() for block in self.blocks]
    
    def debug_format(self):
        f = '[MClient] view.Wrap.debug_format'
        mes = [f'{f}:']
        for block in self.blocks:
            mes.append(f'{block.cellno}, {block.no}, "{block.text}": "{block.code}"')
        return '\n'.join(mes)
    
    def run(self):
        self.wrap()
        self.clear_single_source()
        self.clear_duplicates()
        self.format()
        return self.blocks