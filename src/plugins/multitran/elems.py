#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import shared    as sh
import sharedGUI as sg

import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')


class Elems:
    
    def __init__ (self,data1,data2,Debug=False
                 ,Shorten=True,MaxRow=20
                 ,MaxRows=200
                 ):
        f = '[MClient] plugins.multitran.elems.Elems.__init__'
        self.values()
        self._data1  = data1
        self._data2  = data2
        self.Debug   = Debug
        self.Shorten = Shorten
        self.MaxRow  = MaxRow
        self.MaxRows = MaxRows
        if not self._data1 or not self._data2:
            self.Success = False
            sh.com.empty(f)
    
    def subjects(self):
        f = '[MClient] plugins.multitran.elems.Elems.subjects'
        if self.Success:
            pattern = '[\s]{0,1}(в|in) \d+ (тематиках|тематике|subjects)'
            count = 0
            i = 0
            while i < len(self._data):
                if re.match(pattern,self._data[i][8]):
                    del self._data[i]
                    count += 1
                    i -= 1
                i += 1
            sh.log.append (f,_('INFO')
                          ,_('Blocks removed: %d') % count
                          )
        else:
            sh.com.cancel(f)
    
    def purge(self):
        ''' Delete blocks that are empty, likely duplicates or have
            no value.
        '''
        f = '[MClient] plugins.multitran.elems.Elems.purge'
        if self.Success:
            count = 0
            i = 0
            while i < len(self._data1):
                btype = self._data1[i][7]
                text  = self._data1[i][8]
                ''' It is not easy to distinguish comments and
                    transcriptions at 'multitran.com'. Since
                    'multitran.com' is a development branch of
                    'multitran.ru', we assume that if an article at
                    'multitran.ru' have transcriptions, so does
                    an article at 'multitran.com'.
                '''
                if not text or btype == 'transc':
                    del self._data1[i]
                    count += 1
                    i -= 1
                i += 1
            sh.log.append (f,_('INFO')
                          ,_('Blocks removed: %d') % count
                          )
        else:
            sh.com.cancel(f)
    
    def tolist(self):
        f = '[MClient] plugins.multitran.elems.Elems.tolist'
        if self.Success:
            self._data1 = [list(item) for item in self._data1]
            self._data2 = [list(item) for item in self._data2]
        else:
            sh.com.cancel(f)
    
    def join_phrases(self):
        ''' In order to join phrase sections of different plugins, we
            need to find phrase dic titles and replace corresponding
            DICAs with the same DICA.
        '''
        f = '[MClient] plugins.multitran.elems.Elems.join_phrases'
        if self.Success:
            phrase1 = self._data1[-1][2]
            phrase2 = self._data2[-1][2]
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
                dica = _('%d phrases') % val
                sh.log.append (f,_('DEBUG')
                              ,_('Common phrase dic: "%s"') % dica
                              )
                for i in range(len(self._data1)):
                    # DICA
                    if self._data1[i][2] == phrase1:
                        self._data1[i][2] = dica
                    # DICAF
                    if self._data1[i][30] == phrase1:
                        self._data1[i][30] = dica
                    # TEXT
                    if self._data1[i][8] == phrase1:
                        self._data1[i][8] = dica
                for i in range(len(self._data2)):
                    # DICA
                    if self._data2[i][2] == phrase2:
                        self._data2[i][2] = dica
                    # DICAF
                    if self._data2[i][30] == phrase2:
                        self._data2[i][30] = dica
                    # TEXT
                    if self._data2[i][8] == phrase2:
                        self._data2[i][8] = dica
            else:
                sh.log.append (f,_('INFO')
                              ,_('Nothing to do!')
                              )
        else:
            sh.com.cancel(f)
    
    def values(self):
        self._data   = []
        self.Success = True
    
    def duplicates(self):
        ''' Remove duplicate blocks generated by both plugins.
            #note: the analysis is block-based, so, if one plugin has
            generated some block with an adjacent block having
            SameCell=1 (e.g., term + comment), and the other plugin has
            generated an identical block but without adjacent blocks
            having SameCell=1 (e.g., a term without a comment), then
            adjacent blocks having SameCell=1 may loose their implied
            order. If 'self._dica1' represents 'multitran.ru' and
            'self._dica2' - 'multitran.com', this should never happen,
            because 'multitran.com' should comprise all items of
            'multitran.ru' and also new ones.
        '''
        f = '[MClient] plugins.multitran.elems.Elems.duplicates'
        if self.Success:
            for block in self._data1:
                block[8] = block[8].strip()
            count = 0
            for block in self._data2:
                dica  = block[2]
                dicaf = block[30]
                btype = block[7]
                text  = block[8].strip()
                i = 0
                while i < len(self._data1):
                    dica1  = self._data1[i][2]
                    dicaf1 = self._data1[i][30]
                    btype1 = self._data1[i][7]
                    text1  = self._data1[i][8]
                    cond1  = text and (text == text1)
                    cond2  = dica == dica1 or dicaf == dicaf1
                    cond3  = btype and (btype == btype1)
                    if cond1 and cond2 and cond3:
                        del self._data1[i]
                        i -= 1
                        count += 1
                    i += 1
            sh.log.append (f,_('INFO')
                          ,_('Blocks removed: %d') % count
                          )
        else:
            sh.com.cancel(f)
    
    def debug_both(self):
        f = '[MClient] plugins.multitran.elems.Elems.debug_both'
        if self.Success:
            if self.Debug:
                sh.log.append (f,_('DEBUG')
                              ,_('Table %d:') % 1
                              )
                headers = ('DICA','DICAF','TYPE','TEXT')
                rows    = []
                for row in self._data1:
                    rows.append([row[2],row[30],row[7],row[8]])
                sh.Table (headers = headers
                         ,rows    = rows
                         ,Shorten = self.Shorten
                         ,MaxRow  = self.MaxRow
                         ,MaxRows = self.MaxRows
                         ).print()
                sh.log.append (f,_('DEBUG')
                              ,_('Table %d:') % 2
                              )
                headers = ('DICA','DICAF','TYPE','TEXT')
                rows    = []
                for row in self._data2:
                    rows.append([row[2],row[30],row[7],row[8]])
                sh.Table (headers = headers
                         ,rows    = rows
                         ,Shorten = self.Shorten
                         ,MaxRow  = self.MaxRow
                         ,MaxRows = self.MaxRows
                         ).print()
        else:
            sh.com.cancel(f)
    
    def debug(self):
        f = '[MClient] plugins.multitran.elems.Elems.debug'
        if self.Success:
            if self.Debug:
                sh.log.append (f,_('DEBUG')
                              ,_('The resulting table:')
                              )
                headers = ('DICA','DICAF','TYPE','TEXT')
                rows    = []
                for row in self._data:
                    rows.append([row[2],row[30],row[7],row[8]])
                sh.Table (headers = headers
                         ,rows    = rows
                         ,Shorten = self.Shorten
                         ,MaxRow  = self.MaxRow
                         ,MaxRows = self.MaxRows
                         ).print()
        else:
            sh.com.cancel(f)
    
    def sumup(self):
        f = '[MClient] plugins.multitran.elems.Elems.sumup'
        if self.Success:
            tmp = [self._data1,self._data2]
            tmp = [list(item) for item in tmp if item]
            self._data = []
            for item in tmp:
                self._data += item
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.tolist()
        self.join_phrases()
        self.duplicates()
        self.purge()
        self.debug_both()
        self.sumup()
        self.subjects()
        self.debug()
        return self._data
        
