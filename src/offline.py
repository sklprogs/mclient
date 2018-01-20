#!/usr/bin/python3

import re
import html
import shared as sh
import sharedGUI as sg


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



''' Formatting example:
<a title="dicEnRu"><k>cut</k><tr>kʌt</tr> I 1. гл. 1) резать, разрезать I cut my arm. ≈ Я порезал руку. Cut the bread. ≈ Разрежьте хлеб. Syn : slash, lance, slit; slice 2) а) завершать, прекращать; кончать Cut the rap. ≈ Хватит болтать. б) жать, косить ∙ Syn : mow, prune
'''
class Stardict1:
    
    def __init__(self,text,header='~'):
        self._blocks = []
        self._tags   = []
        self.text    = text
        self.header  = header
        
    #todo: do this before anything else
    def decode(self):
        try:
            self.text = html.unescape(self.text)
        except:
            sg.Message ('Stardict1.decode'
                       ,_('ERROR')
                       ,_('Unable to convert HTML entities to UTF-8!')
                       )
    
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
        self.text = self.text.replace('*',self.header).replace('~',self.header)
    
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
        
    ''' Stripping blocks can be necessary after splitting ';'
        Allow empty blocks because wrong types can be assigned otherwise
    '''
    def strip(self):
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
            elif CurLang == 'LAT' and sym in sh.ru_alphabet:
                CurLang = 'CYR'
                if '≈' in block or '(' in block:
                    block += sym
                else:
                    self._blocks.append(block)
                    block = sym
            elif CurLang == 'CYR' and sym in sh.lat_alphabet:
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
                self._tags.append('<a title="%s"></a>' % block)
                #self._tags.append('<co>' + block + '</co>')
            elif block in dic_titles:
                self._tags.append('<a title="%s"></a>' % block)
                #self._tags.append('<co>' + block + '</co>')
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
                    if sh.Text(text=self._blocks[i]).has_cyrillic() \
                    and sh.Text(text=self._blocks[i-1]).has_latin():
                        Condition = True
                    elif sh.Text(text=self._blocks[i]).has_latin() \
                    and sh.Text(text=self._blocks[i-1]).has_cyrillic():
                        Condition = True
                if Condition:
                    self._blocks[i-1], self._blocks[i] = self._blocks[i], self._blocks[i-1]
        return self._blocks



''' Formatting example:
<a title="dicEnRu">1> порез; надрез; _Ex: I cut my arm _общ. Я порезал руку2> короткий путь3> _мат. раздел; _Ex: please refer to this cut обратитесь к этому разделу _Ex: to cut into pieces рассечь на части
'''
class Stardict2:
    
    def __init__(self,text,header='~'):
        self._blocks = []
        self._tags   = []
        self.text    = text
        self.header  = header
        
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
            elif CurLang == 'LAT' and self.text[i] in sh.ru_alphabet:
                CurLang = 'CYR'
                if i > 0 and self.text[i-1] == '_':
                    block += self.text[i]
                else:
                    if '≈' in block:
                        block += self.text[i]
                    else:
                        self._blocks.append(block)
                        block = self.text[i]
            elif CurLang == 'CYR' and self.text[i] in sh.lat_alphabet:
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
    
    #todo: are there are other types of headers?
    def restore_header(self):
        self.text = self.text.replace('~',self.header)
    
    #todo: do this before anything else
    def decode(self):
        try:
            self.text = html.unescape(self.text)
        except:
            sg.Message ('Stardict2.decode'
                       ,_('ERROR')
                       ,_('Unable to convert HTML entities to UTF-8!')
                       )
    
    def trash(self):
        self.text = self.text.replace(' - ',';')
        #todo: Can we allow decoding before extracting tags?
        self.text = self.text.replace('&gt;','')
    
    ''' Stripping blocks can be necessary after splitting ';'
        Allow empty blocks because wrong types can be assigned otherwise
    '''
    def strip(self):
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
                ''' #todo: create 'dic_abbr' for Stardict2 in order to
                    expand dictionary abbreviations later.
                '''
            elif self.dic(block):
                block = block.replace('_','',1)
                self._tags.append('<a title="%s"></a>' % block)
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
                    if sh.Text(text=self._blocks[i]).has_cyrillic() \
                    and sh.Text(text=self._blocks[i-1]).has_latin():
                        Condition = True
                    elif sh.Text(text=self._blocks[i]).has_latin() \
                    and sh.Text(text=self._blocks[i-1]).has_cyrillic():
                        Condition = True
                if Condition:
                    self._blocks[i-1], self._blocks[i] = self._blocks[i], self._blocks[i-1]
        return self._blocks



''' Formatting example:
<a title="dicRuEn"><k>цель</k><b>I</b><dtrn>aim</dtrn><b>II</b><c><co>при стрельбе</co></c><dtrn>target</dtrn>
'''
class Stardict3:
    
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



#todo: combine shared operations for all Stardict classes
def stardict(text,header='~'):
    if '<dtrn>' in text:
        sh.log.append ('stardict'
                      ,_('DEBUG')
                      ,_('Type 3')
                      )
        return Stardict3(text=text).run()
    elif '_Ex:' in text or re.match('\d\>',text):
        sh.log.append ('stardict'
                      ,_('DEBUG')
                      ,_('Type 2')
                      )
        return Stardict2(text=text,header=header).run()
    else:
        sh.log.append ('stardict'
                      ,_('DEBUG')
                      ,_('Type 1')
                      )
        return Stardict1(text=text,header=header).run()
    


if __name__ == '__main__':
    sg.objs.start()
    
    #text = sh.ReadTextFile(file='/home/pete/tmp/ars/sdict_EnRu_full - cut (fragm).txt').get()
    #text = sh.ReadTextFile(file='/home/pete/tmp/ars/sdict_EnRu_full - cut.txt').get()
    
    text = '''<a title="dicEnRu">1> порез; надрез; _Ex: I cut my arm _общ. Я порезал руку2> короткий путь3> _мат. раздел; _Ex: please refer to this cut обратитесь к этому разделу _Ex: to cut into pieces рассечь на части
    '''
    
    timer = sh.Timer()
    timer.start()
    
    text = stardict(text=text,header='cut')
    
    timer.end()
    
    #sg.objs.txt().reset_logic(words=words1)
    sg.objs.txt().reset_data()
    sg.objs._txt.insert(text)
    sg.objs._txt.show()
    
    sg.objs.end()
