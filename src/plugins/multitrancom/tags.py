#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
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


# Abbreviated dictionary titles
pdic = 'td class="subj"'

# URLs
purl1 = 'href="/m.exe?'
# Failsafe
purl2 = 'href="/M.exe?'
purl3 = 'href="'
purl4 = '">'

# Comments
pcom1 = '<i>'
pcom2 = 'span style="color:gray"'
# Gender
pcom3 = 'span STYLE="color:gray"'

# Corrective comments
pcor1 = '<span STYLE="color:rgb(60,179,113)">'
pcor2 = '<font color=DarkGoldenrod>'

# Word Forms
pwf1 = 'td colspan="'
pwf2 = '" class="gray"'

# Parts of speech
psp = '<em>'

# Terms
ptm1 = 'td class="trans"'
ptm2 = 'td class="termsforsubject"'

# Terms in the 'Phrases' section
pph = 'td class="phras"'

# Tag patterns
tag_pattern_del = ['m.exe?a=40&'          # Log in, Вход
                  ,'m.exe?a=44'           # Купить
                  ,'m.exe?a=45'           # Отзывы
                  ,'m.exe?a=381'          # Скачать
                  ,'m.exe?a=382'          # Contacts, Контакты
                  ,'m.exe?a=256'          # English, Русский
                  ,'m.exe?a=1&'           # Dictionary, Словари
                  ,'m.exe?a=2&'           # Forum, Форум
                  ,'m.exe?a=28&'          # +
                  ,'&fl=1'                # ⇄
                  ,'a href="#phrases'     # phrases, фразы
                  ,'?fscreen=1'           # Full screen, Полный экран
                  ,'td class="phras_cnt"' # Phrase entries count number
                  ,'m.exe?a=365&'         # Terms of Use, Соглашение пользователя
                  ]

useful_tags = [pdic,purl1,purl2,pcom1
              ,pcom2,pwf1,pwf2,psp
              ,ptm1,ptm2,pph,pcor1
              ,pcor2,pcom3
              ]


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
        ''' Tag extraction algorithm is different in comparison with
            the one of 'plugins.multitranru' (in particular, see
            'Tags.blocks'). We need either to fill default SAME values
            after tag extraction or to set the initial SAME value to 0.
        '''
        self.same = 0
        ''' 'select' is an attribute of a *cell* which is valid
            if the cell has a non-blocked block of types 'term',
            'phrase' or 'transc'.
        '''
        self.select = -1
        self.semino = -1
        self.speech = ''
        self.sprior = -1
        self.term = ''
        self.text = ''
        ''' 'comment', 'dic', 'invalid', 'phrase', 'speech', 'term', 
            'transc', 'wform'
        '''
        self.transc = ''
        self.type_ = ''
        self.url = ''
        self.urla = ''
        self.wform = ''



