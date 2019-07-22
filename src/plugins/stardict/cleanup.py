#!/usr/bin/python3

import re
import html
import skl_shared.shared as sh

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')


#todo (?): use shared
speech_abbr = ('гл.','нареч.','прил.','сокр.','сущ.')
dic_abbr    = ('вчт.','карт.','мор.','разг.','уст.','хир.','эл.')
#todo: read from file
dic_titles  = ('(австралийское)'
              ,'(американизм)'
              ,'(военное)'
              ,'(горное)'
              ,'(железнодорожное)'
              ,'(карточное)'
              ,'(кулинарное)'
              ,'(новозеландское)'
              ,'(профессионализм)'
              ,'(разговорное)'
              ,'(сленг)'
              ,'(спортивное)'
              ,'(текстильное)'
              ,'(теннис)'
              ,'(химическое)'
              ,'(электротехника)'
              )
header = '~'



class Common:
    
    def __init__(self,text):
        self._text = text
    
    def unsupported(self):
        ''' Remove characters from a range not supported by Tcl 
            (and causing a Tkinter error). Sample requests causing
            the error: Multitran, EN-RU: 'top', 'et al.'
        '''
        self._text = [char for char in self._text if ord(char) \
                      in range(65536)
                     ]
        self._text = ''.join(self._text)
    
    def decode_entities(self):
        ''' Needed both for MT and Stardict. Convert HTML entities
            to a human readable format, e.g., '&copy;' -> '©'.
        '''
        f = '[MClient] plugins.stardict.cleanup.Common.decode_entities'
        try:
            self._text = html.unescape(self._text)
        except Exception as e:
            sh.com.failed(f,e)
    
    def trash(self):
        self._text = self._text.replace('\r\n','')
        self._text = self._text.replace('\n','')
        self._text = self._text.replace('\xa0',' ')
        while '  ' in self._text:
            self._text = self._text.replace('  ',' ')
        self._text = re.sub(r'\>[\s]{0,1}\<','\><',self._text)
    
    def run(self):
        self.decode_entities()
        self.trash()
        self.unsupported()
        return self._text



