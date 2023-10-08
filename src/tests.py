#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh
import skl_shared_qt.config as qc

import config as cf

DEBUG = True

''' #NOTE: The file should be generated with 'plugins.multitrancom.get.Get',
    otherwise, 'Tags' will fail to set 'subj' and some other types.
'''
SEARCH = 'компьютер'
URL = ''
HTM_FILE = '/home/pete/docs/mclient_tests/multitrancom (saved with Get.get)/clutch (2023-09-30).html'


class Config:
    
    def __init__(self):
        self.schema = sh.objs.get_pdir().add('..', 'resources', 'config', 'schema.json')
        self.default = sh.objs.pdir.add('..', 'resources', 'config', 'default.json')
        self.local = sh.Home(cf.PRODUCT_LOW).add_config(cf.PRODUCT_LOW + '.json')
    
    def run_schema(self):
        ischema = qc.Schema(self.schema)
        ischema.run()
        mes = []
        sub = _('Configuration file: {}').format(ischema.file)
        mes.append(sub)
        if ischema.Success:
            sub = _('Result: Success')
        else:
            sub = _('Result: Failed')
        mes.append(sub)
        sub = _('Dictionary:\n{}').format(ischema.dump())
        mes.append(sub)
        return '\n'.join(mes)
    
    def run_default(self):
        ischema = qc.Schema(self.schema)
        ischema.run()
        idefault = qc.Default(self.default, ischema.get())
        idefault.run()
        mes = []
        sub = _('Configuration file: {}').format(self.default)
        mes.append(sub)
        sub = _('Version: {}').format(idefault.get_version())
        mes.append(sub)
        if idefault.Success:
            sub = _('Result: Success')
        else:
            sub = _('Result: Failed')
        mes.append(sub)
        sub = _('Dictionary:\n{}').format(idefault.dump())
        mes.append(sub)
        return '\n'.join(mes)
    
    def run_local(self):
        f = '[SharedQt] config.Tests.run_local'
        min_version = 2
        ilocal = qc.Local(self.local, min_version)
        ilocal.run()
        timer = sh.Timer(f)
        timer.start()
        mes = []
        sub = _('Configuration file: {}').format(self.local)
        mes.append(sub)
        sub = _('Version: {}').format(ilocal.get_version())
        mes.append(sub)
        if ilocal.Success:
            sub = _('Result: Success')
        else:
            sub = _('Result: Failed')
        mes.append(sub)
        sub = _('Dictionary:\n{}').format(ilocal.dump())
        mes.append(sub)
        timer.end()
        return '\n'.join(mes)
    
    def run_config(self):
        f = '[SharedQt] config.Tests.run_config'
        timer = sh.Timer(f)
        timer.start()
        iconfig = cf.Config(self.default, self.schema, self.local)
        iconfig.run()
        mes = []
        sub = _('Configuration file: {}').format(self.local)
        mes.append(sub)
        sub = _('Version: {}').format(iconfig.ilocal.get_version())
        mes.append(sub)
        if iconfig.Success:
            sub = _('Result: Success')
        else:
            sub = _('Result: Failed')
        mes.append(sub)
        #iconfig.quit()
        sub = _('Dictionary:\n{}').format(iconfig.dump())
        mes.append(sub)
        timer.end()
        return '\n'.join(mes)



