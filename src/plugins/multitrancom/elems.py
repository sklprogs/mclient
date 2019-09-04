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
import skl_shared.shared as sh

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
    
    def wform_comment_fixed(self):
        ''' Set a specific 'definition' type for blocks that are tagged
            by multitran.com as comments (or word forms, see
            'Elems.definitions') but are placed next to word forms.
            We create the new type since after removing fixed types
            there could be no other way to reinsert them without
            associating definitions with wrong cells (fixed types are
            reinserted when DICA, WFORMA or SPEECHA change, but there
            are cases when a definition block is duplicated
            by multitran.com and those fields remain unchanged, see,
            for example, 'memory pressure').
        '''
        if len(self._blocks) > 2:
            i = 2
            while i < len(self._blocks):
                ''' Do not check the '_same' value of a definition block
                    since it can (and should) already be set to 1.
                '''
                if self._blocks[i-2]._type == 'wform' \
                and self._blocks[i-1]._type == 'comment' \
                and self._blocks[i]._type in ('dic','wform','transc'
                                             ,'speech'
                                             ):
                   self._blocks[i-1]._type = 'definition'
                   ''' '_same' value of the definition block should
                       already be set to 1, but we assign it just to be
                       on a safe side.
                   '''
                   self._blocks[i-1]._same = 1
                i += 1
    
    def wform_comment_term(self):
        # Source-specific
        if len(self._blocks) > 2:
            i = 2
            while i < len(self._blocks):
                if self._blocks[i-2]._type == 'wform' \
                and self._blocks[i-2]._same == 0 \
                and self._blocks[i-2]._url \
                and self._blocks[i-1]._type == 'comment' \
                and self._blocks[i-1]._same == 0 \
                and self._blocks[i]._type == 'term' \
                and self._blocks[i]._same == 1:
                   self._blocks[i-2]._type = 'term'
                   self._blocks[i-1]._same = 1
                i += 1
    
    def comment_comment(self):
        ''' Fix the 'comment (SAME=0) - comment (SAME=0)' structure
            which may be encountered due to that word forms can be
            indistinguishable from comments. The latter happens only in
            the present source, so this code is plugin-specific.
        '''
        if len(self._blocks) > 2:
            i = 2
            while i < len(self._blocks):
                if self._blocks[i-1]._type == 'comment' \
                and self._blocks[i-1]._same == 0 \
                and self._blocks[i]._type == 'comment' \
                and self._blocks[i]._same == 0:
                    if self._blocks[i-2]._type in ('dic','wform'
                                                  ,'speech','transc'
                                                  ):
                        self._blocks[i-1]._type = 'wform'
                        self._blocks[i]._same = 1
                    else:
                        self._blocks[i-1]._same = 1
                i += 1
    
    def comment_term(self):
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
            for sym in sh.lg.punc_array:
                if block._text.startswith(sym):
                    block._same = 1
                    break
    
    def debug(self):
        f = 'plugins.multitrancom.elems.Same.debug'
        if self.Debug:
            mes = _('Debug table:')
            sh.objs.mes(f,mes,True).debug()
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
            self.comment_comment()
            self.wform_comment_term()
            self.comment_term()
            self.wform_comment_fixed()
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
    def __init__ (self,blocks,iabbr,langs
                 ,Debug=False,Shorten=True
                 ,MaxRow=20,MaxRows=20,search=''
                 ):
        f = '[MClient] plugins.multitrancom.elems.Elems.__init__'
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
    
    def search_definition(self,block):
        f = '[MClient] plugins.multitrancom.elems.Elems.search_definition'
        if block:
            for definition in self._defins:
                if block._dica == definition._dica \
                and block._wforma == definition._wforma \
                and block._speecha == definition._speecha:
                    mes = '"{}"'.format(definition._text)
                    sh.objs.mes(f,mes,True).debug()
                    self._defins.remove(definition)
                    return definition
        else:
            sh.com.empty(f)
    
    def insert_definitions(self):
        ''' Reisert definitions after word forms
            #NOTE: Do this after reinserting fixed types.
        '''
        f = '[MClient] plugins.multitrancom.elems.Elems.insert_definitions'
        if self._defins:
            i = 0
            while i < len(self._blocks):
                if self._blocks[i]._type == 'wform':
                    block = self.search_definition(self._blocks[i])
                    if block:
                        self._blocks.insert(i+1,block)
                        i += 1
                i += 1
        else:
            sh.com.lazy(f)
    
    def delete_definitions(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.delete_definitions'
        self._defins = [block for block in self._blocks
                        if block._type == 'definition'
                       ]
        self._blocks = [block for block in self._blocks
                        if block._type != 'definition'
                       ]
        if self._defins:
            mes = _('{} blocks have been deleted')
            mes = mes.format(len(self._defins))
            sh.objs.mes(f,mes,True).info()
        else:
            sh.com.lazy(f)
    
    def delete_empty(self):
        ''' - Empty blocks are useless since we recreate fixed columns
              anyways.
            - This is required since we decode HTML entities after
              extracting tags now. Empty blocks may lead to a wrong
              analysis of blocks, e.g.,
              'comment (SAME=0) - comment (SAME=1)' structure, where
              the second block is empty, will be mistakenly converted
              to 'wform - comment'.
        '''
        self._blocks = [block for block in self._blocks if block._text]
    
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
        mes = _('{} blocks have been deleted').format(count)
        sh.objs.mes(f,mes,True).info()
    
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
        ''' User names are initially comments at 'multitran.ru', and
            terms at 'multitran.com'.
        '''
        for block in self._blocks:
            if block._type == 'term' and 'UserName' in block._url:
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
                mes = _('{} blocks have been deleted').format(count)
                sh.objs.mes(f,mes,True).info()
        else:
            sh.com.empty(f)
    
    def definitions(self):
        ''' Definitions are tagged just like word forms, and we can
            judge upon the type only by the length of the block.
            The value of 30 is picked up on the basis of
            a trial-and-error method.
            Examples of long word forms (28+ symbols):
            'закрытая нуклеиновая кислота',
            'nucleoside reverse transcriptase inhibitors'.
        '''
        HasWform = False
        for block in self._blocks:
            # The 'definition' type cannot precede word forms
            if block._type == 'wform':
                if len(block._text) > 30 and HasWform:
                    block._type = 'definition'
                    block._same = 1
                HasWform = True
    
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
            self.delete_empty()
            self.trash()
            self.subjects()
            self.delete_search()
            # Reassign types
            self.transc()
            self.users()
            self.phrases()
            self.corrections()
            self.definitions()
            # Prepare contents
            self.dic_urls()
            self.add_brackets()
            self.user_brackets()
            # Set '_same' attribute and further change some types
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
            self.delete_definitions()
            self.remove_fixed()
            self.insert_fixed()
            self.insert_definitions()
            self.fixed_terma()
            self.expand_dica()
            self.terma_same()
            # Extra spaces in the beginning may cause sorting problems
            self.add_space()
            #todo: expand parts of speech (n -> noun, etc.)
            self.selectables()
            self.restore_dic_urls()
            self.debug()
            return self._blocks
        else:
            sh.com.cancel(f)
    
    def debug(self):
        f = 'plugins.multitrancom.elems.Elems.debug'
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
        for block in self._blocks:
            if block._type == 'comment' \
            and block._text.startswith('[') \
            and block._text.endswith(']'):
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
        f = '[MClient] plugins.multitrancom.elems.Elems.trash'
        patterns = ['|',';',':','(',')','-->','⇄','точно','все формы'
                   ,'// -->'
                   ]
        if self._langs:
            patterns += list(self._langs)
        else:
            sh.com.empty(f)
        self._blocks = [block for block in self._blocks \
                        if not block._text in patterns
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
                  and not self._blocks[i]._text[0] in sh.lg.punc_array \
                  and not self._blocks[i]._text[0] in [')',']','}'] \
                  and not cond:
                    self._blocks[i]._text = ' ' + self._blocks[i]._text

    def phrases(self):
        ''' #note: this must differ from
            'plugins.multitranru.elems.Elems.phrases' since the block to
            be found is of the 'term' (not 'phrase') type here.
        '''
        for block in self._blocks:
            if re.match('\d+ phrase',block._text) \
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
