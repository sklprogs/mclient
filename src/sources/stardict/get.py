#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import struct
import os
import mmap
import zlib
from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.time import Timer
from skl_shared.paths import Home, Path, File, Directory
from skl_shared.logic import Input

INDEX = {}


class Suggest:
    
    def __init__(self, search):
        self.set_values()
        if search:
            self.reset(search)
    
    def set_values(self):
        self.Success = True
        self.pattern = ''
    
    def reset(self, search):
        f = '[MClient] sources.stardict.get.Suggest.reset'
        self.pattern = search
        if not self.pattern:
            self.Success = False
            rep.empty(f)
    
    def get(self):
        f = '[MClient] sources.stardict.get.Suggest.get'
        if not self.Success:
            rep.cancel(f)
            return
        return ALL_DICS.get_all(self.pattern)
    
    def run(self):
        return self.get()



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
        f = '[MClient] sources.stardict.get.DictZip.load'
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
            mes = _('Failed to load "{}"!\n\nDetails: {}').format(self.path, e)
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
        f = '[MClient] sources.stardict.get.DictZip.read'
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
        f = '[MClient] sources.stardict.get.DictZip.close'
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
        self.idx = None
        self.map = None
        self.ifo = {}
        self.wcount = 0
        self.path = ''
        self.bname = ''
        self.title = ''
        self.transl = ''
    
    def set_meta(self):
        f = '[MClient] sources.stardict.get.Stardict.set_meta'
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
        f = '[MClient] sources.stardict.get.Stardict.check'
        if not self.Success:
            rep.cancel(f)
            return
        try:
            for line in open(file = self.bname + '.ifo'
                            ,encoding = 'UTF-8').readlines()[1:]:
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
        f = '[MClient] sources.stardict.get.Stardict.load'
        if not self.Success:
            rep.cancel(f)
            return
        idx = self.bname + '.idx'
        self.idx = open(idx, 'rb')
        # Setting 'prot' avoids PermissionError
        self.map = mmap.mmap(self.idx.fileno(), 0, prot=mmap.PROT_READ)
        # Compression of .dict is optional
        try:
            self.dictf = open(self.bname + '.dict', 'rb')
        except IOError:
            self.dictf = DictZip(self.bname + '.dict.dz')

    def unload(self):
        f = '[MClient] sources.stardict.get.Stardict.unload'
        if not self.Success:
            rep.cancel(f)
            return
        self.map = None
        self.idx.close()
        self.dictf.close()

    def _get_index_data(self, pos, len_):
        self.idx.seek(pos)
        return self.idx.read(len_)
    
    def _get_index(self, end):
        chunk = self._get_index_data(end, 8)
        index, len_ = struct.unpack('>LL', chunk)
        return(index, len_)
    
    def search(self, pattern):
        f = '[MClient] sources.stardict.get.Stardict.search'
        if not self.Success:
            rep.cancel(f)
            return
        if not pattern:
            rep.empty(f)
            return
        bytes_ = bytes(pattern, 'utf-8') + b'\x00'
        start = self.map.find(bytes_)
        if start == -1:
            return
        index, len_ = self._get_index(start + len(bytes_))
        mes = _('Pattern: "{}", position in dictionary: {}, article length: {}')
        mes = mes.format(pattern, index, len_)
        Message(f, mes).show_debug()
        return(index, len_)
    
    def _find_end(self, start):
        return self.map.find(b'\x00', start)
    
    def _find_next(self, bytes_, start):
        f = '[MClient] sources.stardict.get.Stardict._find_next'
        start = self.map.find(bytes_, start)
        if start == -1:
            return
        end = self._find_end(start + len(bytes_))
        if end == -1:
            return
        chunk = self._get_index_data(start, end - start)
        if chunk:
            return(chunk.decode(errors='ignore'), end)
    
    def find_all(self, bytes_):
        f = '[MClient] sources.stardict.get.Stardict.find_all'
        if not self.Success:
            rep.cancel(f)
            return
        if not bytes_:
            rep.empty(f)
            return
        results = []
        start = 0
        while True:
            tuple_ = self._find_next(bytes_, start)
            if not tuple_:
                return results
            match_, start = tuple_[0], tuple_[1]
            '''
            # Print index for all matches (useful for debugging)
            index, len_ = self._get_index(self._find_end(start) + 1)
            mes = _('Pattern: "{}", position in dictionary: {}, article length: {}')
            mes = mes.format(match_, index, len_)
            Message(f, mes).show_debug()
            '''
            results.append(match_)
            start += 1
    
    def get_dict_data(self, index, len_):
        f = '[MClient] sources.stardict.get.Stardict.get_dict_data'
        if not self.Success:
            rep.cancel(f)
            return
        # Return a translation for a word on the given index
        if not self.dictf:
            rep.empty(f)
            return
        self.dictf.seek(index)
        chunk = self.dictf.read(len_)
        if chunk:
            return chunk.decode(errors='ignore')

    def __str__(self):
        return str(self.ifo)