class Wrap:
    
    def run_multitrancom(self):
        f = '[MClient] tests.Wrap.run_multitrancom'
        import logic as lg
        import plugins.multitrancom.cleanup as cu
        import plugins.multitrancom.tags as tg
        import plugins.multitrancom.elems as el
        import cells as cl
        
        text = sh.ReadTextFile(HTM_FILE).get()
        timer = sh.Timer(f)
        timer.start()
        text = cu.CleanUp(text).run()
        blocks = tg.Tags (text = text
                         ,maxrows = 0
                         ).run()
        cells = el.Elems(blocks).run()
        
        lg.objs.get_articles().add (search = SEARCH
                                   ,url = URL
                                   ,cells = cells
                                   )
        
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
        
        text = sh.ReadTextFile(HTM_FILE).get()
        timer = sh.Timer(f)
        timer.start()
        text = cu.CleanUp(text).run()
        blocks = tg.Tags (text = text
                         ,maxrows = 0
                         ).run()
        cells = el.Elems(blocks).run()
        
        lg.objs.get_articles().add (search = SEARCH
                                   ,url = URL
                                   ,cells = cells
                                   )

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
        text = sh.ReadTextFile(file).get()
        text = cu.CleanUp(text).run()
        blocks = tg.Tags(text).run()
        cells = el.Elems(blocks).run()
        lg.objs.get_articles().add (search = SEARCH
                                   ,url = URL
                                   ,cells = cells
                                   )
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
        
        text = sh.ReadTextFile(HTM_FILE).get()
        timer = sh.Timer(f)
        timer.start()
        text = cu.CleanUp(text).run()
        blocks = tg.Tags (text = text
                         ,maxrows = 0
                         ).run()
        cells = el.Elems(blocks).run()
        
        lg.objs.get_articles().add (search = SEARCH
                                   ,url = URL
                                   ,cells = cells
                                   )
        
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
        
        timer = sh.Timer(f)
        timer.start()
        gt.PATH = sh.Home('mclient').add_config('dics')
        articles = gt.Get(SEARCH).run()
        for iarticle in articles:
            code = cu.CleanUp(iarticle.code).run()
            code = cu.TagLike(code).run()
            blocks += tg.Tags (code = code
                              ,Debug = DEBUG
                              ,maxrows = 0
                              ,dicname = iarticle.dic
                              ).run()
        cells = el.Elems(blocks).run()
        
        lg.objs.get_articles().add (search = SEARCH
                                   ,url = URL
                                   ,cells = cells
                                   )
        
        cells = cl.Omit(cells).run()
        cells = cl.Prioritize(cells).run()
        iview = cl.View(cells)
        iview.run()
        timer.end()
        return iview.debug()



class Elems:
    
    def run_stardict(self):
        import plugins.stardict.cleanup as cu
        import plugins.stardict.tags as tg
        import plugins.stardict.elems as el
        file = '/home/pete/docs/mclient_tests/stardict/EnRu full cut.txt'
        text = sh.ReadTextFile(file).get()
        text = cu.CleanUp(text).run()
        blocks = tg.Tags(text).run()
        ielems = el.Elems(blocks)
        ielems.run()
        return ielems.debug()
    
    def run_dsl(self):
        import plugins.dsl.cleanup as cu
        import plugins.dsl.get as gt
        import plugins.dsl.tags as tg
        import plugins.dsl.elems as el
        gt.PATH = sh.Home('mclient').add_config('dics')
        blocks = []
        htm = []
        search = 'account'
        articles = gt.Get(search).run()
        for iarticle in articles:
            htm.append(iarticle.code)
            code = cu.CleanUp(iarticle.code).run()
            code = cu.TagLike(code).run()
            blocks += tg.Tags (code = code
                              ,Debug = DEBUG
                              ,maxrows = 0
                              ,dicname = iarticle.dic
                              ).run()
        htm = '\n'.join(htm)
        ielems = el.Elems (blocks = blocks
                          ,Debug = DEBUG
                          )
        blocks = ielems.run()
        return ielems.debug()
    
    def run_multitrancom(self):
        f = '[MClient] tests.Elems.run_multitrancom'
        import plugins.multitrancom.cleanup as cu
        import plugins.multitrancom.tags as tg
        import plugins.multitrancom.elems as el
        text = sh.ReadTextFile(HTM_FILE).get()
        timer = sh.Timer(f)
        timer.start()
        text = cu.CleanUp(text).run()
        blocks = tg.Tags (text = text
                         ,maxrows = 0
                         ).run()
        ielems = el.Elems(blocks)
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
        self.htm = sh.ReadTextFile(HTM_FILE).get()
        self.text = cu.CleanUp(self.htm).run()
        itags = tg.Tags (text = self.text
                        ,Debug = DEBUG
                        ,maxrows = self.maxrows
                        )
        blocks = itags.run()
        ielems = el.Elems (blocks = blocks
                          ,Debug = DEBUG
                          ,maxrows = self.maxrows
                          )
        ielems.run()
        return ielems.debug()



