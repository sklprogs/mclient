#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json

import skl_shared_qt.shared as sh

''' About this module:
    - This structure describes subjects at multitran.com.
    - Use plugins.multitrancom.utils.subjects to extract and process these
      subjects.
    - multitran.com separates subjects into majors and minors.
    - In order to get major subjects, log in to multitran.com, select any
      article, click "Add". View the source of the web-page and find
      "MajorToMinor" section. Change the interface language at multitran.com
      (you can add &SHL=<language_id> to the URL), do the same. Lists in the
      "MajorToMinor" section have items arranged in the same order for
      different languages, which allows to implement a language-agnostic
      blocking/prioritization algorithm. I decided not to support
      blocking/prioritization lists for different locales because methods for
      a single locale will be faster and easier to implement/maintain;
      moreover, frankly speaking, most people stay on the same locale, and
      blocking/prioritization lists are usually short and can be easily
      recreated.
    - multitran.com has a bug causing such entries as 'Gruzovik, inform.' to be
      expanded as 'Informal'.
'''



        


class Subjects:
    
    def __init__(self):
        self.set_values()
    
    def set_values(self):
        self.Success = True
        self.psubjects = sh.objs.get_pdir().add ('..', '..', '..', 'resources'
                                                ,'plugins', 'multitrancom'
                                                ,'subjects', 'subjects.json'
                                                )
        self.pschema = sh.objs.pdir().add ('..', '..', '..', 'resources'
                                          ,'plugins', 'multitrancom'
                                          ,'subjects', 'schema.json'
                                          )
        
        self.subjects = {}
        self.code = ''
    
    def set_subjects(self):
        f = '[MClient] plugins.multitrancom.subjects.Subjects.set_subjects'
        try:
            self.subjects = json.loads(self.csubjects)
        except Exception as e:
            self.Success = False
            sh.com.rep_third_party(f, e)
    
    def set_schema(self):
        f = '[MClient] plugins.multitrancom.subjects.Subjects.set_schema'
        try:
            self.schema = json.loads(self.cschema)
        except Exception as e:
            self.Success = False
            sh.com.rep_third_party(f, e)
    
    def load(self):
        f = '[MClient] plugins.multitrancom.subjects.Subjects.load'
        if not self.Success:
            sh.com.cancel(f)
            return
        ''' Show the full path in case of not finding the file to make
            debugging easier.
        '''
        self.subjects = sh.Path(self.psubjects).get_absolute()
        self.csubjects = sh.ReadTextFile(self.psubjects).get()
        if not self.csubjects:
            self.Success = False
            sh.com.rep_out(f)
            return
    
    def load_schema(self):
        f = '[MClient] plugins.multitrancom.subjects.Subjects.load_schema'
        if not self.Success:
            sh.com.cancel(f)
            return
        ''' Show the full path in case of not finding the file to make
            debugging easier.
        '''
        self.pschema = sh.Path(self.pschema).get_absolute()
        self.cschema = sh.ReadTextFile(self.pschema).get()
        if not self.cschema:
            self.Success = False
            sh.com.rep_out(f)
            return
    
    def run(self):
        self.load_subjects()
        self.load_schema()
        self.set()
        return self.subjects



class Objects:
    
    def __init__(self):
        self.subjects = None
    
    def get_subjects(self):
        if self.subjects is None:
            self.subjects = Subjects()
            self.subjects.run()
        return self.subjects


objs = Objects()
