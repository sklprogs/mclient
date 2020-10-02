#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import re
import skl_shared.shared as sh
from skl_shared.localize import _


''' A directory storing all DSL files.
    #NOTE: Do not forget to change this variable externally before
    calling anything from this module.
'''
PATH = ''
ICON = sh.objs.get_pdir().add('..','resources','icon_64x64_mclient.gif')
LANG1 = 'English'
LANG2 = 'Russian'
DEBUG = False


class Article:
    
    def __init__(self):
        self.dic = ''
        self.code = ''
        self.search = ''



class Get:
    
    def __init__(self,pattern,Debug=False,maxrows=0):
        self.set_values()
        self.Debug = Debug
        self.maxrows = maxrows
        self.pattern = pattern
    
    def _debug_articles(self):
        nos = []
        searches = []
        dics = []
        codes = []
        for i in range(len(self.articles)):
            nos.append(i+1)
            searches.append(self.articles[i].search)
            dics.append(self.articles[i].dic)
            codes.append(self.articles[i].code)
        iterable = [nos,searches,dics,codes]
        headers = (_('#'),_('SEARCH'),_('DICTIONARY'),_('CODE'))
        mes = sh.FastTable (iterable = iterable
                           ,headers  = headers
                           ,maxrow   = 70
                           ,maxrows  = self.maxrows
                           ).run()
        return _('Articles:') + '\n' + mes
    
    def debug(self):
        f = '[MClient] plugins.dsl.get.Get.debug'
        if self.Debug:
            if self.Success:
                mes = self._debug_articles()
                sh.com.run_fast_debug(f,mes)
            else:
                sh.com.cancel(f)
        else:
            sh.com.rep_lazy(f)
    
    def run(self):
        self.check()
        self.search()
        self.debug()
        return self.articles
    
    def check(self):
        f = '[MClient] plugins.dsl.get.Get.check'
        if not self.pattern:
            self.pattern = ''
        self.pattern = self.pattern.strip()
        self.pattern = self.pattern.lower()
        if not self.pattern:
            self.Success = False
            sh.com.rep_empty(f)
    
    def search(self):
        f = '[MClient] plugins.dsl.get.Get.search'
        if self.Success:
            dics = [idic for idic in objs.get_all_dics().dics \
                    if idic.lang1 == LANG1 and idic.lang2 == LANG2
                   ]
            dicnames = [idic.dicname for idic in dics]
            mes = _('Dictionaries to search in ({}/{}): {}')
            mes = mes.format (len(dicnames)
                             ,len(objs.all_dics.dics)
                             ,'; '.join(dicnames)
                             )
            sh.objs.get_mes(f,mes,True).show_debug()
            for idic in dics:
                iarticle = idic.search(self.pattern)
                if iarticle:
                    iarticle.dic = idic.dicname
                    self.articles.append(iarticle)
        else:
            sh.com.cancel(f)
    
    def set_values(self):
        self.articles = []
        self.blocks = []
        self.pattern = ''
        self.Success = True



