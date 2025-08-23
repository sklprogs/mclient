#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import re

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.time import Timer
from skl_shared.logic import Input, com as shcom
from skl_shared.paths import Path, File, Directory
from skl_shared.graphics.progress_bar.controller import PROGRESS


''' A directory storing all DSL files.
    #NOTE: Do not forget to change this variable externally before
    calling anything from this module.
'''
PATH = ''
LANG1 = 'English'
LANG2 = 'Russian'
DEBUG = False


class Article:
    
    def __init__(self):
        self.dic = ''
        self.code = ''
        self.search = ''



class Get:
    
    def __init__(self, pattern, Debug=False, maxrows=0):
        self.set_values()
        self.Debug = Debug
        self.maxrows = maxrows
        self.pattern = pattern
    
    def _debug_articles(self):
        f = '[MClient] plugins.dsl.get.Get._debug_articles'
        mes = [f'{f}:']
        for i in range(len(self.articles)):
            sub = _('#{}:').format(i + 1)
            mes.append(sub)
            sub = _('Search: "{}"').format(self.articles[i].search)
            mes.append(sub)
            sub = _('Code:')
            mes.append(sub)
            mes.append(self.articles[i].code)
            mes.append('')
        return '\n'.join(mes)
    
    def debug(self):
        f = '[MClient] plugins.dsl.get.Get.debug'
        if not self.Debug:
            rep.lazy(f)
            return
        if not self.Success:
            rep.cancel(f)
            return
        return self._debug_articles()
    
    def run(self):
        self.check()
        self.search()
        return self.articles
    
    def check(self):
        f = '[MClient] plugins.dsl.get.Get.check'
        if not self.pattern:
            self.pattern = ''
        self.pattern = self.pattern.strip().lower()
        if not self.pattern:
            self.Success = False
            rep.empty(f)
    
    def search(self):
        f = '[MClient] plugins.dsl.get.Get.search'
        if not self.Success:
            rep.cancel(f)
            return
        dics = [idic for idic in objs.get_all_dics().dics \
                if idic.lang1 == LANG1 and idic.lang2 == LANG2
               ]
        dicnames = [idic.dicname for idic in dics]
        mes = _('Dictionaries to search in ({}/{}): {}')
        mes = mes.format(len(dicnames), len(objs.all_dics.dics)
                        ,'; '.join(dicnames))
        Message(f, mes).show_debug()
        for idic in dics:
            iarticle = idic.search(self.pattern)
            if iarticle:
                iarticle.dic = idic.dicname
                self.articles.append(iarticle)
    
    def set_values(self):
        self.articles = []
        self.blocks = []
        self.pattern = ''
        self.Success = True



