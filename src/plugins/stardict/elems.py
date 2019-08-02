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

import skl_shared.shared as sh

import gettext
import skl_shared.gettext_windows
skl_shared.gettext_windows.setup_env()
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
        self._type     = 'comment'
        self._text     = ''
        self._url      = ''
        self._dica     = ''
        self._dicaf    = ''
        self._wforma   = ''
        self._speecha  = ''
        self._transca  = ''
        self._terma    = ''



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
    def __init__(self,blocks,iabbr):
        f = '[MClient] plugins.stardict.elems.Elems.__init__'
        self._dic_urls = {}
        self._blocks   = blocks
        self.abbr      = iabbr
        if self._blocks:
            self.Success = True
        else:
            self.Success = False
            sh.com.empty(f)
        
    # Takes ~0,26s for 'set' on AMD E-300.
    def expand_dica(self):
        f = '[MClient] plugins.stardict.elems.Elems.expand_dica'
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
        f = '[MClient] plugins.stardict.elems.Elems.run'
        if self.Success:
            self.phrases()
            self.straight_line()
            self.comments()
            ''' These 2 procedures should not be combined (otherwise,
                corrections will have the same color as comments)
            '''
            self.unite_comments()
            self.comment_same()
            self.add_space()
            self.fill()
            self.fill_terma()
            self.remove_fixed()
            self.insert_fixed()
            self.fixed_terma()
            self.expand_dica()
            self.selectables()
            return self._blocks
        else:
            sh.com.cancel(f)
    
    def debug(self,Shorten=1,MaxRow=20,MaxRows=20):
        print('\nElems.debug (Non-DB blocks):')
        headers = ['DICA','WFORMA','SPEECHA','TRANSCA','TYPE','TEXT'
                  ,'SAMECELL','SELECTABLE'
                  ]
        rows = []
        for block in self._blocks:
            rows.append ([block._dica,block._wforma,block._speecha
                         ,block._transca,block._type,block._text
                         ,block._same,block._select
                         ]
                        )
        sh.Table (headers = headers
                 ,rows    = rows
                 ,Shorten = Shorten
                 ,MaxRow  = MaxRow
                 ,MaxRows = MaxRows
                 ).print()
        
    def unite_comments(self):
        i = 0
        while i < len(self._blocks):
            if self._blocks[i]._type == 'comment' \
            and self._blocks[i]._same > 0:
                if i > 0 and self._blocks[i-1]._type == 'comment':
                    self._blocks[i-1]._text \
                    = sh.List (lst1 = [self._blocks[i-1]._text
                                      ,self._blocks[i]._text
                                      ]
                              ).space_items()
                    del self._blocks[i]
                    i -= 1
            i += 1
            
    def straight_line(self):
        self._blocks = [block for block in self._blocks \
                        if block._text.strip() != '|'
                       ]
    
    def comments(self):
        i = 0
        while i < len(self._blocks):
            if self._blocks[i]._type in ('comment','correction'):
                text_str = self._blocks[i]._text.strip()
                ''' Delete comments that are just ';' or ',' (we don't
                    need them, we have a table view).
                    We delete instead of assigning Block attribute
                    because we may need to unblock blocked dictionaries
                    later.
                '''
                if text_str == ';' or text_str == ',':
                    del self._blocks[i]
                    i -= 1
                elif not self._blocks[i]._same > 0:
                    # For the following cases: "23 фраз в 9 тематиках"
                    if i > 0 and self._blocks[i-1]._type == 'phrase':
                        self._blocks[i]._same = 1
                    # Move the comment to the preceding cell
                    if text_str.startswith(',') \
                    or text_str.startswith(';') \
                    or text_str.startswith('(') \
                    or text_str.startswith(')') \
                    or text_str.startswith('|'):
                        self._blocks[i]._same = 1
                        # Mark the next block as a start of a new cell
                        if i < len(self._blocks) - 1 \
                        and self._blocks[i+1]._type \
                        not in ('comment','correction'):
                            self._blocks[i+1]._same = 0
            i += 1
            
    def comment_same(self):
        ''' Sometimes sources do not provide sufficient information on
        SAMECELL blocks, and the tag parser cannot handle sequences such
        as 'any type (not _same) -> comment (not _same) -> any type (not
        _same)'.
        Rules:
        1) (Should be always correct)
            'i >= 0 -> correction (not _same)
                =>
            'i >= 0 -> correction (_same)
        2) (Preferable)
            'term (not _same) -> comment (not _same) -> any type
            (not _same)'
                =>
            'term (not _same) -> comment (_same) -> any type
            (not _same)'
        3) (Generally correct before removing fixed columns)
            'dic/wform/speech/transc -> comment (not _same) -> term
            (not _same)'
                =>
            'dic/wform/speech/transc -> comment (not _same) -> term
            (_same)'
        4) (By guess, check only after ##2&3)
            'any type (_same) -> comment (not _same) -> any type
            (not _same)'
                =>
            'any type (_same) -> comment (_same) -> any type
            (not _same)'
        5) (Always correct)
            'any type -> comment/correction (not _same) -> END'
                =>
            'any type -> comment/correction (_same) -> END'
        6) (Do this in the end of the loop; + Readability improvement
           ("в 42 тематиках"))
            'any type (not same) -> comment (not same) -> any type
            (not _same)'
                =>
            'any type (not same) -> comment (_same) -> any type
            (not _same)'
        '''
        for i in range(len(self._blocks)):
            cond1  = i > 0 and self._blocks[i]._type == 'correction'
            cond2  = self._blocks[i]._same <= 0
            cond3  = i > 0 and self._blocks[i-1]._type == 'comment' \
            and self._blocks[i-1]._same <= 0
            cond4  = i > 1 and self._blocks[i-2]._type == 'term' \
            and self._blocks[i-2]._same <= 0
            cond5  = i > 1 and self._blocks[i-2]._same <= 0
            cond6  = self._blocks[i]._type == 'term'
            cond7a = i > 1 and self._blocks[i-2]._type == 'dic'
            cond7b = i > 1 and self._blocks[i-2]._type == 'wform'
            cond7c = i > 1 and self._blocks[i-2]._type == 'speech'
            cond7d = i > 1 and self._blocks[i-2]._type == 'transc'
            cond7  = cond7a or cond7b or cond7c or cond7d
            # not equivalent to 'not cond5' because of 'i'
            cond8  = i > 1 and self._blocks[i-2]._same == 1
            # Rule 1
            if cond1 and cond2:
                self._blocks[i]._same = 1
            # Rule 2
            elif cond4 and cond3 and cond2:
                self._blocks[i-1]._same = 1
            # Rule 3
            elif cond7 and cond3 and cond6 and cond2:
                self._blocks[i]._same = 1
            # Rule 4:
            elif cond8 and cond3 and cond2:
                self._blocks[i-1]._same = 1
            # Rule 6:
            elif cond5 and cond3 and cond2:
                self._blocks[i-1]._same = 1
        # Rule 5
        if self._blocks:
            # After exiting the loop, the last block
            cond1 = self._blocks[i]._type in ('comment','correction')
            cond2 = self._blocks[i]._same <= 0
            if cond1 and cond2:
                self._blocks[i]._same = 1
    
    def add_space(self):
        for i in range(len(self._blocks)):
            if self._blocks[i]._same > 0:
                cond = False
                if i > 0:
                    if self._blocks[i-1]._text[-1] in ['(','[','{']:
                        cond = True
                if self._blocks[i]._text \
                  and not self._blocks[i]._text[0].isspace() \
                  and not self._blocks[i]._text[0] in sh.lg.punc_array \
                  and not self._blocks[i]._text[0] in [')',']','}'] \
                  and not cond:
                    self._blocks[i]._text = ' ' + self._blocks[i]._text

    def phrases(self):
        for block in self._blocks:
            if block._type == 'phrase':
                block._type   = 'dic'
                block._select = 1
                block._dica   = block._text.strip()
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
                       
    def selectables(self):
        # block._no is set only after creating DB
        for block in self._blocks:
            if block._type in ('phrase','term','transc') \
            and block._text and block._select < 1:
                block._select = 1
            else:
                block._select = 0
