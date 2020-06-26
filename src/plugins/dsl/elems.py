#!/usr/bin/python3
# -*- coding: UTF-8 -*-

''' This module prepares blocks after extracting tags for permanently
    storing in DB.
    Needs attributes in blocks: TYPE, DICA, WFORMA, SPEECHA, TRANSCA,
    TERMA, SAMECELL
    Modifies attributes:        TYPE, TEXT, DICA, WFORMA, SPEECHA,
    TRANSCA, TERMA, SAMECELL
    SAMECELL is based on Tags and TYPE and is filled fully
    SELECTABLE cannot be filled because it depends on CELLNO which is
    created in Cells; Cells modifies TEXT of DIC, WFORM, SPEECH, TRANSC
    types, and we do not need to make empty cells SELECTABLE, so we
    calculate SELECTABLE fully in Cells.
'''

import copy
import skl_shared.shared as sh
from skl_shared.localize import _



# A copy of Tags.Block
class Block:
    
    def __init__(self):
        self.block = -1
        self.i     = -1
        self.j     = -1
        self.first = -1
        self.last  = -1
        self.no    = -1
        # Applies to non-blocked cells only
        self.cellno = -1
        self.same   = -1
        ''' 'select' is an attribute of a *cell* which is valid
            if the cell has a non-blocked block of types 'term',
            'phrase' or 'transc'
        '''
        self.select   = -1
        self.priority = 0
        ''' 'wform', 'speech', 'dic', 'phrase', 'term', 'comment',
            'correction', 'transc', 'invalid'
        '''
        self.type_   = 'comment'
        self.text    = ''
        self.url     = ''
        self.dica    = ''
        self.dicaf   = ''
        self.wforma  = ''
        self.speecha = ''
        self.transca = ''
        self.terma   = ''



