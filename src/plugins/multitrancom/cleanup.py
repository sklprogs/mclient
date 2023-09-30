#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re

from skl_shared.localize import _
import skl_shared.shared as sh

sep_words_found = 'найдены отдельные слова'


class CleanUp:
    
    def __init__(self,text):
        self.text = text
    
    def delete_trash_tags(self):
        # Do not divide a single block into parts
        self.text = self.text.replace('<i>','')
        self.text = self.text.replace('</i>','')
        self.text = self.text.replace('<u>','')
        self.text = self.text.replace('</u>','')
        self.text = self.text.replace('<b>','')
        self.text = self.text.replace('</b>','')
        # Fix parts of speech
        self.text = self.text.replace('<em><span style="color:gray">', '<em>')
        self.text = self.text.replace('</span></em>', '</em>')
    
    def fix_href(self):
        ''' Fix a malformed URL, e.g., 'href="/m.exe?a=110&l1=1&l2=2&s=process (<редк.>)&sc=671"'
            multitran.com provides for URLs that are not entirely correct: they
            still can contain spaces and unquoted symbols (such as 'à' or 'ф').
            Browsers deal with this correctly but we must perform this
            additional step of quoting. Some symbols like '=', however, should
            not be quoted.
            Takes ~0.056s for 'set' (EN-RU) on AMD E-300.
        '''
        f = '[MClient] plugins.multitrancom.cleanup.CleanUp.fix_href'
        if self.text:
            count = 0
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
                    fragm = self.text[pos:pos1]
                    if '<' in fragm or '>' in fragm:
                        fragm = fragm.replace('<','&lt;')
                        fragm = fragm.replace('>','&gt;')
                        self.text = self.text[0:pos] + fragm \
                                  + self.text[pos1:]
                        count += 1
                else:
                    mes = _('Malformed HTML code!')
                    sh.objs.get_mes(f,mes,True).show_warning()
            sh.com.rep_matches(f,count)
        else:
            sh.com.rep_empty(f)
    
    def fix_tags(self):
        ''' - Multitran does not escape '<' and '>' in user terms/comments
              properly. We try to fix this here.
            - Takes ~0.0044s for 'set' (EN-RU) on AMD E-300.
        '''
        self.text = re.sub(' >+',r' &gt',self.text)
    
    def run_common(self):
        # Delete unicode control codes
        # Takes ~0.037s for 'set' (EN-RU) on AMD E-300
        self.text = re.sub(r'[\x00-\x1f\x7f-\x9f]','',self.text)
        self.text = self.text.replace('\r\n','')
        self.text = self.text.replace('\n','')
        #TODO: Why this does not work?
        self.text = self.text.replace(r'\xa0',' ')
        while '  ' in self.text:
            self.text = self.text.replace('  ',' ')
        self.text = re.sub(r'\>[\s]{0,1}\<','><',self.text)
        # RU-EN: "вспоминать"
        self.text = self.text.replace ('<font color="darkgoldenrod" &gt'
                                      ,'<font color="darkgoldenrod">'
                                      )
    
    def run(self):
        f = '[MClient] plugins.multitrancom.cleanup.CleanUp.run'
        if self.text:
            self.delete_trash_tags()
            self.fix_href()
            self.fix_tags()
            self.run_common()
            ''' #TODO: do we really need this heaviest operation (takes ~0.53s
                for 'set' (EN-RU) on AMD E-300, whereas the entire module takes
                ~0.58s, since we have already deleted unicode control codes?
            '''
            # Delete a non-breaking space before a user name
            self.text = self.text.replace('&nbsp;',' ')
            self.text = sh.Text(self.text).delete_unsupported()
            return self.text
        else:
            sh.com.rep_empty(f)
            return ''
