#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import logic as lg


class Subjects:
    
    def __init__(self):
        self.prior = []
    
    def set_prior(self):
        f = '[MClientQt] subjects.Subjects.set_prior'
        if not lg.objs.get_default().prior or not lg.objs.get_articles().get_subjects():
            sh.com.rep_lazy(f)
            return
        for subject in lg.objs.get_articles().get_subjects():
            if subject in lg.objs.get_default().prior:
                self.prior.append(subject)
            elif ', ' in subject:
                parts = subject.split(', ')
                for part in parts:
                    if part in lg.objs.get_default().prior:
                        self.prior.append(subject)
                        break
        mes = '; '.join(self.prior)
        sh.objs.get_mes(f,mes,True).show_debug()
    
    def expand(self, subject):
        dic = lg.objs.get_articles().get_subjects()
        if not subject or not dic:
            return subject
        if subject in dic:
            return dic[subject]
        if not ', ' in subject:
            return subject
        new_parts = []
        parts = subject.split(', ')
        for part in parts:
            if part in dic:
                new_parts.append(dic[part])
            else:
                new_parts.append(part)
        return ', '.join(new_parts)
    
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
                if part in lg.objs.default.prior:
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
                if part in lg.objs.default.block:
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
