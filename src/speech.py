#!/usr/bin/python3

import json

from skl_shared.message.controller import rep
from skl_shared.paths import PDIR
from skl_shared.logic import com as shcom
from skl_shared.paths import Path
from skl_shared.text_file import Read

from config import CONFIG


class Speech:
    
    def __init__(self):
        self.Success = True
        self.code = ''
        self.dic = {}
        self.file = PDIR.add('..', 'resources', 'speech.json')
        self.load()
        self.set_dic()
    
    def set_dic(self):
        f = '[MClient] speech.Speech.set_dic'
        if not self.Success:
            rep.cancel(f)
            return
        try:
            self.dic = json.loads(self.code)
        except Exception as e:
            self.Success = False
            rep.third_party(f, e)
    
    def load(self):
        f = '[MClient] speech.Speech.load'
        if not self.Success:
            rep.cancel(f)
            return
        ''' Show the full path in case of not finding the file to make
            debugging easier.
        '''
        self.file = Path(self.file).get_absolute()
        self.code = Read(self.file).get()
        if not self.code:
            self.Success = False
            rep.empty_output(f)
    
    def _get_short_by_lang(self, full):
        if not shcom.lang in self.dic:
            return full
        for short in self.dic[shcom.lang]:
            if self.dic[shcom.lang][short] == full:
                return short
        return full
    
    def _get_short(self, full):
        for lang in self.dic:
            for short in self.dic[lang]:
                if self.dic[lang][short] == full:
                    return short
        return full
    
    def _get_full_by_lang(self, short):
        try:
            return self.dic[shcom.lang][short]
        except KeyError:
            return short
    
    def _get_full(self, short):
        for lang in self.dic:
            if short in self.dic[lang]:
                return self.dic[lang][short]
        return short
    
    def expand(self, short):
        f = '[MClient] speech.Speech.expand'
        if not self.Success:
            rep.cancel(f)
            return short
        full = self._get_full_by_lang(short)
        if short != full:
            return full
        return self._get_full(short)
    
    def shorten(self, full):
        f = '[MClient] speech.Speech.shorten'
        if not self.Success:
            rep.cancel(f)
            return full
        short = self._get_short_by_lang(full)
        if short != full:
            return short
        return self._get_short(full)
    
    def get_settings(self):
        f = '[MClient] speech.Speech.get_settings'
        speeches = [CONFIG.new['speech1'], CONFIG.new['speech2']
                   ,CONFIG.new['speech3'], CONFIG.new['speech4']
                   ,CONFIG.new['speech5'], CONFIG.new['speech6']
                   ,CONFIG.new['speech7']]
        if not self.Success:
            rep.cancel(f)
            return speeches
        if not self.dic:
            return speeches
        if not CONFIG.new['ShortSpeech']:
            return speeches
        for i in range(len(speeches)):
            speeches[i] = self.shorten(speeches[i])
        return speeches
    
    def is_speech(self, pattern):
        f = '[MClient] speech.Speech.is_speech'
        if not self.Success:
            rep.cancel(f)
            return
        for lang in self.dic:
            for short in self.dic[lang]:
                if pattern == short:
                    return True
                if self.dic[lang][short] == pattern:
                    return True


SPEECH = Speech()