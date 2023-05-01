#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

''' About this module:
    - This structure describes subjects at multitran.com.
    - Use plugins.multitrancom.utils.subjects to extract and process these
      subjects.
    - multitran.com separates subjects into major and normal ones. A group of
      minors should also comprise its major since the entire group will be
      blocked/prioritized otherwise.
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
    - multitran.com has a bug causing that such entries as 'Gruzovik, inform.'
      will be expanded as 'Informal'.
'''



class Subjects:
    
    def __init__(self):
        self.set_values()
    
    def set_values(self):
        self.Success = True
        self.dic = {}
        self.code = ''
        self.file_ptrn = sh.objs.get_pdir().add ('..', '..', '..'
                                                ,'resources', 'plugins'
                                                ,'multitrancom', 'subjects'
                                                ,'{}.json'
                                                )
    
    def get_lists(self):
        f = '[MClientQt] plugins.multitrancom.subjects.Subjects.get_lists'
        if not self.Success:
            sh.com.cancel(f)
            return
        majors = []
        minors = []
        for major in self.dic:
            majors.append(major)
            minors.append(self.dic[major])
        return(majors, minors)
    
    def set_dic(self):
        f = '[MClientQt] plugins.multitrancom.subjects.Subjects.set_dic'
        try:
            self.dic = json.loads(self.code)
        except Exception as e:
            self.Success = False
            sh.com.rep_third_party(f,e)
    
    def load(self):
        f = '[MClientQt] plugins.multitrancom.subjects.Subjects.load'
        if not self.Success:
            sh.com.cancel(f)
            return
        file = self.file_ptrn.format(sh.com.lang)
        ''' Show the full path in case of not finding the file to make
            debugging easier.
        '''
        file = sh.Path(file).get_absolute()
        self.code = sh.ReadTextFile(file).get()
        if not self.code:
            self.Success = False
            sh.com.rep_out(f)
            return
    
    def run(self):
        self.load()
        self.set_dic()



class Objects:
    
    def __init__(self):
        self.subjects = None
    
    def get_subjects(self):
        if self.subjects is None:
            self.subjects = Subjects()
            self.subjects.run()
        return self.subjects


objs = Objects()


if __name__ == '__main__':
    f = '[MClient] plugins.multitrancom.subjects.__main__'
    sh.com.start()
    lists = objs.get_subjects().get_lists()
    mes = []
    if lists:
        mes.append(_('Majors:'))
        mes.append('; '.join(lists[0]))
        mes.append('')
        mes.append(_('Grouped minors:'))
        mes.append(str(lists[1]))
    mes = '\n'.join(mes)
    idebug = sh.Debug(f,mes)
    idebug.show()
#    mes = _('Ready!')
#    sh.objs.get_mes(f,mes).show_debug()
    sh.com.end()
