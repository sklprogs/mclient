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
        try:
            index_ = self.priorlst.index(item)
            return len(self.priorlst) - index_
        except ValueError:
            pass
        return 0
    
    def is_prioritized(self,item):
        return item in self.priorlst
    
    def is_blocked(self,item):
        return item in self.blacklst
    
    def conform(self):
        f = '[MClient] subjects.order.Order.conform'
        ''' - Create new block and priority lists based on those that
              were read from user files. Lists from user files may
              comprise either full or short dictionary titles.
              New lists will be lowercased and stripped and will
              comprise both full and short titles.
            - We recreate lists in order to preserve the short + full
              title order.
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
    
    def set_values(self):
        self.blacklst = []
        self.priorlst = []
    
    def get_pair(self,item):
        # A dummy class, reassign this in a parent class
        pass
    
    def block(self,item):
        if not item in self.blacklst:
            self.blacklst.append(item)
                          
    def unblock(self,item):
        try:
            self.blacklst.remove(item)
        except ValueError:
            pass
                          
    def prioritize(self,item):
        self.priorlst.append(item)
    
    def unprioritize(self,item):
        try:
            self.priorlst.remove(item)
        except ValueError:
            pass
