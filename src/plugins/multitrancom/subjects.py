#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared_qt.shared as sh
import skl_shared_qt.config as qc

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
        self.Success = True
        self.psubjects = sh.objs.get_pdir().add ('..', 'resources', 'plugins'
                                                ,'multitrancom', 'subjects'
                                                ,'subjects.json'
                                                )
        self.pschema = sh.objs.pdir.add ('..', 'resources', 'plugins'
                                        ,'multitrancom', 'subjects'
                                        ,'schema.json'
                                        )
    
    def set_files(self):
        f = '[MClient] plugins.multitrancom.subjects.Subjects.set_files'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.psubjects or not self.pschema:
            self.Success = False
            sh.com.rep_empty(f)
            return
        self.psubjects = sh.Path(self.psubjects).get_absolute()
        self.pschema = sh.Path(self.pschema).get_absolute()
        self.Success = sh.File(self.psubjects).Success and sh.File(self.pschema).Success
    
    def load(self):
        f = '[MClient] plugins.multitrancom.subjects.Subjects.load'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.ischema = qc.Schema(self.pschema)
        self.ischema.run()
        self.iconfig = qc.Json(self.psubjects)
        self.iconfig.load()
        self.Success = self.ischema.Success and self.iconfig.validate(self.ischema.get())
    
    def get(self):
        f = '[MClient] plugins.multitrancom.subjects.Subjects.get'
        if not self.Success:
            sh.com.cancel(f)
            return {}
        try:
            return self.iconfig.json[sh.com.lang]
        except KeyError:
            sh.com.rep_input(f)
        return {}
    
    def dump(self):
        f = '[MClient] plugins.multitrancom.subjects.Subjects.dump'
        if not self.Success:
            sh.com.cancel(f)
            return ''
        code = self.iconfig.dump()
        if not code:
            sh.com.rep_empty(f)
            return ''
        return code
    
    def run(self):
        self.set_files()
        self.load()



class Objects:
    
    def __init__(self):
        self.subjects = None
    
    def get_subjects(self):
        if self.subjects is None:
            self.subjects = Subjects()
            self.subjects.run()
        return self.subjects


objs = Objects()
