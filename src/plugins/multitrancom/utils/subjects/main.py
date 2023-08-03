#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json

#from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

''' Process 'var subjects' and 'var MajorToMinor' sections from multitran.com
    and create a JSON file from these sequences.
'''
majors = ["Аварийное восстановление", "Авиационная медицина", "Авиация", "Австралийское выражение", "Австралия", "Австрийское выражение", "Австрия", "Автоматика"]
pairs = ["Компьютеры", "Информационные технологии", "Компьютеры", "SAP", "Компьютеры", "Компьютерные сети", "Компьютеры", "Программирование", "Компьютеры", "Операционные системы", "Компьютеры", "Обработка данных", "Компьютеры", "Нейронные сети", "Компьютеры", "Интернет", "Компьютеры", "Расширение файла", "Компьютеры", "SAP технические термины", "Компьютеры", "SAP финансы"]



class Dic:
    
    def __init__(self, pairs):
        self.Success = True
        self.subjects = {}
        self.pairs = pairs
    
    def check(self):
        f = '[MClientQt] plugins.multitrancom.utils.subjects.main.Dic.check'
        if not self.pairs:
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
    
    def run(self):
        self.check()
        self.set_subjects()
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
    mes = com.get_string(Dic(pairs).run())
    idebug = sh.Debug(f, mes)
    idebug.show()
    sh.com.end()
