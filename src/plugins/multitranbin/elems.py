#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import skl_shared.shared as sh
from skl_shared.localize import _



# A copy of Tags.Block
class Block:
    
    def __init__(self):
        self._block    = -1
        self.i         = -1
        self.j         = -1
        self._first    = -1
        self._last     = -1
        self._no       = -1
        # Applies to non-blocked cells only
        self._cell_no  = -1
        self._same     = -1
        ''' '_select' is an attribute of a *cell* which is valid
            if the cell has a non-blocked block of types 'term',
            'phrase' or 'transc'
        '''
        self._select   = -1
        self._priority = 0
        ''' 'wform', 'speech', 'dic', 'phrase', 'term', 'comment',
            'correction', 'transc', 'user', 'invalid'
        '''
        self._type    = 'invalid'
        self._text    = ''
        self._url     = ''
        self._dica    = ''
        self._dicaf   = ''
        self._wforma  = ''
        self._speecha = ''
        self._transca = ''
        self._terma   = ''



class Elems:
    # Process blocks before dumping to DB
    def __init__ (self,blocks,iabbr,langs
                 ,Debug=False,Shorten=True
                 ,MaxRow=20,MaxRows=20,search=''
                 ):
        f = '[MClient] plugins.multitranbin.elems.Elems.__init__'
        self._dic_urls = {}
        self._defins   = []
        self._blocks   = blocks
        self.abbr      = iabbr
        self.Debug     = Debug
        self.Shorten   = Shorten
        self.MaxRow    = MaxRow
        self.MaxRows   = MaxRows
        self._search   = search.strip()
        self._langs    = langs
        if self._blocks:
            self.Success = True
        else:
            self.Success = False
            sh.com.empty(f)
    
    def strip(self):
        for block in self._blocks:
            block._text = block._text.strip()
    
    def run(self):
        f = '[MClient] plugins.multitranbin.elems.Elems.run'
        if self.Success:
            # Do some cleanup
            self.strip()
            self.selectables()
            self.debug()
            return self._blocks
        else:
            sh.com.cancel(f)
    
    def debug(self):
        f = 'plugins.multitranbin.elems.Elems.debug'
        if self.Debug:
            mes = _('Debug table:')
            sh.objs.mes(f,mes,True).debug()
            headers = ['TYPE','TEXT','SAMECELL','CELLNO','ROWNO','COLNO'
                      ,'POS1','POS2'
                      ]
            rows = []
            for block in self._blocks:
                rows.append ([block._type,block._text,block._same
                             ,block._cell_no,block.i,block.j
                             ,block._first,block._last
                             ]
                            )
            sh.Table (headers = headers
                     ,rows    = rows
                     ,Shorten = self.Shorten
                     ,MaxRow  = self.MaxRow
                     ,MaxRows = self.MaxRows
                     ).print()
        
    def transc(self):
        pass
        #block._type = 'transc'
    
    def add_brackets(self):
        for block in self._blocks:
            if block._type in ('comment','correction') \
            and '(' in block._text and not ')' in block._text:
                block._text += ')'
    
    def user_brackets(self):
        for block in self._blocks:
            if block._type == 'user':
                if not block._text.startswith('('):
                    block._text = '(' + block._text
                if not block._text.endswith(')'):
                    block._text += ')'
    
    def add_space(self):
        for i in range(len(self._blocks)):
            if self._blocks[i]._same > 0:
                cond = False
                if i > 0 and self._blocks[i-1]._text:
                    if self._blocks[i-1]._text[-1] in ['(','[','{']:
                        cond = True
                if self._blocks[i]._text \
                  and not self._blocks[i]._text[0].isspace() \
                  and not self._blocks[i]._text[0] in sh.lg.punc_array \
                  and not self._blocks[i]._text[0] in [')',']','}'] \
                  and not cond:
                    self._blocks[i]._text = ' ' + self._blocks[i]._text
                
    def fill(self):
        dica = wforma = speecha = transca = terma = ''
        
        # Find first non-empty values and set them as default
        for block in self._blocks:
            if block._type == 'dic':
                dica = block._text
                break
        for block in self._blocks:
            if block._type == 'wform':
                wforma = block._text
                break
        for block in self._blocks:
            if block._type == 'speech':
                speecha = block._text
                break
        for block in self._blocks:
            if block._type == 'transc':
                transca = block._text
                break
        for block in self._blocks:
            if block._type == 'term' or block._type == 'phrase':
                terma = block._text
                break
        
        for block in self._blocks:
            if block._type == 'dic':
                dica = block._text
            elif block._type == 'wform':
                wforma = block._text
            elif block._type == 'speech':
                speecha = block._text
            elif block._type == 'transc':
                transca = block._text
                ''' #todo: Is there a difference if we use both
                    term/phrase here or the term only?
                '''
            elif block._type in ('term','phrase'):
                terma = block._text
            block._dica    = dica
            block._wforma  = wforma
            block._speecha = speecha
            block._transca = transca
            if block._same > 0:
                block._terma = terma
                
    def insert_fixed(self):
        dica = wforma = speecha = ''
        i = 0
        while i < len(self._blocks):
            if dica != self._blocks[i]._dica \
            or wforma != self._blocks[i]._wforma \
            or speecha != self._blocks[i]._speecha:
                
                block          = Block()
                block._type    = 'speech'
                block._text    = self._blocks[i]._speecha
                block._dica    = self._blocks[i]._dica
                block._wforma  = self._blocks[i]._wforma
                block._speecha = self._blocks[i]._speecha
                block._transca = self._blocks[i]._transca
                block._terma   = self._blocks[i]._terma
                block._same    = 0
                self._blocks.insert(i,block)
                
                block          = Block()
                block._type    = 'transc'
                block._text    = self._blocks[i]._transca
                block._dica    = self._blocks[i]._dica
                block._wforma  = self._blocks[i]._wforma
                block._speecha = self._blocks[i]._speecha
                block._transca = self._blocks[i]._transca
                block._terma   = self._blocks[i]._terma
                block._same    = 0
                self._blocks.insert(i,block)

                block          = Block()
                block._type    = 'wform'
                block._text    = self._blocks[i]._wforma
                block._dica    = self._blocks[i]._dica
                block._wforma  = self._blocks[i]._wforma
                block._speecha = self._blocks[i]._speecha
                block._transca = self._blocks[i]._transca
                block._terma   = self._blocks[i]._terma
                block._same    = 0
                self._blocks.insert(i,block)
                
                block          = Block()
                block._type    = 'dic'
                block._text    = self._blocks[i]._dica
                block._dica    = self._blocks[i]._dica
                block._wforma  = self._blocks[i]._wforma
                block._speecha = self._blocks[i]._speecha
                block._transca = self._blocks[i]._transca
                block._terma   = self._blocks[i]._terma
                block._same    = 0
                self._blocks.insert(i,block)
                
                dica    = self._blocks[i]._dica
                wforma  = self._blocks[i]._wforma
                speecha = self._blocks[i]._speecha
                i += 4
            i += 1
            
    def remove_fixed(self):
        self._blocks = [block for block in self._blocks if block._type \
                        not in ('dic','wform','transc','speech')
                       ]
                       
    def selectables(self):
        # block._no is set only after creating DB
        for block in self._blocks:
            if block._type in ('phrase','term','transc') \
            and block._text and block._select < 1:
                block._select = 1
            else:
                block._select = 0
