#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.logic import com as shcom

from config import CONFIG
from speech import SPEECH


class Speech:
    
    def __init__(self):
        self.mes = []
        self.Success = CONFIG.Success
    
    def get_settings(self):
        f = '[MClient] tests.Speech.get_settings'
        self.mes.append(f + ':')
        if not self.Success:
            rep.cancel(f)
            return
        self.mes.append(str(SPEECH.get_settings()))
        self.mes.append('')
    
    def _expand(self, short):
        full = SPEECH.expand(short)
        self.mes.append(f'"{short}" -> "{full}"')
    
    def _shorten(self, full):
        short = SPEECH.shorten(full)
        self.mes.append(f'"{full}" -> "{short}"')
    
    def _is_speech(self, pattern):
        result = SPEECH.is_speech(pattern)
        self.mes.append(f'"{pattern}": "{result}"')
    
    def is_speech(self):
        f = '[MClient] tests.Speech.is_speech'
        self.mes.append(f + ':')
        if not self.Success:
            rep.cancel(f)
            return
        self._is_speech('сущ.')
        self._is_speech('Verbo')
        self._is_speech('VV')
        self.mes.append('')
    
    def expand(self):
        f = '[MClient] tests.Speech.expand'
        self.mes.append(f + ':')
        if not self.Success:
            rep.cancel(f)
            return
        self.mes.append(_('Expand mismatch'))
        self._expand('mism')
        self._expand('сущ.')
        self._expand('n')
        self._expand('v')
        old = shcom.lang
        shcom.lang = 'es'
        self.mes.append(_('Set language to "{}"').format(shcom.lang))
        self._expand('v')
        shcom.lang = old
        self.mes.append(_('Set language to "{}"').format(shcom.lang))
        self.mes.append('')
    
    def shorten(self):
        f = '[MClient] tests.Speech.shorten'
        self.mes.append(f + ':')
        if not self.Success:
            rep.cancel(f)
            return
        self.mes.append(_('Shorten mismatch'))
        self._shorten('mism')
        self._shorten('Существительное')
        self._shorten('Noun')
        self._shorten('Verb')
        old = shcom.lang
        shcom.lang = 'es'
        self.mes.append(_('Set language to "{}"').format(shcom.lang))
        self._shorten('Verbo')
        shcom.lang = old
        self.mes.append(_('Set language to "{}"').format(shcom.lang))
        self.mes.append('')
    
    def run_all(self):
        self.get_settings()
        self.expand()
        self.shorten()
        self.is_speech()
        return '\n'.join(self.mes)