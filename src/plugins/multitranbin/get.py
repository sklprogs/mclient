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


class Binary:
    
    def __init__(self,file):
        self.file    = file
        self.Success = sh.File(self.file).Success
        self.open()
    
    def check_lengths(self,pattern,lengths):
        f = '[MClient] plugins.multitranbin.get.Binary.check_lengths'
        if self.Success:
            if lengths:
                if lengths[0] == len(pattern) and lengths[1] > 0:
                    return True
                else:
                    mes = _('The check has failed!')
                    sh.objs.mes(f,mes,True).debug()
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def get_part2(self,pattern,start=0):
        f = '[MClient] plugins.multitranbin.get.Binary.get_part2'
        if self.Success:
            pos11 = self.find(pattern,start)
            if pos11 is None:
                sub = com.get_string(pattern)
                mes = _('Pattern: "{}": no matches starting from {}!')
                mes = mes.format(sub,start)
                sh.objs.mes(f,mes,True).info()
            else:
                lengths = self.get_lengths(pos11)
                if self.check_lengths(pattern,lengths):
                    pos21 = pos11 + lengths[0]
                    pos22 = pos21 + lengths[1]
                    return self.read(pos21,pos22)
                else:
                    return self.get_part2(pattern,pos11+1)
        else:
            sh.com.cancel(f)
    
    def get_lengths(self,index_):
        f = '[MClient] plugins.multitranbin.get.Binary.get_lengths'
        if self.Success:
            ''' There are 'M' pages at the beginning, so an index of
                the 1st part will always be positive.
            '''
            if index_ is None:
                sh.com.empty(f)
            elif index_ > 2:
                pos1 = index_ - 2
                pos2 = index_ - 1
                len1 = self.read(pos1,pos1+1)
                len2 = self.read(pos2,pos2+1)
                if len1 and len2:
                    len1 = struct.unpack('<b',len1)[0]
                    len2 = struct.unpack('<b',len2)[0]
                    mes = _('Part #{} length: {}').format(1,len1)
                    sh.objs.mes(f,mes,True).debug()
                    mes = _('Part #{} length: {}').format(2,len2)
                    sh.objs.mes(f,mes,True).debug()
                    return(len1,len2)
                else:
                    sh.com.empty(f)
            else:
                sub = '{} > 2'.format(index_)
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                sh.objs.mes(f,mes,True).warning()
        else:
            sh.com.cancel(f)
    
    def read(self,start,end):
        f = '[MClient] plugins.multitranbin.get.Binary.read'
        if self.Success:
            if start is None or end is None:
                sh.com.empty(f)
            elif 0 <= start < end:
                self.imap.seek(start)
                chunk = self.imap.read(end-start)
                mes = '"{}"'.format(com.get_string(chunk))
                sh.objs.mes(f,mes,True).debug()
                return chunk
            else:
                self.Success = False
                sub = '0 <= {} < {}'.format(start,end)
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



