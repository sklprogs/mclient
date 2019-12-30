#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import urllib.parse
import skl_shared.shared as sh
from skl_shared.localize import _

sep_words_found = 'найдены отдельные слова'


class CleanUp:
    
    def __init__(self,text):
        self._text = text
    
    def fix_tags(self):
        ''' Multitran does not escape '<' and '>' in user terms/comments
            properly. We try to fix this here.
        '''
        self._text = re.sub(' >+',r' &gt',self._text)
    
    def fix_href(self):
        ''' # Fix a malformed URL, e.g., 'href="/m.exe?a=110&l1=1&l2=2&s=process (<редк.>)&sc=671"'
            multitran.com provides for URLs that are not entirely
            correct: they still can contain spaces and unquoted symbols
            (such as 'à' or 'ф'). Browsers deal with this correctly but
            we must perform this additional step of quoting. Some
            symbols like '=', however, should not be quoted.
        '''
        f = '[MClient] plugins.multitrancom.cleanup.CleanUp.fix_href'
        if self._text:
            isearch = sh.Search (text   = self._text
                                ,search = 'href="'
                                )
            poses = isearch.next_loop()
            poses = poses[::-1]
            for pos in poses:
                pos += len('href="')
                isearch.reset (text   = self._text
                              ,search = '"'
                              )
                isearch.i = pos
                pos1 = isearch.next()
                if str(pos1).isdigit():
                    fragm = list(self._text[pos:pos1])
                    for i in range(len(fragm)):
                        if not fragm[i] in (':',';','/','=','&','?','%'):
                            fragm[i] = urllib.parse.quote(fragm[i])
                    fragm = ''.join(fragm)
                    self._text = self._text[0:pos] + fragm \
                                     + self._text[pos1:]
                else:
                    mes = _('Malformed HTML code!')
                    sh.objs.mes(f,mes).warning()
        else:
            sh.com.empty(f)
    
    def trash(self):
        self._text = self._text.replace ('>\xa0Terms for subject <a href'
                                        ,'><a href'
                                        )
        self._text = self._text.replace ('>\xa0Термины по тематике <a href'
                                        ,'><a href'
                                        )
        # Термины по тематике <...>, содержащие
        self._text = self._text.replace ('</a>, содержащие <strong>'
                                        ,'</a><strong>'
                                        )
        self._text = self._text.replace ('</a> containing <strong>'
                                        ,'</a><strong>'
                                        )
    
    def no_matches(self):
        if 'Не найдено<p>' in self._text:
            self._text = ''
    
    def sep_words(self):
        ''' If separate words are found instead of a phrase, prepare
            those words only.
        '''
        if sep_words_found in self._text:
            pos = sh.Search (text   = self._text
                            ,search = sep_words_found
                            ).next()
            # -1 gives False
            if str(pos).isdigit():
                pos += len(sep_words_found)
                self._text = self._text[:pos]
                self._text = self._text.replace (sep_words_found
                                                ,'<span style="color:gray">%s</span>'\
                                                % sep_words_found
                                                )
    
    def distinguish(self):
        ''' Substitute some tags to make tag analysis easier. We should
            delete '<i>' as well, otherwise, there will be no dictionary
            titles.
        '''
        self._text = self._text.replace (' class="phraselist0"><i>'
                                        ,'><td class="subj">'
                                        )
        self._text = self._text.replace (' class="phraselist1"><i>'
                                        ,'><td class="subj">'
                                        )
        self._text = self._text.replace (' class="phraselist1">'
                                        ,'><td class="trans">'
                                        )
                                        
        self._text = self._text.replace (' class="phraselist2">'
                                        ,'><td class="trans">'
                                        )
    
    def common(self):
        # Delete unicode control codes
        self._text = re.sub(r'[\x00-\x1f\x7f-\x9f]','',self._text)
        self._text = self._text.replace('\r\n','')
        self._text = self._text.replace('\n','')
        self._text = self._text.replace('\xa0',' ')
        while '  ' in self._text:
            self._text = self._text.replace('  ',' ')
        self._text = re.sub(r'\>[\s]{0,1}\<','><',self._text)
    
    def unsupported(self):
        ''' Remove characters from a range not supported by Tcl 
            (and causing a Tkinter error). Sample requests causing
            the error: Multitran, EN-RU: 'top', 'et al.'
        '''
        self._text = [char for char in self._text if ord(char) \
                      in range(65536)
                     ]
        self._text = ''.join(self._text)
    
    def run(self):
        f = '[MClient] plugins.multitrancom.cleanup.CleanUp.run'
        if self._text:
            self.fix_tags()
            self.trash()
            self.common()
            self.sep_words()
            self.no_matches()
            self.distinguish()
            self.unsupported()
            self.fix_href()
        else:
            sh.com.empty(f)
        return self._text
