#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import logic as lg


class Subjects:
    
    def __init__(self):
        self.art_dic = {}
        self.article = []
        self.prior = []
    
    def set_article(self):
        f = '[MClientQt] subjects.Subjects.set_article'
        self.art_dic = lg.objs.get_articles().get_subjects()
        if not self.art_dic:
            sh.com.rep_lazy(f)
            return
        for short in self.art_dic:
            self.article.append(self.art_dic[short])
        mes = '; '.join(self.article)
        sh.objs.get_mes(f,mes,True).show_debug()
    
    def set_prior(self):
        f = '[MClientQt] subjects.Subjects.set_prior'
        all_prior = lg.objs.get_default().prior
        if not all_prior or not self.article:
            sh.com.rep_lazy(f)
            return
        for subject in self.article:
            if subject in all_prior:
                self.prior.append(subject)
            elif ', ' in subject:
                parts = subject.split(', ')
                for part in parts:
                    if part in all_prior:
                        self.prior.append(subject)
                        break
        mes = '; '.join(self.prior)
        sh.objs.get_mes(f,mes,True).show_debug()
    
    def expand(self, subject):
        try:
            return self.art_dic[subject]
        except KeyError:
            return subject
    
    def is_prioritized(self, subject):
        # Determine if we need to colorize 'subj' or 'phrase' types
        if not subject:
            return ''
        subject = self.expand(subject)
        if subject in lg.objs.get_default().prior:
            return True
        elif ', ' in subject:
            parts = subject.split(', ')
            for part in parts:
                if self.expand(part) in lg.objs.default.prior:
                    return True



class Objects:
    
    def __init__(self):
        self.subjects = None
    
    def get_subjects(self):
        if self.subjects is None:
            self.subjects = Subjects()
        return self.subjects


objs = Objects()


if __name__ == '__main__':
#    sh.com.start()
    url = 'https://www.multitran.com/m.exe?s=hello&l1=1&l2=2&SHL=2'
    search = 'hello'
    lg.com.start()
    cells = lg.objs.get_plugins().request (search = search
                                          ,url = url
                                          )
    lg.objs.get_articles().add (search = search
                               ,url = url
                               ,cells = cells
                               )
    subject = 'колос., общ.'
    #subject = 'Общая лексика'
    isubj = Subjects()
    isubj.set_article()
    print(isubj.is_prioritized(subject))
    #isubj.set_article()
    #isubj.set_prior()
#    sh.com.end()
