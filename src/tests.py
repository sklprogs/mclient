#!/usr/bin/python3

import shared    as sh
import sharedGUI as sg


class Get:
    
    def multitranru(self):
        f = '[MClient] tests.Get.multitranru'
        import plugins.multitranru.run as mr
        #search  = 'компьютер'
        search   = 'computer'
        url      = 'https://www.multitran.ru/c/m.exe?CL=1&s=computer&l1=1'
        encoding = 'windows-1251'
        timeout  = 6
        timer = sh.Timer(f)
        timer.start()
        result = mr.run (search   = search
                        ,url      = url
                        ,encoding = encoding
                        ,timeout  = timeout
                        )
        timer.end()
        return result
    
    def stardict(self):
        f = '[MClient] tests.Get.stardict'
        import logic                as lg
        import plugins.stardict.run as sd
        #search = 'компьютер'
        search  = 'computer'
        timer   = sh.Timer(f)
        timer.start()
        result = sd.run(lg.objs.default().dics(),search)
        timer.end()
        return result



class Tags:
    
    def stardict(self):
        f = '[MClient] tests.Tags.stardict'
        import plugins.stardict.cleanup as sdcleanup
        import plugins.stardict.tags    as sdtags
        file = '/home/pete/.config/mclient/tests/sdict_EnRu_full - cut.txt'
        text = sh.ReadTextFile(file).get()
        text  = sdcleanup.run(text)
        timer = sh.Timer(f)
        timer.start()
        tags  = sdtags.Tags(text)
        tags.run()
        timer.end()
        tags.debug_tags()
        tags.debug_blocks (Shorten = 1
                          ,MaxRow  = 30
                          ,MaxRows = 300
                          )
    
    def multitranru(self):
        f = '[MClient] tests.Tags.multitranru'
        import plugins.multitranru.cleanup as mrcleanup
        import plugins.multitranru.tags    as mrtags
        file = '/home/pete/.config/mclient/tests/(multitran.ru) set.ru'
        text = sh.ReadTextFile(file).get()
        text  = mrcleanup.run(text)
        timer = sh.Timer(f)
        timer.start()
        tags  = mrtags.Tags(text)
        tags.run()
        timer.end()
        tags.debug_tags()
        tags.debug_blocks (Shorten = 1
                          ,MaxRow  = 30
                          ,MaxRows = 300
                          )


get  = Get()
tags = Tags()


if __name__ == '__main__':
    f = '[MClient] plugins.stardict.tags.__main__'
    sg.objs.start()
    tags.multitranru()
    sg.objs.end()
