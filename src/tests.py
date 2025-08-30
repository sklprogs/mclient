#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.graphics.root.controller import ROOT
from skl_shared.graphics.debug.controller import DEBUG as shDEBUG
from skl_shared.config import Default, Schema, Local
from skl_shared.paths import Home, PDIR
from skl_shared.time import Timer
from skl_shared.text_file import Read, Write
from skl_shared.launch import Launch
from skl_shared.table import Table
from skl_shared.logic import Text

from config import CONFIG

DEBUG = True

SEARCH = 'computer'
URL = 'https://www.multitran.com/m.exe?ll1=1&ll2=2&s=chicken+wing&l2=2'
HTM_FILE = '/home/pete/docs/mclient_tests/multitrancom (saved in browser)/fill (2025-01-31).htm'
#SEARCH = 'chicken wing pork friday coding style'


class Wrap:
    
    def run_multitrancom(self):
        f = '[MClient] tests.Wrap.run_multitrancom'
        import articles as ARTICLES
        # Do not change import style - we already have there Get, Tags, etc.
        import plugins.multitrancom.cleanup as cu
        import plugins.multitrancom.tags as tg
        import plugins.multitrancom.elems as el
        import cells as cl
        
        text = Read(HTM_FILE).get()
        timer = Timer(f)
        timer.start()
        text = cu.CleanUp(text).run()
        blocks = tg.Tags(text=text, maxrows=0).run()
        cells = el.Elems(blocks).run()
        
        ARTICLES.add(SEARCH, URL, cells)
        
        cells = cl.Omit(cells).run()
        cells = cl.Prioritize(cells).run()
        cells = cl.View(cells).run()
        iwrap = cl.Wrap(cells)
        iwrap.run()
        timer.end()
        return iwrap.debug()



class Prioritize:
    
    def run_multitrancom(self):
        f = '[MClient] tests.Prioritize.run_multitrancom'
        import logic as lg
        import plugins.multitrancom.cleanup as cu
        import plugins.multitrancom.tags as tg
        import plugins.multitrancom.elems as el
        import cells as cl
        from subjects import SUBJECTS
        
        text = Read(HTM_FILE).get()
        timer = Timer(f)
        timer.start()
        text = cu.CleanUp(text).run()
        blocks = tg.Tags (text = text
                         ,maxrows = 0
                         ).run()
        ielems = el.Elems(blocks)
        cells = ielems.run()
        
        ''' #FIX: For some reason, lg.objs.get_plugins().get_article_subjects()
            is empty.
        '''
        pairs = ielems.art_subj
        if not pairs:
            rep.empty(f)
            return
        SUBJECTS.reset(pairs)
        
        ARTICLES.add(search = SEARCH
                    ,url = URL
                    ,cells = cells
                    ,subjf = SUBJECTS.article
                    ,blocked = SUBJECTS.block
                    ,prioritized = SUBJECTS.prior)

        cells = cl.Omit(cells).run()
        iprior = cl.Prioritize(cells)
        iprior.run()
        timer.end()
        return iprior.debug()



class View:
    
    def run_stardict(self):
        import logic as lg
        import plugins.stardict.cleanup as cu
        import plugins.stardict.tags as tg
        import plugins.stardict.elems as el
        import cells as cl
        file = '/home/pete/docs/mclient_tests/stardict/EnRu full cut.txt'
        text = Read(file).get()
        text = cu.CleanUp(text).run()
        blocks = tg.Tags(text).run()
        cells = el.Elems(blocks).run()
        ARTICLES.add(SEARCH, URL, cells)
        cells = cl.Omit(cells).run()
        cells = cl.Prioritize(cells).run()
        iview = cl.View(cells)
        iview.run()
        return iview.debug()
    
    def run_multitrancom(self):
        f = '[MClient] tests.View.run_multitrancom'
        import logic as lg
        import plugins.multitrancom.cleanup as cu
        import plugins.multitrancom.tags as tg
        import plugins.multitrancom.elems as el
        import cells as cl
        
        text = Read(HTM_FILE).get()
        timer = Timer(f)
        timer.start()
        text = cu.CleanUp(text).run()
        blocks = tg.Tags(text=text, maxrows=0).run()
        cells = el.Elems(blocks).run()
        
        ARTICLES.add(SEARCH, URL, cells)
        
        cells = cl.Omit(cells).run()
        cells = cl.Prioritize(cells).run()
        iview = cl.View(cells)
        iview.run()
        timer.end()
        return iview.debug()
    
    def run_dsl(self):
        f = '[MClient] tests.View.run_dsl'
        import logic as lg
        import plugins.dsl.get as gt
        import plugins.dsl.cleanup as cu
        import plugins.dsl.tags as tg
        import plugins.dsl.elems as el
        import cells as cl
        
        blocks = []
        
        timer = Timer(f)
        timer.start()
        gt.PATH = Home('mclient').add_config('dics')
        articles = gt.Get(SEARCH).run()
        for iarticle in articles:
            code = cu.CleanUp(iarticle.code).run()
            code = cu.TagLike(code).run()
            blocks += tg.Tags(code = code
                             ,Debug = DEBUG
                             ,maxrows = 0
                             ,dicname = iarticle.dic).run()
        cells = el.Elems(blocks).run()
        
        ARTICLES.add(SEARCH, URL, cells)
        
        cells = cl.Omit(cells).run()
        cells = cl.Prioritize(cells).run()
        iview = cl.View(cells)
        iview.run()
        timer.end()
        return iview.debug()



