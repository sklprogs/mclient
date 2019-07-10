#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import shared    as sh
import sharedGUI as sg

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')



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
tag_pattern_del = ['m.exe?a=40&'              # Log in, Вход
                  ,'m.exe?a=44'               # Купить
                  ,'m.exe?a=45'               # Отзывы
                  ,'m.exe?a=5&s=s_contacts'   # Contacts, Контакты
                  ,'m.exe?a=5&s=DownloadFile' # Скачать
                  ,'m.exe?a=256'              # English, Русский
                  ,'m.exe?a=1&'               # Dictionary, Словари
                  ,'&fl=1'                    # ⇄
                  ,'a href="#phrases'         # phrases, фразы
                  ,'?fscreen=1'               # Full screen, Полный экран
                  ,'td class="phras_cnt"'     # Phrase entries count number
                  ]

useful_tags = [pdic ,purl1,purl2,pcom1
              ,pcom2,pwf1 ,pwf2 ,psp
              ,ptm1 ,ptm2 ,pph  ,pcor1
              ,pcor2
              ]


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
        ''' Tag extraction algorithm is different in comparison with
            the one of 'plugins.multitranru' (in particular, see
            'Tags.blocks'). We need either to fill default SAME values
            after tag extraction or to set the initial SAME value to 0.
        '''
        self._same     = 0
        ''' '_select' is an attribute of a *cell* which is valid
            if the cell has a non-blocked block of types 'term',
            'phrase' or 'transc'.
        '''
        self._select   = -1
        ''' 'wform', 'speech', 'dic', 'phrase', 'term', 'comment',
            'transc', 'invalid'
        '''
        self._type     = ''
        self._text     = ''
        self._url      = ''
        self._urla     = ''
        self._dica     = ''
        self._dicaf    = ''
        self._wforma   = ''
        self._speecha  = ''
        self._transca  = ''
        self._terma    = ''
        self._priority = 0



class AnalyzeTag:

    def __init__(self,tag):
        self.values()
        self._tag = tag
    
    def values(self):
        self._fragms = []
        self._blocks = []

    def correction(self):
        if pcor1 in self._block._text or pcor2 in self._block._text:
            self._block._type = 'correction'
    
    def run(self):
        self.split()
        self._fragms = [fragm.strip() for fragm in self._fragms \
                        if fragm.strip()
                       ]
        for fragm in self._fragms:
            self._blocks.append(Block())
            self._blocks[-1]._text = fragm
        for self._block in self._blocks:
            if self._block._text.startswith('<'):
                if self.useful() and not self.useless():
                    self.phrases()
                    if not self._block._type:
                        self.wform()
                    if not self._block._type:
                        self.dic()
                    if not self._block._type:
                        self.term()
                    if not self._block._type:
                        self.speech()
                    if not self._block._type:
                        self.comment()
                    if not self._block._type:
                        self.correction()
                    self.url()
                else:
                    self._block._type = 'invalid'
        self.set_types()
        return self._blocks

    def set_types(self):
        self._blocks = [self.strip() for self._block in self._blocks]
        prev_url  = ''
        prev_type = 'comment'
        for block in self._blocks:
            if block._url:
                prev_url = block._url
            else:
                block._url = prev_url
            if block._type:
                prev_type = block._type
            else:
                block._type = prev_type
        self._blocks = [block for block in self._blocks 
                        if block._text and block._type != 'invalid'
                       ]
        for block in self._blocks:
            if block._type == 'comment' and block._url:
                block._type = 'term'
    
    def useless(self):
        for tag in tag_pattern_del:
            if tag in self._block._text:
                return True

    def useful(self):
        for tag in useful_tags:
            if tag in self._block._text:
                return True

    def strip(self):
        self._block._text = re.sub('<.*>','',self._block._text)
        self._block._text = self._block._text.strip()
        return self._block
    
    def split(self):
        ''' Use custom split because we need to preserve delimeters
            (cannot distinguish tags and contents otherwise).
        '''
        tmp = ''
        for sym in self._tag:
            if sym == '>':
                tmp += sym
                self._fragms.append(tmp)
                tmp = ''
            elif sym == '<':
                if tmp:
                    self._fragms.append(tmp)
                tmp = sym
            else:
                tmp += sym
        if tmp:
            self._fragms.append(tmp)

    def comment(self):
        if pcom1 in self._block._text or pcom2 in self._block._text:
            self._block._type = 'comment'
    
    def dic(self):
        f = '[MClient] plugins.multitrancom.tags.AnalyzeTag.dic'
        if pdic in self._block._text:
            self._block._type = 'dic'

    def wform(self):
        if pwf1 in self._block._text and pwf2 in self._block._text:
            self._block._type  = 'wform'

    def phrases(self):
        if pph in self._block._text:
            self._block._type = 'phrase'

    def term(self):
        f = '[MClient] plugins.multitrancom.tags.AnalyzeTag.term'
        if ptm1 in self._block._text or ptm2 in self._block._text:
            self._block._type = 'term'

    def url(self):
        ''' Otherwise, 'self._block' will be returned when there is
            no match.
        '''
        if purl1 in self._block._text or purl2 in self._block._text:
            ind = self._block._text.find(purl3)
            if ind > 0:
                ind += len(purl1)
                self._block._url = self._block._text[ind:]
            if self._block._url.endswith(purl4):
                self._block._url = self._block._url.replace(purl4,'')
            else:
                self._block._url = ''

    def speech(self):
        if psp in self._block._text:
            self._block._type = 'speech'



