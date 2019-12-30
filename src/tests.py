#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _

DEBUG = True


class Block:
    
    def __init__(self):
        self._id        = None # (00) Autoincrement
        self._articleid = 0    # (01) ARTICLEID
        self._dica      = ''   # (02) DICA (abbreviation)
        self._wforma    = ''   # (03) WFORMA
        self._speecha   = ''   # (04) SPEECHA
        self._transca   = ''   # (05) TRANSCA
        self._terma     = ''   # (06) TERMA
        self._type      = ''   # (07) TYPE
        self._text      = ''   # (08) TEXT
        self._url       = ''   # (09) URL
        self._block     = 0    # (10) BLOCK
        self._priority  = 0    # (11) PRIORITY
        self._select    = 0    # (12) SELECTABLE
        self._same      = 0    # (13) SAMECELL
        self._cell_no   = 0    # (14) CELLNO
        self._rowno     = -1   # (15) ROWNO
        self._colno     = -1   # (16) COLNO
        self._pos1      = -1   # (17) POS1
        self._pos2      = -1   # (18) POS2
        self._node1     = ''   # (19) NODE1
        self._node2     = ''   # (20) NODE2
        self._offpos1   = -1   # (21) OFFPOS1
        self._offpos2   = -1   # (22) OFFPOS2
        self._bbox1     = -1   # (23) BBOX1
        self._bbox2     = -1   # (24) BBOX2
        self._bboy1     = -1   # (25) BBOY1
        self._bboy2     = -1   # (26) BBOY2
        self._textlow   = ''   # (27) TEXTLOW
        self._ignore    = 0    # (28) IGNORE
        self._speech    = 0    # (29) SPEECHPR
        self._dicaf     = ''   # (30) DICA (full title)
    
    def dump(self):
        return (self._id
               ,self._articleid
               ,self._dica
               ,self._wforma
               ,self._speecha
               ,self._transca
               ,self._terma
               ,self._type
               ,self._text
               ,self._url
               ,self._block
               ,self._priority
               ,self._select
               ,self._same
               ,self._cell_no
               ,self._rowno
               ,self._colno
               ,self._pos1
               ,self._pos2
               ,self._node1
               ,self._node2
               ,self._offpos1
               ,self._offpos2
               ,self._bbox1
               ,self._bbox2
               ,self._bboy1
               ,self._bboy2
               ,self._textlow
               ,self._ignore
               ,self._speech
               ,self._dicaf
               )



class Get:
    
    def multitrancom(self):
        f = '[MClient] tests.Get.multitrancom'
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
        sh.com.fast_txt(result)
    
    def stardict(self):
        f = '[MClient] tests.Get.stardict'
        import logic                as lg
        import plugins.stardict.get as sd
        #search = 'компьютер'
        search  = 'computer'
        timer   = sh.Timer(f)
        timer.start()
        result = sd.Get(search).run()
        timer.end()
        sh.com.fast_txt(result)



class Tags:
    
    def stardict(self):
        f = '[MClient] tests.Tags.stardict'
        import plugins.stardict.cleanup as sdcleanup
        import plugins.stardict.tags    as sdtags
        file = '/home/pete/.config/mclient/tests/(stardict) EnRu_full - cut.txt'
        text = sh.ReadTextFile(file).get()
        text = sdcleanup.CleanUp(text).run()
        sdtags.Tags (text  = text
                    ,Debug = DEBUG
                    ).run()
    
    def multitrancom(self):
        f = '[MClient] tests.Tags.multitrancom'
        import plugins.multitrancom.cleanup as mccleanup
        import plugins.multitrancom.tags    as mctags
        file = '/home/pete/bin/mclient/tests/multitrancom/трос.txt'
        text = sh.ReadTextFile(file).get()
        text = mccleanup.CleanUp(text).run()
        mctags.Tags (text    = text
                    ,Debug   = DEBUG
                    ,Shorten = True
                    ,MaxRow  = 20
                    ,MaxRows = 150
                    ).run()



class Plugin:
    
    def stardict(self):
        f = '[MClient] tests.Plugin.stardict'
        import plugins.stardict.run as sr
        search = 'about'
        iplug = sr.Plugin (Debug   = DEBUG
                          ,Shorten = False
                          )
        iplug.request(search=search)
    
    def multitrancom(self):
        f = '[MClient] tests.Plugin.multitrancom'
        import plugins.multitrancom.run as mc
        #url    = 'https://www.multitran.com/m.exe?s=memory%20pressure&l1=2&l2=1&SHL=2'
        #search = 'memory pressure'
        url     = 'https://www.multitran.com/m.exe?s=nucleoside%20reverse%20transcriptase%20inhibitors&l1=2&l2=1&SHL=2'
        search  = 'nucleoside reverse transcriptase inhibitors'
        
        iplug = mc.Plugin (Debug   = DEBUG
                          ,Shorten = True
                          ,MaxRow  = 20
                          ,MaxRows = 150
                          )
        iplug.request (url    = url
                      ,search = search
                      )