class Type1:
    ''' Formatting example:
        <dic>dicEnRu</dic><k>cut</k><tr>kʌt</tr> I 1. гл. 1) резать, разрезать I cut my arm. ≈ Я порезал руку. Cut the bread. ≈ Разрежьте хлеб. Syn : slash, lance, slit; slice 2) а) завершать, прекращать; кончать Cut the rap. ≈ Хватит болтать. б) жать, косить ∙ Syn : mow, prune
    '''
    def __init__(self,text):
        self._blocks = []
        self._tags   = []
        self.text    = text
        
    #todo: do this before anything else
    def decode(self):
        f = '[MClient] plugins.stardict.cleanup.Type1.decode'
        try:
            self.text = html.unescape(self.text)
        except Exception as e:
            sh.com.failed(f,e)
    
    def trash(self):
        self.text = self.text.replace(' ∙ ',';').replace(' - ',';')
        #todo: Can we allow decoding before extracting tags?
        self.text = self.text.replace('&gt;','')
        
    def numbering(self):
        self.text = re.sub(' \d+[\)\.]',';',self.text)
        
    def alpha_numbering(self):
        self.text = re.sub(' [а-я]\)',';',self.text)
        self.text = re.sub(' [a-z]\)',';',self.text)
        
    def roman_numbering(self):
        self.text = re.sub('> I*','>',self.text)
        self.text = self.text.replace('II','').replace('III','').replace(' IV ','').replace(' V ','')
        
    def restore_header(self):
        self.text = self.text.replace('*',header).replace('~',header)
    
    def run(self):
        self.trash()
        self.decode()
        self.restore_header()
        self.roman_numbering()
        self.numbering()
        self.alpha_numbering()
        self.split()
        self.strip()
        self.swap_dics()
        return '\n'.join(self.tags())
        
    def strip(self):
        ''' Stripping blocks can be necessary after splitting ';'
            Allow empty blocks because wrong types can be assigned
            otherwise.
        '''
        self._blocks = [block.strip() for block in self._blocks]

    def split(self):
        block   = ''
        CurLang = 'LAT'
        for sym in self.text:
            if sym == '(':
                self._blocks.append(block)
                block = sym
            elif sym == ')':
                block += sym
                self._blocks.append(block)
                block = ''
            elif sym == ';':
                if '(' in block:
                    block += sym
                elif 'Syn :' in block:
                    block += ','
                else:
                    self._blocks.append(block)
                    block = ''
            elif CurLang == 'LAT' and sym in sh.lg.ru_alphabet:
                CurLang = 'CYR'
                if '≈' in block or '(' in block:
                    block += sym
                else:
                    self._blocks.append(block)
                    block = sym
            elif CurLang == 'CYR' and sym in sh.lg.lat_alphabet:
                CurLang = 'LAT'
                if '≈' in block or '(' in block:
                    block += sym
                else:
                    self._blocks.append(block)
                    block = sym
            elif sym == '.':
                block += sym
                if block in speech_abbr or block in dic_abbr:
                    self._blocks.append(block)
                    block = ''
            # Risky
            elif sym == ',':
                if '(' in block or '≈' in block or 'Syn :' in block:
                    block += sym
                else:
                    self._blocks.append(block)
                    block = ''
            else:
                block += sym
        self._blocks = [block.strip() for block in self._blocks \
                        if block.strip()
                       ]
        self._blocks = [block.strip(',') for block in self._blocks \
                        if block.strip(',')
                       ]
        return self._blocks

    def tags(self):
        for block in self._blocks:
            if '<' in block or '>' in block:
                self._tags.append(block)
            elif block in speech_abbr:
                self._tags.append('<gr>' + block + '</gr>')
            # Risky
            elif block in dic_abbr:
                self._tags.append('<dic>' + block + '</dic>')
            elif block in dic_titles:
                self._tags.append('<dic>' + block + '</dic>')
                ''' #todo: create a 'Synonyms' dictionary, split items
                    after it and set 'term' type to them
                '''
            elif block.startswith('(') or '≈' in block or 'Syn :' \
            in block:
                #todo (?) use variables instead of hardcoding
                self._tags.append('<co>' + block + '</co>')
            else:
                self._tags.append('<dtrn>' + block + '</dtrn>')
        return self._tags

    def swap_dics(self):
        for i in range(len(self._blocks)):
            if self._blocks[i] in dic_titles:
                Condition = False
                if i > 0:
                    if sh.lg.Text(text=self._blocks[i]).has_cyrillic() \
                    and sh.lg.Text(text=self._blocks[i-1]).has_latin():
                        Condition = True
                    elif sh.lg.Text(text=self._blocks[i]).has_latin() \
                    and sh.lg.Text(text=self._blocks[i-1]).has_cyrillic():
                        Condition = True
                if Condition:
                    self._blocks[i-1], self._blocks[i] = self._blocks[i], self._blocks[i-1]
        return self._blocks