class Elems:
    
    def run_multitrandem(self):
        import plugins.multitrandem.get as gt
        import plugins.multitrandem.tags as tg
        import plugins.multitrandem.elems as el
        gt.PATH = Home('mclient').add_config('dics')
        iget = gt.Get(SEARCH)
        chunks = iget.run()
        if not chunks:
            chunks = []
        blocks = []
        for i in range(len(chunks)):
            add = tg.Tags(chunks[i], i).run()
            if add:
                blocks += add
        ielems = el.Elems(blocks = blocks
                         ,abbr = None
                         ,langs = gt.objs.get_all_dics().get_langs()
                         ,search = SEARCH)
        ielems.run()
        return ielems.debug()
    
    def run_stardict(self):
        import plugins.stardict.cleanup as cu
        import plugins.stardict.tags as tg
        import plugins.stardict.elems as el
        #file = '/home/pete/docs/mclient_tests/stardict/EnRu full cut.txt'
        file = '/home/pete/docs/mclient_tests/stardict/English-Russian full dictionary - product.txt'
        text = Read(file).get()
        text = cu.CleanUp(text).run()
        blocks = tg.Tags(text).run()
        ielems = el.Elems(blocks)
        ielems.run()
        return ielems.debug()
    
    def run_fora(self):
        f = '[MClient] tests.Elems.run_fora'
        from plugins.fora.run import Plugin
        from plugins.fora.stardictx.elems import Elems
        cells = Plugin().request(SEARCH)
        if not cells:
            rep.lazy(f)
            return
        ielems = Elems(cells[-1].blocks)
        ielems.cells = cells
        return ielems.debug()
    
    def run_fora_stardictx(self):
        f = '[MClient] tests.Elems.run_fora_stardictx'
        from plugins.fora.get import ALL_DICS
        from plugins.fora.stardictx.tags import Tags
        from plugins.fora.stardictx.elems import Elems
        article = ALL_DICS.search(SEARCH)
        if not article:
            rep.empty(f)
            return
        blocks = Tags(article).run()
        ielems = Elems(blocks)
        ielems.run()
        return ielems.debug()
    
    def run_fora_dsl(self):
        f = '[MClient] tests.Elems.run_fora_dsl'
        from plugins.fora.get import ALL_DICS
        from plugins.fora.dsl.cleanup import CleanUp
        from plugins.fora.dsl.tags import Tags
        from plugins.fora.dsl.elems import Elems
        article = ALL_DICS.search(SEARCH)
        if not article:
            rep.empty(f)
            return
        article = CleanUp(article).run()
        blocks = Tags(article).run()
        ielems = Elems(blocks)
        ielems.run()
        return ielems.debug()
    
    def run_dsl(self):
        import plugins.dsl.cleanup as cu
        import plugins.dsl.get as gt
        import plugins.dsl.tags as tg
        import plugins.dsl.elems as el
        blocks = []
        htm = []
        articles = gt.Get(SEARCH).run()
        for iarticle in articles:
            htm.append(iarticle.code)
            code = cu.CleanUp(iarticle.code).run()
            blocks += tg.Tags(code).run()
        htm = '\n'.join(htm)
        ielems = el.Elems(blocks)
        blocks = ielems.run()
        return ielems.debug()
    
    def run_multitrancom(self):
        f = '[MClient] tests.Elems.run_multitrancom'
        from skl_shared.text_file import Read
        from skl_shared.time import Timer
        from plugins.multitrancom.cleanup import CleanUp
        from plugins.multitrancom.tags import Tags
        from plugins.multitrancom.elems import Elems
        text = Read(HTM_FILE).get()
        timer = Timer(f)
        timer.start()
        text = CleanUp(text).run()
        blocks = Tags(text = text
                     ,maxrows = 0).run()
        ielems = Elems(blocks)
        ielems.run()
        timer.end()
        return ielems.debug()



class Offline:
    
    def __init__(self):
        self.maxrows = 0
    
    def run_multitrancom(self):
        import plugins.multitrancom.cleanup as cu
        import plugins.multitrancom.tags as tg
        import plugins.multitrancom.elems as el
        self.htm = Read(HTM_FILE).get()
        self.text = cu.CleanUp(self.htm).run()
        itags = tg.Tags(text = self.text
                       ,Debug = DEBUG
                       ,maxrows = self.maxrows)
        blocks = itags.run()
        ielems = el.Elems(blocks = blocks
                         ,Debug = DEBUG
                         ,maxrows = self.maxrows)
        ielems.run()
        return ielems.debug()



