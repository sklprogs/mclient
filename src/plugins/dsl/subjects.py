#!/usr/bin/python3
# -*- coding: UTF-8 -*-

SUBJECTS = []


class Subjects:
    
    def __init__(self):
        self.lst = []
        self.majors = []
    
    def get_majors(self):
        return self.majors
    
    def get_list(self):
        return self.lst
    
    def get_group(self, subject):
        return []
    
    def get_group_with_header(self, subject):
        return [subject]



class Objects:
    
    def __init__(self):
        self.subjects = None
    
    def get_subjects(self):
        if self.subjects is None:
            self.subjects = Subjects()
        return self.subjects


objs = Objects()