class Type2:
    ''' Formatting example:
        <dic>dicEnRu</dic>1> порез; надрез; _Ex: I cut my arm _общ. Я порезал руку2> короткий путь3> _мат. раздел; _Ex: please refer to this cut обратитесь к этому разделу _Ex: to cut into pieces рассечь на части
    '''
    def __init__(self,text):
        self._blocks = []
        self._tags   = []
        self.text    = text
        
    def split(self):
        block   = ''
        CurLang = 'LAT'
        for i in range(len(self.text)):
            if self.text[i] == '_':
                self._blocks.append(block)
                block = self.text[i]
            elif self.text[i] == ';':
                if '(' in block:
                    block += self.text[i]
                elif 'Syn :' in block:
                    block += ','
                else:
                    self._blocks.append(block)
                    block = ''
            elif CurLang == 'LAT' and self.text[i] in sh.lg.ru_alphabet:
                CurLang = 'CYR'
                if i > 0 and self.text[i-1] == '_':
                    block += self.text[i]
                else:
                    if '≈' in block:
                        block += self.text[i]
                    else:
                        self._blocks.append(block)
                        block = self.text[i]
            elif CurLang == 'CYR' and self.text[i] in sh.lg.lat_alphabet:
                CurLang = 'LAT'
                if i > 0 and self.text[i-1] == '_':
                    block += self.text[i]
                else:
                    if '≈' in block:
                        block += self.text[i]
                    else:
                        self._blocks.append(block)
                        block = self.text[i]
            elif self.text[i] == '.':
                ''' Split text only when a dictionary abbreviation is
                    met, ignore the dot otherwise (especially useful
                    when "smb.", "smb.'s", "smth.", "т.п." are met).
                '''
                block += self.text[i]
                if self.dic(block):
                    self._blocks.append(block)
                    block = ''
            else:
                block += self.text[i]
        self._blocks = [block.strip() for block in self._blocks \
                        if block.strip()
                       ]
        self._blocks = [block.strip(',') for block in self._blocks \
                        if block.strip(',')
                       ]
        return self._blocks
    
    def numbering(self):
        self.text = re.sub('\d+\> ',';',self.text)
    
    def restore_header(self):
        #todo: are there are other types of headers?
        self.text = self.text.replace('~',header)
    
    #todo: do this before anything else
    def decode(self):
        f = '[MClient] plugins.stardict.cleanup.Type2.decode'
        try:
            self.text = html.unescape(self.text)
        except Exception as e:
            sh.com.failed(f,e)
    
    def trash(self):
        self.text = self.text.replace(' - ',';')
        #todo: Can we allow decoding before extracting tags?
        self.text = self.text.replace('&gt;','')
    
    def strip(self):
        ''' Stripping blocks can be necessary after splitting ';'.
            Allow empty blocks because wrong types can be assigned
            otherwise.
        '''
        self._blocks = [block.strip() for block in self._blocks]
        for i in range(len(self._blocks)):
            if self._blocks[i].endswith(';'):
                self._blocks[i] = self._blocks[i][:-1]
    
    def run(self):
        self.trash()
        self.decode()
        self.restore_header()
        self.numbering()
        self.split()
        self.strip()
        self.tags()
        self.swap_dics()
        return '\n'.join(self.tags())
    
    def tags(self):
        for block in self._blocks:
            if '<' in block or '>' in block:
                self._tags.append(block)
                ''' #todo: create 'dic_abbr' for Type2 in order to
                    expand dictionary abbreviations later.
                '''
            elif self.dic(block):
                block = block.replace('_','',1)
                self._tags.append('<dic>' + block + '</dic>')
            elif block.startswith('_Ex:'):
                block = block.replace('_Ex:','',1)
                ''' Examples are essentially comments, but we draft
                    an original as a term because we have both 
                    an original and a translation, and 
                    the translation is parsed as a term.
                '''
                self._tags.append('<dtrn>' + block + '</dtrn>')
            elif block.startswith('_Id: '):
                block = block.replace('_Id: ','')
                self._tags.append('<dtrn>' + block + '</dtrn>')
            elif block.startswith('(') or '≈' in block or 'Syn :' \
            in block:
                #todo (?) use variables instead of hardcoding
                self._tags.append('<co>' + block + '</co>')
            else:
                self._tags.append('<dtrn>' + block + '</dtrn>')
        return self._tags

    def dic(self,string):
        if string.startswith('_') and string == string.lower():
            return True
    
    def swap_dics(self):
        for i in range(len(self._blocks)):
            if self.dic(self._blocks[i]):
                Condition = False
                if i > 0:
                    if sh.lg.Text(text=self._blocks[i]).has_cyrillic() \
                    and sh.lg.Text(text=self._blocks[i-1]).has_latin():
                        Condition = True
                    elif sh.lg.Text(text=self._blocks[i]).has_latin() \
                    and sh.lg.Text(text=self._blocks[i-1]).has_cyrillic():
                        Condition = True
                if Condition:
                    self._blocks[i-1], self._blocks[i] = self._blocks[i], self._blocks[i-1]
        return self._blocks



class Type3:
    ''' Formatting example:
        <dic>dicEnRu</dic><k>цель</k><b>I</b><dtrn>aim</dtrn><b>II</b><c><co>при стрельбе</co></c><dtrn>target</dtrn>
    '''
    def __init__(self,text):
        self.text = text
        
    def disamb(self):
        # This is done to speed up and eliminate tag disambiguation
        try:
            self.text = self.text.replace('<i>','').replace('</i>','')
        # Encoding has failed
        except TypeError:
            self.text = ''
        
    def run(self):
        self.disamb()
        return self.text



class CleanUp:
    # This class is basically needed for compliance with other code
    def __init__(self,text):
        self._text = text

    def run(self):
        #todo: combine shared operations for all Stardict classes
        f = '[MClient] plugins.stardict.cleanup.CleanUp.run'
        if self._text and header:
            self._text = Common(self._text).run()
            if '<dtrn>' in self._text:
                mes = _('Type 3')
                sh.objs.mes(f,mes,True).debug()
                self._text = Type3(self._text).run()
            elif '_Ex:' in self._text or re.search('\d\>',self._text):
                mes = _('Type 2')
                sh.objs.mes(f,mes,True).debug()
                self._text = Type2(self._text).run()
            else:
                mes = _('Type 1')
                sh.objs.mes(f,mes,True).debug()
                self._text = Type1(self._text).run()
        else:
            sh.com.empty(f)
        return self._text
