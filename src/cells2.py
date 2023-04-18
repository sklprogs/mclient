#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import operator

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import subjects.subjects as sj


class Omit:
    
    def __init__(self,cells):
        self.cells = cells
    
    def run(self):
        return self.cells



class Prioritize:
    
    def __init__(self,cells):
        self.cells = cells
    
    def set_phrases(self):
        for cell in self.cells:
            if cell.fixed_block and cell.fixed_block.type_ == 'phsubj':
                cell.priority = 1000
    
    def run(self):
        self.set_phrases()
        return self.cells



class Commands:
    
    def set_view(self,cells):
        f = '[MClientQt] cells.Commands.set_view'
        if not cells:
            sh.com.rep_empty(f)
            return
        view = []
        for cell in cells:
            row = [cell.no,cell.text,cell.code,cell.url,cell.subj,cell.wform
                  ,cell.transc,cell.speech,cell.priority,cell.rowno
                  ]
            view.append(row)
        return view
    
    def order(self,cells):
        cells = Omit(cells).run()
        cells = Prioritize(cells).run()
        cells = View(self.set_view(cells)).run()
        return cells



class View:
    # Create user-specific data set
    def __init__(self,view,fixed_types=('subj','wform','transc','speech')):
        ''' 0: no, 1: text, 2: code, 3: url, 4: subj, 5: wform, 6: transc,
            7: speech, 8: priority, 9: rowno.
        '''
        self.Success = True
        self.view = view
        self.fixed_types = fixed_types

    def check(self):
        f = '[MClientQt] cells.View.check'
        if not self.view:
            self.Success = False
            sh.com.rep_empty(f)
            return
        if len(self.view[0]) != 10:
            self.Success = False
            mes = f'{len(self.view[0])} = 10'
            sh.com.rep_condition(f,mes)
    
    def sort(self):
        f = '[MClientQt] cells.View.sort'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.view.sort(key=operator.itemgetter(8,4,5,6,7,1,0))
    
    def _get_fixed_type_no(self,type_):
        f = '[MClientQt] cells.View._get_fixed_type_no'
        if type_ in ('subj','phsubj'):
            return 4
        elif type_ == 'wform':
            return 5
        elif type_ == 'transc':
            return 6
        elif type_ == 'speech':
            return 7
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format (type_,'; '.join (['subj','phsubj','wform'
                                               ,'speech','transc'
                                               ]
                                              )
                             )
            sh.objs.get_mes(f,mes,True).show_warning()
    
    def _create_fixed(self,i,no):
        new_row = list(self.view[i])
        # HTML code must be generated at the formatting step coming the last
        new_row[2] = ''
        if self.view[i-1][no] == self.view[i][no]:
            new_row[1] = ''
        else:
            new_row[1] = self.view[i][no]
        return new_row
    
    def _is_new_row(self,i):
        # 'i > 0' condition is observed in 'restore_fixed'
        return self.view[i-1][9] != self.view[i][9]
    
    def restore_fixed(self):
        f = '[MClientQt] cells.View.restore_fixed'
        if not self.Success:
            sh.com.cancel(f)
            return
        count = 0
        i = 1
        while i < len(self.view):
            if self._is_new_row(i):
                add = []
                for type_ in self.fixed_types:
                    no = self._get_fixed_type_no(type_)
                    if no is None:
                        sh.com.rep_empty(f)
                        return
                    add.append(self._create_fixed(i,no))
                    count += 1
                for row in add:
                    self.view.insert(i,row)
                    i += 1
            i += 1
        sh.com.rep_matches(f,count)
    
    def debug(self):
        f = '[MClientQt] cells.View.debug'
        if not self.Success:
            sh.com.cancel(f)
            return
        headers = (_('CELL #'),_('TEXT'),_('CODE'),_('URL'),'SUBJ','WFORM'
                  ,'TRANSC','SPEECH','PRIORITY',_('ROW #')
                  )
        return sh.FastTable (headers = headers
                            ,iterable = self.view
                            ,Transpose = True
                            ,maxrow = 50
                            ).run()
    
    def run(self):
        self.check()
        self.sort()
        self.restore_fixed()
        return self.view


com = Commands()


if __name__ == '__main__':
    sh.com.start()
    com.order(cells)
    sh.com.end()