class Subjects:
    
    def __init__(self):
        from subjects import SUBJECTS
        self.report = []
        self.isubj = SUBJECTS
    
    def create(self):
        pairs = {'общ.': 'Общая лексика', 'комп.': 'Компьютеры'
                ,'Майкр.': 'Майкрософт', 'вульг.': 'Вульгаризм'
                ,'разг., сл.': 'Разговорная лексика, Сленг'
                ,'сокр., воен., авиац.': 'Сокращение, Военный термин, Авиация'
                ,'тлф.': 'Телефония', 'устн.': 'Устная речь'
                ,'СМИ.': 'Средства массовой информации'}
        self.isubj.reset(pairs)
        self.report.append(self.isubj.debug())
    
    def expand(self, subj):
        f = '[MClient] tests.Subjects.expand'
        sub = self.isubj.expand(subj)
        self.report.append(f'{f}:\n{sub}')
    
    def is_phrase_blocked(self, subject):
        f = '[MClient] tests.Subjects.is_phrase_blocked'
        if self.isubj.is_phrase_blocked(subject):
            sub = _('Phrase "{}" is blocked').format(subject)
        else:
            sub = _('Phrase "{}" is NOT blocked').format(subject)
        self.report.append(f'{f}:\n{sub}')
    
    def is_phrase_prior(self, subject):
        f = '[MClient] tests.Subjects.is_phrase_prior'
        if self.isubj.is_phrase_prior(subject):
            sub = _('Phrase "{}" is prioritized').format(subject)
        else:
            sub = _('Phrase "{}" is NOT prioritized').format(subject)
        self.report.append(f'{f}:\n{sub}')
    
    def is_blocked(self, subject):
        f = '[MClient] tests.Subjects.is_blocked'
        if self.isubj.is_blocked(subject):
            sub = _('Subject "{}" is blocked').format(subject)
        else:
            sub = _('Subject "{}" is NOT blocked').format(subject)
        self.report.append(f'{f}:\n{sub}')
    
    def is_prioritized(self, subject):
        f = '[MClient] tests.Subjects.is_prioritized'
        if self.isubj.is_prioritized(subject):
            sub = _('Subject "{}" is prioritized').format(subject)
        else:
            sub = _('Subject "{}" is NOT prioritized').format(subject)
        self.report.append(f'{f}:\n{sub}')
    
    def run(self):
        self.create()
        self.is_phrase_blocked('Сленг')
        self.is_phrase_prior('Майкрософт')
        self.is_blocked('разг., сл.')
        self.is_prioritized('общ.')
        self.expand('разг., сл.')
        return '\n\n'.join(self.report)



class Get:
    
    def decode_indexes(self, indexes):
        from plugins.fora.get import Index
        iindex = Index('/home/pete/.config/mclient/dics/Fora/dict pl-ru')
        for i in range(len(indexes)):
            indexes[i][0] = iindex.decode(indexes[i][0])
            indexes[i][1] = iindex.decode(indexes[i][1])
        return indexes
    
    def run_fora_many_matches(self):
        from plugins.fora.get import ALL_DICS
        articles = []
        # Multiple occurrences of 'aprobować' (and many others) in 'dict pl-ru'
        indexes = [['JbY', '8'], ['JcV', 'BK'], ['Jdg', 'BA']]
        indexes = self.decode_indexes(indexes)
        for index in indexes:
            for ifora in ALL_DICS.dics:
                article = ifora.dic.get(index)
                if article:
                    articles.append(article)
        return '\n\n'.join(articles)
    
    def run_fora(self):
        import os
        from plugins.fora.get import Fora
        dic = 'ComputersEnRu'
        folder = '/home/pete/.config/mclient/dics/Fora'
        folder = os.path.join(folder, dic)
        return Fora(folder).search('account')
    
    def run_dsl(self):
        from plugins.dsl.get import Get
        iget = Get('account')
        iget.run()
        return iget.debug()
    
    def run_multitrandem(self):
        f = '[MClient] tests.Get.run_multitrandem'
        from manager import PLUGINS
        import plugins.multitrandem.get as gt
        PLUGINS.Debug = False
        PLUGINS.maxrows = 1000
        result = gt.Get(SEARCH).run()
        if not result:
            rep.empty(f)
            return
        for i in range(len(result)):
            result[i] = result[i].decode(gt.CODING)
        return str(result)
    
    def run_multitrancom(self):
        f = '[MClient] tests.Get.run_multitrancom'
        import plugins.multitrancom.get as gt
        #url = 'https://www.multitran.com/m.exe?a=3&sc=8&s=%D1%81%D0%B8%D0%BC%D0%BF%D1%82%D0%BE%D0%BC&l1=2&l2=1&SHL=2'
        #search = 'Медицина'
        url = 'https://www.multitran.com/m.exe?s=working%20documentation&l1=1&l2=2&SHL=2'
        search = 'working documentation'
        timer = Timer(f)
        timer.start()
        result = gt.Get(search=search, url=url).run()
        timer.end()
        filename = f'{search} ({Time().get_date()}).html'
        file = Home().add('docs', 'mclient_tests'
                         ,'multitrancom (saved with Get.get)', filename)
        Write(file).write(result)
        Launch(file).launch_default()
    
    def run_stardict(self):
        f = '[MClient] tests.Get.run_stardict'
        from manager import PLUGINS
        import plugins.stardict.get
        PLUGINS.Debug = False
        PLUGINS.maxrows = 1000
        search = 'abstersion'
        timer = Timer(f)
        timer.start()
        result = plugins.stardict.get.Get(search).run()
        timer.end()
        return result



