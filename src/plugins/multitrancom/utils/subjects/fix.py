#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _


class Split:
    ''' #NOTE: comma + space are used by Multitran to separate subjects;
        they are originally not always correct, e.g,
        'хобби.' -> 'Хобби, увлечения, досуг'.
    '''
    def __init__(self,lst):
        self.set_values()
        self.lst = lst
    
    def set_values(self):
        self.Success = True
        self.appropriate = []
        self.add = []
        self.lst = []
    
    def check(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.fix.Split.check'
        if self.lst:
            for row in self.lst:
                if not row:
                    self.Success = False
                    mes = _('Wrong input data!')
                    sh.objs.get_mes(f,mes,True).show_warning()
                    break
        else:
            self.Success = False
            sh.com.rep_empty(f)
    
    def _verify_commas(self,lst):
        commas = [item.count(', ') for item in lst]
        set_ = set(commas)
        return (len(set_) == 1) and (set_ != {0})
    
    def clean_up(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.fix.Split.clean_up'
        if self.Success:
            len_ = len(self.lst)
            for row in self.appropriate:
                self.lst.remove(row)
            delta = len_ - len(self.lst)
            sh.com.rep_deleted(f,delta)
        else:
            sh.com.cancel(f)
    
    def insert(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.fix.Split.insert'
        if self.Success:
            len_ = len(self.lst)
            for lst in self.add:
                self.lst.append(lst)
            delta = len(self.lst) - len_
            sh.com.rep_matches(f,delta)
        else:
            sh.com.cancel(f)
    
    def _split_row(self,lst):
        sub = []
        for item in lst:
            sub.append(item.split(', '))
        len_ = len(sub[0])
        for i in range(len_):
            row = []
            for j in range(len(sub)):
                row.append(sub[j][i])
            self.add.append(row)
    
    def split(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.fix.Split.split'
        if self.Success:
            for row in self.appropriate:
                self._split_row(row)
        else:
            sh.com.cancel(f)
    
    def set_appropriate(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.fix.Split.set_appropriate'
        if self.Success:
            for row in self.lst:
                if self._verify_commas(row):
                    self.appropriate.append(row)
            sh.com.rep_matches(f,len(self.appropriate))
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.check()
        self.set_appropriate()
        self.split()
        self.clean_up()
        self.insert()
        return self.lst



class Fix:
    
    def __init__(self,Debug=False):
        self.file = '/home/pete/bin/mclient/tests/subjects_orig.txt'
        self.filew = '/home/pete/bin/mclient/tests/subjects_auto.txt'
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
            self.split_by_tabs()
            delta = len_ - len(self.lst)
            sh.com.rep_deleted(f,delta)
        else:
            sh.com.cancel(f)
    
    def split_by_tabs(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.fix.Fix.split_by_tabs'
        if self.Success:
            self.lst = self.text.splitlines()
            for i in range(len(self.lst)):
                self.lst[i] = self.lst[i].split('\t')
        else:
            sh.com.cancel(f)
    
    def load(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.fix.Fix.load'
        if self.Success:
            self.text = sh.ReadTextFile(self.file).get()
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
    
    def split_by_subjects(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.fix.Fix.split_by_subjects'
        if self.Success:
            self.lst = Split(self.lst).run()
            lst = ['\t'.join(row) for row in self.lst]
            self.text = '\n'.join(lst)
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.load()
        self.split_by_tabs()
        self.delete_duplicates()
        self.check_tabs()
        self.check_titles()
        self.split_by_subjects()
        ''' We delete duplicates twice: first, to speed up processing,
            second, to delete duplicates generated by splitting the list
            by subjects.
        '''
        self.delete_duplicates()
        self.debug()
        self.save()
        self.launch()