class Commands:
    
    def nonpairs(self):
        ''' Get languages that are not supported by multitran.com for
            both directions.
        '''
        f = '[MClient] tests.Commands.nonpairs'
        import plugins.multitrancom.pairs as pairs
        lst = []
        for lang in pairs.LANGS:
            pairs1 = pairs.objs.pairs().pairs1(lang)
            pairs2 = pairs.objs.pairs().pairs2(lang)
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
        sh.objs.mes(f,mes,True).info()
    
    def compare_elems(self):
        f = '[MClient] tests.Commands.compare_elems'
        import plugins.multitran.elems as el
        data1 = []
        data2 = []
        # Create blocks
        #1 #1
        block = list(Block().dump())
        # DICA
        block[2]  = 'Общая лексика'
        # DICAF
        block[30] = 'общ.'
        # TYPE
        block[7]  = 'term'
        # TEXT
        block[8]  = 'hello'
        data1.append(block)
        #1 #2
        block = list(Block().dump())
        # DICA
        block[2]  = 'Общая лексика'
        # DICAF
        block[30] = 'общ.'
        # TYPE
        block[7]  = 'comment'
        # TEXT
        block[8]  = 'yes'
        data1.append(block)
        #1 #3
        block = list(Block().dump())
        # DICA
        block[2]  = 'Общая лексика'
        # DICAF
        block[30] = 'общ.'
        # TYPE
        block[7]  = 'term'
        # TEXT
        block[8]  = 'goodbye'
        data1.append(block)
        #2 #1
        block = list(Block().dump())
        # DICA
        block[2]  = 'Общая лексика'
        # DICAF
        block[30] = 'общ.'
        # TYPE
        block[7]  = 'term'
        # TEXT
        block[8]  = 'goodbye'
        data2.append(block)
        #2 #2
        block = list(Block().dump())
        # DICA
        block[2]  = 'Физиология'
        # DICAF
        block[30] = 'физиол.'
        # TYPE
        block[7]  = 'comment'
        # TEXT
        block[8]  = 'yes'
        data2.append(block)
        #2 #3
        block = list(Block().dump())
        # DICA
        block[2]  = 'Общая лексика'
        # DICAF
        block[30] = 'общ.'
        # TYPE
        block[7]  = 'term'
        # TEXT
        block[8]  = 'hello'
        data2.append(block)
        # Compare
        data = el.Elems(data1,data2).run()
        data = [str(item) for item in data]
        data = '\n'.join(data)
        sh.com.fast_txt(data)
    
    def request(self):
        f = '[MClient] tests.Commands.request'
        source = _('Multitran')
        pair   = 'DEU <=> RUS'
        search = 'ernährung'
        mes = 'Source: "{}"; pair: "{}"; search: "{}"'.format (source
                                                              ,pair
                                                              ,search
                                                              )
        lg.objs.plugins().set(source)
        lg.objs._plugins.set_pair(pair)
        sh.objs.mes(f,mes,True).info()
        data = lg.objs._plugins.request (search = search
                                        ,url    = ''
                                        )
        if data:
            sh.com.fast_txt(data)
        else:
            sh.com.empty(f)
    
    def get_url(self):
        f = '[MClient] tests.Commands.get_url'
        source  = 'multitran.com'
        pair    = 'RUS <=> XAL'
        search  = 'До свидания!'
        mes     = 'Source: "{}"; pair: "{}"; search: "{}"'
        mes     = mes.format(source,pair,search)
        lg.objs.plugins().set(source)
        lg.objs._plugins.set_pair(pair)
        sh.objs.mes(f,mes,True).info()
        lg.objs._plugins.get_url(search)
    
    def suggest(self):
        f = '[MClient] tests.Commands.suggest'
        source  = 'multitran.com'
        pair    = 'DEU <=> RUS'
        search  = 'Scheiße'
        mes     = 'Source: "{}"; pair: "{}"; search: "{}"'
        mes     = mes.format(source,pair,search)
        lg.objs.plugins().set(source)
        lg.objs._plugins.set_pair(pair)
        sh.objs.mes(f,mes,True).info()
        lg.com.suggest(search)
    
    def _set_timeout(self,module,source,timeout):
        f = '[MClient] tests.Commands._set_timeout'
        lg.objs.plugins().set(source)
        lg.objs._plugins.set_timeout(timeout)
        mes = 'Source: {}; Timeout: {}'.format (source
                                               ,module.TIMEOUT
                                               )
        sh.objs.mes(f,mes,True).debug()
    
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
        lg.objs.plugins().set(source)
        result  = lg.objs._plugins.accessible()
        mes     = 'Source: {}; Accessibility: {}'.format(source,result)
        sh.objs.mes(f,mes,True).debug()
        source = 'multitran.com'
        lg.objs._plugins.set(source)
        result  = lg.objs._plugins.accessible()
        mes     = 'Source: {}; Accessibility: {}'.format(source,result)
        sh.objs.mes(f,mes,True).debug()
    
    def welcome(self):
        f = '[MClient] tests.Commands.welcome'
        file_w = '/tmp/test.html'
        code   = lg.Welcome().run()
        if code:
            sh.WriteTextFile(file_w).write(code)
            sh.Launch(file_w).default()
        else:
            sh.com.empty(f)
    
    def set_pair(self):
        f = '[MClient] tests.Commands.set_pair'
        import plugins.multitrancom.get
        pair   = 'RUS <=> XAL'
        source = 'multitran.com'
        lg.objs.plugins().set(source)
        lg.objs._plugins.set_pair(pair)
        
        mes = '{}: {}'.format(source,plugins.multitrancom.get.PAIR)
        sh.objs.mes(f,mes,True).debug()
        pair   = 'XAL <=> RUS'
        source = _('Multitran')
        lg.objs._plugins.set(source)
        lg.objs._plugins.set_pair(pair)
        mes = 'multitrancom: {}'.format(plugins.multitrancom.get.PAIR)
        sh.objs.mes(f,mes,True).debug()
        
    def translate_gui (self,source,pair
                      ,search,url
                      ):
        f = '[MClient] tests.Commands.translate_gui'
        import mclient
        lg.objs.plugins().set(source)
        lg.objs._plugins.set_pair(pair)
        lg.objs.request()._search = search
        lg.objs._request._url     = url
        mclient.objs.webframe().load_article()
        mclient.objs._webframe.gui.show()
    
    def translate_cli (self,source,pair
                      ,search,url,MaxRows=100
                      ):
        f = '[MClient] tests.Commands.translate_cli'
        import cells as cl
        lg.objs.plugins().set(source)
        lg.objs._plugins.set_pair(pair)
        lg.objs.request()._search = search
        lg.objs._request._url     = url
        data   = lg.objs._plugins.request (search = search
                                          ,url    = url
                                          )
        cldata = []
        for i in range(len(data)):
            row = [i,data[i][7],data[i][8],data[i][13],data[i][2]
                  ,data[i][3],data[i][4],data[i][5]
                  ]
            cldata.append(row)
        cells = cl.Cells (data         = cldata
                         ,cols         = ('dic','wform','transc'
                                         ,'speech'
                                         )
                         ,collimit     = 8
                         ,phrase_dic   = ''
                         ,Reverse      = False
                         ,ExpandSpeech = False
                         ,Debug        = DEBUG
                         ,MaxRows      = MaxRows
                         )
        cells.run()
    
    def translate (self,source,pair
                  ,search,url,MaxRows=100
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
                               ,MaxRows = MaxRows
                               )
            
    
    def com_complex(self,GUI=False):
        self.translate (source = 'multitran.com'
                       ,pair   = 'ENG <=> RUS'
                       ,search = 'complex'
                       ,url    = 'https://www.multitran.com/m.exe?s=complex&l1=2&l2=1&SHL=2'
                       ,GUI    = GUI
                       )
    
    def com_abatis2(self,GUI=False):
        self.translate (source = 'multitran.com'
                       ,pair   = 'ENG <=> RUS'
                       ,search = 'abatis'
                       ,url    = 'https://www.multitran.com/m.exe?s=abatis&l1=2&l2=1&SHL=2'
                       ,GUI    = GUI
                       )
    
    def com_abatis(self,GUI=False):
        self.translate (source = 'multitran.com'
                       ,pair   = 'ENG <=> RUS'
                       ,search = 'засека'
                       ,url    = 'https://www.multitran.com/m.exe?s=%D0%B7%D0%B0%D1%81%D0%B5%D0%BA%D0%B0&l1=2&l2=1&SHL=2'
                       ,GUI    = GUI
                       )
    
    def all_ernahrung(self,GUI=False):
        self.translate (source = _('Multitran')
                       ,pair   = 'DEU <=> RUS'
                       ,search = 'ernährung'
                       ,url    = 'https://www.multitran.com/m.exe?s=ern%C3%A4hrung&l1=3&l2=2&SHL=2'
                       ,GUI    = GUI
                       )
    
    def com_mud(self,GUI=False):
        self.translate (source = 'multitran.com'
                       ,pair   = 'ENG <=> RUS'
                       ,search = 'mud'
                       ,url    = 'https://multitran.com/m.exe?s=mud&l1=1&l2=2&SHL=2'
                       ,GUI    = GUI
                       )
    
    def com_systemwide(self,GUI=False):
        self.translate (source = 'multitran.com'
                       ,pair   = 'ENG <=> RUS'
                       ,search = 'system-wide'
                       ,url    = 'https://www.multitran.com/m.exe?s=system-wide&l1=2&l2=1&SHL=2'
                       ,GUI    = GUI
                       )
    
    def go_keyboard(self,event=None):
        f = '[MClient] tests.Commands.go_keyboard'
        mes = _('Triggered!')
        sh.objs.mes(f,mes,True).debug()
    
    def copy_text(self,event=None):
        f = '[MClient] tests.Commands.copy_text'
        mes = _('Triggered!')
        sh.objs.mes(f,mes,True).debug()


com = Commands()


if __name__ == '__main__':
    f = '[MClient] plugins.stardict.tags.__main__'
    sh.com.start()
    Plugin().multitrancom()
    sh.com.end()
