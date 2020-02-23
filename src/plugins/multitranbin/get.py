#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import mmap
import struct
import codecs
import itertools
import skl_shared.shared as sh
from skl_shared.localize import _

ENCODING = 'windows-1251'
LANG1    = _('Russian')
LANG2    = _('English')
PATH     = ''
#TODO: elaborate
STEM1    = '/home/pete/.wine/drive_c/mt_demo/mt/network/english/stem.eng'
DICTD1   = '/home/pete/.wine/drive_c/mt_demo/mt/network/eng_rus/dict.erd'
DICTT    = '/home/pete/.wine/drive_c/mt_demo/mt/network/eng_rus/dict.ert'


class Suggest:
    
    def __init__(self,search):
        self.values()
        if search:
            self.reset(search)
    
    def values(self):
        self.Success = True
        self._search = ''
    
    def reset(self,search):
        f = '[MClient] plugins.multitranbin.get.Suggest.reset'
        self._search = search
        if not self._search:
            self.Success = False
            sh.com.empty(f)
    
    def get(self):
        f = '[MClient] plugins.multitranbin.get.Suggest.get'
        if self.Success:
            pass
        else:
            sh.com.cancel(f)
    
    def run(self):
        return self.get()



class AllDics:
    
    def __init__(self):
        self.values()
        self.reset()
    
    def langs(self):
        # Return all available languages
        f = '[MClient] plugins.multitranbin.get.AllDics.langs'
        if self.Success:
            pass
        else:
            sh.com.cancel(f)
    
    def get(self,search):
        f = '[MClient] plugins.multitranbin.get.AllDics.get'
        if self.Success:
            if search:
                pass
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def values(self):
        self._dics   = []
        self._path   = ''
        # Do not run anything if 'self.reset' was not run
        self.Success = False
    
    def reset(self):
        self.values()
        self._path   = PATH
        self.Success = sh.Directory(self._path).Success
    
    def walk(self):
        f = '[MClient] plugins.multitranbin.get.AllDics.walk'
        if self.Success:
            pass
        else:
            sh.com.cancel(f)
    
    def locate(self):
        f = '[MClient] plugins.multitranbin.get.AllDics.locate'
        if self.Success:
            if not self._dics:
                if self.walk():
                    #TODO: implement
                    self._dics = []
                else:
                    sh.com.lazy(f)
            mes = _('{} offline dictionaries are available')
            mes = mes.format(len(self._dics))
            sh.objs.mes(f,mes,True).info()
            return self._dics
        else:
            sh.com.cancel(f)
    
    def load(self):
        f = '[MClient] plugins.multitranbin.get.AllDics.load'
        if self.Success:
            pass
        else:
            sh.com.cancel(f)



