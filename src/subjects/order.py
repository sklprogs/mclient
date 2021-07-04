#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.shared as sh


class Order:
    # Create block and priority lists and supplement them
    def __init__(self):
        self.set_values()
        self.conform()
            
    def get_priority(self,item):
        f = '[MClient] subjects.order.Order.get_priority'
        if self.Success:
            try:
                index_ = self.priorlst.index(item)
                return len(self.priorlst) - index_
            except ValueError:
                pass
        else:
            sh.com.cancel(f)
        return 0
    
    def is_prioritized(self,item):
        f = '[MClient] subjects.order.Order.is_prioritized'
        if self.Success:
            return item in self.priorlst
        else:
            sh.com.cancel(f)
    
    def is_blocked(self,item):
        f = '[MClient] subjects.order.Order.is_blocked'
        if self.Success:
            return item in self.blacklst
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
    
    def get_pair(self,item):
        # A dummy class, reassign this in a parent class
        pass
    
    def block(self,item):
        f = '[MClient] subjects.order.Order.block'
        if self.Success:
            if not item in self.blacklst:
                self.blacklst.append(item)
        else:
            sh.com.cancel(f)
                          
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
