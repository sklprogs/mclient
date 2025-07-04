#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import struct
import os
import zlib
from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.time import Timer
from skl_shared.paths import Path, File, Directory
from skl_shared.logic import Input
from skl_shared.graphics.progress_bar.controller import PROGRESS


''' A directory storing all stardict files.
    #NOTE: Do not forget to change this variable externally before calling
    anything from this module.
'''
PATH = ''


class Suggest:
    
    def __init__(self, search):
        self.set_values()
        if search:
            self.reset(search)
    
    def set_values(self):
        self.Success = True
        self.pattern = ''
    
    def reset(self, search):
        f = '[MClient] plugins.stardict.get.Suggest.reset'
        self.pattern = search
        if not self.pattern:
            self.Success = False
            rep.empty(f)
    
    def get(self):
        f = '[MClient] plugins.stardict.get.Suggest.get'
        if not self.Success:
            rep.cancel(f)
            return
        items = objs.get_all_dics().get_index()
        if not items:
            self.Success = False
            rep.empty(f)
            return
        timer = Timer(f)
        timer.start()
        search = self.pattern.lower()
        result = [item for item in items if str(item).lower().startswith(search)]
        timer.end()
        mes = '; '.join(result)
        Message(f, mes).show_debug()
        return result
    
    def run(self):
        return self.get()



class Get:
    # This class is basically needed for compliance with other code
    def __init__(self, search):
        self.htm = ''
        self.pattern = search
    
    def run(self):
        f = '[MClient] plugins.stardict.get.Get.run'
        if not PATH or not self.pattern:
            rep.empty(f)
            return
        return objs.get_all_dics().get(self.pattern)



class DictZip:
    # Based on https://github.com/cz7asm/pyStarDictViewer
    # Read archives in '.dict.dz' format
    def __init__(self, path=''):
        if path:
            self.reset(path)
    
    def set_values(self):
        self.obj = None
        self.Success = True
        self.deflate = zlib.decompressobj(-15)
        self.path = ''
        self.len_ = 0
        self.size = 0
        self.offset = 0
        self.offsets = 0
        self.count = 0
    
    def reset(self, path):
        self.set_values()
        self.path = path
        self.Success = File(self.path).Success
        self.load()
    
    def load(self):
        f = '[MClient] plugins.stardict.get.DictZip.load'
        if not self.Success:
            rep.cancel(f)
            return
        try:
            self.obj = open(self.path, 'rb')
            info = self._read_header()
            self.len_ = info[0]
            self.size = info[1]
            self.offsets = info[2]
            self.count = len(self.size)
        except Exception as e:
            self.Success = False
            mes = _('Failed to load "{}"!\n\nDetails: {}')
            mes = mes.format(self.path, e)
            Message(f, mes, True).show_warning()

    def _read_header(self):
        # This method is internal and should be wrapped with try-except
        self.obj.seek(0)
        # Check header parameters
        header = self.obj.read(10)
        #TODO: fail on error
        if header[:2] != b'\x1f\x8b':
            message = _('GZIP signature is expected, but found "{}"!')
            message = message.format(header[:2])
            raise ValueError(message)
        if header[2] != 8:
            raise ValueError(_('Only DEFLATE archives are supported!'))
        flags = header[3]
        if not flags&(1<<2):
            raise ValueError(_('An extra dictzip field is expected!'))
        # Read dictzip data
        XLEN, SI1, SI2, LEN = struct.unpack('<H2cH', self.obj.read(6))
        if SI1+SI2 != b'RA':
            raise ValueError(_('An RA signature is expected!'))
        data = self.obj.read(LEN)
        VER, CHLEN, CHCNT = struct.unpack('<3H', data[:6])
        sizes = struct.unpack('<'+str(CHCNT)+'H', data[6:])
        # Skip filename if present
        if flags&(1<<3):
            while self.obj.read(1) != b'\x00':
                pass
        # Transform sizes into start offsets of chunks
        ofs = [self.obj.tell()]
        for s in sizes[:-1]:
            ofs.append(ofs[-1]+s)
        return CHLEN, sizes, ofs

    def seek(self, offset):
        # This is only to provide a file-like interface
        self.offset = offset

    def read(self, size):
        ''' - Determines which chunk to read and decompress.
            - It's possible that data overrun to the following chunk so this
              must be handled too.
            - Do not rename this function since 'read' can be called on
              a different class.
        '''
        f = '[MClient] plugins.stardict.get.DictZip.read'
        if not self.Success:
            rep.cancel(f)
            return
        # Prevent 'ZeroDivisionError'
        if not self.len_:
            # You've probably forgot to run 'self.load' first
            rep.empty(f)
            return
        chunk = self.offset // self.len_
        self.obj.seek(self.offsets[chunk])
        compr = self.obj.read(self.size[chunk])
        data = self.deflate.decompress(compr)
        # Offset in the chunk
        chofs = self.offset % self.len_
        if chofs + size > self.len_:
            # Data continue in the next chunk
            out = data[chofs:]
            self.seek(self.offset + len(out))
            out += self.read(size - len(out))
        else:
            # All in the current chunk
            out = data[chofs:chofs+size]
        return out

    def close(self):
        f = '[MClient] plugins.stardict.get.DictZip.close'
        if not self.Success:
            rep.cancel(f)
            return
        self.obj.close()



