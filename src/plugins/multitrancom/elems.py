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
import skl_shared.shared as sh
from skl_shared.localize import _



class Same:
    ''' Finely adjust SAME fields here. Default SAME values are already
        set (as early as in 'Tags'), so rewrite them carefully.
    '''
    def __init__ (self,blocks,Debug=False
                 ,Shorten=True,MaxRow=70
                 ,MaxRows=200
                 ):
        self.blocks = blocks
        self.Debug   = Debug
        self.Shorten = Shorten
        self.MaxRow  = MaxRow
        self.MaxRows = MaxRows
    
    def run_wform_com_fixed(self):
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
        if len(self.blocks) > 2:
            i = 2
            while i < len(self.blocks):
                ''' Do not check the '_same' value of a definition block
                    since it can (and should) already be set to 1.
                '''
                if self.blocks[i-2].type_ == 'wform' \
                and self.blocks[i-1].type_ == 'comment' \
                and self.blocks[i].type_ in ('dic','wform','transc'
                                             ,'speech'
                                             ):
                   self.blocks[i-1].type_ = 'definition'
                   ''' '_same' value of the definition block should
                       already be set to 1, but we assign it just to be
                       on a safe side.
                   '''
                   self.blocks[i-1].same = 1
                i += 1
    
    def run_wform_com_term(self):
        # Source-specific
        if len(self.blocks) > 2:
            i = 2
            while i < len(self.blocks):
                if self.blocks[i-2].type_ == 'wform' \
                and self.blocks[i-2].same == 0 \
                and self.blocks[i-2].url \
                and self.blocks[i-1].type_ == 'comment' \
                and self.blocks[i-1].same == 0 \
                and self.blocks[i].type_ == 'term' \
                and self.blocks[i].same == 1:
                   self.blocks[i-2].type_ = 'term'
                   self.blocks[i-1].same = 1
                i += 1
    
    def run_com_com(self):
        ''' Fix the 'comment (SAME=0) - comment (SAME=0)' structure
            which may be encountered due to that word forms can be
            indistinguishable from comments. The latter happens only in
            the present source, so this code is plugin-specific.
        '''
        if len(self.blocks) > 2:
            i = 2
            while i < len(self.blocks):
                if self.blocks[i-1].type_ == 'comment' \
                and self.blocks[i-1].same == 0 \
                and self.blocks[i].type_ == 'comment' \
                and self.blocks[i].same == 0:
                    if self.blocks[i-2].type_ in ('dic','wform'
                                                  ,'speech','transc'
                                                  ):
                        self.blocks[i-1].type_ = 'wform'
                        self.blocks[i].same = 1
                    else:
                        self.blocks[i-1].same = 1
                i += 1
    
    def run_com_term(self):
        ''' If a comment has SAME=0, then the next non-fixed type block
            must have SAME=1 because the comment cannot occupy
            an entire cell (otherwise, this is actually, for example,
            a word form). I do not use 'correction' and 'user' types
            here since they come only after other blocks and always have
            SAME=1.
        '''
        if len(self.blocks) > 1:
            i = 1
            while i < len(self.blocks):
                if self.blocks[i-1].type_ == 'comment' \
                and self.blocks[i-1].same == 0:
                    if self.blocks[i].type_ == 'term':
                        self.blocks[i].same = 1
                    else:
                        self.blocks[i-1].same = 1
                i += 1
    
    def run_term_com_fixed(self):
        ''' Set SAME value of a comment prior to a fixed type to 1
            even if it does not comprise brackets.
        '''
        if len(self.blocks) > 2:
            i = 2
            while i < len(self.blocks):
                if self.blocks[i-2].type_ == 'term' \
                and self.blocks[i-1].type_ == 'comment' \
                and self.blocks[i].type_ in ('dic','wform','speech'
                                             ,'transc'
                                             ):
                    self.blocks[i-1].same = 1
                i += 1
    
    def run_all_coms(self):
        for block in self.blocks:
            if (block.type_ == 'comment' and block.text.startswith('(')\
               ) or block.type_ in ('user','correction'):
                block.same = 1
    
    def run_term_com_term(self):
        if len(self.blocks) > 2:
            i = 2
            while i < len(self.blocks):
                if self.blocks[i-2].type_ == 'term' \
                and self.blocks[i-1].type_ == 'comment' \
                and self.blocks[i].type_ == 'term':
                    ''' There can be a 'comment-term; comment-term' case
                        (with the comments having SAME=1) which
                        shouldn't be matched. See multitran.com:
                        eng-rus: 'tree limb'.
                    '''
                    if not self.blocks[i-1].text.startswith('('):
                        cond1 = sh.Text(self.blocks[i-2].text).has_cyrillic()\
                                and sh.Text(self.blocks[i-1].text).has_cyrillic()\
                                and sh.Text(self.blocks[i].text).has_cyrillic()
                        cond2 = sh.Text(self.blocks[i-2].text).has_latin()\
                                and sh.Text(self.blocks[i-1].text).has_latin()\
                                and sh.Text(self.blocks[i].text).has_latin()
                        if cond1 or cond2:
                            self.blocks[i-1].same = 1
                            self.blocks[i  ].same = 1
                i += 1
    
    def run_speech(self):
        ''' 'speech' blocks have '_same = 1' when analyzing MT because
            they are within a single tag. We fix it here, not in Tags,
            because Tags are assumed to output the result 'as is'.
        '''
        for i in range(len(self.blocks)):
            if self.blocks[i].type_ == 'speech':
                self.blocks[i].same = 0
                if i < len(self.blocks) - 1:
                    self.blocks[i+1].same = 0
    
    def run_punc(self):
        for block in self.blocks:
            for sym in sh.lg.punc_array:
                if block.text.startswith(sym):
                    block.same = 1
                    break
    
    def debug(self):
        f = 'plugins.multitrancom.elems.Same.debug'
        if self.Debug:
            mes = _('Debug table:')
            sh.objs.get_mes(f,mes,True).show_debug()
            headers = ['TYPE','TEXT','SAMECELL']
            rows = []
            for block in self.blocks:
                rows.append([block.type_,block.text,block.same])
            sh.Table (headers = headers
                     ,rows    = rows
                     ,Shorten = self.Shorten
                     ,MaxRow  = self.MaxRow
                     ,MaxRows = self.MaxRows
                     ).print()
    
    def run(self):
        f = 'plugins.multitrancom.elems.Same.run'
        if self.blocks:
            self.run_speech()
            self.run_all_coms()
            self.run_term_com_term()
            self.run_term_com_fixed()
            self.run_com_com()
            self.run_wform_com_term()
            self.run_com_term()
            self.run_wform_com_fixed()
            self.run_punc()
            self.debug()
            return self.blocks
        else:
            sh.com.rep_empty(f)
            return []



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
        self.dicurls = {}
        self.defins  = []
        self.blocks  = blocks
        self.abbr    = iabbr
        self.Debug   = Debug
        self.Shorten = Shorten
        self.MaxRow  = MaxRow
        self.MaxRows = MaxRows
        self.pattern = search.strip()
        self.langs   = langs
        if self.blocks:
            self.Success = True
        else:
            self.Success = False
            sh.com.rep_empty(f)
    
    def fix_thesaurus(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.fix_thesaurus'
        for i in range(len(self.blocks)):
            if self.blocks[i].text in ('русский тезаурус'
                                      ,'английский тезаурус'
                                      ,'Russian thesaurus'
                                      ,'English thesaurus'
                                      ):
                self.blocks[i].type_ = 'definition'
                self.blocks[i].same = 1
                if i + 1 < len(self.blocks):
                    if self.blocks[i+1].type_ == 'dic':
                        self.blocks[i], self.blocks[i+1] = \
                        self.blocks[i+1], self.blocks[i]
    
    def delete_set_form(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.delete_set_form'
        patterns = ['только в заданном порядке \d+'
                   ,'только заданная форма слов \d+'
                   ,'только в заданной форме \d+'
                   ,'только в указанном порядке \d+'
                   ,'exact matches only \d+'
                   ,'in specified order only \d+'
                   ]
        i = 0
        count = 0
        while i < len(self.blocks):
            for pattern in patterns:
                if re.match(pattern,self.blocks[i].text):
                    del self.blocks[i]
                    i -= 1
                    count += 1
                    break
            i += 1
        if count:
            mes = _('{} blocks have been deleted').format(count)
            sh.objs.get_mes(f,mes,True).show_info()
        else:
            sh.com.rep_lazy(f)
    
    def delete_phantom(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.delete_phantom'
        ''' Delete a block that looks like a WFORM but has pluses
            instead of spaces and a colon on its end, e.g.,
            'data vector' -> 'data+vector:'. If the block ends with '!',
            then '!' will be omitted. Case is preserved.
        '''
        wformas = [block.text for block in self.blocks \
                   if block.text and block.type_ == 'wform'
                  ]
        wformas = sorted(set(wformas))
        compare = []
        for item in wformas:
            item = item.replace(' ','+')
            # We have already deleted empty items
            if item[-1] in sh.lg.punc_array:
                item = item[:-1]
            item += ':'
            compare.append(item)
        i = 0
        count = 0
        while i in range(len(self.blocks)):
            if self.blocks[i].text in compare:
                count += 1
                del self.blocks[i]
                i -= 1
            i += 1
        if count:
            mes = _('{} blocks have been deleted').format(count)
            sh.objs.get_mes(f,mes,True).show_info()
        else:
            sh.com.rep_lazy(f)
    
    def delete_numeration(self):
        self.blocks = [block for block in self.blocks \
                        if not re.match('^\d+\.$',block.text)
                       ]
    
    def search_definition(self,block):
        f = '[MClient] plugins.multitrancom.elems.Elems.search_definition'
        if block:
            for definition in self.defins:
                if block.dica == definition.dica \
                and block.wforma == definition.wforma \
                and block.speecha == definition.speecha:
                    mes = '"{}"'.format(definition.text)
                    sh.objs.get_mes(f,mes,True).show_debug()
                    self.defins.remove(definition)
                    return definition
        else:
            sh.com.rep_empty(f)
    
    def insert_definitions(self):
        ''' Reisert definitions after word forms
            #NOTE: Do this after reinserting fixed types.
        '''
        f = '[MClient] plugins.multitrancom.elems.Elems.insert_definitions'
        if self.defins:
            i = 0
            while i < len(self.blocks):
                if self.blocks[i].type_ == 'wform':
                    block = self.search_definition(self.blocks[i])
                    if block:
                        self.blocks.insert(i+1,block)
                        i += 1
                i += 1
        else:
            sh.com.rep_lazy(f)
    
    def delete_definitions(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.delete_definitions'
        self.defins = [block for block in self.blocks
                        if block.type_ == 'definition'
                       ]
        self.blocks = [block for block in self.blocks
                        if block.type_ != 'definition'
                       ]
        if self.defins:
            mes = _('{} blocks have been deleted')
            mes = mes.format(len(self.defins))
            sh.objs.get_mes(f,mes,True).show_info()
        else:
            sh.com.rep_lazy(f)
    
    def delete_empty(self):
        ''' - Empty blocks are useless since we recreate fixed columns
              anyways.
            - This is required since we decode HTM entities after
              extracting tags now. Empty blocks may lead to a wrong
              analysis of blocks, e.g.,
              'comment (SAME=0) - comment (SAME=1)' structure, where
              the second block is empty, will be mistakenly converted
              to 'wform - comment'.
        '''
        self.blocks = [block for block in self.blocks if block.text]
    
    def set_terma_same(self):
        ''' #NOTE: all blocks of the same cell must have the same TERMA,
            otherwise, alphabetizing may put blocks with SAME=1 outside
            of their cells.
        '''
        terma = ''
        for block in self.blocks:
            if block.same == 0:
                terma = block.terma
            elif block.same == 1:
                block.terma = terma
    
    def delete_subjects(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.subjects'
        pattern = '(в|in) \d+ (тематиках|тематике|subjects)'
        count = 0
        i = 0
        while i < len(self.blocks):
            if re.match(pattern,self.blocks[i].text):
                del self.blocks[i]
                count += 1
                i -= 1
            i += 1
        mes = _('{} blocks have been deleted').format(count)
        sh.objs.get_mes(f,mes,True).show_info()
    
    def set_corrections(self):
        ''' Replace 'comment' with 'correction' in
            the 'correction-user-comment-user' structure.
        '''
        if len(self.blocks) > 3:
            i = 3
            while i < len(self.blocks):
                if self.blocks[i-3].type_ == 'correction' \
                and self.blocks[i-2].type_ == 'user' \
                and self.blocks[i-1].type_ == 'comment' \
                and self.blocks[i].type_ == 'user':
                    self.blocks[i-1].type_ = 'correction'
                i += 1
    
    def set_users(self):
        ''' User names are initially comments at 'multitran.ru', and
            terms at 'multitran.com'.
        '''
        for block in self.blocks:
            if block.type_ == 'term' and 'UserName' in block.url:
                block.type_ = 'user'
    
    def strip(self):
        for block in self.blocks:
            block.text = block.text.strip()
    
    def delete_search(self):
        ''' Remove a block that looks like "SEARCH:" and comes before
            the phrase "NUMBER phrases in NUMBER subjects".
            Interestingly enough, the server preserves the case of
            mY sEaRch, so there is no need to make the search
            lower-case.
        '''
        f = '[MClient] plugins.multitrancom.elems.Elems.delete_search'
        if self.pattern:
            count = 0
            i = 0
            while i < len(self.blocks):
                if self.blocks[i].type_ == 'comment' \
                and self.blocks[i].text == self.pattern + ':':
                    del self.blocks[i]
                    count += 1
                    i -= 1
                i += 1
            if count:
                mes = _('{} blocks have been deleted').format(count)
                sh.objs.get_mes(f,mes,True).show_info()
        else:
            sh.com.rep_empty(f)
    
    def set_definitions(self):
        ''' Definitions are tagged just like word forms, and we can
            judge upon the type only by the length of the block.
            The value of 30 is picked up on the basis of
            a trial-and-error method.
            Examples of long word forms (28+ symbols):
            'закрытая нуклеиновая кислота',
            'nucleoside reverse transcriptase inhibitors'.
        '''
        HasWform = False
        for block in self.blocks:
            # The 'definition' type cannot precede word forms
            if block.type_ == 'wform':
                if len(block.text) > 30 and HasWform:
                    block.type_ = 'definition'
                    block.same = 1
                HasWform = True
    
    # Takes ~0,26s for 'set' on AMD E-300.
    def expand_dica(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.expand_dica'
        if self.abbr:
            if self.abbr.Success:
                for block in self.blocks:
                    lst = block.dica.split(',')
                    for i in range(len(lst)):
                        lst[i] = lst[i].strip()
                        try:
                            ind = self.abbr.orig.index(lst[i])
                            lst[i] = self.abbr.transl[ind]
                        except ValueError:
                            pass
                    block.dicaf = ', '.join(lst)
            else:
                sh.com.cancel(f)
        else:
            sh.com.rep_empty(f)
    
    def run(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.run'
        if self.Success:
            # Do some cleanup
            self.strip()
            self.delete_empty()
            self.delete_trash()
            self.delete_subjects()
            self.delete_search()
            self.delete_phantom()
            self.delete_set_form()
            self.delete_numeration()
            # Reassign types
            self.fix_thesaurus()
            self.set_transc()
            self.set_users()
            self.set_phrases()
            self.set_corrections()
            self.set_definitions()
            # Prepare contents
            self.set_dic_urls()
            self.add_brackets()
            self.set_user_brackets()
            # Set '_same' attribute and further change some types
            ''' We do not pass debug options here since Same debug has
                few columns and it is reasonable to make them wider than
                for Elems.
            '''
            self.blocks = Same (blocks = self.blocks
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
            self.set_terma_same()
            # Extra spaces in the beginning may cause sorting problems
            self.add_space()
            #TODO: expand parts of speech (n -> noun, etc.)
            self.set_selectables()
            self.restore_dic_urls()
            self.debug()
            return self.blocks
        else:
            sh.com.cancel(f)
    
    def debug(self):
        f = 'plugins.multitrancom.elems.Elems.debug'
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
        for block in self.blocks:
            if block.type_ == 'comment' \
            and block.text.startswith('[') \
            and block.text.endswith(']'):
                block.type_ = 'transc'
    
    def add_brackets(self):
        for block in self.blocks:
            if block.type_ in ('comment','correction') \
            and '(' in block.text and not ')' in block.text:
                block.text += ')'
    
    def set_user_brackets(self):
        for block in self.blocks:
            if block.type_ == 'user':
                if not block.text.startswith('('):
                    block.text = '(' + block.text
                if not block.text.endswith(')'):
                    block.text += ')'
            
    def delete_trash(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.trash'
        patterns = ['|',';',':','(',')','-->','// -->','⇄','точно'
                   ,'все формы','точные совпадения','Сообщить об ошибке'
                   ]
        if self.langs:
            patterns += list(self.langs)
        else:
            sh.com.rep_empty(f)
        self.blocks = [block for block in self.blocks \
                        if not block.text in patterns
                       ]
    
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

    def set_phrases(self):
        ''' #NOTE: this must differ from
            'plugins.multitranru.elems.Elems.phrases' since the block to
            be found is of the 'term' (not 'phrase') type here.
        '''
        for block in self.blocks:
            if re.match('\d+ phrase',block.text) \
            or re.match('\d+ фраз',block.text):
                block.type_   = 'dic'
                block.select = 1
                block.dica   = block.text
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
            block.dica    = dica
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
            
    def fixed_terma(self):
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
                
                block         = Block()
                block.type_   = 'speech'
                block.text    = self.blocks[i].speecha
                block.dica    = self.blocks[i].dica
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
    
    def set_dic_urls(self):
        for block in self.blocks:
            if block.type_ == 'dic' \
            and not block.text in self.dicurls:
                self.dicurls[block.text] = block.url
    
    def restore_dic_urls(self):
        for i in range(len(self.blocks)):
            if self.blocks[i].type_ == 'dic' \
            and self.blocks[i].text in self.dicurls:
                self.blocks[i].url = self.dicurls[self.blocks[i].text]