class Subjects:
    
    def __init__(self):
        self.report = []
    
    def run(self):
        #self.run_history()
        self.expand('комп.')
        self.expand('Компьютеры')
        self.show_prior_default()
        self.show_prior_local()
        self.show_prioritized()
        self.is_prioritized('общ.')
        self.is_prioritized('Общая лексика')
        self.is_prioritized('комп., Майкр.')
        self.is_prioritized('Майкрософт')
        self.is_prioritized('ИТ.')
        self.is_prioritized('Информационные технологии')
        return '\n'.join(self.report)
    
    def show_prior_default(self):
        f = '[MClient] tests.Subjects.show_prior_default'
        sub = f'{f}:'
        self.report.append(sub)
        sub = 'Prioritized subjects from default config:'
        self.report.append(sub)
        try:
            prior = cf.objs.get_config().idefault.get()['subjects']['prioritized']
        except KeyError:
            prior = []
            sh.com.rep_out(f)
        self.report.append('; '.join(prior))
        self.report.append('')
    
    def show_prior_local(self):
        f = '[MClient] tests.Subjects.show_prior_local'
        sub = f'{f}:'
        self.report.append(sub)
        sub = 'Prioritized subjects from local config:'
        self.report.append(sub)
        try:
            prior = cf.objs.get_config().ilocal.get()['subjects']['prioritized']
        except KeyError:
            prior = []
            sh.com.rep_out(f)
        self.report.append('; '.join(prior))
        self.report.append('')
    
    def show_prioritized(self):
        f = '[MClient] tests.Subjects.show_prioritized'
        sub = f'{f}:'
        self.report.append(sub)
        try:
            prior = cf.objs.get_config().new['subjects']['prioritized']
        except KeyError:
            prior = []
            sh.com.rep_out(f)
        sub = 'Prioritized subjects from final config:'
        self.report.append(sub)
        self.report.append('; '.join(prior))
        self.report.append('')
    
    def is_prioritized(self, subject):
        f = '[MClient] tests.Subjects.is_prioritized'
        import subjects as sj
        sub = f'{f}:'
        self.report.append(sub)
        Prioritized = sj.objs.get_subjects().is_prioritized(subject)
        if Prioritized:
            result = 'is prioritized'
        else:
            result = 'is NOT prioritized'
        sub = f'"{subject}" {result}'
        self.report.append(sub)
        self.report.append('')
    
    def expand(self, short):
        f = '[MClient] tests.Subjects.expand'
        import subjects as sj
        sub = f'{f}:'
        self.report.append(sub)
        sub = f'"{short}" expanded from history: "{sj.objs.get_subjects().expand(short)}"'
        self.report.append(sub)
        self.report.append('')
    
    def run_history(self):
        f = '[MClient] tests.Subjects.run_history'
        sub = f'{f}:'
        self.report.append(sub)
        sub = _('History subjects:')
        self.report.append(sub)
        sub = str(cf.objs.get_config().new['subjects']['history'])
        self.report.append(sub)
        self.report.append('')



class ArticleSubjects:
    
    def __init__(self):
        self.blocks = []
    
    def run(self):
        self.set_blocks()
        self.set_article()
    
    def set_article(self):
        f = '[MClient] tests.Subjects.set_article'
        import subjects.subjects as sj
        import mclientqt as mclient
        pairs = mclient.objs.get_blocksdb().get_dic_pairs()
        mes = _('Pairs: {}').format(pairs)
        sh.objs.get_mes(f, mes, True).show_debug()
        sj.objs.get_article().reset(pairs, DEBUG)
        sj.objs.article.run()
    
    def set_blocks(self):
        f = '[MClient] tests.Subjects.set_blocks'
        import mclientqt as mclient
        # Lists will be automatically read from files on import
        import logic as lg
        #search = 'hello'
        #url = 'https://www.multitran.com/m.exe?s=hello&l1=1&l2=2&SHL=2'
        search = 'messenger'
        url = 'https://www.multitran.com/m.exe?s=messenger&l1=1&l2=2'
        blocks = lg.objs.get_plugins().request (search = search
                                               ,url = url
                                               )
        mclient.objs.get_blocksdb().artid = 1
        data = lg.com.dump_elems (blocks = blocks
                                 ,artid = mclient.objs.blocksdb.artid
                                 )
        if not data:
            sh.com.rep_empty(f)
            return
        mclient.objs.blocksdb.fill_blocks(data)