class StarDict:
    # Based on https://github.com/cz7asm/pyStarDictViewer
    def __init__(self, ifopath=''):
        if ifopath:
            self.reset(ifopath)
    
    def reset(self, ifopath):
        self.set_values()
        self.path = ifopath
        ipath = Path(self.path)
        ''' We need a filename with an absolute path here. 'file'[:-4]
            does the same thing (providing that extensions are only 3 symbols
            long). 'Path' is more precise for other cases.
        '''
        self.bname = os.path.join(ipath.get_dirname(), ipath.get_basename())
        self.Success = File(self.path).Success
        self.check()
        self.set_meta()

    def set_values(self):
        self.Success = True
        self.Block = False
        self.dictf = None
        self.idx = []
        self.ifo = {}
        self.wcount = 0
        self.path = ''
        self.bname = ''
        self.title = ''
        self.transl = ''
    
    def set_meta(self):
        f = '[MClient] plugins.stardict.get.Stardict.set_meta'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.ifo:
            rep.empty(f)
            return
        if not 'bookname' in self.ifo or not 'wordcount' in self.ifo:
            self.Success = False
            mes = _('File "{}" is incorrect!')
            mes = mes.format(self.bname + '.ifo')
            Message(f, mes, True).show_warning()
            return
        self.title = str(self.ifo['bookname'])
        self.wcount = Input(f, self.ifo['wordcount']).get_integer()
    
    def fail(self, f, e):
        self.Success = False
        mes = _('Failed to load "{}"!\n\nDetails: {}')
        mes = mes.format(self.path, e)
        Message(f, mes, True).show_warning()
    
    def check(self):
        ''' Load .ifo data and check that all needed dictionary files
            are present.
        '''
        f = '[MClient] plugins.stardict.get.Stardict.check'
        if not self.Success:
            rep.cancel(f)
            return
        try:
            for line in open (file = self.bname + '.ifo'
                             ,encoding = 'UTF-8'
                             ).readlines()[1:]:
                pair = line.split('=')
                self.ifo[pair[0]] = pair[1][:-1]

            if (not os.path.exists(self.bname + '.idx')):
                raise ValueError('An .idx file is missing!')

            if (not os.path.exists(self.bname + '.dict') and \
            not os.path.exists(self.bname + '.dict.dz')):
                raise ValueError('A .dict file is missing!')
        except Exception as e:
            self.fail(f, e)
    
    def load(self):
        ''' Build a list of (word, (dict_index, length)) tuples from .idx and
            open .dict[.dz] file for reading.
        '''
        f = '[MClient] plugins.stardict.get.Stardict.load'
        if not self.Success:
            rep.cancel(f)
            return
        idx = self.bname + '.idx'
        iopen = open(idx, 'rb')
        data = iopen.read(os.path.getsize(idx))
        iopen.close()
        a = 0
        b = data.find(b'\0', a)
        while b > 0:
            try:
                self.idx.append ((data[a:b].decode('utf-8')
                                 ,struct.unpack('>LL', data[b+1:b+9])
                                 ))
            except Exception as e:
                self.fail(f, e)
                return
            a = b + 9
            b = data.find(b'\0', a)
        if self.wcount != len(self.idx):
            self.Success = False
            sub = f'{self.wcount} = {len(self.idx)}'
            mes = _('The condition "{}" is not observed!').format(sub)
            Message(f, mes, True).show_error()
        if not self.Success:
            rep.cancel(f)
            return
        # Compression of .dict is optional
        try:
            self.dictf = open(self.bname + '.dict', 'rb')
        except IOError:
            self.dictf = DictZip(self.bname + '.dict.dz')

    def unload(self):
        # Release idx word list and opened .dict file
        f = '[MClient] plugins.stardict.get.Stardict.unload'
        if not self.Success:
            rep.cancel(f)
            return
        self.idx = []
        self.dictf.close()

    def __len__(self):
        return len(self.idx)

    def __getitem__(self, key):
        ''' int and slice return coresponding words string key is used for
            reverse lookup.
        '''
        f = '[MClient] plugins.stardict.get.Stardict.__getitem__'
        if not self.Success:
            rep.cancel(f)
            return
        if type(key) is int:
            return self.idx[key][0]
        if type(key) is slice:
            return [w[0] for w in self.idx[key]]
        if type(key) is str:
            return Input(title=f, value=self.search(key)).get_integer()

    def search(self, word, prefix=False):
        ''' Binary search for words in idx list. In case prefix=True,
            the search will be performed for the lowest record with 'word' as
            its prefix.
        '''
        f = '[MClient] plugins.stardict.get.Stardict.search'
        if not self.Success:
            rep.cancel(f)
            return
        if word == '':
            return -1
        a, b = 0, len(self.idx) - 1
        if (b < 0):
             return -1
        word = word.lower()
        while a <= b:                
            i = a + (b - a) // 2
            if prefix:
                # Search words that include 'word' in their prefix
                if self.idx[i][0].lower().startswith(word):
                    if i and self.idx[i-1][0].lower().startswith(word):
                        b = i - 1
                        continue
                    else:
                        return i
            else:
                # Search for the entire match
                if self.idx[i][0].lower() == word:
                    return i
            if a == b:
                # No match
                return -1
            elif word > self.idx[i][0].lower():
                # Move upward
                a = i + 1
            else:
                # Move downward
                b = i - 1
        return -1
    
    def get_dict_link(self, index):
        f = '[MClient] plugins.stardict.get.Stardict.get_dict_link'
        if not self.Success:
            rep.cancel(f)
            return
        # Return (dict_index, len) tuple of a word on a given index
        return self.idx[index][1]

    def get_dict_data(self, index):
        f = '[MClient] plugins.stardict.get.Stardict.get_dict_data'
        if not self.Success:
            rep.cancel(f)
            return
        # Return a translation for a word on the given index
        if not self.dictf:
            rep.empty(f)
            return
        self.dictf.seek(self.idx[index][1][0])
        result = self.dictf.read(self.idx[index][1][1])
        if result:
            return result.decode()

    def __str__(self):
        return str(self.ifo)