class Tests:
    
    def translate_stem(self):
        f = '[MClient] plugins.multitranbin.get.Tests.translate_stem'
        chnos = objs.stems().search(b'abasin')
        objs._stems.close()
        #290202, 290203
        glued = []
        for chno in chnos:
            chunk = objs.glue().search(chno)
            if chunk:
                glued += chunk
        objs._glue.close()
        sh.objs.mes(f,glued,True).debug()
        articles = []
        for chno in glued:
            articles.append(objs.articles().search(chno))
        objs._articles.close()
        articles = [article for article in articles if article]
        sh.objs.mes(f,articles,True).debug()
    
    def get_part2(self):
        # stem.eng
        file = STEM1
        ''' 13 ['aberrationist']
            8 b'\x01\x83\x8e\x02\x03\x00C\x00' -> [167,555; 3; 67]
        '''
        pattern = 'aberrationist'
        pattern = bytes(pattern,ENCODING)
        ibin = Binary(file)
        ibin.get_part2(pattern)
        ibin.close()
        # dict.erd
        file = DICTD1
        ''' 3 b'\x83\x8e\x02' -> [167,555]
            5 b'k\x00\\\x0b\x00' -> [107; 2,908]
        '''
        pattern = b'\x83\x8e\x02' # 167,555
        ibin = Binary(file)
        ibin.get_part2(pattern)
        ibin.close()
        # dict.ert
        file = DICTT
        ''' 3 b'\\\x0b\x00' [2908]
            55 b'\xfcbir\x85\x8b\x80\x99\x94\xa0\xa5\xa6\xb6\xbdQL@LUOXc\x9fv\xab~|\x8c\x93\x8e\x93\xa6\xa5\xa1\xae\xc0\xb8\xc5\xda\xd1\x0b\xe0\xe5\xdf\xe8\xed\xf4\x02\x03\x06\x13<div'
        '''
        pattern = b'\\\x0b\x00'
        ibin = Binary(file)
        xorred = ibin.get_part2(pattern)
        ibin.close()
        Xor (data   = xorred
            ,offset = -251
            ).dexor()
    
    def translate_many(self):
        # 'absolute measurements' = 'абсолютный способ измерения'
        '''
        # Successfully processed patterns
        patterns = ['abasin'
                   ,'absolute measurements'
                   ,'baby fish'
                   ,'sack duty'
                   ,'habitable room'
                   ,'a posteriori'
                   ,'abatement of tax'
                   ,'abatement of purchase price'
                   ,'habitable room'
                   ,'absolute distribution'
                   ,'abolishment of a scheme'
                   ,'calcium gallium germanium garnet'
                   ,'daily reports notice'
                   ]
        # Failed patterns
        # No combos:      ['he has not a sou'
                          ,'World Union of Catholic Teachers'
                          ,'Kapteyn transformation'
                          ]
        # Stack overflow: ['Bachelor of Vocational Education'
                          ,'ashlar line'
                          ,'acceleration measured in G'
                          ,'acceleration spectral density'
                          ,'A & E'
                          ,'Abelian equation'
                          ]
        '''
        patterns = ['he has not a sou'
                   ,'Bachelor of Vocational Education'
                   ,'ashlar line'
                   ,'acceleration measured in G'
                   ]
        for pattern in patterns:
            self.translate(pattern)
            input(_('Press any key'))
    
    def translate(self,pattern):
        f = '[MClient] plugins.multitranbin.get.Tests.translate'
        timer = sh.Timer(f)
        timer.start()
        iget = Get(pattern)
        sh.objs.mes(f,iget.run(),True).debug()
        timer.end()



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



class Articles(Binary):
    # Parse files like 'dict.ert'
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    
    def parse(self,chunk):
        f = '[MClient] plugins.multitranbin.get.Articles.parse'
        if self.Success:
            if chunk:
                return Xor (data   = chunk
                           ,offset = -251
                           ).dexor()
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def search(self,coded):
        # Do not fail the whole class on a failed search
        f = '[MClient] plugins.multitranbin.get.Articles.search'
        if self.Success:
            if coded:
                chunk = self.get_part2(coded)
                return self.parse(chunk)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)



class Glue(Binary):
    # Parse files like 'dict.erd'
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    
    def search(self,coded):
        # Do not fail the whole class on a failed search
        f = '[MClient] plugins.multitranbin.get.Glue.search'
        if self.Success:
            if coded:
                chunk = self.get_part2(coded)
                if chunk:
                    return self.parse(chunk)
                else:
                    ''' 'dict.erd' sometimes does not comprise
                        stem numbers provided by 'stem.eng' (at least
                        in the demo version).
                    '''
                    sh.com.lazy(f)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def parse(self,chunk):
        f = '[MClient] plugins.multitranbin.get.Glue.parse'
        if self.Success:
            if chunk:
                if (len(chunk) - 2) % 3 == 0 and len(chunk) != 2:
                    chunk = chunk[2:]
                    nos   = []
                    chnos = com.get_chunks(chunk,3)
                    for chno in chnos:
                        nos.append(com.unpack(chno))
                    sh.objs.mes(f,chnos,True).debug()
                    sh.objs.mes(f,nos,True).debug()
                    return chnos
                else:
                    mes = _('Wrong input data: "{}"!')
                    mes = mes.format(com.get_string(chunk))
                    sh.objs.mes(f,mes).warning()
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)