class Block:
    
    def __init__(self):
        self.id_ = None   # (00) Autoincrement
        self.artid = 0    # (01) ARTICLEID
        self.dic = ''     # (02) DIC (short title)
        self.wform = ''   # (03) WFORM
        self.speech = ''  # (04) SPEECH
        self.transc = ''  # (05) TRANSC
        self.term = ''    # (06) TERM
        self.type = ''    # (07) TYPE
        self.text = ''    # (08) TEXT
        self.url = ''     # (09) URL
        self.block = 0    # (10) BLOCK
        self.dprior = 0   # (11) DICPR
        self.select = 0   # (12) SELECTABLE
        self.same = 0     # (13) SAMECELL
        self.cellno = 0   # (14) CELLNO
        self.rowno = -1   # (15) ROWNO
        self.colno = -1   # (16) COLNO
        self.pos1 = -1    # (17) POS1
        self.pos2 = -1    # (18) POS2
        self.node1 = ''   # (19) NODE1
        self.node2 = ''   # (20) NODE2
        self.offpos1 = -1 # (21) OFFPOS1
        self.offpos2 = -1 # (22) OFFPOS2
        self.bbox1 = -1   # (23) BBOX1
        self.bbox2 = -1   # (24) BBOX2
        self.bboy1 = -1   # (25) BBOY1
        self.bboy2 = -1   # (26) BBOY2
        self.textlow = '' # (27) TEXTLOW
        self.ignore = 0   # (28) IGNORE
        self.sprior = 0   # (29) SPEECHPR
        self.dicf = ''    # (30) DIC (full title)
    
    def dump(self):
        return (self.id_
               ,self.artid
               ,self.dic
               ,self.wform
               ,self.speech
               ,self.transc
               ,self.term
               ,self.type
               ,self.text
               ,self.url
               ,self.block
               ,self.dprior
               ,self.select
               ,self.same
               ,self.cellno
               ,self.rowno
               ,self.colno
               ,self.pos1
               ,self.pos2
               ,self.node1
               ,self.node2
               ,self.offpos1
               ,self.offpos2
               ,self.bbox1
               ,self.bbox2
               ,self.bboy1
               ,self.bboy2
               ,self.textlow
               ,self.ignore
               ,self.speech
               ,self.dicf
               )



class Get:
    
    def run_dsl(self):
        import plugins.dsl.get
        plugins.dsl.get.PATH = sh.Home('mclient').add_config('dics')
        iget = plugins.dsl.get.Get (pattern = 'account'
                                   ,Debug = DEBUG
                                   )
        iget.run()
        return iget.debug()
    
    def run_multitrancom(self):
        f = '[MClient] tests.Get.run_multitrancom'
        import plugins.multitrancom.get as gt
        #url = 'https://www.multitran.com/m.exe?a=3&sc=8&s=%D1%81%D0%B8%D0%BC%D0%BF%D1%82%D0%BE%D0%BC&l1=2&l2=1&SHL=2'
        #search = 'Медицина'
        url = 'https://www.multitran.com/m.exe?s=working%20documentation&l1=1&l2=2&SHL=2'
        search = 'working documentation'
        timer = sh.Timer(f)
        timer.start()
        result = gt.Get (search = search
                        ,url = url
                        ).run()
        timer.end()
        basename = f'{search} ({sh.Time().get_date()}).html'
        file = sh.Home().add ('docs', 'mclient_tests'
                             ,'multitrancom (saved with Get.get)', basename
                             )
        sh.WriteTextFile(file).write(result)
        sh.Launch(file).launch_default()
    
    def run_stardict(self):
        f = '[MClient] tests.Get.run_stardict'
        import plugins.stardict.get
        #search = 'компьютер'
        search = 'computer'
        timer = sh.Timer(f)
        timer.start()
        result = plugins.stardict.get.Get(search).run()
        timer.end()
        return result



