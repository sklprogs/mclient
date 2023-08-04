#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class Dic:
    
    def __init__(self, majors, pairs):
        self.Success = True
        self.subjects = {}
        self.majors = majors
        self.pairs = pairs
    
    def check(self):
        f = '[MClientQt] plugins.multitrancom.utils.subjects.main.Dic.check'
        if not self.majors or not self.pairs:
            self.Success = False
            sh.com.rep_empty(f)
            return
        if len(self.pairs) % 2 != 0:
            self.Success = False
            mes = f'{len(self.pairs)} % 2 != 0'
            sh.com.rep_condition(f, mes)
    
    def set_subjects(self):
        f = '[MClientQt] plugins.multitrancom.utils.subjects.main.Dic.set_subjects'
        if not self.Success:
            sh.com.cancel(f)
            return
        i = 1
        while i < len(self.pairs):
            major = self.pairs[i-1]
            minor = self.pairs[i]
            if not major in self.subjects:
                self.subjects[major] = {}
            self.subjects[major][minor] = {}
            i += 2
    
    def _search(self, subject):
        for key, value in self.subjects.items():
            if key == subject:
                return True
            if subject in value:
                return True
    
    def add(self):
        f = '[MClientQt] plugins.multitrancom.utils.subjects.main.Dic.add'
        if not self.Success:
            sh.com.cancel(f)
            return
        for major in self.majors:
            if not self._search(major):
                self.subjects[major] = {}
    
    def sort(self):
        f = '[MClientQt] plugins.multitrancom.utils.subjects.main.Dic.sort'
        if not self.Success:
            sh.com.cancel(f)
            return
        subjects = {}
        keys = sorted(self.subjects.keys())
        for key in keys:
            values = sorted(self.subjects[key].keys())
            subjects[key] = {}
            for value in values:
                subjects[key][value] = {}
        self.subjects = subjects
    
    def run(self):
        self.check()
        self.set_subjects()
        self.add()
        self.sort()
        return self.subjects



class Loop:
    
    def __init__(self):
        self.Success = True
        self.langs = ['ru']
        self.majors = []
        self.pairs = []
        self.subjects = {}
        self.filew = sh.objs.get_pdir().add ('..', '..', '..', '..', '..'
                                            ,'resources', 'plugins'
                                            ,'multitrancom', 'subjects'
                                            ,'subjects.json'
                                            )
    
    def input(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.main.Loop.input'
        if not self.Success:
            sh.com.cancel(f)
            return
        mes = _('Copy "var subjects" section to clipboard for language "{}"')
        mes = mes.format(self.lang)
        sh.objs.get_mes(f, mes).show_info()
#        ques = sh.objs.get_mes(f, mes).show_question()
#        if not ques:
#            self.Success = False
#            mes = _('Operation has been canceled by the user.')
#            sh.objs.get_mes(f, mes, True).show_info()
#            return
        self.majors = sh.Clipboard().paste()
        if not self.majors:
            self.Success = False
            sh.com.rep_empty(f)
            return
        mes = _('Copy "var MajorToMinor" section to clipboard for language "{}"')
        mes = mes.format(self.lang)
        sh.objs.get_mes(f, mes).show_info()
        self.pairs = sh.Clipboard().paste()
        if not self.pairs:
            self.Success = False
            sh.com.rep_empty(f)
            return
    
    def _convert(self, string):
        f = '[MClient] plugins.multitrancom.utils.subjects.main.Loop._convert'
        try:
            return json.loads(string)
        except Exception as e:
            sh.com.rep_third_party(f, e)
    
    def set_lists(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.main.Loop.set_lists'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.majors = self._convert(self.majors)
        if not self.majors:
            self.Success = False
            sh.com.rep_out(f)
            return
        self.pairs = self._convert(self.pairs)
        if not self.pairs:
            self.Success = False
            sh.com.rep_out(f)
            return
    
    def add(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.main.Loop.add'
        if not self.Success:
            sh.com.cancel(f)
            return
        idic = Dic(self.majors, self.pairs)
        self.subjects[self.lang] = idic.run()
        self.Success = idic.Success
    
    def save(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.main.Loop.save'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.Success = sh.WriteTextFile(self.filew, True).write(com.get_string(self.subjects))
    
    def _run_lang(self):
        self.input()
        self.set_lists()
        self.add()
        return self.Success
    
    def run(self):
        for self.lang in self.langs:
            if not self._run_lang():
                return
        self.save()
        return self.subjects



class Commands:
    
    def get_string(self, dic):
        f = '[MClient] plugins.multitrancom.utils.subjects.main.Commands.get_string'
        try:
            return json.dumps(dic, ensure_ascii=False, indent=4)
        except Exception as e:
            sh.com.rep_third_party(f, e)

com = Commands()


if __name__ == '__main__':
    f = '[MClientQt] plugins.multitrancom.utils.subjects.main.__main__'
    sh.com.start()
    mes = com.get_string(Loop().run())
    idebug = sh.Debug(f, mes)
    idebug.show()
    sh.com.end()
