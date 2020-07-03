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
        self.sprior   = -1
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
    def __init__(self,blocks,abbr):
        f = '[MClient] plugins.stardict.elems.Elems.__init__'
        self.dicurls = {}
        self.blocks  = blocks
        self.abbr    = abbr
        if self.blocks:
            self.Success = True
        else:
            self.Success = False
            sh.com.rep_empty(f)

    def expand_dica(self):
        #TODO (?): implement
        pass
    
    def run(self):
        f = '[MClient] plugins.stardict.elems.Elems.run'
        if self.Success:
            self.set_phrases()
            self.delete_straight_line()
            self.run_comments()
            ''' These 2 procedures should not be combined (otherwise,
                corrections will have the same color as comments)
            '''
            self.unite_comments()
            self.set_com_same()
            self.add_space()
            self.fill()
            self.fill_terma()
            self.remove_fixed()
            self.insert_fixed()
            self.set_fixed_terma()
            self.expand_dica()
            self.set_selectables()
            return self.blocks
        else:
            sh.com.cancel(f)
    
    def debug(self,maxrow=20,maxrows=1000):
        f = '[MClient] plugins.stardict.elems.Elems.debug'
        headers = ('NO','DICA','WFORMA','SPEECHA','TRANSCA','TYPE'
                  ,'TEXT','SAME','SELECT'
                  )
        rows = []
        for i in range(len(self.blocks)):
            rows.append ([i + 1
                         ,self.blocks[i].dica
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
        
    def unite_comments(self):
        i = 0
        while i < len(self.blocks):
            if self.blocks[i].type_ == 'comment' \
            and self.blocks[i].same > 0:
                if i > 0 and self.blocks[i-1].type_ == 'comment':
                    self.blocks[i-1].text \
                    = sh.List (lst1 = [self.blocks[i-1].text
                                      ,self.blocks[i].text
                                      ]
                              ).space_items()
                    del self.blocks[i]
                    i -= 1
            i += 1
            
    def delete_straight_line(self):
        self.blocks = [block for block in self.blocks \
                       if block.text.strip() != '|'
                      ]
    
    def run_comments(self):
        i = 0
        while i < len(self.blocks):
            if self.blocks[i].type_ in ('comment','correction'):
                text_str = self.blocks[i].text.strip()
                ''' Delete comments that are just ';' or ',' (we don't
                    need them, we have a table view).
                    We delete instead of assigning Block attribute
                    because we may need to unblock blocked dictionaries
                    later.
                '''
                if text_str == ';' or text_str == ',':
                    del self.blocks[i]
                    i -= 1
                elif not self.blocks[i].same > 0:
                    # For the following cases: "23 фраз в 9 тематиках"
                    if i > 0 and self.blocks[i-1].type_ == 'phrase':
                        self.blocks[i].same = 1
                    # Move the comment to the preceding cell
                    if text_str.startswith(',') \
                    or text_str.startswith(';') \
                    or text_str.startswith('(') \
                    or text_str.startswith(')') \
                    or text_str.startswith('|'):
                        self.blocks[i].same = 1
                        # Mark the next block as a start of a new cell
                        if i < len(self.blocks) - 1 \
                        and self.blocks[i+1].type_ \
                        not in ('comment','correction'):
                            self.blocks[i+1].same = 0
            i += 1
            
    def set_com_same(self):
        ''' Sometimes sources do not provide sufficient information on
        SAMECELL blocks, and the tag parser cannot handle sequences such
        as 'any type (not same) -> comment (not same) -> any type (not
        same)'.
        Rules:
        1) (Should be always correct)
            'i >= 0 -> correction (not same)
                =>
            'i >= 0 -> correction (same)
        2) (Preferable)
            'term (not same) -> comment (not same) -> any type
            (not same)'
                =>
            'term (not same) -> comment (same) -> any type
            (not same)'
        3) (Generally correct before removing fixed columns)
            'dic/wform/speech/transc -> comment (not same) -> term
            (not same)'
                =>
            'dic/wform/speech/transc -> comment (not same) -> term
            (same)'
        4) (By guess, check only after ##2&3)
            'any type (same) -> comment (not same) -> any type
            (not same)'
                =>
            'any type (same) -> comment (same) -> any type
            (not same)'
        5) (Always correct)
            'any type -> comment/correction (not same) -> END'
                =>
            'any type -> comment/correction (same) -> END'
        6) (Do this in the end of the loop; + Readability improvement
           ("в 42 тематиках"))
            'any type (not same) -> comment (not same) -> any type
            (not same)'
                =>
            'any type (not same) -> comment (same) -> any type
            (not same)'
        '''
        for i in range(len(self.blocks)):
            cond1  = i > 0 and self.blocks[i].type_ == 'correction'
            cond2  = self.blocks[i].same <= 0
            cond3  = i > 0 and self.blocks[i-1].type_ == 'comment' \
            and self.blocks[i-1].same <= 0
            cond4  = i > 1 and self.blocks[i-2].type_ == 'term' \
            and self.blocks[i-2].same <= 0
            cond5  = i > 1 and self.blocks[i-2].same <= 0
            cond6  = self.blocks[i].type_ == 'term'
            cond7a = i > 1 and self.blocks[i-2].type_ == 'dic'
            cond7b = i > 1 and self.blocks[i-2].type_ == 'wform'
            cond7c = i > 1 and self.blocks[i-2].type_ == 'speech'
            cond7d = i > 1 and self.blocks[i-2].type_ == 'transc'
            cond7  = cond7a or cond7b or cond7c or cond7d
            # not equivalent to 'not cond5' because of 'i'
            cond8  = i > 1 and self.blocks[i-2].same == 1
            # Rule 1
            if cond1 and cond2:
                self.blocks[i].same = 1
            # Rule 2
            elif cond4 and cond3 and cond2:
                self.blocks[i-1].same = 1
            # Rule 3
            elif cond7 and cond3 and cond6 and cond2:
                self.blocks[i].same = 1
            # Rule 4:
            elif cond8 and cond3 and cond2:
                self.blocks[i-1].same = 1
            # Rule 6:
            elif cond5 and cond3 and cond2:
                self.blocks[i-1].same = 1
        # Rule 5
        if self.blocks:
            # After exiting the loop, the last block
            cond1 = self.blocks[i].type_ in ('comment','correction')
            cond2 = self.blocks[i].same <= 0
            if cond1 and cond2:
                self.blocks[i].same = 1
    
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

    def set_phrases(self):
        for block in self.blocks:
            if block.type_ == 'phrase':
                block.type_  = 'dic'
                block.select = 1
                block.dica   = block.text.strip()
                break
                
    def fill(self):
        dica = wforma = speecha = transca = terma = ''
        
        # Find first non-empty values and set them as default
        for block in self.blocks:
            if block.type_ == 'dic':
                dica = block.text
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
                dica = block.text
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
            block.dica    = dica.strip()
            block.wforma  = wforma
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
        dica = wforma = speecha = ''
        i = 0
        while i < len(self.blocks):
            if dica != self.blocks[i].dica \
            or wforma != self.blocks[i].wforma \
            or speecha != self.blocks[i].speecha:
                
                block          = Block()
                block.type_    = 'speech'
                block.text    = self.blocks[i].speecha
                block.dica    = self.blocks[i].dica
                block.wforma  = self.blocks[i].wforma
                block.speecha = self.blocks[i].speecha
                block.transca = self.blocks[i].transca
                block.terma   = self.blocks[i].terma
                block.same    = 0
                self.blocks.insert(i,block)
                
                block          = Block()
                block.type_    = 'transc'
                block.text    = self.blocks[i].transca
                block.dica    = self.blocks[i].dica
                block.wforma  = self.blocks[i].wforma
                block.speecha = self.blocks[i].speecha
                block.transca = self.blocks[i].transca
                block.terma   = self.blocks[i].terma
                block.same    = 0
                self.blocks.insert(i,block)

                block          = Block()
                block.type_    = 'wform'
                block.text    = self.blocks[i].wforma
                block.dica    = self.blocks[i].dica
                block.wforma  = self.blocks[i].wforma
                block.speecha = self.blocks[i].speecha
                block.transca = self.blocks[i].transca
                block.terma   = self.blocks[i].terma
                block.same    = 0
                self.blocks.insert(i,block)
                
                block          = Block()
                block.type_    = 'dic'
                block.text    = self.blocks[i].dica
                block.dica    = self.blocks[i].dica
                block.wforma  = self.blocks[i].wforma
                block.speecha = self.blocks[i].speecha
                block.transca = self.blocks[i].transca
                block.terma   = self.blocks[i].terma
                block.same    = 0
                self.blocks.insert(i,block)
                
                dica    = self.blocks[i].dica
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