class Tags:
    
    def run_dsl(self):
        import plugins.dsl.get
        import plugins.dsl.cleanup
        import plugins.dsl.tags
        plugins.dsl.get.PATH = sh.Home('mclient').add_config('dics')
        articles = plugins.dsl.get.Get('account balance').run()
        blocks = []
        debug = []
        for iarticle in articles:
            code = plugins.dsl.cleanup.CleanUp(iarticle.code).run()
            code = plugins.dsl.cleanup.TagLike(code).run()
            itags = plugins.dsl.tags.Tags (code = code
                                          ,Debug = DEBUG
                                          ,maxrows = 0
                                          ,dicname = iarticle.dic
                                          )
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
        file = '/home/pete/docs/mclient_tests/stardict/EnRu full cut.txt'
        text = sh.ReadTextFile(file).get()
        text = cu.CleanUp(text).run()
        itags = tg.Tags (text = text
                        ,Debug = DEBUG
                        ,maxrows = 0
                        )
        itags.run()
        return itags.debug()
    
    def run_multitrancom(self):
        import plugins.multitrancom.cleanup as cu
        import plugins.multitrancom.tags as tg
        text = sh.ReadTextFile(HTM_FILE).get()
        text = cu.CleanUp(text).run()
        itags = tg.Tags (text = text
                        ,Debug = DEBUG
                        ,maxrows = 0
                        )
        itags.run()
        return itags.debug()



class Plugin:
    
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
        iplug = mb.Plugin (Debug = DEBUG
                          ,maxrows = 150
                          )
        
        blocks = iplug.request (url = url
                               ,search = search
                               )
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
        plugins.dsl.get.PATH = sh.Home('mclient').add_config('dics')
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
        
        mc.Plugin (Debug = DEBUG
                  ,maxrows = 0
                  ).request (url = url
                            ,search = search
                            )



