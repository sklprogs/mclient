#!/usr/bin/python3

import shared    as sh
import sharedGUI as sg


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
        sg.fast_txt(result)
    
    def multitranru(self):
        f = '[MClient] tests.Get.multitranru'
        import plugins.multitranru.get as gt
        #search = 'компьютер'
        search  = 'computer'
        url     = 'https://www.multitran.ru/c/m.exe?CL=1&s=computer&l1=1'
        timeout = 6
        timer   = sh.Timer(f)
        timer.start()
        result = gt.Get (search  = search
                        ,url     = url
                        ,timeout = timeout
                        ).run()
        timer.end()
        sg.fast_txt(result)
    
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
        sg.fast_txt(result)



class Tags:
    
    def stardict(self):
        f = '[MClient] tests.Tags.stardict'
        import plugins.stardict.cleanup as sdcleanup
        import plugins.stardict.tags    as sdtags
        file = '/home/pete/.config/mclient/tests/(stardict) EnRu_full - cut.txt'
        text = sh.ReadTextFile(file).get()
        text = sdcleanup.CleanUp(text).run()
        sdtags.Tags (text  = text
                    ,Debug = True
                    ).run()
    
    def multitranru(self):
        f = '[MClient] tests.Tags.multitranru'
        import plugins.multitranru.cleanup as mrcleanup
        import plugins.multitranru.tags    as mrtags
        file = '/home/pete/.config/mclient/tests/(multitran.ru) set.txt'
        text = sh.ReadTextFile(file).get()
        text = mrcleanup.CleanUp(text).run()
        mrtags.Tags (text    = text
                    ,Debug   = True
                    ,Shorten = True
                    ,MaxRow  = 20
                    ,MaxRows = 100
                    ).run()
    
    def multitrancom(self):
        f = '[MClient] tests.Tags.multitrancom'
        import plugins.multitrancom.cleanup as mccleanup
        import plugins.multitrancom.tags    as mctags
        #file = '/home/pete/.config/mclient/tests/(multitran.com) computer.txt'
        file = '/home/pete/.config/mclient/tests/(multitran.com) counting machine (phrases).txt'
        text = sh.ReadTextFile(file).get()
        text = mccleanup.CleanUp(text).run()
        mctags.Tags (text    = text
                    ,Debug   = True
                    ,Shorten = True
                    ,MaxRow  = 20
                    ,MaxRows = 150
                    ).run()



class Plugin:
    
    def stardict(self):
        f = '[MClient] tests.Plugin.stardict'
        import plugins.stardict.run as sr
        search = 'about'
        iplug = sr.Plugin (Debug   = True
                          ,Shorten = False
                          )
        iplug.request(search=search)
    
    def multitranru(self):
        f = '[MClient] tests.Plugin.multitranru'
        import plugins.multitranru.run as mr
        url    = 'https://www.multitran.ru/c/m.exe?CL=1&s=computer&l1=1'
        search = 'computer'
        iplug = mr.Plugin (timeout = 6
                          ,Debug   = True
                          ,Shorten = True
                          ,MaxRow  = 20
                          ,MaxRows = 300
                          )
        iplug.request (url    = url
                      ,search = search
                      )
    
    def multitrancom(self):
        f = '[MClient] tests.Plugin.multitrancom'
        import plugins.multitrancom.run as mc
        #url    = 'https://multitran.com/m.exe?s=computer&l1=1&l2=2&SHL=2'
        #search = 'computer'
        url     = 'https://multitran.com/m.exe?a=3&l1=1&l2=2&s=counting%20machine'
        search  = 'counting machine'
        
        iplug = mc.Plugin (timeout = 6
                          ,Debug   = True
                          ,Shorten = True
                          ,MaxRow  = 20
                          ,MaxRows = 150
                          )
        iplug.request (url    = url
                      ,search = search
                      )