class DSL:
    
    def __init__(self,file):
        self.set_values()
        self.file = file
        self.check()
    
    def run(self):
        f = '[MClient] plugins.dsl.get.DSL.run'
        timer = sh.Timer(f)
        timer.start()
        self.load()
        self.set_dic_name()
        self.set_lang1()
        self.set_lang2()
        self.cleanup()
        self.get_index()
        timer.end()
    
    def cleanup(self):
        f = '[MClient] plugins.dsl.get.DSL.cleanup'
        if self.Success:
            ''' #NOTE: a line can consist of spaces (actually happened).
                Be careful: 'strip' also deletes tabulation.
            '''
            self.lst = [line.strip(' ') for line in self.lst]
            self.lst = [line for line in self.lst if line \
                        and not line.startswith('#')
                       ]
        else:
            sh.com.cancel(f)
    
    def set_lang1(self):
        f = '[MClient] plugins.dsl.get.DSL.set_lang1'
        if self.Success:
            if len(self.lst) > 1:
                match = re.match('#INDEX_LANGUAGE	"(.*)"',self.lst[1])
                if match:
                    lang1 = match.group(1).strip()
                    if lang1:
                        self.lang1 = lang1
            else:
                mes = _('The file "{}" is too short ({} lines)!')
                mes = mes.format(self.file,len(self.lst))
                sh.objs.get_mes(f,mes,True).show_warning()
            mes = '"{}"'.format(self.lang1)
            sh.objs.get_mes(f,mes,True).show_debug()
        else:
            sh.com.cancel(f)
    
    def set_lang2(self):
        f = '[MClient] plugins.dsl.get.DSL.set_lang2'
        if self.Success:
            if len(self.lst) > 2:
                match = re.match ('#CONTENTS_LANGUAGE	"(.*)"'
                                 ,self.lst[2]
                                 )
                if match:
                    lang2 = match.group(1).strip()
                    if lang2:
                        self.lang2 = lang2
            else:
                mes = _('The file "{}" is too short ({} lines)!')
                mes = mes.format(self.file,len(self.lst))
                sh.objs.get_mes(f,mes,True).show_warning()
            mes = '"{}"'.format(self.lang2)
            sh.objs.get_mes(f,mes,True).show_debug()
        else:
            sh.com.cancel(f)
    
    def set_dic_name(self):
        # Do this before deleting comments ('self.strip')
        f = '[MClient] plugins.dsl.get.DSL.set_dic_name'
        if self.Success:
            ''' Since 'self.load' fails 'self.Success' on an empty
                input, 'self.lst' will always have a first item.
            '''
            match = re.match('#NAME	"(.*)"',self.lst[0])
            if match:
                dicname = match.group(1).strip()
                if dicname:
                    self.dicname = dicname
            mes = '"{}"'.format(self.dicname)
            sh.objs.get_mes(f,mes,True).show_debug()
        else:
            sh.com.cancel(f)
    
    def get_entry(self,pos):
        f = '[MClient] plugins.dsl.get.DSL.get_entry'
        if self.Success:
            pos = sh.Input(f,pos).get_integer()
            # We expect a translation which occupies the following line
            if 0 <= pos < len(self.lst) - 1:
                article = []
                i = pos + 1
                while i < len(self.lst):
                    if self.lst[i].startswith('\t'):
                        article.append(self.lst[i])
                    else:
                        break
                    i += 1
                iarticle = Article()
                iarticle.search = self.lst[pos]
                iarticle.code = '\n'.join(article)
                mes = '"{}"'.format(iarticle.code)
                sh.objs.get_mes(f,mes,True).show_debug()
                return iarticle
            else:
                sub = '0 <= {} < {}'.format(pos+1,len(self.lst))
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                sh.objs.get_mes(f,mes).show_error()
        else:
            sh.com.cancel(f)
    
    def search(self,pattern):
        f = '[MClient] plugins.dsl.get.DSL.search'
        if self.Success:
            if not pattern:
                pattern = ''
            pattern = pattern.strip()
            if pattern:
                pattern = pattern.lower()
                pos = -1
                try:
                    pos = self.get_index().index(pattern)
                except ValueError:
                    pass
                if pos > -1:
                    return self.get_entry(self.poses[pos])
                else:
                    mes = _('No search results for "{}" in "{}"')
                    mes = mes.format(pattern,self.dicname)
                    sh.objs.get_mes(f,mes,True).show_info()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def _delete_curly_brackets(self,line):
        line = re.sub('\{.*\}','',line)
        line = line.strip()
        line = line.lower()
        return line
    
    def get_index(self):
        f = '[MClient] plugins.dsl.get.DSL.get_index'
        if self.Success:
            if not self.index_:
                for i in range(len(self.lst)):
                    if not self.lst[i].startswith('\t'):
                        line = self._delete_curly_brackets(self.lst[i])
                        if line:
                            self.index_.append(line)
                            self.poses.append(i)
                mes = _('Dictionary "{}" ({}) has {} records')
                linesnum = sh.com.set_figure_commas(len(self.index_))
                mes = mes.format(self.bname,self.dicname,linesnum)
                sh.objs.get_mes(f,mes,True).show_info()
        else:
            sh.com.cancel(f)
        return self.index_
    
    def check(self):
        f = '[MClient] plugins.dsl.get.DSL.check'
        if self.file:
            self.Success = sh.File(self.file).Success
        else:
            self.Success = False
            sh.com.rep_empty(f)
    
    def load(self):
        f = '[MClient] plugins.dsl.get.DSL.load'
        if self.Success:
            self.bname = sh.Path(self.file).get_basename()
            mes = _('Load "{}"').format(self.file)
            sh.objs.get_mes(f,mes,True).show_info()
            text = ''
            try:
                with open(self.file,'r',encoding='UTF-16') as fi:
                    text = fi.read()
            except Exception as e:
                self.Success = False
                mes = _('Operation has failed!\n\nDetails: {}')
                mes = mes.format(e)
                sh.objs.get_mes(f,mes).show_warning()
            ''' Possibly, a memory consumption will be lower 
                if we do not store 'self.text'.
            '''
            if text:
                self.lst = text.splitlines()
            else:
                self.Success = False
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def set_values(self):
        self.file = ''
        self.bname = ''
        self.lst = []
        self.lang1 = _('Any')
        self.lang2 = _('Any')
        self.poses = []
        self.index_ = []
        self.blocks = []
        self.Success = True
        self.dicname = _('Untitled dictionary')



