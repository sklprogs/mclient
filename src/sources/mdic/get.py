#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import mmap
import zstd

from skl_shared.localize import _
from skl_shared.message.controller import rep, Message
from skl_shared.paths import Home, File
from skl_shared.time import Timer
from skl_shared.logic import Input


class Index:
    ''' This class is recreated each time upon search (should be cheap because
        of mmap), so self.pos and self.length are OK.
    '''
    def __init__(self, wform):
        self.Success = True
        self.wform = wform
        self.folder = Home('mclient').add_config('dics', 'MDIC', 'collection.indexes')
        self.file = ''
        self.pos = []
        self.length = []
    
    def _get_abbr(self):
        abbr = [char for char in self.wform.lower() if str(char).isalpha()]
        abbr = ''.join(abbr)
        abbr = abbr[0:2]
        ''' If abbr is empty and there is no extension, the app tries to save
            the file as a directory and fails. Either use an extension or
            do not allow an empty name.
        '''
        if not abbr:
            abbr = 'unknown'
        return abbr
    
    def set_file(self):
        f = '[MClient] sources.mdic.get.Index.set_file'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.wform:
            self.Success = False
            rep.empty(f)
            return
        self.file = os.path.join(self.folder, self._get_abbr())
        self.Success = File(self.file).Success
    
    def load(self):
        f = '[MClient] sources.mdic.get.Index.load'
        if not self.Success:
            rep.cancel(f)
            return
        self.bin = open(self.file, 'rb')
        # 'mmap' fails upon opening an empty file!
        try:
            self.imap = mmap.mmap(self.bin.fileno(), 0, prot=mmap.PROT_READ)
        except Exception as e:
            self.Success = False
            rep.third_part(f, e)
    
    def search(self, start=0):
        f = '[MClient] sources.mdic.get.Index.search'
        if not self.Success:
            rep.cancel(f)
            return
        bpattern = bytes('\n' + self.wform + '\t', 'utf-8')
        pos = self.imap.find(bpattern, start)
        if pos > -1:
            return pos + len(bpattern)
        bpattern = bytes(self.wform + '\t', 'utf-8')
        pos = self.imap.find(bpattern, start)
        if pos == 0:
            return len(bpattern)
    
    def suggest(self, pattern, limit=0):
        #TODO: Implement finding 1st entry
        f = '[MClient] sources.mdic.get.Index.suggest'
        if not self.Success:
            rep.cancel(f)
            return
        start = 0
        matches = []
        bpattern = bytes('\n' + pattern, 'utf-8')
        while True:
            pos = self.imap.find(bpattern, start)
            if pos == -1:
                return matches
            self.imap.seek(pos + 1)
            chunk = self.imap.readline()
            line = chunk.decode('utf-8', 'errors=ignore')
            if not line:
                rep.empty(f)
                start = self.imap.tell() - 1
                continue
            line = line.split('\t')
            matches.append(line[0])
            if limit and limit == len(matches):
                return matches
            ''' imap.tell returns position after the line break (read by
                imap.readline), but we need the line break to find the pattern.
            '''
            start = self.imap.tell() - 1
    
    def close(self):
        f = '[MClient] sources.mdic.get.Index.close'
        if not self.Success:
            rep.cancel(f)
            return
        self.imap.flush()
        self.imap.close()
        self.bin.close()
    
    def _set_pos(self, start=0):
        f = '[MClient] sources.mdic.get.Index._set_pos'
        pos = self.search(start)
        if pos is None:
            return
        self.imap.seek(pos)
        bytes_ = self.imap.readline()
        line = bytes_.decode('utf-8')
        if not line:
            rep.empty(f)
            return
        parts = line.split('\t')
        ''' Remove empty items because 'test\t'.split('\t') outputs
            ['test', '']. Strip to remove \n at the end. Do not strip before
            splitting - we need \t.
        '''
        parts = [part.strip() for part in parts if part.strip()]
        if len(parts) == 1 or len(parts) % 2 != 0:
            self.Success = False
            rep.wrong_input(f, parts)
            return
        for i in range(len(parts)):
            if (i + 1) % 2 == 0:
                self.length.append(parts[i])
            else:
                self.pos.append(parts[i])
        return self.imap.tell()
    
    def set_pos(self):
        f = '[MClient] sources.mdic.get.Index.set_pos'
        if not self.Success:
            rep.cancel(f)
            return
        ''' There can be multiple matches within a portion. In additiom, we
            export the index immediately after finishing the portion to avoid
            performance issues, so there can be multiple identical wforms
            within the index. The index is named after first two characters of
            wforms, so the index is guaranteed to have all matches of the same
            wform.
        '''
        start = 0
        while True:
            start = self._set_pos(start)
            if start is None:
                break
        if not self.pos:
            mes = _('No matches!')
            Message(f, mes).show_info()
            return
        for i in range(len(self.pos)):
            mes = _('Pattern: "{}". Position: {}. Length: {}')
            mes = mes.format(self.wform, self.pos[i], self.length[i])
            Message(f, mes).show_debug()
    
    def run(self):
        self.set_file()
        self.load()
        self.set_pos()
        self.close()



