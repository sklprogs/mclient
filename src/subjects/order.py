#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.shared as sh


class Order:
    # Create block and priority lists and supplement them
    def __init__(self):
        self.set_values()
        self.conform()
        
    def fill_dic(self,lst,ind):
        lst = lst[1:]
        lst = lst[::-1]
        for item in lst:
            self.priorlst.insert(ind,item)
            
    def get_priority(self,search):
        f = '[MClient] subjects.order.Order.get_priority'
        if self.Success:
            lst = self.get_list(search)
            if lst:
                prior = []
                for item in lst:
                    try:
                        ind = self.priorlst.index(item)
                        prior.append(len(self.priorlst)-ind)
                    except ValueError:
                        pass
                if prior:
                    return max(prior)
                else:
                    return 0
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def is_prioritized(self,lst):
        f = '[MClient] subjects.order.Order.is_prioritized'
        if self.Success:
            if lst:
                for item in lst:
                    if item in self.priorlst:
                        return True
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def is_blocked(self,lst):
        f = '[MClient] subjects.order.Order.is_blocked'
        if self.Success:
            if lst:
                for item in lst:
                    if item in self.blacklst:
                        return True
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def conform(self):
        f = '[MClient] subjects.order.Order.conform'
        ''' Create new block and priority lists based on those that were
            read from user files. Lists from user files may comprise
            either full or short dictionary titles. New lists will be
            lowercased and stripped and will comprise both full and
            short titles.
        '''
        if self.Success:
            ''' We recreate lists in order to preserve 
                the short + full title order.
            '''
            if self.blacklst:
                blacklst = list(self.blacklst)
                self.blacklst = []
                for item in blacklst:
                    pair = self.get_pair(item)
                    if pair:
                        self.block(pair[0])
                        self.block(pair[1])
                    else:
                        sh.com.rep_empty(f)
            else:
                sh.com.rep_lazy(f)
            if self.priorlst:
                priorlst = list(self.priorlst)
                self.priorlst = []
                for item in priorlst:
                    pair = self.get_pair(item)
                    if pair:
                        self.prioritize(pair[0])
                        self.prioritize(pair[1])
                    else:
                        sh.com.rep_empty(f)
            else:
                sh.com.rep_lazy(f)
        else:
            sh.com.cancel(f)
    
    def set_values(self):
        self.Success = True
        self.blacklst = []
        self.priorlst = []
        self.dic1 = ''
        self.dic2 = ''
            
    def sort_dic(self,lst):
        f = '[MClient] subjects.order.Order.sort_dic'
        if self.Success:
            if lst:
                indexes = []
                for item in lst:
                    try:
                        ind = self.priorlst.index(item)
                    except ValueError:
                        # Place an unpriotitized dictionary at the end
                        ind = 1000
                    indexes.append(ind)
                lst = sorted(zip(indexes,lst))
                lst = [item[1] for item in lst]
                return lst
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def set(self,dic1,dic2=''):
        f = '[MClient] subjects.order.Order.set'
        if self.Success:
            ''' This allows to return an empty value instead of the last
                memory in case there is no previous/next dictionary.
            '''
            self.dic1 = self.dic2 = ''
            if dic1:
                dic1 = self.get_list(dic1)
                dic1 = self.sort_dic(dic1)
                self.dic1 = list(dic1)
            else:
                sh.com.rep_empty(f)
            if dic2:
                dic2 = self.get_list(dic2)
                dic2 = self.sort_dic(dic2)
                self.dic2 = list(dic2)
        else:
            sh.com.cancel(f)
    
    def get_pair(self,item):
        # A dummy class, reassign this in a parent class
        pass
    
    def get_list(self,search):
        f = '[MClient] subjects.order.Order.get_list'
        if self.Success:
            if search:
                search = search.split(', ')
                search = [item.strip() for item in search]
                search = [item for item in search if item]
                lst = []
                for item in search:
                    pair = self.get_pair(item)
                    if pair:
                        lst += pair
                return lst
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
        mes = '"{}"'.format(search)
        sh.objs.get_mes(f,mes,True).show_warning()
        return []
    
    def block(self,item):
        if self.Success:
            if not item in self.blacklst:
                self.blacklst.append(item)
                          
    def unblock(self,item):
        f = '[MClient] subjects.order.Order.unblock'
        if self.Success:
            try:
                self.blacklst.remove(item)
            except ValueError:
                pass
        else:
            sh.com.cancel(f)
                          
    def prioritize(self,item):
        f = '[MClient] subjects.order.Order.prioritize'
        if self.Success:
            self.priorlst.append(item)
        else:
            sh.com.cancel(f)
    
    def unprioritize(self,item):
        f = '[MClient] subjects.order.Order.unprioritize'
        if self.Success:
            try:
                self.priorlst.remove(item)
            except ValueError:
                pass
        else:
            sh.com.cancel(f)
