#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.shared as sh


SUBJECTS = []


class Subjects:
    
    def __init__(self):
        self.lst = []
        self.majors = []
    
    def get_majors(self):
        return self.majors
    
    def get_list(self):
        return self.lst
    
    def get_group(self,subject):
        return ''



class Objects:
    
    def __init__(self):
        self.subjects = None
    
    def get_subjects(self):
        if self.subjects is None:
            self.subjects = Subjects()
        return self.subjects


objs = Objects()


if __name__ == '__main__':
    f = '[MClient] plugins.multitrandem.subjects.__main__'
    sh.com.start()
    timer = sh.Timer(f)
    timer.start()
    mes = Subjects().get_group('Wood processing')
    sh.objs.get_mes(f,mes,True).show_debug()
    timer.end()
    sh.com.end()