class Tags:
    
    def run_fora_stardictx(self):
        f = '[MClient] tests.Tags.run_fora_stardictx'
        from plugins.fora.get import ALL_DICS
        from plugins.fora.stardictx.cleanup import CleanUp
        from plugins.fora.stardictx.tags import Tags
        article = ALL_DICS.search(SEARCH)
        if not article:
            rep.empty(f)
            return
        article = CleanUp(article).run()
        itags = Tags(article)
        itags.run()
        return itags.debug()
    
    def run_fora_dsl(self):
        f = '[MClient] tests.Tags.run_fora_dsl'
        from plugins.fora.get import ALL_DICS
        from plugins.fora.dsl.cleanup import CleanUp
        from plugins.fora.dsl.tags import Tags
        article = ALL_DICS.search(SEARCH)
        if not article:
            rep.empty(f)
            return
        article = CleanUp(article).run()
        itags = Tags(article)
        itags.run()
        return itags.debug()
    
    def run_multitrandem(self):
        f = '[MClient] tests.Tags.run_multitrandem'
        from manager import PLUGINS
        import plugins.multitrandem.get as gt
        import plugins.multitrandem.tags as tg
        PLUGINS.Debug = False
        PLUGINS.maxrows = 1000
        chunks = gt.Get(SEARCH).run()
        if not chunks:
            rep.empty(f)
            return
        tags = []
        blocks = []
        for chunk in chunks:
            itags = tg.Tags(chunk)
            itags.run()
            tags += itags.tags
            blocks += itags.blocks
        itags.tags = tags
        itags.blocks = blocks
        return itags.debug()
    
    def run_dsl(self):
        import plugins.dsl.get
        import plugins.dsl.cleanup
        import plugins.dsl.tags
        plugins.dsl.get.PATH = Home('mclient').add_config('dics')
        articles = plugins.dsl.get.Get('account balance').run()
        blocks = []
        debug = []
        for iarticle in articles:
            code = plugins.dsl.cleanup.CleanUp(iarticle.code).run()
            code = plugins.dsl.cleanup.TagLike(code).run()
            itags = plugins.dsl.tags.Tags(code = code
                                         ,Debug = DEBUG
                                         ,maxrows = 0
                                         ,dicname = iarticle.dic)
            blocks += itags.run()
            debug.append(itags.debug())
        return '\n'.join(debug)
    
    def analyze_tag(self):
        import plugins.multitrancom.tags as tg
        #tag = '<tr><td class="subj" width="1"><a href="https://www.multitran.com/m.exe?a=110&amp;l1=2&amp;l2=1&amp;s=%D1%82%D1%80%D0%BE%D1%81&amp;sc=371" title="Автоматика">автомат.'
        #tag = '''<tr><td class="subj" width="1"><a href="https://www.multitran.com/m.exe?a=110&amp;l1=2&amp;l2=1&amp;s=%D1%82%D1%80%D0%BE%D1%81&amp;sc=0" title="Общая лексика">общ.'''
        tag = '<tr><td class="subj" width="1"><a href="https://www.multitran.com/m.exe?a=110&amp;l1=2&amp;l2=1&amp;s=%D1%82%D1%80%D0%BE%D1%81&amp;sc=134" title="Электроника">эл.'
        itag = tg.AnalyzeTag(tag)
        itag.run()
        itag.debug()
    
    def run_stardict(self):
        import plugins.stardict.cleanup as cu
        import plugins.stardict.tags as tg
        file = '/home/pete/docs/mclient_tests/stardict/English-Russian full dictionary - abstersion.txt'
        text = Read(file).get()
        text = cu.CleanUp(text).run()
        itags = tg.Tags(text)
        '''
        itags = tg.Tags(text = text
                       ,Debug = DEBUG
                       ,maxrows = 0)
        '''
        itags.run()
        return itags.debug()
    
    def run_multitrancom(self):
        from skl_shared.text_file import Read
        from plugins.multitrancom.cleanup import CleanUp
        from plugins.multitrancom.tags import Tags
        text = Read(HTM_FILE).get()
        text = CleanUp(text).run()
        itags = Tags(text = text
                    ,Debug = DEBUG
                    ,maxrows = 0)
        itags.run()
        return itags.debug()