class Commands:
    
    def unpack(self,chno):
        f = '[MClient] plugins.multitranbin.get.Commands.unpack'
        if chno:
            chno += b'\x00'
            try:
                return struct.unpack('<L',chno)[0]
            except Exception as e:
                mes = _('Third-party module has failed!\n\nDetails: {}')
                mes = mes.format(e)
                sh.objs.mes(f,mes,True).warning()
        else:
            sh.com.empty(f)
    
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
            self._articles = Articles(DICTT)
        return self._articles
    
    def glue(self):
        if self._glue is None:
            self._glue = Glue(DICTD1)
        return self._glue
    
    def stems(self):
        if self._stems is None:
            self._stems = Stems(STEM1)
        return self._stems



class Stems(Binary):
    # Parse files like 'stem.eng'
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    
    def parse(self,chunk):
        ''' According to "libmtquery-0.0.1alpha3/doc/README.rus":
            the 1st byte - a type designating the use of capital letters
            (not used), further - a vector of 7-byte codes, each code
            including:
            3 bytes - a word number (4-byte long type compressed to
            3 bytes)
            2 bytes - sik (terminations)
            2 bytes - lgk (speech part codes)
        '''
        f = '[MClient] plugins.multitranbin.get.Stems.parse'
        if self.Success:
            if chunk:
                nos   = []
                chnos = []
                #NOTE: 0 % 7 == 0
                if len(chunk) > 1 and (len(chunk) - 1) % 7 == 0:
                    chunks = com.get_chunks(chunk[1:],7)
                    for i in range(len(chunks)):
                        chnos.append(chunks[i][0:3])
                    for chno in chnos:
                        nos.append(com.unpack(chno))
                    sh.objs.mes(f,chnos,True).debug()
                    sh.objs.mes(f,nos,True).debug()
                    return chnos
                else:
                    sub = com.get_string(chunk)
                    mes = _('Wrong input data: "{}"!').format(sub)
                    sh.objs.mes(f,mes,True).warning()
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def search(self,coded):
        # Do not fail the whole class on a failed search
        f = '[MClient] plugins.multitranbin.get.Stems.search'
        if self.Success:
            if coded:
                chunk = self.get_part2(coded)
                return self.parse(chunk)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)



class Get:
    
    def __init__(self,pattern):
        self.values()
        self.pattern = pattern
    
    def combos(self):
        f = '[MClient] plugins.multitranbin.get.Get.combos'
        if self.Success:
            sh.objs.mes(f,self.stemnos,True).debug()
            self.stemnos = list(itertools.product(*self.stemnos))
            sh.objs.mes(f,self.stemnos,True).debug()
            self.stemnos = [b''.join(item) for item in self.stemnos]
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
                all_stems = []
                i = len(word)
                while i > 0:
                    stem = word[0:i]
                    mes = _('Try for "{}"').format(stem)
                    sh.objs.mes(f,mes,True).debug()
                    coded = bytes(stem,ENCODING,'ignore')
                    stem_nos = objs.stems().search(coded)
                    if stem_nos:
                        mes = _('Found stem: "{}"').format(stem)
                        sh.objs.mes(f,mes,True).debug()
                        all_stems += stem_nos
                        ''' Stems forms can be both 'absolute' and
                            'absolut', so we do not break here.
                        '''
                    i -= 1
                self.stemnos.append(all_stems)
            self.stemnos = [item for item in self.stemnos if item]
            sh.objs.mes(f,self.stemnos,True).debug()
        else:
            sh.com.cancel(f)
    
    def values(self):
        self.Success = True
        self.pattern = ''
        self._html   = ''
        self.stems   = []
        self.stemnos = []
    
    def search(self):
        f = '[MClient] plugins.multitranbin.get.Get.search'
        if self.Success:
            art_nos = []
            for combo in self.stemnos:
                art_no = objs.glue().search(combo)
                if art_no:
                    art_nos += art_no
            if art_nos:
                mes = _('Found combinations: {}').format(art_nos)
            else:
                mes = _('No stem combinations have been found!')
            sh.objs.mes(f,mes,True).info()
            articles = []
            for art_no in art_nos:
                articles.append(objs.articles().search(art_no))
            articles = [article for article in articles if article]
            return articles
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.check()
        self.strip()
        self.get_stems()
        self.combos()
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
    #Tests().translate_many()
    Tests().translate('above all')
