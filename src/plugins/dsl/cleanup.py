#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import skl_shared.shared as sh
from skl_shared.localize import _


class CleanUp:
    
    def __init__(self,text):
        self.Success = True
        self.text = text
    
    def delete_unsupported(self):
        ''' Remove characters from a range not supported by Tcl
            (and causing a Tkinter error).
        '''
        f = '[MClient] plugins.dsl.cleanup.CleanUp.delete_unsupported'
        if self.Success:
            self.text = [char for char in self.text if ord(char) \
                         in range(65536)
                        ]
            self.text = ''.join(self.text)
        else:
            sh.com.cancel(f)
    
    def delete_trash(self):
        f = '[MClient] plugins.dsl.cleanup.CleanUp.delete_trash'
        if self.Success:
            while '  ' in self.text:
                self.text = self.text.replace('  ',' ')
            self.text = self.text.replace('[i]','')
            self.text = self.text.replace('[/i]','')
            self.text = re.sub('\[lang id=\d+\]','',self.text)
            self.text = self.text.replace('[/lang]','')
        else:
            sh.com.cancel(f)
    
    def check(self):
        f = '[MClient] plugins.dsl.cleanup.CleanUp.check'
        if not self.text:
            # Avoid None on output
            self.text = ''
            sh.com.rep_empty(f)
            self.Success = False
    
    def replace_tagged(self):
        # Replace cases like '\[item\]' with '(item)'
        f = '[MClient] plugins.dsl.cleanup.CleanUp.replace_tagged'
        if self.Success:
            pattern = r'.*\\\[(.+)\\\].*'
            match = re.match(pattern,self.text)
            count = 0
            while match:
                count += 1
                matched = match.group(1)
                replace_what = '\[{}\]'.format(matched)
                replace_with = '({})'.format(matched)
                self.text = self.text.replace(replace_what,replace_with)
                match = re.match(pattern,self.text)
            if count:
                mes = _('{} matches').format(count)
                sh.objs.get_mes(f,mes,True).show_debug()
        else:
            sh.com.cancel(f)

    def run(self):
        self.check()
        self.delete_trash()
        self.delete_unsupported()
        self.replace_tagged()
        return self.text