class Body:
    
    def __init__(self):
        self.file = Home('mclient').add_config('dics', 'MDIC', 'collection.mdic')
        self.load()
    
    def load(self):
        f = '[MClient] sources.mdic.get.Body.load'
        if not os.path.exists(self.file):
            self.Success = False
            rep.lazy(f)
            return
        # Ensure that collection.mdic is a file
        self.Success = File(self.file).Success
        if not self.Success:
            rep.cancel(f)
            return
        self.bin = open(self.file, 'rb')
        # 'mmap' fails upon opening an empty file!
        try:
            self.imap = mmap.mmap(self.bin.fileno(), 0, prot=mmap.PROT_READ)
        except Exception as e:
            self.Success = False
            rep.third_part(f, e)
    
    def _get(self, pos, length):
        f = '[MClient] sources.mdic.get.Body._get'
        pos = Input(f, pos).get_integer()
        length = Input(f, length).get_integer()
        self.imap.seek(pos)
        return self.imap.read(length)
    
    def _decompress(self, data):
        f = '[MClient] sources.mdic.get.Body._decompress'
        # If this happens, .mdic is malformed
        if not data:
            self.Success = False
            rep.empty(f)
            return
        try:
            return zstd.decompress(data)
        except Exception as e:
            self.Success = False
            rep.third_party(f, e)
    
    def search(self, wform):
        # Search is case-insensitive for MDIC
        f = '[MClient] sources.mdic.get.Body.search'
        if not self.Success:
            rep.cancel(f)
            return
        wform = wform.lower().strip()
        if not wform:
            # Failed search should not fail the class
            rep.lazy(f)
            return
        timer = Timer(f)
        timer.start()
        iindex = Index(wform)
        iindex.run()
        self.Success = iindex.Success
        if not self.Success:
            rep.cancel(f)
            return
        if not iindex.pos:
            rep.lazy(f)
            return
        # Can be empty if nothing is found, but not if pos list is not empty
        if not iindex.length:
            rep.empty(f)
            return
        matches = []
        for i in range(len(iindex.pos)):
            bytes_ = self._get(iindex.pos[i], iindex.length[i])
            bytes_ = self._decompress(bytes_)
            ''' We do not allow empty or malformed fragments because they can
                be caused by failing storage.
            '''
            if not self.Success:
                rep.cancel(f)
                return
            fragm = bytes_.decode(errors='ignore')
            # Create valid JSON structure
            if not fragm.startswith('{'):
                fragm = '{' + fragm
            fragm = fragm + '}'
            matches.append(fragm)
        timer.end()
        return matches
    
    def close(self):
        f = '[MClient] sources.mdic.get.Body.close'
        if not self.Success:
            rep.cancel(f)
            return
        self.imap.flush()
        self.imap.close()
        self.bin.close()
    
    def suggest(self, pattern, limit=0):
        f = '[MClient] sources.mdic.get.Body.suggest'
        if not self.Success:
            rep.cancel(f)
            return []
        pattern = pattern.strip().lower()
        iindex = Index(pattern)
        iindex.set_file()
        iindex.load()
        self.Success = iindex.Success
        if not self.Success:
            rep.cancel(f)
            return []
        matches = iindex.suggest(pattern, limit)
        iindex.close()
        return matches


ALL_DICS = Body()