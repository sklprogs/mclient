#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import html
from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.logic import Text, ru_alphabet, lat_alphabet


#TODO (?): use shared
speech_abbr = ('гл.', 'нареч.', 'прил.', 'сокр.', 'сущ.')
dic_abbr = ('вчт.', 'карт.', 'мор.', 'разг.', 'уст.', 'хир.', 'эл.')
#TODO: read from file
dic_titles = ('(австралийское)', '(американизм)', '(военное)', '(горное)'
             ,'(железнодорожное)', '(карточное)', '(кулинарное)'
             ,'(новозеландское)', '(профессионализм)', '(разговорное)'
             ,'(сленг)', '(спортивное)', '(текстильное)', '(теннис)'
             ,'(химическое)', '(электротехника)')
header = '~'


class CleanUp:
    # This class is basically needed for compliance with other code
    def __init__(self, text):
        self.blocks = []
        self.tags = []
        self.text = text
        if self.text is None:
            self.text = ''

    def decode(self):
        ''' Needed both for MT and Stardict. Convert HTM entities to a human
            readable format, e.g., '&copy;' -> '©'.
        '''
        f = '[MClient] plugins.stardict.cleanup.Common.decode'
        try:
            self.text = html.unescape(self.text)
        except Exception as e:
            rep.failed(f, e)
    
    def delete_trash(self):
        self.text = self.text.replace('\r\n', '\n')
        # Non-breaking space
        self.text = self.text.replace('\xa0', ' ')
        while '  ' in self.text:
            self.text = self.text.replace('  ', ' ')
        self.text = re.sub(r'\>[\s]{0,1}\<', '\><', self.text)
        self.text = self.text.replace('&gt;', '').replace('&lt;', '')
        #self.text = self.text.replace(' ∙ ', ';').replace(' - ', ';')
        self.text = self.text.replace('; ', '\n')
        self.text = self.text.replace(';', '\n')
        self.text = self.text.replace('_Id: ', '')
    
    def delete_disamb(self):
        # TODO: Warn about unsupported tags while preserving their contents
        # This is done to speed up and eliminate tag disambiguation
        try:
            self.text = self.text.replace('<i>', '').replace('</i>', '')
        # Encoding has failed
        except TypeError:
            self.text = ''
    
    def delete_roman_numbering(self):
        #self.text = re.sub('> I*', '>', self.text)
        self.text = re.sub(r'[\s]{0,1}II[\s]', '\n', self.text)
        self.text = re.sub(r'[\s]{0,1}III[\s]', '\n', self.text)
        self.text = re.sub(r'[\s]{0,1}IV[\s]', '\n', self.text)
        self.text = re.sub(r'[\s]{0,1}V[\s]', '\n', self.text)
        self.text = re.sub(r'[\s]{0,1}VI[\s]', '\n', self.text)
        self.text = re.sub(r'[\s]{0,1}VII[\s]', '\n', self.text)
        self.text = re.sub(r'[\s]{0,1}VIII[\s]', '\n', self.text)
        self.text = re.sub(r'[\s]{0,1}IX[\s]', '\n', self.text)
        self.text = re.sub(r'[\s]{0,1}X[\s]', '\n', self.text)
    
    def delete_numbering(self):
        self.text = re.sub(r'[\s]{0,1}\d+[\)\.][\s]', '\n', self.text)
        #self.text = re.sub('\d+\> ', ';',self.text)
    
    def delete_alpha_numbering(self):
        self.text = re.sub(r'[\s]{0,1}[а-я]\)[\s]', '\n', self.text)
        self.text = re.sub(r'[\s]{0,1}[a-z]\)[\s]', '\n', self.text)
    
    def restore_header(self):
        self.text = self.text.replace('*', header).replace('~', header)
    
    def split_by_lang(self):
        #TODO: Add line breaks when the current language is changed
        pass
    
    def set_blocks(self):
        self.blocks = self.text.splitlines()
    
    def set_tags(self):
        #TODO (?): Assign tags in elems
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
                ''' #TODO: create a 'Synonyms' subject, split items after it
                    and set 'term' type to them.
                '''
            elif block.startswith('(') or '≈' in block or 'Syn :' in block:
                #TODO: (?) use variables instead of hardcoding
                self.tags.append('<co>' + block + '</co>')
            else:
                self.tags.append('<dtrn>' + block + '</dtrn>')
    
    def is_dic(self, string):
        if string.startswith('_') and string == string.lower():
            return True
    
    def swap_dics(self):
        for i in range(len(self.blocks)):
            if self.blocks[i] in dic_titles:
                Condition = False
                if i > 0:
                    if Text(self.blocks[i]).has_cyrillic() \
                    and Text(self.blocks[i-1]).has_latin():
                        Condition = True
                    elif Text(self.blocks[i]).has_latin() \
                    and Text(self.blocks[i-1]).has_cyrillic():
                        Condition = True
                if Condition:
                    self.blocks[i-1], self.blocks[i] = self.blocks[i], self.blocks[i-1]
        return self.blocks
    
    def run(self):
        f = '[MClient] plugins.stardict.cleanup.CleanUp.run'
        if not self.text or not header:
            rep.empty(f)
            return ''
        self.decode()
        self.delete_trash()
        self.delete_disamb()
        self.delete_roman_numbering()
        self.delete_numbering()
        self.delete_alpha_numbering()
        self.restore_header()
        self.split_by_lang()
        self.set_blocks()
        self.swap_dics()
        self.set_tags()
        return self.text
