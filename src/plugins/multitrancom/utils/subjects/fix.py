#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _


class Fix:
    
    def __init__(self):
        #NOTE: create a backup first
        self.filew = '/home/pete/tmp/subjects'
        self.Success = True
        self.text = ''
        self.max_tabs = 9
    
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
            lst = self.text.splitlines()
            lst = sorted(set(lst))
            self.text = '\n'.join(lst)
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
        f = '[MClient] plugins.multitrancom.utils.subjects.fix.Fix.check_titles'
        if self.Success:
            mes = []
            lst = self.text.splitlines()
            for i in range(len(lst)):
                tmp = lst[i].split('\t')
                #TODO: delete when ready
                if len(tmp) == self.max_tabs + 1:
                    for j in range(len(tmp)):
                        if (j + 1) % 2 == 0 and '.' in tmp[j]:
                            sub = _('Line #{}, column #{}')
                            sub = sub.format(i+1,j+1)
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
            lst = self.text.splitlines()
            for i in range(len(lst)):
                count = lst[i].count('\t')
                if count != self.max_tabs:
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
        self.delete_duplicates()
        self.check_titles()
        self.check_tabs()
        self.save()
        self.launch()