class AnalyzeTag:

    def __init__(self,tag):
        self.set_values()
        self.tag = tag
    
    def set_values(self):
        self.blocks = []
        self.dicf = ''
        self.fragms = []

    def set_dicf(self):
        pattern = ' title="'
        if pattern in self.tag and not 'UserName' in self.tag:
            pos1 = self.tag.index(pattern) + len(pattern)
            pos2 = self.tag.rfind('">')
            self.dicf = self.tag[pos1:pos2]
    
    def debug(self):
        f = '[MClient] plugins.multitrancom.tags.AnalyzeTag.debug'
        mes = _('Tag: "{}"').format(self.tag)
        sh.objs.get_mes(f,mes,True).show_debug()
        nos = [i + 1 for i in range(len(self.fragms))]
        headers = ['NO','FRAGM']
        fragms = ['"{}"'.format(fragm) for fragm in self.fragms]
        iterable = [nos,fragms]
        mes = sh.FastTable(iterable,headers).run()
        types = []
        texts = []
        nos = []
        for i in range(len(self.blocks)):
            nos.append(i+1)
            types.append(self.blocks[i].type_)
            texts.append(self.blocks[i].text)
        iterable = [nos,types,texts]
        headers = ('NO','TYPE','TEXT')
        mes += '\n\n' + sh.FastTable(iterable,headers).run()
        mes += '\n' + 'DICF: "{}"'.format(self.dicf)
        sh.objs.txt = None
        sh.com.run_fast_debug(f,mes)
    
    def set_correction(self):
        if pcor1 in self.block.text or pcor2 in self.block.text:
            self.block.type_ = 'correction'
    
    def run(self):
        self.split()
        self.fragms = [fragm.strip() for fragm in self.fragms \
                       if fragm.strip()
                      ]
        for fragm in self.fragms:
            self.blocks.append(Block())
            self.blocks[-1].text = fragm
        for self.block in self.blocks:
            if self.block.text.startswith('<'):
                if self.is_useful() and not self.is_useless():
                    self.set_phrases()
                    if not self.block.type_:
                        self.set_wform()
                    if not self.block.type_:
                        self.set_dic()
                    if not self.block.type_:
                        self.set_term()
                    if not self.block.type_:
                        self.set_speech()
                    if not self.block.type_:
                        self.set_comment()
                    if not self.block.type_:
                        self.set_correction()
                    self.set_url()
                else:
                    self.block.type_ = 'invalid'
        self.set_types()
        self.set_dicf()
        return self.blocks

    def set_types(self):
        self.blocks = [self.strip() for self.block in self.blocks]
        prev_url = ''
        prev_type = 'comment'
        for block in self.blocks:
            if block.url:
                prev_url = block.url
            else:
                block.url = prev_url
            if block.type_:
                prev_type = block.type_
            else:
                block.type_ = prev_type
        self.blocks = [block for block in self.blocks 
                       if block.text and block.type_ != 'invalid'
                      ]
        for block in self.blocks:
            if block.type_ == 'comment' and block.url:
                block.type_ = 'term'
    
    def is_useless(self):
        for tag in tag_pattern_del:
            if tag in self.block.text:
                return True

    def is_useful(self):
        for tag in useful_tags:
            if tag in self.block.text:
                return True

    def strip(self):
        self.block.text = re.sub('<.*>','',self.block.text)
        self.block.text = self.block.text.strip()
        return self.block
    
    def split(self):
        ''' Use custom split because we need to preserve delimeters
            (cannot distinguish tags and contents otherwise).
        '''
        tmp = ''
        for sym in self.tag:
            if sym == '>':
                tmp += sym
                self.fragms.append(tmp)
                tmp = ''
            elif sym == '<':
                if tmp:
                    self.fragms.append(tmp)
                tmp = sym
            else:
                tmp += sym
        if tmp:
            self.fragms.append(tmp)

    def set_comment(self):
        if pcom1 in self.block.text or pcom2 in self.block.text \
        or pcom3 in self.block.text:
            self.block.type_ = 'comment'
    
    def set_dic(self):
        if pdic in self.block.text:
            self.block.type_ = 'dic'

    def set_wform(self):
        if pwf1 in self.block.text and pwf2 in self.block.text:
            self.block.type_ = 'wform'

    def set_phrases(self):
        if pph in self.block.text:
            self.block.type_ = 'phrase'

    def set_term(self):
        f = '[MClient] plugins.multitrancom.tags.AnalyzeTag.term'
        if ptm1 in self.block.text or ptm2 in self.block.text:
            self.block.type_ = 'term'

    def set_url(self):
        ''' Otherwise, 'self.block' will be returned when there is
            no match.
        '''
        if purl1 in self.block.text or purl2 in self.block.text:
            ind = self.block.text.find(purl3)
            if ind > 0:
                ind += len(purl1)
                self.block.url = self.block.text[ind:]
            if self.block.url.endswith(purl4):
                self.block.url = self.block.url.replace(purl4,'')
            else:
                self.block.url = ''

    def set_speech(self):
        if psp in self.block.text:
            self.block.type_ = 'speech'