class AllDics:
    
    def __init__(self):
        self.set_values()
        self.reset()
    
    def get_index(self):
        f = '[MClient] plugins.stardict.get.AllDics.get_index'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.index_:
            for idic in self.dics:
                if idic.idx:
                    self.index_ += [item[0] for item in idic.idx]
        return self.index_
    
    def get(self, search):
        f = '[MClient] plugins.stardict.get.AllDics.get'
        if not self.Success:
            rep.cancel(f)
            return
        if not search:
            rep.empty(f)
            return
        dics = [dic for dic in self.dics if not dic.Block]
        lst = []
        for dic in dics:
            ind = dic.search(search, True)
            # Returns True if ind >= 0
            if not str(ind).isdigit():
                mes = _('No matches for "{}"!').format(dic.title)
                Message(f, mes).show_info()
                return ''
            result = dic.get_dict_data(ind)
            if result:
                # Set offline dictionary title
                lst.append(f'<dic>{dic.title}</dic>{result}')
                mes = _('"{}" has matches for "{}"')
                mes = mes.format(dic.title, search)
                Message(f, mes).show_debug()
        return '\n'.join(lst)
    
    def set_values(self):
        self.ifos = []
        self.dics = []
        self.index_ = []
        self.path = ''
        # Do not run anything if 'self.reset' was not run
        self.Success = False
    
    def reset(self):
        self.set_values()
        self.path = PATH
        self.Success = Directory(self.path).Success
    
    def walk(self):
        ''' Explore all subdirectories of path searching for filenames that
            have all three .ifo, .idx and .dict[.dz] suffixes.
        '''
        f = '[MClient] plugins.stardict.get.AllDics.walk'
        if not self.Success:
            rep.cancel(f)
            return
        if self.ifos:
            return self.ifos
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if not file.endswith('.ifo'):
                    continue
                ''' #TODO: #FIX: Path.basename works incorrectly for cases
                    like file.dict.dz.
                '''
                name = file[:-4]
                if (name + '.idx' in files and (name + '.dict.dz' in files
                                                or name + '.dict' in files)):
                    self.ifos.append(os.path.join(root, name + '.ifo'))
        return self.ifos
    
    def locate(self):
        f = '[MClient] plugins.stardict.get.AllDics.locate'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.dics:
            if self.walk():
                for ifo in self.ifos:
                    self.dics.append(StarDict(ifo))
                self.dics = sorted(self.dics, key=lambda d:d.title+str(d.wcount))
            else:
                rep.lazy(f)
        mes = _('{} offline dictionaries are available').format(len(self.dics))
        Message(f, mes).show_info()
        return self.dics
    
    def load(self):
        f = '[MClient] plugins.stardict.get.AllDics.load'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.locate():
            rep.lazy(f)
            return
        PROGRESS.set_title(_('Dictionary Loader'))
        PROGRESS.show()
        PROGRESS.set_value(0)
        PROGRESS.set_max(len(self.dics))
        timer = Timer(f)
        timer.start()
        for i in range(len(self.dics)):
            PROGRESS.update()
            text = _('Load Stardict dictionaries ({}/{})')
            text = text.format(i + 1, len(self.dics))
            PROGRESS.set_info(text)
            self.dics[i].load()
            PROGRESS.inc()
        timer.end()
        total_no = len(self.dics)
        self.dics = [dic for dic in self.dics if dic.Success]
        mes = _('Dictionaries loaded: {}/{}').format(len(self.dics), total_no)
        Message(f, mes).show_info()
        PROGRESS.close()



class Objects:
    
    def __init__(self):
        self.alldics = None
        
    def get_all_dics(self):
        if self.alldics is None:
            self.alldics = AllDics()
            self.alldics.load()
        return self.alldics



class Commands:
    
    def is_accessible(self):
        return len(objs.get_all_dics().dics)


objs = Objects()
com = Commands()
