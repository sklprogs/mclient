#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.shared as sh
import plugins.multitrancom.utils.subjects.groups as gp


class Compile:
    
    def __init__(self,Debug=False):
        self.Success = True
        self.file = '/home/pete/bin/mclient/tests/subjects_auto.txt'
        self.text = ''
        self.lst = []
        self.subjects = {}
        self.colsno = 10
        self.Debug = Debug
    
    def _debug_attrs(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.compile.Compile._debug_attrs'
        nos = [i + 1 for i in range(len(self.subjects.keys()))]
        keys = []
        valid = []
        en = []
        majors = []
        groups = []
        for key in self.subjects:
            keys.append(key)
            en.append(self.subjects[key]['en']['title'])
            valid.append(self.subjects[key]['valid'])
            majors.append(self.subjects[key]['major'])
            groups.append(self.subjects[key]['group'])
        headers = (_('#'),_('KEY'),'EN',_('VALID'),_('MAJOR'),_('GROUP')
                  )
        iterable = [nos,keys,en,valid,majors,groups]
        # 10'' monitor: 30 symbols per column
        mes = sh.FastTable (iterable = iterable
                           ,headers = headers
                           ,maxrow = 30
                           ).run()
        return f + '\n' + mes
    
    def _debug_langs(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.compile.Compile._debug_langs'
        nos = [i + 1 for i in range(len(self.subjects.keys()))]
        keys = []
        valid = []
        en_short = []
        en = []
        ru_short = []
        ru = []
        de_short = []
        de = []
        sp_short = []
        sp = []
        uk_short = []
        uk = []
        for key in self.subjects:
            keys.append(key)
            valid.append(self.subjects[key]['valid'])
            en_short.append(self.subjects[key]['en']['short'])
            en.append(self.subjects[key]['en']['title'])
            ru_short.append(self.subjects[key]['ru']['short'])
            ru.append(self.subjects[key]['ru']['title'])
            de_short.append(self.subjects[key]['de']['short'])
            de.append(self.subjects[key]['de']['title'])
            sp_short.append(self.subjects[key]['es']['short'])
            sp.append(self.subjects[key]['es']['title'])
            uk_short.append(self.subjects[key]['uk']['short'])
            uk.append(self.subjects[key]['uk']['title'])
        headers = (_('#'),_('KEY'),_('VALID'),'ENS','EN','RUS','RU'
                  ,'DES','DE','SPS','SP','UKS','UK'
                  )
        iterable = [nos,keys,valid,en_short,en,ru_short,ru,de_short,de
                   ,sp_short,sp,uk_short,uk
                   ]
        # 10'' monitor: 8 symbols per column
        mes = sh.FastTable (iterable = iterable
                           ,headers = headers
                           ,maxrow = 8
                           ,ShowGap = False
                           ).run()
        return f + '\n' + mes
    
    def debug(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.compile.Compile.debug'
        if self.Success:
            if self.Debug:
                mes = [self._debug_langs(),self._debug_attrs()]
                mes = '\n\n'.join(mes)
                sh.com.run_fast_debug(f,mes)
            else:
                sh.com.rep_lazy(f)
        else:
            sh.com.cancel(f)
    
    def _is_valid(self,row):
        for item in row:
            if ', ' in item:
                return False
        return True
    
    def compile(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.compile.Compile.compile'
        if self.Success:
            for row in self.lst:
                if len(row) == self.colsno:
                    if row[0] in self.subjects:
                        mes = _('Key "{}" already exists!')
                        mes = mes.format(row[0])
                        sh.objs.get_mes(f,mes,True).show_warning()
                    else:
                        self.subjects[row[0]] = {}
                        self.subjects[row[0]]['valid'] = self._is_valid(row)
                        self.subjects[row[0]]['major'] = gp.objs.get_groups().is_major(row[1])
                        self.subjects[row[0]]['group'] = gp.objs.groups.get_major(row[1])
                        self.subjects[row[0]]['en'] = {}
                        self.subjects[row[0]]['ru'] = {}
                        self.subjects[row[0]]['de'] = {}
                        self.subjects[row[0]]['es'] = {}
                        self.subjects[row[0]]['uk'] = {}
                        self.subjects[row[0]]['en']['short'] = row[0]
                        self.subjects[row[0]]['en']['title'] = row[1]
                        self.subjects[row[0]]['ru']['short'] = row[2]
                        self.subjects[row[0]]['ru']['title'] = row[3]
                        self.subjects[row[0]]['de']['short'] = row[4]
                        self.subjects[row[0]]['de']['title'] = row[5]
                        self.subjects[row[0]]['es']['short'] = row[6]
                        self.subjects[row[0]]['es']['title'] = row[7]
                        self.subjects[row[0]]['uk']['short'] = row[8]
                        self.subjects[row[0]]['uk']['title'] = row[9]
                else:
                    self.Success = False
                    sub = '{} == {}'.format(len(row),self.colsno)
                    mes = _('The condition "{}" is not observed!')
                    mes = mes.format(sub)
                    sh.objs.get_mes(f,mes,True).show_warning()
        else:
            sh.com.cancel(f)
    
    def load(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.compile.Compile.load'
        if self.Success:
            self.text = sh.ReadTextFile(self.file).get()
            if not self.text:
                self.Success = False
                sh.com.rep_out(f)
        else:
            sh.com.cancel(f)
    
    def split(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.compile.Compile.split'
        if self.Success:
            self.lst = self.text.splitlines()
            self.lst = [row.split('\t') for row in self.lst]
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.load()
        self.split()
        self.compile()
        self.debug()
        #print(self.subjects)
