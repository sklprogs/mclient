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

#SEARCH = 'analyzer'
SEARCH = 'hello'
#SEARCH = 'account'
#SEARCH = 'book'
#SEARCH = 'good'
#SEARCH = 'orderly'
URL = 'https://www.multitran.com/m.exe?ll1=1&ll2=2&s=chicken+wing&l2=2'
#HTM_FILE = '/home/pete/docs/mclient_tests/multitrancom (saved in browser)/account (2025-10-26).htm'
HTM_FILE = '/home/pete/docs/mclient_tests/multitrancom (saved in browser)/inundate (2024-04-08).html'


class Wrap:
    
    def run_multitrancom(self):
        f = '[MClient] tests.sources.Wrap.run_multitrancom'
        import articles as ARTICLES
        # Do not change import style - we already have there Get, Tags, etc.
        import sources.multitrancom.cleanup as cu
        import sources.multitrancom.tags as tg
        import sources.multitrancom.elems as el
        import cells as cl
        import view as vw
        
        text = Read(HTM_FILE).get()
        timer = Timer(f)
        timer.start()
        text = cu.CleanUp(text).run()
        blocks = tg.Tags(text).run()
        blocks = el.Elems(blocks).run()
        cells = cl.Cells(blocks).run()
        
        ARTICLES.add(SEARCH, URL, cells)
        
        cells = vw.Omit(cells).run()
        cells = vw.Prioritize(cells).run()
        cells = vw.View(cells).run()
        iwrap = vw.Wrap(cells)
        iwrap.run()
        timer.end()
        return iwrap.debug()



