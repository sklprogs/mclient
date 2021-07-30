#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.shared as sh


class ArticleSubjects:
    ''' Set a dictionary to call DIC/DICF fast without the need
        to directly utilize plugins.multitrancom.subjects.SUBJECTS
        which is slow and should be abstracted.
    '''
    def __init__(self):
        self.set_values()
    
    def check(self):
        f = '[MClient] subjects.subjects.ArticleSubjects.check'
        if self.pairs:
            for pair in self.pairs:
                if len(pair) != 2:
                    self.Success = False
                    mes = _('Wrong input data!')
                    sh.objs.get_mes(f,mes,True).show_warning()
        else:
            self.Success = False
            sh.com.rep_empty(f)
    
    def get_priority(self,item):
        f = '[MClient] subjects.subjects.ArticleSubjects.get_priority'
        if self.Success:
            try:
                return self.subjects[item]['priority']
            except KeyError:
                mes = _('Wrong input data: "{}"!').format(item)
                sh.objs.get_mes(f,mes,True).show_warning()
        else:
            sh.com.cancel(f)
        return 0
    
    def is_blocked(self,item):
        f = '[MClient] subjects.subjects.ArticleSubjects.is_blocked'
        if self.Success:
            try:
                return self.subjects[item]['block']
            except KeyError:
                mes = _('Wrong input data: "{}"!').format(item)
                sh.objs.get_mes(f,mes,True).show_warning()
        else:
            sh.com.cancel(f)
    
    def set_values(self):
        self.Success = True
        self.Debug = False
        self.subjects = {}
        self.blocks = []
    
    def reset(self,pairs,Debug=False):
        self.set_values()
        self.pairs = pairs
        self.Debug = Debug
    
    def _debug_subjects(self):
        f = '[MClient] subjects.subjects.ArticleSubjects._debug_subjects'
        nos = [i + 1 for i in range(len(self.subjects.keys()))]
        keys = []
        shorts = []
        titles = []
        blocked = []
        priorities = []
        for key in self.subjects.keys():
            keys.append(key)
            shorts.append(self.subjects[key]['short'])
            titles.append(self.subjects[key]['title'])
            blocked.append(self.subjects[key]['block'])
            priorities.append(self.subjects[key]['priority'])
        headers = (_('#'),_('KEY'),_('SHORT'),_('TITLE'),_('BLOCKED')
                  ,_('PRIORITY')
                  )
        iterable = [nos,keys,shorts,titles,blocked,priorities]
        # 10'' monitor: 30 symbols per column
        mes = sh.FastTable (iterable = iterable
                           ,headers = headers
                           ,maxrow = 30
                           ).run()
        return f + ':\n' + mes
    
    def debug(self):
        f = '[MClient] subjects.subjects.ArticleSubjects.debug'
        if self.Success:
            if self.Debug:
                mes = [self._debug_subjects()]
                mes = '\n\n'.join(mes)
                sh.com.run_fast_debug(f,mes)
            else:
                sh.com.rep_lazy(f)
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.check()
        self.fill()
        self.debug()
    
    def fill(self):
        # Takes ~0.007s for 'set' on Intel Atom
        f = '[MClient] subjects.subjects.ArticleSubjects.fill'
        if self.Success:
            for pair in self.pairs:
                if pair[0] and not pair[0] in self.subjects:
                    if objs.get_order().is_blocked(pair[1]):
                        Blocked = True
                        priority = objs.order.get_priority(pair[1])
                    elif objs.order.is_prioritized(pair[1]):
                        Blocked = objs.order.is_blocked(pair[1])
                        priority = objs.order.get_priority(pair[1])
                    else:
                        count1 = pair[0].count(', ')
                        count2 = pair[1].count(', ')
                        if count1 and count1 == count2:
                            short_lst = pair[0].split(', ')
                            title_lst = pair[1].split(', ')
                            Blocked = self._is_list_blocked(title_lst)
                            priority = self._get_list_priority(title_lst)
                        else:
                            Blocked = False
                            priority = 0
                    self.subjects[pair[0]] = {}
                    self.subjects[pair[1]] = {}
                    self.subjects[pair[0]]['short'] = pair[0]
                    self.subjects[pair[1]]['short'] = pair[0]
                    self.subjects[pair[0]]['title'] = pair[1]
                    self.subjects[pair[1]]['title'] = pair[1]
                    self.subjects[pair[0]]['block'] = Blocked
                    self.subjects[pair[1]]['block'] = Blocked
                    self.subjects[pair[0]]['priority'] = priority
                    self.subjects[pair[1]]['priority'] = priority
        else:
            sh.com.cancel(f)
    
    def _is_list_blocked(self,lst):
        for item in lst:
            if objs.get_order().is_blocked(item):
                return True
    
    def _get_list_priority(self,lst):
        priorities = []
        for item in lst:
            priorities.append(objs.get_order().get_priority(item))
        # An error will be thrown on an empty list
        try:
            return max(priorities)
        except ValueError:
            return 0



class Order:
    # Create block and priority lists and manage them
    def __init__(self):
        self.set_values()
            
    def get_priority(self,title):
        try:
            index_ = self.priorlst.index(title)
            return len(self.priorlst) - index_
        except ValueError:
            pass
        return 0
    
    def is_prioritized(self,title):
        return title in self.priorlst
    
    def is_blocked(self,title):
        return title in self.blacklst
    
    def set_values(self):
        self.blacklst = []
        self.priorlst = []
    
    def block(self,title):
        if not title in self.blacklst:
            self.blacklst.append(title)
                          
    def unblock(self,title):
        try:
            self.blacklst.remove(title)
        except ValueError:
            pass
                          
    def prioritize(self,title):
        if not title in self.priorlst:
            self.priorlst.append(title)
    
    def unprioritize(self,title):
        try:
            self.priorlst.remove(title)
        except ValueError:
            pass



class Objects:
    
    def __init__(self):
        self.order = self.article = None
    
    def get_article(self):
        if self.article is None:
            self.article = ArticleSubjects()
        return self.article
    
    def get_order(self):
        if self.order is None:
            self.order = Order()
        return self.order


objs = Objects()
