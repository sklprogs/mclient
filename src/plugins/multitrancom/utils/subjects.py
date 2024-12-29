#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message, rep
from skl_shared_qt.text_file import Write
from skl_shared_qt.paths import PDIR
from skl_shared_qt.graphics.clipboard.controller import CLIPBOARD
from skl_shared_qt.text_file import Write


class Dic:
    
    def __init__(self, majors, pairs):
        self.Success = True
        self.subjects = {}
        self.majors = majors
        self.pairs = pairs
    
    def check(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.Dic.check'
        if not self.majors or not self.pairs:
            self.Success = False
            rep.empty(f)
            return
        if len(self.pairs) % 2 != 0:
            self.Success = False
            mes = f'{len(self.pairs)} % 2 != 0'
            rep.condition(f, mes)
    
    def set_subjects(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.Dic.set_subjects'
        if not self.Success:
            rep.cancel(f)
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
        f = '[MClient] plugins.multitrancom.utils.subjects.Dic.add'
        if not self.Success:
            rep.cancel(f)
            return
        for major in self.majors:
            if not self._search(major):
                self.subjects[major] = {}
    
    def sort(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.Dic.sort'
        if not self.Success:
            rep.cancel(f)
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
        self.langs = ('en', 'ru', 'de', 'es', 'uk', 'pl', 'zh')
        self.majors = []
        self.pairs = []
        self.subjects = {}
        ''' Copy "var subjects" and "var MajorToMinor" sections from
            view-source:https://www.multitran.com/m.exe?a=104&l1=1&l2=2&s=hello&SHL=%d,
            where %d is
            en: 1
            ru: 2
            de: 3
            es: 5
            uk: 33
            pl: 14
            zh: 17.
        '''
        self.filew = PDIR.add('..', '..', '..', '..', 'resources', 'plugins'
                             ,'multitrancom', 'subjects','subjects.json')
    
    def input(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.Loop.input'
        if not self.Success:
            rep.cancel(f)
            return
        mes = _('Copy "var subjects" section to clipboard for language "{}"')
        mes = mes.format(self.lang)
        Message(f, mes, True).show_info()
#        ques = Message(f, mes, True).show_question()
#        if not ques:
#            self.Success = False
#            mes = _('Operation has been canceled by the user.')
#            Message(f, mes).show_info()
#            return
        self.majors = CLIPBOARD.paste()
        if not self.majors:
            self.Success = False
            rep.empty(f)
            return
        mes = _('Copy "var MajorToMinor" section to clipboard for language "{}"')
        mes = mes.format(self.lang)
        Message(f, mes, True).show_info()
        self.pairs = CLIPBOARD.paste()
        if not self.pairs:
            self.Success = False
            rep.empty(f)
            return
    
    def _convert(self, string):
        f = '[MClient] plugins.multitrancom.utils.subjects.Loop._convert'
        try:
            return json.loads(string)
        except Exception as e:
            rep.third_party(f, e)
    
    def set_lists(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.Loop.set_lists'
        if not self.Success:
            rep.cancel(f)
            return
        self.majors = self._convert(self.majors)
        if not self.majors:
            self.Success = False
            rep.empty_output(f)
            return
        self.pairs = self._convert(self.pairs)
        if not self.pairs:
            self.Success = False
            rep.empty_output(f)
            return
    
    def add(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.Loop.add'
        if not self.Success:
            rep.cancel(f)
            return
        idic = Dic(self.majors, self.pairs)
        self.subjects[self.lang] = idic.run()
        self.Success = idic.Success
    
    def save(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.Loop.save'
        if not self.Success:
            rep.cancel(f)
            return
        self.Success = Write(self.filew, True).write(com.get_string(self.subjects))
    
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
        f = '[MClient] plugins.multitrancom.utils.subjects.Commands.get_string'
        try:
            return json.dumps(dic, ensure_ascii=False, indent=4)
        except Exception as e:
            rep.third_party(f, e)

com = Commands()
