#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import config as cf
import logic as lg



class Subjects:
    
    def __init__(self):
        self.prior = []
        self.plain_prior = []
        self.plain_block = []
        self.ihistory = cf.HistorySubjects()
    
    def _set_prior_section(self, section):
        for key, value in section.items():
            self.plain_prior.append(key)
            self._set_prior_section(value)
    
    def _set_block_section(self, section):
        for key, value in section.items():
            self.plain_block.append(key)
            self._set_block_section(value)
    
    def set_plain(self):
        self._set_prior_section(cf.objs.get_config().new['subjects']['prioritized'])
        self._set_block_section(cf.objs.get_config().new['subjects']['blocked'])
    
    def add_fixed_urls(self):
        f = '[MClientQt] subjects.Subjects.add_fixed_urls'
        dic = lg.objs.get_plugins().get_fixed_urls()
        if not dic or not 'subj' in dic:
            sh.com.rep_lazy(f)
            return dic
        ''' We need to create a separate list of dictionary keys since we will
            get a "dictionary changed size during iteration" error otherwise.
        '''
        for subj in list(dic['subj'].keys()):
            subjf = self.expand(subj)
            dic['subj'][subjf] = dic['subj'][subj]
        return dic
    
    def expand(self, subject):
        if not subject:
            return ''
        full = self.ihistory.get_pair(subject)
        if full:
            return full
        if not ', ' in subject:
            return subject
        new_parts = []
        parts = subject.split(', ')
        for part in parts:
            full = self.ihistory.get_pair(part)
            if full:
                new_parts.append(full)
            else:
                new_parts.append(part)
        return ', '.join(new_parts)
    
    def is_prioritized(self, subject):
        # Determine if we need to colorize 'subj' or 'phrase' types
        if not subject:
            return
        expanded = self.expand(subject)
        if subject in self.plain_prior or expanded in self.plain_prior:
            return True
        if ', ' in subject:
            parts = subject.split(', ')
            for part in parts:
                if part in self.plain_prior:
                    return True
    
    def is_blocked(self, subject):
        if not subject:
            return
        subject = self.expand(subject)
        if subject in self.plain_block:
            return True
        if ', ' in subject:
            parts = subject.split(', ')
            for part in parts:
                if part in self.plain_block:
                    return True
    
    def _get_priority(self, subject):
        try:
            return self.plain_prior.index(subject)
        except ValueError:
            return
    
    def get_priority(self, subject):
        if not subject:
            return
        expanded = self.expand(subject)
        priority = self._get_priority(subject)
        priority_exp = self._get_priority(expanded)
        if priority is not None:
            return priority
        if priority_exp is not None:
            return priority_exp
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
            self.subjects.set_plain()
        return self.subjects


objs = Objects()