class Plugin:
    
    def run_fora(self):
        from plugins.fora.run import Plugin
        search = 'about'
        iplug = Plugin(Debug=DEBUG)
        iplug.request(search=search)
    
    def run_multitrandem(self):
        import plugins.multitrandem.get
        import plugins.multitrandem.run as mb
        #search = 'Kafir'
        search = 'abasin'
        #search = 'a posteriori'
        #search = 'abed'
        #search = 'accommodation coefficient'
        #search = 'according'
        #search = 'фабричный корпус'
        #search = 'build market'
        #search = 'bunching device'
        #search = 'valve rocker shank'
        # пласт, характеризуемый определённой скоростью
        #search = 'velocity bed'
        #отравление хинной коркой и её алкалоидами = quininism
        url = ''
        
        ''' #NOTE: This is a standard 'dics' folder, do not include subfolders
            here.
        '''
        plugins.multitrandem.get.PATH = '/home/pete/.config/mclient/dics'
        iplug = mb.Plugin(Debug=DEBUG, maxrows=150)
        
        blocks = iplug.request(url=url, search=search)
        if not blocks:
            blocks = []
        for i in range(len(blocks)):
            mes = f'{i}: {blocks[i].type}: "{blocks[i].text}"'
            print(mes)
    
    def run_stardict(self):
        import plugins.stardict.run as sr
        search = 'about'
        iplug = sr.Plugin(Debug=DEBUG)
        iplug.request(search=search)
    
    def run_dsl(self):
        f = '[MClient] tests.Plugin.run_dsl'
        import plugins.dsl.get
        import plugins.dsl.run as dr
        plugins.dsl.get.DEBUG = DEBUG
        plugins.dsl.get.PATH = Home('mclient').add_config('dics')
        #search = 'компьютер'
        #search = 'computer'
        #search = 'bunker'
        #search = 'accounting'
        search = 'gear'
        iplug = dr.Plugin(Debug=DEBUG)
        iplug.request(search=search)
        mes = [f'{f}:']
        sub = _('Number of blocks: {}').format(len(iplug.blocks))
        mes.append(sub)
        sub = _('Web-page:')
        mes.append(sub)
        sub = iplug.get_htm()
        mes.append(sub)
        sub = _('Text:')
        mes.append(sub)
        sub = iplug.get_text()
        mes.append(sub)
        return '\n'.join(mes)
    
    def run_multitrancom(self):
        import plugins.multitrancom.run as mc
        #url = 'https://www.multitran.com/m.exe?s=memory%20pressure&l1=2&l2=1&SHL=2'
        #search = 'memory pressure'
        #url = 'https://www.multitran.com/m.exe?s=nucleoside%20reverse%20transcriptase%20inhibitors&l1=2&l2=1&SHL=2'
        #search = 'nucleoside reverse transcriptase inhibitors'
        #url = 'https://www.multitran.com/m.exe?s=%D0%BD%D1%83%D0%BA%D0%BB%D0%B5%D0%B8%D0%BD%D0%BE%D0%B2%D1%8B%D0%B9&l1=2&l2=1&SHL=2'
        #search = 'нуклеиновый'
        #url = 'https://www.multitran.com/m.exe?a=3&l1=2&l2=1&s=%D0%B2%2B%D1%8F%D0%B1%D0%BB%D0%BE%D1%87%D0%BA%D0%BE&SHL=2'
        #search = '47 фраз'
        #url = 'https://www.multitran.com/m.exe?s=Antiquity&l1=1&l2=2&SHL=2'
        #search = 'Antiquity'
        #url = 'https://www.multitran.com/m.exe?s=hello&l1=1&l2=2&SHL=2'
        #search = 'hello'
        #url = 'https://www.multitran.com/m.exe?s=set&l1=1&l2=2&SHL=2'
        #search = 'set'
        #url = 'https://www.multitran.com/m.exe?a=3&l1=1&l2=2&s=hello&SHL=2'
        #search = '97 фраз в 16 тематиках'
        #url = 'https://www.multitran.com/m.exe?a=3&l1=1&l2=2&s=icon&SHL=2'
        #search = 'icon'
        #url = 'https://www.multitran.com/m.exe?a=3&l1=1&l2=2&s=heaven+and+hell+bond&SHL=2'
        #search = 'heaven and hell bond'
        #url = 'https://www.multitran.com/m.exe?s=%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B0&l1=1&l2=2&SHL=2'
        #search = 'задача'
        #url = 'https://www.multitran.com/m.exe?s=ntthing&l1=1&l2=2&SHL=2'
        #search = 'ntthing'
        #url = 'https://www.multitran.com/m.exe?s=question&l1=2&l2=1&SHL=2'
        #search = 'question'
        #url = 'https://www.multitran.com/m.exe?s=%D1%86%D0%B5%D0%BF%D1%8C:+%D0%BF%D1%80%D0%BE%D0%B2%D0%BE%D0%B4&l1=2&l2=1'
        #search = 'цепь: провод'
        #url = 'https://www.multitran.com/m.exe?s=%D0%B2%D1%81%D0%BF%D0%BE%D0%BC%D0%B8%D0%BD%D0%B0%D1%82%D1%8C&l1=2&l2=1&SHL=2'
        #search = 'вспоминать'
        url = 'https://www.multitran.com/m.exe?s=reticulated+siren&l1=1&l2=10000&SHL=33'
        search = 'reticulated siren'
        
        mc.Plugin(Debug = DEBUG
                 ,maxrows = 0).request(url = url
                                      ,search = search)



