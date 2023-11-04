#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import instance as ic
import config as cf


class Split:

    def __init__(self, subjf):
        self.subjf = subjf
        self.parts = []
        self.indexes = []

    def debug(self):
        f = '[MClient] subjects.Split.debug'
        mes = _('Indexes: {}').format(self.indexes)
        sh.objs.get_mes(f, mes, True).show_debug()
        mes = _('Parts: {}').format(sorted(self.parts))
        sh.objs.get_mes(f, mes, True).show_debug()
    
    def run(self):
        self.set_indexes()
        self.set_parts()
        return self.parts
    
    def set_parts(self):
        start = 0
        for index_ in self.indexes:
            self.parts.append(self.subjf[start:index_])
            start = index_ + 2
        last = self.subjf[start:]
        if last:
            self.parts.append(last)
    
    def set_indexes(self):
        items = re.finditer(r', [А-Я,A-Z]', self.subjf)
        if not items:
            return
        for item in items:
            self.indexes.append(item.span()[0])



class PriorIndex:
    
    def __init__(self, prior_all, parts):
        self.indexes = []
        self.min = -1
        self.prior_all = prior_all
        self.parts = parts
    
    def debug(self):
        f = '[MClient] subjects.PriorIndex.debug'
        mes = _('Indexes: {}').format(self.indexes)
        sh.objs.get_mes(f, mes, True).show_debug()
        mes = _('Minimal index: {}').format(self.min)
        sh.objs.get_mes(f, mes, True).show_debug()
    
    def _get(self, subjf):
        try:
            return self.prior_all.index(subjf)
        except ValueError:
            return -1
    
    def set_indexes(self):
        self.indexes = [self._get(part) for part in self.parts]
    
    def set_min(self):
        # Cannot use 'min' on an empty list
        indexes = [index_ for index_ in self.indexes if index_ > -1]
        if not indexes:
            return
        self.min = min(indexes)
    
    def run(self):
        self.set_indexes()
        self.set_min()
        return self.min



