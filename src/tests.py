#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _

DEBUG = True


class Block:
    
    def __init__(self):
        self.id_      = None # (00) Autoincrement
        self.artid    = 0    # (01) ARTICLEID
        self.dica     = ''   # (02) DICA (abbreviation)
        self.wforma   = ''   # (03) WFORMA
        self.speecha  = ''   # (04) SPEECHA
        self.transca  = ''   # (05) TRANSCA
        self.terma    = ''   # (06) TERMA
        self.type_    = ''   # (07) TYPE
        self.text     = ''   # (08) TEXT
        self.url      = ''   # (09) URL
        self.block    = 0    # (10) BLOCK
        self.priority = 0    # (11) PRIORITY
        self.select   = 0    # (12) SELECTABLE
        self.same     = 0    # (13) SAMECELL
        self.cellno   = 0    # (14) CELLNO
        self.rowno    = -1   # (15) ROWNO
        self.colno    = -1   # (16) COLNO
        self.pos1     = -1   # (17) POS1
        self.pos2     = -1   # (18) POS2
        self.node1    = ''   # (19) NODE1
        self.node2    = ''   # (20) NODE2
        self.offpos1  = -1   # (21) OFFPOS1
        self.offpos2  = -1   # (22) OFFPOS2
        self.bbox1    = -1   # (23) BBOX1
        self.bbox2    = -1   # (24) BBOX2
        self.bboy1    = -1   # (25) BBOY1
        self.bboy2    = -1   # (26) BBOY2
        self.textlow  = ''   # (27) TEXTLOW
        self.ignore   = 0    # (28) IGNORE
        self.speech   = 0    # (29) SPEECHPR
        self.dicaf    = ''   # (30) DICA (full title)
    
    def dump(self):
        return (self.id_
               ,self.artid
               ,self.dica
               ,self.wforma
               ,self.speecha
               ,self.transca
               ,self.terma
               ,self.type_
               ,self.text
               ,self.url
               ,self.block
               ,self.priority
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
               ,self.dicaf
               )



class Get:
    
    def run_multitrancom(self):
        f = '[MClient] tests.Get.run_multitrancom'
        import plugins.multitrancom.get as gt
        #search = 'компьютер'
        search  = 'computer'
        url     = 'https://multitran.com/m.exe?s=computer&l1=1&l2=2'
        timeout = 6
        timer   = sh.Timer(f)
        timer.start()
        result = gt.Get (search  = search
                        ,url     = url
                        ,timeout = timeout
                        ).run()
        timer.end()
        sh.com.run_fast_txt(result)
    
    def run_stardict(self):
        f = '[MClient] tests.Get.run_stardict'
        import logic as lg
        import plugins.stardict.get as sd
        #search = 'компьютер'
        search  = 'computer'
        timer   = sh.Timer(f)
        timer.start()
        result = sd.Get(search).run()
        timer.end()
        sh.com.run_fast_txt(result)



