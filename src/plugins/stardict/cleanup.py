#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import html
from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.logic import Text, ru_alphabet, lat_alphabet

header = '~'


class CleanUp:
    
    def __init__(self, text):
        if text is None:
            text = ''
        self.text = text

    def decode(self):
        ''' Needed both for MT and Stardict. Convert HTM entities to a human
            readable format, e.g., '&copy;' -> '©'.
        '''
        f = '[MClient] plugins.stardict.cleanup.CleanUp.decode'
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
        # Semicolons should not be replaced with line breaks within phrases
        #self.text = self.text.replace('; ', '\n')
        #self.text = self.text.replace(';', '\n')
        self.text = self.text.replace('∙', '\n')
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
        self.text = re.sub(r'[\s][а-я]\)[\s]', '\n', self.text)
        self.text = re.sub(r'[\s][a-z]\)[\s]', '\n', self.text)
    
    def _get_prev_lang(self, i):
        i -= 1
        while i >= 0:
            if self.text[i] in ru_alphabet:
                return 'ru'
            elif self.text[i] in lat_alphabet:
                return 'en'
            i -= 1
    
    def _get_next_lang(self, i):
        i += 1
        while i < len(self.text):
            if self.text[i] in ru_alphabet:
                return 'ru'
            elif self.text[i] in lat_alphabet:
                return 'en'
            i += 1
    
    def _is_lang_mixed(self, i):
        prev_lang = self._get_prev_lang(i)
        next_lang = self._get_next_lang(i)
        return prev_lang and next_lang and prev_lang != next_lang
    
    def separate_phrases(self):
        lang = ''
        text = ''
        SepFound = False
        Pair = False
        for char in self.text:
            if char == '\n':
                SepFound = False
                Pair = False
            elif char in ('~', '≈', '*'):
                SepFound = True
            elif char in ru_alphabet:
                if not lang:
                    lang = 'ru'
                elif lang == 'en':
                    lang = 'ru'
                    if SepFound:
                        if Pair:
                            text += '\n'
                            SepFound = False
                            Pair = False
                        else:
                            Pair = True
            elif char in lat_alphabet:
                if not lang:
                    lang = 'en'
                elif lang == 'ru':
                    lang = 'en'
                    if SepFound:
                        if Pair:
                            text += '\n'
                            SepFound = False
                            Pair = False
                        else:
                            Pair = True
            text += char
        text = text.replace('* \n', '\n* ')
        text = text.replace('*\n', '\n*')
        text = text.replace('\n\n', '\n')
        self.text = text
    
    def replace_punc(self):
        ''' It's risky to replace at once, e.g.:
            'что имеем - не храним, потерявши - плачем'.
        '''
        self.text = list(self.text)
        for i in range(len(self.text)):
            if self.text[i] in ('-', ';') and self._is_lang_mixed(i):
                self.text[i] = '\n'
        self.text = ''.join(self.text)
    
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
        self.replace_punc()
        self.separate_phrases()
        return self.text
