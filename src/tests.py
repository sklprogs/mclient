#!/usr/bin/python3

import re
import shared    as sh
import sharedGUI as sg
import page      as pg


class Commands:
    
    def __init__(self):
        pass
    
    def search_local(self,search='test'):
        ext_dics = pg.ExtDics(path=sh.objs.pdir().add('dics'))
        text = ext_dics.get (lang   = 'English'
                            ,search = search
                            )
        '''
        page = Page (search = search
                    ,url    = 'https://www.multitran.ru/c/M.exe?CL=1&s=filter&l1=1'
                    )
        page.run()
        text = page._page
        '''
        words = sh.Words(text,Auto=0)
        words.sent_nos()
        sg.objs.txt().reset_data()
        sg.objs._txt.reset_logic(words=words)
        sg.objs._txt.insert(text)
        sg.objs._txt.show()


if __name__ == '__main__':
    sg.objs.start()
    com = Commands()
    com.search_local('snitch')
    sg.objs.end()
