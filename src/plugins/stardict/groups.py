#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.shared as sh


SUBJECTS = []


class Groups:
    
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
        self.groups = None
    
    def get_groups(self):
        if self.groups is None:
            self.groups = Groups()
        return self.groups


objs = Objects()


if __name__ == '__main__':
    f = '[MClient] plugins.stardict.__main__'
    sh.com.start()
    timer = sh.Timer(f)
    timer.start()
    mes = Groups().get_group('Wood processing')
    sh.objs.get_mes(f,mes,True).show_debug()
    timer.end()
    sh.com.end()
