#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import mmap
from lxml import etree
from lxml.etree import XMLSyntaxError

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.paths import File, Directory, Path, Home
from skl_shared.time import Timer

# Must be lowercase
'''
FORMATS = ('stardict-0', 'stardict-h', 'stardict-m', 'stardict-x', 'xdxf'
          , 'dictd', 'dsl')
'''
FORMATS = ('stardict-x', 'dsl')


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
            rep.third_party(f, e)
    
    def close(self):
        f = '[MClient] plugins.fora.get.Dic.close'
        if not self.Success:
            rep.cancel(f)
            return
        self.imap.flush()
        self.bin.close()
    
    def get(self, indexes):
        f = '[MClient] plugins.fora.get.Dic.get'
        if not self.Success:
            rep.cancel(f)
            return
        if not indexes:
            rep.empty(f)
            return
        self.imap.seek(indexes[0])
        # -1 may be required by stardict-0 to avoid broken UTF-8
        text = self.imap.read(indexes[1])
        return text.decode(errors='ignore')
    
    def set_file(self):
        f = '[MClient] plugins.fora.get.Dic.set_file'
        if not self.Success:
            rep.cancel(f)
            return
        self.file = os.path.join(self.folder, 'dict.data')
        self.Success = File(self.file, Graphical=False).Success



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
        pos = self.imap.find(bpattern, 0)
        if pos > -1:
            return pos + len(bpattern)
        bpattern = bytes(pattern + '\t', 'utf-8')
        pos = self.imap.find(bpattern, 0)
        if pos == 0:
            return len(bpattern)
    
    def search_all(self, pattern):
        f = '[MClient] plugins.fora.get.Index.search_all'
        if not self.Success:
            rep.cancel(f)
            return
        bpattern = bytes(pattern, 'utf-8')
        poses = []
        pos = 0
        while True:
            pos = self.imap.find(bpattern, pos)
            if pos == -1:
                break
            pos = self.imap.find(b'\t', pos)
            if pos == -1:
                mes = _('File {} has an invalid structure!').format(self.file)
                Message(f, mes).show_warning()
                break
            pos += 1
            poses.append(pos)
        return poses
    
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
        #Message(f, indexes).show_debug()
        return indexes
    
    def set_file(self):
        f = '[MClient] plugins.fora.get.Index.set_file'
        if not self.Success:
            rep.cancel(f)
            return
        self.file = os.path.join(self.folder, 'dict.index')
        self.Success = File(self.file, Graphical=False).Success
    
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
        self.check_format()
    
    def check_format(self):
        f = '[MClient] plugins.fora.get.Properties.check_format'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.format in FORMATS:
            self.Success = False
            mes = _('Dictionary "{}" has an unknown format "{}"!')
            mes = mes.format(self.file, self.format)
            Message(f, mes).show_warning()
    
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
        return ''
    
    def set_attrs(self):
        f = '[MClient] plugins.fora.get.Properties.set_attrs'
        if not self.Success:
            rep.cancel(f)
            return
        self.name = self._get_attr('name').replace('[', '(').replace(']', ')')
        self.format = self._get_attr('contentFormat')
        # Format can be called several times, so we just save the trouble here
        if self.format:
            self.format = self.format.lower()
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
        self.pattern = ''
        self.prop = Properties(folder)
        self.index = Index(folder)
        self.dic = Dic(folder)
        self.Success = self.prop.Success and self.index.Success and self.dic.Success
    
    def get_lang1(self):
        return self.prop.lang1
    
    def get_lang2(self):
        return self.prop.lang2
    
    def get_format(self):
        return self.prop.format
    
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
        self.pattern = pattern
        pos = self.index.search(self.pattern)
        if not pos:
            return
        indexes = self.index.get(pos)
        self.article = self.dic.get(indexes)
        if self.article.strip():
            self.article = '<dic>' + self.get_name() + '</dic>' + self.article
        return self.article
    
    def search_all(self, pattern):
        f = '[MClient] plugins.fora.get.Fora.search_all'
        if not self.Success:
            rep.cancel(f)
            return
        self.article = ''
        self.pattern = pattern
        poses = self.index.search_all(self.pattern)
        if not poses:
            return
        for pos in poses:
            indexes = self.index.get(pos)
            article = self.dic.get(indexes)
            if article:
                self.article += article + '\n'
        if self.article.strip():
            self.article = '<dic>' + self.get_name() + '</dic>' + self.article
        return self.article
    
    def close(self):
        f = '[MClient] plugins.fora.get.Fora.close'
        if not self.Success:
            rep.cancel(f)
            return
        self.index.close()
        self.dic.close()



