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
        file = '/home/pete/.config/mclient/tests/(multitran.com) computer.txt'
        text = sh.ReadTextFile(file).get()
        text = mccleanup.CleanUp(text).run()
        mctags.Tags (text    = text
                    ,Debug   = True
                    ,Shorten = True
                    ,MaxRow  = 70
                    ,MaxRows = 10000
                    ).run()



class Plugin:
    
    def stardict(self):
        f = '[MClient] tests.Plugin.stardict'
        import plugins.stardict.run as sr
        blocks = sr.Plugin (search  = 'about'
                           ,Debug   = True
                           ,Shorten = False
                           ).run()
    
    def multitranru(self):
        f = '[MClient] tests.Plugin.multitranru'
        import plugins.multitranru.run as mr
        blocks = mr.Plugin (url     = 'https://www.multitran.ru/c/m.exe?CL=1&s=computer&l1=1'
                           ,search  = 'computer'
                           ,timeout = 6
                           ,Debug   = True
                           ,Shorten = True
                           ,MaxRow  = 20
                           ,MaxRows = 300
                           ).run()
    
    def multitrancom(self):
        f = '[MClient] tests.Plugin.multitrancom'
        import plugins.multitrancom.run as mc
        blocks = mc.Plugin (url     = 'https://multitran.com/m.exe?s=computer&l1=1&l2=2&SHL=2'
                           ,search  = 'computer'
                           ,timeout = 6
                           ,Debug   = True
                           ,Shorten = True
                           ,MaxRow  = 20
                           ,MaxRows = 300
                           ).run()


#get  = Get()
#tags = Tags()
#plug = Plugin()


if __name__ == '__main__':
    f = '[MClient] plugins.stardict.tags.__main__'
    sg.objs.start()
    import logic as lg
    print('Source:',lg.objs.plugins()._source)
    print('Root URL:',lg.objs._plugins.root_url())
    sg.objs.end()
