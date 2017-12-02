#!/usr/bin/python3

import re
import html
import shared as sh
import sharedGUI as sg


# todo (?): use shared
speech_abbr = ('гл.','нареч.','прил.','сокр.','сущ.')
dic_abbr    = ('вчт.','карт.','мор.','разг.','уст.','хир.','эл.')
# todo: read from file
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



class Stardict1:
    
    def __init__(self,text,header='~'):
        self._blocks = []
        self._tags   = []
        self.text    = text
        self.header  = header
        
    # todo: do this before anything else
    def decode(self):
        try:
            self.text = html.unescape(self.text)
        except:
            sg.Message ('Prepare.decode'
                       ,_('ERROR')
                       ,_('Unable to convert HTML entities to UTF-8!')
                       )
    
    def trash(self):
        self.text = self.text.replace(' ∙ ',';').replace(' - ',';')
        # todo: Can we allow decoding before extracting tags?
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
        self.swap_dics()
        return '\n'.join(self.tags())

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
            elif sym == ',': # Risky
                if '(' in block or '≈' in block or 'Syn :' in block:
                    block += sym
                else:
                    self._blocks.append(block)
                    block = ''
            else:
                block += sym
        self._blocks = [block.strip() for block in self._blocks if block.strip()]
        self._blocks = [block.strip(',') for block in self._blocks if block.strip(',')]
        return self._blocks

    def tags(self):
        for block in self._blocks:
            # note: either do html decode before that or use specific tags
            if '<' in block or '>' in block:
                self._tags.append(block)
            elif block in speech_abbr:
                self._tags.append('<k>' + block + '</k>')
            elif block in dic_abbr: # Risky
                self._tags.append('<a title="%s"></a>' % block)
                #self._tags.append('<co>' + block + '</co>')
            elif block in dic_titles:
                self._tags.append('<a title="%s"></a>' % block)
                #self._tags.append('<co>' + block + '</co>')
            # todo: create a 'Synonyms' dictionary, split items after it and set 'term' type to them
            elif block.startswith('(') or '≈' in block or 'Syn :' in block:
                # todo (?) use variables instead of hardcoding
                self._tags.append('<co>' + block + '</co>')
            else:
                self._tags.append('<dtrn>' + block + '</dtrn>')
        return self._tags

    def swap_dics(self):
        for i in range(len(self._blocks)):
            if self._blocks[i] in dic_titles:
                Condition = False
                if i > 0:
                    if sh.Text(text=self._blocks[i]).has_cyrillic() and sh.Text(text=self._blocks[i-1]).has_latin():
                        Condition = True
                    elif sh.Text(text=self._blocks[i]).has_latin() and sh.Text(text=self._blocks[i-1]).has_cyrillic():
                        Condition = True
                if Condition:
                    self._blocks[i-1], self._blocks[i] = self._blocks[i], self._blocks[i-1]
        return self._blocks



if __name__ == '__main__':
    sg.objs.start()
    
    #text = sh.ReadTextFile(file='/home/pete/tmp/ars/sdict_EnRu_full - cut (fragm).txt').get()
    text = sh.ReadTextFile(file='/home/pete/tmp/ars/sdict_EnRu_full - cut.txt').get()
    
    timer = sh.Timer()
    timer.start()
    
    sd = Stardict1(text=text,header='cut')
    text = sd.run()
    
    timer.end()
    
    #sg.objs.txt().reset_logic(words=words1)
    sg.objs.txt().reset_data()
    sg.objs._txt.insert(text)
    sg.objs._txt.show()
    
    sg.objs.end()
