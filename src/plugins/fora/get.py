#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import mmap
from lxml import etree
from lxml.etree import XMLSyntaxError

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.paths import File


class Dic:
    
    def __init__(self, folder):
        self.Success = True
        self.folder = folder
        self.set_file()
        self.load()
    
    def load(self):
        f = '[MClient] plugins.fora.get.Dic.load'
        if not self.Success:
            rep.cancel(f)
            return
        # .index can be opened as a text file, but no need to read it in full
        self.bin = open(self.file, 'rb')
        # 'mmap' fails upon opening an empty file!
        try:
            self.imap = mmap.mmap(self.bin.fileno(), 0, prot=mmap.PROT_READ)
        except Exception as e:
            self.Success = False
            mes = _('Third-party module has failed!\n\nDetails: {}').format(e)
            Message(f, mes).show_error()
    
    def close(self):
        f = '[MClient] plugins.fora.get.Dic.close'
        if not self.Success:
            rep.cancel(f)
            return
        self.imap.flush()
        self.bin.close()
    
    def get(self, indexes):
        f = '[MClient] plugins.fora.get.Dic.search'
        if not self.Success:
            rep.cancel(f)
            return
        if not indexes:
            rep.empty(f)
            return
        self.imap.seek(indexes[0])
        text = self.imap.read(indexes[1])
        text = text.decode()
        mes = f'"{text}"'
        Message(f, mes).show_debug()
        return text
    
    def set_file(self):
        f = '[MClient] plugins.fora.get.Dic.set_file'
        if not self.Success:
            rep.cancel(f)
            return
        self.file = os.path.join(self.folder, 'dict.data')
        self.Success = File(self.file).Success



class Index:
    
    def __init__(self, folder):
        self.Success = True
        self.b64_list = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        self.folder = folder
        self.set_file()
        self.load()
    
    def load(self):
        f = '[MClient] plugins.fora.get.Index.load'
        if not self.Success:
            rep.cancel(f)
            return
        # .index can be opened as a text file, but no need to read it in full
        self.bin = open(self.file, 'rb')
        # 'mmap' fails upon opening an empty file!
        try:
            self.imap = mmap.mmap(self.bin.fileno(), 0, prot=mmap.PROT_READ)
        except Exception as e:
            self.Success = False
            mes = _('Third-party module has failed!\n\nDetails: {}').format(e)
            Message(f, mes).show_error()
    
    def close(self):
        f = '[MClient] plugins.fora.get.Index.close'
        if not self.Success:
            rep.cancel(f)
            return
        self.imap.flush()
        self.bin.close()
    
    def search(self, pattern):
        f = '[MClient] plugins.fora.get.Index.search'
        if not self.Success:
            rep.cancel(f)
            return
        bpattern = bytes('\n' + pattern + '\t', 'utf-8')
        pos = self.imap.find(bpattern)
        if pos > -1:
            return pos + len(bpattern)
        bpattern = bytes(pattern + '\t', 'utf-8')
        pos = self.imap.find(bpattern)
        if pos == 0:
            return len(bpattern)
    
    def get(self, pos):
        f = '[MClient] plugins.fora.get.Index.get'
        if not self.Success:
            rep.cancel(f)
            return
        if pos is None:
            rep.empty(f)
            return
        self.imap.seek(pos)
        indexes = self.imap.readline()
        indexes = indexes.decode()
        indexes = indexes.strip()
        indexes = indexes.split('\t')
        if len(indexes) != 2:
            mes = f'{len(indexes)} == 2'
            rep.condition(f, mes)
            return
        indexes = [self.decode(index) for index in indexes]
        if None in indexes:
            rep.wrong_input(f, indexes)
            return
        Message(f, indexes).show_debug()
        return indexes
    
    def set_file(self):
        f = '[MClient] plugins.fora.get.Index.set_file'
        if not self.Success:
            rep.cancel(f)
            return
        self.file = os.path.join(self.folder, 'dict.index')
        self.Success = File(self.file).Success
    
    def decode(self, index):
        ''' - See https://github.com/jgoerzen/dictdlib.git.
            - Take a string as input and return an integer value of it decoded
              with the base64 algorithm used by dict indexes.
        '''
        f = '[MClient] plugins.fora.get.Index.decode'
        if not self.Success:
            rep.cancel(f)
            return
        if not index:
            # Do not fail the class upon an empty search
            rep.empty(f)
            return
        retval = 0
        shiftval = 0
        for i in range(len(index) - 1, -1, -1):
            val = self.b64_list.index(index[i])
            retval = retval | (val << shiftval)
            shiftval += 6
        return retval
