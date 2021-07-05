#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import html
from skl_shared.localize import _
import skl_shared.shared as sh


#TODO (?): use shared
speech_abbr = ('гл.','нареч.','прил.','сокр.','сущ.')
dic_abbr = ('вчт.','карт.','мор.','разг.','уст.','хир.','эл.')
#TODO: read from file
dic_titles = ('(австралийское)'
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
        self.text = text
    
    def decode_entities(self):
        ''' Needed both for MT and Stardict. Convert HTM entities
            to a human readable format, e.g., '&copy;' -> '©'.
        '''
        f = '[MClient] plugins.stardict.cleanup.Common.decode_entities'
        try:
            self.text = html.unescape(self.text)
        except Exception as e:
            sh.com.rep_failed(f,e)
    
    def delete_trash(self):
        self.text = self.text.replace('\r\n','')
        self.text = self.text.replace('\n','')
        self.text = self.text.replace('\xa0',' ')
        while '  ' in self.text:
            self.text = self.text.replace('  ',' ')
        self.text = re.sub(r'\>[\s]{0,1}\<','\><',self.text)
    
    def run(self):
        f = '[MClient] plugins.stardict.cleanup.Common.run'
        if self.text:
            self.decode_entities()
            self.delete_trash()
            self.text = sh.Text(self.text).delete_unsupported()
            return self.text
        else:
            sh.com.rep_empty(f)
            return ''



class Type1:
    ''' Formatting example:
        <dic>dicEnRu</dic><k>cut</k><tr>kʌt</tr> I 1. гл. 1) резать, разрезать I cut my arm. ≈ Я порезал руку. Cut the bread. ≈ Разрежьте хлеб. Syn : slash, lance, slit; slice 2) а) завершать, прекращать; кончать Cut the rap. ≈ Хватит болтать. б) жать, косить ∙ Syn : mow, prune
    '''
    def __init__(self,text):
        self.blocks = []
        self.tags = []
        self.text = text
        
    #TODO: do this before anything else
    def decode(self):
        f = '[MClient] plugins.stardict.cleanup.Type1.decode'
        try:
            self.text = html.unescape(self.text)
        except Exception as e:
            sh.com.rep_failed(f,e)
    
    def delete_trash(self):
        self.text = self.text.replace(' ∙ ',';').replace(' - ',';')
        #TODO: Can we allow decoding before extracting tags?
        self.text = self.text.replace('&gt;','')
        
    def delete_numbering(self):
        self.text = re.sub(' \d+[\)\.]',';',self.text)
        
    def delete_alpha_numbering(self):
        self.text = re.sub(' [а-я]\)',';',self.text)
        self.text = re.sub(' [a-z]\)',';',self.text)
        
    def delete_roman_numbering(self):
        self.text = re.sub('> I*','>',self.text)
        self.text = self.text.replace('II','').replace('III','').replace(' IV ','').replace(' V ','')
        
    def restore_header(self):
        self.text = self.text.replace('*',header).replace('~',header)
    
    def run(self):
        self.delete_trash()
        self.decode()
        self.restore_header()
        self.delete_roman_numbering()
        self.delete_numbering()
        self.delete_alpha_numbering()
        self.split()
        self.strip()
        self.swap_dics()
        return '\n'.join(self.get_tags())
        
    def strip(self):
        ''' Stripping blocks can be necessary after splitting ';'
            Allow empty blocks because wrong types can be assigned
            otherwise.
        '''
        self.blocks = [block.strip() for block in self.blocks]

    def split(self):
        block = ''
        CurLang = 'LAT'
        for sym in self.text:
            if sym == '(':
                self.blocks.append(block)
                block = sym
            elif sym == ')':
                block += sym
                self.blocks.append(block)
                block = ''
            elif sym == ';':
                if '(' in block:
                    block += sym
                elif 'Syn :' in block:
                    block += ','
                else:
                    self.blocks.append(block)
                    block = ''
            elif CurLang == 'LAT' and sym in sh.lg.ru_alphabet:
                CurLang = 'CYR'
                if '≈' in block or '(' in block:
                    block += sym
                else:
                    self.blocks.append(block)
                    block = sym
            elif CurLang == 'CYR' and sym in sh.lg.lat_alphabet:
                CurLang = 'LAT'
                if '≈' in block or '(' in block:
                    block += sym
                else:
                    self.blocks.append(block)
                    block = sym
            elif sym == '.':
                block += sym
                if block in speech_abbr or block in dic_abbr:
                    self.blocks.append(block)
                    block = ''
            # Risky
            elif sym == ',':
                if '(' in block or '≈' in block or 'Syn :' in block:
                    block += sym
                else:
                    self.blocks.append(block)
                    block = ''
            else:
                block += sym
        self.blocks = [block.strip() for block in self.blocks \
                        if block.strip()
                       ]
        self.blocks = [block.strip(',') for block in self.blocks \
                        if block.strip(',')
                       ]
        return self.blocks

    def get_tags(self):
        for block in self.blocks:
            if '<' in block or '>' in block:
                self.tags.append(block)
            elif block in speech_abbr:
                self.tags.append('<gr>' + block + '</gr>')
            # Risky
            elif block in dic_abbr:
                self.tags.append('<dic>' + block + '</dic>')
            elif block in dic_titles:
                self.tags.append('<dic>' + block + '</dic>')
                ''' #TODO: create a 'Synonyms' dictionary, split items
                    after it and set 'term' type to them
                '''
            elif block.startswith('(') or '≈' in block or 'Syn :' \
            in block:
                #TODO: (?) use variables instead of hardcoding
                self.tags.append('<co>' + block + '</co>')
            else:
                self.tags.append('<dtrn>' + block + '</dtrn>')
        return self.tags

    def swap_dics(self):
        for i in range(len(self.blocks)):
            if self.blocks[i] in dic_titles:
                Condition = False
                if i > 0:
                    if sh.Text(text=self.blocks[i]).has_cyrillic() \
                    and sh.Text(text=self.blocks[i-1]).has_latin():
                        Condition = True
                    elif sh.Text(text=self.blocks[i]).has_latin() \
                    and sh.Text(text=self.blocks[i-1]).has_cyrillic():
                        Condition = True
                if Condition:
                    self.blocks[i-1], self.blocks[i] = self.blocks[i], self.blocks[i-1]
        return self.blocks



class Type2:
    ''' Formatting example:
        <dic>dicEnRu</dic>1> порез; надрез; _Ex: I cut my arm _общ. Я порезал руку2> короткий путь3> _мат. раздел; _Ex: please refer to this cut обратитесь к этому разделу _Ex: to cut into pieces рассечь на части
    '''
    def __init__(self,text):
        self.blocks = []
        self.tags = []
        self.text = text
        
    def split(self):
        block = ''
        CurLang = 'LAT'
        for i in range(len(self.text)):
            if self.text[i] == '_':
                self.blocks.append(block)
                block = self.text[i]
            elif self.text[i] == ';':
                if '(' in block:
                    block += self.text[i]
                elif 'Syn :' in block:
                    block += ','
                else:
                    self.blocks.append(block)
                    block = ''
            elif CurLang == 'LAT' and self.text[i] in sh.lg.ru_alphabet:
                CurLang = 'CYR'
                if i > 0 and self.text[i-1] == '_':
                    block += self.text[i]
                else:
                    if '≈' in block:
                        block += self.text[i]
                    else:
                        self.blocks.append(block)
                        block = self.text[i]
            elif CurLang == 'CYR' and self.text[i] in sh.lg.lat_alphabet:
                CurLang = 'LAT'
                if i > 0 and self.text[i-1] == '_':
                    block += self.text[i]
                else:
                    if '≈' in block:
                        block += self.text[i]
                    else:
                        self.blocks.append(block)
                        block = self.text[i]
            elif self.text[i] == '.':
                ''' Split text only when a short dictionary title is
                    met, ignore the dot otherwise (especially useful
                    when "smb.", "smb.'s", "smth.", "т.п." are met).
                '''
                block += self.text[i]
                if self.is_dic(block):
                    self.blocks.append(block)
                    block = ''
            else:
                block += self.text[i]
        self.blocks = [block.strip() for block in self.blocks \
                       if block.strip()
                      ]
        self.blocks = [block.strip(',') for block in self.blocks \
                       if block.strip(',')
                      ]
        return self.blocks
    
    def delete_numbering(self):
        self.text = re.sub('\d+\> ',';',self.text)
    
    def restore_header(self):
        #TODO: are there are other types of headers?
        self.text = self.text.replace('~',header)
    
    #TODO: do this before anything else
    def decode(self):
        f = '[MClient] plugins.stardict.cleanup.Type2.decode'
        try:
            self.text = html.unescape(self.text)
        except Exception as e:
            sh.com.rep_failed(f,e)
    
    def delete_trash(self):
        self.text = self.text.replace(' - ',';')
        #TODO: Can we allow decoding before extracting tags?
        self.text = self.text.replace('&gt;','')
    
    def strip(self):
        ''' Stripping blocks can be necessary after splitting ';'.
            Allow empty blocks because wrong types can be assigned
            otherwise.
        '''
        self.blocks = [block.strip() for block in self.blocks]
        for i in range(len(self.blocks)):
            if self.blocks[i].endswith(';'):
                self.blocks[i] = self.blocks[i][:-1]
    
    def run(self):
        self.delete_trash()
        self.decode()
        self.restore_header()
        self.delete_numbering()
        self.split()
        self.strip()
        self.get_tags()
        self.swap_dics()
        return '\n'.join(self.tags)
    
    def get_tags(self):
        for block in self.blocks:
            if '<' in block or '>' in block:
                self.tags.append(block)
                ''' #TODO: create 'dic_abbr' for Type2 in order to
                    expand short dictionary titles later.
                '''
            elif self.is_dic(block):
                block = block.replace('_','',1)
                self.tags.append('<dic>' + block + '</dic>')
            elif block.startswith('_Ex:'):
                block = block.replace('_Ex:','',1)
                ''' Examples are essentially comments, but we draft
                    an original as a term because we have both 
                    an original and a translation, and 
                    the translation is parsed as a term.
                '''
                self.tags.append('<dtrn>' + block + '</dtrn>')
            elif block.startswith('_Id: '):
                block = block.replace('_Id: ','')
                self.tags.append('<dtrn>' + block + '</dtrn>')
            elif block.startswith('(') or '≈' in block or 'Syn :' \
            in block:
                #TODO: (?) use variables instead of hardcoding
                self.tags.append('<co>' + block + '</co>')
            else:
                self.tags.append('<dtrn>' + block + '</dtrn>')
        return self.tags

    def is_dic(self,string):
        if string.startswith('_') and string == string.lower():
            return True
    
    def swap_dics(self):
        for i in range(len(self.blocks)):
            if self.is_dic(self.blocks[i]):
                Condition = False
                if i > 0:
                    if sh.Text(text=self.blocks[i]).has_cyrillic() \
                    and sh.Text(text=self.blocks[i-1]).has_latin():
                        Condition = True
                    elif sh.Text(text=self.blocks[i]).has_latin() \
                    and sh.Text(text=self.blocks[i-1]).has_cyrillic():
                        Condition = True
                if Condition:
                    self.blocks[i-1], self.blocks[i] = self.blocks[i], self.blocks[i-1]
        return self.blocks



class Type3:
    ''' Formatting example:
        <dic>dicEnRu</dic><k>цель</k><b>I</b><dtrn>aim</dtrn><b>II</b><c><co>при стрельбе</co></c><dtrn>target</dtrn>
    '''
    def __init__(self,text):
        self.text = text
        
    def delete_disamb(self):
        # This is done to speed up and eliminate tag disambiguation
        try:
            self.text = self.text.replace('<i>','').replace('</i>','')
        # Encoding has failed
        except TypeError:
            self.text = ''
        
    def run(self):
        self.delete_disamb()
        return self.text



class CleanUp:
    # This class is basically needed for compliance with other code
    def __init__(self,text):
        self.text = text
        if self.text is None:
            self.text = ''

    def run(self):
        #TODO: combine shared operations for all Stardict classes
        f = '[MClient] plugins.stardict.cleanup.CleanUp.run'
        if self.text and header:
            self.text = Common(self.text).run()
            if '<dtrn>' in self.text:
                mes = _('Type 3')
                sh.objs.get_mes(f,mes,True).show_debug()
                self.text = Type3(self.text).run()
            elif '_Ex:' in self.text or re.search('\d\>',self.text):
                mes = _('Type 2')
                sh.objs.get_mes(f,mes,True).show_debug()
                self.text = Type2(self.text).run()
            else:
                mes = _('Type 1')
                sh.objs.get_mes(f,mes,True).show_debug()
                self.text = Type1(self.text).run()
        else:
            sh.com.rep_empty(f)
        return self.text
