#!/usr/bin/python3

import json

from skl_shared.localize import _
from skl_shared.message.controller import rep
from skl_shared.paths import PDIR
from skl_shared.paths import Path
from skl_shared.text_file import Read

from config import CONFIG


class Speech:
    
    def __init__(self):
        self.Success = True
        self.code = ''
        self.dic = {}
        self.dicrw = {}
        self.file = PDIR.add('..', 'resources', 'speech.json')
        self.load()
        self.set_dic()
        self.restructure()
    
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
    
    def _add_item(self, section, lang, item):
        f = '[MClient] speech.Speech._add_item'
        item = item.lower()
        if item in self.dicrw:
            return
        self.dicrw[item] = {}
        # 'lang' key is just for information
        #self.dicrw[item]['lang'] = lang
        # Presence of keys should be checked at the scheme level
        if not self.dic[section]['full']['en']:
            self.Success = False
            rep.empty(f)
            return
        if not self.dic[section]['short']['en']:
            self.Success = False
            rep.empty(f)
            return
        if isinstance(self.dic[section]['full']['en'], str):
            full = self.dic[section]['full']['en']
        else:
            full = self.dic[section]['full']['en'][0]
        if isinstance(self.dic[section]['short']['en'], str):
            short = self.dic[section]['short']['en']
        else:
            short = self.dic[section]['short']['en'][0]
        self.dicrw[item]['full'] = full
        self.dicrw[item]['short'] = short
    
    def restructure(self):
        ''' Create a search-friendly dictionary. Unlike the dictionary read from
            resources, this is less user-friendly, much larger when dumped to
            JSON (~12 times), does not store languages and has each search key
            lowercased.
        '''
        f = '[MClient] speech.Speech.restructure'
        if not self.Success:
            rep.cancel(f)
            return
        # This loop is very fast (<0.002s)
        for section in self.dic:
            for type_ in self.dic[section]:
                for lang in self.dic[section][type_]:
                    items = self.dic[section][type_][lang]
                    if isinstance(items, str):
                        self._add_item(section, lang, items)
                    else:
                        for item in items:
                            self._add_item(section, lang, item)
    
    def expand(self, short):
        f = '[MClient] speech.Speech.expand'
        if not self.Success:
            rep.cancel(f)
            return short
        lower = short.lower().strip()
        try:
            return _(self.dicrw[lower]['full'])
        except KeyError:
            return short
    
    def shorten(self, full):
        f = '[MClient] speech.Speech.shorten'
        if not self.Success:
            rep.cancel(f)
            return full
        lower = full.lower().strip()
        try:
            return _(self.dicrw[lower]['short'])
        except KeyError:
            return full
    
    def get_settings(self):
        f = '[MClient] speech.Speech.get_settings'
        speeches = [CONFIG.new['speech1'], CONFIG.new['speech2']
                   ,CONFIG.new['speech3'], CONFIG.new['speech4']
                   ,CONFIG.new['speech5'], CONFIG.new['speech6']
                   ,CONFIG.new['speech7']]
        if not self.Success:
            rep.cancel(f)
            return speeches
        if not self.dicrw:
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
        return pattern.lower() in self.dicrw


SPEECH = Speech()