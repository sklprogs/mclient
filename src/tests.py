#!/usr/bin/python3

import shared    as sh
import sharedGUI as sg


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


if __name__ == '__main__':
    f = '[MClient] plugins.stardict.tags.__main__'
    sg.objs.start()
    import logic as lg
    #lg.objs.plugins().set('multitran.com')
    #search = 'good'
    search  = 'азбука'
    pair    = 'https://www.multitran.ru/c/m.exe?l1=1&l2=2&s=%s'
    print ( lg.com.suggest (search = search
                           ,pair   = pair
                           )
          )
    sg.objs.end()
