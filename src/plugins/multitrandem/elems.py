#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class Block:
    # A copy of Tags.Block
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
        self.lang = 0
        self.last = -1
        self.no = -1
        self.same = -1
        ''' '_select' is an attribute of a *cell* which is valid if the cell
            has a non-blocked block of types 'term', 'phrase' or 'transc'.
        '''
        self.select = -1
        self.speech = ''
        self.sprior = -1
        self.term = ''
        self.text = ''
        self.transc = ''
        ''' 'comment', 'correction', 'dic', 'invalid', 'phrase', 'speech',
            'term', 'transc', 'user', 'wform'.
        '''
        self.type = 'invalid'
        self.url = ''
        self.wform = ''



class Elems:
    # Process blocks before dumping to DB
    def __init__(self, blocks, abbr, langs=[], Debug=False, maxrow=20
                ,maxrows=20, search=''
                ):
        f = '[MClient] plugins.multitrandem.elems.Elems.__init__'
        self.abbr = abbr
        self.Debug = Debug
        self.defins = []
        self.dicurls = {}
        self.langs = langs
        self.maxrow = maxrow
        self.maxrows = maxrows
        self.pattern = search.strip()
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
                if self.blocks[i].type == 'dic':
                    pos = i
                    break
            if pos >= 0:
                self.blocks.append(self.blocks[pos])
                del self.blocks[pos]
            pos = -1
            for i in range(len(self.blocks)):
                if self.blocks[i].type == 'comment':
                    pos = i
                    break
            if pos >= 0:
                self.blocks.append(self.blocks[pos])
                del self.blocks[pos]
            if sh.Text(self.pattern).has_cyrillic():
                for i in range(len(self.blocks)):
                    if self.blocks[i-1].type == 'term' \
                    and self.blocks[i].type == 'term' \
                    and self.blocks[i-1].lang != 2 \
                    and self.blocks[i].lang == 2:
                        self.blocks[i-1], self.blocks[i] = self.blocks[i], self.blocks[i-1]
    
    def _get_pair(self, text):
        f = '[MClient] plugins.multitrandem.elems.Elems._get_pair'
        code = sh.Input(f, text).get_integer()
        return self.abbr.get_pair(code)
    
    def _check_dic_codes(self, text):
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
        if not self.abbr:
            sh.com.rep_empty(f)
            return
        if not self.abbr.Success:
            sh.com.cancel(f)
            return
        for block in self.blocks:
            if block.type != 'dic' or not block.text:
                continue
            if not self._check_dic_codes(block.text):
                mes = _('Wrong input data: "{}"!')
                mes = mes.format(block.text)
                sh.objs.get_mes(f, mes, True).show_warning()
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
                    sh.com.rep_empty(f)
            abbr = '; '.join(abbr)
            full = '; '.join(full)
            block.text = abbr
            block.dic = abbr
            block.dicf = full
    
    def strip(self):
        for block in self.blocks:
            block.text = block.text.strip()
    
    def run(self):
        f = '[MClient] plugins.multitrandem.elems.Elems.run'
        if not self.Success:
            sh.com.cancel(f)
            return self.blocks
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
        return self.blocks
    
    def debug(self):
        f = 'plugins.multitrandem.elems.Elems.debug'
        if not self.Debug:
            sh.com.rep_lazy(f)
            return
        mes = _('Debug table:')
        sh.objs.get_mes(f, mes, True).show_debug()
        headers = ('NO', 'TYPE', 'TEXT', 'SAME', 'CELLNO', 'ROWNO', 'COLNO'
                  ,'POS1', 'POS2'
                  )
        rows = []
        for i in range(len(self.blocks)):
            rows.append ([i + 1
                         ,self.blocks[i].type
                         ,self.blocks[i].text
                         ,self.blocks[i].same
                         ,self.blocks[i].cellno
                         ,self.blocks[i].i
                         ,self.blocks[i].j
                         ,self.blocks[i].first
                         ,self.blocks[i].last
                         ]
                        )
        mes = sh.FastTable (headers = headers
                           ,iterable = rows
                           ,maxrow = self.maxrow
                           ,maxrows = self.maxrows
                           ,Transpose = True
                           ).run()
        sh.com.run_fast_debug(f, mes)
        
    def set_transc(self):
        pass
        #block.type = 'transc'
    
    def add_brackets(self):
        for block in self.blocks:
            if block.type in ('comment', 'user', 'correction'):
                block.same = 1
                if not block.text.startswith('(') \
                and not block.text.endswith(')'):
                    block.text = '(' + block.text + ')'
    
    def add_space(self):
        for i in range(len(self.blocks)):
            if self.blocks[i].same <= 0:
                continue
            cond = False
            if i > 0 and self.blocks[i-1].text:
                if self.blocks[i-1].text[-1] in ['(', '[', '{']:
                    cond = True
            if self.blocks[i].text and not self.blocks[i].text[0].isspace() \
            and not self.blocks[i].text[0] in sh.lg.punc_array \
            and not self.blocks[i].text[0] in [')', ']', '}'] and not cond:
                self.blocks[i].text = ' ' + self.blocks[i].text
                
    def fill(self):
        dic = dicf = wform = speech = transc = term = ''
        
        # Find first non-empty values and set them as default
        for block in self.blocks:
            if block.type == 'dic':
                dic = block.dic
                dicf = block.dicf
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
            if block.type == 'dic':
                dic = block.dic
                dicf = block.dicf
            elif block.type == 'wform':
                wform = block.text
            elif block.type == 'speech':
                speech = block.text
            elif block.type == 'transc':
                transc = block.text
                ''' #TODO: Is there a difference if we use both
                    term/phrase here or the term only?
                '''
            elif block.type in ('term', 'phrase'):
                term = block.text
            block.dic = dic
            block.dicf = dicf
            block.wform = wform
            block.speech = speech
            block.transc = transc
            if block.same > 0:
                block.term = term
                
    def insert_fixed(self):
        dic = wform = speech = ''
        i = 0
        while i < len(self.blocks):
            if dic != self.blocks[i].dic or wform != self.blocks[i].wform \
            or speech != self.blocks[i].speech:
                
                block = Block()
                block.type = 'speech'
                block.text = self.blocks[i].speech
                block.dic = self.blocks[i].dic
                block.dicf = self.blocks[i].dicf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                block.term = self.blocks[i].term
                block.same = 0
                self.blocks.insert(i, block)
                
                block = Block()
                block.type = 'transc'
                block.text = self.blocks[i].transc
                block.dic = self.blocks[i].dic
                block.dicf = self.blocks[i].dicf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                block.term = self.blocks[i].term
                block.same = 0
                self.blocks.insert(i, block)

                block = Block()
                block.type = 'wform'
                block.text = self.blocks[i].wform
                block.dic = self.blocks[i].dic
                block.dicf = self.blocks[i].dicf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                block.term = self.blocks[i].term
                block.same = 0
                self.blocks.insert(i, block)
                
                block = Block()
                block.type = 'dic'
                block.text = self.blocks[i].dic
                block.dic = self.blocks[i].dic
                block.dicf = self.blocks[i].dicf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                block.term = self.blocks[i].term
                block.same = 0
                self.blocks.insert(i, block)
                
                dic = self.blocks[i].dic
                wform = self.blocks[i].wform
                speech = self.blocks[i].speech
                i += 4
            i += 1
            
    def remove_fixed(self):
        self.blocks = [block for block in self.blocks if block.type \
                       not in ('dic', 'wform', 'transc', 'speech')
                      ]
                       
    def set_selectables(self):
        # block.no is set only after creating DB
        for block in self.blocks:
            if block.type in ('phrase', 'term', 'transc') \
            and block.text and block.select < 1:
                block.select = 1
            else:
                block.select = 0


if __name__ == '__main__':
    f = '[MClient] plugins.multitrandem.elems.__main__'
    search = 'phrenosin'
    import get as gt
    import tags as tg
    iget = gt.Get(search)
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
                   ,abbr = None
                   ,search = search
                   ,Debug = True
                   ).run()
    for i in range(len(blocks)):
        mes = f'{i}: {blocks[i].type}: "{blocks[i].text}"'
        print(mes)
