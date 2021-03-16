#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import html

import skl_shared.shared as sh
from skl_shared.localize import _


''' Tag patterns:
    •  Short dictionary titles:
         <td class="subj" width="1"><a href="/m.exe?a=110&amp;l1=1&amp;l2=2&amp;s=computer&amp;sc=197">astronaut.</a>
         td class="subj"
         <td class="phraselist0"><i><a href="/m.exe?a=110&l1=2&l2=1&s=акушерская конъюгата">мед.</a></i></td>
         td class="phraselist0"
    •  Terms:
         <td class="trans" width="100%"><a href="/m.exe?s=компьютер&amp;l1=2&amp;l2=1"> компьютер</a>
         td class="trans"
         <td class="termsforsubject">
         td class="termsforsubject"
    •  Comments:
         <span style="color:gray">(прибора)</span>
         span style="color:gray"
    •  Users:
         (116 is for everyone)
         <a href="/m.exe?a=116&UserName=Буткова">Буткова</a>
         a href="/m.exe?a=116&UserName=
    •  Parts of speech
         <em>n</em>
         em
    •  Genders:
         <span STYLE="color:gray">n</span>
         span STYLE="color:gray"
    •  Word forms + thesaurus:
         <td colspan="2" class="gray">&nbsp;(quantity) computer <em>n</em></td>
         td colspan="2" class="gray"
    •  Transcription:
         <td colspan="2" class="gray">&nbsp;computer <span style="color:gray">kəm'pju:tə</span> <em>n</em> <span style="color:gray">|</span>
         (same as word forms) ', ə and other marks
    •  Full dic titles:
         ' title="Религия, Латынь">рел., лат.</a></td>'
    •  Phrase dics (25 is the number of entries in the dic)
         <td class="phras"><a href="/m.exe?a=3&amp;sc=448&amp;s=computer&amp;l1=1&amp;l2=2">Chemical weapons</a></td><td class="phras_cnt">25</td>
         td class="phras"
    '''


class Tag:
    
    def __init__(self):
        self.type_ = ''
        self.text = ''
        self.name = ''
        self.url = ''
        self.dicf = ''
        self.rowno = -1
        self.cellno = -1
        self.Close = False
        self.inherent = []