class AllDics:
    
    def __init__(self):
        self.ifos = []
        self.dics = []
        self.index_ = []
        self.path = Home('mclient').add_config('dics')
        self.Success = Directory(self.path).Success
        self.load()
    
    def get_valid(self):
        return [dic for dic in self.dics if dic.Success]
    
    def get_invalid(self):
        return [dic for dic in self.dics if not dic.Success]
    
    def get_index(self):
        f = '[MClient] sources.stardict.get.AllDics.get_index'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.index_:
            for idic in self.dics:
                if idic.idx:
                    self.index_ += [item[0] for item in idic.idx]
        return self.index_
    
    def get(self, search):
        f = '[MClient] sources.stardict.get.AllDics.get'
        if not self.Success:
            rep.cancel(f)
            return
        if not search:
            rep.empty(f)
            return
        dics = [dic for dic in self.dics if not dic.Block]
        lst = []
        for dic in dics:
            tuple_ = dic.search(search)
            if tuple_ is None:
                mes = _('No matches for "{}"!').format(dic.title)
                Message(f, mes).show_info()
                continue
            result = dic.get_dict_data(tuple_[0], tuple_[1])
            if result:
                # Set offline dictionary title
                lst.append(f'<dic>{dic.title}</dic>{result}')
                mes = _('"{}" has matches for "{}"').format(dic.title, search)
                Message(f, mes).show_debug()
        return '\n'.join(lst)
    
    def get_all(self, search):
        f = '[MClient] sources.stardict.get.AllDics.get_all'
        if not self.Success:
            rep.cancel(f)
            return
        if not search:
            rep.empty(f)
            return
        #TODO: .lower() when index is lowercased
        bytes_ = bytes(search, 'utf-8')
        dics = [dic for dic in self.dics if not dic.Block]
        lst = []
        for dic in dics:
            results = dic.find_all(bytes_)
            if not results:
                mes = _('No matches for "{}"!').format(dic.title)
                Message(f, mes).show_info()
                continue
            lst += results
            mes = _('"{}" has matches for "{}"').format(dic.title, search)
            Message(f, mes).show_debug()
        return lst
    
    def walk(self):
        ''' Explore all subdirectories of path searching for filenames that
            have all three .ifo, .idx and .dict[.dz] suffixes.
        '''
        f = '[MClient] sources.stardict.get.AllDics.walk'
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
        f = '[MClient] sources.stardict.get.AllDics.locate'
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
        f = '[MClient] sources.stardict.get.AllDics.load'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.locate():
            rep.lazy(f)
            return
        timer = Timer(f)
        timer.start()
        for idic in self.dics:
            idic.load()
        timer.end()
        total_no = len(self.dics)
        self.dics = [dic for dic in self.dics if dic.Success]
        mes = _('Dictionaries loaded: {}/{}').format(len(self.dics), total_no)
        Message(f, mes).show_info()



class Index:
    
    def __init__(self, file):
        self.file = file
        self.Success = File(self.file).Success
    
    def load(self):
        f = '[MClient] sources.stardict.get.Index.load'
        if not self.Success:
            rep.cancel(f)
            return
        try:
            self.idx = open(self.file, 'rb')
        except Exception as e:
            self.Success = False
            mes = _('Failed to load "{}"!\n\nDetails: {}').format(self.path, e)
            Message(f, mes, True).show_warning()
    
    def _get_phrase(self):
        phrase = []
        while True:
            char = self.idx.read(1)
            if char in (b'', b'\x00'):
                phrase = b''.join(phrase)
                return phrase.decode(errors='ignore')
            phrase.append(char)
    
    def parse(self):
        f = '[MClient] sources.stardict.get.Index.parse'
        if not self.Success:
            rep.cancel(f)
            return
        mes = _('Load "{}"').format(self.file)
        Message(f, mes).show_info()
        timer = Timer(f)
        timer.start()
        INDEX[self.file] = {}
        while True:
            phrase = self._get_phrase()
            if not phrase:
                timer.end()
                return
            poses = self.idx.read(8)
            if not poses:
                timer.end()
                return
            if not phrase in INDEX[self.file]:
                INDEX[self.file][phrase] = []
            INDEX[self.file][phrase].append(poses)
    
    def run(self):
        self.load()
        self.parse()



class Indexes:
    
    def __init__(self):
        self.Success = True
    
    def get_poses(self, chunk):
        f = '[MClient] sources.stardict.get.Indexes.get_poses'
        if not self.Success:
            rep.cancel(f)
            return
        try:
            pos, len_ = struct.unpack('>LL', chunk)
            return(pos, len_)
        except Exception as e:
            self.Success = False
            rep.third_party(f, e)
    
    def debug(self):
        f = '[MClient] sources.stardict.get.Index.debug'
        if not self.Success:
            rep.cancel(f)
            return
        timer = Timer(f)
        timer.start()
        for file in INDEX:
            phrases = INDEX[file].keys()
            phrases = sorted(phrases)[:100]
            for phrase in phrases:
                for poses in INDEX[file][phrase]:
                    if not poses:
                        continue
                    pos, len_ = self.get_poses(poses)
                    print(f'Phrase: "{phrase}", pos: {pos}, len: {len_}')
        timer.end()


#ALL_DICS = AllDics()