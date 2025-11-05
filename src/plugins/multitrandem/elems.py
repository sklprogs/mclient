#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.logic import Input, Text, digits, punc_array
from skl_shared.table import Table
from skl_shared.list import List

from instance import Block


class Elems:

    def __init__(self, blocks, abbr, langs=[], search=''):
        f = '[MClient] plugins.multitrandem.elems.Elems.__init__'
        self.art_subj = {}
        self.Parallel = False
        self.Separate = False
        self.abbr = abbr
        self.langs = langs
        self.pattern = search.strip()
        if blocks:
            self.Success = True
            self.blocks = blocks
        else:
            self.Success = False
            rep.empty(f)
            self.blocks = []
    
    def _get_pair(self, text):
        f = '[MClient] plugins.multitrandem.elems.Elems._get_pair'
        code = Input(f, text).get_integer()
        return self.abbr.get_pair(code)
    
    def _check_dic_codes(self, text):
        # Emptyness check is performed before that
        if text[0] == ' ' or text[-1] == ' ' or '  ' in text:
            return
        if set(text) == {' '}:
            return
        pattern = digits + ' '
        for sym in text:
            if not sym in pattern:
                return
        return True
    
    def set_dic_titles(self):
        f = '[MClient] plugins.multitrandem.elems.Elems.set_dic_titles'
        if not self.abbr:
            rep.empty(f)
            return
        if not self.abbr.Success:
            rep.cancel(f)
            return
        for block in self.blocks:
            if block.type != 'subj' or not block.text:
                continue
            if not self._check_dic_codes(block.text):
                mes = _('Wrong input data: "{}"!').format(block.text)
                Message(f, mes).show_warning()
                continue
            abbr = []
            full = []
            dics = block.text.split(' ')
            for dic in dics:
                pair = self._get_pair(dic)
                if pair:
                    abbr.append(pair[0])
                    full.append(pair[1])
                else:
                    rep.empty(f)
            abbr = '; '.join(abbr)
            full = '; '.join(full)
            block.text = abbr
            block.subj = abbr
            block.subjf = full
    
    def strip(self):
        for block in self.blocks:
            block.text = block.text.strip()
    
    def set_art_subj(self):
        f = '[MClient] plugins.multitrandem.elems.Elems.set_art_subj'
        count = 0
        for block in self.blocks:
            if block.type in ('subj', 'phsubj') and block.subj and block.subjf:
                count += 1
                self.art_subj[block.subj] = block.subjf
                self.art_subj[block.subjf] = block.subj
        rep.matches(f, count)
    
    def set_cellnos(self):
        cellno = 0
        cellnos = [0]
        i = 1
        while i < len(self.blocks):
            if self.blocks[i-1].cellno != self.blocks[i].cellno:
                cellno += 1
            cellnos.append(cellno)
            i += 1
        for i in range(len(self.blocks)):
            self.blocks[i].cellno = cellnos[i]
    
    def _get_wforms(self):
        return set([block.text for block in self.blocks if block.type == 'wform'])
    
    def remove_dupl_wforms(self):
        f = '[MClient] plugins.multitrandem.elems.Elems.remove_dupl_wforms'
        wforms = self._get_wforms()
        if not wforms:
            rep.lazy(f)
            return
        blocks = [block for block in self.blocks \
                  if not (block.type == 'term' and block.text in wforms)]
        rep.deleted(f, len(self.blocks) - len(blocks))
        self.blocks = blocks
    
    def run(self):
        f = '[MClient] plugins.multitrandem.elems.Elems.run'
        if not self.Success:
            rep.cancel(f)
            return self.blocks
        # Do some cleanup
        self.strip()
        # Prepare contents
        self.set_dic_titles()
        self.add_brackets()
        self.remove_dupl_wforms()
        # Prepare for cells
        self.fill()
        self.remove_fixed()
        self.insert_fixed()
        self.set_cellnos()
        # Extra spaces in the beginning may cause sorting problems
        self.add_space()
        #TODO: expand parts of speech (n -> noun, etc.)
        return self.blocks
    
    def debug(self, maxrow=20, maxrows=0):
        f = 'plugins.multitrandem.elems.Elems.debug'
        headers = ('NO', 'TYPE', 'CELLNO', 'SUBJ', 'TEXT')
        rows = []
        for i in range(len(self.blocks)):
            rows.append([i+1, self.blocks[i].type, self.blocks[i].cellno
                       ,self.blocks[i].subj, self.blocks[i].text])
        mes = Table(headers=headers, iterable=rows, maxrow=maxrow
                   ,maxrows=maxrows, Transpose=True).run()
        return f'{f}:\n{mes}'
        
    def set_transc(self):
        pass
        #block.type = 'transc'
    
    def add_brackets(self):
        i = 1
        while i < len(self.blocks):
            if self.blocks[i].type in ('comment', 'user', 'correction'):
                self.blocks[i].cellno = self.blocks[i-1].cellno
                if not self.blocks[i].text.startswith('(') \
                and not self.blocks[i].text.endswith(')'):
                    self.blocks[i].text = '(' + self.blocks[i].text + ')'
            i += 1
    
    def add_space(self):
        i = 1
        while i < len(self.blocks):
            if self.blocks[i-1].cellno != self.blocks[i].cellno:
                i += 1
                continue
            cond = False
            if i > 0 and self.blocks[i-1].text:
                if self.blocks[i-1].text[-1] in ['(', '[', '{']:
                    cond = True
            if self.blocks[i].text and not self.blocks[i].text[0].isspace() \
            and not self.blocks[i].text[0] in punc_array \
            and not self.blocks[i].text[0] in [')', ']', '}'] and not cond:
                self.blocks[i].text = ' ' + self.blocks[i].text
            i += 1
                
    def fill(self):
        dic = dicf = wform = speech = transc = term = ''
        
        # Find first non-empty values and set them as default
        for block in self.blocks:
            if block.type == 'subj':
                dic = block.subj
                dicf = block.subjf
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
            if block.type == 'term' or block.type == 'phrase':
                term = block.text
                break
        
        for block in self.blocks:
            if block.type == 'subj':
                dic = block.subj
                dicf = block.subjf
            elif block.type == 'wform':
                wform = block.text
            elif block.type == 'speech':
                speech = block.text
            elif block.type == 'transc':
                transc = block.text
                ''' #TODO: Is there a difference if we use both term/phrase
                    here or the term only?
                '''
            elif block.type in ('term', 'phrase'):
                term = block.text
            block.subj = dic
            block.subjf = dicf
            block.wform = wform
            block.speech = speech
            block.transc = transc
                
    def insert_fixed(self):
        subj = wform = speech = ''
        i = 0
        cellno = 0
        while i < len(self.blocks):
            if subj != self.blocks[i].subj or wform != self.blocks[i].wform \
            or speech != self.blocks[i].speech:
                
                if i > 0:
                    cellno = self.blocks[i-1].cellno
                
                block = Block()
                block.type = 'speech'
                block.text = self.blocks[i].speech
                block.subj = self.blocks[i].subj
                block.subjf = self.blocks[i].subjf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                cellno += 0.01
                block.cellno = cellno
                self.blocks.insert(i, block)
                
                block = Block()
                block.type = 'transc'
                block.text = self.blocks[i].transc
                block.subj = self.blocks[i].subj
                block.subjf = self.blocks[i].subjf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                cellno += 0.01
                block.cellno = cellno
                self.blocks.insert(i, block)

                block = Block()
                block.type = 'wform'
                block.text = self.blocks[i].wform
                block.subj = self.blocks[i].subj
                block.subjf = self.blocks[i].subjf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                cellno += 0.01
                block.cellno = cellno
                self.blocks.insert(i, block)
                
                block = Block()
                block.type = 'subj'
                block.text = self.blocks[i].subj
                block.subj = self.blocks[i].subj
                block.subjf = self.blocks[i].subjf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                cellno += 0.01
                block.cellno = cellno
                self.blocks.insert(i, block)
                
                subj = self.blocks[i].subj
                wform = self.blocks[i].wform
                speech = self.blocks[i].speech
                i += 4
            i += 1
            
    def remove_fixed(self):
        self.blocks = [block for block in self.blocks if block.type \
                      not in ('subj', 'wform', 'transc', 'speech')]