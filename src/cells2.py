#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import operator

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import subjects.subjects as sj


class Omit:
    
    def __init__(self,cells):
        self.cells = cells



class Commands:
    
    def set_view(self,cells):
        f = '[MClientQt] cells.Commands.set_view'
        if not cells:
            sh.com.rep_empty(f)
            return
        view = []
        for cell in cells:
            row = [cell.no,cell.text,cell.code,cell.url,cell.subj,cell.wform
                  ,cell.transc,cell.speech,cell.priority
                  ]
            view.append(row)
        return view



class Sort:
    
    def __init__(self,view):
        ''' 0: no, 1: text, 2: code, 3: url, 4: subj, 5: wform, 6: transc,
            7: speech, 8: priority.
        '''
        self.Success = True
        self.view = view

    def check(self):
        f = '[MClientQt] cells.Sort.check'
        if not self.view:
            self.Success = False
            sh.com.rep_empty(f)
            return
        if len(self.view[0]) != 9:
            self.Success = False
            mes = f'{len(self.view[0])} = 9'
            sh.com.rep_condition(f,mes)
    
    def sort(self):
        f = '[MClientQt] cells.Sort.sort'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.view.sort(key=operator.itemgetter(8,4,5,6,7,1,0))
    
    def debug(self):
        f = '[MClientQt] cells.Sort.debug'
        if not self.Success:
            sh.com.cancel(f)
            return
        headers = (_('CELL #'),_('TEXT'),_('CODE'),_('URL'),'SUBJ','WFORM'
                  ,'TRANSC','SPEECH','PRIORITY'
                  )
        return sh.FastTable (headers = headers
                            ,iterable = self.view
                            ,Transpose = True
                            ,maxrow = 50
                            ).run()
    
    def run(self):
        self.check()
        self.sort()


com = Commands()


if __name__ == '__main__':
    Sort().run()