class Xor:
    
    def __init__(self,data,offset=0,step=6):
        self.data   = data
        self.offset = offset
        self.step   = step
    
    def dexor(self):
        f = '[MClient] plugins.multitranbin.get.Xor.dexor'
        if self.data:
            poses = []
            pos11 = 0
            pos12 = 0
            pos21 = 0
            coef  = 0
            for i in range(len(self.data)):
                pos21 = self.data[i]
                pos   = self.data[i] + self.offset - i * self.step \
                                      + coef
                if not 0 <= pos <= 255:
                    pos = abs(pos)
                    overhead = pos - (pos // 255) * 255 - 1
                    pos = 255 - overhead
                    delta = pos11 - pos12 - pos21 + pos
                    ''' This is a hack to comply with Multitran's
                        internal logic.
                    '''
                    if delta == 249:
                        pos  += 1
                        coef += 1
                    elif delta == -261:
                        pos  -= 1
                        coef -= 1
                    #mes = _('Overflow: {} -> {}').format(pos21,pos)
                    #sh.objs.mes(f,mes,True).debug()
                mes = '{} -> {}'.format(self.data[i],pos)
                sh.objs.mes(f,mes,True).debug()
                poses.append(pos)
                pos11 = self.data[i]
                pos12 = pos
            ''' If the algorithm is correct, this should not be needed.
                I keep this code, however, because a ValueError will
                be raised otherwise.
            '''
            for i in range(len(poses)):
                if not 0 <= poses[i] <= 255:
                    mes = _('Invalid value "{}" at position {}!')
                    mes = mes.format(poses[i],i)
                    sh.objs.mes(f,mes,True).error()
                    poses[i] = 0
            result = bytes(poses)
            mes = com.get_string(result)
            sh.objs.mes(f,mes,True).debug()
            return result
        else:
            sh.com.empty(f)
    
    def xor(self):
        f = '[MClient] plugins.multitranbin.get.Xor.xor'
        if data:
            poses = []
            pos11 = 0
            pos12 = 0
            pos21 = 0
            coef  = 0
            for i in range(len(self.data)):
                pos21 = self.data[i]
                pos   = self.data[i] + self.offset + i * self.step \
                                      + coef
                if not 0 <= pos <= 255:
                    pos = abs(pos)
                    pos = pos - (pos // 255) * 255 - 1
                    delta = pos11 - pos12 - pos21 + pos
                    ''' This is a hack to comply with Multitran's
                        internal logic.
                    '''
                    if delta == -249:
                        pos  -= 1
                        coef -= 1
                    elif delta == 261:
                        pos  += 1
                        coef += 1
                    #mes = _('Overflow: {} -> {}').format(pos21,pos)
                    #sh.objs.mes(f,mes,True).debug()
                mes = '{} -> {}'.format(data[i],pos)
                sh.objs.mes(f,mes,True).debug()
                poses.append(pos)
                pos11 = data[i]
                pos12 = pos
            ''' If the algorithm is correct, this should not be needed.
                I keep this code, however, because a ValueError will
                be raised otherwise.
            '''
            for i in range(len(poses)):
                if not 0 <= poses[i] <= 255:
                    mes = _('Invalid value "{}" at position {}!')
                    mes = mes.format(poses[i],i)
                    sh.objs.mes(f,mes,True).error()
                    poses[i] = 0
            result = bytes(poses)
            mes = com.get_string(result)
            sh.objs.mes(f,mes,True).debug()
            return result
        else:
            sh.com.empty(f)



class Articles:
    # Parse files like 'dict.ert'
    def __init__(self):
        self.values()
        self.load()
    
    def check_pos(self,pos):
        f = '[MClient] plugins.multitranbin.get.Articles.check_pos'
        if self.Success:
            if pos:
                read = self.bin.read(pos-2,pos-1)
                if read:
                    mes = com.get_string(read)
                    sh.objs.mes(f,mes,True).debug()
                    value = struct.unpack('<b',read)[0]
                    if value == 3:
                        read = self.bin.read(pos-1,pos)
                        if read:
                            mes = com.get_string(read)
                            sh.objs.mes(f,mes,True).debug()
                            return struct.unpack('<b',read)[0]
                        else:
                            sh.com.empty(f)
                else:
                    sh.com.empty(f)
            else:
                sh.com.empty(f)
            mes = _('The check has failed')
            sh.objs.mes(f,mes,True).debug()
        else:
            sh.com.cancel(f)
    
    def get_article_pos(self,no):
        f = '[MClient] plugins.multitranbin.get.Articles.get_article_pos'
        if self.Success:
            packed = self.pack(no)
            start  = 0
            while True:
                sub = com.get_string(packed)
                mes = _('Search for article #{} ({})').format(no,sub)
                sh.objs.mes(f,mes,True).debug()
                pos  = self.bin.find(packed,start)
                pos2 = None
                if pos is None:
                    mes = _('No matches!')
                    sh.objs.mes(f,mes,True).info()
                    break
                else:
                    length = self.check_pos(pos)
                    if length:
                        pos1 = pos + len(packed)
                        pos2 = pos1 + length
                        mes = '{}:{}'.format(pos1,pos2)
                        sh.objs.mes(f,mes,True).debug()
                        return(pos1,pos2)
                    else:
                        start = pos + 1
    
    def pack(self,no):
        f = '[MClient] plugins.multitranbin.get.Articles.pack'
        if self.Success:
            if no:
                packed = b''
                try:
                    packed = struct.pack('<L',no)
                    packed = packed[0:3]
                except Exception as e:
                    mes = _('Third-party module has failed!\n\nDetails: {}')
                    mes = mes.format(e)
                    sh.objs.mes(f,mes,True).warning()
                return packed
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def get_article(self,no):
        f = '[MClient] plugins.multitranbin.get.Articles.get_article'
        if self.Success:
            if no:
                poses = self.get_article_pos(no)
                if poses:
                    read = self.bin.read(poses[0],poses[1])
                    if read:
                        mes = com.get_string(read)
                        sh.objs.mes(f,mes,True).debug()
                        dexorred = Xor (data   = read
                                       ,offset = -251
                                       ).dexor()
                        return dexorred
                else:
                    sh.com.empty(f)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def get_articles(self,nos):
        f = '[MClient] plugins.multitranbin.get.Articles.get_articles'
        if self.Success:
            if nos:
                chunks = []
                for no in nos:
                    chunks.append(self.get_article(no))
                return chunks
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def values(self):
        self.Success = True
        self.blocks  = []
    
    def close(self):
        f = '[MClient] plugins.multitranbin.get.Articles.close'
        if self.Success:
            self.bin.close()
        else:
            sh.com.cancel(f)
    
    def load(self):
        f = '[MClient] plugins.multitranbin.get.Articles.load'
        if self.Success:
            self.bin = Binary(DICTT)
            self.bin.open()
            self.Success = self.bin.Success
        else:
            sh.com.cancel(f)



class Glue:
    # Parse files like 'dict.erd'
    def __init__(self):
        self.values()
        self.load()
    
    def get_pos(self,chunk):
        f = '[MClient] plugins.multitranbin.get.Glue.get_pos'
        if self.Success:
            pos = self.bin.find(chunk)
            sub = com.get_string(chunk)
            if pos:
                mes = _('Chunk "{}": position {}').format(sub,pos)
                sh.objs.mes(f,mes,True).info()
                return pos
            else:
                mes = _('Chunk "{}": no matches').format(sub)
                sh.objs.mes(f,mes,True).debug()
        else:
            sh.com.cancel(f)
    
    def pack(self,stem_no):
        f = '[MClient] plugins.multitranbin.get.Glue.pack'
        if self.Success:
            if stem_no or stem_no == 0:
                packed = b''
                try:
                    packed = struct.pack('<L',stem_no)
                    packed = packed[0:3]
                except Exception as e:
                    mes = _('Third-party module has failed!\n\nDetails: {}')
                    mes = mes.format(e)
                    sh.objs.mes(f,mes,True).warning()
                return packed
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def check_pos(self,pos):
        f = '[MClient] plugins.multitranbin.get.Glue.check_pos'
        if self.Success:
            if pos:
                read = self.bin.read(pos-2,pos-1)
                if read:
                    mes = com.get_string(read)
                    sh.objs.mes(f,mes,True).debug()
                    value = struct.unpack('<b',read)[0]
                    if value % 3 == 0:
                        read = self.bin.read(pos-1,pos)
                        if read:
                            mes = com.get_string(read)
                            sh.objs.mes(f,mes,True).debug()
                            value = struct.unpack('<b',read)[0]
                            if (value - 2) % 3 == 0 and value != 2:
                                return value
                        else:
                            sh.com.empty(f)
                else:
                    sh.com.empty(f)
            else:
                sh.com.empty(f)
            mes = _('The check has failed')
            sh.objs.mes(f,mes,True).debug()
        else:
            sh.com.cancel(f)
    
    def get_article_nos(self,chunk):
        f = '[MClient] plugins.multitranbin.get.Glue.get_article_nos'
        if self.Success:
            if chunk:
                pos = self.get_pos(chunk)
                if pos:
                    delta = self.check_pos(pos)
                    if delta:
                        pos1 = pos + len(chunk)
                        pos2 = pos1 + delta
                        read = self.bin.read(pos1,pos2)
                        if read:
                            mes = com.get_string(read)
                            sh.objs.mes(f,mes,True).debug()
                            if (len(read) - 2) % 3 == 0 \
                            and len(read) != 2:
                                read = read[2:]
                                chunks = com.get_chunks(read,3)
                                nos = []
                                for chunk in chunks:
                                    chunk += b'\x00'
                                    try:
                                        nos.append(struct.unpack('<L',chunk)[0])
                                    except Exception as e:
                                        mes = _('Third-party module has failed!\n\nDetails: {}')
                                        mes = mes.format(e)
                                        sh.objs.mes(f,mes,True).warning()
                                sh.objs.mes(f,nos,True).debug()
                                return nos
                            else:
                                mes = _('Wrong input data: "{}"!')
                                mes = mes.format(com.get_string(read))
                                sh.objs.mes(f,mes).warning()
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def values(self):
        self.Success = True
        self.stems   = []
        self.arts    = []
    
    def close(self):
        f = '[MClient] plugins.multitranbin.get.Glue.close'
        if self.Success:
            self.bin.close()
        else:
            sh.com.cancel(f)
    
    def load(self):
        f = '[MClient] plugins.multitranbin.get.Glue.load'
        if self.Success:
            self.bin = Binary(DICTD1)
            self.bin.open()
            self.Success = self.bin.Success
        else:
            sh.com.cancel(f)



class Commands:
    
    def accessible(self):
        return len(objs.all_dics()._dics)
    
    def get_string(self,chunk):
        ''' Only raw strings should be used in GUI (otherwise,
            for example, '\x00' will be treated like b'\x00').
        '''
        f = '[MClient] plugins.multitranbin.get.Commands.get_string'
        result = ''
        if chunk:
            try:
                chunk  = chunk.decode('latin1')
                result = codecs.encode(chunk,'unicode_escape')
                result = str(result)
                result = result.replace('\\\\','\\')
                result = result[2:-1]
            except Exception as e:
                sh.objs.mes(f,str(e)).warning()
                result = str(chunk)
        else:
            sh.com.empty(f)
        return result
    
    def get_chunks(self,iterable,limit=3):
        ''' - Divide an iterable in a consecutive order.
            - Output chunks may have different lengths.
        '''
        f = '[MClient] plugins.multitranbin.get.Commands.get_chunks'
        if iterable:
            return [iterable[i:i+limit] \
                    for i in range(0,len(iterable),limit)
                   ]
        else:
            sh.com.empty(f)
            return []
    
    # Orphan
    def get_subseq(self,iterable,length):
        ''' - Unlike 'self.get_chunks', this provides for combinations
              of chunks at different positions instead of slicing
              an iterable.
            - All chunk will have the same length.
        '''
        return [iterable[i: i + length] \
                for i in range(len(iterable) - length + 1)
               ]



class Objects:
    
    def __init__(self):
        self._stems = self._glue = self._articles = self._all_dics \
                    = None
    
    def all_dics(self):
        if self._all_dics is None:
            self._all_dics = AllDics()
        return self._all_dics
    
    def articles(self):
        if self._articles is None:
            self._articles = Articles()
        return self._articles
    
    def glue(self):
        if self._glue is None:
            self._glue = Glue()
        return self._glue
    
    def stems(self):
        if self._stems is None:
            self._stems = Stems()
        return self._stems


class Binary:
    
    def __init__(self,file):
        self.file    = file
        self.Success = sh.File(self.file).Success
    
    def read(self,start,end):
        f = '[MClient] plugins.multitranbin.get.Binary.read'
        if self.Success:
            if end > start:
                self.imap.seek(start)
                return self.imap.read(end-start)
            else:
                self.Success = False
                sub = '{} < {}'.format(start,end)
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                sh.objs.mes(f,mes).warning()
        else:
            sh.com.cancel(f)
    
    def find(self,pattern,start=0):
        f = '[MClient] plugins.multitranbin.get.Binary.find'
        if self.Success:
            if pattern:
                self.imap.seek(start)
                result = self.imap.find(pattern)
                if result >= 0:
                    return result
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def open(self):
        f = '[MClient] plugins.multitranbin.get.Binary.open'
        if self.Success:
            mes = _('Open "{}"').format(self.file)
            sh.objs.mes(f,mes,True).info()
            self.bin = open(self.file,'rb')
            # 'mmap' fails upon opening an empty file!
            try:
                self.imap = mmap.mmap (self.bin.fileno(),0
                                      ,prot=mmap.PROT_READ
                                      )
            except Exception as e:
                self.Success = False
                mes = _('Third-party module has failed!\n\nDetails: {}')
                mes = mes.format(e)
                sh.objs.mes(f,mes,True).warning()
        else:
            sh.com.cancel(f)
    
    def close(self):
        f = '[MClient] plugins.multitranbin.get.Binary.close'
        if self.Success:
            mes = _('Close "{}"').format(self.file)
            sh.objs.mes(f,mes,True).info()
            self.imap.flush()
            self.bin.close()
        else:
            sh.com.cancel(f)



class Stems:
    
    def __init__(self):
        self.values()
        self.load()
    
    def stem_nos(self,chunk):
        ''' According to "libmtquery-0.0.1alpha3/doc/README.rus":
            the 1st byte - a type designating the use of capital letters
            (not used), further - a vector of 7-byte codes, each code
            including:
            3 bytes - a word number (4-byte long type compressed to
            3 bytes)
            2 bytes - sik (terminations)
            2 bytes - lgk (speech part codes)
        '''
        f = '[MClient] plugins.multitranbin.get.Stems.stem_nos'
        if self.Success:
            if chunk:
                nos = []
                #NOTE: 0 % 7 == 0
                if len(chunk) > 1 and (len(chunk) - 1) % 7 == 0:
                    chunks = com.get_chunks(chunk[1:],7)
                    #mes = com.get_string(chunk)
                    #sh.objs.mes(f,mes,True).debug()
                    for i in range(len(chunks)):
                        no = chunks[i][0:3] + b'\x00'
                        try:
                            nos.append(struct.unpack('<L',no)[0])
                        except Exception as e:
                            mes = _('Third-party module has failed!\n\nDetails: {}')
                            mes = mes.format(e)
                            sh.objs.mes(f,mes,True).warning()
                    sh.objs.mes(f,nos,True).debug()
                    return nos
                else:
                    sub = com.get_string(chunk)
                    mes = _('Wrong input data: "{}"!').format(sub)
                    sh.objs.mes(f,mes,True).warning()
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def close(self):
        f = '[MClient] plugins.multitranbin.get.Stems.close'
        if self.Success:
            self.bin.close()
        else:
            sh.com.cancel(f)
    
    def load(self):
        f = '[MClient] plugins.multitranbin.get.Stems.load'
        if self.Success:
            self.bin = Binary(STEM1)
            self.bin.open()
            self.Success = self.bin.Success
        else:
            sh.com.cancel(f)
    
    def indexes(self):
        f = '[MClient] plugins.multitranbin.get.Stems.indexes'
        if self.Success:
            ind = self.bin.find(self.coded)
            if ind is None:
                mes = _('No matches!')
                sh.objs.mes(f,mes,True).info()
            else:
                if ind > 1:
                    sizes = self.bin.read(ind-2,ind)
                    indexes = ()
                    try:
                        indexes = struct.unpack('<2b',sizes)
                    except Exception as e:
                        mes = _('Third-party module has failed!\n\nDetails: {}')
                        mes = mes.format(e)
                        sh.objs.mes(f,mes).warning()
                    if indexes:
                        pos1 = ind + indexes[0]
                        pos2 = pos1 + indexes[1]
                        mes = '{} -> {}; {} -> {}'.format (indexes[0]
                                                          ,pos1
                                                          ,indexes[1]
                                                          ,pos2
                                                          )
                        sh.objs.mes(f,mes,True).debug()
                        return(pos1,pos2)
                    else:
                        sh.com.empty(f)
                else:
                    mes = _('Wrong input data: "{}"!').format(ind)
                    sh.objs.mes(f,mes).warning()
        else:
            sh.com.cancel(f)
    
    def chunk2(self,poses):
        f = '[MClient] plugins.multitranbin.get.Stems.chunk2'
        if self.Success:
            if poses:
                return self.bin.read(poses[0],poses[1])
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def search(self,coded):
        # Do not fail the whole class on a failed search
        f = '[MClient] plugins.multitranbin.get.Stems.search'
        if self.Success:
            if coded:
                self.coded = coded
                indexes = self.indexes()
                ''' Empty output is a common situation and should not
                    be warned. 'self.indexes' already outputs a message
                    about that.
                '''
                if indexes:
                    chunk = self.chunk2(indexes)
                    return self.stem_nos(chunk)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def values(self):
        self.Success = True
        self.coded   = b''
        self.chunk   = b''



class Get:
    
    def __init__(self,pattern):
        self.values()
        self.pattern = pattern
    
    def combos(self):
        f = '[MClient] plugins.multitranbin.get.Get.combos'
        if self.Success:
            self.stemnos = list(itertools.product(*self.stemnos))
            sh.objs.mes(f,self.stemnos,True).debug()
        else:
            sh.com.cancel(f)
    
    def check(self):
        f = '[MClient] plugins.multitranbin.get.Get.check'
        if not self.pattern:
            self.Success = False
            sh.com.empty(f)
    
    def strip(self):
        f = '[MClient] plugins.multitranbin.get.Get.strip'
        if self.Success:
            self.pattern = self.pattern.strip()
            self.pattern = sh.Text(self.pattern).convert_line_breaks()
            self.pattern = sh.Text(self.pattern).delete_line_breaks()
            self.pattern = sh.Text(self.pattern).delete_punctuation()
            self.pattern = sh.Text(self.pattern).delete_duplicate_spaces()
            self.pattern = self.pattern.lower()
        else:
            sh.com.cancel(f)
    
    def get_stems(self):
        f = '[MClient] plugins.multitranbin.get.Get.get_stems'
        if self.Success:
            words = self.pattern.split(' ')
            for word in words:
                i = len(word)
                while i >= 0:
                    stem = word[0:i]
                    mes = _('Try for "{}"').format(stem)
                    sh.objs.mes(f,mes,True).debug()
                    coded = bytes(stem,ENCODING,'ignore')
                    stem_nos = objs.stems().search(coded)
                    if stem_nos:
                        mes = _('Found stem: "{}"').format(stem)
                        sh.objs.mes(f,mes,True).debug()
                        self.stemnos.append(stem_nos)
                        break
                    i -= 1
            
        else:
            sh.com.cancel(f)
    
    def values(self):
        self.Success = True
        self.pattern = ''
        self._html   = ''
        self.stems   = []
        self.stemnos = []
        self.packed  = []
    
    def _pack(self,item):
        packed = b''
        for subitem in item:
            subitem = struct.pack('<L',subitem)
            subitem = subitem[:-1]
            packed += subitem
        return packed
    
    def pack(self):
        f = '[MClient] plugins.multitranbin.get.Get.pack'
        if self.Success:
            self.packed = [self._pack(item) for item in self.stemnos]
        else:
            sh.com.cancel(f)
    
    def search(self):
        f = '[MClient] plugins.multitranbin.get.Get.search'
        if self.Success:
            article_nos = []
            for chunk in self.packed:
                article_nos = objs.glue().get_article_nos(chunk)
                if article_nos:
                    break
            return objs.articles().get_articles(article_nos)
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.check()
        self.strip()
        self.get_stems()
        self.combos()
        self.pack()
        return self.search()


objs = Objects()
com  = Commands()


if __name__ == '__main__':
    f = '[MClient] plugins.multitranbin.get.__main__'
    ''' stem.eng, position 8,455:
        b'\x06\x0fabasin\x01\x9am\x04\x03\x80C\x00\x9bm\x04\x14\x80 \x00'
        b'\x06\x0f' -> (6;15)
        6 -> b'abasin'
        15 -> b'\x01\x9am\x04\x03\x80C\x00\x9bm\x04\x14\x80 \x00':
            b'\x9am\x04' -> 290,202
        dict.erd, find b'\x9am\x04 (290,202):
            b'\x9am\x04%\x00( \x00' ->
            3 [290,202] 5 [37; 8,232]
        290,203: not found
        dict.ert, find b'( \x00\' (8,232):
        181,793 3 b'( \x00' [8232] 17 b"\xfcbin\x86\x82\x8d'\x0b\x12\x17$+6^\x88\x92"
        \x01abasin\x02\xe0\xe1\xe0\xe7\xe8\xed\x0f37
        [b'\x01', 'abasin', b'\x02', 'абазин', b'\x0f', '37']
    '''
    timer = sh.Timer(f)
    timer.start()
    # 'abasin'
    # 'absolute measurements' = 'абсолютный способ измерения'
    # 'Bachelor of Vocational Education'
    # baby fish
    # sack duty
    # he has not a sou
    # habitable room
    # a posteriori
    # ashlar line
    # abatement of tax
    ''' absolute distribution
        [188481, 2604] 5 [41, 6400]
    '''
    iget = Get('abatement of tax')
    print(iget.run())
    objs.stems().close()
    objs.glue().close()
    objs.articles().close()
    timer.end()
