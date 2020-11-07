#!/usr/bin/python3
# -*- coding: UTF-8 -*-

''' This module prepares blocks after extracting tags for permanently
    storing in DB.
    Needs attributes in blocks: TYPE, DIC, WFORM, SPEECH, TRANSC,
    TERM, SAMECELL
    Modifies attributes:        TYPE, TEXT, DIC, WFORM, SPEECH,
    TRANSC, TERM, SAMECELL
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
        # Applies to non-blocked cells only
        self.cellno = -1
        self.dic = ''
        self.dicf = ''
        self.dprior = 0
        self.first = -1
        self.i = -1
        self.j = -1
        self.last = -1
        self.no = -1
        self.same = -1
        ''' 'select' is an attribute of a *cell* which is valid
            if the cell has a non-blocked block of types 'term',
            'phrase' or 'transc'
        '''
        self.select = -1
        self.speech = ''
        self.sprior = -1
        self.term = ''
        self.text = ''
        ''' 'comment', 'correction', 'dic', 'invalid', 'phrase',
            'speech', 'term', 'transc', 'wform'
        '''
        self.type_ = 'comment'
        self.transc = ''
        self.url = ''
        self.wform = ''



class Elems:
    ''' Process blocks before dumping to DB.
        About filling 'term':
        - We fill 'term' from the start in order to ensure the correct
          'term' value for blocks having 'same == 1'
        - We fill 'term' from the end in order to ensure that 'term'
          of blocks of non-selectable types will have the value of
          the 'term' AFTER those blocks
        - We fill 'term' from the end in order to ensure that 'term'
          is also filled for blocks having 'same == 0'
        - When filling 'term' from the start to the end, in order
          to set a default 'term' value, we also search for blocks of
          the 'phrase' type (just to be safe in such cases when
          'phrase' blocks anticipate 'term' blocks). However, we fill
          'term' for 'phrase' blocks from the end to the start because
          we want the 'phrase' dictionary to have the 'term' value of
          the first 'phrase' block AFTER it
        - Finally, we clear TERM values for fixed columns. Sqlite
          sorts '' before a non-empty string, so we ensure thereby that
          sorting by TERM will be correct. Otherwise, we would have to
          correctly calculate TERM values for fixed columns that will
          vary depending on the view. Incorrect sorting by TERM may
          result in putting a 'term' item before fixed columns.
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
    
    def delete_trash(self):
        self.blocks = [block for block in self.blocks \
                       if block.text != ','
                      ]
    
    def divide_block(self):
        sep1 = ' || '
        sep2 = '; '
        i = 0
        while i < len(self.blocks):
            if sep1 in self.blocks[i].text \
            or sep2 in self.blocks[i].text:
                text = self.blocks[i].text
                text = text.replace(sep2,sep1)
                split = text.split(sep1)
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
            self.delete_trash()
            self.add_space()
            self.fill()
            self.fill_term()
            self.remove_fixed()
            self.insert_fixed()
            self.set_fixed_term()
            self.set_selectables()
            self.set_same()
            self.debug()
            return self.blocks
        else:
            sh.com.cancel(f)
    
    def debug(self,maxrow=20,maxrows=1000):
        f = '[MClient] plugins.dsl.elems.Elems.debug'
        if self.Debug and self.blocks:
            headers = ('NO','DIC','DICF','WFORM'
                      ,'SPEECH','TRANSC','TYPE'
                      ,'TEXT','SAME','SELECT'
                      )
            rows = []
            for i in range(len(self.blocks)):
                rows.append ([i + 1
                             ,self.blocks[i].dic
                             ,self.blocks[i].dicf
                             ,self.blocks[i].wform
                             ,self.blocks[i].speech
                             ,self.blocks[i].transc
                             ,self.blocks[i].type_
                             ,self.blocks[i].text
                             ,self.blocks[i].same
                             ,self.blocks[i].select
                             ]
                            )
            mes = sh.FastTable (headers = headers
                               ,iterable = rows
                               ,maxrow = maxrow
                               ,maxrows = maxrows
                               ,Transpose = True
                               ).run()
            mes = _('Non-DB blocks:') + '\n\n' + mes
            sh.com.run_fast_debug(f,mes)
        else:
            sh.com.rep_lazy(f)
    
    def add_space(self):
        f = '[MClient] plugins.dsl.elems.Elems.add_space'
        count = 0
        i = 1
        while i < len(self.blocks):
            if self.blocks[i].same > 0:
                if self.blocks[i].text \
                  and not self.blocks[i].text[0].isspace() \
                  and not self.blocks[i].text[0] in sh.lg.punc_array \
                  and not self.blocks[i].text[0] in [')',']','}'] \
                  and not self.blocks[i-1].text[-1] in ['(','[','{']:
                      count += 1
                      self.blocks[i].text = ' ' + self.blocks[i].text
            i += 1
        if count:
            mes = _('{} matches').format(count)
            sh.objs.get_mes(f,mes,True).show_debug()

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
                # There is no separate section for phrases
                block.select = 0
                mes = _('{} phrases').format(count)
                block.text = block.dic = block.dicf = mes
                self.blocks.insert(i,block)
                return True
                
    def fill(self):
        dic = dicf = wform = speech = transc = term = ''
        
        # Find first non-empty values and set them as default
        for block in self.blocks:
            if block.type_ == 'dic':
                dic = dicf = block.text
                break
        for block in self.blocks:
            if block.type_ == 'wform':
                wform = block.text
                break
        for block in self.blocks:
            if block.type_ == 'speech':
                speech = block.text
                break
        for block in self.blocks:
            if block.type_ == 'transc':
                transc = block.text
                break
        for block in self.blocks:
            if block.type_ == 'term' or block.type_ == 'phrase':
                term = block.text
                break
        
        for block in self.blocks:
            if block.type_ == 'dic':
                dic = dicf = block.text
            elif block.type_ == 'wform':
                wform = block.text
            elif block.type_ == 'speech':
                speech = block.text
            elif block.type_ == 'transc':
                transc = block.text
                ''' #TODO: Is there a difference if we use both
                    term/phrase here or the term only?
                '''
            elif block.type_ in ('term','phrase'):
                term = block.text
            block.dic = block.dicf = dic.strip()
            block.wform = wform
            block.speech = speech
            block.transc = transc
            if block.same > 0:
                block.term = term
    
    def fill_term(self):
        term = ''
        ''' This is just to get a non-empty value of 'term' if some
            other types besides 'phrase' and 'term' follow them in the
            end.
        '''
        i = len(self.blocks) - 1
        while i >= 0:
            if self.blocks[i].type_ in ('term','phrase'):
                term = self.blocks[i].text
                break
            i -= 1
        i = len(self.blocks) - 1
        while i >= 0:
            if self.blocks[i].type_ in ('term','phrase'):
                term = self.blocks[i].text
            if not self.blocks[i].same > 0:
                self.blocks[i].term = term
            i -= 1
            
    def set_fixed_term(self):
        for block in self.blocks:
            if block.type_ in ('dic','wform','speech','transc'):
                block.term = ''
                
    def insert_fixed(self):
        dic = dicf = wform = speech = ''
        i = 0
        while i < len(self.blocks):
            if dic != self.blocks[i].dic \
            or dicf != self.blocks[i].dicf \
            or wform != self.blocks[i].wform \
            or speech != self.blocks[i].speech:
                
                block = Block()
                block.type_ = 'speech'
                block.text = self.blocks[i].speech
                block.dic = self.blocks[i].dic
                block.dicf = self.blocks[i].dicf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                block.term = self.blocks[i].term
                block.same = 0
                self.blocks.insert(i,block)
                
                block = Block()
                block.type_ = 'transc'
                block.text = self.blocks[i].transc
                block.dic = self.blocks[i].dic
                block.dicf = self.blocks[i].dicf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                block.term = self.blocks[i].term
                block.same = 0
                self.blocks.insert(i,block)

                block = Block()
                block.type_ = 'wform'
                block.text = self.blocks[i].wform
                block.dic = self.blocks[i].dic
                block.dicf = self.blocks[i].dicf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                block.term = self.blocks[i].term
                block.same = 0
                self.blocks.insert(i,block)
                
                block = Block()
                block.type_ = 'dic'
                block.text = self.blocks[i].dic
                block.dic = self.blocks[i].dic
                block.dicf = self.blocks[i].dicf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                block.term = self.blocks[i].term
                block.same = 0
                self.blocks.insert(i,block)
                
                dic = self.blocks[i].dic
                dicf = self.blocks[i].dicf
                wform = self.blocks[i].wform
                speech = self.blocks[i].speech
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
