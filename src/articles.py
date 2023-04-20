#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class Articles:
    
    def __init__(self):
        self.reset()
    
    def set_values(self):
        self.cur_id = 0
        self.articles = {'ids':{}}
    
    def reset(self):
        self.set_values()
    
    def get_max_id(self):
        f = '[MClientQt] articles.Articles.get_max_id'
        try:
            # Do not use 'max' on an empty sequence
            return len(self.articles['ids']) - 1
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f,mes).show_warning()
        return -1
    
    def add(self,request='',url='',cells=[]):
        id_ = self.get_max_id() + 1
        self.articles['ids'][id_] = {'request' : request
                                    ,'url' : url
                                    ,'cells' : cells
                                    }
        self.set_cur_id(id_)
    
    def set_cur_id(self,id_):
        f = '[MClientQt] articles.Articles.set_cur_id'
        try:
            self.articles['ids'][id_]
        except KeyError:
            mes = _('Wrong input data: "{}"!').format(id_)
            sh.objs.get_mes(f,mes).show_warning()
            return
        self.cur_id = id_
    
    def get_cur_request(self):
        f = '[MClientQt] articles.Articles.get_cur_request'
        try:
            return self.articles['ids'][self.cur_id]['request']
        except KeyError:
            mes = _('Wrong input data: "{}"!').format(self.cur_id)
            sh.objs.get_mes(f,mes).show_warning()
        return ''



class Objects:
    
    def __init__(self):
        self.articles = None
    
    def get_articles(self):
        if self.articles is None:
            self.articles = Articles()
        return self.articles


objs = Objects()


if __name__ == '__main__':
    sh.com.start()
    request = 'back'
    url = 'https://www.multitran.com/m.exe?s=back&l1=1&l2=2'
    cells = []
    objs.get_articles().add(request,url,cells)
    print(objs.articles.get_cur_request())
    sh.com.end()