class Tags:

    def __init__ (self,text,Debug=False
                 ,Shorten=True,MaxRow=20
                 ,MaxRows=50
                 ):
        self.values()
        if text:
            self._text = list(text)
        self.Debug   = Debug
        self.Shorten = Shorten
        self.MaxRow  = MaxRow
        self.MaxRows = MaxRows

    def values(self):
        self._tags   = []
        self._blocks = []
        self._text   = ''
    
    def tags(self):
        ''' Split the text by closing tags. To speed up, we remove
            closing tags right away.
        '''
        if not self._tags:
            Ignore = False
            tmp = ''
            for i in range(len(self._text)):
                if self._text[i] == '<':
                    if i < len(self._text) - 1 \
                    and self._text[i+1] == '/':
                        Ignore = True
                        if tmp:
                            self._tags.append(tmp)
                            tmp = ''
                    else:
                        tmp += self._text[i]
                elif self._text[i] == '>':
                    if Ignore:
                        Ignore = False
                    else:
                        tmp += self._text[i]
                elif not Ignore:
                    tmp += self._text[i]
            # Should be needed only for broken tags
            if tmp:
                self._tags.append(tmp)
        return self._tags

    def debug_tags(self):
        f = '[MClient] plugins.multitrancom.tags.Tags.debug_tags'
        message = ''
        for i in range(len(self._tags)):
            message += '%d:%s\n' % (i,self._tags[i])
        '''
        sh.objs.mes (f,_('INFO')
                    ,message
                    )
        '''
        words = sh.Words (text = message
                         ,Auto = 1
                         )
        words.sent_nos()
        sg.objs.txt(words=words).reset_data()
        sg.objs._txt.title(f)
        sg.objs._txt.insert(text=message)
        sg.objs._txt.show()

    def debug_blocks(self):
        f = '[MClient] plugins.multitrancom.tags.Tags.debug_blocks'
        sh.log.append (f,_('INFO')
                      ,_('Debug table:')
                      )
        headers = ['TYPE'
                  ,'TEXT'
                  ,'URL'
                  ,'SAMECELL'
                  ]
        rows = []
        for block in self._blocks:
            rows.append ([block._type
                         ,block._text
                         ,block._url
                         ,block._same
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

    def blocks(self):
        if not self._blocks:
            for tag in self._tags:
                self._blocks += AnalyzeTag(tag).run()
        return self._blocks

    def run(self):
        self.tags()
        self.blocks()
        self.debug()
        return self._blocks