class AllDics:
    
    def __init__(self):
        self.Success = True
        self.dics = []
        self.path = Home('mclient').add_config('dics')
        self.set()
    
    def get_valid(self):
        return [dic for dic in self.dics if dic.Success]
    
    def get_invalid(self):
        return [dic for dic in self.dics if not dic.Success]
    
    def get_summary(self):
        f = '[MClient] plugins.fora.get.AllDics.get_summary'
        if not self.Success:
            rep.cancel(f)
            return
        format_dic = {}
        errors = []
        mes = []
        names = []
        pairs = []
        formats = []
        sub = _('Names:')
        mes.append(sub)
        for dic in self.dics:
            if not dic.Success:
                errors.append(dic.get_file())
                continue
            names.append(dic.get_name())
            pairs.append(f'{dic.get_lang1()}-{dic.get_lang2()}')
            formats.append(dic.get_format())
            if not dic.get_format() in format_dic:
                format_dic[dic.get_format()] = []
            format_dic[dic.get_format()].append(dic.get_file())
        mes += names
        mes.append('')
        pairs = sorted(set(pairs))
        sub = _('Languages: {}').format(', '.join(pairs))
        mes.append(sub)
        formats = sorted(set(formats))
        sub = _('Formats: {}').format(', '.join(formats))
        mes.append(sub)
        if errors:
            mes.append('')
            sub = _('Files with errors:')
            mes.append(sub)
            mes += errors
        mes.append('')
        for format_ in format_dic:
            sub = f'{format_}:'
            mes.append(sub)
            mes += format_dic[format_]
            mes.append('')
        return '{}:\n{}'.format(f, '\n'.join(mes))
    
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
            rep.lazy(f)
            return
        for file in files:
            ipath = Path(file)
            if ipath.get_filename() != 'fdblite.properties':
                continue
            self.dics.append(Fora(ipath.get_dirname()))
        timer.end()
        if not self.get_valid():
            self.Success = False
            rep.empty_output(f)
    
    def search(self, pattern):
        f = '[MClient] plugins.fora.get.AllDics.search'
        if not self.Success:
            rep.cancel(f)
            return
        if not pattern:
            rep.empty(f)
            return
        timer = Timer(f)
        timer.start()
        for dic in self.dics:
            dic.search(pattern)
        timer.end()
        articles = [dic.article for dic in self.dics \
                   if dic.Success and dic.article]
        mes = _('"{}": {} matches in {} Fora dictionaries')
        mes = mes.format(pattern, len(articles), len(self.get_valid()))
        Message(f, mes).show_debug()
        ''' #NOTE: This output should be used for debugging purposes only,
            since it is incorrect to join articles of different formats.
        '''
        return '\n\n'.join(articles)
    
    def close(self):
        f = '[MClient] plugins.fora.get.AllDics.close'
        if not self.Success:
            rep.cancel(f)
            return
        for dic in self.dics:
            dic.close()



class Get:
    # This class is basically needed for compliance with other code
    def __init__(self, search):
        self.htm = ''
        self.pattern = search
    
    def debug(self):
        return ALL_DICS.get_summary()
    
    def run(self):
        ''' #NOTE: This output should be used for debugging purposes only,
            since it is incorrect to join articles of different formats.
        '''
        return ALL_DICS.search(self.pattern)


ALL_DICS = AllDics()
