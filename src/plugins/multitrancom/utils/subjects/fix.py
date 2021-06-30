#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _


class Fix:
    
    def __init__(self,Debug=False):
        #NOTE: create a backup first
        self.filew = '/home/pete/bin/mclient/tests/subjects'
        self.Success = True
        self.text = ''
        self.lst = []
        self.colsno = 10
        self.Debug = Debug
    
    def _debug_list(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.fix.Fix._debug_list'
        return f + ':\n' + str(self.lst)
    
    def _debug_text(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.fix.Fix._debug_text'
        return f + ':\n' + self.text
    
    def debug(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.fix.Fix.debug'
        if self.Success:
            if self.Debug:
                mes = [self._debug_text(),self._debug_list()]
                mes = '\n\n'.join(mes)
                sh.com.run_fast_debug(f,mes)
            else:
                sh.com.rep_lazy(f)
        else:
            sh.com.cancel(f)
    
    def parse(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.fix.Fix.parse'
        if self.Success:
            pass
        else:
            sh.com.cancel(f)
    
    def save(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.fix.Fix.save'
        if self.Success:
            self.Success = sh.WriteTextFile(self.filew,True).write(self.text)
        else:
            sh.com.cancel(f)
    
    def launch(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.fix.Fix.launch'
        if self.Success:
            sh.Launch(self.filew).launch_default()
        else:
            sh.com.cancel(f)
    
    def delete_duplicates(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.fix.Fix.delete_duplicates'
        if self.Success:
            # We cannot do 'set' without joining sub-lists first
            lst = self.text.splitlines()
            len_ = len(lst)
            lst = sorted(set(lst))
            self.text = '\n'.join(lst)
            self.split()
            delta = len_ - len(self.lst)
            sh.com.rep_deleted(f,delta)
        else:
            sh.com.cancel(f)
    
    def split(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.fix.Fix.load'
        if self.Success:
            self.lst = self.text.splitlines()
            for i in range(len(self.lst)):
                self.lst[i] = self.lst[i].split('\t')
        else:
            sh.com.cancel(f)
    
    def load(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.fix.Fix.load'
        if self.Success:
            self.text = sh.ReadTextFile(self.filew).get()
            if not self.text:
                self.Success = False
                sh.com.rep_out(f)
        else:
            sh.com.cancel(f)
    
    def check_titles(self):
        # Do after 'self.check_tabs'
        f = '[MClient] plugins.multitrancom.utils.subjects.fix.Fix.check_titles'
        if self.Success:
            mes = []
            for i in range(len(self.lst)):
                for j in range(len(self.lst[i])):
                    ''' The presence of a dot is not enough, e.g.,
                        'SAP.tech.' -> 'SAP tech.'
                    '''
                    if (j + 1) % 2 == 0 \
                    and self.lst[i][j] == self.lst[i][j-1] \
                    and '.' in self.lst[i][j]:
                        sub = _('Line #{}, column #{}: "{}"')
                        sub = sub.format(i+1,j+1,self.lst[i][j])
                        mes.append(sub)
            if mes:
                self.Success = False
                sub = _('Errors in total: {}').format(len(mes))
                mes.insert(0,sub)
                mes.insert(1,_('Abbreviations instead of titles:'))
                mes = '\n'.join(mes)
                sh.objs.get_mes(f,mes).show_warning()
        else:
            sh.com.cancel(f)
    
    def check_tabs(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.fix.Fix.check_tabs'
        if self.Success:
            mes = []
            for i in range(len(self.lst)):
                if len(self.lst[i]) != self.colsno:
                    sub = _('Line #{}: a wrong number of tabulation characters: {}')
                    sub = sub.format(i+1,count)
                    mes.append(sub)
            if mes:
                self.Success = False
                sub = _('Errors in total: {}').format(len(mes))
                mes.insert(0,sub)
                mes = '\n'.join(mes)
                sh.objs.get_mes(f,mes).show_warning()
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.load()
        self.split()
        self.delete_duplicates()
        self.check_tabs()
        self.check_titles()
        self.debug()
        #self.save()
        #self.launch()