class Elems:
    ''' Process blocks before dumping to DB.
        About filling 'terma':
        - We fill 'terma' from the start in order to ensure the correct
          'terma' value for blocks having 'same == 1'
        - We fill 'terma' from the end in order to ensure that 'terma'
          of blocks of non-selectable types will have the value of
          the 'term' AFTER those blocks
        - We fill 'terma' from the end in order to ensure that 'terma'
          is also filled for blocks having 'same == 0'
        - When filling 'terma' from the start to the end, in order
          to set a default 'terma' value, we also search for blocks of
          the 'phrase' type (just to be safe in such cases when
          'phrase' blocks anticipate 'term' blocks). However, we fill
          'terma' for 'phrase' blocks from the end to the start because
          we want the 'phrase' dictionary to have the 'terma' value of
          the first 'phrase' block AFTER it
        - Finally, we clear TERMA values for fixed columns. Sqlite
          sorts '' before a non-empty string, so we ensure thereby that
          sorting by TERMA will be correct. Otherwise, we would have to
          correctly calculate TERMA values for fixed columns that will
          vary depending on the view. Incorrect sorting by TERMA may
          result in putting a TERM item before fixed columns.
    '''
    def __init__(self,blocks,Debug=False):
        f = '[MClient] plugins.dsl.elems.Elems.__init__'
        self.blocks = blocks
        self.Debug = Debug
        if self.blocks:
            self.Success = True
        else:
            self.Success = False
            sh.com.rep_empty(f)
    
    def divide_block(self):
        sep = ' || '
        i = 0
        while i < len(self.blocks):
            if sep in self.blocks[i].text:
                split = self.blocks[i].text.split(sep)
                block = copy.copy(self.blocks[i])
                del self.blocks[i]
                for item in split[::-1]:
                    block_copy = copy.copy(block)
                    block_copy.text = item
                    self.blocks.insert(i,block_copy)
                i = i - 1 + len(split)
            i += 1
    
    def set_same(self):
        i = 1
        while i < len(self.blocks):
            if self.blocks[i].same == -1:
                if self.blocks[i-1].type_ in ('dic','wform','transc'
                                             ,'speech'
                                             ):
                    self.blocks[i].same = 0
                elif self.blocks[i].type_ == 'comment':
                    self.blocks[i].same = 1
                else:
                    self.blocks[i].same = 0
            i += 1
    
    def run(self):
        f = '[MClient] plugins.dsl.elems.Elems.run'
        if self.Success:
            self.divide_block()
            self.set_phrase_dic()
            self.add_space()
            self.fill()
            self.fill_terma()
            self.remove_fixed()
            self.insert_fixed()
            self.set_fixed_terma()
            self.set_selectables()
            self.set_same()
            self.debug()
            return self.blocks
        else:
            sh.com.cancel(f)
    
    def debug(self,maxrow=20,maxrows=1000):
        f = '[MClient] plugins.dsl.elems.Elems.debug'
        if self.Debug and self.blocks:
            headers = ('NO','DICA','DICAF','WFORMA'
                      ,'SPEECHA','TRANSCA','TYPE'
                      ,'TEXT','SAME','SELECT'
                      )
            rows = []
            for i in range(len(self.blocks)):
                rows.append ([i + 1
                             ,self.blocks[i].dica
                             ,self.blocks[i].dicaf
                             ,self.blocks[i].wforma
                             ,self.blocks[i].speecha
                             ,self.blocks[i].transca
                             ,self.blocks[i].type_
                             ,self.blocks[i].text
                             ,self.blocks[i].same
                             ,self.blocks[i].select
                             ]
                            )
            mes = sh.FastTable (headers   = headers
                               ,iterable  = rows
                               ,maxrow    = maxrow
                               ,maxrows   = maxrows
                               ,Transpose = True
                               ).run()
            mes = _('Non-DB blocks:') + '\n\n' + mes
            sh.com.run_fast_debug(f,mes)
        else:
            sh.com.rep_lazy(f)
    
    def add_space(self):
        for i in range(len(self.blocks)):
            if self.blocks[i].same > 0:
                cond = False
                if i > 0:
                    if self.blocks[i-1].text[-1] in ['(','[','{']:
                        cond = True
                if self.blocks[i].text \
                  and not self.blocks[i].text[0].isspace() \
                  and not self.blocks[i].text[0] in sh.lg.punc_array \
                  and not self.blocks[i].text[0] in [')',']','}'] \
                  and not cond:
                    self.blocks[i].text = ' ' + self.blocks[i].text

    def set_phrase_dic(self):
        count = 0
        for block in self.blocks:
            if block.type_ == 'phrase':
                count += 1
        for i in range(len(self.blocks)):
            if self.blocks[i].type_ == 'phrase':
                block = Block()
                block.type_ = 'dic'
                block.same = 0
                block.select = 1
                mes = _('{} phrases').format(count)
                block.text = block.dica = block.dicaf = mes
                self.blocks.insert(i,block)
                return True
                
    def fill(self):
        dica = dicaf = wforma = speecha = transca = terma = ''
        
        # Find first non-empty values and set them as default
        for block in self.blocks:
            if block.type_ == 'dic':
                dica = dicaf = block.text
                break
        for block in self.blocks:
            if block.type_ == 'wform':
                wforma = block.text
                break
        for block in self.blocks:
            if block.type_ == 'speech':
                speecha = block.text
                break
        for block in self.blocks:
            if block.type_ == 'transc':
                transca = block.text
                break
        for block in self.blocks:
            if block.type_ == 'term' or block.type_ == 'phrase':
                terma = block.text
                break
        
        for block in self.blocks:
            if block.type_ == 'dic':
                dica = dicaf = block.text
            elif block.type_ == 'wform':
                wforma = block.text
            elif block.type_ == 'speech':
                speecha = block.text
            elif block.type_ == 'transc':
                transca = block.text
                ''' #TODO: Is there a difference if we use both
                    term/phrase here or the term only?
                '''
            elif block.type_ in ('term','phrase'):
                terma = block.text
            block.dica = block.dicaf = dica.strip()
            block.wforma = wforma
            block.speecha = speecha
            block.transca = transca
            if block.same > 0:
                block.terma = terma
    
    def fill_terma(self):
        terma = ''
        ''' This is just to get a non-empty value of 'terma' if some
            other types besides 'phrase' and 'term' follow them in the
            end.
        '''
        i = len(self.blocks) - 1
        while i >= 0:
            if self.blocks[i].type_ in ('term','phrase'):
                terma = self.blocks[i].text
                break
            i -= 1
        i = len(self.blocks) - 1
        while i >= 0:
            if self.blocks[i].type_ in ('term','phrase'):
                terma = self.blocks[i].text
            if not self.blocks[i].same > 0:
                self.blocks[i].terma = terma
            i -= 1
            
    def set_fixed_terma(self):
        for block in self.blocks:
            if block.type_ in ('dic','wform','speech','transc'):
                block.terma = ''
                
    def insert_fixed(self):
        dica = dicaf = wforma = speecha = ''
        i = 0
        while i < len(self.blocks):
            if dica != self.blocks[i].dica \
            or dicaf != self.blocks[i].dicaf \
            or wforma != self.blocks[i].wforma \
            or speecha != self.blocks[i].speecha:
                
                block         = Block()
                block.type_   = 'speech'
                block.text    = self.blocks[i].speecha
                block.dica    = self.blocks[i].dica
                block.dicaf   = self.blocks[i].dicaf
                block.wforma  = self.blocks[i].wforma
                block.speecha = self.blocks[i].speecha
                block.transca = self.blocks[i].transca
                block.terma   = self.blocks[i].terma
                block.same    = 0
                self.blocks.insert(i,block)
                
                block         = Block()
                block.type_   = 'transc'
                block.text    = self.blocks[i].transca
                block.dica    = self.blocks[i].dica
                block.dicaf   = self.blocks[i].dicaf
                block.wforma  = self.blocks[i].wforma
                block.speecha = self.blocks[i].speecha
                block.transca = self.blocks[i].transca
                block.terma   = self.blocks[i].terma
                block.same    = 0
                self.blocks.insert(i,block)

                block         = Block()
                block.type_   = 'wform'
                block.text    = self.blocks[i].wforma
                block.dica    = self.blocks[i].dica
                block.dicaf   = self.blocks[i].dicaf
                block.wforma  = self.blocks[i].wforma
                block.speecha = self.blocks[i].speecha
                block.transca = self.blocks[i].transca
                block.terma   = self.blocks[i].terma
                block.same    = 0
                self.blocks.insert(i,block)
                
                block         = Block()
                block.type_   = 'dic'
                block.text    = self.blocks[i].dica
                block.dica    = self.blocks[i].dica
                block.dicaf   = self.blocks[i].dicaf
                block.wforma  = self.blocks[i].wforma
                block.speecha = self.blocks[i].speecha
                block.transca = self.blocks[i].transca
                block.terma   = self.blocks[i].terma
                block.same    = 0
                self.blocks.insert(i,block)
                
                dica    = self.blocks[i].dica
                dicaf   = self.blocks[i].dicaf
                wforma  = self.blocks[i].wforma
                speecha = self.blocks[i].speecha
                i += 4
            i += 1
            
    def remove_fixed(self):
        self.blocks = [block for block in self.blocks if block.type_ \
                       not in ('dic','wform','transc','speech')
                      ]
                       
    def set_selectables(self):
        # block.no is set only after creating DB
        for block in self.blocks:
            if block.type_ in ('phrase','term','transc') \
            and block.text and block.select < 1:
                block.select = 1
            else:
                block.select = 0
