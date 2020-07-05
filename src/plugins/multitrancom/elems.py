#!/usr/bin/python3
# -*- coding: UTF-8 -*-

''' This module prepares blocks after extracting tags for permanently
    storing in DB.
    Needs attributes in blocks: TYPE, DIC, WFORM, SPEECH, TRANSC,
    TERM, SAMECELL
    Modifies attributes:        TYPE, TEXT, DIC, WFORM, SPEECH,
    TRANSC, TERM, SAMECELL
    Since TYPE is modified here, SAMECELL is filled here.
    SELECTABLE cannot be filled because it depends on CELLNO which is
    created in Cells; Cells modifies TEXT of DIC, WFORM, SPEECH, TRANSC
    types, and we do not need to make empty cells SELECTABLE, so we
    calculate SELECTABLE fully in Cells.
'''

import re
import skl_shared.shared as sh
from skl_shared.localize import _


class Abbr:
    
    def __init__(self):
        self.set_values()
        self.set_file()
        self.load()
    
    def set_values(self):
        self.Success = True
        self.fabbr = ''
    
    def get_full(self,abbr):
        f = '[MClient] plugins.multitrancom.Abbr.get_full'
        if self.Success:
            if abbr:
                try:
                    index_ = self.dic.orig.index(abbr)
                    return self.dic.transl[index_]
                except ValueError:
                    pass
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
        return abbr
    
    def load(self):
        f = '[MClient] plugins.multitrancom.Abbr.load'
        if self.Success:
            self.dic = sh.Dic (file     = self.fabbr
                              ,Sortable = True
                              )
            self.Success = self.dic.Success
        else:
            sh.com.cancel(f)
    
    def set_file(self):
        f = '[MClient] plugins.multitrancom.Abbr.set_file'
        if self.Success:
            self.fabbr = sh.objs.get_pdir().add ('..','resources'
                                                ,'abbr.txt'
                                                )
            self.Success = sh.File(file=self.fabbr).Success
        else:
            sh.com.cancel(f)



