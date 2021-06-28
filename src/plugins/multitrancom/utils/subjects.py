#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
from skl_shared.localize import _
import skl_shared.shared as sh
# Will only work when being called from src/utils
import plugins.multitrancom.get as gt
import plugins.multitrancom.cleanup as cu
import plugins.multitrancom.tags as tg
import plugins.multitrancom.elems as el
import plugins.multitrancom.run as rn


class MiddlePage:
    
    def __init__(self,url,search='search'):
        self.Success = True
        self.blocks = []
        self.url = url
        self.search = search
    
    def run(self):
        self.check()
        self.fix_url()
        self.set_blocks()
        self.get_first()
    
    def get_first(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.MiddlePage.get_first'
        if self.Success:
            for block in self.blocks:
                if block.type_ == 'term' and block.text.strip() \
                and block.url:
                    return(block.url,block.text)
        else:
            sh.com.cancel(f)
    
    def set_blocks(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.MiddlePage.set_blocks'
        if self.Success:
            mes = _('Get "{}" at "{}"').format(self.search,self.url)
            sh.objs.get_mes(f,mes,True).show_debug()
            self.blocks = rn.Plugin().request (search = self.search
                                              ,url = self.url
                                              )
            if not self.blocks:
                self.Success = False
                sh.com.rep_out(f)
        else:
            sh.com.cancel(f)
    
    def fix_url(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.MiddlePage.fix_url'
        if self.Success:
            self.url = gt.com.fix_url(self.url)
            what = '&SHL=\d+'
            # Force a page to be in English
            with_ = '&SHL=1'
            self.url = re.sub(what,with_,self.url)
            if not '&SHL=' in self.url:
                self.url += with_
        else:
            sh.com.cancel(f)
    
    def check(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.MiddlePage.check'
        if not self.url:
            self.Success = False
            sh.com.rep_empty(f)



class Extractor:
    
    def __init__(self,Debug=False):
        self.Success = True
        self.filew = '/tmp/subjects'
        self.match = ''
        self.Debug = Debug
    
    def save(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.Extractor.save'
        if self.Success:
            match = self.match.splitlines()
            match = [item for item in match if item]
            match.sort()
            self.match = '\n'.join(match)
            sh.WriteTextFile(self.filew,True).write(self.match)
        else:
            sh.com.cancel(f)
    
    def launch(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.Extractor.launch'
        if self.Success:
            sh.Launch(self.filew).launch_default()
        else:
            sh.com.cancel(f)
    
    def run_batch(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.Extractor.run_pass'
        if self.Success:
            #cur
            #TODO: delete range when ready
            blocks = self.istart.blocks[20:25]
            for block in blocks:
                imiddle = MiddlePage(block.url,block.text)
                imiddle.run()
                tuple_ = imiddle.get_first()
                if tuple_:
                    icompare = Compare (url = tuple_[0]
                                       ,search = tuple_[1]
                                       ,Debug = self.Debug
                                       )
                    icompare.run()
                    self.match += icompare.match
                else:
                    self.Success = False
                    sh.com.rep_empty(f)
            else:
                self.Success = False
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def run_pass(self,lang1,lang2):
        f = '[MClient] plugins.multitrancom.utils.subjects.Extractor.run_pass'
        if self.Success:
            self.istart = StartPage (lang1 = lang1
                                    ,lang2 = lang2
                                    ,Debug = self.Debug
                                    )
            self.istart.run()
            self.Success = self.istart.Success
            self.run_batch()
        else:
            sh.com.cancel(f)
    
    def loop(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.Extractor.loop'
        if self.Success:
            self.run_pass(1,1)
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.loop()
        self.save()
        self.launch()



class Elems(el.Elems):
    
    def run(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.Elems.run'
        if self.check():
            # Do this before deleting ';'
            self.set_semino()
            # Do some cleanup
            self.delete_empty()
            self.delete_semi()
            self.delete_numeration()
            self.delete_tail_links()
            self.delete_trash_com()
            self.delete_langs()
            self.debug()
            return self.blocks
        else:
            sh.com.cancel(f)



class StartPage:
    
    def __init__(self,lang1=1,lang2=2,Debug=False):
        self.Success = True
        self.filew = '/tmp/subjects (abbr + full)'
        self.url = ''
        self.blocks = []
        self.lang1 = lang1
        self.lang2 = lang2
        self.Debug = Debug
    
    def _debug_blocks(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.StartPage._debug_blocks'
        nos = [i + 1 for i in range(len(self.blocks))]
        types = []
        texts = []
        urls = []
        for block in self.blocks:
            types.append(block.type_)
            texts.append(block.text)
            urls.append(block.url)
        headers = (_('#'),_('TYPE'),_('TEXT'),'URL')
        iterable = [nos,types,texts,urls]
        # 10'' monitor: 40 symbols per row
        mes = sh.FastTable (headers = headers
                           ,iterable = iterable
                           ,maxrow = 40
                           ).run()
        return f + '\n' + mes
    
    def debug(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.StartPage.debug'
        if self.Success:
            if self.Debug:
                mes = self._debug_blocks()
                sh.com.run_fast_debug(f,mes)
            else:
                sh.com.rep_lazy(f)
        else:
            sh.com.cancel(f)
    
    def set_blocks(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.StartPage.set_blocks'
        if self.Success:
            search = 'menu{}-{}'.format(self.lang1,self.lang2)
            htm = gt.Get (search = search
                         ,url = self.url
                         ).run()
            text = cu.CleanUp(htm).run()
            itags = tg.Tags(text)
            self.blocks = itags.run()
            self.blocks = Elems(self.blocks).run()
            for block in self.blocks:
                block.text = block.text.strip()
            self.blocks = [block for block in self.blocks \
                           if block.url and block.text
                          ]
            if not self.blocks:
                self.Success = False
                sh.com.rep_out(f)
        else:
            sh.com.cancel(f)
    
    def check(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.StartPage.check'
        self.Success = self.lang1 and self.lang2
        if not self.Success:
            sh.com.rep_empty(f)
        
    def set_url(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.StartPage.set_url'
        if self.Success:
            ''' Since gettext entries are English-based, English is
                selected as a primary language.
            '''
            self.url = 'https://www.multitran.com/m.exe?a=112&l1={}&l2={}&SHL=1'
            self.url = self.url.format(self.lang1,self.lang2)
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.check()
        self.set_url()
        self.set_blocks()
        self.debug()



class Compare:
    
    def __init__(self,url,search='search',Debug=False):
        self.Success = True
        self.ui_langs = [1,2,3,5,33]
        self.ipages = []
        self.match = ''
        self.Debug = Debug
        self.url = url
        self.search = search
    
    def debug(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.Compare.debug'
        if self.Success:
            if self.Debug:
                if self.match:
                    sh.com.run_fast_debug(f,self.match)
                else:
                    sh.com.rep_empty(f)
            else:
                sh.com.rep_lazy(f)
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.get_pages()
        self.compare()
        self.debug()
    
    def compare(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.Compare.compare'
        if self.Success:
            matches = []
            # Checks are done in 'self.get_pages'
            for hash_ in self.ipages[0].get_hashes():
                row = []
                for ipage in self.ipages:
                    tuple_ = ipage.get_by_hash(hash_)
                    if tuple_:
                        row.append(tuple_[0])
                        row.append(tuple_[1])
                matches.append('\t'.join(row))
            self.match = '\n'.join(matches)
        else:
            sh.com.cancel(f)
    
    def get_pages(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.Compare.get_pages'
        if self.Success:
            for ui_lang in self.ui_langs:
                ipage = EndPage (url = self.url
                                ,ui_lang = ui_lang
                                ,search = self.search
                                ,Debug = self.Debug
                                )
                ipage.run()
                if ipage.Success:
                    self.ipages.append(ipage)
                else:
                    self.Success = False
                    return
        else:
            sh.com.cancel(f)



class EndPage:
    
    def __init__(self,url,ui_lang,search='search',Debug=False):
        self.Success = True
        self.blocks = []
        self.rows = []
        self.subjects = {}
        self.url = url
        self.ui_lang = ui_lang
        self.Debug = Debug
        self.search = search
    
    def get_hashes(self):
        return list(self.subjects.keys())
    
    def get_by_hash(self,hash_):
        f = '[MClient] plugins.multitrancom.utils.subjects.EndPage.get_by_hash'
        if self.Success:
            # Hash can actually be 0
            try:
                return (self.subjects[hash_]['dic']
                       ,self.subjects[hash_]['dicf']
                       )
            except KeyError:
                mes = _('Wrong input data: "{}"!').format(hash_)
                sh.objs.get_mes(f,mes,True).show_warning()
        else:
            sh.com.cancel(f)
    
    def debug(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.EndPage.debug'
        if self.Success:
            if self.Debug:
                mes = [self._debug_rows(),self._debug_subjects()]
                mes = '\n\n'.join(mes)
                sh.com.run_fast_debug(f,mes)
            else:
                sh.com.rep_lazy(f)
        else:
            sh.com.cancel(f)
    
    def set_hashes(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.EndPage.set_hashes'
        if self.Success:
            for row in self.rows:
                if row:
                    texts = [block.text for block in row]
                    hash_ = hash(' '.join(texts))
                    block = row[0]
                    self.subjects[hash_] = {'dic':block.dic
                                           ,'dicf':block.dicf
                                           }
                else:
                    sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def fix_url(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.EndPage.fix_url'
        if self.Success:
            self.url = gt.com.fix_url(self.url)
            #TODO: Skip when 'gt.com.fix_url' is reworked
            what = '&SHL=\d+'
            with_ = '&SHL={}'.format(self.ui_lang)
            self.url = re.sub(what,with_,self.url)
            if not '&SHL=' in self.url:
                self.url += with_
        else:
            sh.com.cancel(f)
    
    def check(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.EndPage.check'
        if not self.url or not self.ui_lang:
            self.Success = False
            sh.com.rep_empty(f)
    
    def set_blocks(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.EndPage.set_blocks'
        if self.Success:
            search = '{} (lang: {})'.format(self.search,self.ui_lang)
            mes = _('Get "{}" at "{}"').format(search,self.url)
            sh.objs.get_mes(f,mes,True).show_debug()
            self.blocks = rn.Plugin().request (search = search
                                              ,url = self.url
                                              )
            if not self.blocks:
                self.Success = False
                sh.com.rep_out(f)
        else:
            sh.com.cancel(f)
    
    def _debug_rows(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.EndPage._debug_rows'
        # 'self.rows' contains blocks of certain types
        count = 0
        for row in self.rows:
            for block in row:
                count += 1
        nos = [i + 1 for i in range(count)]
        rownos = []
        types = []
        texts = []
        dic = []
        dicf = []
        for row in self.rows:
            for block in row:
                rownos.append(block.rowno)
                types.append(block.type_)
                texts.append(block.text)
                dic.append(block.dic)
                dicf.append(block.dicf)
        headers = (_('#'),_('ROW #'),'DIC','DICF',_('TYPE'),_('TEXT'))
        iterable = [nos,rownos,dic,dicf,types,texts]
        # 10'' screen: 30 symbols
        mes = sh.FastTable (headers = headers
                           ,iterable = iterable
                           ,maxrow = 30
                           ).run()
        return f + ':\n' + mes
    
    def _debug_subjects(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.EndPage._debug_subjects'
        nos = [i + 1 for i in range(len(self.subjects.keys()))]
        dic = []
        dicf = []
        hashes = []
        for key in self.subjects.keys():
            hashes.append(key)
            dic.append(self.subjects[key]['dic'])
            dicf.append(self.subjects[key]['dicf'])
        headers = (_('#'),_('DIC'),_('DICF'),_('HASH'))
        iterable = [nos,dic,dicf,hashes]
        # 10'' screen: 40 symbols
        mes = sh.FastTable (headers = headers
                           ,iterable = iterable
                           ,maxrow = 40
                           ).run()
        return f + ':\n' + mes
    
    def set_rows(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.EndPage.set_rows'
        if self.Success:
            blocks = [block for block in self.blocks \
                      if block.type_ in ('term','comment','user') \
                      and block.text
                     ]
            dic = ''
            row = []
            for block in blocks:
                if block.dic == dic:
                    row.append(block)
                elif row:
                    dic = block.dic
                    self.rows.append(row)
                    row = [block]
                else:
                    dic = block.dic
                    row = [block]
            if row:
                self.rows.append(row)
            if not self.rows:
                self.Success = False
                sh.com.rep_out(f)
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.check()
        self.fix_url()
        self.set_blocks()
        self.set_rows()
        self.set_hashes()
        self.debug()
        
