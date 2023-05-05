#!/usr/bin/python3

import json

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
    
    def get_dic(self):
        return self.dic
    
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
