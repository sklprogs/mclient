#!/usr/bin/python3

import re
import shared    as sh
import sharedGUI as sg
import page      as pg
import logic     as lg


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
        
    def order(self):
        print('Priorities (1):',lg.objs.order()._prioritize)
        print('Action: move "Техника" and "Юридический термин" to the left, add "Военно-политический термин" to the end')
        lg.objs._order.prioritize_mult(search='Техника, юр., воен.-полит.')
        print('Priorities (2):',lg.objs.order()._prioritize)
        print('Action: ignore "Звезда", delete "Военно-политический термин", move "Общая лексика" to the right')
        lg.objs._order.unprioritize_mult(search='Звезда, Военно-политический термин, Общая лексика')
        print('Priorities (3):',lg.objs.order()._prioritize)
        print('Blacklist (1):',lg.objs._order._blacklist)
        print('Action: add "Общая лексика" and "Мода"')
        lg.objs.order().block_mult(search='общ., Мода')
        print('Blacklist (2):',lg.objs._order._blacklist)
        print('Action: delete "Общая лексика" and "Мода"')
        lg.objs.order().unblock_mult(search='общ., Мода')
        print('Blacklist (3):',lg.objs._order._blacklist)


if __name__ == '__main__':
    sg.objs.start()
    com = Commands()
    #com.search_local('snitch')
    com.order()
    sg.objs.end()