class Create:
    
    def __init__(self):
        self.set_values()
    
    def set_values(self):
        self.prior_all = []
        self.block_all = []
        self.subjects = []
        self.article = []
        self.prior = []
        self.block = []
        self.pairs = {}
    
    def set_article(self):
        self.article = sorted(set(self.pairs.values()), key=lambda s: s.casefold())
    
    def _set_prior_section(self, section):
        for key, value in section.items():
            self.prior_all.append(key)
            self._set_prior_section(value)
    
    def _set_block_section(self, section):
        for key, value in section.items():
            self.block_all.append(key)
            self._set_block_section(value)
    
    def set_prior_all(self):
        f = '[MClient] subjects.Create.set_prior_all'
        self._set_prior_section(cf.objs.get_config().new['subjects']['prioritized'])
        mes = '; '.join(self.prior_all)
        sh.objs.get_mes(f, mes, True).show_debug()
    
    def set_blocked_all(self):
        f = '[MClient] subjects.Create.set_blocked_all'
        self._set_block_section(cf.objs.get_config().new['subjects']['blocked'])
        mes = '; '.join(self.block_all)
        sh.objs.get_mes(f, mes, True).show_debug()
    
    def reset(self, pairs):
        self.set_values()
        self.pairs = pairs
        self.run()
    
    def debug(self):
        report = [self._debug_lists(), self._debug_subjects()]
        report = [item for item in report if item]
        return '\n\n'.join(report)
    
    def _debug_lists(self):
        f = '[MClient] subjects.Create._debug_lists'
        mes = []
        sub = _('Pairs:')
        mes.append(sub)
        mes.append(str(self.pairs))
        sub = _('Loaded prioritized subjects:')
        mes.append(sub)
        sub = '; '.join(self.prior_all)
        mes.append(sub)
        sub = _('Loaded blocked subjects:')
        mes.append(sub)
        sub = '; '.join(self.block_all)
        mes.append(sub)
        sub = _('Sort by short subjects:')
        mes.append(sub)
        mes.append(str(cf.objs.get_config().new['ShortSubjects']))
        return '\n'.join(mes)
    
    def _debug_subjects(self):
        f = '[MClient] subjects.Create._debug_subjects'
        subj = []
        subjf = []
        blocked = []
        indexes = []
        subjpr = []
        for isubj in self.subjects:
            subj.append(isubj.subj)
            subjf.append(isubj.subjf)
            blocked.append(isubj.Block)
            indexes.append(isubj.prior_index)
            subjpr.append(isubj.subjpr)
        headers = ('SUBJ', 'SUBJF', _('BLOCKED'), 'PRIOR_INDEX', 'SUBJPR')
        iterable = [subj, subjf, blocked, indexes, subjpr]
        mes = sh.FastTable (iterable = iterable
                           ,headers = headers
                           ,maxrow = 70
                           ).run()
        return f'{f}:\n{mes}'
    
    def set_subjects(self):
        for subj, subjf in self.pairs.items():
            isubj = ic.Subject()
            isubj.subj = subj
            isubj.subjf = subjf
            self.subjects.append(isubj)
            parts = Split(subjf).run()
            for part in parts:
                if part in self.block_all:
                    self.block.append(part)
                    isubj.Block = True
                if part in self.prior_all:
                    self.prior.append(part)
            isubj.prior_index = PriorIndex(self.prior_all, parts).run()
    
    def alphabetize(self):
        if cf.objs.get_config().new['ShortSubjects']:
            self.subjects.sort(key=lambda x: x.subj.casefold())
        else:
            self.subjects.sort(key=lambda x: x.subjf.casefold())
    
    def set_subjpr(self):
        prior_indexes = [isubj.prior_index for isubj in self.subjects]
        max_ = max(prior_indexes)
        for isubj in self.subjects:
            if isubj.prior_index > -1:
                isubj.subjpr = isubj.prior_index
            else:
                max_ += 1
                isubj.subjpr = max_
    
    def prioritize(self):
        self.subjects.sort(key=lambda x: x.subjpr)
    
    def run(self):
        self.set_article()
        self.set_blocked_all()
        self.set_prior_all()
        self.set_subjects()
        self.alphabetize()
        self.set_subjpr()
        self.prioritize()



class Subjects(Create):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def add_fixed_urls(self):
        #TODO: Rework
        pass
    
    def expand(self, subj):
        # Works only for subjects within the current article
        for isubj in self.subjects:
            if subj == isubj.subj:
                return isubj.subjf
        return subj
    
    def get_max_subjpr(self):
        subjpr = [isubj.subjpr for isubj in self.subjects]
        # Cannot use 'max' on empty lists
        if not subjpr:
            return -1
        return max(subjpr)
    
    def is_phrase_blocked(self, phrase):
        ''' This can find out if a subject is blocked globally, not just in the
            current article, but the subject must be in a full form. Works best
            for items of the 'phrase' type.
        '''
        return phrase in self.block_all
    
    def is_phrase_prior(self, phrase):
        ''' This can find out if a subject is prioritized globally, not just in
            the current article, but the subject must be in a full form. Works
            best for items of the 'phrase' type.
        '''
        return phrase in self.prior_all
    
    def is_blocked(self, subject):
        ''' For a subject (either simple or compound) to be found, all article
            subjects must be collected beforehand. 'vulg.' will be shown as not
            blocked if the article has only 'inf., vulg.'.
        '''
        for isubj in self.subjects:
            if subject in (isubj.subj, isubj.subjf):
                return isubj.Block
    
    def is_prioritized(self, subject):
        ''' For a subject (either simple or compound) to be found, all article
            subjects must be collected beforehand. 'IT' will be shown as not
            prioritized if the article has only 'IT, tech.'.
        '''
        for isubj in self.subjects:
            if subject in (isubj.subj, isubj.subjf):
                return isubj.prior_index > -1


class Objects:
    
    def __init__(self):
        self.subjects = None
    
    def get_subjects(self):
        if self.subjects is None:
            self.subjects = Subjects()
        return self.subjects


objs = Objects()
