#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import mmap

from skl_shared.localize import _
from skl_shared.message.controller import rep, Message
from skl_shared.paths import Home, File
from skl_shared.time import Timer


class Index:
    
    def __init__(self, wform):
        self.Success = True
        self.wform = wform
        self.folder = Home('mclient').add_config('dics', 'MDIC', 'collection.indexes')
        self.file = ''
        self.pos = -1
        self.length = 0
    
    def _get_abbr(self):
        abbr = [char for char in self.wform.lower() if str(char).isalpha()]
        abbr = ''.join(abbr)
        return abbr[0:2]
    
    def set_file(self):
        f = '[MClient] plugins.mdic.get.Index.set_file'
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
        f = '[MClient] plugins.mdic.get.Index.load'
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
    
    def search(self):
        f = '[MClient] plugins.mdic.get.Index.search'
        if not self.Success:
            rep.cancel(f)
            return
        bpattern = bytes('\n' + self.wform + '\t', 'utf-8')
        pos = self.imap.find(bpattern, 0)
        if pos > -1:
            return pos + len(bpattern)
        bpattern = bytes(self.wform + '\t', 'utf-8')
        pos = self.imap.find(bpattern, 0)
        if pos == 0:
            return len(bpattern)
    
    def close(self):
        f = '[MClient] plugins.mdic.get.Index.close'
        if not self.Success:
            rep.cancel(f)
            return
        self.imap.flush()
        self.bin.close()
    
    def set_pos(self):
        f = '[MClient] plugins.mdic.get.Index.set_pos'
        if not self.Success:
            rep.cancel(f)
            return
        pos = self.search()
        if pos is None:
            mes = _('No matches!')
            Message(f, mes).show_info()
            return
        self.imap.seek(pos)
        bytes_ = self.imap.readline()
        line = bytes_.decode('utf-8')
        parts = line.split('\t')
        if len(parts) != 2:
            self.Success = False
            rep.wrong_input(f)
            return
        self.pos = int(parts[0])
        self.length = int(parts[1])
        mes = _('Position: {}. Length: {}').format(self.pos, self.length)
        Message(f, mes).show_debug()
    
    def run(self):
        self.set_file()
        self.load()
        self.set_pos()
        self.close()



class Body:
    
    def __init__(self):
        self.file = Home('mclient').add_config('dics', 'MDIC', 'collection.mdic')
        self.Success = File(self.file).Success
        self.load()
    
    def load(self):
        f = '[MClient] plugins.mdic.get.Body.load'
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
        f = '[MClient] plugins.mdic.get.Body._get'
        self.imap.seek(pos)
        text = self.imap.read(length)
        return text.decode(errors='ignore')
    
    def search(self, wform):
        f = '[MClient] plugins.mdic.get.Body.search'
        if not self.Success:
            rep.cancel(f)
            return
        if not wform:
            rep.empty(f)
            return
        timer = Timer(f)
        timer.start()
        iindex = Index(wform)
        iindex.run()
        self.Success = iindex.Success
        if not self.Success:
            return
        if not iindex.length:
            rep.lazy(f)
            return
        text = self._get(iindex.pos, iindex.length)
        timer.end()
        return text
    
    def close(self):
        f = '[MClient] plugins.mdic.get.Body.close'
        if not self.Success:
            rep.cancel(f)
            return
        self.imap.flush()
        self.bin.close()


ALL_DICS = Body()