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



class Subjects:
    
    def __init__(self):
        self.set_values()
    
    def _get_title(self,url):
        match = re.match('.* title="(.*)',url)
        if match:
            return match.group(1)

    def _find_abbr(self,abbr,url,subject):
        f = '[MClient] plugins.multitrancom.utils.subjects.Subjects._find_abbr'
        title = self._get_title(url)
        if title and abbr and url and subject:
            # This actually happens
            title = title.replace(sh.lg.nbspace,' ')
            # Just to be on a safe side
            abbr = abbr.replace(sh.lg.nbspace,' ')
            title_split = title.split(', ')
            abbr_split = abbr.split(', ')
            title_split = [title.strip() for title in title_split]
            abbr_split = [abbr.strip() for abbr in abbr_split]
            ''' Sometimes not all abbreviations are given the full form,
                e.g., 'юр., англос.' -> 'Общее право (англосаксонская
                правовая система)'. Since this function returns only
                one abbreviation, it is safe to make the lists to be
                of the same length.
            '''
            filler = title_split[0]
            Filled = False
            while len(title_split) < len(abbr_split):
                Filled = True
                title_split.append(filler)
            if len(title_split) == len(abbr_split):
                for i in range(len(title_split)):
                    if title_split[i] == subject:
                        if Filled:
                            return abbr
                        else:
                            return abbr_split[i]
            else:
                sub = '{} == {}'.format (len(title_split)
                                        ,len(abbr_split)
                                        )
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                sh.objs.get_mes(f,mes,True).show_warning()
        else:
            sh.com.rep_empty(f)
    
    def _fix_url(self,url):
        url = gt.com.fix_url(url)
        #TODO: Skip when 'gt.com.fix_url' is reworked
        what = '&SHL=\d+'
        with_ = '&SHL={}'.format(self.ui_lang)
        url = re.sub(what,with_,url)
        if not '&SHL=' in url:
            url += with_
        return url
    
    def _debug_dics(self,blocks):
        f = '[MClient] plugins.multitrancom.utils.subjects.Subjects._debug_dics'
        nos = [i + 1 for i in range(len(blocks))]
        types = ['dic' for i in range(len(blocks))]
        texts = [block.text for block in blocks]
        urls = [block.url for block in blocks]
        headers = (_('#'),_('TYPE'),_('TEXT'),_('URL'))
        texts, nos, urls = (list(x) for x \
            in zip (*sorted (zip (texts,nos,urls)
                            ,key = lambda x:x[0].lower()
                            )
                   )
                                   )
        iterable = [nos,types,texts,urls]
        mes = sh.FastTable (iterable = iterable
                           ,headers = headers
                           ).run()
        sh.com.run_fast_debug(f,mes)
    
    def dump(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.Subjects.dump'
        if self.Success:
            mes = []
            for i in range(len(self.titles)):
                sub = '{}\t{}'.format(self.titles[i],self.abbrs[i])
                mes.append(sub)
            for i in range(len(self.failed_titles)):
                sub = '{}\t{}'.format(self.failed_titles[i],'?')
                mes.append(sub)
            mes = '\n'.join(mes)
            #sh.com.run_fast_debug(f,mes)
            sh.WriteTextFile(self.filew,True).write(mes)
            sh.Launch(self.filew).launch_default()
        else:
            sh.com.cancel(f)
    
    def debug(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.Subjects.debug'
        if self.Success:
            nos = [i + 1 for i in range(len(self.abbrs))]
            headers = (_('#'),_('TITLE'),_('ABBREVIATION'))
            iterable = [nos,self.titles,self.abbrs]
            mes = sh.FastTable (headers = headers
                               ,iterable = iterable
                               ).run()
            sh.com.run_fast_debug(f,mes)
        else:
            sh.com.cancel(f)
    
    def filter_subjects(self,blocks):
        return [block for block in blocks \
                if block.type_ == 'dic' and block.text
               ]
    
    def get_blocks_final(self,block):
        f = '[MClient] plugins.multitrancom.utils.subjects.Subjects.get_blocks_final'
        blocks = []
        if self.Success:
            if block:
                block.url = self._fix_url(block.url)
                mes = _('Get "{}" at "{}"').format(block.text,block.url)
                sh.objs.get_mes(f,mes,True).show_debug()
                return rn.Plugin().request (search = block.text
                                           ,url = block.url
                                           )
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
        return blocks
    
    def get_abbr(self,block,dicf):
        f = '[MClient] plugins.multitrancom.utils.subjects.Subjects.get_abbr'
        if self.Success:
            blocks = self.get_blocks_final(block)
            #self._debug_dics(blocks)
            for block in blocks:
                abbr = self._find_abbr (abbr = block.text
                                       ,url = block.url
                                       ,subject = dicf
                                       )
                if abbr:
                    return(abbr,block.no)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def get_next(self,block):
        f = '[MClient] plugins.multitrancom.utils.subjects.Subjects.get_next'
        if self.Success:
            if block:
                url = block.url
                url = self._fix_url(url)
                mes = _('Get "{}" at "{}"').format(block.text,url)
                sh.objs.get_mes(f,mes,True).show_debug()
                blocks = rn.Plugin().request (search = block.text
                                             ,url = url
                                             )
                blocks = [block for block in blocks \
                          if block.type_ == 'term' and block.url
                         ]
                if blocks:
                    blocks[0].text = blocks[0].text.strip()
                    return blocks[0]
                else:
                    sh.com.rep_empty(f)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def get_english(self,block):
        f = '[MClient] plugins.multitrancom.utils.subjects.Subjects.get_english'
        if self.Success:
            self.ui_lang = 1
            blocks = self.get_blocks_final(block)
            blocks = self.filter_subjects(blocks)
        else:
            sh.com.cancel(f)
    
    def get_urls(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.Subjects.get_urls'
        if self.Success:
            if self.blocks:
                # For testing purposes, decrease a number of blocks here
                #cur
                #self.blocks[20:30]
                self.blocks = [self.blocks[30]]
                ui_langs = list(self.ui_langs)
                ui_langs.remove(1)
                for block in self.blocks:
                    dicf = block.text
                    # This actually happens
                    dicf = dicf.replace(sh.lg.nbspace,' ')
                    dicf = dicf.strip()
                    if not dicf in self.titles:
                        self.ui_lang = 1
                        block = self.get_next(block)
                        tuple_ = self.get_abbr(block,dicf)
                        if dicf and tuple_:
                            abbr = tuple_[0]
                            block_no = tuple_[1] - 1
                            mes = '"{}" -> "{}"'.format(abbr,dicf)
                            sh.objs.get_mes(f,mes,True).show_info()
                            self.titles.append(dicf)
                            self.abbrs.append(abbr)
                            for self.ui_lang in ui_langs:
                                block = self.get_next(block)
                                blocks = self.get_blocks_final(block)
                                if block_no < len(blocks):
                                    block = blocks[block_no]
                                    subject = block.text
                                    subject = subject.replace(sh.lg.nbspace,'')
                                    subject = subject.strip()
                                    tuple_ = self._find_abbr (abbr = block.text
                                                             ,url = block.url
                                                             ,subject = subject
                                                             )
                                    if tuple_:
                                        abbr = tuple_[0]
                                        mes = '"{}" -> "{}"'
                                        mes = mes.format(abbr,dicf)
                                        sh.objs.get_mes(f,mes,True).show_info()
                                        self.titles.append(subject)
                                        self.abbrs.append(abbr)
                                    else:
                                        sh.com.rep_empty(f)
                                else:
                                    sub = '{} < {}'.format (block_no
                                                           ,len(blocks)
                                                           )
                                    mes = _('The condition "{}" is not observed!')
                                    mes = mes.format(sub)
                                    sh.objs.get_mes(f,mes,True).show_warning()
                        elif dicf:
                            mes = _('No match has been found for "{}"!')
                            mes = mes.format(dicf)
                            sh.objs.get_mes(f,mes,True).show_warning()
                            if not dicf in self.failed_titles:
                                self.failed_titles.append(dicf)
                        else:
                            sh.com.rep_empty(f)
            else:
                self.Success = False
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def get_menu(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.Subjects.get_menu'
        if self.Success:
            search = 'menu{}-{}'.format(self.lang1,self.lang2)
            htm = gt.Get (search = search
                         ,url = self.menu_url
                         ).run()
            text = cu.CleanUp(htm).run()
            itags = tg.Tags(text)
            self.blocks = itags.run()
            self.blocks = Elems(self.blocks).run()
            self.blocks = [block for block in self.blocks if block.url]
            for block in self.blocks:
                block.text = block.text.strip()
        else:
            sh.com.cancel(f)
    
    def check(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.Subjects.check'
        self.Success = self.lang1 and self.lang2
        if not self.Success:
            sh.com.rep_empty(f)
        
    def set_menu_url(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.Subjects.set_menu_url'
        if self.Success:
            ''' Since gettext entries are English-based, English is
                selected as a primary language.
            '''
            self.menu_url = 'https://www.multitran.com/m.exe?a=112&l1={}&l2={}&SHL=1'
            self.menu_url = self.menu_url.format (self.lang1
                                                 ,self.lang2
                                                 )
        else:
            sh.com.cancel(f)
    
    def set_values(self):
        self.Success = True
        self.ui_langs = [1,2,3,5,33]
        self.abbrs = []
        self.titles = []
        self.failed_titles = []
        self.menu_url = ''
        self.filew = '/tmp/subjects (abbr + full)'
        self.lang1 = 1
        self.lang2 = 2
        self.ui_lang = 1
        
    def _run(self):
        self.set_menu_url()
        self.get_menu()
        self.get_urls()
    
    def run_pass(self,lang1,lang2):
        f = '[MClient] plugins.multitrancom.utils.subjects.Subjects.run_pass'
        if self.Success:
            len_ = len(self.titles)
            self.lang1 = lang1
            self.lang2 = lang2
            self._run()
            delta = len(self.titles) - len_
            mes = _('Pass {}-{}: {} new titles')
            mes = mes.format(self.lang1,self.lang2,delta)
            sh.objs.get_mes(f,mes,True).show_info()
            print('================================================')
        else:
            sh.com.cancel(f)
    
    def loop(self):
        ''' Currently available interface languages:
            1  (English)
            2  (Russian)
            3  (German)
            5  (Spanish)
            33 (Ukranian)
        '''
        self.run_pass(1,1)
        self.run_pass(1,2)
        self.run_pass(2,2)
        self.run_pass(2,3)
        self.run_pass(3,3)
        self.run_pass(2,4)
        self.run_pass(4,4)
        self.run_pass(2,5)
        self.run_pass(5,5)
    
    def run(self):
        self.check()
        #cur
        #self.loop()
        self.run_pass(1,1)
        self.dump()
        #self.debug()



class Subjects2:
    
    def __init__(self):
        self.set_values()
    
    def reassign_rows(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.Subjects.reassign_rows'
        if self.Success:
            len_ = len(self.rows)
            self.rows = sorted(set(self.rows))
            delta = len_ - len(self.rows)
            sh.com.rep_deleted(f,delta)
        else:
            sh.com.cancel(f)
    
    def dump(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.Subjects.dump'
        if self.Success:
            text = '\n'.join(self.rows)
            sh.WriteTextFile(self.filew,True).write(text)
            sh.Launch(self.filew).launch_default()
        else:
            sh.com.cancel(f)
    
    def debug(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.Subjects.debug'
        if self.Success:
            nos = [i + 1 for i in range(len(self.mult))]
            rownos = []
            types = []
            texts = []
            urls = []
            for i in range(len(self.mult)):
                for block in self.mult[i]:
                    rownos.append(i)
                    types.append(block.type_)
                    texts.append(block.text)
                    urls.append(block.url)
            headers = (_('#'),_('ROW #'),_('TYPE'),_('TEXT'),'URL')
            iterable = [nos,rownos,types,texts,urls]
            mes = sh.FastTable (headers = headers
                               ,iterable = iterable
                               ).run()
            sh.com.run_fast_debug(f,mes)
        else:
            sh.com.cancel(f)
    
    def _get_title(self,url):
        match = re.match('.* title="(.*)',url)
        if match:
            title = match.group(1)
            title = title.replace(sh.lg.nbspace,' ')
            return title.strip()
        return ''
    
    def set_values(self):
        self.Success = True
        self.ui_langs = [1,2,3,5,33]
        self.abbrs = []
        self.titles = []
        self.failed_titles = []
        self.mult = []
        self.rows = []
        self.menu_url = ''
        self.filew = '/tmp/subjects (abbr + full)'
        self.lang1 = 1
        self.lang2 = 2
        self.ui_lang = 1
    
    def _fix_url(self,url):
        url = gt.com.fix_url(url)
        #TODO: Skip when 'gt.com.fix_url' is reworked
        what = '&SHL=\d+'
        with_ = '&SHL={}'.format(self.ui_lang)
        url = re.sub(what,with_,url)
        if not '&SHL=' in url:
            url += with_
        return url
    
    def get_subjects(self,search,url):
        f = '[MClient] plugins.multitrancom.utils.subjects.Subjects.get_subjects'
        blocks = []
        if self.Success:
            if search and url:
                url = self._fix_url(url)
                mes = _('Get "{}" at "{}"').format(search,url)
                sh.objs.get_mes(f,mes,True).show_debug()
                blocks = rn.Plugin().request (search = search
                                             ,url = url
                                             )
                blocks = [block for block in blocks \
                          if block.type_ == 'dic' and block.text.strip()
                         ]
                for block in blocks:
                    block.text = block.text.replace(sh.lg.nbspace,' ')
                    block.text = block.text.strip()
                return blocks
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
        return blocks
    
    def run(self):
        #url = 'https://www.multitran.com/m.exe?s=3D+printer&l1=1&l2=2'
        url = 'https://www.multitran.com/m.exe?s=printer&l1=1&l2=2'
        self.get_all_subjects(url)
        self.check_mult()
        self.reassign_mult()
        self.reassign_rows()
        #self.debug_mult()
        self.add()
        self.debug()
        #self.dump()
    
    def add(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.Subjects.add'
        if self.Success:
            count = 0
            for list_ in self.mult:
                row = []
                for block in list_:
                    #cur
                    #title = self._get_title(block.url)
                    #abbr = block.text
                    title = block.dicf
                    abbr = block.dic
                    if not title:
                        count += 1
                        title = _('Logic error!')
                    if not abbr:
                        count += 1
                        abbr = _('Logic error!')
                    row.append(title)
                    row.append(abbr)
                self.rows.append('\t'.join(row))
            if count:
                mes = _('{} errors').format(count)
                sh.objs.get_mes(f,mes,True).show_warning()
        else:
            sh.com.cancel(f)
    
    def reassign_mult(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.Subjects.reassign_mult'
        if self.Success:
            mult = []
            for i in range(len(self.mult[0])):
                row = []
                for list_ in self.mult:
                    row.append(list_[i])
                mult.append(row)
            self.mult = mult
        else:
            sh.com.cancel(f)
    
    def check_mult(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.Subjects.check_mult'
        if self.Success:
            if self.mult:
                lens = [len(list_) for list_ in self.mult]
                if len(set(lens)) != 1:
                    self.Success = False
                    mes = _('Wrong input data: "{}"!').format(lens)
                    sh.objs.get_mes(f,mes).show_warning()
            else:
                self.Success = False
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def get_all_subjects(self,url):
        f = '[MClient] plugins.multitrancom.utils.subjects.Subjects.get_all_subjects'
        if self.Success:
            for self.ui_lang in self.ui_langs:
                search = 'search (lang: {})'.format(self.ui_lang)
                self.mult.append(self.get_subjects(search,url))
            self.mult = [item for item in self.mult if item]
        else:
            sh.com.cancel(f)



class Compare:
    
    def __init__(self,url,Debug=False):
        self.Success = True
        self.ui_langs = [1,2,3,5,33]
        self.ipages = []
        self.match = ''
        self.Debug = Debug
        self.url = url
    
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
    
    def __init__(self,url,ui_lang,Debug=False):
        self.Success = True
        self.blocks = []
        self.rows = []
        self.subjects = {}
        self.url = url
        self.ui_lang = ui_lang
        self.Debug = Debug
    
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
                    text = ' '.join(texts)
                    hash_ = hash(text)
                    block = row[0]
                    self.subjects[hash_] = {'dic':block.dic
                                           ,'dicf':block.dicf
                                           ,'text':text
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
            search = 'search (lang: {})'.format(self.ui_lang)
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
    
    def process_blocks(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.EndPage.get_blocks'
        if self.Success:
            for block in self.blocks:
                block.text = block.text.replace(sh.lg.nbspace,' ')
                block.text = block.text.strip()
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
        # 10'' screen: 35 symbols
        mes = sh.FastTable (headers = headers
                           ,iterable = iterable
                           ,maxrow = 35
                           ).run()
        return f + ':\n' + mes
    
    def _debug_subjects(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.EndPage._debug_subjects'
        nos = [i + 1 for i in range(len(self.subjects.keys()))]
        dic = []
        dicf = []
        texts = []
        hashes = []
        for key in self.subjects.keys():
            hashes.append(key)
            dic.append(self.subjects[key]['dic'])
            dicf.append(self.subjects[key]['dicf'])
            texts.append(self.subjects[key]['text'])
        headers = (_('#'),_('DIC'),_('DICF'),_('TEXT'),_('HASH'))
        iterable = [nos,dic,dicf,texts,hashes]
        # 10'' screen: 35 symbols
        mes = sh.FastTable (headers = headers
                           ,iterable = iterable
                           ,maxrow = 35
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
        #TODO: do we really need this?
        #self.process_blocks()
        self.set_rows()
        self.set_hashes()
        self.debug()
        