class Commands:
    
    def get_all_subjects(self):
        import plugins.multitrancom.subjects as sj
        return sj.objs.get_subjects().dump()
    
    def run_config(self):
        cf.objs.get_config().run()
    
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
        f = '[MClientQt] tests.Commands.get_priority'
        import logic as lg
        import subjects as sj
        #NOTE: the article must comprise example subjects to be expanded
        search = 'code'
        url = 'https://www.multitran.com/m.exe?s=code&l1=2&l2=1&SHL=2'
        cells = lg.objs.get_plugins().request (search = search
                                              ,url = url
                                              )
        lg.objs.get_articles().add (search = search
                                   ,url = url
                                   ,cells = cells
                                   )
        mes = []
        sub = f'{f}:'
        mes.append(sub)
        mes.append(_('Prioritized subjects:'))
        sub = '; '.join(cf.objs.get_config().new['subjects']['prioritized'])
        mes.append(sub)
        mes.append('')
        subject = 'тест., ИТ., Gruzovik, прогр.'
        sub = _('Subject: "{}"').format(subject)
        mes.append(sub)
        isubj = sj.Subjects()
        priority = isubj.get_priority(subject)
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
        sub = sh.FastTable (headers = (_('SUBJECT'), _('PRIORITY'))
                           ,iterable = [parts, priorities]
                           ).run()
        mes.append(sub)
        return '\n'.join(mes)
    
    def run_article_subjects(self):
        f = '[MClientQt] tests.Commands.run_article_subjects'
        import logic as lg
        search = 'set'
        # SHL should correspond to locale
        url = 'https://www.multitran.com/m.exe?s=set&l1=2&l2=1'
        cells = lg.objs.get_plugins().request (search = search
                                              ,url = url
                                              )
        lg.objs.get_articles().add (search = search
                                   ,url = url
                                   ,cells = cells
                                   )
        subjects = lg.objs.get_articles().get_subjects()
        if not subjects:
            sh.com.rep_empty(f)
            return
        shorts = []
        fulls = []
        for short in subjects:
            shorts.append(short)
            fulls.append(subjects[short])
        mes = sh.FastTable (headers = (_('SHORT'), _('FULL'))
                           ,iterable = [shorts, fulls]
                           ,maxrow = 70
                           ).run()
        return mes
    
    def run_prior(self):
        import config as cf
        import mclientqt as mc
        cf.objs.get_config()
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
        file = sh.objs.get_pdir().add('..', 'resources', 'third parties.txt')
        text = sh.ReadTextFile(file).get()
        text = sh.Text(text, True).delete_line_breaks() * 10
        ipopup.fill(text)
        return ipopup
    
    def run_font_limits(self):
        f = '[MClient] tests.Commands.run_font_limits'
        import mclientqt as mc
        text = 'Раз, два, три, четыре, пять - вышел зайчик погулять'
        ilimits = mc.FontLimits (family = cf.objs.get_config().new['terms']['font']['family']
                                ,size = cf.objs.config.new['terms']['font']['size']
                                ,Bold = False
                                ,Italic = False
                                )
        timer = sh.Timer(f)
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
        import mclientqt as mc
        ihis = mc.History()
        ihis.add()
        ihis.add()
        ihis.add()
        ihis.add()
        return ihis
    
    def run_welcome(self):
        import mclientqt as mc
        cf.objs.get_config()
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
                ,['5', _('English'), _('Russian'), 'fifth']
                ]
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
        sh.com.end()
    
    def get_column_width(self):
        f = '[MClient] tests.Commands.get_column_width'
        import logic as lg
        #cf.objs.get_config().new['columns']['num'] = 0
        mes = f'"{lg.com.get_column_width()}%"'
        sh.objs.get_mes(f, mes, True).show_debug()
    
    def check_width(self):
        import mclientqt as mc
        file = '/home/pete/tmp/frame rate.htm'
        #file = '/tmp/f.htm'
        code = sh.ReadTextFile(file).get()
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
            sh.com.run_fast_debug(f, mes)
        else:
            sh.com.rep_lazy(f)
    
    def get_modified_subjects(self):
        f = '[MClient] tests.Commands.get_modified_subjects'
        import plugins.multitrancom.subjects as sj
        titles = []
        for key in sj.SUBJECTS.keys():
            if sj.SUBJECTS[key]['Modified']:
                titles.append(sj.SUBJECTS[key]['ru']['title'])
        titles.sort()
        mes = '\n'.join(titles)
        sh.com.run_fast_debug(f, mes)
    
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
        mes = sh.FastTable (iterable = iterable
                           ,headers = headers
                           ,maxrow = 30
                           ).run()
        sh.com.run_fast_debug(f, mes)
    
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
        import mclientqt as mc
        import logic as lg
        mc.objs.get_priorities().reset (lst1 = lg.objs.get_order().priorlst
                                       ,lst2 = lg.objs.get_plugins().get_subjects()
                                       ,art_subjects = []
                                       ,majors = lg.objs.plugins.get_majors()
                                       )
        mc.objs.priorities.show()
    
    def edit_blacklist(self):
        import mclientqt as mc
        import logic as lg
        mc.objs.get_blacklist().reset (lst1 = lg.objs.get_order().blacklst
                                      ,lst2 = lg.objs.get_plugins().get_subjects()
                                      ,art_subjects = []
                                      ,majors = lg.objs.plugins.get_majors()
                                      )
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
        sh.objs.get_mes(f, mes, True).show_info()
    
    def compare_elems(self):
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
        data = '\n'.join(data)
        sh.com.run_fast_txt(data)
    
    def request(self):
        import logic as lg
        f = '[MClient] tests.Commands.request'
        source = _('Multitran')
        pair = 'DEU <=> RUS'
        search = 'ernährung'
        mes = _('Source: "{}"; pair: "{}"; search: "{}"').format (source
                                                                 ,pair
                                                                 ,search
                                                                 )
        lg.objs.get_plugins().set(source)
        lg.objs.plugins.set_pair(pair)
        sh.objs.get_mes(f, mes, True).show_info()
        data = lg.objs.plugins.request (search = search
                                       ,url = ''
                                       )
        if not data:
            sh.com.rep_empty(f)
            return
        sh.com.run_fast_txt(data)
    
    def get_url(self):
        import logic as lg
        f = '[MClient] tests.Commands.get_url'
        source = 'multitran.com'
        pair = 'RUS <=> XAL'
        search = 'До свидания!'
        mes = 'Source: "{}"; pair: "{}"; search: "{}"'
        mes = mes.format(source, pair, search)
        lg.objs.get_plugins().set(source)
        lg.objs.plugins.set_pair(pair)
        sh.objs.get_mes(f, mes, True).show_info()
        lg.objs.plugins.get_url(search)
    
    def suggest(self):
        import logic as lg
        f = '[MClient] tests.Commands.suggest'
        source = 'multitran.com'
        pair = 'DEU <=> RUS'
        search = 'Scheiße'
        mes = 'Source: "{}"; pair: "{}"; search: "{}"'
        mes = mes.format(source, pair, search)
        lg.objs.get_plugins().set(source)
        lg.objs.plugins.set_pair(pair)
        sh.objs.get_mes(f, mes, True).show_info()
        lg.com.suggest(search)
    
    def _set_timeout(self, module, source, timeout):
        import logic as lg
        f = '[MClient] tests.Commands._set_timeout'
        lg.objs.get_plugins().set(source)
        lg.objs.plugins.set_timeout(timeout)
        mes = _('Source: {}; timeout: {}').format(source, module.TIMEOUT)
        sh.objs.get_mes(f, mes, True).show_debug()
    
    def set_timeout(self):
        import plugins.multitrancom.get as mc
        import plugins.stardict.get as sd
        self._set_timeout (module = sd
                          ,source = _('Offline')
                          ,timeout = 1
                          )
        self._set_timeout (module = mc
                          ,source = _('Multitran')
                          ,timeout = 2
                          )
        self._set_timeout (module = mc
                          ,source = 'multitran.com'
                          ,timeout = 3
                          )
    
    def is_accessible(self):
        import logic as lg
        f = '[MClient] tests.Commands.is_accessible'
        source = _('Offline')
        lg.objs.get_plugins().set(source)
        result = lg.objs.plugins.is_accessible()
        mes = _('Source: {}; accessibility: {}').format(source, result)
        sh.objs.get_mes(f, mes, True).show_debug()
        source = 'multitran.com'
        lg.objs.plugins.set(source)
        result = lg.objs.plugins.is_accessible()
        mes = _('Source: {}; accessibility: {}').format(source, result)
        sh.objs.get_mes(f, mes, True).show_debug()
    
    def welcome(self):
        import logic as lg
        f = '[MClient] tests.Commands.welcome'
        file_w = '/tmp/test.html'
        code = lg.Welcome().run()
        if code:
            sh.WriteTextFile(file_w).write(code)
            sh.Launch(file_w).launch_default()
        else:
            sh.com.rep_empty(f)
    
    def set_pair(self):
        import logic as lg
        f = '[MClient] tests.Commands.set_pair'
        import plugins.multitrancom.get
        pair = 'RUS <=> XAL'
        source = 'multitran.com'
        lg.objs.get_plugins().set(source)
        lg.objs.plugins.set_pair(pair)
        
        mes = f'{source}: {plugins.multitrancom.get.PAIR}'
        sh.objs.get_mes(f, mes, True).show_debug()
        pair = 'XAL <=> RUS'
        source = _('Multitran')
        lg.objs.plugins.set(source)
        lg.objs.plugins.set_pair(pair)
        mes = 'multitrancom: {}'.format(plugins.multitrancom.get.PAIR)
        sh.objs.get_mes(f, mes, True).show_debug()



