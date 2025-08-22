#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import html

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.table import Table
from skl_shared.logic import lat_alphabet_low

from instance import Tag, Block

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
    •  Word forms:
         <a name="verb"></a>
         <a href="/m.exe?a=118&amp;s=inundate&amp;l1=1&amp;l2=2&amp;init=1">inundate</a>
    •  Thesaurus:
         <td colspan="2">&nbsp;<b>Английский тезаурус</b></td>
         <td colspan="2">&nbsp;<b>Русский тезаурус</b></td>
    •  Transcription:
         <span style="color:gray">['ɪnəndeɪt]</span>
    •  Full subj titles:
         ' title="Религия, Латынь">рел., лат.</a></td>'
    •  Phrase section subject:
         <td class="grayline"><a name="phrases"></a>local component: <a href="/m.exe?a=3&amp;l1=1&amp;l2=2&amp;s=local+component">5 фраз</a> в 3 тематиках</td>
         td class="grayline"
    •  Phrase section terms (25 is the number of entries under the subject)
         <td class="phras"><a href="/m.exe?a=3&amp;sc=448&amp;s=computer&amp;l1=1&amp;l2=2">Chemical weapons</a></td><td class="phras_cnt">25</td>
         td class="phras"
    '''


class AnalyzeTag:

    def __init__(self, fragm):
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
            rep.empty(f)
    
    def _set_subjf(self):
        pattern = ' title="'
        ''' #NOTE: A subject can have 'UserName' in its URL since some user
            entries were separated into subjects.
        '''
        if self.tag.url and pattern in self.tag.text:
            pos1 = self.tag.text.index(pattern) + len(pattern)
            pos2 = self.tag.text.rfind('">')
            self.tag.subjf = self.tag.text[pos1:pos2]
    
    def _set_name(self):
        # Do this before setting a URL
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
            Message(f, mes).show_warning()
        if self.tag.text.endswith('>'):
            self.tag.text = self.tag.text[:-1]
        else:
            mes = _('Pattern "{}" is not a tag!').format(self.tag.text)
            Message(f, mes).show_warning()

    def _is_tag(self):
        if self.fragm.startswith('<') and self.fragm.endswith('>'):
            return True
    
    def _is_term(self):
        return 'class="trans"' in self.tag.text \
        or 'class="trans1"' in self.tag.text \
        or 'class="trans2"' in self.tag.text \
        or 'class="termsforsubject"' in self.tag.text \
        or 'class="phraselist1"' in self.tag.text \
        or 'class="phraselist2"' in self.tag.text
    
    def _is_subj(self):
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
        return 'a name="verb"' in self.tag.text \
               or 'a name="noun"' in self.tag.text \
               or 'a name="adjective"' in self.tag.text \
               or 'a name="adverb"' in self.tag.text \
               or 'a name="abbreviation"' in self.tag.text \
               or 'a name="preposition"' in self.tag.text \
               or 'a name="interjection"' in self.tag.text \
               or 'a name="pronoun"' in self.tag.text \
               or 'a name="word form"' in self.tag.text \
               or 'a name="automatically"' in self.tag.text \
               or 'a name=""' in self.tag.text \
               or 'a name="numeral"' in self.tag.text \
               or 'a name="ordinal number"' in self.tag.text \
               or self.tag.name == 'h1'
    
    def _is_speech(self):
        return self.tag.text == 'em'
    
    def _is_phrase_subj(self):
        return 'td class="grayline"' in self.tag.text
    
    def _is_phrase(self):
        # Terms in the 'Phrases' section
        return 'class="phras"' in self.tag.text
    
    def _is_phcount(self):
        return 'class="phras_cnt"' in self.tag.text
    
    def _is_trash(self):
        return 'div class="offset1"' in self.tag.text \
        or 'div class="middle_mobile"' in self.tag.text \
        or 'div style="float:left"' in self.tag.text \
        or 'div style="padding-top:0px; padding-bottom:0px;"' in self.tag.text\
        or self.tag.name in ('script', 'title', 'audio')
    
    def _set_type(self):
        if self._is_term():
            self.tag.type = 'term'
        elif self._is_comment():
            self.tag.type = 'comment'
        elif self._is_subj():
            self.tag.type = 'subj'
        elif self._is_wform():
            self.tag.type = 'wform'
        elif self._is_correction():
            self.tag.type = 'correction'
        elif self._is_phrase():
            self.tag.type = 'phrase'
        elif self._is_user():
            # 'user' type should have a priority over 'url'
            self.tag.type = 'user'
        elif self._is_url():
            self.tag.type = 'url'
        elif self._is_speech():
            self.tag.type = 'speech'
        elif self._is_phrase_subj():
            self.tag.type = 'phsubj'
        elif self._is_phcount():
            self.tag.type = 'phcount'
        elif self._is_trash():
            self.tag.type = 'trash'
    
    def _set_close(self):
        if self.fragm.startswith('</'):
            self.tag.Close = True
    
    def set_attr(self):
        f = '[MClient] plugins.multitrancom.tags.AnalyzeTag.set_attr'
        if not self.Success:
            rep.cancel(f)
            return
        if self._is_tag():
            self._set_close()
            self._set_text()
            self._set_name()
            self._set_type()
            self._set_url()
            self._set_subjf()
        else:
            self.tag.type = 'text'
            self.tag.text = self.fragm
    
    def run(self):
        self.check()
        self.set_attr()
        return self.tag
    
    def _set_url(self):
        if self.tag.type != 'url':
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
    
    def __init__(self, text, Debug=False, maxrows=0):
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
    
    def _is_trash(self, tag):
        for subtag in tag.inherent:
            if subtag.type == 'trash':
                return True
    
    def _close(self, name):
        i = len(self.open) - 1
        while i >= 0:
            if self.open[i].name == name:
                del self.open[i]
                return True
            i -= 1
    
    def set_inherent(self):
        f = '[MClient] plugins.multitrancom.tags.Tags.set_inherent'
        if not self.Success:
            rep.cancel(f)
            return
        for tag in self.tags:
            if tag.Close:
                self._close(tag.name)
            elif tag.type == 'text':
                tag.inherent = list(self.open)
            elif tag.type:
                self.open.append(tag)
    
    def set_nos(self):
        f = '[MClient] plugins.multitrancom.tags.Tags.set_nos'
        if not self.Success:
            rep.cancel(f)
            return
        curcell = -1
        for tag in self.tags:
            if not tag.Close:
                if tag.name in ('tr', 'td', 'br') or tag.text == '; ':
                    curcell += 1
            tag.cellno = curcell
    
    def _debug_blocks(self):
        nos = [i + 1 for i in range(len(self.blocks))]
        types = [block.type for block in self.blocks]
        texts = [f'"{block.text}"' for block in self.blocks]
        urls = [f'"{block.url}"' for block in self.blocks]
        subjs = [f'"{block.subj}"' for block in self.blocks]
        subjfs = [f'"{block.subjf}"' for block in self.blocks]
        cellnos = [block.cellno for block in self.blocks]
        iterable = [nos, types, texts, urls, subjs, subjfs, cellnos]
        headers = (_('#'), _('TYPE'), _('TEXT'), 'URL', 'SUBJ', 'SUBJF'
                  ,_('CELL #'))
        # 10'' monitor: 20 symbols per a column
        # 23'' monitor: 50 symbols per a column
        mes = Table(iterable = iterable, headers = headers, maxrow = 50
                   ,maxrows = self.maxrows).run()
        return _('Blocks:') + '\n' + mes
    
    def set_blocks(self):
        f = '[MClient] plugins.multitrancom.tags.Tags.set_blocks'
        if not self.Success:
            rep.cancel(f)
            return
        tags = [tag for tag in self.tags if tag.type == 'text' \
               and not self._is_trash(tag)]
        for tag in tags:
            block = Block()
            for subtag in tag.inherent:
                if subtag.type == 'url':
                    block.url = subtag.url
                    block.subjf = subtag.subjf
                else:
                    block.type = subtag.type
            block.text = tag.text
            block.cellno = tag.cellno
            # This is because MT generates invalid links
            block.url = html.unescape(block.url)
            block.text = html.unescape(block.text)
            if block.type in ('subj', 'phsubj'):
                block.subj = block.text
            self.blocks.append(block)
    
    def assign(self):
        f = '[MClient] plugins.multitrancom.tags.Tags.assign'
        if not self.Success:
            rep.cancel(f)
            return
        for fragm in self.fragms:
            self.tags.append(AnalyzeTag(fragm).run())
    
    def _debug_code(self):
        return _('Code:') + '\n' + '"{}"'.format(self.code)
    
    def _debug_fragms(self):
        mes = []
        for i in range(len(self.fragms)):
            mes.append(f'{i+1}: "{self.fragms[i]}"')
        return _('Fragments:') + '\n' + '\n'.join(mes)
    
    def _debug_tags(self):
        nos = [i + 1 for i in range(len(self.tags))]
        closes = [f'{tag.Close}' for tag in self.tags]
        names = [f'"{tag.name}"' for tag in self.tags]
        types = [f'"{tag.type}"' for tag in self.tags]
        texts = [f'"{tag.text}"' for tag in self.tags]
        urls = [f'"{tag.url}"' for tag in self.tags]
        subjfs = [f'"{tag.subjf}"' for tag in self.tags]
        cellnos = [f'{tag.cellno}' for tag in self.tags]
        inherent = []
        for tag in self.tags:
            subtags = []
            for subtag in tag.inherent:
                subtags.append(subtag.name)
            subtags = ', '.join(subtags)
            inherent.append(subtags)
        iterable = [nos, closes, names, types, texts, urls, subjfs, inherent
                   ,cellnos]
        headers = (_('#'), _('CLOSING'), _('NAME'), _('TYPE'), _('TEXT'), 'URL'
                  ,'DICF', _('OPEN'), _('CELL'))
        # 10'' monitor: 13 symbols per a column
        # 23'' monitor: 30 symbols per a column
        mes = Table(iterable = iterable, headers = headers, maxrow = 30
                   ,maxrows = self.maxrows, CutStart = True).run()
        return _('Tags:') + '\n' + mes
    
    def debug(self):
        f = '[MClient] plugins.multitrancom.tags.Tags.debug'
        if not self.Success:
            rep.cancel(f)
            return ''
        if not self.Debug:
            rep.lazy(f)
            return ''
        '''
        mes = [self._debug_code(), self._debug_fragms(), self._debug_tags()
              ,self._debug_blocks()]
        '''
        mes = [self._debug_tags(), self._debug_blocks()]
        return '\n\n'.join(mes)
    
    def check(self):
        f = '[MClient] plugins.multitrancom.tags.Tags.check'
        if not self.code:
            # Avoid None on output
            self.code = ''
            self.Success = False
            rep.empty(f)
    
    def split(self):
        f = '[MClient] plugins.multitrancom.tags.Tags.split'
        if not self.Success:
            rep.cancel(f)
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
            rep.cancel(f)
            return
        count = 0
        mes = []
        # <!--, </
        allowed = lat_alphabet_low + '!' + '/'
        for i in range(len(self.fragms)):
            ''' We should check only symbol #1 since 'multitran.com' uses URI
                instead of URL (https://stackoverflow.com/questions/1547899/which-characters-make-a-url-invalid),
                so URL tags can actually comprise Cyrillic, but not at the very
                beginning.
            '''
            if self.fragms[i].startswith('<') and len(self.fragms[i]) > 1 \
            and not self.fragms[i][1] in allowed:
                mes.append(self.fragms[i])
                self.fragms[i] = self.fragms[i].replace('<', '')
                self.fragms[i] = self.fragms[i].replace('>', '')
                count += 1
        #mes = sorted(set(mes))
        mes = '; '.join(mes)
        Message(f, mes).show_debug()
        rep.matches(f, count)
    
    def run(self):
        self.check()
        self.split()
        self.fix_non_tags()
        self.assign()
        self.set_inherent()
        self.set_nos()
        self.set_blocks()
        return self.blocks