class Commands:
    
    def get_fixed_urls(self):
        f = '[MClient] tests.Commands.get_fixed_urls'
        import json
        import plugins.multitrancom.cleanup as cu
        import plugins.multitrancom.tags as tg
        import plugins.multitrancom.elems as el
        text = Read(HTM_FILE).get()
        text = cu.CleanUp(text).run()
        blocks = tg.Tags(text=text, maxrows=0).run()
        ielems = el.Elems(blocks)
        ielems.run()
        mes = json.dumps(ielems.fixed_urls, ensure_ascii=False, indent=4)
        return mes
    
    def get_all_subjects(self):
        import plugins.multitrancom.subjects as sj
        return sj.objs.get_subjects().dump()
    
    def run_suggest(self):
        import suggest.controller as sg
        lst = []
        for i in range(20):
            lst.append(f'item {i+1}')
        isuggest = sg.Suggest()
        isuggest.fill(lst)
        isuggest.go_end()
        isuggest.set_width(96)
        return isuggest
    
    def get_priority(self):
        f = '[MClient] tests.Commands.get_priority'
        from manager import PLUGINS
        from articles import ARTICLES
        from subjects import SUBJECTS
        #NOTE: the article must comprise example subjects to be expanded
        search = 'code'
        url = 'https://www.multitran.com/m.exe?s=code&l1=2&l2=1&SHL=2'
        cells = PLUGINS.request(search=search, url=url)
        ARTICLES.add(search=search, url=url, cells=cells)
        mes = []
        sub = f'{f}:'
        mes.append(sub)
        mes.append(_('Prioritized subjects:'))
        sub = '; '.join(CONFIG.new['subjects']['prioritized'])
        mes.append(sub)
        mes.append('')
        subject = 'тест., ИТ., Gruzovik, прогр.'
        sub = _('Subject: "{}"').format(subject)
        mes.append(sub)
        priority = SUBJECTS.get_priority(subject)
        sub = _('Highest priority (ascending order): {}').format(priority)
        mes.append(sub)
        mes.append('')
        sub = _('Details:')
        mes.append(sub)
        priorities = []
        parts = subject.split(', ')
        for part in parts:
            priorities.append(isubj.get_priority(part))
        parts = [f'"{part}"' for part in parts]
        sub = Table(headers = (_('SUBJECT'), _('PRIORITY'))
                   ,iterable = [parts, priorities]).run()
        mes.append(sub)
        return '\n'.join(mes)
    
    def run_article_subjects(self):
        f = '[MClient] tests.Commands.run_article_subjects'
        from manager import PLUGINS
        from articles import ARTICLES
        search = 'set'
        # SHL should correspond to locale
        url = 'https://www.multitran.com/m.exe?s=set&l1=2&l2=1'
        cells = PLUGINS.request(search=search, url=url)
        ARTICLES.add(search=search, url=url, cells=cells)
        subjects = ARTICLES.get_subjects()
        if not subjects:
            rep.empty(f)
            return
        shorts = []
        fulls = []
        for short in subjects:
            shorts.append(short)
            fulls.append(subjects[short])
        mes = Table(headers = (_('SHORT'), _('FULL'))
                   ,iterable = [shorts, fulls]
                   ,maxrow = 70).run()
        return mes
    
    def run_prior(self):
        import config as cf
        import mclient as mc
        return mc.Priorities()
    
    def run_prior_contr(self):
        import prior_block.priorities.controller as pr
        iprior = pr.Priorities()
        dic1 = {'Общая лексика': {}, 'Компьютеры': {'Компьютеры': {}, 'Майкрософт': {}, 'Программирование': {}, 'Информатика': {}}}
        iprior.fill(dic1, dic1)
        iprior.show()
        return iprior
    
    def run_popup(self):
        import popup.controller as pp
        ipopup = pp.Popup()
        file = PDIR.add('..', 'resources', 'third parties.txt')
        text = Read(file).get()
        text = Text(text, True).delete_line_breaks() * 10
        ipopup.fill(text)
        return ipopup
    
    def run_font_limits(self):
        f = '[MClient] tests.Commands.run_font_limits'
        from font_limits.controller import FontLimits
        from skl_shared.time import Timer
        text = 'Раз, два, три, четыре, пять - вышел зайчик погулять'
        ilimits = FontLimits(family = CONFIG.new['terms']['font']['family']
                            ,size = CONFIG.new['terms']['font']['size']
                            ,Bold = False
                            ,Italic = False)
        timer = Timer(f)
        timer.start()
        ilimits.set_text(text)
        ilimits.get_space()
        timer.end()
    
    def run_save(self):
        import save.controller as sv
        return sv.Save()
    
    def run_settings(self):
        import settings.controller as st
        return st.Settings()
    
    def run_history(self):
        import mclient as mc
        ihis = mc.History()
        ihis.add()
        ihis.add()
        ihis.add()
        ihis.add()
        return ihis
    
    def run_welcome(self):
        import mclient as mc
        iwelcome = mc.Welcome(mc.About().get_product())
        iwelcome.reset()
        return iwelcome
    
    def run_history_contr(self):
        import history.controller as hs
        ihis = hs.History()
        table = [['1', _('Russian'), _('English'), 'start']
                ,['2', _('Russian'), _('English'), 'hello']
                ,['3', _('English'), _('Russian'), 'bye']
                ,['4', _('English'), _('Russian'), 'fourth']
                ,['5', _('English'), _('Russian'), 'fifth']]
        ihis.fill_model(table)
        # The model is updated entirely each time, but still this is fast
        count = 0
        for i in range(100):
            count += 1
            ihis.add_row(str(count), 'Main', _('English'), _('Russian'), 'start')
            count += 1
            ihis.add_row(str(count), 'Main', _('Russian'), _('English'), 'hello')
            count += 1
            ihis.add_row(str(count), 'Main', _('French'), _('Esperanto'), 'bye')
            count += 1
            ihis.add_row(str(count), 'Main', _('English'), _('Russian'), 'end')
        return ihis
    
    def run_symbols(self):
        import symbols.controller as sm
        sym = sm.Symbols()
        sym.show()
    
    def get_column_width(self):
        f = '[MClient] tests.Commands.get_column_width'
        import logic as lg
        #CONFIG.new['columns']['num'] = 0
        mes = f'"{lg.com.get_column_width()}%"'
        Message(f, mes).show_debug()
    
    def check_width(self):
        import mclient as mc
        file = '/home/pete/tmp/frame rate.htm'
        #file = '/tmp/f.htm'
        code = Read(file).get()
        mc.objs.get_webframe().fill(code)
        mc.objs.webframe.show()
    
    def get_subjects_wo_majors(self):
        ''' Get subjects not united by a major subject. This is not an error
            and can be witnessed sometimes at multitran.com.
        '''
        f = '[MClient] tests.Commands.get_subjects_wo_majors'
        import plugins.multitrancom.subjects as sj
        titles = []
        for key in sj.SUBJECTS.keys():
            if not sj.SUBJECTS[key]['major_en'] \
            and sj.SUBJECTS[key]['Single']:
                titles.append(sj.SUBJECTS[key]['en']['title'])
        titles = sorted(set(titles))
        if titles:
            mes = '\n'.join(titles)
            shDEBUG.reset(f, mes)
            shDEBUG.show()
        else:
            rep.lazy(f)
    
    def get_modified_subjects(self):
        f = '[MClient] tests.Commands.get_modified_subjects'
        import plugins.multitrancom.subjects as sj
        titles = []
        for key in sj.SUBJECTS.keys():
            if sj.SUBJECTS[key]['Modified']:
                titles.append(sj.SUBJECTS[key]['ru']['title'])
        titles.sort()
        mes = '\n'.join(titles)
        shDEBUG.reset(f, mes)
        shDEBUG.show()
    
    def get_majors_en(self):
        f = '[MClient] tests.Commands.get_majors_en'
        import plugins.multitrancom.subjects as sj
        groups = []
        shorts = []
        titles = []
        for key in sj.SUBJECTS.keys():
            if sj.SUBJECTS[key]['Major']:
                groups.append(sj.SUBJECTS[key]['major_en'])
                shorts.append(sj.SUBJECTS[key]['en']['short'])
                titles.append(sj.SUBJECTS[key]['en']['title'])
        nos = [i + 1 for i in range(len(groups))]
        headers = (_('#'), _('MAJOR (EN)'), _('SHORT'), _('TITLE'))
        iterable = [nos, groups, shorts, titles]
        mes = Table(iterable = iterable
                   ,headers = headers
                   ,maxrow = 30).run()
        shDEBUG.reset(f, mes)
        shDEBUG.show()
    
    def get_majors(self):
        import plugins.multitrancom.subjects as sj
        print(sj.objs.get_subjects().get_majors())
    
    def run_speech(self):
        import plugins.multitrancom.speech as sp
        # ru_RU locale is required
        short = 'прил.'
        full = sp.objs.get_speech().find(short)
        mes = f'"{short}" -> "{full}"'
        return mes
    
    def edit_priorities(self):
        from manager import PLUGINS
        import mclient as mc
        #TODO: Rework lg.objs.get_order
        mc.objs.get_priorities().reset(lst1 = lg.objs.get_order().priorlst
                                      ,lst2 = PLUGINS.get_subjects()
                                      ,art_subjects = []
                                      ,majors = PLUGINS.get_majors())
        mc.objs.priorities.show()
    
    def edit_blacklist(self):
        from manager import PLUGINS
        import mclient as mc
        #TODO: Rework lg.objs.get_order
        mc.objs.get_blacklist().reset(lst1 = lg.objs.get_order().blacklst
                                     ,lst2 = PLUGINS.get_subjects()
                                     ,art_subjects = []
                                     ,majors = PLUGINS.get_majors())
        mc.objs.blacklist.show()
    
    def show_about(self):
        from mclient import About
        About().show()
    
    def get_nonpairs(self):
        ''' Get languages that are not supported by multitran.com for
            both directions.
        '''
        f = '[MClient] tests.Commands.get_nonpairs'
        import plugins.multitrancom.pairs as pairs
        lst = []
        for lang in pairs.LANGS:
            pairs1 = pairs.objs.get_pairs().get_pairs1(lang)
            pairs2 = pairs.objs.get_pairs().get_pairs2(lang)
            if not pairs1:
                pairs1 = []
            if not pairs2:
                pairs2 = []
            if pairs1 != pairs2:
                for xlang in pairs1:
                    if xlang not in pairs2:
                        lst.append(f'{xlang}-{lang}')
                for xlang in pairs2:
                    if xlang not in pairs1:
                        lst.append(f'{lang}-{xlang}')
        lst = list(set(lst))
        lst.sort()
        mes = _('The following pairs are not supported:\n{}')
        mes = mes.format(lst)
        Message(f, mes).show_info()
    
    def compare_elems(self):
        f = '[MClient] tests.Commands.compare_elems'
        import plugins.multitran.elems as el
        data1 = []
        data2 = []
        # Create blocks
        #1 #1
        block = list(Block().dump())
        block[2] = 'Общая лексика' # DIC
        block[30] = 'общ.'         # DICF
        block[7] = 'term'          # TYPE
        block[8] = 'hello'         # TEXT
        data1.append(block)
        #1 #2
        block = list(Block().dump())
        block[2] = 'Общая лексика' # DIC
        block[30] = 'общ.'         # DICF
        block[7] = 'comment'       # TYPE
        block[8] = 'yes'           # TEXT
        data1.append(block)
        #1 #3
        block = list(Block().dump())
        block[2] = 'Общая лексика' # DIC
        block[30] = 'общ.'         # DICF
        block[7] = 'term'          # TYPE
        block[8] = 'goodbye'       # TEXT
        data1.append(block)
        #2 #1
        block = list(Block().dump())
        block[2] = 'Общая лексика' # DIC
        block[30] = 'общ.'         # DICF
        block[7] = 'term'          # TYPE
        block[8] = 'goodbye'       # TEXT
        data2.append(block)
        #2 #2
        block = list(Block().dump())
        block[2] = 'Физиология'    # DIC
        block[30] = 'физиол.'      # DICF
        block[7] = 'comment'       # TYPE
        block[8] = 'yes'           # TEXT
        data2.append(block)
        #2 #3
        block = list(Block().dump())
        block[2] = 'Общая лексика' # DIC
        block[30] = 'общ.'         # DICF
        block[7] = 'term'          # TYPE
        block[8] = 'hello'         # TEXT
        data2.append(block)
        # Compare
        data = el.Elems(data1, data2).run()
        data = [str(item) for item in data]
        shDEBUG.reset(f, '\n'.join(data))
        shDEBUG.show()
    
    def request(self):
        from manager import PLUGINS
        f = '[MClient] tests.Commands.request'
        source = _('Multitran')
        pair = 'DEU <=> RUS'
        search = 'ernährung'
        mes = _('Source: "{}"; pair: "{}"; search: "{}"')
        mes = mes.format(source, pair, search)
        PLUGINS.set(source)
        PLUGINS.set_pair(pair)
        Message(f, mes).show_info()
        data = PLUGINS.request(search=search, url='')
        if not data:
            rep.empty(f)
            return
        shDEBUG.reset(f, data)
        shDEBUG.show()
    
    def get_url(self):
        from manager import PLUGINS
        f = '[MClient] tests.Commands.get_url'
        source = 'multitran.com'
        pair = 'RUS <=> XAL'
        search = 'До свидания!'
        mes = 'Source: "{}"; pair: "{}"; search: "{}"'
        mes = mes.format(source, pair, search)
        PLUGINS.set(source)
        PLUGINS.set_pair(pair)
        Message(f, mes).show_info()
        PLUGINS.get_url(search)
    
    def suggest(self):
        from manager import PLUGINS
        f = '[MClient] tests.Commands.suggest'
        source = 'multitran.com'
        pair = 'DEU <=> RUS'
        search = 'Scheiße'
        mes = 'Source: "{}"; pair: "{}"; search: "{}"'
        mes = mes.format(source, pair, search)
        PLUGINS.set(source)
        PLUGINS.set_pair(pair)
        Message(f, mes).show_info()
        lg.com.suggest(search)
    
    def _set_timeout(self, module, source, timeout):
        from manager import PLUGINS
        f = '[MClient] tests.Commands._set_timeout'
        PLUGINS.set(source)
        PLUGINS.set_timeout(timeout)
        mes = _('Source: {}; timeout: {}').format(source, module.TIMEOUT)
        Message(f, mes).show_debug()
    
    def set_timeout(self):
        import plugins.multitrancom.get as mc
        import plugins.stardict.get as sd
        self._set_timeout(module=sd, source=_('Offline'), timeout=1)
        self._set_timeout(module=mc, source=_('Multitran'), timeout=2)
        self._set_timeout(module=mc, source='multitran.com', timeout=3)
    
    def count_valid(self):
        from manager import PLUGINS
        f = '[MClient] tests.Commands.count_valid'
        source = _('Offline')
        PLUGINS.set(source)
        result = PLUGINS.count_valid()
        mes = _('Source: {}; accessibility: {}').format(source, result)
        Message(f, mes).show_debug()
        source = 'multitran.com'
        PLUGINS.set(source)
        result = PLUGINS.count_valid()
        mes = _('Source: {}; accessibility: {}').format(source, result)
        Message(f, mes).show_debug()
    
    def welcome(self):
        import logic as lg
        f = '[MClient] tests.Commands.welcome'
        file_w = '/tmp/test.html'
        code = lg.Welcome().run()
        if code:
            Write(file_w).write(code)
            Launch(file_w).launch_default()
        else:
            rep.empty(f)
    
    def set_pair(self):
        from manager import PLUGINS
        f = '[MClient] tests.Commands.set_pair'
        import plugins.multitrancom.get
        pair = 'RUS <=> XAL'
        source = 'multitran.com'
        PLUGINS.set(source)
        PLUGINS.set_pair(pair)
        mes = f'{source}: {plugins.multitrancom.get.PAIR}'
        Message(f, mes).show_debug()
        PLUGINS.set(_('Multitran'))
        PLUGINS.set_pair('XAL <=> RUS')
        mes = 'multitrancom: {}'.format(plugins.multitrancom.get.PAIR)
        Message(f, mes).show_debug()



