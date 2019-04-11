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
message_board   = 'спросить в форуме'
p1 = '" href'
p2 = '<trash>'
p3 = '"</trash><a href'
p4 = '<a title="'
p5 = '</a>'
p6 = '<span STYLE="color:gray">'
p7 = '<span STYLE="color:black">'


class CleanUp:
    
    def __init__(self,text):
        self._text = text
    
    def common(self):
        self._text = self._text.replace('\r\n','')
        self._text = self._text.replace('\n','')
        self._text = self._text.replace('\xa0',' ')
        while '  ' in self._text:
            self._text = self._text.replace('  ',' ')
        self._text = re.sub(r'\>[\s]{0,1}\<','><',self._text)
    
    def style(self):
        ''' Do this before unescaping, otherwise, some tags describing
            wforms will become exactly comments. It seems that 'wform'
            tags are already present. Replacing these tags with
            alternative 'wform' tags does not work.
        '''
        self._text = self._text.replace('<span STYLE=&#34;color:gray&#34;>','').replace('<span STYLE=&#34;color:black&#34;>','')
    
    def decode_entities(self):
        ''' Needed both for MT and Stardict. Convert HTML entities
            to a human readable format, e.g., '&copy;' -> '©'.
        '''
        f = '[MClient] plugins.multitranru.CleanUp.decode_entities'
        try:
            self._text = html.unescape(self._text)
        except:
            sh.objs.mes (f,_('ERROR')
                        ,_('Unable to convert HTML entities to UTF-8!')
                        )
    
    def trash(self):
        ''' We need to close the tag since all following blocks with be
            'SAMECELL == 1' otherwise.
        '''
        self._text = self._text.replace ('<span STYLE="color:black">'
                                        ,'</span>'
                                        )
        ''' These tags shall be replaced since they are not related to
            'useful_tags' (useless/undefined tags with their contents
            are further removed), but we need the contents, and we
            cannot determine the type of the block yet.
        '''
        self._text = self._text.replace('<b>','').replace('</b>','')
        ''' Do this before 'common_replace'. Splitting terms is hindered
            without this.
        '''
        self._text = self._text.replace ('>;  <'
                                        ,'><'
                                        )
        self._text = self._text.replace ('Требуется авторизация'
                                        ,''
                                        )
        self._text = self._text.replace ('Термины, содержащие '
                                        ,''
                                        )
        self._text = self._text.replace ('Пожалуйста, войдите на сайт под Вашим именем'
                                        ,''
                                        )
        self._text = self._text.replace ('Вы знаете перевод этого слова? Добавьте его в словарь:'
                                        ,''
                                        )
        self._text = self._text.replace ('Вы знаете перевод этого выражения? Добавьте его в словарь:'
                                        ,''
                                        )
        self._text = self._text.replace('</span>Наблюдаются проблемы со входом из Хрома<span lang="en-us"> (</span>на','</span><span lang="en-us"></span>')
        self._text = self._text.replace ('сайте кое-что устарело, но пока не удаётся поменять'
                                        ,''
                                        )
        self._text = self._text.replace ('</a>, содержащие <strong>'
                                        ,'</a><strong>'
                                        )
    def word_forms(self):
        # An excessive space must be removed after unescaping the page
        self._text = re.sub('[:]{0,1}[\s]{0,1}все формы слов[а]{0,1} \(\d+\)','',self._text)
    
    def article_not_found(self):
        ''' If separate words are found instead of a phrase, prepare
            those words only.
        '''
        if sep_words_found in self._text:
            self._text = self._text.replace(sep_words_found,'')
            if message_board in self._text:
                board_pos = self._text.index(message_board)
            else:
                board_pos = -1
            while p1 in self._text:
                if self._text.index(p1) < board_pos:
                    self._text = self._text.replace(p1,p3)
                else:
                    break
            while p4 in self._text:
                tag_pos = self._text.index(p4)
                if tag_pos < board_pos:
                    self._text = self._text.replace(p4,p2,1)
                else:
                    break
            self._text = self._text[:board_pos] + p5 + p6 \
                                                + sep_words_found + p7
            self._text = self._text.replace(message_board,'')
    
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
        f = '[MClient] plugins.multitranru.CleanUp.run'
        if self._text:
            self.style()
            self.decode_entities()   # Shared
            self.trash()
            self.word_forms()
            self.common()            # Shared
            self.article_not_found()
            self.unsupported()       # Shared
        else:
            sh.com.empty(f)
        return self._text
