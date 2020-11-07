#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import urllib.parse
import skl_shared.shared as sh
from skl_shared.localize import _

sep_words_found = 'найдены отдельные слова'


class CleanUp:
    
    def __init__(self,text):
        self.text = text
    
    def fix_tags(self):
        ''' Multitran does not escape '<' and '>' in user terms/comments
            properly. We try to fix this here.
        '''
        self.text = re.sub(' >+',r' &gt',self.text)
    
    def fix_href(self):
        ''' # Fix a malformed URL, e.g., 'href="/m.exe?a=110&l1=1&l2=2&s=process (<редк.>)&sc=671"'
            multitran.com provides for URLs that are not entirely
            correct: they still can contain spaces and unquoted symbols
            (such as 'à' or 'ф'). Browsers deal with this correctly but
            we must perform this additional step of quoting. Some
            symbols like '=', however, should not be quoted.
        '''
        f = '[MClient] plugins.multitrancom.cleanup.CleanUp.fix_href'
        if self.text:
            isearch = sh.Search (text = self.text
                                ,pattern = 'href="'
                                )
            poses = isearch.get_next_loop()
            poses = poses[::-1]
            for pos in poses:
                pos += len('href="')
                isearch.reset (text = self.text
                              ,pattern = '"'
                              )
                isearch.i = pos
                pos1 = isearch.get_next()
                if str(pos1).isdigit():
                    fragm = list(self.text[pos:pos1])
                    for i in range(len(fragm)):
                        if not fragm[i] in (':',';','/','=','&','?','%'):
                            fragm[i] = urllib.parse.quote(fragm[i])
                    fragm = ''.join(fragm)
                    self.text = self.text[0:pos] + fragm \
                                     + self.text[pos1:]
                else:
                    mes = _('Malformed HTML code!')
                    sh.objs.get_mes(f,mes).show_warning()
        else:
            sh.com.rep_empty(f)
    
    def delete_trash(self):
        self.text = self.text.replace ('>\xa0Terms for subject <a href'
                                      ,'><a href'
                                      )
        self.text = self.text.replace ('>\xa0Термины по тематике <a href'
                                      ,'><a href'
                                      )
        # Термины по тематике <...>, содержащие
        self.text = self.text.replace ('</a>, содержащие <strong>'
                                      ,'</a><strong>'
                                      )
        self.text = self.text.replace ('</a> containing <strong>'
                                      ,'</a><strong>'
                                      )
        self.text = self.text.replace('<u>','')
        self.text = self.text.replace('</u>','')
        ''' This allows to avoid further problems with tag parsing
            (unable to find terms in constructs like
            '<br><a href="/m.exe?SOME_URL" title="SOME_TITLE">BUGGY_TERM'
            which results in the first term being skipped when only 
            separate words were found).
        '''
        self.text = self.text.replace('<br>','')
    
    def delete_no_matches(self):
        if 'Не найдено<p>' in self.text:
            self.text = ''
    
    def run_sep_words(self):
        ''' If separate words are found instead of a phrase, prepare
            those words only.
        '''
        if sep_words_found in self.text:
            pos = sh.Search (text = self.text
                            ,pattern = sep_words_found
                            ).get_next()
            # -1 gives False
            if str(pos).isdigit():
                pos += len(sep_words_found)
                self.text = self.text[:pos]
                self.text = self.text.replace (sep_words_found
                                              ,'<span style="color:gray">%s</span>'\
                                              % sep_words_found
                                              )
    
    def distinguish(self):
        ''' Substitute some tags to make tag analysis easier. We should
            delete '<i>' as well, otherwise, there will be no dictionary
            titles.
        '''
        self.text = self.text.replace (' class="phraselist0"><i>'
                                      ,'><td class="subj">'
                                      )
        self.text = self.text.replace (' class="phraselist1"><i>'
                                      ,'><td class="subj">'
                                      )
        self.text = self.text.replace (' class="phraselist1">'
                                      ,'><td class="trans">'
                                      )
                                        
        self.text = self.text.replace (' class="phraselist2">'
                                      ,'><td class="trans">'
                                      )
    
    def run_common(self):
        # Delete unicode control codes
        self.text = re.sub(r'[\x00-\x1f\x7f-\x9f]','',self.text)
        self.text = self.text.replace('\r\n','')
        self.text = self.text.replace('\n','')
        self.text = self.text.replace('\xa0',' ')
        while '  ' in self.text:
            self.text = self.text.replace('  ',' ')
        self.text = re.sub(r'\>[\s]{0,1}\<','><',self.text)
    
    def delete_unsupported(self):
        ''' Remove characters from a range not supported by Tcl 
            (and causing a Tkinter error). Sample requests causing
            the error: Multitran, EN-RU: 'top', 'et al.'
        '''
        self.text = [char for char in self.text if ord(char) \
                     in range(65536)
                    ]
        self.text = ''.join(self.text)
    
    def run(self):
        f = '[MClient] plugins.multitrancom.cleanup.CleanUp.run'
        if self.text:
            self.fix_tags()
            self.delete_trash()
            self.run_common()
            self.run_sep_words()
            self.delete_no_matches()
            self.distinguish()
            self.delete_unsupported()
            self.fix_href()
        else:
            sh.com.rep_empty(f)
        return self.text
