#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import html

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import instance as ic


''' Tag patterns:
    •  Short subject titles:
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


class AnalyzeTag:

    def __init__(self,fragm):
        self.set_values()
        self.fragm = fragm
    
    def set_values(self):
        self.Success = True
        self.tag = ic.Tag()
        self.cur_row = 0
        self.cur_cell = 0
    
    def check(self):
        f = '[MClient] plugins.multitrancom.tags.AnalyzeTag.check'
        if not self.fragm:
            self.Success = False
            sh.com.rep_empty(f)
    
    def _set_dicf(self):
        pattern = ' title="'
        ''' #NOTE: A subject can have 'UserName' in its URL since some user
            entries were separated into subjects.
        '''
        if self.tag.url and pattern in self.tag.text:
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
        or 'class="trans1"' in self.tag.text \
        or 'class="trans2"' in self.tag.text \
        or 'class="termsforsubject"' in self.tag.text \
        or 'class="phraselist1"' in self.tag.text \
        or 'class="phraselist2"' in self.tag.text
    
    def _is_dic(self):
        # An abbreviated subject title
        return 'class="subj"' in self.tag.text \
        or 'class="phraselist0"' in self.tag.text
    
    def _is_comment(self):
        # Comment/gender
        # Can comprise both 'style' and 'STYLE'
        return 'span style="color:gray"' in self.tag.text.lower()
    
    def _is_correction(self):
        return 'span STYLE="color:rgb(60,179,113)"' in self.tag.text \
               or 'font color=DarkGoldenrod' in self.tag.text \
               or 'font color="darkgoldenrod"' in self.tag.text
    
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
        if not self.Success:
            sh.com.cancel(f)
            return
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
    
    def run(self):
        self.check()
        self.set_attr()
        return self.tag
    
    def _set_url(self):
        if self.tag.type_ != 'url':
            return
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



class Tags:
    
    def __init__(self,text,Debug=False,maxrows=0):
        self.set_values()
        self.code = text
        self.Debug = Debug
        self.maxrows = maxrows
    
    def set_values(self):
        self.Success = True
        self.blocks = []
        self.fragms = []
        self.tags = []
        self.open = []
    
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
        if not self.Success:
            sh.com.cancel(f)
            return
        for tag in self.tags:
            if tag.Close:
                self._close(tag.name)
            elif tag.type_ == 'text':
                tag.inherent = list(self.open)
            elif tag.type_:
                self.open.append(tag)
    
    def set_nos(self):
        f = '[MClient] plugins.multitrancom.tags.Tags.set_nos'
        if not self.Success:
            return
        curcell = -1
        for tag in self.tags:
            if not tag.Close:
                if tag.name in ('tr','td','br') or tag.text == '; ':
                    curcell += 1
            tag.cellno = curcell
    
    def _debug_blocks(self):
        nos = [i + 1 for i in range(len(self.blocks))]
        types = [block.type_ for block in self.blocks]
        texts = ['"{}"'.format(block.text) for block in self.blocks]
        urls = ['"{}"'.format(block.url) for block in self.blocks]
        dics = ['"{}"'.format(block.dic) for block in self.blocks]
        dicfs = ['"{}"'.format(block.dicf) for block in self.blocks]
        cellnos = [block.cellno for block in self.blocks]
        iterable = [nos,types,texts,urls,dics,dicfs,cellnos]
        headers = (_('#'),_('TYPE'),_('TEXT'),'URL','DIC','DICF',_('CELL #'))
        # 10'' monitor: 20 symbols per a column
        # 23'' monitor: 50 symbols per a column
        mes = sh.FastTable (iterable = iterable
                           ,headers = headers
                           ,maxrow = 20
                           ,maxrows = self.maxrows
                           ).run()
        return _('Blocks:') + '\n' + mes
    
    def set_blocks(self):
        f = '[MClient] plugins.multitrancom.tags.Tags.set_blocks'
        if not self.Success:
            sh.com.cancel(f)
            return
        tags = [tag for tag in self.tags if tag.type_ == 'text' \
                and not self._is_script(tag)
               ]
        for tag in tags:
            block = ic.Block()
            for subtag in tag.inherent:
                if subtag.type_ == 'url':
                    block.url = subtag.url
                    block.dicf = subtag.dicf
                else:
                    block.type_ = subtag.type_
            block.text = tag.text
            block.cellno = tag.cellno
            # This is because MT generates invalid links
            block.url = html.unescape(block.url)
            block.text = html.unescape(block.text)
            if block.type_ in ('dic','phdic'):
                block.dic = block.text
            self.blocks.append(block)
    
    def assign(self):
        f = '[MClient] plugins.multitrancom.tags.Tags.assign'
        if not self.Success:
            sh.com.cancel(f)
            return
        for fragm in self.fragms:
            self.tags.append(AnalyzeTag(fragm).run())
    
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
        cellnos = ['{}'.format(tag.cellno) for tag in self.tags]
        inherent = []
        for tag in self.tags:
            subtags = []
            for subtag in tag.inherent:
                subtags.append(subtag.name)
            subtags = ', '.join(subtags)
            inherent.append(subtags)
        iterable = [nos,closes,names,types,texts,urls,dicfs,inherent,cellnos]
        headers = (_('#'),_('CLOSING'),_('NAME'),_('TYPE'),_('TEXT'),'URL'
                  ,'DICF',_('OPEN'),_('CELL')
                  )
        # 10'' monitor: 13 symbols per a column
        # 23'' monitor: 30 symbols per a column
        mes = sh.FastTable (iterable = iterable
                           ,headers = headers
                           ,maxrow = 13
                           ,maxrows = self.maxrows
                           ).run()
        return _('Tags:') + '\n' + mes
    
    def debug(self):
        f = '[MClient] plugins.multitrancom.tags.Tags.debug'
        if not self.Success:
            sh.com.cancel(f)
            return ''
        if not self.Debug:
            sh.com.rep_lazy(f)
            return ''
        mes = [self._debug_code(),self._debug_fragms()
              ,self._debug_tags(),self._debug_blocks()
              ]
        return '\n\n'.join(mes)
    
    def check(self):
        f = '[MClient] plugins.multitrancom.tags.Tags.check'
        if not self.code:
            # Avoid None on output
            self.code = ''
            self.Success = False
            sh.com.rep_empty(f)
    
    def split(self):
        f = '[MClient] plugins.multitrancom.tags.Tags.split'
        if not self.Success:
            sh.com.cancel(f)
            return
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
    
    def fix_non_tags(self):
        ''' - Work around '<' and '>' that can be unquoted at 'multitran.com'
              and do not represent tags, e.g., EN-RU,
              'wind up' => '<переносн.>'.
            - Takes ~0.024s for 'set' (EN-RU) on AMD E-300.
        '''
        f = '[MClient] plugins.multitrancom.tags.Tags.fix_non_tags'
        if not self.Success:
            sh.com.cancel(f)
            return
        count = 0
        mes = []
        # <!--, </
        allowed = sh.lg.lat_alphabet_low + '!' + '/'
        for i in range(len(self.fragms)):
            ''' We should check only symbol #1 since 'multitran.com' uses URI
                instead of URL (https://stackoverflow.com/questions/1547899/which-characters-make-a-url-invalid),
                so URL tags can actually comprise Cyrillic, but not at the very
                beginning.
            '''
            if self.fragms[i].startswith('<') and len(self.fragms[i]) > 1 \
            and not self.fragms[i][1] in allowed:
                mes.append(self.fragms[i])
                self.fragms[i] = self.fragms[i].replace('<','')
                self.fragms[i] = self.fragms[i].replace('>','')
                count += 1
        #mes = sorted(set(mes))
        mes = '; '.join(mes)
        sh.objs.get_mes(f,mes,True).show_debug()
        sh.com.rep_matches(f,count)
    
    def run(self):
        self.check()
        self.split()
        self.fix_non_tags()
        self.assign()
        self.set_inherent()
        self.set_nos()
        self.set_blocks()
        return self.blocks
