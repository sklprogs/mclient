#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
from skl_shared.localize import _
import skl_shared.shared as sh
import plugins.multitrancom.utils.subjects.groups as gp

''' Compile and Missing classes play a similar role but have a different
    implementation:
    - they take tab-delimited input with a different number of columns
    - due to the different input, compiling a final structure is
      different
    - 'Modified' and 'comment' attributes are different in Missing
'''


class Format:
    
    def __init__(self,subjects):
        self.set_values()
        self.subjects = subjects
    
    def set_values(self):
        self.Success = True
        self.formatted = ''
        self.subjects = {}
    
    def check(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.compile.Format.check'
        # Additional checks can be used if necessary
        if not self.subjects:
            self.Success = False
            sh.com.rep_empty(f)
    
    def run(self):
        self.check()
        self.format()
        return self.formatted
    
    def _format_valid(self):
        what = "': {'Valid':"
        with_ = "':\n{}{{'Valid':".format(15*' ')
        self.formatted = self.formatted.replace(what,with_)
    
    def _format_major_en(self):
        what = ", 'major_en':"
        with_ = "\n{},'major_en':".format(15*' ')
        self.formatted = self.formatted.replace(what,with_)
    
    def _format_major(self):
        what = ", 'Major':"
        with_ = "\n{},'Major':".format(15*' ')
        self.formatted = self.formatted.replace(what,with_)
    
    def _format_modified(self):
        what = ", 'Modified':"
        with_ = "\n{},'Modified':".format(15*' ')
        self.formatted = self.formatted.replace(what,with_)
    
    def _format_comment(self):
        what = ", 'comment':"
        with_ = "\n{},'comment':".format(15*' ')
        self.formatted = self.formatted.replace(what,with_)
    
    def _format_en(self):
        what = ", 'en':"
        with_ = "\n{},'en':".format(15*' ')
        self.formatted = self.formatted.replace(what,with_)
    
    def _format_ru(self):
        what = "}, 'ru':"
        with_ = "\n{}}}\n{},'ru':".format(19*' ',15*' ')
        self.formatted = self.formatted.replace(what,with_)
    
    def _format_de(self):
        what = "}, 'de':"
        with_ = "\n{}}}\n{},'de':".format(19*' ',15*' ')
        self.formatted = self.formatted.replace(what,with_)
    
    def _format_es(self):
        what = "}, 'es':"
        with_ = "\n{}}}\n{},'es':".format(19*' ',15*' ')
        self.formatted = self.formatted.replace(what,with_)
    
    def _format_uk(self):
        what = "}, 'uk':"
        with_ = "\n{}}}\n{},'uk':".format(19*' ',15*' ')
        self.formatted = self.formatted.replace(what,with_)
    
    def _format_short(self):
        what = ": {'short':"
        with_ = ":\n{}{{'short':".format(19*' ')
        self.formatted = self.formatted.replace(what,with_)
    
    def _format_title(self):
        what = ", 'title':"
        with_ = "\n{},'title':".format(19*' ')
        self.formatted = self.formatted.replace(what,with_)
    
    def _format_end(self):
        what = '}}, '
        with_ = '\n{}}}\n{}}}\n{},'.format(19*' ',15*' ',11*' ')
        self.formatted = self.formatted.replace(what,with_)
    
    def _format_last(self):
        what = '}}}'
        with_ = '\n{}}}\n{}}}\n{}}}'.format(19*' ',15*' ',11*' ')
        self.formatted = self.formatted.replace(what,with_)
    
    def format(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.compile.Compile.format'
        if self.Success:
            self.formatted = 'SUBJECTS = {}'.format(self.subjects)
            self._format_valid()
            self._format_major_en()
            self._format_major()
            self._format_modified()
            self._format_comment()
            self._format_en()
            self._format_ru()
            self._format_de()
            self._format_es()
            self._format_uk()
            self._format_short()
            self._format_title()
            self._format_end()
            self._format_last()
        else:
            sh.com.cancel(f)



class Missing:
    
    def __init__(self,Debug=False):
        self.set_values()
        self.Debug = Debug
    
    def copy(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.compile.Missing.copy'
        if self.Success:
            if self.formatted:
                sh.Clipboard().copy(self.formatted)
                mes = _('Copied to clipboard. Paste it and press Return to exit.')
                input(mes)
            else:
                self.Success = False
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def _is_valid(self,row):
        for item in row:
            if ', ' in item:
                return False
        return True
    
    def _is_vip(self,item):
        for vip in self.vip:
            if vip in item:
                return True
    
    def compile(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.compile.Missing.compile'
        if self.Success:
            for row in self.missing:
                if len(row) == self.col_num:
                    if row[0] in self.subjects:
                        mes = _('Key "{}" already exists!')
                        mes = mes.format(row[0])
                        sh.objs.get_mes(f,mes,True).show_warning()
                    else:
                        self.subjects[row[0]] = {}
                        self.subjects[row[0]]['Valid'] = self._is_valid(row)
                        major_en = gp.objs.get_groups().get_major(row[0])
                        is_major = gp.objs.groups.is_major(row[0])
                        is_vip = self._is_vip(row[0])
                        self.subjects[row[0]]['Major'] = is_major and not is_vip
                        self.subjects[row[0]]['Modified'] = True
                        self.subjects[row[0]]['comment'] = 'Short title is unknown'
                        self.subjects[row[0]]['major_en'] = major_en
                        self.subjects[row[0]]['en'] = {}
                        self.subjects[row[0]]['ru'] = {}
                        self.subjects[row[0]]['de'] = {}
                        self.subjects[row[0]]['es'] = {}
                        self.subjects[row[0]]['uk'] = {}
                        self.subjects[row[0]]['en']['short'] = row[0]
                        self.subjects[row[0]]['en']['title'] = row[0]
                        self.subjects[row[0]]['ru']['short'] = row[1]
                        self.subjects[row[0]]['ru']['title'] = row[1]
                        self.subjects[row[0]]['de']['short'] = row[2]
                        self.subjects[row[0]]['de']['title'] = row[2]
                        self.subjects[row[0]]['es']['short'] = row[3]
                        self.subjects[row[0]]['es']['title'] = row[3]
                        self.subjects[row[0]]['uk']['short'] = row[4]
                        self.subjects[row[0]]['uk']['title'] = row[4]
                else:
                    self.Success = False
                    sub = '{} == {}'.format(len(row),self.col_num)
                    mes = _('The condition "{}" is not observed!')
                    mes = mes.format(sub)
                    sh.objs.get_mes(f,mes,True).show_warning()
        else:
            sh.com.cancel(f)
    
    def _debug_missing(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.compile.Missing._debug_missing'
        rows = []
        for i in range(len(self.missing)):
            row = list(self.missing[i])
            row.insert(0,i+1)
            rows.append(row)
        headers = (_('#'),'EN','RU','DE','ES','UK')
        mes = sh.FastTable (iterable = rows
                           ,headers = headers
                           ,maxrow = 20
                           ,Transpose = True
                           ).run()
        return f + ':\n' + mes
    
    def match(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.compile.Missing.match'
        if self.Success:
            for subject in self.lst_wanted:
                for row in self.lst_titles:
                    if row[0] == subject:
                        self.missing.append(row)
            sh.com.rep_matches(f,len(self.missing))
        else:
            sh.com.cancel(f)
    
    def _debug_wanted(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.compile.Missing._debug_wanted'
        nos = [i + 1 for i in range(len(self.lst_wanted))]
        headers = (_('#'),_('TEXT'))
        iterable = [nos,self.lst_wanted]
        mes = sh.FastTable (headers = headers
                           ,iterable = iterable
                           ,maxrow = 50
                           ).run()
        return f + ':\n' + mes
    
    def _debug_original(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.compile.Missing._debug_original'
        nos = [i + 1 for i in range(len(self.lst_titles))]
        rows = []
        for i in range(len(self.lst_titles)):
            row = list(self.lst_titles[i])
            row.insert(0,i+1)
            rows.append(row)
        headers = (_('#'),'EN','RU','DE','ES','UK')
        mes = sh.FastTable (iterable = rows
                           ,headers = headers
                           ,Transpose = True
                           ,maxrow = 20
                           ).run()
        return f + ':\n' + mes
    
    def debug(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.compile.Missing.debug'
        if self.Success:
            if self.Debug:
                mes = [self._debug_original(),self._debug_wanted()
                      ,self._debug_missing()
                      ]
                mes = '\n\n'.join(mes)
                sh.com.run_fast_debug(f,mes)
            else:
                sh.com.rep_lazy(f)
        else:
            sh.com.cancel(f)
    
    def set_values(self):
        self.Success = True
        self.Debug = False
        self.file_titles = '/home/pete/bin/mclient/tests/all_titles_auto.txt'
        self.file_wanted = '/home/pete/bin/mclient/tests/translate titles.txt'
        self.subjects = {}
        self.lst_titles = []
        self.lst_wanted = []
        self.missing = []
        self.vip = ['Gruzovik','Игорь Миг']
        self.text_titles = ''
        self.text_wanted = ''
        self.col_num = 5
    
    def _delete_no(self,row):
        for i in range(len(row)):
            row[i] = re.sub('@\d+','',row[i])
        return row
    
    def split_titles(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.compile.Missing.split_titles'
        if self.Success:
            titles = self.text_titles.splitlines()
            titles = [item.strip() for item in titles if item.strip()]
            if titles:
                for row in titles:
                    row = row.split('\t')
                    if len(row) == self.col_num:
                        row = self._delete_no(row)
                        if row[0]:
                            self.lst_titles.append(row)
                        else:
                            self.Success = False
                            sh.com.rep_empty(f)
                            return
                    else:
                        self.Success = False
                        sub = '{} == {}'.format(len(row),self.col_num)
                        mes = _('The condition "{}" is not observed!')
                        mes = mes.format(sub)
                        sh.objs.get_mes(f,mes).show_warning()
                        return
            else:
                self.Success = False
                sh.com.rep_out(f)
        else:
            sh.com.cancel(f)
    
    def split_wanted(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.compile.Missing.split_wanted'
        if self.Success:
            self.lst_wanted = self.text_wanted.splitlines()
            self.lst_wanted = [item.strip() for item in self.lst_wanted\
                               if item.strip()
                              ]
            if not self.lst_wanted:
                self.Success = False
                sh.com.rep_out(f)
        else:
            sh.com.cancel(f)
    
    def load(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.compile.Missing.load'
        if self.Success:
            self.text_titles = sh.ReadTextFile(self.file_titles).get()
            self.text_wanted = sh.ReadTextFile(self.file_wanted).get()
            if not self.text_titles or not self.text_wanted:
                self.Success = False
                sh.com.rep_out(f)
        else:
            sh.com.cancel(f)
    
    def format(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.compile.Missing.format'
        if self.Success:
            self.formatted = Format(self.subjects).run()
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.load()
        self.split_wanted()
        self.split_titles()
        self.match()
        self.debug()
        self.compile()
        self.format()
        self.copy()



class Compile:
    
    def __init__(self,Debug=False):
        self.set_values()
        self.Debug = Debug
    
    def set_values(self):
        self.Debug = False
        self.Success = True
        self.file = '/home/pete/bin/mclient/tests/subjects_auto.txt'
        self.text = ''
        self.lst = []
        self.duplicates = []
        self.vip = ['Gruzovik','Игорь Миг']
        self.subjects = {}
        self.col_num = 10
        self.formatted = ''
    
    def _debug_duplicates(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.compile.Compile._debug_duplicates'
        mes = ['; '.join(row) for row in self.duplicates]
        mes = '\n\n'.join(mes)
        return f + ':\n' + mes
    
    def copy(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.compile.Compile.copy'
        if self.Success:
            if self.formatted:
                sh.Clipboard().copy(self.formatted)
                mes = _('Copied to clipboard. Paste it and press Return to exit.')
                input(mes)
            else:
                self.Success = False
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
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
            valid.append(self.subjects[key]['Valid'])
            majors.append(self.subjects[key]['Major'])
            groups.append(self.subjects[key]['major_en'])
        headers = (_('#'),_('KEY'),'EN',_('VALID'),_('MAJOR')
                  ,_('MAJOR (EN)')
                  )
        iterable = [nos,keys,en,valid,majors,groups]
        # 10'' monitor: 25 symbols per column
        mes = sh.FastTable (iterable = iterable
                           ,headers = headers
                           ,maxrow = 25
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
            valid.append(self.subjects[key]['Valid'])
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
                mes = [self._debug_langs(),self._debug_attrs()
                      ,self._debug_duplicates()
                      ]
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
    
    def _is_vip(self,item):
        for vip in self.vip:
            if vip in item:
                return True
    
    def compile(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.compile.Compile.compile'
        if self.Success:
            for row in self.lst:
                if len(row) == self.col_num:
                    if row[0] in self.subjects:
                        mes = _('Key "{}" already exists!')
                        mes = mes.format(row[0])
                        sh.objs.get_mes(f,mes,True).show_warning()
                        self.duplicates.append(row)
                    else:
                        self.subjects[row[0]] = {}
                        self.subjects[row[0]]['Valid'] = self._is_valid(row)
                        major_en = gp.objs.get_groups().get_major(row[1])
                        is_major = gp.objs.groups.is_major(row[1])
                        is_vip = self._is_vip(row[0])
                        self.subjects[row[0]]['Major'] = is_major and not is_vip
                        self.subjects[row[0]]['Modified'] = False
                        self.subjects[row[0]]['comment'] = ''
                        self.subjects[row[0]]['major_en'] = major_en
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
                    sub = '{} == {}'.format(len(row),self.col_num)
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
    
    def format(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.compile.Compile.format'
        if self.Success:
            self.formatted = Format(self.subjects).run()
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.load()
        self.split()
        self.compile()
        self.debug()
        self.format()
        self.copy()