class Tags:
    
    def run_dsl(self):
        f = '[MClient] tests.Tags.run_dsl'
        import plugins.dsl.get
        import plugins.dsl.tags
        plugins.dsl.get.PATH = sh.Home('mclient').add_config('dics')
        tag_lst = plugins.dsl.get.Get('computer').run()
        plugins.dsl.tags.Tags (lst   = tag_lst
                              ,Debug = DEBUG
                              ).run()
    
    def analyze_tag(self):
        import plugins.multitrancom.tags as tg
        #tag = '<tr><td class="subj" width="1"><a href="https://www.multitran.com/m.exe?a=110&amp;l1=2&amp;l2=1&amp;s=%D1%82%D1%80%D0%BE%D1%81&amp;sc=371" title="Автоматика">автомат.'
        #tag = '''<tr><td class="subj" width="1"><a href="https://www.multitran.com/m.exe?a=110&amp;l1=2&amp;l2=1&amp;s=%D1%82%D1%80%D0%BE%D1%81&amp;sc=0" title="Общая лексика">общ.'''
        tag = '<tr><td class="subj" width="1"><a href="https://www.multitran.com/m.exe?a=110&amp;l1=2&amp;l2=1&amp;s=%D1%82%D1%80%D0%BE%D1%81&amp;sc=134" title="Электроника">эл.'
        itag = tg.AnalyzeTag(tag)
        itag.run()
        itag.debug()
    
    def run_stardict(self):
        f = '[MClient] tests.Tags.run_stardict'
        import plugins.stardict.cleanup as sdcleanup
        import plugins.stardict.tags    as sdtags
        file = '/home/pete/.config/mclient/tests/(stardict) EnRu_full - cut.txt'
        text = sh.ReadTextFile(file).get()
        text = sdcleanup.CleanUp(text).run()
        sdtags.Tags (text  = text
                    ,Debug = DEBUG
                    ).run()
    
    def run_multitrancom(self):
        f = '[MClient] tests.Tags.run_multitrancom'
        import plugins.multitrancom.cleanup as mccleanup
        import plugins.multitrancom.tags    as mctags
        ''' #NOTE: The file should be generated with
            'plugins.multitrancom.get.Get', otherwise, 'Tags' will fail
            to set 'dic' and some other types.
        '''
        file = '/home/pete/bin/mclient/tests/multitrancom/трос.txt'
        text = sh.ReadTextFile(file).get()
        text = mccleanup.CleanUp(text).run()
        mctags.Tags (text   = text
                    ,Debug  = DEBUG
                    ,maxrow = 30
                    ).run()



class Plugin:
    
    def run_multitrandem(self):
        f = '[MClient] tests.Plugin.run_multitrandem'
        import plugins.multitrandem.get
        import plugins.multitrandem.run as mb
        #search = 'Kafir'
        #search = 'abasin'
        #search = 'a posteriori'
        #search = 'abed'
        #search = 'accommodation coefficient'
        #search = 'according'
        #search = 'фабричный корпус'
        #search = 'build market'
        #search = 'bunching device'
        #search = 'valve rocker shank'
        # пласт, характеризуемый определённой скоростью
        search  = 'velocity bed'
        #отравление хинной коркой и её алкалоидами = quininism
        url    = ''
        
        plugins.multitrandem.get.PATH = '/home/pete/.config/mclient/dics/eng_rus'
        iplug = mb.Plugin (Debug   = DEBUG
                          ,maxrow  = 20
                          ,maxrows = 150
                          )
        
        blocks = iplug.request (url    = url
                               ,search = search
                               )
        if not blocks:
            blocks = []
        for i in range(len(blocks)):
            mes = '{}: {}: "{}"'.format (i,blocks[i].type_
                                        ,blocks[i].text
                                        )
            print(mes)
    
    def run_stardict(self):
        f = '[MClient] tests.Plugin.run_stardict'
        import plugins.stardict.run as sr
        search = 'about'
        iplug = sr.Plugin(Debug=DEBUG)
        iplug.request(search=search)
    
    def run_dsl(self):
        f = '[MClient] tests.Plugin.run_dsl'
        import plugins.dsl.get
        import plugins.dsl.run as dr
        plugins.dsl.get.PATH = sh.Home('mclient').add_config('dics')
        #search = 'компьютер'
        search  = 'computer'
        iplug = dr.Plugin(Debug=DEBUG)
        iplug.request(search=search)
        mes = _('Number of blocks: {}').format(len(iplug.blocks))
        sh.objs.get_mes(f,mes,True).show_debug()
        mes = _('Web-page:') + '\n' + iplug.htm
        sh.com.run_fast_debug(f,mes)
        mes = _('Text:') + '\n' + iplug.text
        sh.com.run_fast_debug(f,mes)
    
    def run_multitrancom(self):
        f = '[MClient] tests.Plugin.run_multitrancom'
        import plugins.multitrancom.run as mc
        #url    = 'https://www.multitran.com/m.exe?s=memory%20pressure&l1=2&l2=1&SHL=2'
        #search = 'memory pressure'
        #url    = 'https://www.multitran.com/m.exe?s=nucleoside%20reverse%20transcriptase%20inhibitors&l1=2&l2=1&SHL=2'
        #search = 'nucleoside reverse transcriptase inhibitors'
        #url    = 'https://www.multitran.com/m.exe?s=%D0%BD%D1%83%D0%BA%D0%BB%D0%B5%D0%B8%D0%BD%D0%BE%D0%B2%D1%8B%D0%B9&l1=2&l2=1&SHL=2'
        #search = 'нуклеиновый'
        url     = 'https://www.multitran.com/m.exe?a=3&l1=2&l2=1&s=%D0%B2%2B%D1%8F%D0%B1%D0%BB%D0%BE%D1%87%D0%BA%D0%BE&SHL=2'
        search  = '47 фраз'
        
        iplug = mc.Plugin (Debug   = DEBUG
                          ,maxrow  = 20
                          ,maxrows = 150
                          )
        iplug.request (url    = url
                      ,search = search
                      )