class AnalyzeTag:

    def __init__(self,fragm):
        self.set_values()
        self.fragm = fragm
    
    def set_values(self):
        self.Success = True
        self.tag = Tag()
        self.cur_row = 0
        self.cur_cell = 0
    
    def check(self):
        f = '[MClient] plugins.multitrancom.tags.AnalyzeTag.check'
        if not self.fragm:
            self.Success = False
            sh.com.rep_empty(f)
    
    def _set_dicf(self):
        pattern = ' title="'
        if self.tag.url and pattern in self.tag.text \
        and not 'UserName' in self.tag.text:
            pos1 = self.tag.text.index(pattern) + len(pattern)
            pos2 = self.tag.text.rfind('">')
            self.tag.dicf = self.tag.text[pos1:pos2]
    
    def _set_name(self):
        # Do this before setting a URL
        f = '[MClient] plugins.multitrancom.tags.Tags._set_name'
        self.tag.name = self.tag.text
        if self.tag.name.startswith('<'):
            self.tag.name = self.tag.name[1:]
        pos = self.tag.name.find(' ')
        if pos > -1:
            self.tag.name = self.tag.name[:pos]
        self.tag.name = self.tag.name.lower()
    
    def _set_text(self):
        f = '[MClient] plugins.multitrancom.tags.Tags._set_text'
        self.tag.text = self.fragm
        if self.tag.text.startswith('</'):
            self.tag.text = self.tag.text[2:]
        elif self.tag.text.startswith('<'):
            self.tag.text = self.tag.text[1:]
        else:
            mes = _('Pattern "{}" is not a tag!').format(self.tag.text)
            sh.objs.get_mes(f,mes,True).show_warning()
        if self.tag.text.endswith('>'):
            self.tag.text = self.tag.text[:-1]
        else:
            mes = _('Pattern "{}" is not a tag!').format(self.tag.text)
            sh.objs.get_mes(f,mes,True).show_warning()

    def _is_tag(self):
        if self.fragm.startswith('<') and self.fragm.endswith('>'):
            return True
    
    def _is_phrase(self):
        # Terms in the 'Phrases' section
        return 'class="phras"' in self.tag.text
    
    def _is_term(self):
        return 'class="trans"' in self.tag.text \
        or 'class="termsforsubject"' in self.tag.text \
        or 'class="phraselist1"' in self.tag.text \
        or 'class="phraselist2"' in self.tag.text
    
    def _is_dic(self):
        # An abbreviated dictionary title
        return 'class="subj"' in self.tag.text \
        or 'class="phraselist0"' in self.tag.text
    
    def _is_comment(self):
        # Comment/gender
        # Can comprise both 'style' and 'STYLE'
        return 'span style="color:gray"' in self.tag.text.lower()
    
    def _is_correction(self):
        return self.tag.text in ('span STYLE="color:rgb(60,179,113)"'
                                ,'font color=DarkGoldenrod'
                                )
    
    def _is_user(self):
        return 'UserName=' in self.tag.text
    
    def _is_url(self):
        return 'href="' in self.tag.text
    
    def _is_wform(self):
        # Wform/transcription
        return 'td colspan="' in self.tag.text \
        or '" class="gray"' in self.tag.text
    
    def _is_speech(self):
        return self.tag.text == 'em'
    
    def _is_phrase_dic(self):
        return 'name="phrases"' in self.tag.text
    
    def _is_phcount(self):
        return 'class="phras_cnt"' in self.tag.text
    
    def _is_script(self):
        return self.tag.name == 'script'
    
    def _set_type(self):
        if self._is_term():
            self.tag.type_ = 'term'
        elif self._is_comment():
            self.tag.type_ = 'comment'
        elif self._is_dic():
            self.tag.type_ = 'dic'
        elif self._is_wform():
            self.tag.type_ = 'wform'
        elif self._is_correction():
            self.tag.type_ = 'correction'
        elif self._is_phrase():
            self.tag.type_ = 'phrase'
        elif self._is_user():
            # 'user' type should have a priority over 'url'
            self.tag.type_ = 'user'
        elif self._is_url():
            self.tag.type_ = 'url'
        elif self._is_speech():
            self.tag.type_ = 'speech'
        elif self._is_phrase_dic():
            self.tag.type_ = 'phdic'
        elif self._is_script():
            self.tag.type_ = 'script'
        elif self._is_phcount():
            self.tag.type_ = 'phcount'
    
    def _set_close(self):
        if self.fragm.startswith('</'):
            self.tag.Close = True
    
    def set_attr(self):
        f = '[MClient] plugins.multitrancom.tags.AnalyzeTag.set_attr'
        if self.Success:
            if self._is_tag():
                self._set_close()
                self._set_text()
                self._set_name()
                self._set_type()
                self._set_url()
                self._set_dicf()
            else:
                self.tag.type_ = 'text'
                self.tag.text = self.fragm
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.check()
        self.set_attr()
        return self.tag
    
    def _set_url(self):
        if self.tag.type_ == 'url':
            self.tag.url = self.tag.text
            pattern = 'href="/m.exe?'
            # Can be either 'm.exe' or 'M.exe'
            ind = self.tag.url.lower().find(pattern)
            if ind > 0:
                ind += len(pattern)
                self.tag.url = self.tag.url[ind:]
            else:
                self.tag.url = ''
            if self.tag.url.endswith('"'):
                self.tag.url = self.tag.url[:-1]
            else:
                self.tag.url = ''



class Block:

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
        self.last = -1
        self.no = -1
        self.same = -1
        ''' 'select' is an attribute of a *cell* which is valid
            if the cell has a non-blocked block of types 'term',
            'phrase' or 'transc'.
        '''
        self.select = -1
        self.speech = ''
        self.sprior = -1
        self.transc = ''
        self.term = ''
        self.text = ''
        ''' 'comment', 'correction', 'dic', 'invalid', 'phrase',
            'speech', 'term', 'transc', 'wform'
        '''
        self.type_ = 'comment'
        self.url = ''
        self.urla = ''
        self.wform = ''



