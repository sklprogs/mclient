#!/usr/bin/python3
# -*- coding: UTF-8 -*-

''' This module prepares blocks after extracting tags for permanently
    storing in DB.
    Needs attributes in blocks: DIC,DICF,SAMECELL,SPEECH,TERM,TRANSC
                               ,TYPE,WFORM
    Modifies attributes: DIC,DICF,SAMECELL,SELECTABLE,SPEECH,TERM,TEXT
                        ,TRANSC,TYPE,WFORM
    Since TYPE is modified here, SAMECELL is filled here.
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
        self.fabbr = ''
        self.Success = True
    
    def get_full(self,abbr):
        f = '[MClient] plugins.multitrancom.elems.Abbr.get_full'
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
        f = '[MClient] plugins.multitrancom.elems.Abbr.load'
        if self.Success:
            self.dic = sh.Dic (file = self.fabbr
                              ,Sortable = True
                              )
            self.Success = self.dic.Success
        else:
            sh.com.cancel(f)
    
    def set_file(self):
        f = '[MClient] plugins.multitrancom.elems.Abbr.set_file'
        if self.Success:
            self.fabbr = sh.objs.get_pdir().add ('..','resources'
                                                ,'abbr.txt'
                                                )
            self.Success = sh.File(self.fabbr).Success
        else:
            sh.com.cancel(f)



# A copy of Tags.Block
class Block:
    
    def __init__(self):
        self.block = -1
        # Applies to non-blocked cells only
        self.cellno = -1
        self.rowno = -1
        self.dic = ''
        self.dicf = ''
        self.dprior = 0
        self.first = -1
        self.i = -1
        self.semino = -1
        self.j = -1
        self.last = -1
        self.no = -1
        self.same = -1
        ''' 'select' is an attribute of a *cell* which is valid
            if the cell has a non-blocked block of types 'term',
            'phrase' or 'transc'
        '''
        self.select = -1
        self.speech = ''
        self.sprior = -1
        self.term = ''
        self.text = ''
        self.transc = ''
        ''' 'comment', 'correction', 'dic', 'invalid', 'phrase',
            'speech', 'term', 'transc', 'user', 'wform'
        '''
        self.type_ = 'invalid'
        self.url = ''
        self.wform = ''



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
    def __init__(self,blocks,Debug=False,maxrows=1000,abbr={}):
        self.defins = []
        self.dicurls = {}
        self.phdic = ''
        self.fixed = ('dic','wform','transc','speech')
        self.abbr = abbr
        self.blocks = blocks
        self.Debug = Debug
        self.maxrows = maxrows
    
    def get_separate_head(self):
        blocks = ('Forvo','|','+')
        texts = [block.text for block in self.blocks]
        return sh.List(texts,blocks).find()
    
    def get_separate_tail(self):
        i = 0
        while i < len(self.blocks):
            ''' If the last word is correct, then 'block.text' will be
                ' - найдены отдельные слова', otherwise, it will be
                ' wrong_word - найдены отдельные слова'.
            '''
            if ' - найдены отдельные слова' in self.blocks[i].text \
            or ' - only individual words found' in self.blocks[i].text:
                return i
            i += 1
    
    def set_separate(self):
        # Takes ~0.0109s for 'set' (EN-RU) on AMD E-300
        f = '[MClient] plugins.multitrancom.elems.Elems.set_separate'
        head = self.get_separate_head()
        if head:
            head = head[0]
            tail = self.get_separate_tail()
            if tail:
                self.blocks = self.blocks[head+3:tail+1]
                self.blocks = [block for block in self.blocks \
                               if not block.text in ('+','|')
                              ]
                for block in self.blocks:
                    ''' Those words that were not found will not have
                        a URL and should be kept as comments (as in
                        a source). However, SAME should be 0 everywhere.
                    '''
                    if block.url:
                        block.type_ = 'term'
                    else:
                        block.text = block.text.replace(' - найдены отдельные слова','')
                        block.text = block.text.replace(' - only individual words found','')
                    block.same = 0
                block = Block()
                block.type_ = 'dic'
                block.text = block.dic = block.dicf = _('Separate words')
                block.same = 0
                self.blocks.insert(0,block)
                ''' The last matching block may be a comment with no
                    text since we have deleted ' - найдены отдельные
                    слова'. Zero-length blocks are not visible in
                    a one-row table, so this may be needed just to
                    output a correct number of matches.
                '''
                self.blocks = [block for block in self.blocks \
                               if block.text
                              ]
                for i in range(len(self.blocks)):
                    mes = '{}: "{}", {}'.format(i+1,self.blocks[i].text,self.blocks[i].type_)
                    print(mes)
                sh.com.rep_matches(f,len(self.blocks))
            else:
                sh.com.rep_lazy(f)
        else:
            sh.com.rep_lazy(f)
    
    def make_fixed(self):
        # Takes ~0.0064s for 'set' (EN-RU) on AMD E-300
        f = '[MClient] plugins.multitrancom.elems.Elems.make_fixed'
        count = 0
        i = 1
        while i < len(self.blocks):
            if self.blocks[i-1].rowno != self.blocks[i].rowno \
            and self.blocks[i].type_ == 'user':
                self.blocks[i].type_ = 'dic'
                ''' Since this block is originally not DIC, we should
                    set DICF at the step of 'self.expand_dic_file'.
                '''
                self.blocks[i].dic = self.blocks[i].text
                count += 1
            i += 1
        sh.com.rep_matches(f,count)
    
    def set_synonyms(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.set_synonyms'
        count = 0
        i = 2
        while i < len(self.blocks):
            if self.blocks[i-2].rowno != self.blocks[i-1].rowno \
            and self.blocks[i-1].text == '⇒ ' \
            and self.blocks[i-1].rowno == self.blocks[i].rowno \
            and self.blocks[i-1].cellno == self.blocks[i].cellno:
                self.blocks[i-1].type_ = 'dic'
                self.blocks[i-1].dic = _('syn.')
                self.blocks[i-1].text = _('syn.')
                self.blocks[i-1].dicf = _('Synonyms')
                self.blocks[i-1].same = 0
                self.blocks[i].same = 0
                count += 2
            i += 1
        sh.com.rep_matches(f,count)
    
    def set_phcount(self):
        for block in self.blocks:
            if block.type_ == 'phcount':
                block.text = ' [{}]'.format(block.text)
                block.same = 1
    
    def set_same(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.set_same'
        # I have witnessed this error despite 'self.check' was passed
        if self.blocks:
            self.blocks[0].same = 0
            i = 1
            while i < len(self.blocks):
                # multitran.com originally sets some types with SAME = 1
                if self.blocks[i-1].semino != self.blocks[i].semino \
                or self.blocks[i-1].rowno != self.blocks[i].rowno \
                or self.blocks[i-1].cellno != self.blocks[i].cellno \
                or self.blocks[i].type_ in ('speech','transc'):
                    self.blocks[i].same = 0
                elif self.blocks[i].same == -1:
                    # Do not overwrite SAME of fixed types
                    self.blocks[i].same = 1
                i += 1
        else:
            sh.com.rep_empty(f)
    
    def _delete_tail_links(self,poses):
        f = '[MClient] plugins.multitrancom.elems.Elems._delete_tail_links'
        if poses:
            pos1, pos2 = poses[0], poses[1] + 1
            self.blocks[pos1:pos2] = []
            sh.com.rep_deleted(f,pos2-pos1)
    
    def delete_tail_links(self):
        ''' - Sometimes it's not enough to delete comment-only tail
              since there might be no 'phdic' type which serves as
              an indicator.
            - Takes ~0.005s for 'set' (EN-RU) on AMD E-300
        '''
        ru = ('Добавить','|','Сообщить об ошибке','|'
             ,'Способы выбора языков'
             )
        en = ('Add','|','Report an error','|','Language Selection Tips')
        texts = [block.text for block in self.blocks]
        self._delete_tail_links(sh.List(texts,ru).find())
        self._delete_tail_links(sh.List(texts,en).find())
        ru = ('спросить в форуме','Добавить','|','Способы выбора языков')
        en = ('ask in forum','Add','|','Language Selection Tips')
        self._delete_tail_links(sh.List(texts,ru).find())
        self._delete_tail_links(sh.List(texts,en).find())
    
    def delete_site_coms(self):
        ''' Sometimes it's not enough to delete comment-only tail since
            there might be no 'phdic' type which serves as an indicator.
        '''
        f = '[MClient] plugins.multitrancom.elems.Elems.delete_site_coms'
        len_ = len(self.blocks)
        self.blocks = [block for block in self.blocks \
                       if block.text not in ('<!--','-->')
                      ]
        sh.com.rep_deleted(f,len_-len(self.blocks))
    
    def set_phdic(self):
        # Takes ~0.001s for 'set' (EN-RU) on AMD E-300
        f = '[MClient] plugins.multitrancom.elems.Elems.set_phdic'
        index_ = self.get_phdic()
        if index_ is None:
            sh.com.rep_lazy(f)
        else:
            text = self.blocks[index_+1].text + self.blocks[index_+2].text
            url = self.blocks[index_+1].url
            del self.blocks[index_]
            del self.blocks[index_]
            self.blocks[index_].type_ = 'phdic'
            self.phdic = self.blocks[index_].text = text
            self.blocks[index_].url = url
            self.blocks[index_].select = 1
            self.blocks[index_].dic = self.blocks[index_].dicf \
                                    = self.blocks[index_].text
    
    def get_phdic(self):
        ''' Sample blocks:
            comment, comment, comment, phrase
            " process: ", "17416 фраз", " в 327 тематиках", "3D-печать"
        '''
        f = '[MClient] plugins.multitrancom.elems.Elems.get_phdic'
        i = len(self.blocks) - 1
        while i > 3:
            if self.blocks[i-3].type_ == 'comment' \
            and self.blocks[i-2].type_ == 'comment' \
            and self.blocks[i-1].type_ == 'comment' \
            and self.blocks[i].type_ == 'phrase':
                return i - 3
            i -= 1
    
    def delete_head(self):
        # Takes ~0.003s for 'set' (EN-RU) on AMD E-300
        f = '[MClient] plugins.multitrancom.elems.Elems.delete_head'
        count = 0
        i = 0
        while i < len(self.blocks):
            if self.blocks[i].type_ == 'comment':
                del self.blocks[i]
                count += 1
                i -= 1
            else:
                break
            i += 1
        sh.com.rep_deleted(f,count)
    
    def get_tail(self):
        i = len(self.blocks) - 1
        while i > 0:
            if self.blocks[i-1].type_ == 'phrase' \
            and self.blocks[i].type_ == 'phcount':
                return i
            i -= 1
    
    def delete_tail(self):
        # Takes ~0.0004s for 'set' (EN-RU) on AMD E-300
        f = '[MClient] plugins.multitrancom.elems.Elems.delete_tail'
        count = 0
        last = self.get_tail()
        if last is None or last + 1 == len(self.blocks):
            sh.com.rep_lazy(f)
        else:
            last += 1
            count = len(self.blocks) - last
            self.blocks = self.blocks[:last]
            sh.com.rep_deleted(f,count)
    
    def unite_fixed_same(self):
        ''' We should unite items in 'fixed+comment (SAME=1)' structures
            directly since fixed columns having supplementary SAME=1
            blocks cannot be properly sorted.
        '''
        f = '[MClient] plugins.multitrancom.elems.Elems.unite_fixed_same'
        count = 0
        i = 2
        while i < len(self.blocks):
            if self.blocks[i-2].type_ in self.fixed \
            and self.blocks[i-1].same == 1 and self.blocks[i].same == 0:
                mes = '"{}" <- "{}"'
                mes = mes.format (self.blocks[i-2].text
                                 ,self.blocks[i-1].text
                                 )
                sh.objs.get_mes(f,mes,True).show_debug()
                self.blocks[i-2].text = sh.List ([self.blocks[i-2].text
                                                 ,self.blocks[i-1].text
                                                 ]
                                                ).space_items()
                del self.blocks[i-1]
                i =- 1
                count += 1
            i += 1
        sh.com.rep_deleted(f,count)
    
    def delete_semi(self):
        # I don't like '; ' in special pages, so I delete it everywhere
        f = '[MClient] plugins.multitrancom.elems.Elems.delete_semi'
        len_ = len(self.blocks)
        self.blocks = [block for block in self.blocks \
                       if block.text != '; '
                      ]
        sh.com.rep_deleted(f,len_-len(self.blocks))
    
    def set_semino(self):
        semino = 0
        for block in self.blocks:
            if block.text == '; ' and block.type_ == 'term':
                semino += 1
            block.semino = semino
    
    def check(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.check'
        if self.blocks:
            return True
        else:
            sh.com.rep_empty(f)
    
    def reassign_brackets(self):
        ''' It is a common case when an opening bracket, a phrase and 
            a closing bracket are 3 separate blocks. Tkinter (unlike
            popular web browsers) wraps these blocks after ')'.
            We just fix this behavior. This also allows to skip user
            names without showing extra brackets.
        '''
        f = '[MClient] plugins.multitrancom.elems.Elems.reassign_brackets'
        count = 0
        i = 2
        while i < len(self.blocks):
            if self.blocks[i-2].text == '(' \
            and self.blocks[i].text == ')' \
            and self.blocks[i-1].type_ in ('comment','user','correction'
                                          ):
                count += 2
                self.blocks[i-1].text = '(' + self.blocks[i-1].text + ')'
                del self.blocks[i-2]
                i -= 1
                del self.blocks[i]
                i -= 1
            i += 1
        sh.com.rep_deleted(f,count)
    
    def expand_dic_file(self):
        ''' Do not delete this, since 'multitran.com' does not provide
            full dictionary titles in phrase articles!
        '''
        f = '[MClient] plugins.multitrancom.elems.Elems.expand_dic_file'
        for block in self.blocks:
            if block.dic and not block.dicf:
                dics = block.dic.split(', ')
                dicfs = []
                for dic in dics:
                    dicfs.append(objs.get_abbr().get_full(dic))
                block.dicf = ', '.join(dicfs)
    
    def delete_numeration(self):
        # Takes ~0.027s for 'set' (EN-RU) on AMD E-300
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
        # Reisert definitions after word forms
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
        sh.com.rep_deleted(f,len(self.defins))
    
    def delete_empty(self):
        ''' - Empty blocks are useless since we recreate fixed columns
              anyways.
            - The most common example of an empty block is a wform-type
              block with ' ' text.
            - Takes ~0.0041s for 'set' (EN-RU) on AMD E-300
        '''
        f = '[MClient] plugins.multitrancom.elems.Elems.delete_empty'
        len_ = len(self.blocks)
        self.blocks = [block for block in self.blocks \
                       if block.text.strip()
                      ]
        count = len_ - len(self.blocks)
        sh.com.rep_deleted(f,count)
    
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
    
    def get_suggested(self):
        for i in range(len(self.blocks)):
            if self.blocks[i].text in (' Варианты замены: '
                                      ,' Suggest: '
                                      ):
                return i
    
    def is_special_page(self):
        if set([block.type_ for block in self.blocks]) == {'comment'}:
            return True
    
    def set_suggested(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.set_suggested'
        count = 0
        i = self.get_suggested()
        if i is None:
            sh.com.rep_lazy(f)
        else:
            rowno = self.blocks[i].rowno
            self.blocks[i].type_ = 'dic'
            self.blocks[i].text = _('Suggestions')
            self.blocks[i].dic = _('Suggestions')
            self.blocks[i].dicf = _('Suggestions')
            self.blocks[i].same = 0
            count += 1
            i += 1
            while i < len(self.blocks):
                if self.blocks[i].rowno == rowno:
                    if self.blocks[i].text != '; ':
                        self.blocks[i].type_ = 'term'
                        self.blocks[i].same = 0
                        count += 1
                else:
                    break
                i += 1
        sh.com.rep_matches(f,count)
    
    def run(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.run'
        if self.check():
            # Process special pages before deleting anything
            if self.is_special_page():
                self.set_suggested()
            self.set_separate()
            # Do this before deleting ';'
            self.set_semino()
            # Do some cleanup
            self.delete_head()
            self.delete_tail()
            self.delete_empty()
            self.delete_semi()
            self.delete_numeration()
            self.delete_site_coms()
            self.delete_tail_links()
            # Reassign types
            self.set_phdic()
            self.set_transc()
            self.set_synonyms()
            self.make_fixed()
            self.set_same()
            # Prepare contents
            self.set_dic_urls()
            self.set_phcount()
            self.unite_fixed_same()
            self.reassign_brackets()
            # Prepare for cells
            self.fill()
            self.fill_term()
            self.delete_definitions()
            self.remove_fixed()
            self.insert_fixed()
            # Do this after reinserting fixed types
            self.insert_definitions()
            self.set_fixed_term()
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
            headers = ('NO','TYPE','TEXT','URL','SAME','SEMINO','ROWNO'
                      ,'CELLNO','SELECT','DIC','DICF','TERM'
                      )
            rows = []
            for i in range(len(self.blocks)):
                rows.append ([i + 1
                             ,self.blocks[i].type_
                             ,'"{}"'.format(self.blocks[i].text)
                             ,'"{}"'.format(self.blocks[i].url)
                             ,self.blocks[i].same
                             ,self.blocks[i].semino
                             ,self.blocks[i].rowno
                             ,self.blocks[i].cellno
                             ,self.blocks[i].select
                             ,self.blocks[i].dic
                             ,self.blocks[i].dicf
                             ,self.blocks[i].term
                             ]
                            )
            # 23'' monitor: 20 symbols per a column
            mes = sh.FastTable (headers = headers
                               ,iterable = rows
                               ,maxrow = 20
                               ,maxrows = self.maxrows
                               ,Transpose = True
                               ).run()
            sh.com.run_fast_debug(f,mes)
        
    def set_transc(self):
        # Takes ~0.003s for 'set' (EN-RU) on AMD E-300
        f = '[MClient] plugins.multitrancom.elems.Elems.set_transc'
        count = 0
        for block in self.blocks:
            if block.type_ == 'comment' and block.text.startswith('[') \
            and block.text.endswith(']'):
                block.type_ = 'transc'
                count += 1
        sh.com.rep_matches(f,count)
    
    def add_space(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.add_space'
        count = 0
        i = 1
        while i < len(self.blocks):
            if self.blocks[i].same > 0:
                if self.blocks[i].text and self.blocks[i-1].text \
                  and not self.blocks[i].text[0].isspace() \
                  and not self.blocks[i].text[0] in sh.lg.punc_array \
                  and not self.blocks[i].text[0] in [')',']','}'] \
                  and not self.blocks[i-1].text[-1] in ['(','[','{']:
                      count += 1
                      self.blocks[i].text = ' ' + self.blocks[i].text
            i += 1
        if count:
            mes = _('{} matches').format(count)
            sh.objs.get_mes(f,mes,True).show_debug()

    def fill(self):
        dic = dicf = wform = speech = transc = term = ''
        
        # Find first non-empty values and set them as default
        for block in self.blocks:
            if block.type_ in ('dic','phdic'):
                dic = block.dic
                dicf = block.dicf
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
            if block.type_ in ('term','phrase'):
                term = block.text
                break
        
        for block in self.blocks:
            if block.type_ in ('dic','phdic'):
                dic = block.dic
                dicf = block.dicf
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
            block.dic = dic
            block.dicf = dicf
            block.wform = wform
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
            if block.type_ in self.fixed:
                block.term = ''
                
    def insert_fixed(self):
        dic = wform = speech = ''
        i = 0
        while i < len(self.blocks):
            if dic != self.blocks[i].dic \
            or wform != self.blocks[i].wform \
            or speech != self.blocks[i].speech:
                ''' #NOTE: We do not inherit SEMINO here since it's not
                    needed anymore.
                '''
                block = Block()
                block.type_ = 'speech'
                block.text = self.blocks[i].speech
                block.dic = self.blocks[i].dic
                block.dicf = self.blocks[i].dicf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                block.term = self.blocks[i].term
                block.same = 0
                self.blocks.insert(i,block)
                
                block = Block()
                block.type_ = 'transc'
                block.text = self.blocks[i].transc
                block.dic = self.blocks[i].dic
                block.dicf = self.blocks[i].dicf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                block.term = self.blocks[i].term
                block.same = 0
                self.blocks.insert(i,block)

                block = Block()
                block.type_ = 'wform'
                block.text = self.blocks[i].wform
                block.dic = self.blocks[i].dic
                block.dicf = self.blocks[i].dicf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                block.term = self.blocks[i].term
                block.same = 0
                self.blocks.insert(i,block)
                
                if self.blocks[i].dic != self.phdic:
                    block = Block()
                    block.type_ = 'dic'
                    block.text = self.blocks[i].dic
                    block.dic = self.blocks[i].dic
                    block.dicf = self.blocks[i].dicf
                    block.wform = self.blocks[i].wform
                    block.speech = self.blocks[i].speech
                    block.transc = self.blocks[i].transc
                    block.term = self.blocks[i].term
                    block.same = 0
                    self.blocks.insert(i,block)
                
                dic = self.blocks[i].dic
                wform = self.blocks[i].wform
                speech = self.blocks[i].speech
                i += 4
            i += 1
            
    def remove_fixed(self):
        self.blocks = [block for block in self.blocks \
                       if block.type_ not in self.fixed
                      ]
                       
    def set_selectables(self):
        # block.no is set only after creating DB
        for block in self.blocks:
            if block.type_ in ('term','phrase','transc','phdic') \
            and block.text:
                block.select = 1
            else:
                block.select = 0
    
    def set_dic_urls(self):
        for block in self.blocks:
            if block.type_ in ('dic','phdic') \
            and not block.text in self.dicurls:
                self.dicurls[block.text] = block.url
    
    def restore_dic_urls(self):
        for i in range(len(self.blocks)):
            if self.blocks[i].type_ in ('dic','phdic') \
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