class Same:
    ''' Finely adjust SAME fields here. Default SAME values are already
        set (as early as in 'Tags'), so rewrite them carefully.
    '''
    def __init__ (self,blocks,Debug=False
                 ,maxrow=70,maxrows=1000
                 ):
        self.blocks  = blocks
        self.Debug   = Debug
        self.maxrow  = maxrow
        self.maxrows = maxrows
    
    def run_user_cor_user(self):
        # (GeorgeK; это "тендерная документация" playa4life)
        i = 4
        while i < len(self.blocks):
            if self.blocks[i-4].type_ in ('comment','correction') \
            and self.blocks[i-3].type_ == 'user' \
            and self.blocks[i-2].type_ == 'correction' \
            and self.blocks[i-1].type_ == 'user' \
            and self.blocks[i].type_ in ('comment','correction') \
            and self.blocks[i-4].text.endswith('(') \
            and self.blocks[i].text.startswith(')'):
                self.blocks[i-3].same = 1
                self.blocks[i-2].same = 1
                self.blocks[i-1].same = 1
                self.blocks[i].same = 1
            i += 1
    
    def _has_extra_bracket(self,block):
        return block.text.count('(') > block.text.count(')')
    
    def run_user_brackets(self):
        i = 2
        while i < len(self.blocks):
            if self.blocks[i-2].type_ in ('comment','correction') \
            and self._has_extra_bracket(self.blocks[i-2]) \
            and self.blocks[i-1].type_ == 'user' \
            and self.blocks[i].text.startswith(')'):
                self.blocks[i-1].same = 1
                self.blocks[i].same = 1
            i += 1
    
    def run_com_term_com(self):
        i = 2
        while i < len(self.blocks):
            if self.blocks[i-2].type_ == 'comment' \
            and self.blocks[i-1].type_ == 'term' \
            and self.blocks[i].type_ in ('comment','correction'):
                if self.blocks[i-2].text.startswith('(') \
                and not ')' in self.blocks[i-2].text \
                and self.blocks[i].text.startswith(')'):
                    # 'self.blocks[i-2]' can actually have any SAME
                    self.blocks[i-1].same = 1
                    self.blocks[i].same = 1
            i += 1
    
    def run_wform_com_fixed(self):
        ''' Set a specific 'definition' type for blocks that are tagged
            by multitran.com as comments (or word forms, see
            'Elems.definitions') but are placed next to word forms.
            We create the new type since after removing fixed types
            there could be no other way to reinsert them without
            associating definitions with wrong cells (fixed types are
            reinserted when DIC, WFORM or SPEECH change, but there
            are cases when a definition block is duplicated
            by multitran.com and those fields remain unchanged, see,
            for example, 'memory pressure').
        '''
        i = 2
        while i < len(self.blocks):
            ''' Do not check the 'same' value of a definition block
                since it can (and should) already be set to 1.
            '''
            if self.blocks[i-2].type_ == 'wform' \
            and self.blocks[i-1].type_ == 'comment' \
            and self.blocks[i].type_ in ('dic','wform','transc'
                                        ,'speech'
                                        ):
                self.blocks[i-1].type_ = 'definition'
                ''' 'same' value of the definition block should
                    already be set to 1, but we assign it just to be
                    on a safe side.
                '''
                self.blocks[i-1].same = 1
            i += 1
    
    def run_wform_com_term(self):
        # Source-specific
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
        i = 1
        while i < len(self.blocks):
            ''' First comments in constructs like 'com-term-com' can be
                of SAME=0, so we should be careful here.
            '''
            if self.blocks[i].type_ == 'comment' \
            and self.blocks[i].text.startswith('(') \
            or self.blocks[i].type_ in ('user','correction'):
                if self.blocks[i-1].type_ not in ('dic','wform','transc'
                                                 ,'speech'
                                                 ):
                    self.blocks[i].same = 1
            i += 1
    
    def run_term_com_term(self):
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
                        self.blocks[i].same = 1
            i += 1
    
    def run_speech(self):
        ''' 'speech' blocks have 'same = 1' when analyzing MT because
            they are within a single tag. We fix it here, not in Tags,
            because Tags are assumed to output the result 'as is'.
        '''
        i = 1
        while i < len(self.blocks):
            if self.blocks[i-1].type_ == 'speech':
                self.blocks[i-1].same = 0
                self.blocks[i].same = 0
            i += 1
    
    def run_punc(self):
        for block in self.blocks:
            for sym in sh.lg.punc_array + [')']:
                if block.text.startswith(sym):
                    block.same = 1
                    break
    
    def debug(self):
        f = 'plugins.multitrancom.elems.Same.debug'
        if self.Debug:
            headers = ('NO','TYPE','TEXT','SAMECELL')
            rows = []
            for i in range(len(self.blocks)):
                rows.append ([i + 1
                             ,self.blocks[i].type_
                             ,self.blocks[i].text
                             ,self.blocks[i].same
                             ]
                            )
            mes = sh.FastTable (headers   = headers
                               ,iterable  = rows
                               ,maxrow    = self.maxrow
                               ,maxrows   = self.maxrows
                               ,Transpose = True
                               ).run()
            sh.com.run_fast_debug(f,mes)
    
    def run(self):
        f = 'plugins.multitrancom.elems.Same.run'
        if self.blocks:
            self.run_speech()
            self.run_all_coms()
            self.run_user_cor_user()
            self.run_user_brackets()
            self.run_term_com_term()
            self.run_term_com_fixed()
            self.run_com_com()
            self.run_wform_com_term()
            self.run_wform_com_fixed()
            self.run_com_term_com()
            # Can cause wrong SAME=1 if used beforehand
            self.run_com_term()
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
        self.sprior   = -1
        self.dprior   = 0
        ''' 'wform', 'speech', 'dic', 'phrase', 'term', 'comment',
            'correction', 'transc', 'user', 'invalid'
        '''
        self.type_  = 'invalid'
        self.text   = ''
        self.url    = ''
        self.dic    = ''
        self.dicf   = ''
        self.wform  = ''
        self.speech = ''
        self.transc = ''
        self.term   = ''



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
    def __init__ (self,blocks,abbr,langs
                 ,Debug=False,maxrow=20
                 ,maxrows=1000,search=''
                 ):
        f = '[MClient] plugins.multitrancom.elems.Elems.__init__'
        self.dicurls = {}
        self.defins  = []
        self.blocks  = blocks
        self.abbr    = abbr
        self.Debug   = Debug
        self.maxrow  = maxrow
        self.maxrows = maxrows
        self.pattern = search.strip()
        self.langs   = langs
        if self.blocks:
            self.Success = True
        else:
            self.Success = False
            sh.com.rep_empty(f)
    
    def reassign_brackets(self):
        ''' It is a common case when an opening bracket, a phrase and 
            a closing bracket are 3 separate blocks. Tkinter (unlike
            popular web browsers) wraps these blocks after ')'.
            We just fix this behavior. This also allows to skip user
            names without showing extra brackets.
        '''
        i = 2
        while i < len(self.blocks):
            if self.blocks[i-2].text == '(' \
            and self.blocks[i].text == ')' \
            and self.blocks[i-1].type_ in ('comment','user','correction'
                                          ):
                self.blocks[i-1].text = '(' + self.blocks[i-1].text + ')'
                del self.blocks[i-2]
                i -= 1
                del self.blocks[i]
                i -= 1
            i += 1
    
    def expand_dic_file(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.expand_dic_file'
        for block in self.blocks:
            if block.dic and not block.dicf:
                dics = block.dic.split(', ')
                dicfs = []
                for dic in dics:
                    dicfs.append(objs.get_abbr().get_full(dic))
                block.dicf = ', '.join(dicfs)
    
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
    
    def delete_phantom(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.delete_phantom'
        ''' Delete a block that looks like a WFORM but has pluses
            instead of spaces and a colon on its end, e.g.,
            'data vector' -> 'data+vector:'. If the block ends with '!',
            then '!' will be omitted. Case is preserved.
        '''
        wforms = [block.text for block in self.blocks \
                  if block.text and block.type_ == 'wform'
                 ]
        wforms = sorted(set(wforms))
        compare = []
        for item in wforms:
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
                if block.dic == definition.dic \
                and block.wform == definition.wform \
                and block.speech == definition.speech:
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
    
    def set_term_same(self):
        ''' #NOTE: all blocks of the same cell must have the same TERM,
            otherwise, alphabetizing may put blocks with SAME=1 outside
            of their cells.
        '''
        term = ''
        for block in self.blocks:
            if block.same == 0:
                term = block.term
            elif block.same == 1:
                block.term = term
    
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
    
    def expand_dic(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.expand_dic'
        if self.abbr:
            for block in self.blocks:
                if block.dic in self.abbr:
                    block.dicf = self.abbr[block.dic]
                else:
                    ''' Each dictionary must have full and short titles.
                        This is especially needed for a phrase dic.
                    '''
                    block.dicf = block.dic
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
            # Set 'same' attribute and further change some types
            ''' We do not pass debug options here since Same debug has
                few columns and it is reasonable to make them wider than
                for Elems.
            '''
            self.blocks = Same (blocks = self.blocks
                               ,Debug  = self.Debug
                               ).run()
            self.reassign_brackets()
            # Prepare for cells
            self.fill()
            self.fill_term()
            self.delete_definitions()
            self.remove_fixed()
            self.insert_fixed()
            self.insert_definitions()
            self.set_fixed_term()
            self.expand_dic()
            self.expand_dic_file()
            self.set_term_same()
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
            headers = ('NO','TYPE','TEXT','SAMECELL','CELLNO','ROWNO'
                      ,'COLNO','POS1','POS2'
                      )
            rows = []
            for i in range(len(self.blocks)):
                rows.append ([i + 1
                             ,self.blocks[i].type_
                             ,self.blocks[i].text
                             ,self.blocks[i].same
                             ,self.blocks[i].cellno
                             ,self.blocks[i].i
                             ,self.blocks[i].j
                             ,self.blocks[i].first
                             ,self.blocks[i].last
                             ]
                            )
            mes = sh.FastTable (headers   = headers
                               ,iterable  = rows
                               ,maxrow    = self.maxrow
                               ,maxrows   = self.maxrows
                               ,Transpose = True
                               ).run()
            sh.com.run_fast_debug(f,mes)
        
    def set_transc(self):
        for block in self.blocks:
            if block.type_ == 'comment' \
            and block.text.startswith('[') \
            and block.text.endswith(']'):
                block.type_ = 'transc'
            
    def delete_trash(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.trash'
        patterns = ['|',';',':','-->','// -->','⇄','точно' ,'все формы'
                   ,'точные совпадения','Сообщить об ошибке'
                   ,'только в указанном порядке'
                   ,'только в заданной форме','all forms'
                   ,'exact matches only','in specified order only'
                   ,'Forvo','Google'
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
            if re.match('\d+ phrase[s]{0,1}',block.text) \
            or re.match('\d+ фраз',block.text):
                block.type_ = 'dic'
                block.select = 1
                block.dic = block.text
                break
                
    def fill(self):
        dic = wform = speech = transc = term = ''
        
        # Find first non-empty values and set them as default
        for block in self.blocks:
            if block.type_ == 'dic':
                dic = block.text
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
                dic = block.text
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
            block.dic    = dic
            block.wform  = wform
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
        dic = wform = speech = ''
        i = 0
        while i < len(self.blocks):
            if dic != self.blocks[i].dic \
            or wform != self.blocks[i].wform \
            or speech != self.blocks[i].speech:
                
                block        = Block()
                block.type_  = 'speech'
                block.text   = self.blocks[i].speech
                block.dic    = self.blocks[i].dic
                block.wform  = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                block.term   = self.blocks[i].term
                block.same   = 0
                self.blocks.insert(i,block)
                
                block        = Block()
                block.type_  = 'transc'
                block.text   = self.blocks[i].transc
                block.dic    = self.blocks[i].dic
                block.wform  = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                block.term   = self.blocks[i].term
                block.same   = 0
                self.blocks.insert(i,block)

                block        = Block()
                block.type_  = 'wform'
                block.text   = self.blocks[i].wform
                block.dic    = self.blocks[i].dic
                block.wform  = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                block.term   = self.blocks[i].term
                block.same   = 0
                self.blocks.insert(i,block)
                
                block        = Block()
                block.type_  = 'dic'
                block.text   = self.blocks[i].dic
                block.dic    = self.blocks[i].dic
                block.wform  = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                block.term   = self.blocks[i].term
                block.same   = 0
                self.blocks.insert(i,block)
                
                dic    = self.blocks[i].dic
                wform  = self.blocks[i].wform
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



class Objects:
    
    def __init__(self):
        self.abbr = None
    
    def get_abbr(self):
        if self.abbr is None:
            self.abbr = Abbr()
        return self.abbr


objs = Objects()