class Tags:
    
    def __init__(self,text,Debug=False,maxrows=0):
        self.set_values()
        self.code = text
        self.Debug = Debug
        self.maxrows = maxrows
    
    def set_values(self):
        self.Success = True
        self.abbr = {}
        self.blocks = []
        self.fragms = []
        self.tags = []
        self.open = []
    
    def set_abbr(self):
        f = '[MClient] plugins.multitrancom.tags.Tags.set_abbr'
        if self.Success:
            #NOTE: set 'block.dic' before this (or use 'block.text')
            blocks = [block for block in self.blocks \
                      if block.dic and block.dicf
                     ]
            for block in blocks:
                if not block.dic in self.abbr \
                and not block.dicf in self.abbr:
                    self.abbr[block.dic] = {}
                    self.abbr[block.dicf] = {}
                    self.abbr[block.dic]['abbr'] = block.dic
                    self.abbr[block.dicf]['abbr'] = block.dic
                    self.abbr[block.dic]['full'] = block.dicf
                    self.abbr[block.dicf]['full'] = block.dicf
        else:
            sh.com.cancel(f)
    
    def _debug_abbr(self):
        f = '[MClient] plugins.multitrancom.tags.Tags._debug_abbr'
        mes = ''
        if self.abbr:
            keys = []
            abbr = []
            full = []
            try:
                for key in self.abbr.keys():
                    keys.append(key)
                    abbr.append(self.abbr[key]['abbr'])
                    full.append(self.abbr[key]['full'])
            except KeyError:
                mes = _('Wrong input data!')
                sh.objs.get_mes(f,mes).show_warning()
            keys = ['"{}"'.format(key) for key in keys]
            abbr = ['"{}"'.format(item) for item in abbr]
            full = ['"{}"'.format(item) for item in full]
            nos = [i + 1 for i in range(len(keys))]
            headers = (_('#'),_('KEY'),_('ABBREVIATION')
                      ,_('FULL TITLE')
                      )
            iterable = [nos,keys,abbr,full]
            # 10'' screen: 40 symbols per a column
            mes = sh.FastTable (iterable = iterable
                               ,headers = headers
                               ,maxrow = 40
                               ).run()
        else:
            sh.com.rep_empty(f)
        return _('Abbreviations:') + '\n' + mes
    
    def _is_script(self,tag):
        for subtag in tag.inherent:
            if subtag.name == 'script':
                return True
    
    def _close(self,name):
        i = len(self.open) - 1
        while i >= 0:
            if self.open[i].name == name:
                del self.open[i]
                return True
            i -= 1
    
    def set_inherent(self):
        f = '[MClient] plugins.multitrancom.tags.Tags.set_inherent'
        if self.Success:
            for tag in self.tags:
                if tag.Close:
                    self._close(tag.name)
                elif tag.type_ == 'text':
                    tag.inherent = list(self.open)
                elif tag.type_:
                    self.open.append(tag)
        else:
            sh.com.cancel(f)
    
    def set_nos(self):
        f = '[MClient] plugins.multitrancom.tags.Tags.set_nos'
        if self.Success:
            currow = -1
            curcell = -1
            for tag in self.tags:
                if not tag.Close:
                    if tag.name in ('tr','br'):
                        currow += 1
                    elif tag.name == 'td':
                        curcell += 1
                tag.rowno = currow
                tag.cellno = curcell
            """
            ''' tag.cellno == -1 is actually OK since rows come before
                any cells.
            '''
            for tag in self.tags:
                if tag.rowno > -1:
                    tag.cellno += 1
                break
            """
    
    def _debug_blocks(self):
        nos = [i + 1 for i in range(len(self.blocks))]
        types = [block.type_ for block in self.blocks]
        texts = ['"{}"'.format(block.text) for block in self.blocks]
        urls = ['"{}"'.format(block.url) for block in self.blocks]
        dics = ['"{}"'.format(block.dic) for block in self.blocks]
        dicfs = ['"{}"'.format(block.dicf) for block in self.blocks]
        rownos = [block.rowno for block in self.blocks]
        cellnos = [block.cellno for block in self.blocks]
        iterable = [nos,types,texts,urls,dics,dicfs,rownos,cellnos]
        headers = (_('#'),_('TYPE'),_('TEXT'),'URL','DIC','DICF'
                  ,_('ROW #'),_('CELL #')
                  )
        # 10'' monitor: 20 symbols per a column
        # 23'' monitor: 50 symbols per a column
        mes = sh.FastTable (iterable = iterable
                           ,headers = headers
                           ,maxrow = 50
                           ,maxrows = self.maxrows
                           ).run()
        return _('Blocks:') + '\n' + mes
    
    def set_blocks(self):
        f = '[MClient] plugins.multitrancom.tags.Tags.set_blocks'
        if self.Success:
            tags = [tag for tag in self.tags \
                    if tag.type_ == 'text' and not self._is_script(tag)
                   ]
            for tag in tags:
                block = Block()
                for subtag in tag.inherent:
                    if subtag.type_ == 'url':
                        block.url = subtag.url
                        block.dicf = subtag.dicf
                    else:
                        block.type_ = subtag.type_
                block.text = tag.text
                block.rowno = tag.rowno
                block.cellno = tag.cellno
                # This is because MT generates invalid links
                block.url = html.unescape(block.url)
                block.text = html.unescape(block.text)
                if block.type_ in ('dic','phdic'):
                    block.dic = block.text
                self.blocks.append(block)
        else:
            sh.com.cancel(f)
    
    def assign(self):
        f = '[MClient] plugins.multitrancom.tags.Tags.assign'
        if self.Success:
            for fragm in self.fragms:
                self.tags.append(AnalyzeTag(fragm).run())
        else:
            sh.com.cancel(f)
    
    def _debug_code(self):
        return _('Code:') + '\n' + '"{}"'.format(self.code)
    
    def _debug_fragms(self):
        mes = []
        for i in range(len(self.fragms)):
            sub = '{}: "{}"'.format(i+1,self.fragms[i])
            mes.append(sub)
        return _('Fragments:') + '\n' + '\n'.join(mes)
    
    def _debug_tags(self):
        nos = [i + 1 for i in range(len(self.tags))]
        closes = ['{}'.format(tag.Close) for tag in self.tags]
        names = ['"{}"'.format(tag.name) for tag in self.tags]
        types = ['"{}"'.format(tag.type_) for tag in self.tags]
        texts = ['"{}"'.format(tag.text) for tag in self.tags]
        urls = ['"{}"'.format(tag.url) for tag in self.tags]
        dicfs = ['"{}"'.format(tag.dicf) for tag in self.tags]
        rownos = ['{}'.format(tag.rowno) for tag in self.tags]
        cellnos = ['{}'.format(tag.cellno) for tag in self.tags]
        inherent = []
        for tag in self.tags:
            subtags = []
            for subtag in tag.inherent:
                subtags.append(subtag.name)
            subtags = ', '.join(subtags)
            inherent.append(subtags)
        iterable = [nos,closes,names,types,texts,urls,dicfs,inherent
                   ,rownos,cellnos
                   ]
        headers = (_('#'),_('CLOSING'),_('NAME'),_('TYPE'),_('TEXT')
                  ,'URL','DICF',_('OPEN'),_('ROW'),_('CELL')
                  )
        # 10'' monitor: 13 symbols per a column
        # 23'' monitor: 30 symbols per a column
        mes = sh.FastTable (iterable = iterable
                           ,headers = headers
                           ,maxrow = 30
                           ,maxrows = self.maxrows
                           ).run()
        return _('Tags:') + '\n' + mes
    
    def debug(self):
        f = '[MClient] plugins.multitrancom.tags.Tags.debug'
        if self.Debug:
            if self.Success:
                mes = [self._debug_code(),self._debug_fragms()
                      ,self._debug_tags(),self._debug_blocks()
                      ,self._debug_abbr()
                      ]
                mes = '\n\n'.join(mes)
                sh.com.run_fast_debug(f,mes)
            else:
                sh.com.cancel(f)
        else:
            sh.com.rep_lazy(f)
    
    def check(self):
        f = '[MClient] plugins.multitrancom.tags.Tags.check'
        if not self.code:
            # Avoid None on output
            self.code = ''
            self.Success = False
            sh.com.rep_empty(f)
    
    def split(self):
        f = '[MClient] plugins.multitrancom.tags.Tags.split'
        if self.Success:
            fragm = ''
            for sym in list(self.code):
                if sym == '<':
                    if fragm:
                        self.fragms.append(fragm)
                    fragm = sym
                elif sym == '>':
                    fragm += sym
                    self.fragms.append(fragm)
                    fragm = ''
                else:
                    fragm += sym
            if fragm:
                self.fragms.append(fragm)
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.check()
        self.split()
        self.assign()
        self.set_nos()
        self.set_inherent()
        self.set_blocks()
        self.set_abbr()
        self.debug()
        return self.blocks
