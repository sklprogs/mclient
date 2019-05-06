#!/usr/bin/python3
# -*- coding: UTF-8 -*-

''' This module prepares blocks after extracting tags for permanently
    storing in DB.
    #note: 'multitran.com' does not support corrections yet
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



class Same:
    ''' Finely adjust SAME fields here. Default SAME values are already
        set (as early as in 'Tags'), so rewrite them carefully.
    '''
    def __init__ (self,blocks,Debug=False
                 ,Shorten=True,MaxRow=70
                 ,MaxRows=200
                 ):
        self._blocks = blocks
        self.Debug   = Debug
        self.Shorten = Shorten
        self.MaxRow  = MaxRow
        self.MaxRows = MaxRows
    
    def comment_next(self):
        ''' If a comment has SAME=0, then the next non-fixed type block
            must have SAME=1 because the comment cannot occupy
            an entire cell (otherwise, this is actually, for example,
            a word form). I do not use 'correction' and 'user' types
            here since they come only after other blocks and always have
            SAME=1.
        '''
        if len(self._blocks) > 1:
            i = 1
            while i < len(self._blocks):
                if self._blocks[i-1]._type == 'comment' \
                and self._blocks[i-1]._same == 0:
                    if self._blocks[i]._type == 'term':
                        self._blocks[i]._same = 1
                    else:
                        self._blocks[i-1]._same = 1
                i += 1
    
    def term_comment_fixed(self):
        ''' Set SAME value of a comment prior to a fixed type to 1
            even if it does not comprise brackets.
        '''
        if len(self._blocks) > 2:
            i = 2
            while i < len(self._blocks):
                if self._blocks[i-2]._type == 'term' \
                and self._blocks[i-1]._type == 'comment' \
                and self._blocks[i]._type in ('dic','wform','speech'
                                             ,'transc'
                                             ):
                    self._blocks[i-1]._same = 1
                i += 1
    
    def all_comments(self):
        for block in self._blocks:
            if (block._type == 'comment' \
                and block._text.startswith('(')
               ) or block._type in ('user','correction'):
                block._same = 1
    
    def term_comment_term(self):
        if len(self._blocks) > 2:
            i = 2
            while i < len(self._blocks):
                if self._blocks[i-2]._type == 'term' \
                and self._blocks[i-1]._type == 'comment' \
                and self._blocks[i]._type == 'term':
                    ''' There can be a 'comment-term; comment-term' case
                        (with the comments having SAME=1) which
                        shouldn't be matched. See multitran.com:
                        eng-rus: 'tree limb'.
                    '''
                    if not self._blocks[i-1]._text.startswith('('):
                        cond1 = sh.Text(self._blocks[i-2]._text).has_cyrillic()\
                                and sh.Text(self._blocks[i-1]._text).has_cyrillic()\
                                and sh.Text(self._blocks[i]._text).has_cyrillic()
                        cond2 = sh.Text(self._blocks[i-2]._text).has_latin()\
                                and sh.Text(self._blocks[i-1]._text).has_latin()\
                                and sh.Text(self._blocks[i]._text).has_latin()
                        if cond1 or cond2:
                            self._blocks[i-1]._same = 1
                            self._blocks[i  ]._same = 1
                i += 1
    
    def speech(self):
        ''' 'speech' blocks have '_same = 1' when analyzing MT because
            they are within a single tag. We fix it here, not in Tags,
            because Tags are assumed to output the result 'as is'.
        '''
        for i in range(len(self._blocks)):
            if self._blocks[i]._type == 'speech':
                self._blocks[i]._same = 0
                if i < len(self._blocks) - 1:
                    self._blocks[i+1]._same = 0
    
    def punc(self):
        for block in self._blocks:
            for sym in sh.punc_array:
                if block._text.startswith(sym):
                    block._same = 1
                    break
    
    def debug(self):
        f = 'plugins.multitrancom.elems.Same.debug'
        if self.Debug:
            sh.log.append (f,_('INFO')
                          ,_('Debug table:')
                          )
            headers = ['TYPE','TEXT','SAMECELL']
            rows = []
            for block in self._blocks:
                rows.append([block._type,block._text,block._same])
            sh.Table (headers = headers
                     ,rows    = rows
                     ,Shorten = self.Shorten
                     ,MaxRow  = self.MaxRow
                     ,MaxRows = self.MaxRows
                     ).print()
    
    def run(self):
        f = 'plugins.multitrancom.elems.Same.run'
        if self._blocks:
            self.speech()
            self.all_comments()
            self.term_comment_term()
            self.term_comment_fixed()
            self.comment_next()
            self.punc()
            self.debug()
            return self._blocks
        else:
            sh.com.empty(f)
            return []



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
    
    def terma_same(self):
        ''' #note: all blocks of the same cell must have the same TERMA,
            otherwise, alphabetizing may put blocks with SAME=1 outside
            of their cells.
        '''
        terma = ''
        for block in self._blocks:
            if block._same == 0:
                terma = block._terma
            elif block._same == 1:
                block._terma = terma
    
    def subjects(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.subjects'
        pattern = '(в|in) \d+ (тематиках|тематике|subjects)'
        count = 0
        i = 0
        while i < len(self._blocks):
            if re.match(pattern,self._blocks[i]._text):
                del self._blocks[i]
                count += 1
                i -= 1
            i += 1
        sh.log.append (f,_('INFO')
                      ,_('%d blocks have been deleted') % count
                      )
    
    def corrections(self):
        ''' Replace 'comment' with 'correction' in
            the 'correction-user-comment-user' structure.
        '''
        if len(self._blocks) > 3:
            i = 3
            while i < len(self._blocks):
                if self._blocks[i-3]._type == 'correction' \
                and self._blocks[i-2]._type == 'user' \
                and self._blocks[i-1]._type == 'comment' \
                and self._blocks[i]._type == 'user':
                    self._blocks[i-1]._type = 'correction'
                i += 1
    
    def users(self):
        for block in self._blocks:
            if block._type == 'comment' and 'UserName' in block._url:
                block._type = 'user'
    
    def strip(self):
        for block in self._blocks:
            block._text = block._text.strip()
    
    def delete_search(self):
        ''' Remove a block that looks like "SEARCH:" and comes before
            the phrase "NUMBER phrases in NUMBER subjects".
            Interestingly enough, the server preserves the case of
            mY sEaRch, so there is no need to make the search
            lower-case.
        '''
        f = '[MClient] plugins.multitrancom.elems.Elems.delete_search'
        if self._search:
            count = 0
            i = 0
            while i < len(self._blocks):
                if self._blocks[i]._type == 'comment' \
                and self._blocks[i]._text == self._search + ':':
                    del self._blocks[i]
                    count += 1
                    i -= 1
                i += 1
            if count:
                sh.log.append (f,_('INFO')
                              ,_('%d blocks have been deleted') % count
                              )
        else:
            sh.com.empty(f)
    
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
    
    def run(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.run'
        if self.Success:
            # Do some cleanup
            self.strip()
            self.trash()
            self.subjects()
            self.delete_search()
            # Reassign types
            self.transc()
            self.users()
            self.phrases()
            #todo: uncomment when 'multitran.com' supports corrections
            #self.corrections()
            self.thesaurus()
            # Prepare contents
            self.dic_urls()
            self.add_brackets()
            self.user_brackets()
            # Set SAME
            ''' We do not pass debug options here since Same debug has
                few columns and it is reasonable to make them wider than
                for Elems.
            '''
            self._blocks = Same (blocks = self._blocks
                                ,Debug  = self.Debug
                                ).run()
            # Prepare for cells
            self.fill()
            self.fill_terma()
            self.remove_fixed()
            self.insert_fixed()
            self.fixed_terma()
            self.expand_dica()
            self.terma_same()
            # Extra spaces in the beginning may cause sorting problems
            self.add_space()
            #todo: expand parts of speech (n -> noun, etc.)
            self.selectables()
            self.restore_dic_urls()
            self.dump()
            self.debug()
            return self._data
        else:
            sh.com.cancel(f)
    
    def debug(self):
        f = 'plugins.multitrancom.elems.Elems.debug'
        if self.Debug:
            sh.log.append (f,_('INFO')
                          ,_('Debug table:')
                          )
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
            
    def trash(self):
        self._blocks = [block for block in self._blocks \
                        if not block._text in ('|',';',':','(',')'
                                              ,'English','Russian'
                                              ,'Английский','Русский'
                                              ,'-->','точно','все формы'
                                              )
                       ]
    
    def add_space(self):
        for i in range(len(self._blocks)):
            if self._blocks[i]._same > 0:
                cond = False
                if i > 0 and self._blocks[i-1]._text:
                    if self._blocks[i-1]._text[-1] in ['(','[','{']:
                        cond = True
                if self._blocks[i]._text \
                  and not self._blocks[i]._text[0].isspace() \
                  and not self._blocks[i]._text[0] in sh.punc_array \
                  and not self._blocks[i]._text[0] in [')',']','}'] \
                  and not cond:
                    self._blocks[i]._text = ' ' + self._blocks[i]._text

    def phrases(self):
        ''' #note: this must differ from
            'plugins.multitranru.elems.Elems.phrases' since the block to
            be found is of the 'term' (not 'phrase') type here.
        '''
        for block in self._blocks:
            if re.match('\d+ phrases',block._text) \
            or re.match('\d+ фраз',block._text):
                block._type   = 'dic'
                block._select = 1
                block._dica   = block._text
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
            block._dica    = dica
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