class Prioritize:
    
    def run_multitrancom(self):
        f = '[MClient] tests.sources.Prioritize.run_multitrancom'
        import logic as lg
        import sources.multitrancom.cleanup as cu
        import sources.multitrancom.tags as tg
        import sources.multitrancom.elems as el
        import cells as cl
        import view as vw
        from subjects import SUBJECTS
        
        text = Read(HTM_FILE).get()
        timer = Timer(f)
        timer.start()
        text = cu.CleanUp(text).run()
        blocks = tg.Tags(text).run()
        ielems = el.Elems(blocks)
        blocks = ielems.run()
        cells = cl.Cells(blocks).run()
        
        ''' #FIX: For some reason, lg.objs.get_sources().get_article_subjects()
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

        cells = vw.Omit(cells).run()
        iprior = vw.Prioritize(cells)
        iprior.run()
        timer.end()
        return iprior.debug()



class View:
    
    def run_stardict(self):
        import logic as lg
        import sources.stardict.cleanup as cu
        import sources.stardict.tags as tg
        import sources.stardict.elems as el
        import cells as cl
        import view as vw
        file = '/home/pete/docs/mclient_tests/stardict/EnRu full cut.txt'
        text = Read(file).get()
        text = cu.CleanUp(text).run()
        blocks = tg.Tags(text).run()
        blocks = el.Elems(blocks).run()
        cells = cl.Cells(blocks).run()
        ARTICLES.add(SEARCH, URL, cells)
        cells = vw.Omit(cells).run()
        cells = vw.Prioritize(cells).run()
        iview = vw.View(cells)
        iview.run()
        return iview.debug()
    
    def run_multitrancom(self):
        f = '[MClient] tests.sources.View.run_multitrancom'
        import logic as lg
        import sources.multitrancom.cleanup as cu
        import sources.multitrancom.tags as tg
        import sources.multitrancom.elems as el
        import cells as cl
        import view as vw
        
        text = Read(HTM_FILE).get()
        timer = Timer(f)
        timer.start()
        text = cu.CleanUp(text).run()
        blocks = tg.Tags(text).run()
        blocks = el.Elems(blocks).run()
        cells = cl.Cells(blocks).run()
        
        ARTICLES.add(SEARCH, URL, cells)
        
        cells = vw.Omit(cells).run()
        cells = vw.Prioritize(cells).run()
        iview = vw.View(cells)
        iview.run()
        timer.end()
        return iview.debug()
    
    def run_dsl(self):
        f = '[MClient] tests.sources.View.run_dsl'
        import logic as lg
        import sources.dsl.get as gt
        import sources.dsl.cleanup as cu
        import sources.dsl.tags as tg
        import sources.dsl.elems as el
        import cells as cl
        import view as vw
        
        blocks = []
        
        timer = Timer(f)
        timer.start()
        gt.PATH = Home('mclient').add_config('dics')
        articles = gt.Get(SEARCH).run()
        for iarticle in articles:
            code = cu.CleanUp(iarticle.code).run()
            code = cu.TagLike(code).run()
            blocks += tg.Tags(code = code
                             ,dicname = iarticle.dic).run()
        blocks = el.Elems(blocks).run()
        cells = cl.Cells(blocks).run()
        
        ARTICLES.add(SEARCH, URL, cells)
        
        cells = vw.Omit(cells).run()
        cells = vw.Prioritize(cells).run()
        iview = vw.View(cells)
        iview.run()
        timer.end()
        return iview.debug()



class Elems:
    
    def run_all(self):
        from manager import SOURCES
        from cells import Elems
        blocks = SOURCES.request(SEARCH)
        ielems = Elems(blocks)
        ielems.run()
        return ielems.debug()
    
    def run_multitrandem(self):
        import sources.multitrandem.get as gt
        import sources.multitrandem.tags as tg
        import sources.multitrandem.elems as el
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
        from sources.stardict.cleanup import CleanUp as mCleanUp
        from sources.stardict.tags import Tags as mTags
        from sources.stardict.elems import Elems as mElems
        file = '/home/pete/docs/mclient_tests/stardict/English-Russian full dictionary - hello.txt'
        text = Read(file).get()
        text = mCleanUp(text).run()
        blocks = mTags(text).run()
        ielems = mElems(blocks)
        ielems.run()
        return ielems.debug()
    
    def run_stardict_cells(self):
        from sources.stardict.cleanup import CleanUp as mCleanUp
        from sources.stardict.tags import Tags as mTags
        from sources.stardict.elems import Elems as mElems
        from cells import Elems as cElems, Cells
        file = '/home/pete/docs/mclient_tests/stardict/English-Russian full dictionary - hello.txt'
        text = Read(file).get()
        text = mCleanUp(text).run()
        blocks = mTags(text).run()
        blocks = mElems(blocks).run()
        blocks = cElems(blocks).run()
        icells = Cells(blocks)
        icells.run()
        return icells.debug()
    
    def run_fora(self):
        f = '[MClient] tests.sources.Elems.run_fora'
        from cells import Cells
        from sources.fora.run import Source
        blocks = Source().request(SEARCH)
        if not blocks:
            rep.lazy(f)
            return
        icells = Cells(blocks)
        icells.run()
        return icells.debug()
    
    def run_fora_stardictx(self):
        f = '[MClient] tests.sources.Elems.run_fora_stardictx'
        from sources.fora.get import ALL_DICS
        from sources.fora.stardictx.tags import Tags
        from sources.fora.stardictx.elems import Elems
        article = ALL_DICS.search(SEARCH)
        if not article:
            rep.empty(f)
            return
        blocks = Tags(article).run()
        ielems = Elems(blocks)
        ielems.run()
        return ielems.debug()
    
    def run_fora_dsl(self):
        f = '[MClient] tests.sources.Elems.run_fora_dsl'
        from sources.fora.get import ALL_DICS
        import sources.fora.dsl.cleanup as cu
        import sources.fora.dsl.tags as tg
        import sources.fora.dsl.elems as el
        article = ALL_DICS.search(SEARCH)
        if not article:
            rep.empty(f)
            return
        article = cu.CleanUp(article).run()
        blocks = tg.Tags(article).run()
        ielems = el.Elems(blocks)
        ielems.run()
        return ielems.debug()
    
    def run_mdic(self):
        import sources.mdic.get as gt
        import sources.mdic.elems as el
        import cells as cl
        result = gt.ALL_DICS.search(SEARCH)
        blocks = el.Elems(result).run()
        blocks = cl.Elems(blocks).run()
        icell = cl.Cells(blocks)
        icell.run()
        return icell.debug()
    
    def run_dsl(self):
        import sources.dsl.cleanup as cu
        import sources.dsl.get as gt
        import sources.dsl.tags as tg
        import sources.dsl.elems as el
        blocks = []
        htm = []
        articles = gt.Get(SEARCH).run()
        for iarticle in articles:
            htm.append(iarticle.code)
            code = cu.CleanUp(iarticle.code).run()
            blocks += tg.Tags(code).run()
        htm = '\n'.join(htm)
        ielems = el.Elems(blocks)
        ielems.run()
        return ielems.debug()
    
    def run_multitrancom(self):
        f = '[MClient] tests.sources.Elems.run_multitrancom'
        from skl_shared.text_file import Read
        from skl_shared.time import Timer
        from cells import Cells
        from sources.multitrancom.cleanup import CleanUp as mCleanUp
        from sources.multitrancom.tags import Tags as mTags
        from sources.multitrancom.elems import Elems as mElems
        text = Read(HTM_FILE).get()
        timer = Timer(f)
        timer.start()
        text = mCleanUp(text).run()
        blocks = mTags(text).run()
        blocks = mElems(blocks).run()
        timer.end()
        icells = Cells(blocks)
        icells.run()
        return icells.debug()



class Offline:
    
    def run_multitrancom(self):
        import sources.multitrancom.cleanup as cu
        import sources.multitrancom.tags as tg
        import sources.multitrancom.elems as el
        self.htm = Read(HTM_FILE).get()
        self.text = cu.CleanUp(self.htm).run()
        itags = tg.Tags(self.text)
        blocks = itags.run()
        ielems = el.Elems(blocks)
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
        f = '[MClient] tests.sources.Subjects.expand'
        sub = self.isubj.expand(subj)
        self.report.append(f'{f}:\n{sub}')
    
    def is_phrase_blocked(self, subject):
        f = '[MClient] tests.sources.Subjects.is_phrase_blocked'
        if self.isubj.is_phrase_blocked(subject):
            sub = _('Phrase "{}" is blocked').format(subject)
        else:
            sub = _('Phrase "{}" is NOT blocked').format(subject)
        self.report.append(f'{f}:\n{sub}')
    
    def is_phrase_prior(self, subject):
        f = '[MClient] tests.sources.Subjects.is_phrase_prior'
        if self.isubj.is_phrase_prior(subject):
            sub = _('Phrase "{}" is prioritized').format(subject)
        else:
            sub = _('Phrase "{}" is NOT prioritized').format(subject)
        self.report.append(f'{f}:\n{sub}')
    
    def is_blocked(self, subject):
        f = '[MClient] tests.sources.Subjects.is_blocked'
        if self.isubj.is_blocked(subject):
            sub = _('Subject "{}" is blocked').format(subject)
        else:
            sub = _('Subject "{}" is NOT blocked').format(subject)
        self.report.append(f'{f}:\n{sub}')
    
    def is_prioritized(self, subject):
        f = '[MClient] tests.sources.Subjects.is_prioritized'
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



class CleanUp:
    
    def run_dsl(self):
        f = '[MClient] tests.sources.CleanUp.run_dsl'
        import sources.dsl.get as gt
        import sources.dsl.cleanup as cu
        code = []
        articles = gt.Get(SEARCH).run()
        for iarticle in articles:
            code.append(cu.CleanUp(iarticle.code).run())
        code = '\n\n'.join(code)
        return f + '\n"' + cu.CleanUp(code).run() + '"'



class Get:
    
    def run_local(self):
        mes = []
        mes.append('DSL:')
        mes.append(self.run_dsl())
        mes.append('\n')
        mes.append('Fora:')
        mes.append(self.run_fora())
        mes.append('\n')
        mes.append('MDIC:')
        mes.append(self.run_mdic())
        mes.append('\n')
        mes.append('Multitran (Demo):')
        mes.append(self.run_multitrandem())
        mes.append('\n')
        mes.append('Stardict:')
        mes.append(self.run_stardict())
        mes.append('\n')
        mes = [item for item in mes if item]
        return '\n'.join(mes)
    
    def run_mdic(self):
        from sources.mdic.get import ALL_DICS
        # Search is case-insensitive for MDIC
        result = ALL_DICS.search(SEARCH)
        if result:
            # Useful for debugging only
            return '\n\n'.join(result)
        else:
            return ''
    
    def decode_indexes(self, indexes):
        from sources.fora.get import Index
        iindex = Index('/home/pete/.config/mclient/dics/Fora/dict pl-ru')
        for i in range(len(indexes)):
            indexes[i][0] = iindex.decode(indexes[i][0])
            indexes[i][1] = iindex.decode(indexes[i][1])
        return indexes
    
    def run_fora_many_matches(self):
        from sources.fora.get import ALL_DICS
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
        from sources.fora.get import ALL_DICS
        return ALL_DICS.search(SEARCH)
    
    def run_dsl(self):
        from sources.dsl.get import Get as mGet
        iget = mGet(SEARCH)
        iget.run()
        return iget.debug()
    
    def run_multitrandem(self):
        from sources.multitrandem.get import CODING, Get as mGet
        result = mGet(SEARCH).run()
        if not result:
            rep.empty(f)
            return
        for i in range(len(result)):
            result[i] = result[i].decode(CODING)
        return str(result)
    
    def run_multitrancom(self):
        f = '[MClient] tests.sources.Get.run_multitrancom'
        import sources.multitrancom.get as gt
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
        from sources.stardict.get import ALL_DICS
        return ALL_DICS.get(SEARCH)



class Tags:
    
    def run_fora_stardictx(self):
        f = '[MClient] tests.sources.Tags.run_fora_stardictx'
        import sources.fora.get as gt
        import sources.fora.stardictx.cleanup as cu
        import sources.fora.stardictx.tags as tg
        article = gt.ALL_DICS.search(SEARCH)
        if not article:
            rep.empty(f)
            return
        article = cu.CleanUp(article).run()
        itags = tg.Tags(article)
        itags.run()
        return itags.debug()
    
    def run_fora_dsl(self):
        f = '[MClient] tests.sources.Tags.run_fora_dsl'
        import sources.fora.get as gt
        import sources.fora.dsl.cleanup as cu
        import sources.fora.dsl.tags as tg
        article = gt.ALL_DICS.search(SEARCH)
        if not article:
            rep.empty(f)
            return
        article = cu.CleanUp(article).run()
        itags = tg.Tags(article)
        itags.run()
        return itags.debug()
    
    def run_multitrandem(self):
        f = '[MClient] tests.sources.Tags.run_multitrandem'
        from manager import SOURCES
        import sources.multitrandem.get as gt
        import sources.multitrandem.tags as tg
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
        import sources.dsl.get as gt
        import sources.dsl.cleanup as cu
        import sources.dsl.tags as tg
        articles = gt.Get('account').run()
        debug = []
        for iarticle in articles:
            code = cu.CleanUp(iarticle.code).run()
            itags = tg.Tags(code)
            itags.run()
            debug.append(itags.debug())
        return '\n\n'.join(debug)
    
    def analyze_tag(self):
        import sources.multitrancom.tags as tg
        #tag = '<tr><td class="subj" width="1"><a href="https://www.multitran.com/m.exe?a=110&amp;l1=2&amp;l2=1&amp;s=%D1%82%D1%80%D0%BE%D1%81&amp;sc=371" title="Автоматика">автомат.'
        #tag = '''<tr><td class="subj" width="1"><a href="https://www.multitran.com/m.exe?a=110&amp;l1=2&amp;l2=1&amp;s=%D1%82%D1%80%D0%BE%D1%81&amp;sc=0" title="Общая лексика">общ.'''
        tag = '<tr><td class="subj" width="1"><a href="https://www.multitran.com/m.exe?a=110&amp;l1=2&amp;l2=1&amp;s=%D1%82%D1%80%D0%BE%D1%81&amp;sc=134" title="Электроника">эл.'
        itag = tg.AnalyzeTag(tag)
        itag.run()
        itag.debug()
    
    def run_stardict(self):
        import sources.stardict.cleanup as cu
        import sources.stardict.tags as tg
        file = '/home/pete/docs/mclient_tests/stardict/English-Russian full dictionary - good.txt'
        text = Read(file).get()
        text = cu.CleanUp(text).run()
        itags = tg.Tags(text)
        itags.run()
        return itags.debug()
    
    def run_multitrancom(self):
        from skl_shared.text_file import Read
        from sources.multitrancom.cleanup import CleanUp
        from sources.multitrancom.tags import Tags
        text = Read(HTM_FILE).get()
        text = CleanUp(text).run()
        itags = Tags(text)
        itags.run()
        return itags.debug()



class Source:
    
    def run_all(self):
        from manager import SOURCES
        from cells import Cells
        blocks = SOURCES.request(SEARCH)
        icells = Cells(blocks)
        icells.run()
        return icells.debug()
    
    def run_fora(self):
        from cells import Cells
        from sources.fora.run import Source as mSource
        blocks = mSource().request(SEARCH)
        icells = Cells(blocks)
        icells.run()
        return icells.debug()
    
    def run_multitrandem(self):
        from cells import Cells
        from sources.multitrandem.run import Source as mSource
        blocks = mSource().request(search=SEARCH)
        icells = Cells(blocks)
        icells.run()
        return icells.debug()
    
    def run_stardict(self):
        from cells import Cells
        from sources.stardict.run import Source as mSource
        blocks = mSource().request(SEARCH)
        icells = Cells(blocks)
        icells.run()
        return icells.debug()
    
    def run_mdic(self):
        from cells import Cells
        from sources.mdic.run import Source as mSource
        blocks = mSource().request(SEARCH)
        icells = Cells(blocks)
        icells.run()
        return icells.debug()
    
    def run_dsl(self):
        from cells import Cells
        from sources.dsl.run import Source as mSource
        blocks = mSource().request(SEARCH)
        icells = Cells(blocks)
        icells.run()
        return icells.debug()
    
    def run_multitrancom(self):
        from cells import Cells
        from sources.multitrancom.run import Source as mSource
        blocks = mSource().request(url=url, search=SEARCH)
        icells = Cells(blocks)
        icells.run()
        return icells.debug()



class Commands:
    
    def get_all_subjects(self):
        import sources.multitrancom.subjects as sj
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
        f = '[MClient] tests.sources.Commands.get_priority'
        from manager import SOURCES
        from articles import ARTICLES
        from subjects import SUBJECTS
        #NOTE: the article must comprise example subjects to be expanded
        search = 'code'
        url = 'https://www.multitran.com/m.exe?s=code&l1=2&l2=1&SHL=2'
        cells = SOURCES.request(search=search, url=url)
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
        f = '[MClient] tests.sources.Commands.run_article_subjects'
        from manager import SOURCES
        from articles import ARTICLES
        search = 'set'
        # SHL should correspond to locale
        url = 'https://www.multitran.com/m.exe?s=set&l1=2&l2=1'
        cells = SOURCES.request(search=search, url=url)
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
        f = '[MClient] tests.sources.Commands.run_font_limits'
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
        f = '[MClient] tests.sources.Commands.get_column_width'
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
    
    def get_modified_subjects(self):
        f = '[MClient] tests.sources.Commands.get_modified_subjects'
        import sources.multitrancom.subjects as sj
        titles = []
        for key in sj.SUBJECTS.keys():
            if sj.SUBJECTS[key]['Modified']:
                titles.append(sj.SUBJECTS[key]['ru']['title'])
        titles.sort()
        mes = '\n'.join(titles)
        shDEBUG.reset(f, mes)
        shDEBUG.show()
    
    def run_speech(self):
        import sources.multitrancom.speech as sp
        # ru_RU locale is required
        short = 'прил.'
        full = sp.objs.get_speech().find(short)
        mes = f'"{short}" -> "{full}"'
        return mes
    
    def show_about(self):
        from mclient import About
        About().show()
    
    def get_nonpairs(self):
        ''' Get languages that are not supported by multitran.com for
            both directions.
        '''
        f = '[MClient] tests.sources.Commands.get_nonpairs'
        import sources.multitrancom.pairs as pairs
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
        f = '[MClient] tests.sources.Commands.compare_elems'
        import sources.multitran.elems as el
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
        from manager import SOURCES
        f = '[MClient] tests.sources.Commands.request'
        source = _('Multitran')
        pair = 'DEU <=> RUS'
        search = 'ernährung'
        mes = _('Source: "{}"; pair: "{}"; search: "{}"')
        mes = mes.format(source, pair, search)
        SOURCES.set(source)
        SOURCES.set_pair(pair)
        Message(f, mes).show_info()
        data = SOURCES.request(search=search, url='')
        if not data:
            rep.empty(f)
            return
        shDEBUG.reset(f, data)
        shDEBUG.show()
    
    def get_url(self):
        from manager import SOURCES
        f = '[MClient] tests.sources.Commands.get_url'
        source = 'multitran.com'
        pair = 'RUS <=> XAL'
        search = 'До свидания!'
        mes = 'Source: "{}"; pair: "{}"; search: "{}"'
        mes = mes.format(source, pair, search)
        SOURCES.set(source)
        SOURCES.set_pair(pair)
        Message(f, mes).show_info()
        SOURCES.get_url(search)
    
    def suggest(self):
        from manager import SOURCES
        f = '[MClient] tests.sources.Commands.suggest'
        source = 'multitran.com'
        pair = 'DEU <=> RUS'
        search = 'Scheiße'
        mes = 'Source: "{}"; pair: "{}"; search: "{}"'
        mes = mes.format(source, pair, search)
        SOURCES.set(source)
        SOURCES.set_pair(pair)
        Message(f, mes).show_info()
        lg.com.suggest(search)
    
    def _set_timeout(self, module, source, timeout):
        from manager import SOURCES
        f = '[MClient] tests.sources.Commands._set_timeout'
        SOURCES.set(source)
        SOURCES.set_timeout(timeout)
        mes = _('Source: {}; timeout: {}').format(source, module.TIMEOUT)
        Message(f, mes).show_debug()
    
    def set_timeout(self):
        import sources.multitrancom.get as mc
        import sources.stardict.get as sd
        self._set_timeout(module=sd, source=_('Offline'), timeout=1)
        self._set_timeout(module=mc, source=_('Multitran'), timeout=2)
        self._set_timeout(module=mc, source='multitran.com', timeout=3)
    
    def count_valid(self):
        from manager import SOURCES
        f = '[MClient] tests.sources.Commands.count_valid'
        source = _('Offline')
        SOURCES.set(source)
        result = SOURCES.count_valid()
        mes = _('Source: {}; accessibility: {}').format(source, result)
        Message(f, mes).show_debug()
        source = 'multitran.com'
        SOURCES.set(source)
        result = SOURCES.count_valid()
        mes = _('Source: {}; accessibility: {}').format(source, result)
        Message(f, mes).show_debug()
    
    def welcome(self):
        import logic as lg
        f = '[MClient] tests.sources.Commands.welcome'
        file_w = '/tmp/test.html'
        code = lg.Welcome().run()
        if code:
            Write(file_w).write(code)
            Launch(file_w).launch_default()
        else:
            rep.empty(f)
    
    def set_pair(self):
        from manager import SOURCES
        f = '[MClient] tests.sources.Commands.set_pair'
        import sources.multitrancom.get
        pair = 'RUS <=> XAL'
        source = 'multitran.com'
        SOURCES.set(source)
        SOURCES.set_pair(pair)
        mes = f'{source}: {sources.multitrancom.get.PAIR}'
        Message(f, mes).show_debug()
        SOURCES.set(_('Multitran'))
        SOURCES.set_pair('XAL <=> RUS')
        mes = 'multitrancom: {}'.format(sources.multitrancom.get.PAIR)
        Message(f, mes).show_debug()



com = Commands()