class Suggest:
    
    def __init__(self,search):
        self.set_values()
        if search:
            self.reset(search)
    
    def set_values(self):
        self.Success = True
        self.pattern = ''
    
    def reset(self,search):
        f = '[MClient] plugins.dsl.get.Suggest.reset'
        self.pattern = search
        if not self.pattern:
            self.Success = False
            sh.com.rep_empty(f)
    
    def get(self):
        f = '[MClient] plugins.dsl.get.Suggest.get'
        if self.Success:
            items = objs.get_all_dics().get_index()
            if items:
                timer = sh.Timer(f)
                timer.start()
                search = self.pattern.lower()
                result = [item for item in items \
                          if str(item).lower().startswith(search)
                         ]
                timer.end()
                mes = '; '.join(result)
                sh.objs.get_mes(f,mes,True).show_debug()
                return result
            else:
                self.Success = False
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def run(self):
        return self.get()



class AllDics:
    
    def __init__(self):
        self.set_values()
        self.reset()
    
    def get_index(self):
        f = '[MClient] plugins.dsl.get.AllDics.get_index'
        if self.Success:
            if not self.index_:
                for idic in self.dics:
                    self.index_ += idic.get_index()
                self.index_ = sorted(set(self.index_))
                mes = _('Index has {} entries').format(len(self.index_))
                sh.objs.get_mes(f,mes,True).show_info()
            return self.index_
        else:
            sh.com.cancel(f)
    
    def set_values(self):
        self.dsls = []
        self.dics = []
        self.path = ''
        self.index_ = []
        # Do not run anything if 'self.reset' was not run
        self.Success = False
    
    def reset(self):
        self.set_values()
        self.path = PATH
        self.Success = sh.Directory(self.path).Success
    
    def walk(self):
        f = '[MClient] plugins.dsl.get.AllDics.walk'
        if self.Success:
            if not self.dsls:
                for dirpath, dirnames, filenames in os.walk(self.path):
                    for filename in filenames:
                        lower = filename.lower()
                        if lower.endswith('.dsl'):
                            file = os.path.join(dirpath,filename)
                            self.dsls.append(file)
                sh.objs.get_mes(f,self.dsls,True).show_debug()
        else:
            sh.com.cancel(f)
        return self.dsls
    
    def locate(self):
        f = '[MClient] plugins.dsl.get.AllDics.locate'
        if self.Success:
            if not self.dics:
                if self.walk():
                    for dsl in self.dsls:
                        self.dics.append(DSL(dsl))
                else:
                    sh.com.rep_lazy(f)
            mes = _('{} offline dictionaries are available')
            mes = mes.format(len(self.dics))
            sh.objs.get_mes(f,mes,True).show_info()
            return self.dics
        else:
            sh.com.cancel(f)
    
    def load(self):
        f = '[MClient] plugins.dsl.get.AllDics.load'
        if self.Success:
            if self.locate():
                objs.get_progress().show()
                timer = sh.Timer(f)
                timer.start()
                for i in range(len(self.dics)):
                    text = _('Load DSL dictionaries ({}/{})')
                    text = text.format(i+1,len(self.dics))
                    objs.progress.set_text(text)
                    objs.progress.update(i,len(self.dics))
                    self.dics[i].run()
                timer.end()
                objs.progress.close()
                total_no = len(self.dics)
                self.dics = [dic for dic in self.dics if dic.Success]
                mes = _('Dictionaries loaded: {}/{}')
                mes = mes.format(len(self.dics),total_no)
                sh.objs.get_mes(f,mes,True).show_info()
            else:
                sh.com.rep_lazy(f)
        else:
            sh.com.cancel(f)



class Objects:
    
    def __init__(self):
        self.all_dics = self.progress = None
        
    def get_progress(self):
        if self.progress is None:
            self.progress = sh.ProgressBar(icon=ICON)
            self.progress.add()
        return self.progress
    
    def get_all_dics(self):
        if self.all_dics is None:
            self.all_dics = AllDics()
            self.all_dics.load()
        return self.all_dics



class Commands:
    
    def is_accessible(self):
        return len(objs.get_all_dics().dics)


objs = Objects()
com = Commands()


if __name__ == '__main__':
    f = '[MClient] plugins.dsl.get.__main__'
    PATH = sh.Home('mclient').add_config('dics')
    objs.get_all_dics().locate()
