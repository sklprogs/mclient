#!/usr/bin/python3
# -*- coding: UTF-8 -*-

''' This module prepares blocks after extracting tags for permanently
    storing in DB.
    Needs attributes in blocks: TYPE, DICA, WFORMA, SPEECHA, TRANSCA,
    TERMA, SAMECELL
    Modifies attributes:        TYPE, TEXT, DICA, WFORMA, SPEECHA,
    TRANSCA, TERMA, SAMECELL
    Since TYPE is modified here, SAMECELL is filled here.
    SELECTABLE cannot be filled because it depends on CELLNO which is
    created in Cells; Cells modifies TEXT of DIC, WFORM, SPEECH, TRANSC
    types, and we do not need to make empty cells SELECTABLE, so we
    calculate SELECTABLE fully in Cells.
'''

import re
import shared    as sh
import sharedGUI as sg

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')



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
            'correction', 'transc', 'invalid'
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
    ''' Process blocks before dumping to DB.
        About filling 'terma':
        - We fill 'terma' from the start in order to ensure the correct
          'terma' value for blocks having '_same == 1'
        - We fill 'terma' from the end in order to ensure that 'terma'
          of blocks of non-selectable types will have the value of
          the 'term' AFTER those blocks
        - We fill 'terma' from the end in order to ensure that 'terma'
          is also filled for blocks having '_same == 0'
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
    def __init__ (self,blocks,articleid,iabbr
                 ,Debug=False,Shorten=True
                 ,MaxRow=20,MaxRows=20,search=''
                 ):
        f = '[MClient] plugins.multitrancom.elems.Elems.__init__'
        self._data      = []
        self._dic_urls  = {}
        self._blocks    = blocks
        self._articleid = articleid
        self.abbr       = iabbr
        self.Debug      = Debug
        self.Shorten    = Shorten
        self.MaxRow     = MaxRow
        self.MaxRows    = MaxRows
        self._search    = search.strip()
        if self._blocks and self._articleid:
            self.Success = True
        else:
            self.Success = False
            sh.com.empty(f)
    
    def same_punc(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.same_punc'
        if self.Success:
            for i in range(len(self._blocks)):
                text = self._blocks[i]._text.strip()
                for sym in sh.punc_array:
                    if text.startswith(sym):
                        self._blocks[i]._same = 1
                        break
        else:
            sh.com.cancel(f)
    
    def three(self,i):
        # Check for the 'term-comment-term' construct
        if 0 < i < len(self._blocks) - 1:
            if self._blocks[i-1]._type == 'term' \
            and self._blocks[i+1]._type == 'term':
                cond1 = sh.Text(self._blocks[i-1]._text).has_cyrillic()\
                        and sh.Text(self._blocks[i]._text).has_cyrillic()\
                        and sh.Text(self._blocks[i+1]._text).has_cyrillic()
                cond2 = sh.Text(self._blocks[i-1]._text).has_latin()\
                        and sh.Text(self._blocks[i]._text).has_latin()\
                        and sh.Text(self._blocks[i+1]._text).has_latin()
                ''' There can be a 'comment-term; comment-term' case
                    (with the comments having SAME=1) which shouldn't
                    be matched. See multitran.com: eng-rus: 'tree limb'.
                '''
                Allow = True
                if i > 1:
                    if self._blocks[i-2]._type == 'comment' \
                    and not '(' in self._blocks[i-2]._text \
                    and not ')' in self._blocks[i-2]._text:
                        Allow = False
                if (cond1 or cond2) and Allow:
                    return True
    
    def same_comments(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.same_comments'
        if self.Success:
            for i in range(len(self._blocks)):
                if self._blocks[i]._type == 'comment':
                    if '(' in self._blocks[i]._text \
                    or ')' in self._blocks[i]._text:
                        if i > 0:
                            self._blocks[i]._same = 1
                        else:
                            self._blocks[i]._same = 0
                    else:
                        if self.three(i):
                            self._blocks[i-1]._same = 0
                            self._blocks[i  ]._same = 1
                            self._blocks[i+1]._same = 1
                        elif i < len(self._blocks):
                            self._blocks[i  ]._same = 0
                            self._blocks[i+1]._same = 1
                        else:
                            self._blocks[i]._same = 1
        else:
            sh.com.cancel(f)
    
    def same_non_comments(self):
        ''' If a comment has SAME=0, then the next non-fixed type block
            must have SAME=1 because the comment cannot occupy
            an entire cell (otherwise, this is actually, for example,
            a word form).
        '''
        f = '[MClient] plugins.multitrancom.elems.Elems.same_non_comments'
        if self.Success:
            for i in range(len(self._blocks)):
                if self._blocks[i]._type == 'comment' \
                and self._blocks[i]._same == 0:
                    if i < len(self._blocks) - 1:
                        if self._blocks[i+1]._type in ('dic','wform'
                                                      ,'speech','transc'
                                                      ):
                            self._blocks[i]._same = 1
                        elif self._blocks[i+1]._type == 'term' \
                        and self._blocks[i+1]._same == 0:
                            self._blocks[i+1]._same == 1
        else:
            sh.com.cancel(f)
    
    def delete_search(self):
        ''' Remove a block that looks like "SEARCH:" and comes before
            the phrase "NUMBER phrases in NUMBER subjects".
            Interestingly enough, the server preserves the case of
            mY sEaRch, so there is no need to make the search
            lower-case.
        '''
        f = '[MClient] plugins.multitrancom.elems.Elems.delete_search'
        if self.Success:
            if self._search:
                count = 0
                i = 0
                while i < len(self._blocks):
                    if self._blocks[i]._type == 'comment' \
                    and self._blocks[i]._text.strip() == self._search \
                    + ':':
                        del self._blocks[i]
                        count += 1
                        i -= 1
                    i += 1
                if count:
                    sh.log.append (f,_('INFO')
                                  ,_('%d blocks have been deleted') \
                                  % count
                                  )
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def thesaurus(self):
        ''' Explanations are tagged just like word forms, and we can
            judge upon the type only by the length of the block.
        '''
        for block in self._blocks:
            if block._type == 'wform' and len(block._text) > 25:
                block._type = 'comment'
    
    # Takes ~0,26s for 'set' on AMD E-300.
    def expand_dica(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.expand_dica'
        if self.abbr:
            if self.abbr.Success:
                for block in self._blocks:
                    lst = block._dica.split(',')
                    for i in range(len(lst)):
                        lst[i] = lst[i].strip()
                        try:
                            ind = self.abbr.orig.index(lst[i])
                            lst[i] = self.abbr.transl[ind]
                        except ValueError:
                            pass
                    block._dicaf = ', '.join(lst)
            else:
                sh.com.cancel(f)
        else:
            sh.com.empty(f)

    def same_cells(self):
        for i in range(len(self._blocks)):
            if self._blocks[i]._type == 'dic':
                if i > 0 and self._blocks[i-1]._type == 'dic':
                    self._blocks[i]._same = 1
                else:
                    self._blocks[i]._same = 0
            elif self._blocks[i]._type == 'transc':
                self._blocks[i]._same = 0
            elif self._blocks[i]._type in ('term','speech','phrase'):
                self._blocks[i]._same = 0
            elif self._blocks[i]._type == 'wform':
                if i > 0 and self._blocks[i-1]._type == 'wform':
                    self._blocks[i]._same = 1
                else:
                    self._blocks[i]._same = 0
    
    def run(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.run'
        if self.Success:
            self.transc()
            self.thesaurus()
            self.phrases()
            self.trash()
            self.delete_search()
            # Change types and delete garbage blocks before this
            self.same_cells()
            self.dic_urls()
            self.unite_comments()
            self.add_brackets()
            ''' Comments also can be separate in this source, so do this
                after uniting them.
            '''
            self.same_comments()
            self.same_punc()
            self.same_non_comments()
            self.add_space()
            self.fill()
            self.fill_terma()
            self.remove_fixed()
            self.insert_fixed()
            self.fixed_terma()
            self.expand_dica()
            #todo: expand parts of speech (n -> noun, etc.)
            self.selectables()
            self.restore_dic_urls()
            self.debug()
            self.dump()
            return self._data
        else:
            sh.com.cancel(f)
    
    def debug(self):
        if self.Debug:
            print('\nplugins.multitrancom.elems.Elems.debug (Non-DB blocks):')
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
        
    def has_transc(self,text):
        ''' There are no square brackets in phonetics anymore, so we
            need to guess.
        '''
        if 'ʌ' in text or 'ɔ' in text or 'ə' in text or 'æ' in text \
        or 'ɑ' in text or 'ɛ' in text or 'ʒ' in text or 'ʤ' in text \
        or 'ð' in text or 'ʃ' in text or 'ʧ'in text or 'θ' in text \
        or 'ŋ' in text or 'ɪ' in text:
            return True
    
    def transc(self):
        for block in self._blocks:
            if block._type == 'comment' \
            and self.has_transc(block._text):
                block._type = 'transc'
                            
    def unite_comments(self):
        i = 0
        while i < len(self._blocks):
            if i > 0:
                if self._blocks[i]._type == 'comment' \
                and self._blocks[i-1]._type == 'comment':
                    if i < len(self._blocks) - 1 \
                    and self._blocks[i+1]._text.strip().startswith(')'):
                        cond = True
                    else:
                        cond = False
                    if self._blocks[i]._text.strip().endswith('(') \
                    or cond:
                        self._blocks[i-1]._text \
                        = sh.List (lst1 = [self._blocks[i-1]._text
                                          ,self._blocks[i]._text
                                          ]
                                  ).space_items()
                    del self._blocks[i]
                    i -= 1
            i += 1
    
    def add_brackets(self):
        for block in self._blocks:
            if block._type == 'comment' and '(' in block._text \
            and not ')' in block._text:
                block._text += ')'
            
    def trash(self):
        self._blocks = [block for block in self._blocks \
                        if not block._text \
                        in ('|',';',':','English','Russian','Английский'
                           ,'Русский','-->','точно','все формы'
                           )
                       ]
    
    def add_space(self):
        for i in range(len(self._blocks)):
            if self._blocks[i]._same > 0:
                cond = False
                if i > 0:
                    if self._blocks[i-1]._text[-1] in ['(','[','{']:
                        cond = True
                if self._blocks[i]._text \
                  and not self._blocks[i]._text[0].isspace() \
                  and not self._blocks[i]._text[0] in sh.punc_array \
                  and not self._blocks[i]._text[0] in [')',']','}'] \
                  and not cond:
                    self._blocks[i]._text = ' ' + self._blocks[i]._text

    def phrases(self):
        for block in self._blocks:
            if re.match('\d+ phrases',block._text) \
            or re.match('\d+ фраз',block._text):
                block._type   = 'dic'
                block._select = 1
                block._dica   = block._text
                block._same   = 0
                break
                
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
            block._dica    = dica.strip()
            block._wforma  = wforma
            block._speecha = speecha
            block._transca = transca
            if block._same > 0:
                block._terma = terma
    
    def fill_terma(self):
        terma = ''
        ''' This is just to get a non-empty value of 'terma' if some
            other types besides 'phrase' and 'term' follow them in the
            end.
        '''
        i = len(self._blocks) - 1
        while i >= 0:
            if self._blocks[i]._type in ('term','phrase'):
                terma = self._blocks[i]._text
                break
            i -= 1
        i = len(self._blocks) - 1
        while i >= 0:
            if self._blocks[i]._type in ('term','phrase'):
                terma = self._blocks[i]._text
            if not self._blocks[i]._same > 0:
                self._blocks[i]._terma = terma
            i -= 1
            
    def fixed_terma(self):
        for block in self._blocks:
            if block._type in ('dic','wform','speech','transc'):
                block._terma = ''
                
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
                       
    def dump(self):
        for block in self._blocks:
            self._data.append (
              (None                # (00) Skips the autoincrement
              ,self._articleid     # (01) ARTICLEID
              ,block._dica         # (02) DICA (abbreviation)
              ,block._wforma       # (03) WFORMA
              ,block._speecha      # (04) SPEECHA
              ,block._transca      # (05) TRANSCA
              ,block._terma        # (06) TERMA
              ,block._type         # (07) TYPE
              ,block._text         # (08) TEXT
              ,block._url          # (09) URL
              ,block._block        # (10) BLOCK
              ,block._priority     # (11) PRIORITY
              ,block._select       # (12) SELECTABLE
              ,block._same         # (13) SAMECELL
              ,block._cell_no      # (14) CELLNO
              ,-1                  # (15) ROWNO
              ,-1                  # (16) COLNO
              ,-1                  # (17) POS1
              ,-1                  # (18) POS2
              ,''                  # (19) NODE1
              ,''                  # (20) NODE2
              ,-1                  # (21) OFFPOS1
              ,-1                  # (22) OFFPOS2
              ,-1                  # (23) BBOX1
              ,-1                  # (24) BBOX2
              ,-1                  # (25) BBOY1
              ,-1                  # (26) BBOY2
              ,block._text.lower() # (27) TEXTLOW
              ,0                   # (28) IGNORE
              ,0                   # (29) SPEECHPR
              ,block._dicaf        # (30) DICA (full title)
              )
                              )

    def selectables(self):
        # block._no is set only after creating DB
        for block in self._blocks:
            if block._type in ('phrase','term','transc') \
            and block._text and block._select < 1:
                block._select = 1
            else:
                block._select = 0
    
    def dic_urls(self):
        for block in self._blocks:
            if block._type == 'dic' \
            and not block._text in self._dic_urls:
                self._dic_urls[block._text] = block._url
    
    def restore_dic_urls(self):
        for i in range(len(self._blocks)):
            if self._blocks[i]._type == 'dic' \
            and self._blocks[i]._text in self._dic_urls:
                self._blocks[i]._url = self._dic_urls[self._blocks[i]._text]
