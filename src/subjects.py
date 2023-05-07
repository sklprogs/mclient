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
            return
        subject = self.expand(subject)
        if subject in lg.objs.get_default().prior:
            return True
        elif ', ' in subject:
            parts = subject.split(', ')
            for part in parts:
                if self.expand(part) in lg.objs.default.prior:
                    return True
    
    def is_blocked(self, subject):
        if not subject:
            return
        subject = self.expand(subject)
        if subject in lg.objs.get_default().block:
            return True
        elif ', ' in subject:
            parts = subject.split(', ')
            for part in parts:
                if self.expand(part) in lg.objs.default.block:
                    return True
    
    def _get_priority(self, subject):
        try:
            return lg.objs.get_default().prior.index(subject)
        except ValueError:
            return
    
    def get_priority(self, subject):
        if not subject:
            return
        subject = self.expand(subject)
        priority = self._get_priority(subject)
        if priority is not None:
            return priority
        if ', ' in subject:
            priorities = []
            parts = subject.split(', ')
            for part in parts:
                part = self.expand(part)
                priority = self._get_priority(part)
                if priority is not None:
                    priorities.append(priority)
            if priorities:
                return min(priorities)



class Objects:
    
    def __init__(self):
        self.subjects = None
    
    def get_subjects(self):
        if self.subjects is None:
            self.subjects = Subjects()
        return self.subjects


objs = Objects()
