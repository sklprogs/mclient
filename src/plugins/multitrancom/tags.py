#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import html
import skl_shared2.shared as sh
from skl_shared2.localize import _



''' Tag patterns:
    •  Abbreviations of dictionaries:
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
    •  Genders:
         <em>n</em>
         em
    •  Word forms + thesaurus:
         <td colspan="2" class="gray">&nbsp;(quantity) computer <em>n</em></td>
         td colspan="2" class="gray"
    •  Transcription:
         <td colspan="2" class="gray">&nbsp;computer <span style="color:gray">kəm'pju:tə</span> <em>n</em> <span style="color:gray">|</span>
         (same as word forms) ', ə and other marks
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
                  ,'m.exe?a=5&'           # Contacts, Контакты, Скачать
                  ,'m.exe?a=256'          # English, Русский
                  ,'m.exe?a=1&'           # Dictionary, Словари
                  ,'m.exe?a=2&'           # Forum, Форум
                  ,'m.exe?a=28&'          # +
                  ,'&fl=1'                # ⇄
                  ,'a href="#phrases'     # phrases, фразы
                  ,'?fscreen=1'           # Full screen, Полный экран
                  ,'td class="phras_cnt"' # Phrase entries count number
                  ]

useful_tags = [pdic ,purl1,purl2,pcom1
              ,pcom2,pwf1 ,pwf2 ,psp
              ,ptm1 ,ptm2 ,pph  ,pcor1
              ,pcor2
              ]


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
        ''' 'wform', 'speech', 'dic', 'phrase', 'term', 'comment',
            'transc', 'invalid'
        '''
        self.type_    = ''
        self.text     = ''
        self.url      = ''
        self.urla     = ''
        self.dica     = ''
        self.dicaf    = ''
        self.wforma   = ''
        self.speecha  = ''
        self.transca  = ''
        self.terma    = ''
        self.priority = 0



class AnalyzeTag:

    def __init__(self,tag):
        self.set_values()
        self.tag = tag
    
    def set_values(self):
        self.fragms = []
        self.blocks = []

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
        return self.blocks

    def set_types(self):
        self.blocks = [self.strip() for self.block in self.blocks]
        prev_url  = ''
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
        if pcom1 in self.block.text or pcom2 in self.block.text:
            self.block.type_ = 'comment'
    
    def set_dic(self):
        f = '[MClient] plugins.multitrancom.tags.AnalyzeTag.set_dic'
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
                 ,Shorten=True,MaxRow=20
                 ,MaxRows=50
                 ):
        self.set_values()
        if text:
            self.text = list(text)
        self.Debug   = Debug
        self.Shorten = Shorten
        self.MaxRow  = MaxRow
        self.MaxRows = MaxRows

    def set_values(self):
        self.tags   = []
        self.blocks = []
        self.text   = ''
    
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
        message = ''
        for i in range(len(self.tags)):
            message += '{}:{}\n'.format(i,self.tags[i])
        #sh.objs.get_mes(f,message,True).show_debug()
        words = sh.Words (text = message
                         ,Auto = 1
                         )
        words.sent_nos()
        sh.objs.get_txt().reset(words=words)
        sh.objs.txt.set_title(f)
        sh.objs.txt.insert(text=message)
        sh.objs.txt.show()

    def debug_blocks(self):
        f = '[MClient] plugins.multitrancom.tags.Tags.debug_blocks'
        mes = _('Debug table:')
        sh.objs.get_mes(f,mes,True).show_info()
        headers = ['TYPE'
                  ,'TEXT'
                  ,'URL'
                  ,'SAMECELL'
                  ]
        rows = []
        for block in self.blocks:
            rows.append ([block.type_
                         ,block.text
                         ,block.url
                         ,block.same
                         ]
                        )
        sh.Table (headers = headers
                 ,rows    = rows
                 ,Shorten = self.Shorten
                 ,MaxRow  = self.MaxRow
                 ,MaxRows = self.MaxRows
                 ).print()

    def debug(self):
        if self.Debug:
            #self.debug_tags()
            self.debug_blocks()

    def decode_entities(self):
        ''' - Needed both for MT and Stardict. Convert HTM entities
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
                self.blocks += AnalyzeTag(tag).run()
        return self.blocks

    def run(self):
        self.get_tags()
        self.get_blocks()
        self.decode_entities()
        self.debug()
        return self.blocks
