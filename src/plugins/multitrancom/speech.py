#!/usr/bin/python3

import json

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class Speech:
    
    def __init__(self):
        self.set_values()
    
    def set_values(self):
        self.Success = True
        self.code = ''
        self.dic = {}
        self.file_ptrn = sh.objs.get_pdir().add ('..', 'resources', 'plugins'
                                                ,'multitrancom', 'speech'
                                                ,'{}.json'
                                                )
    
    def set_dic(self):
        f = '[MClientQt] plugins.multitrancom.speech.Speech.set_dic'
        if not self.Success:
            sh.com.cancel(f)
            return
        try:
            self.dic = json.loads(self.code)
        except Exception as e:
            self.Success = False
            sh.com.rep_third_party(f,e)
    
    def load(self):
        f = '[MClientQt] plugins.multitrancom.speech.Speech.load'
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
    
    def find(self, short):
        ''' This takes ~0.007s on AMD E-300 for 'set' (processing 'speech'
            attribute for each block) without debug output, running in terminal
            (not in IDE). Since the function is used very frequently, debugging
            can slow it down to ~1s!
        '''
        f = '[MClientQt] plugins.multitrancom.speech.Speech.find'
        if not self.Success:
            sh.com.cancel(f)
            return short
        try:
            return self.dic[short]
        except KeyError:
            mes = _('Wrong input data: "{}"!').format(short)
            sh.objs.get_mes(f,mes,True).show_warning()
        return short
    
    def run(self):
        self.load()
        self.set_dic()



class Objects:
    
    def __init__(self):
        self.speech = None
    
    def get_speech(self):
        if self.speech is None:
            self.speech = Speech()
            self.speech.run()
        return self.speech


objs = Objects()
