#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import copy

from skl_shared.localize import _
from skl_shared.message.controller import rep
from skl_shared.list import List
from skl_shared.logic import Text, punc_array
from skl_shared.table import Table

from instance import Block, is_block_fixed
from subjects import SUBJECTS
from speech import SPEECH


class Elems:

    def __init__(self, blocks):
        f = '[MClient] sources.dsl.elems.Elems.__init__'
        self.art_subj = {}
        self.Parallel = False
        self.Separate = False
        self.blocks = blocks
        if self.blocks:
            self.Success = True
        else:
            self.Success = False
            rep.empty(f)
    
    def _is_transc(self, i):
        return self.blocks[i-2].type == 'comment' \
        and self.blocks[i-2].text == r'\[' \
        and self.blocks[i-1].type == 'transc' \
        and self.blocks[i].type == 'comment' and self.blocks[i].text == r'\]'
    
    def fix_transc(self):
        f = '[MClient] sources.dsl.elems.Elems.fix_transc'
        if len(self.blocks) < 3:
            return
        count = 0
        i = 2
        while i < len(self.blocks):
            if self._is_transc(i):
                count += 1
                self.blocks[i-1].cellno = self.blocks[i].cellno
                self.blocks[i-1].text = '[' + self.blocks[i-1].text + ']'
            i += 1
        rep.matches(f, count)
        if count > 0:
            self.blocks = [block for block in self.blocks \
                          if not block.text in (r'\[', r'\]')]
    
    def _is_numeration(self, text):
        return re.match(r'\d+[\),\.][\s]{0,1}', text) \
        or re.match(r'[а-я][\),\.][\s]{0,1}', text) \
        or re.match(r'[a-z][\),\.][\s]{0,1}', text)
    
    def delete_numeration(self):
        f = '[MClient] sources.dsl.elems.Elems.delete_numeration'
        old_len = len(self.blocks)
        self.blocks = [block for block in self.blocks \
                      if not self._is_numeration(block.text)]
        count = old_len - len(self.blocks)
        rep.matches(f, count)
    
    def set_speech(self):
        f = '[MClient] sources.dsl.elems.Elems.set_speech'
        count = 0
        for block in self.blocks:
            if SPEECH.is_speech(block.text):
                count += 1
                block.type = 'speech'
                block.speech = block.text
        rep.matches(f, count)
    
    def set_subjects(self):
        f = '[MClient] sources.dsl.elems.Elems.set_subjects'
        count = 0
        for block in self.blocks:
            subjf = SUBJECTS.expand(block.text)
            if subjf != block.text:
                count += 1
                block.type = 'subj'
                block.subj = block.text
                block.subjf = subjf
        rep.matches(f, count)

    def fix_cellnos(self):
        ''' By design, fixed blocks can lie within the same cell in DSL.
            We force incrementing block.cellno here. By the same reason, we
            cannot increment cellno only on the basis of fixed blocks.
        '''
        f = '[MClient] sources.dsl.elems.Elems.fix_cellnos'
        cellno = 0
        count = 0
        for block in self.blocks:
            if is_block_fixed(block) or block.type == 'phrase':
                count += 1
                cellno += 0.01
                block.cellno = cellno
            else:
                cellno = block.cellno
        rep.matches(f, count)
    
    def delete_trash(self):
        f = '[MClient] sources.dsl.elems.Elems.delete_trash'
        old_len = len(self.blocks)
        self.blocks = [block for block in self.blocks \
                      if not block.text.strip() in ('-', ',', ';', 'See:', 'см. тж')]
        rep.matches(f, old_len - len(self.blocks))
    
    def move_phrases(self):
        f = '[MClient] sources.dsl.elems.Elems.move_phrases'
        ''' Unlike other sources, we can move phrases directly to the bottom
            without taking into account blocks with the same cellno.
        '''
        phrases = [copy.deepcopy(block) for block in self.blocks \
                  if block.type == 'phrase']
        if not phrases:
            rep.lazy(f)
            return
        self.separate_refs()
        for block in self.blocks:
            if block.type == 'phrase':
                block.type = 'comment'
        phsubj = Block()
        phsubj.text = _('{} phrases').format(len(phrases))
        phsubj.type = 'phsubj'
        self.blocks += [phsubj] + phrases
    
    def separate_refs(self):
        f = '[MClient] sources.dsl.elems.Elems.separate_refs'
        count = 0
        i = 1
        while i < len(self.blocks):
            if self.blocks[i-1].type == 'phrase' \
            and self.blocks[i].type == 'phrase':
                text = self.blocks[i-1].text.strip()
                if not text or text[-1] in punc_array:
                    i += 1
                    continue
                count += 1
                self.blocks[i-1].text = self.blocks[i-1].text + ', '
            i += 1
        rep.matches(f, count)
    
    def delete_backslash(self):
        for block in self.blocks:
            block.text = block.text.replace(r'\[', r'[').replace(r'\]', r']')
    
    def set_source(self):
        for block in self.blocks:
            block.source = 'Lingvo (.dsl)'
    
    def run(self):
        f = '[MClient] sources.dsl.elems.Elems.run'
        if not self.Success:
            rep.cancel(f)
            return []
        self.fix_transc()
        self.delete_trash()
        self.delete_numeration()
        self.delete_backslash()
        self.set_speech()
        self.set_subjects()
        self.set_source()
        #self.move_phrases()
        self.fix_cellnos()
        self.fill()
        return self.blocks
    
    def debug(self, maxrow=70, maxrows=1000):
        f = '[MClient] sources.dsl.elems.Elems.debug'
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