class Tags:

    def __init__ (self,text,Debug=False
                 ,maxrow=50,maxrows=1000
                 ):
        self.set_values()
        if text:
            self.text = list(text)
        self.Debug = Debug
        self.maxrow = maxrow
        self.maxrows = maxrows

    def set_values(self):
        self.abbr = {}
        self.blocks = []
        self.tags = []
        self.text = ''
    
    def debug_abbr(self):
        f = '[MClient] plugins.multitrancom.tags.Tags.debug_abbr'
        if self.abbr:
            keys = []
            values = []
            for key in self.abbr.keys():
                keys.append(key)
                values.append(self.abbr[key])
            nos = [i + 1 for i in range(len(keys))]
            headers = ('NO','ABBR','FULL')
            iterable = [nos,keys,values]
            mes = sh.FastTable(iterable,headers).run()
            sh.com.run_fast_debug(f,mes)
        else:
            sh.com.rep_empty(f)
    
    def get_tags(self):
        ''' Split the text by closing tags. To speed up, we remove
            closing tags right away.
        '''
        if not self.tags:
            Ignore = False
            tmp = ''
            for i in range(len(self.text)):
                if self.text[i] == '<':
                    if i < len(self.text) - 1 \
                    and self.text[i+1] == '/':
                        Ignore = True
                        if tmp:
                            self.tags.append(tmp)
                            tmp = ''
                    else:
                        tmp += self.text[i]
                elif self.text[i] == '>':
                    if Ignore:
                        Ignore = False
                    else:
                        tmp += self.text[i]
                elif not Ignore:
                    tmp += self.text[i]
            # Should be needed only for broken tags
            if tmp:
                self.tags.append(tmp)
        return self.tags

    def debug_tags(self):
        f = '[MClient] plugins.multitrancom.tags.Tags.debug_tags'
        messages = []
        for i in range(len(self.tags)):
            mes = "{}:'{}'".format(i,self.tags[i])
            messages.append(mes)
        mes = '\n'.join(messages)
        #sh.objs.get_mes(f,message,True).show_debug()
        sh.objs.get_txt().reset (title = f
                                ,text = mes
                                )
        sh.objs.txt.show()

    def debug_blocks(self):
        f = '[MClient] plugins.multitrancom.tags.Tags.debug_blocks'
        headers = ('NO','TYPE','TEXT','URL','SAME')
        rows = []
        for i in range(len(self.blocks)):
            rows.append ([i + 1
                         ,self.blocks[i].type_
                         ,self.blocks[i].text
                         ,self.blocks[i].url
                         ,self.blocks[i].same
                         ]
                        )
        mes = sh.FastTable (headers = headers
                           ,iterable = rows
                           ,maxrow = self.maxrow
                           ,maxrows = self.maxrows
                           ,Transpose = True
                           ).run()
        sh.objs.txt = None
        sh.com.run_fast_debug(f,mes)

    def debug(self):
        if self.Debug:
            self.debug_tags()
            self.debug_blocks()
            self.debug_abbr()

    def decode_entities(self):
        ''' - Needed both for MT and Stardict. Convert HTML entities
              to a human readable format, e.g., '&copy;' -> '©'.
            - We should decode entities only after extracting tags since
              user terms/comments in Multitran often contain such
              symbols as '<' or '>'.
              #NOTE: currently this does not help since Multitran
              does not escape '<' and '>' in user terms/comments
              properly!
        '''
        f = '[MClient] plugins.multitrancom.tags.Tags.decode_entities'
        try:
            for block in self.blocks:
                block.text = html.unescape(block.text)
                ''' This is done since we do not unescape
                    the entire text any more.
                '''
                block.url = block.url.replace('&amp;','&')
        except Exception as e:
            sh.com.rep_failed(f,e)
    
    def get_blocks(self):
        if not self.blocks:
            for tag in self.tags:
                itag = AnalyzeTag(tag)
                self.blocks += itag.run()
                if itag.dicf:
                    dics = [block.text for block in itag.blocks \
                            if block.type_ == 'dic'
                           ]
                    if dics:
                        self.abbr[dics[0]] = itag.dicf
        return self.blocks

    def run(self):
        self.get_tags()
        self.get_blocks()
        self.decode_entities()
        self.debug()
        return self.blocks
