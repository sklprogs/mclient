#!/usr/bin/python3

import shared    as sh
import sharedGUI as sg
import logic as lg
import plugins.stardict.run    as sd
import plugins.multitranru.run as mr


class Commands:
    
    def __init__(self):
        pass


if __name__ == '__main__':
    sg.objs.start()
    com = Commands()
    #search  = 'компьютер'
    search   = 'computer'
    url      = 'https://www.multitran.ru/c/m.exe?CL=1&s=computer&l1=1'
    encoding = 'windows-1251'
    timeout  = 6
    timer = sh.Timer('tests (1)')
    timer.start()
    #result = sd.run(lg.objs.default().dics(),search)
    result = mr.run (search   = search
                    ,url      = url
                    ,encoding = encoding
                    ,timeout  = timeout
                    )
    timer.end()
    '''
    timer = sh.Timer('tests (2)')
    timer.start()
    result2 = sd.run(lg.objs.default().dics(),'lift')
    timer.end()
    sg.fast_txt(result+result2)
    '''
    sg.fast_txt(result)
    sg.objs.end()