class DSL:
    
    def __init__(self, file):
        self.set_values()
        self.file = file
        self.check()
    
    def run(self):
        f = '[MClient] plugins.dsl.get.DSL.run'
        timer = Timer(f)
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
        if not self.Success:
            rep.cancel(f)
            return
        ''' #NOTE: a line can consist of spaces (actually happened).
            Be careful: 'strip' also deletes tabulation.
        '''
        self.lst = [line.strip(' ') for line in self.lst]
        self.lst = [line for line in self.lst if line \
                   and not line.startswith('#')]
    
    def set_lang1(self):
        f = '[MClient] plugins.dsl.get.DSL.set_lang1'
        if not self.Success:
            rep.cancel(f)
            return
        if len(self.lst) <= 1:
            mes = _('The file "{}" is too short ({} lines)!')
            mes = mes.format(self.file, len(self.lst))
            Message(f, mes).show_warning()
            return
        match = re.match('#INDEX_LANGUAGE	"(.*)"', self.lst[1])
        if match:
            lang1 = match.group(1).strip()
            if lang1:
                self.lang1 = lang1
        mes = '"{}"'.format(self.lang1)
        Message(f, mes).show_debug()
    
    def set_lang2(self):
        f = '[MClient] plugins.dsl.get.DSL.set_lang2'
        if not self.Success:
            rep.cancel(f)
            return
        if len(self.lst) <= 2:
            mes = _('The file "{}" is too short ({} lines)!')
            mes = mes.format(self.file, len(self.lst))
            Message(f, mes).show_warning()
            return
        match = re.match('#CONTENTS_LANGUAGE	"(.*)"', self.lst[2])
        if match:
            lang2 = match.group(1).strip()
            if lang2:
                self.lang2 = lang2
        mes = '"{}"'.format(self.lang2)
        Message(f, mes).show_debug()
    
    def set_dic_name(self):
        # Do this before deleting comments ('self.strip')
        f = '[MClient] plugins.dsl.get.DSL.set_dic_name'
        if not self.Success:
            rep.cancel(f)
            return
        ''' Since 'self.load' fails 'self.Success' on an empty input,
            'self.lst' will always have a first item.
        '''
        match = re.match('#NAME	"(.*)"', self.lst[0])
        if match:
            dicname = match.group(1).strip()
            if dicname:
                self.dicname = dicname
        mes = '"{}"'.format(self.dicname)
        Message(f, mes).show_debug()
    
    def get_entry(self, pos):
        f = '[MClient] plugins.dsl.get.DSL.get_entry'
        if not self.Success:
            rep.cancel(f)
            return
        pos = Input(f, pos).get_integer()
        # We expect a translation which occupies the following line
        if not (0 <= pos < len(self.lst) - 1):
            sub = '0 <= {} < {}'.format(pos + 1, len(self.lst))
            mes = _('The condition "{}" is not observed!')
            mes = mes.format(sub)
            Message(f, mes, True).show_error()
            return
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
        mes = f'"{iarticle.code}"'
        Message(f, mes).show_debug()
        return iarticle
    
    def search(self, pattern):
        f = '[MClient] plugins.dsl.get.DSL.search'
        if not self.Success:
            rep.cancel(f)
            return
        if not pattern:
            pattern = ''
        pattern = pattern.strip()
        if not pattern:
            rep.empty(f)
            return
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
            mes = mes.format(pattern, self.dicname)
            Message(f, mes).show_info()
    
    def _delete_curly_brackets(self, line):
        line = re.sub('\{.*\}', '', line)
        line = line.strip()
        line = line.lower()
        return line
    
    def get_index(self):
        f = '[MClient] plugins.dsl.get.DSL.get_index'
        if not self.Success:
            rep.cancel(f)
            return self.index_
        if not self.index_:
            for i in range(len(self.lst)):
                if not self.lst[i].startswith('\t'):
                    line = self._delete_curly_brackets(self.lst[i])
                    if line:
                        self.index_.append(line)
                        self.poses.append(i)
            mes = _('Dictionary "{}" ({}) has {} records')
            linesnum = shcom.set_figure_commas(len(self.index_))
            mes = mes.format(self.fname, self.dicname, linesnum)
            Message(f, mes).show_info()
        return self.index_
    
    def check(self):
        f = '[MClient] plugins.dsl.get.DSL.check'
        if not self.file:
            self.Success = False
            rep.empty(f)
            return
        self.Success = File(self.file).Success
    
    def load(self):
        f = '[MClient] plugins.dsl.get.DSL.load'
        if not self.Success:
            rep.cancel(f)
            return
        self.fname = Path(self.file).get_filename()
        mes = _('Load "{}"').format(self.file)
        Message(f, mes).show_info()
        text = ''
        try:
            with open(self.file, 'r', encoding='UTF-16') as fi:
                text = fi.read()
        except Exception as e:
            self.Success = False
            mes = _('Operation has failed!\n\nDetails: {}')
            mes = mes.format(e)
            Message(f, mes, True).show_warning()
        ''' Possibly, a memory consumption will be lower if we do not store
            'self.text'.
        '''
        if not text:
            self.Success = False
            rep.empty(f)
            return
        self.lst = text.splitlines()
    
    def set_values(self):
        self.file = ''
        self.fname = ''
        self.lst = []
        self.lang1 = _('Any')
        self.lang2 = _('Any')
        self.poses = []
        self.index_ = []
        self.blocks = []
        self.Success = True
        self.dicname = _('Untitled dictionary')



class Suggest:
    
    def __init__(self, search):
        self.set_values()
        if search:
            self.reset(search)
    
    def set_values(self):
        self.Success = True
        self.pattern = ''
    
    def reset(self, search):
        f = '[MClient] plugins.dsl.get.Suggest.reset'
        self.pattern = search
        if not self.pattern:
            self.Success = False
            rep.empty(f)
    
    def get(self):
        f = '[MClient] plugins.dsl.get.Suggest.get'
        if not self.Success:
            rep.cancel(f)
            return
        items = objs.get_all_dics().get_index()
        if not items:
            self.Success = False
            rep.empty(f)
            return
        timer = Timer(f)
        timer.start()
        search = self.pattern.lower()
        result = [item for item in items if str(item).lower().startswith(search)]
        timer.end()
        mes = '; '.join(result)
        Message(f, mes).show_debug()
        return result
    
    def run(self):
        return self.get()