com = Commands()


if __name__ == '__main__':
    f = '[MClient] tests.__main__'
    sh.com.start()
    ''' #NOTE: Putting QMainWindow.show() or QWidget.show() (without
        explicitly invoking QMainWindow in __main__) in a separate procedure,
        e.g. com.run_welcome, will cause an infinite loop.
    '''
    #mes = com.get_all_subjects()
    #mes = Plugin().run_dsl()
    #mes = Tags().run_dsl()
    #mes = Tags().run_stardict()
    #mes = Elems().run_dsl()
    #mes = Elems().run_stardict()
    #mes = Subjects().run()
    #mes = View().run_dsl()
    mes = View().run_stardict()
    idebug = sh.Debug(f, mes)
    idebug.show()
    #idebug = sh.Debug(f, Tags().run_multitrancom())
    #idebug = sh.Debug(f, Elems().run_multitrancom())
    #idebug = sh.Debug(f, Prioritize().run_multitrancom())
    #idebug = sh.Debug(f, View().run_multitrancom())
    #idebug = sh.Debug(f, Wrap().run_multitrancom())
    # This MUST be on a separate line, the widget will not be shown otherwise
    #idebug.show()
    
    #mes = com.run_speech()
    #sh.objs.get_mes(f, mes).show_debug()
    
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
    sh.objs.get_mes(f, mes, True).show_debug()
    sh.com.end()
