#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import skl_shared2.shared as sh
from skl_shared2.localize import _



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
        ''' '_select' is an attribute of a *cell* which is valid
            if the cell has a non-blocked block of types 'term',
            'phrase' or 'transc'
        '''
        self.select   = -1
        self.priority = 0
        ''' 'wform', 'speech', 'dic', 'phrase', 'term', 'comment',
            'correction', 'transc', 'user', 'invalid'
        '''
        self.type_   = 'invalid'
        self.text    = ''
        self.url     = ''
        self.dica    = ''
        self.dicaf   = ''
        self.wforma  = ''
        self.speecha = ''
        self.transca = ''
        self.terma   = ''
        self.lang    = 0



class Elems:
    # Process blocks before dumping to DB
    def __init__ (self,blocks,iabbr,langs=[]
                 ,Debug=False,Shorten=True
                 ,MaxRow=20,MaxRows=20,search=''
                 ):
        f = '[MClient] plugins.multitrandem.elems.Elems.__init__'
        self.dicurls = {}
        self.defins  = []
        self.abbr    = iabbr
        self.Debug   = Debug
        self.Shorten = Shorten
        self.MaxRow  = MaxRow
        self.MaxRows = MaxRows
        self.pattern = search.strip()
        self.langs   = langs
        if blocks:
            self.Success = True
            self.blocks = blocks
        else:
            self.Success = False
            sh.com.rep_empty(f)
            self.blocks = []
    
    def reorder(self):
        if len(self.blocks) > 1:
            pos = -1
            for i in range(len(self.blocks)):
                if self.blocks[i].type_ == 'dic':
                    pos = i
                    break
            if pos >= 0:
                self.blocks.append(self.blocks[pos])
                del self.blocks[pos]
            pos = -1
            for i in range(len(self.blocks)):
                if self.blocks[i].type_ == 'comment':
                    pos = i
                    break
            if pos >= 0:
                self.blocks.append(self.blocks[pos])
                del self.blocks[pos]
            if sh.Text(self.pattern).has_cyrillic():
                for i in range(len(self.blocks)):
                    if self.blocks[i-1].type_ == 'term' \
                    and self.blocks[i].type_ == 'term' \
                    and self.blocks[i-1].lang != 2 \
                    and self.blocks[i].lang == 2:
                        self.blocks[i-1], self.blocks[i] = self.blocks[i], self.blocks[i-1]
    
    def _get_pair(self,text):
        f = '[MClient] plugins.multitrandem.elems.Elems._get_pair'
        code = sh.Input(f,text).get_integer()
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
        f = '[MClient] plugins.multitrandem.elems.Elems.set_dic_titles'
        if self.abbr:
            if self.abbr.Success:
                for block in self.blocks:
                    if block.type_ == 'dic' and block.text:
                        if self._check_dic_codes(block.text):
                            abbr = []
                            full = []
                            dics = block.text.split(' ')
                            for dic in dics:
                                pair = self._get_pair(dic)
                                if pair:
                                    abbr.append(pair[0])
                                    full.append(pair[1])
                                else:
                                    sh.com.rep_empty(f)
                            abbr = '; '.join(abbr)
                            full = '; '.join(full)
                            block.text  = abbr
                            block.dica  = abbr
                            block.dicaf = full
                        else:
                            mes = _('Wrong input data: "{}"!')
                            mes = mes.format(block.text)
                            sh.objs.get_mes(f,mes,True).show_warning()
            else:
                sh.com.cancel(f)
        else:
            sh.com.rep_empty(f)
    
    def strip(self):
        for block in self.blocks:
            block.text = block.text.strip()
    
    def run(self):
        f = '[MClient] plugins.multitrandem.elems.Elems.run'
        if self.Success:
            # Do some cleanup
            self.strip()
            # Prepare contents
            self.reorder()
            self.set_dic_titles()
            self.add_brackets()
            # Prepare for cells
            self.fill()
            self.remove_fixed()
            self.insert_fixed()
            # Extra spaces in the beginning may cause sorting problems
            self.add_space()
            #TODO: expand parts of speech (n -> noun, etc.)
            self.set_selectables()
            self.debug()
        else:
            sh.com.cancel(f)
        return self.blocks
    
    def debug(self):
        f = 'plugins.multitrandem.elems.Elems.debug'
        if self.Debug:
            mes = _('Debug table:')
            sh.objs.get_mes(f,mes,True).show_debug()
            headers = ['TYPE','TEXT','SAMECELL','CELLNO','ROWNO','COLNO'
                      ,'POS1','POS2'
                      ]
            rows = []
            for block in self.blocks:
                rows.append ([block.type_,block.text,block.same
                             ,block.cellno,block.i,block.j
                             ,block.first,block.last
                             ]
                            )
            sh.Table (headers = headers
                     ,rows    = rows
                     ,Shorten = self.Shorten
                     ,MaxRow  = self.MaxRow
                     ,MaxRows = self.MaxRows
                     ).print()
        
    def set_transc(self):
        pass
        #block.type_ = 'transc'
    
    def add_brackets(self):
        for block in self.blocks:
            if block.type_ in ('comment','user','correction'):
                block.same = 1
                if not block.text.startswith('(') \
                and not block.text.endswith(')'):
                    block.text = '(' + block.text + ')'
    
    def add_space(self):
        for i in range(len(self.blocks)):
            if self.blocks[i].same > 0:
                cond = False
                if i > 0 and self.blocks[i-1].text:
                    if self.blocks[i-1].text[-1] in ['(','[','{']:
                        cond = True
                if self.blocks[i].text \
                  and not self.blocks[i].text[0].isspace() \
                  and not self.blocks[i].text[0] in sh.lg.punc_array \
                  and not self.blocks[i].text[0] in [')',']','}'] \
                  and not cond:
                    self.blocks[i].text = ' ' + self.blocks[i].text
                
    def fill(self):
        dica = dicaf = wforma = speecha = transca = terma = ''
        
        # Find first non-empty values and set them as default
        for block in self.blocks:
            if block.type_ == 'dic':
                dica  = block.dica
                dicaf = block.dicaf
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
                dica  = block.dica
                dicaf = block.dicaf
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
            block.dica    = dica
            block.dicaf   = dicaf
            block.wforma  = wforma
            block.speecha = speecha
            block.transca = transca
            if block.same > 0:
                block.terma = terma
                
    def insert_fixed(self):
        dica = wforma = speecha = ''
        i = 0
        while i < len(self.blocks):
            if dica != self.blocks[i].dica \
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


if __name__ == '__main__':
    f = '[MClient] plugins.multitrandem.elems.__main__'
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
                   ,search = search
                   ,Debug  = True
                   ).run()
    for i in range(len(blocks)):
        mes = '{}: {}: "{}"'.format (i,blocks[i].type_
                                    ,blocks[i].text
                                    )
        print(mes)