com = Commands()


if __name__ == '__main__':
    f = '[MClient] tests.__main__'
    ROOT.get_root()
    ''' #NOTE: Putting QMainWindow.show() or QWidget.show() (without
        explicitly invoking QMainWindow in __main__) in a separate procedure,
        e.g. com.run_welcome, will cause an infinite loop.
    '''
    #mes = com.get_all_subjects()
    #mes = Plugin().run_dsl()
    #mes = Tags().run_dsl()
    #mes = Get().run_stardict()
    #mes = Get().run_dsl()
    mes = Get().run_fora()
    #mes = Get().run_fora_many_matches()
    #mes = Tags().run_stardict()
    #mes = Tags().run_fora_stardictx()
    #mes = Tags().run_fora_dsl()
    #mes = Tags().run_multitrancom()
    #mes = Elems().run_dsl()
    #mes = Elems().run_stardict()
    #mes = Elems().run_fora_stardictx()
    #mes = Elems().run_fora_dsl()
    #mes = Elems().run_fora()
    #mes = Elems().run_multitrancom()
    #mes = Subjects().run()
    #mes = View().run_dsl()
    #mes = View().run_stardict()
    #mes = Subjects().run()
    #mes = View().run_multitrancom()
    #mes = Wrap().run_multitrancom()
    #mes = Elems().run_multitrandem()
    #mes = Prioritize().run_multitrancom()
    #mes = Get().run_multitrandem()
    shDEBUG.reset(f, mes)
    shDEBUG.show()
    # This MUST be on a separate line, the widget will not be shown otherwise
    #idebug.show()
    
    #mes = com.run_speech()
    #Message(f, mes, True).show_debug()
    
    #isuggest = com.run_suggest()
    #isuggest.show()

    # Priorities
    #iprior = com.run_prior()
    #iprior.show()

    # Priorities (from the controller)
    #iprior = com.run_prior_contr()
    #iprior.show()

    '''
    # Popup
    ipopup = com.run_popup()
    ipopup.show()
    '''
    '''
    isave = com.run_save()
    isave.show()
    '''
    '''
    # Settings
    isettings = com.run_settings()
    isettings.show()
    '''
    '''
    # History
    ihis = com.run_history()
    ihis.show()
    '''
    '''
    # History (history.controller)
    ihis = com.run_history_contr()
    ihis.show()
    '''

    # Welcome
    #iwelcome = com.run_welcome()
    #iwelcome.show()

    mes = _('Goodbye!')
    Message(f, mes).show_debug()
    ROOT.end()