class Commands:
    
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
                        lst.append('{}-{}'.format(xlang,lang))
                for xlang in pairs2:
                    if xlang not in pairs1:
                        lst.append('{}-{}'.format(lang,xlang))
        lst = list(set(lst))
        lst.sort()
        mes = _('The following pairs are not supported:\n{}')
        mes = mes.format(lst)
        sh.objs.get_mes(f,mes,True).show_info()
    
    def compare_elems(self):
        f = '[MClient] tests.Commands.compare_elems'
        import plugins.multitran.elems as el
        data1 = []
        data2 = []
        # Create blocks
        #1 #1
        block = list(Block().dump())
        block[2]  = 'Общая лексика' # DICA
        block[30] = 'общ.'          # DICAF
        block[7]  = 'term'          # TYPE
        block[8]  = 'hello'         # TEXT
        data1.append(block)
        #1 #2
        block = list(Block().dump())
        block[2]  = 'Общая лексика' # DICA
        block[30] = 'общ.'          # DICAF
        block[7]  = 'comment'       # TYPE
        block[8]  = 'yes'           # TEXT
        data1.append(block)
        #1 #3
        block = list(Block().dump())
        block[2]  = 'Общая лексика' # DICA
        block[30] = 'общ.'          # DICAF
        block[7]  = 'term'          # TYPE
        block[8]  = 'goodbye'       # TEXT
        data1.append(block)
        #2 #1
        block = list(Block().dump())
        block[2]  = 'Общая лексика' # DICA
        block[30] = 'общ.'          # DICAF
        block[7]  = 'term'          # TYPE
        block[8]  = 'goodbye'       # TEXT
        data2.append(block)
        #2 #2
        block = list(Block().dump())
        block[2]  = 'Физиология'    # DICA
        block[30] = 'физиол.'       # DICAF
        block[7]  = 'comment'       # TYPE
        block[8]  = 'yes'           # TEXT
        data2.append(block)
        #2 #3
        block = list(Block().dump())
        block[2]  = 'Общая лексика' # DICA
        block[30] = 'общ.'          # DICAF
        block[7]  = 'term'          # TYPE
        block[8]  = 'hello'         # TEXT
        data2.append(block)
        # Compare
        data = el.Elems(data1,data2).run()
        data = [str(item) for item in data]
        data = '\n'.join(data)
        sh.com.run_fast_txt(data)
    
    def request(self):
        f = '[MClient] tests.Commands.request'
        source = _('Multitran')
        pair   = 'DEU <=> RUS'
        search = 'ernährung'
        mes = 'Source: "{}"; pair: "{}"; search: "{}"'.format (source
                                                              ,pair
                                                              ,search
                                                              )
        lg.objs.get_plugins().set(source)
        lg.objs.plugins.set_pair(pair)
        sh.objs.get_mes(f,mes,True).show_info()
        data = lg.objs.plugins.request (search = search
                                       ,url    = ''
                                       )
        if data:
            sh.com.run_fast_txt(data)
        else:
            sh.com.rep_empty(f)
    
    def get_url(self):
        f = '[MClient] tests.Commands.get_url'
        source = 'multitran.com'
        pair   = 'RUS <=> XAL'
        search = 'До свидания!'
        mes    = 'Source: "{}"; pair: "{}"; search: "{}"'
        mes    = mes.format(source,pair,search)
        lg.objs.get_plugins().set(source)
        lg.objs.plugins.set_pair(pair)
        sh.objs.get_mes(f,mes,True).show_info()
        lg.objs.plugins.get_url(search)
    
    def suggest(self):
        f = '[MClient] tests.Commands.suggest'
        source = 'multitran.com'
        pair   = 'DEU <=> RUS'
        search = 'Scheiße'
        mes    = 'Source: "{}"; pair: "{}"; search: "{}"'
        mes    = mes.format(source,pair,search)
        lg.objs.get_plugins().set(source)
        lg.objs.plugins.set_pair(pair)
        sh.objs.get_mes(f,mes,True).show_info()
        lg.com.suggest(search)
    
    def _set_timeout(self,module,source,timeout):
        f = '[MClient] tests.Commands._set_timeout'
        lg.objs.get_plugins().set(source)
        lg.objs.plugins.set_timeout(timeout)
        mes = 'Source: {}; Timeout: {}'.format (source
                                               ,module.TIMEOUT
                                               )
        sh.objs.get_mes(f,mes,True).show_debug()
    
    def set_timeout(self):
        f = '[MClient] tests.Commands.set_timeout'
        import plugins.multitrancom.get as mc
        import plugins.stardict.get     as sd
        self._set_timeout (module  = sd
                          ,source  = _('Offline')
                          ,timeout = 1
                          )
        self._set_timeout (module  = mc
                          ,source  = _('Multitran')
                          ,timeout = 2
                          )
        self._set_timeout (module  = mc
                          ,source  = 'multitran.com'
                          ,timeout = 3
                          )
    
    def accessibility(self):
        f = '[MClient] tests.Commands.accessibility'
        source = _('Offline')
        lg.objs.get_plugins().set(source)
        result  = lg.objs.plugins.is_accessible()
        mes     = 'Source: {}; Accessibility: {}'.format(source,result)
        sh.objs.get_mes(f,mes,True).show_debug()
        source = 'multitran.com'
        lg.objs.plugins.set(source)
        result  = lg.objs.plugins.is_accessible()
        mes     = 'Source: {}; Accessibility: {}'.format(source,result)
        sh.objs.get_mes(f,mes,True).show_debug()
    
    def welcome(self):
        f = '[MClient] tests.Commands.welcome'
        file_w = '/tmp/test.html'
        code   = lg.Welcome().run()
        if code:
            sh.WriteTextFile(file_w).write(code)
            sh.Launch(file_w).default()
        else:
            sh.com.rep_empty(f)
    
    def set_pair(self):
        f = '[MClient] tests.Commands.set_pair'
        import plugins.multitrancom.get
        pair   = 'RUS <=> XAL'
        source = 'multitran.com'
        lg.objs.get_plugins().set(source)
        lg.objs.plugins.set_pair(pair)
        
        mes = '{}: {}'.format(source,plugins.multitrancom.get.PAIR)
        sh.objs.get_mes(f,mes,True).show_debug()
        pair   = 'XAL <=> RUS'
        source = _('Multitran')
        lg.objs.plugins.set(source)
        lg.objs.plugins.set_pair(pair)
        mes = 'multitrancom: {}'.format(plugins.multitrancom.get.PAIR)
        sh.objs.get_mes(f,mes,True).show_debug()
        
    def translate_gui (self,source,pair
                      ,search,url
                      ):
        f = '[MClient] tests.Commands.translate_gui'
        import mclient
        lg.objs.get_plugins().set(source)
        lg.objs.plugins.set_pair(pair)
        lg.objs.get_request().search = search
        lg.objs.request.url = url
        mclient.objs.webframe().load_article()
        mclient.objs.webframe.gui.show()
    
    def translate_cli (self,source,pair
                      ,search,url,maxrows=100
                      ):
        f = '[MClient] tests.Commands.translate_cli'
        import cells as cl
        lg.objs.get_plugins().set(source)
        lg.objs.plugins.set_pair(pair)
        lg.objs.get_request().search = search
        lg.objs.request.url = url
        data = lg.objs.plugins.request (search = search
                                       ,url    = url
                                       )
        cldata = []
        for i in range(len(data)):
            row = [i,data[i][7],data[i][8],data[i][13],data[i][2]
                  ,data[i][3],data[i][4],data[i][5]
                  ]
            cldata.append(row)
        cells = cl.Cells (data     = cldata
                         ,cols     = ('dic','wform','transc'
                                     ,'speech'
                                     )
                         ,collimit = 8
                         ,phdic    = ''
                         ,Reverse  = False
                         ,ExpandSp = False
                         ,Debug    = DEBUG
                         ,maxrows  = maxrows
                         )
        cells.run()
    
    def translate (self,source,pair
                  ,search,url,maxrows=100
                  ,GUI=False
                  ):
        if GUI:
            self.translate_gui (source  = source
                               ,pair    = pair
                               ,search  = search
                               ,url     = url
                               )
        else:
            self.translate_cli (source  = source
                               ,pair    = pair
                               ,search  = search
                               ,url     = url
                               ,maxrows = maxrows
                               )
            
    
    def run_com_complex(self,GUI=False):
        self.translate (source = 'multitran.com'
                       ,pair   = 'ENG <=> RUS'
                       ,search = 'complex'
                       ,url    = 'https://www.multitran.com/m.exe?s=complex&l1=2&l2=1&SHL=2'
                       ,GUI    = GUI
                       )
    
    def run_com_abatis2(self,GUI=False):
        self.translate (source = 'multitran.com'
                       ,pair   = 'ENG <=> RUS'
                       ,search = 'abatis'
                       ,url    = 'https://www.multitran.com/m.exe?s=abatis&l1=2&l2=1&SHL=2'
                       ,GUI    = GUI
                       )
    
    def run_com_abatis(self,GUI=False):
        self.translate (source = 'multitran.com'
                       ,pair   = 'ENG <=> RUS'
                       ,search = 'засека'
                       ,url    = 'https://www.multitran.com/m.exe?s=%D0%B7%D0%B0%D1%81%D0%B5%D0%BA%D0%B0&l1=2&l2=1&SHL=2'
                       ,GUI    = GUI
                       )
    
    def run_all_ernahrung(self,GUI=False):
        self.translate (source = _('Multitran')
                       ,pair   = 'DEU <=> RUS'
                       ,search = 'ernährung'
                       ,url    = 'https://www.multitran.com/m.exe?s=ern%C3%A4hrung&l1=3&l2=2&SHL=2'
                       ,GUI    = GUI
                       )
    
    def run_com_mud(self,GUI=False):
        self.translate (source = 'multitran.com'
                       ,pair   = 'ENG <=> RUS'
                       ,search = 'mud'
                       ,url    = 'https://multitran.com/m.exe?s=mud&l1=1&l2=2&SHL=2'
                       ,GUI    = GUI
                       )
    
    def run_com_systemwide(self,GUI=False):
        self.translate (source = 'multitran.com'
                       ,pair   = 'ENG <=> RUS'
                       ,search = 'system-wide'
                       ,url    = 'https://www.multitran.com/m.exe?s=system-wide&l1=2&l2=1&SHL=2'
                       ,GUI    = GUI
                       )
    
    def go_keyboard(self,event=None):
        f = '[MClient] tests.Commands.go_keyboard'
        mes = _('Triggered!')
        sh.objs.get_mes(f,mes,True).show_debug()
    
    def copy_text(self,event=None):
        f = '[MClient] tests.Commands.copy_text'
        mes = _('Triggered!')
        sh.objs.get_mes(f,mes,True).show_debug()


com = Commands()


if __name__ == '__main__':
    f = '[MClient] plugins.stardict.tags.__main__'
    sh.com.start()
    #Plugin().run_multitrancom()
    Plugin().run_dsl()
    #Tags().run_dsl()
    sh.com.end()
