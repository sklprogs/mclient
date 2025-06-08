#!/usr/bin/python3

import json

from skl_shared.message.controller import rep
from skl_shared.paths import PDIR
from skl_shared.logic import com
from skl_shared.paths import Path
from skl_shared.text_file import Read


class Speech:
    
    def __init__(self):
        self.set_values()
    
    def set_values(self):
        self.Success = True
        self.code = ''
        self.dic = {}
        self.file_ptrn = PDIR.add('..', 'resources', 'plugins', 'multitrancom'
                                 ,'speech', '{}.json')
    
    def set_dic(self):
        f = '[MClient] plugins.multitrancom.speech.Speech.set_dic'
        if not self.Success:
            rep.cancel(f)
            return
        try:
            self.dic = json.loads(self.code)
        except Exception as e:
            self.Success = False
            rep.third_party(f, e)
    
    def get_dic(self):
        return self.dic
    
    def load(self):
        f = '[MClient] plugins.multitrancom.speech.Speech.load'
        if not self.Success:
            rep.cancel(f)
            return
        file = self.file_ptrn.format(com.lang)
        ''' Show the full path in case of not finding the file to make
            debugging easier.
        '''
        file = Path(file).get_absolute()
        self.code = Read(file).get()
        if not self.code:
            self.Success = False
            rep.empty_output(f)
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
