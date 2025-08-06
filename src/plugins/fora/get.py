#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import mmap
from lxml import etree
from lxml.etree import XMLSyntaxError

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.paths import File, Directory, Path
from skl_shared.time import Timer


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
        return text.decode()
    
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



class Properties:
    
    def __init__(self, folder):
        self.file = ''
        self.lang1 = ''
        self.lang2 = ''
        self.format = ''
        self.name = _('Fora Dictionary')
        self.Success = True
        self.folder = folder
        self.set_file()
        self.load()
        self.set_attrs()
    
    def set_file(self):
        f = '[MClient] plugins.fora.get.Properties.set_file'
        if not self.Success:
            rep.cancel(f)
            return
        self.file = os.path.join(self.folder, 'fdblite.properties')
        self.Success = File(self.file).Success
    
    def load(self):
        f = '[MClient] plugins.fora.get.Properties.load'
        if not self.Success:
            rep.cancel(f)
            return
        try:
            self.root = etree.parse(self.file)
        except Exception as e:
            #TODO: Try recover=True
            self.Success = False
            mes = _('Unable to process "{}"! Details: {}').format(self.file, e)
            Message(f, mes).show_error()
    
    def _get_attr(self, attr):
        items = self.root.xpath(f'//entry[@key="{attr}"]/text()')
        if items:
            return items[0]
    
    def set_attrs(self):
        f = '[MClient] plugins.fora.get.Properties.set_attrs'
        if not self.Success:
            rep.cancel(f)
            return
        self.name = self._get_attr('name')
        self.format = self._get_attr('contentFormat')
        self.lang1 = self._get_attr('sourceLanguage')
        self.lang2 = self._get_attr('targetLanguage')
    
    def debug(self):
        f = '[MClient] plugins.fora.get.Properties.debug'
        if not self.Success:
            rep.cancel(f)
            return
        mes = []
        sub = _('File: "{}"').format(self.file)
        mes.append(sub)
        sub = _('Dictionary name: "{}"').format(self.name)
        mes.append(sub)
        sub = _('Format: "{}"').format(self.format)
        mes.append(sub)
        sub = _('Source language: "{}"').format(self.lang1)
        mes.append(sub)
        sub = _('Target language: "{}"').format(self.lang2)
        mes.append(sub)
        mes.append('')
        return '\n'.join(mes)



class Fora:
    
    def __init__(self, folder):
        self.article = ''
        self.prop = Properties(folder)
        self.index = Index(folder)
        self.dic = Dic(folder)
        self.Success = self.prop.Success and self.index.Success and self.dic.Success
    
    def get_name(self):
        return self.prop.name
    
    def get_file(self):
        return self.dic.file
    
    def search(self, pattern):
        f = '[MClient] plugins.fora.get.Fora.search'
        if not self.Success:
            rep.cancel(f)
            return
        self.article = ''
        pos = self.index.search(pattern)
        if not pos:
            '''
            mes = _('No matches for "{}" in "{}" ({})!')
            mes = mes.format(pattern, self.prop.name, self.dic.file)
            Message(f, mes).show_debug()
            '''
            return
        indexes = self.index.get(pos)
        self.article = self.dic.get(indexes)
        #mes = f'"{self.article}"'
        #Message(f, mes).show_debug()
        return self.article
    
    def close(self):
        f = '[MClient] plugins.fora.get.Fora.close'
        if not self.Success:
            rep.cancel(f)
            return
        self.index.close()
        self.dic.close()



class AllDics:
    
    def __init__(self, path):
        self.Success = True
        self.successful = 0
        self.dics = []
        self.path = path
        self.set()
    
    def set_successful(self):
        f = '[MClient] plugins.fora.get.AllDics.set_successful'
        if not self.Success:
            rep.cancel(f)
            return
        for dic in self.dics:
            if dic.Success:
                self.successful += 1
    
    def set(self):
        f = '[MClient] plugins.fora.get.AllDics.set'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.path:
            self.Success = False
            rep.empty(f)
            return
        timer = Timer(f)
        timer.start()
        idir = Directory(self.path)
        files = idir.get_subfiles()
        if not files:
            self.Success = False
            rep.empty(f)
            return
        for file in files:
            ipath = Path(file)
            if ipath.get_filename() != 'fdblite.properties':
                continue
            self.dics.append(Fora(ipath.get_dirname()))
        self.set_successful()
        timer.end()
        if not self.successful:
            self.Success = False
            rep.empty_output(f)
    
    def search(self, pattern):
        f = '[MClient] plugins.fora.get.AllDics.search'
        if not self.Success:
            rep.cancel(f)
            return
        timer = Timer(f)
        timer.start()
        count = 0
        for dic in self.dics:
            if dic.search(pattern):
                count += 1
        timer.end()
        mes = _('"{}": {} matches in {} Fora dictionaries')
        mes = mes.format(pattern, count, self.successful)
        Message(f, mes).show_debug()
    
    def close(self):
        f = '[MClient] plugins.fora.get.AllDics.close'
        if not self.Success:
            rep.cancel(f)
            return
        for dic in self.dics:
            dic.close()
