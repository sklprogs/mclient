#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.message.controller import rep
from skl_shared_qt.paths import PDIR, Path, File
from skl_shared_qt.config import Schema, Json
from skl_shared_qt.logic import com

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

class ByLangs:
    
    def __init__(self):
        self.Success = True
        self.psubjects = PDIR.add('..', 'resources', 'plugins', 'multitrancom'
                                 ,'subjects', 'subjects.json')
        self.pschema = PDIR.add('..', 'resources', 'plugins', 'multitrancom'
                               ,'subjects', 'schema.json')
    
    def set_files(self):
        f = '[MClient] plugins.multitrancom.subjects.ByLangs.set_files'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.psubjects or not self.pschema:
            self.Success = False
            rep.empty(f)
            return
        self.psubjects = Path(self.psubjects).get_absolute()
        self.pschema = Path(self.pschema).get_absolute()
        self.Success = File(self.psubjects).Success and File(self.pschema).Success
    
    def load(self):
        f = '[MClient] plugins.multitrancom.subjects.ByLangs.load'
        if not self.Success:
            rep.cancel(f)
            return
        self.ischema = Schema(self.pschema)
        self.ischema.run()
        self.iconfig = Json(self.psubjects)
        self.iconfig.load()
        self.Success = self.ischema.Success and self.iconfig.validate(self.ischema.get())
    
    def get(self):
        f = '[MClient] plugins.multitrancom.subjects.ByLangs.get'
        if not self.Success:
            rep.cancel(f)
            return {}
        try:
            return self.iconfig.json[com.lang]
        except KeyError:
            rep.input(f)
        return {}
    
    def dump(self):
        f = '[MClient] plugins.multitrancom.subjects.ByLangs.dump'
        if not self.Success:
            rep.cancel(f)
            return ''
        code = self.iconfig.dump()
        if not code:
            rep.empty(f)
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
            self.subjects = ByLangs()
            self.subjects.run()
        return self.subjects


objs = Objects()
