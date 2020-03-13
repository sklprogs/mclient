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
        self.abbr      = iabbr
        self.Debug     = Debug
        self.Shorten   = Shorten
        self.MaxRow    = MaxRow
        self.MaxRows   = MaxRows
        self._search   = search.strip()
        self._langs    = langs
        if blocks:
            self.Success = True
            self._blocks = blocks
        else:
            self.Success = False
            sh.com.empty(f)
            self._blocks = []
    
    def _get_pair(self,text):
        f = '[MClient] plugins.multitranbin.elems.Elems._get_pair'
        code = sh.Input (title = f
                        ,value = text
                        ).integer()
        return self.abbr.get_pair(code)
    
    def _check_dic_codes(self,text):
        # Emptyness check is performed before that
        if text[0] == ' ' or text[-1] == ' ' or '  ' in text:
            return
        if set(text) == {' '}:
            return
        pattern = sh.lg.digits + ' '
        for sym in text:
            if not sym in pattern:
                return
        return True
    
    def set_dic_titles(self):
        f = '[MClient] plugins.multitranbin.elems.Elems.set_dic_titles'
        if self.abbr:
            if self.abbr.Success:
                for block in self._blocks:
                    if block._type == 'dic' and block._text:
                        if self._check_dic_codes(block._text):
                            abbr = []
                            full = []
                            dics = block._text.split(' ')
                            for dic in dics:
                                pair = self._get_pair(dic)
                                if pair:
                                    abbr.append(pair[0])
                                    full.append(pair[1])
                                else:
                                    sh.com.empty(f)
                            abbr = '; '.join(abbr)
                            full = '; '.join(full)
                            block._text  = abbr
                            block._dica  = abbr
                            block._dicaf = full
                        else:
                            mes = _('Wrong input data: "{}"!')
                            mes = mes.format(block._text)
                            sh.objs.mes(f,mes,True).warning()
            else:
                sh.com.cancel(f)
        else:
            sh.com.empty(f)
    
    def strip(self):
        for block in self._blocks:
            block._text = block._text.strip()
    
    def run(self):
        f = '[MClient] plugins.multitranbin.elems.Elems.run'
        if self.Success:
            # Do some cleanup
            self.strip()
            '''
            # Reassign types
            self.transc()
            self.users()
            self.phrases()
            self.corrections()
            self.definitions()
            '''
            # Prepare contents
            self.set_dic_titles()
            self.add_brackets()
            self.user_brackets()
            # Prepare for cells
            self.fill()
            self.remove_fixed()
            self.insert_fixed()
            # Extra spaces in the beginning may cause sorting problems
            self.add_space()
            #TODO: expand parts of speech (n -> noun, etc.)
            self.selectables()
            self.debug()
        else:
            sh.com.cancel(f)
        return self._blocks
    
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
        dica = dicaf = wforma = speecha = transca = terma = ''
        
        # Find first non-empty values and set them as default
        for block in self._blocks:
            if block._type == 'dic':
                dica  = block._dica
                dicaf = block._dicaf
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
                dica  = block._dica
                dicaf = block._dicaf
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
            block._dicaf   = dicaf
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
                block._dicaf   = self._blocks[i]._dicaf
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
                block._dicaf   = self._blocks[i]._dicaf
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
                block._dicaf   = self._blocks[i]._dicaf
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
                block._dicaf   = self._blocks[i]._dicaf
                block._wforma  = self._blocks[i]._wforma
                block._speecha = self._blocks[i]._speecha
                block._transca = self._blocks[i]._transca
                block._terma   = self._blocks[i]._terma
                block._same    = 0
                self._blocks.insert(i,block)
                
                dica    = self._blocks[i]._dica
                dicaf   = self._blocks[i]._dicaf
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


if __name__ == '__main__':
    f = '[MClient] plugins.multitranbin.elems.__main__'
    search = 'phrenosin'
    import get  as gt
    import tags as tg
    iget   = gt.Get(search)
    chunks = iget.run()
    if not chunks:
        chunks = []
    blocks = []
    for chunk in chunks:
        add = tg.Tags (chunk = chunk
                      ,Debug = True
                      ).run()
        if add:
            blocks += add
    blocks = Elems (blocks = blocks
                   ,iabbr  = None
                   ,langs  = gt.objs.all_dics().langs()
                   ,search = search
                   ,Debug  = True
                   ).run()
    for i in range(len(blocks)):
        mes = '{}: {}: "{}"'.format (i,blocks[i]._type
                                    ,blocks[i]._text
                                    )
        print(mes)