class Commands:
    
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
        sg.fast_txt(data)
    
    def request(self):
        f = '[MClient] tests.Commands.request'
        source = _('Multitran')
        pair   = 'DEU <=> RUS'
        search = 'ernährung'
        message = 'Source: "%s"; pair: "%s"; search: "%s"' % (source,pair,search)
        lg.objs.plugins().set(source)
        lg.objs._plugins.set_pair(pair)
        sh.log.append (f,_('INFO')
                      ,message
                      )
        data = lg.objs._plugins.request (search = search
                                        ,url    = ''
                                        )
        if data:
            sg.fast_txt(data)
        else:
            sh.com.empty(f)
    
    def get_url(self):
        f = '[MClient] tests.Commands.get_url'
        #1
        source  = 'multitran.ru'
        pair    = 'DEU <=> RUS'
        search  = 'привет'
        message = 'Source: "%s"; pair: "%s"; search: "%s"' % (source,pair,search)
        lg.objs.plugins().set(source)
        lg.objs._plugins.set_pair(pair)
        sh.log.append (f,_('INFO')
                      ,message
                      )
        lg.objs._plugins.get_url(search)
        #2
        source  = 'multitran.com'
        pair    = 'RUS <=> XAL'
        search  = 'До свидания!'
        message = 'Source: "%s"; pair: "%s"; search: "%s"' % (source,pair,search)
        lg.objs.plugins().set(source)
        lg.objs._plugins.set_pair(pair)
        sh.log.append (f,_('INFO')
                      ,message
                      )
        lg.objs._plugins.get_url(search)
        #3
        ''' Since 'plugins.multitran.get.Commands.get_url' has several
            modes, this default request should actually return the same
            as 'multitran.ru' (if 'pair' and 'search' are the same).
        '''
        source  = _('Multitran')
        pair    = 'XAL <=> RUS'
        search  = 'До свидания!'
        message = 'Source: "%s"; pair: "%s"; search: "%s"' % (source,pair,search)
        lg.objs.plugins().set(source)
        lg.objs._plugins.set_pair(pair)
        sh.log.append (f,_('INFO')
                      ,message
                      )
        lg.objs._plugins.get_url(search)
    
    def suggest(self):
        f = '[MClient] tests.Commands.suggest'
        #1
        source  = 'multitran.ru'
        pair    = 'ENG <=> RUS'
        search  = 'привет'
        message = 'Source: "%s"; pair: "%s"; search: "%s"' % (source,pair,search)
        lg.objs.plugins().set(source)
        lg.objs._plugins.set_pair(pair)
        sh.log.append (f,_('INFO')
                      ,message
                      )
        lg.com.suggest(search)
        #2
        source  = 'multitran.com'
        pair    = 'DEU <=> RUS'
        search  = 'Scheiße'
        message = 'Source: "%s"; pair: "%s"; search: "%s"' % (source,pair,search)
        lg.objs.plugins().set(source)
        lg.objs._plugins.set_pair(pair)
        sh.log.append (f,_('INFO')
                      ,message
                      )
        lg.com.suggest(search)
        #3
        source  = _('Multitran')
        pair    = 'FRA <=> RUS'
        search  = 'œuf'
        message = 'Source: "%s"; pair: "%s"; search: "%s"' % (source,pair,search)
        lg.objs.plugins().set(source)
        lg.objs._plugins.set_pair(pair)
        sh.log.append (f,_('INFO')
                      ,message
                      )
        lg.com.suggest(search)
    
    def _set_timeout(self,module,source,timeout):
        f = '[MClient] tests.Commands._set_timeout'
        lg.objs.plugins().set(source)
        lg.objs._plugins.set_timeout(timeout)
        message = 'Source: %s; Timeout: %d' % (source,module.TIMEOUT)
        sh.log.append (f,_('DEBUG')
                      ,message
                      )
    
    def set_timeout(self):
        f = '[MClient] tests.Commands.set_timeout'
        import plugins.multitrancom.get as mc
        import plugins.multitranru.get  as mr
        import plugins.stardict.get     as sd
        self._set_timeout (module  = sd
                          ,source  = _('Offline')
                          ,timeout = 1
                          )
        self._set_timeout (module  = mr
                          ,source  = _('Multitran')
                          ,timeout = 2
                          )
        self._set_timeout (module  = mc
                          ,source  = _('Multitran')
                          ,timeout = 2
                          )
        self._set_timeout (module  = mc
                          ,source  = 'multitran.com'
                          ,timeout = 3
                          )
        self._set_timeout (module  = mr
                          ,source  = 'multitran.ru'
                          ,timeout = 4
                          )
    
    def accessibility(self):
        f = '[MClient] tests.Commands.accessibility'
        source = _('Offline')
        lg.objs.plugins().set(source)
        result  = lg.objs._plugins.accessible()
        message = 'Source: {}; Accessibility: {}'.format(source,result)
        sh.log.append (f,_('DEBUG')
                      ,message
                      )
        source = 'multitran.ru'
        lg.objs._plugins.set(source)
        result  = lg.objs._plugins.accessible()
        message = 'Source: {}; Accessibility: {}'.format(source,result)
        sh.log.append (f,_('DEBUG')
                      ,message
                      )
        source = 'multitran.com'
        lg.objs._plugins.set(source)
        result  = lg.objs._plugins.accessible()
        message = 'Source: {}; Accessibility: {}'.format(source,result)
        sh.log.append (f,_('DEBUG')
                      ,message
                      )
        source = _('Multitran')
        lg.objs._plugins.set(source)
        result  = lg.objs._plugins.accessible()
        message = 'Source: {}; Accessibility: {}'.format(source,result)
        sh.log.append (f,_('DEBUG')
                      ,message
                      )
    
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
        import plugins.multitranru.get
        import plugins.multitrancom.get
        pair   = 'RUS <=> XAL'
        source = 'multitran.com'
        lg.objs.plugins().set(source)
        lg.objs._plugins.set_pair(pair)
        
        sh.log.append (f,_('DEBUG')
                      ,source + ': ' + plugins.multitrancom.get.PAIR
                      )
        pair   = 'ENG <=> DEU'
        source = 'multitran.ru'
        lg.objs._plugins.set(source)
        lg.objs._plugins.set_pair(pair)
        sh.log.append (f,_('DEBUG')
                      ,source + ': ' + plugins.multitranru.get.PAIR
                      )
        pair   = 'XAL <=> RUS'
        source = _('Multitran')
        lg.objs._plugins.set(source)
        lg.objs._plugins.set_pair(pair)
        sh.log.append (f,_('DEBUG')
                      ,'multitranru: ' + plugins.multitranru.get.PAIR
                      )
        sh.log.append (f,_('DEBUG')
                      ,'multitrancom: ' + plugins.multitrancom.get.PAIR
                      )
        pair   = 'XAL <=> FAIL'
        source = _('Multitran')
        lg.objs._plugins.set(source)
        lg.objs._plugins.set_pair(pair)
        sh.log.append (f,_('DEBUG')
                      ,'multitranru: ' + plugins.multitranru.get.PAIR
                      )
        sh.log.append (f,_('DEBUG')
                      ,'multitrancom: ' + plugins.multitrancom.get.PAIR
                      )


