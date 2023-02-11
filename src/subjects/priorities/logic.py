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
        headers = ('text','Major','cur_major','prev_major')
        iterable = (text,major,cur_major,prev_major)
        mes = sh.FastTable (iterable = iterable
                           ,headers = headers
                           ,maxrow = 50
                           ).run()
        #sh.com.run_fast_debug('debug',mes)
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
                
    
    def reset(self,dic1,dic2):
        self.dic1 = dic1
        self.dic2 = dic2
        self.set_subjects()


if __name__ == '__main__':
    dic1 = {'Компьютеры':
               {'Компьютеры','Майкрософт','Программирование','Оракл'}
           ,'Разговорная лексика':
               {'Разговорная лексика','Арго','Грубо','Мат','Возвышенно'
               ,'Поэтически'
               }
           ,'Языки':
               {'Языки','Английский','Французский','Немецкий','Русский'
               ,'Датский','Японский','Китайский'
               }
           }
    iprior = Priorities()
    iprior.reset(dic1,{})
    iprior.debug()