class AllDics:
    
    def __init__(self):
        self.reset()
    
    def get_langs2(self):
        f = '[MClient] plugins.dsl.get.AllDics.get_langs2'
        if not self.Success:
            rep.cancel(f)
            return self.langs2
        if not self.langs2:
            for lang in self.langs:
                self.langs2 += self.langs[lang]['pairs']
            self.langs2 = list(set(lang for lang in self.langs2 if lang))
            for i in range(len(self.langs2)):
                self.langs2[i] = self.langs[self.langs2[i]]['localized']
            self.langs2 = tuple(sorted(self.langs2))
            mes = '; '.join(self.langs2)
            Message(f, f'"{mes}"').show_debug()
        return self.langs2
    
    def get_langs1(self):
        f = '[MClient] plugins.dsl.get.AllDics.get_langs1'
        if not self.Success:
            rep.cancel(f)
            return self.langs1
        if not self.langs1:
            for lang in self.langs.keys():
                try:
                    if self.langs[lang]['pairs']:
                        self.langs1.append(self.langs[lang]['localized'])
                except KeyError:
                    rep.wrong_input(f, lang)
            self.langs1 = tuple(sorted(set(self.langs1)))
            mes = '; '.join(self.langs1)
            mes = '"{}"'.format(mes)
            Message(f, mes).show_debug()
        return self.langs1
    
    def get_code(self, lang):
        # Both language code and localization name are accepted at input
        f = '[MClient] plugins.dsl.get.AllDics.get_code'
        if not self.Success:
            rep.cancel(f)
            return lang
        if lang in self.langs:
            return self.langs[lang]['code']
        else:
            rep.wrong_input(f, lang)
        return lang
    
    def get_pairs(self, lang):
        # Both language code and localization name are accepted at input
        f = '[MClient] plugins.dsl.get.AllDics.get_pairs'
        pairs = []
        if not self.Success:
            rep.cancel(f)
            return pairs
        if not lang:
            rep.empty(f)
            return pairs
        if not lang in self.langs:
            rep.wrong_input(f, lang)
            return pairs
        langs = self.langs[lang]['pairs']
        for code in langs:
            if code in self.langs:
                pairs.append(self.langs[code]['localized'])
            else:
                rep.wrong_input(f, code)
        pairs = tuple(sorted(set(pairs)))
        mes = '; '.join(pairs)
        Message(f, mes).show_debug()
        return pairs
    
    def _create_lang(self, lang):
        localized = _(lang)
        if not lang in self.langs:
            self.langs[lang] = {}
            self.langs[lang]['code'] = lang
            self.langs[lang]['localized'] = localized
            self.langs[lang]['pairs'] = []
            self.langs[localized] = {}
            self.langs[localized]['code'] = lang
            self.langs[localized]['localized'] = localized
            self.langs[localized]['pairs'] = []
    
    def set_langs(self):
        ''' DSL dictionaries are one-way only because of the index
            structure.
        '''
        f = '[MClient] plugins.dsl.get.AllDics.set_langs'
        if not self.Success:
            rep.cancel(f)
            return
        for idic in self.dics:
            self._create_lang(idic.lang1)
            self._create_lang(idic.lang2)
            self.langs[idic.lang1]['pairs'].append(idic.lang2)
            self.langs[_(idic.lang1)]['pairs'].append(idic.lang2)
    
    def get_index(self):
        f = '[MClient] plugins.dsl.get.AllDics.get_index'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.index_:
            for idic in self.dics:
                self.index_ += idic.get_index()
            self.index_ = sorted(set(self.index_))
            mes = _('Index has {} entries').format(len(self.index_))
            Message(f, mes).show_info()
        return self.index_
    
    def set_values(self):
        self.path = ''
        self.dsls = []
        self.dics = []
        self.index_ = []
        self.langs = {}
        self.langs1 = []
        self.langs2 = []
        # Do not run anything if 'self.reset' was not run
        self.Success = False
    
    def reset(self):
        self.set_values()
        self.path = PATH
        self.Success = Directory(self.path).Success
    
    def walk(self):
        f = '[MClient] plugins.dsl.get.AllDics.walk'
        if not self.Success:
            rep.cancel(f)
            return self.dsls
        if self.dsls:
            return self.dsls
        for dirpath, dirnames, filenames in os.walk(self.path):
            for filename in filenames:
                lower = filename.lower()
                if lower.endswith('.dsl'):
                    file = os.path.join(dirpath, filename)
                    self.dsls.append(file)
        Message(f, self.dsls).show_debug()
        return self.dsls
    
    def locate(self):
        f = '[MClient] plugins.dsl.get.AllDics.locate'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.dics:
            if self.walk():
                for dsl in self.dsls:
                    self.dics.append(DSL(dsl))
            else:
                rep.lazy(f)
        mes = _('{} offline dictionaries are available')
        mes = mes.format(len(self.dics))
        Message(f, mes).show_info()
        return self.dics
    
    def load(self):
        f = '[MClient] plugins.dsl.get.AllDics.load'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.locate():
            rep.lazy(f)
            return
        PROGRESS.set_title(_('Dictionary Loader'))
        PROGRESS.show()
        timer = Timer(f)
        timer.start()
        PROGRESS.set_value(0)
        PROGRESS.set_max(len(self.dics))
        for i in range(len(self.dics)):
            PROGRESS.update()
            text = _('Load DSL dictionaries ({}/{})')
            text = text.format(i + 1, len(self.dics))
            PROGRESS.set_info(text)
            self.dics[i].run()
            PROGRESS.inc()
        timer.end()
        PROGRESS.close()
        total_no = len(self.dics)
        self.dics = [dic for dic in self.dics if dic.Success]
        mes = _('Dictionaries loaded: {}/{}')
        mes = mes.format(len(self.dics), total_no)
        Message(f, mes).show_info()



class Objects:
    
    def __init__(self):
        self.all_dics = None
    
    def get_all_dics(self):
        if self.all_dics is None:
            self.all_dics = AllDics()
            self.all_dics.load()
            self.all_dics.set_langs()
        return self.all_dics



class Commands:
    
    def count_valid(self):
        return len(objs.get_all_dics().dics)


objs = Objects()
com = Commands()
