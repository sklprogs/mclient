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


class Get:
    
    def __init__(self,pattern):
        self.set_values()
        self.pattern = pattern
    
    def run(self):
        self.check()
        self.search()
    
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
            for idic in objs.get_all_dics().dics:
                blocks = idic.search(self.pattern)
                if blocks:
                    self.blocks += blocks
        else:
            sh.com.cancel(f)
    
    def set_values(self):
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
    
    def _delete_trash(self,text):
        text = re.sub('\[lang id=\d+\]','',text)
        return text.replace('[/lang]','')
    
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
    
    def search(self):
        f = '[MClient] plugins.dsl.get.DSL.search'
        if self.Success:
            pass
        else:
            sh.com.cancel(f)
    
    def _delete_curly_brackets(self,line):
        line = re.sub('{.*}','',line)
        line = line.strip()
        line = line.lower()
        return line
    
    def get_index(self):
        f = '[MClient] plugins.dsl.get.DSL.get_index'
        if self.Success:
            if not self.index_:
                for line in self.lst:
                    if not line.startswith('\t'):
                        line = self._delete_curly_brackets(line)
                        if line:
                            self.index_.append(line)
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
                text = self._delete_trash(text)
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
                    self.index_ += [block.text for block in idic.blocks\
                                    if block.type_ == 'term'
                                   ]
                self.index_ = sorted(set(self.index_))
                mes = _('Index has {} entries').format(len(self.index_))
                sh.objs.get_mes(f,mes,True).show_info()
            return self.index_
        else:
            sh.com.cancel(f)
    
    def get(self,search):
        f = '[MClient] plugins.dsl.get.AllDics.get'
        if self.Success:
            if search:
                lst = []
                for dic in self.dics:
                    ind = dic.search(search)
                    # Returns True if ind >= 0
                    if str(ind).isdigit():
                        result = dic.get_dict_data(ind)
                        if result:
                            mes = _('"{}" has matches for "{}"')
                            mes = mes.format(dic.title,search)
                            sh.objs.get_mes(f,mes,True).show_debug()
                    else:
                        mes = _('No matches for "{}"!')
                        mes = mes.format(dic.title)
                        sh.objs.get_mes(f,mes,True).show_info()
                return '\n'.join(lst)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def set_values(self):
        self.dsls = []
        self.dics = []
        self.index_ = []
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
                sh.objs.get_waitbox().reset (func    = f
                                            ,message = _('Load local dictionaries')
                                            )
                sh.objs.waitbox.show()
                mes = _('Load offline dictionaries (DSL)')
                sh.objs.get_mes(f,mes,True).show_info()
                timer = sh.Timer(f)
                timer.start()
                for idic in self.dics:
                    idic.run()
                timer.end()
                total_no = len(self.dics)
                self.dics = [dic for dic in self.dics if dic.Success]
                mes = _('Dictionaries loaded: {}/{}')
                mes = mes.format(len(self.dics),total_no)
                sh.objs.get_mes(f,mes,True).show_info()
                sh.objs.waitbox.close()
            else:
                sh.com.rep_lazy(f)
        else:
            sh.com.cancel(f)



class Objects:
    
    def __init__(self):
        self.alldics = None
        
    def get_all_dics(self):
        if self.alldics is None:
            self.alldics = AllDics()
            self.alldics.load()
        return self.alldics



class Commands:
    
    def is_accessible(self):
        return len(objs.get_all_dics().dics)


objs = Objects()
com  = Commands()


if __name__ == '__main__':
    f = '[MClient] plugins.dsl.get.__main__'
    PATH = sh.Home('mclient').add_config('dics')
    objs.get_all_dics().locate()