com = Commands()


if __name__ == '__main__':
    f = '[MClient] plugins.stardict.tags.__main__'
    sg.objs.start()
    import logic as lg
    '''
    lg.objs.plugins().set(_('Multitran'))
    lg.objs._plugins.set_pair('DEU <=> RUS')
    lg.objs._plugins.request(search='ernährung')
    '''
    lg.objs.plugins().set('multitran.com')
    lg.objs._plugins.set_pair('ENG <=> RUS')
    data = lg.objs._plugins.request (search = 'засека'
                                    ,url    = 'https://www.multitran.com/m.exe?a=3&sc=24&s=%D0%B7%D0%B0%D1%81%D0%B5%D0%BA%D0%B0&l1=2&l2=1&SHL=2'
                                    )
    data = [list(row) for row in data]
    print(data[0])
    '''
    data[0][13] = 0
    cldata = []
    for i in range(len(data)):
        row = [i,data[i][7],data[i][8],data[i][13],data[i][2],data[i][3]
              ,data[i][4],data[i][5]
              ]
        cldata.append(row)
    import cells as cl
    cells = cl.Cells (data         = cldata
                     ,cols         = ('dic','wform','transc','speech')
                     ,collimit     = 8
                     ,phrase_dic   = ''
                     ,Reverse      = False
                     ,ExpandSpeech = False
                     )
    cells.run()
    cells.debug()
    '''
    sg.objs.end()
