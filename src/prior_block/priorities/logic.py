#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class Subject:
    
    def __init__(self):
        self.text = ''
        self.Major = False
        self.cur_major = 0
        self.prev_major = 0



class Priorities:
    
    def __init__(self):
        self.dic1 = {}
        self.dic2 = {}
        self.subjects = []
    
    def debug(self):
        major = []
        cur_major = []
        prev_major = []
        text = []
        for subject in self.subjects:
            text.append(subject.text)
            major.append(subject.Major)
            cur_major.append(subject.cur_major)
            prev_major.append(subject.prev_major)
        headers = ('text', 'Major', 'cur_major', 'prev_major')
        iterable = (text,major,cur_major,prev_major)
        mes = sh.FastTable (iterable = iterable
                           ,headers = headers
                           ,maxrow = 50
                           ).run()
        #sh.com.run_fast_debug('debug', mes)
        print(mes)
    
    def set_subjects(self):
        count = 0
        cur_major = 0
        prev_major = 0
        for key in self.dic1.keys():
            subject = Subject()
            subject.Major = True
            cur_major = count
            subject.text = key
            subject.cur_major = cur_major
            subject.prev_major = prev_major
            self.subjects.append(subject)
            count += 1
            for key in self.dic1[key]:
                subject = Subject()
                subject.text = key
                subject.cur_major = cur_major
                subject.prev_major = prev_major
                self.subjects.append(subject)
                count += 1
            prev_major = cur_major
                
    def move_group_up(self, pos):
        f = '[MClientQt] prior_block.priorities.logic.Priorities.move_group_up'
        print(f)
        print(self.subjects[pos].text)
    
    def move_minor_up(self, pos):
        f = '[MClientQt] prior_block.priorities.logic.Priorities.move_minor_up'
        print(f)
        print(self.subjects[pos].text)
        if pos - 1 == self.subjects[pos].cur_major:
            print('Need to create new group')
            self.subjects.insert(pos - 1, self.subjects[pos])
            self.subjects.insert(pos - 1, self.subjects[self.subjects[pos].cur_major+1])
            # 21 since we have inserted 2 new items
            del self.subjects[pos + 2]
        elif pos == 0:
            # Subject #0 should be major
            mes = _('Wrong input data!')
            sh.objs.get_mes(f, mes, True).show_debug()
        elif pos == 1:
            sh.com.rep_lazy(f)
        else:
            self.subjects.insert(pos - 1, self.subjects[pos])
            # +1 since we have inserted a new item
            del self.subjects[pos + 1]
        
    def move_up(self,pos):
        if self.subjects[pos].Major:
            self.move_group_up(pos)
        else:
            self.move_minor_up(pos)
    
    def reset(self, dic1, dic2):
        self.dic1 = dic1
        self.dic2 = dic2
        self.set_subjects()


if __name__ == '__main__':
    dic1 = {'Компьютеры':
               ['Компьютеры', 'Майкрософт', 'Программирование', 'Оракл']
           ,'Разговорная лексика':
               ['Разговорная лексика', 'Арго', 'Грубо', 'Мат', 'Возвышенно'
               ,'Поэтически'
               ]
           ,'Языки':
               ['Языки', 'Английский', 'Французский', 'Немецкий', 'Русский'
               ,'Датский', 'Японский', 'Китайский'
               ]
           }
    iprior = Priorities()
    iprior.reset(dic1, {})
    print(iprior.dic1)
    iprior.move_up(6)
    iprior.debug()
