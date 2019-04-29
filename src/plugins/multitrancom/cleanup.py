#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import html
import shared    as sh
import sharedGUI as sg

import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')

sep_words_found = 'найдены отдельные слова'


class CleanUp:
    
    def __init__(self,text):
        self._text = text
    
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
    
    def langs(self):
        self._text = self._text.replace ('<a href="/m.exe?a=256">Русский</a>'
                                        ,''
                                        )
        self._text = self._text.replace ('</a>Русский <a href'
                                        ,'</a><a href'
                                        )
        self._text = self._text.replace ('</a> Английский<p>'
                                        ,'</a><p>'
                                        )
        ''' Do not set a closing tag here; it can be both <p> and <div>.
            The space before '<' can be either missing or present.
        '''
        self._text = self._text.replace ('>⇄</a> Немецкий <'
                                        ,'></a><'
                                        )
        self._text = self._text.replace ('>⇄</a> Немецкий<'
                                        ,'></a><'
                                        )
        self._text = self._text.replace ('>Немецкий</a> <div id="suggest">'
                                        ,'></a><div id="suggest">'
                                        )
        self._text = self._text.replace ('>Словари</a>Немецкий <a href'
                                        ,'></a><a href'
                                        )
        self._text = self._text.replace ('class="phraselist2"><b>Немецкий</b>'
                                        ,'class="phraselist2">'
                                        )
        self._text = self._text.replace ('class="phraselist1"><b>English</b></td>'
                                        ,'class="phraselist1"></td>'
                                        )
        self._text = self._text.replace ('class="phraselist1"><b>Russian</b></td>'
                                        ,'class="phraselist1"></td>'
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
        self._text = self._text.replace('','')
        self._text = self._text.replace('','')
        self._text = self._text.replace('','')
        self._text = self._text.replace('','')
        self._text = self._text.replace('\r\n','')
        self._text = self._text.replace('\n','')
        self._text = self._text.replace('\xa0',' ')
        while '  ' in self._text:
            self._text = self._text.replace('  ',' ')
        self._text = re.sub(r'\>[\s]{0,1}\<','><',self._text)
    
    def decode_entities(self):
        ''' Needed both for MT and Stardict. Convert HTML entities
            to a human readable format, e.g., '&copy;' -> '©'.
        '''
        f = '[MClient] plugins.multitrancom.CleanUp.decode_entities'
        try:
            self._text = html.unescape(self._text)
        except:
            sh.objs.mes (f,_('ERROR')
                        ,_('Unable to convert HTML entities to UTF-8!')
                        )
    
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
        f = '[MClient] plugins.multitrancom.CleanUp.run'
        if self._text:
            self.decode_entities() # Shared
            self.trash()
            self.langs()
            self.common()          # Shared
            self.sep_words()
            self.no_matches()
            self.distinguish()
            self.unsupported()     # Shared
        else:
            sh.com.empty(f)
        return self._text
