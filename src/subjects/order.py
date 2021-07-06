#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.shared as sh


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
    
    def get_pair(self,item):
        # A dummy class, reassign this in a parent class
        pass
    
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
