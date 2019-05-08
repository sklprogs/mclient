#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import shared    as sh
import sharedGUI as sg

import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')


class Elems:
    
    def __init__ (self,blocks1,blocks2
                 ,Debug=False,Shorten=True
                 ,MaxRow=20,MaxRows=200
                 ):
        self.values()
        if blocks1:
            self._blocks1 = blocks1
        if blocks2:
            self._blocks2 = blocks2
        self.Debug   = Debug
        self.Shorten = Shorten
        self.MaxRow  = MaxRow
        self.MaxRows = MaxRows
    
    def join_blocks(self):
        if self._blocks1 and self._blocks2:
            #todo: elaborate
            self._blocks = self._blocks1 + self._blocks2
        elif self._blocks1:
            self._blocks = list(self._blocks1)
        elif self._blocks2:
            self._blocks = list(self._blocks2)
    
    def phrase_block(self):
        f = '[MClient] plugins.multitran.elems.Elems.phrase_block'
        if self._phblock is None:
            if self._phdic:
                for block in self._blocks2:
                    if self._phdic == block._text:
                        self._phblock = block
                        break
            else:
                sh.com.empty(f)
        return self._phblock
    
    def phrase_prop(self):
        ''' In order to be in the same section, phrases must have
            the same DICA, WFORMA and (probably) SPEECHA, TRANSCA.
        '''
        f = '[MClient] plugins.multitran.elems.Elems.phrase_prop'
        if self.phrase_block():
            for block in self._blocks:
                if block._type == 'phrase':
                    block._dica = self._phblock._dica
                    block._wforma  = self._phblock._wforma
                    block._speecha = self._phblock._speecha
        else:
            sh.log.append (f,_('INFO')
                          ,_('Nothing to do!')
                          )
    
    def delete_empty(self):
        self._blocks1 = [block for block in self._blocks1 if block._text]
        self._blocks2 = [block for block in self._blocks2 if block._text]
    
    def delete_transc(self):
        ''' Since 'multitran.com' is a development branch of
            'multitran.ru', we assume that if an article at
            'multitran.ru' has transcriptions, so does an article at
            'multitran.com'.
        '''
        self._blocks1 = [block for block in self._blocks1
                         if block._type != 'transc'
                        ]
    
    def join_phrases(self):
        ''' In order to join phrase sections of different plugins, we
            need to find phrase dic titles and replace corresponding
            DICAs with the same DICA.
        '''
        f = '[MClient] plugins.multitran.elems.Elems.join_phrases'
        if self._blocks1 and self._blocks2:
            phrase1 = self._blocks1[-1]._dica
            phrase2 = self._blocks2[-1]._dica
            pattern = '(\d+)\s(phrases|фраза|фраз)'
            match1  = re.match(pattern,phrase1)
            match2  = re.match(pattern,phrase2)
            if match1 and match2:
                sh.log.append (f,_('DEBUG')
                              ,_('Phrase dic 1: "%s"') % match1.group(0)
                              )
                sh.log.append (f,_('DEBUG')
                              ,_('Phrase dic 2: "%s"') % match2.group(0)
                              )
                val1 = int(match1.group(1))
                val2 = int(match2.group(1))
                val  = max(val1,val2)
                self._phdic = _('%d phrases') % val
                sh.log.append (f,_('DEBUG')
                              ,_('Common phrase dic: "%s"') % self._phdic
                              )
                for block in self._blocks1:
                    if block._dica == phrase1:
                        block._dica = self._phdic
                    if block._dicaf == phrase1:
                        block._dicaf = self._phdic
                    if block._text == phrase1:
                        block._text = self._phdic
                for block in self._blocks2:
                    if block._dica == phrase2:
                        block._dica = self._phdic
                    if block._dicaf == phrase2:
                        block._dicaf = self._phdic
                    if block._text == phrase2:
                        block._text = self._phdic
        else:
            sh.log.append (f,_('INFO')
                          ,_('Nothing to do!')
                          )
    
    def values(self):
        self._blocks  = []
        self._blocks1 = []
        self._blocks2 = []
        self._phdic   = ''
        self._phblock = None
    
    def debug(self):
        f = '[MClient] plugins.multitran.elems.Elems.debug'
        if self.Debug:
            if self._blocks:
                sh.log.append (f,_('DEBUG')
                              ,_('Debug table:')
                              )
                headers = ('DICA','DICAF','TYPE','TEXT')
                rows    = []
                for row in self._blocks:
                    rows.append ([block._dica,block._dicaf
                                 ,block._type,block._text
                                 ]
                                )
                sh.Table (headers = headers
                         ,rows    = rows
                         ,Shorten = self.Shorten
                         ,MaxRow  = self.MaxRow
                         ,MaxRows = self.MaxRows
                         ).print()
            else:
                sh.com.empty(f)
    
    def run(self):
        f = '[MClient] plugins.multitran.elems.Elems.run'
        self.delete_transc()
        self.delete_empty()
        self.join_phrases()
        self.join_blocks()
        self.phrase_prop()
        self.debug()
        return self._blocks
