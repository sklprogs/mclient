#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import mmap
import struct
import codecs
import locale
import itertools
import skl_shared.shared as sh
from skl_shared.localize import _

# Do not localize language names here
CODING   = 'windows-1251'
LANG1    = 'English'
LANG2    = 'Russian'
PATH     = ''
MAXSTEMS = 2
DEBUG    = False


class Xor:
    
    def __init__(self):
        self.vectors = []
        self.set_vectors()
    
    def get_shift(self,pos1,pos2):
        f = '[MClient] plugins.multitranbin.get.Xor.get_shift'
        min_ = min(pos1,pos2) + 1
        max_ = max(pos1,pos2)
        shift = 0
        while min_ <= max_:
            vector = self.vectors[min_]
            mes = _('Position: {}; vector: {}').format(min_,vector)
            sh.objs.get_mes(f,mes,True).show_debug()
            if pos2 > pos1:
                shift -= vector
            else:
                shift += vector
            min_ += 1
        if DEBUG:
            sh.objs.get_mes(f,shift,True).show_debug()
        return shift
    
    def overflow(self,pos):
        f = '[MClient] plugins.multitranbin.get.Xor.overflow'
        if not 0 <= pos <= 255:
            old = pos = abs(pos)
            overhead = pos - (pos // 255) * 255 - 1
            pos = 255 - overhead
            if DEBUG:
                mes = _('Overflow: {} -> {}').format(old,pos)
                sh.objs.get_mes(f,mes,True).show_debug()
        return pos
    
    def xor(self,byte,pos,start):
        f = '[MClient] plugins.multitranbin.get.Xor.xor'
        if byte:
            if 0 <= byte[0] <= 255:
                shift = self.get_shift(pos1,pos2)
                #pos = 
                vector = self.vectors[byte[0]]
                pos = -vector + start + byte[0]
                pos = self.overflow(pos)
                byte2 = bytes([pos])
                if DEBUG:
                    mes = _('Original byte: "{}"; original position: {}; vector: {}; final byte: "{}"; final position: {}')
                    mes = mes.format (com.get_string(byte)
                                     ,byte[0],vector
                                     ,com.get_string(byte2)
                                     ,pos
                                     )
                    sh.objs.get_mes(f,mes,True).show_debug()
                return byte2
            else:
                sub = '0 <= {} <= 255'.format(byte[0])
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                sh.objs.get_mes(f,mes,True).show_warning()
        else:
            sh.com.rep_empty(f)
    
    def set_vectors(self):
        ''' MT's XOR algorithm is basically shifting positions by
            -2, -2, -2, +6, -2, -2, -2, +10... with a few exceptions.
        '''
        i = 0
        while i < 256:
            if (i + 1) % 4 == 0:
                if (i + 1) % 8 == 0:
                    self.vectors.append(-10)
                else:
                    self.vectors.append(6)
            else:
                self.vectors.append(-2)
            i += 1
        
        self.vectors[163] = 48
        self.vectors[164] = -44
        self.vectors[255] = 246



class Ending:
    # Parse files like 'sik.eng'
    def __init__(self,file):
        self.set_values()
        self.file = file
        self.load()
        self.parse()
    
    def overflow(self,no):
        f = '[MClient] plugins.multitranbin.get.Ending.overflow'
        new = no
        if self.Success:
            new = com.overflowh(new)
            if not new in self.ordered and len(self.ordered) > 1:
                i = 1
                while i < len(self.ordered):
                    if self.ordered[i-1] <= no < self.ordered[i]:
                        break
                    i += 1
                i -= 1
                new = self.ordered[i]
                if DEBUG:
                    mes = '{} -> {}'.format(no,new)
                    sh.objs.get_mes(f,mes,True).show_debug()
        else:
            sh.com.cancel(f)
        return new
    
    def has_match(self,no,pattern):
        f = '[MClient] plugins.multitranbin.get.Ending.has_match'
        if self.Success:
            no = self.overflow(no)
            #TODO: implement 'X' (full pattern match)
            if not pattern:
                # An empty ending
                pattern = '#'
            # MT (at least demo) can have negatives for some reason
            if no < 0:
                # Redirection to an empty class
                no = 0
            try:
                index_ = self.nos.index(no)
                match  = pattern in self.ends[index_]
                if match:
                    sub = _('Yes')
                else:
                    sub = _('No')
                if DEBUG:
                    mes = _('#: {}; Pattern: "{}"; Match: {}')
                    mes = mes.format(no,pattern,sub)
                    sh.objs.get_mes(f,mes,True).show_debug()
                return match
            except ValueError:
                mes = _('Wrong input data: "{}"!').format(no)
                sh.objs.get_mes(f,mes,True).show_warning()
        else:
            sh.com.cancel(f)
    
    def load(self):
        f = '[MClient] plugins.multitranbin.get.Ending.load'
        if self.Success:
            self.text = sh.ReadTextFile(self.file).get()
            if not self.text:
                self.Success = False
                mes = _('Empty output is not allowed!')
                sh.objs.get_mes(f,mes,True).show_warning()
        else:
            sh.com.cancel(f)
    
    def parse(self):
        f = '[MClient] plugins.multitranbin.get.Ending.parse'
        if self.Success:
            lines = self.text.splitlines()
            lines = [line for line in lines if line]
            if len(lines) > 1:
                if lines[0] == 'SIK PORTION':
                    lines = lines[1:]
                for i in range(len(lines)):
                    line = lines[i].strip()
                    line = sh.Text(line).delete_duplicate_spaces()
                    # Remove comments
                    line = line.split(';')[0]
                    # Empty input means the entire line is a comment
                    if line:
                        if len(line) < 2:
                            mes = _('Wrong input data: "{}"!')
                            mes = mes.format(line)
                            sh.objs.get_mes(f,mes,True).show_warning()
                        else:
                            # Remove a gender separator
                            line = line.replace('/',' ')
                            line = line.replace(',',' ')
                            line = line.split(' ')
                            line = [item for item in line if item]
                            no   = sh.Input(f,line[0]).get_integer()
                            ends = line[1:]
                            self.nos.append(no)
                            self.ends.append(ends)
                self.ordered = sorted(set(self.nos))
            else:
                sub = '{} > 1'.format(len(lines))
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                sh.objs.get_mes(f,mes,True).show_warning()
        else:
            sh.com.cancel(f)
    
    def set_values(self):
        self.file    = ''
        self.text    = ''
        self.Success = True
        self.nos     = []
        self.ends    = []
        self.ordered = []



class Subject:
    # Parse files like 'SUBJECTS.TXT'
    def __init__(self,file):
        self.set_values()
        self.file = file
        self.get_locale()
        self.load()
        self.parse()
    
    def get_pair(self,code):
        f = '[MClient] plugins.multitranbin.get.Subject.get_pair'
        if self.Success:
            if code in self.dic_nos:
                ind = self.dic_nos.index(code)
                if self.lang == 'ru':
                    pair = (self.ru_dic[ind],self.ru_dicf[ind])
                else:
                    pair = (self.en_dic[ind],self.en_dicf[ind])
                mes = '{} -> {}'.format(code,pair)
                sh.objs.get_mes(f,mes,True).show_debug()
                return pair
            else:
                mes = _('Wrong input data: "{}"!').format(code)
                sh.objs.get_mes(f,mes,True).show_warning()
        else:
            sh.com.cancel(f)
    
    def get_locale(self):
        f = '[MClient] plugins.multitranbin.get.Subject.get_locale'
        if self.Success:
            info = locale.getdefaultlocale()
            if info:
                # 'en' is set in 'set_values' by default
                if info[0] in ('ru_RU','ru_UA'):
                    self.lang = 'ru'
        else:
            sh.com.cancel(f)
    
    def set_values(self):
        self.Success = True
        self.file    = ''
        self.text    = ''
        self.dic_nos = []
        self.en_dicf = []
        self.ru_dicf = []
        self.en_dic  = []
        self.ru_dic  = []
        self.lang    = 'en'
    
    def parse(self):
        f = '[MClient] plugins.multitranbin.get.Subject.parse'
        if self.Success:
            lst = self.text.splitlines()
            # This should not be needed. We do that just to be safe.
            lst = [item for item in lst if item]
            for line in lst:
                items = line.split(';')
                # Delete comments (which also start with ';')
                items = items[0:5]
                # Fail if items < 5
                if len(items) == 5:
                    dic_no = sh.Input(f,items[0]).get_integer()
                    self.dic_nos.append(dic_no)
                    self.en_dicf.append(items[1])
                    self.en_dic.append(items[2])
                    self.ru_dicf.append(items[3])
                    self.ru_dic.append(items[4])
                else:
                    self.Success = False
                    mes = _('Wrong input data: "{}"!').format(line)
                    sh.objs.get_mes(f,mes).show_warning()
                    break
        else:
            sh.com.cancel(f)
    
    def load(self):
        f = '[MClient] plugins.multitranbin.get.Subject.load'
        if self.Success:
            # We need silent logging here
            if os.path.exists(self.file):
                self.text = sh.ReadTextFile(self.file).get()
                if not self.text:
                    self.Success = False
                    mes = _('Empty output is not allowed!')
                    sh.objs.get_mes(f,mes).show_warning()
            else:
                self.Success = False
                mes = _('File "{}" does not exist!').format(self.file)
                sh.objs.get_mes(f,mes,True).show_warning()
        else:
            sh.com.cancel(f)



class Binary:
    
    def __init__(self,file):
        self.fsize   = 0
        self.bsize   = 0
        self.file    = file
        self.bname   = sh.Path(file).get_basename()
        # We need silent logging here (not 'sh.File.Success')
        self.Success = os.path.exists(self.file)
        self.open()
    
    def get_zero(self,start,end):
        f = '[MClient] plugins.multitranbin.get.Binary.get_zero'
        result = []
        if self.Success:
            pos = self.find(b'\x00',start,end)
            if pos:
                #TODO (?): implement finding multiple zero chunks
                result = [pos+2]
        else:
            sh.com.cancel(f)
        return result
    
    def get_parts2(self,pattern,start=0,end=0):
        # Run 'get_part2' in loop (only useful for finding stems)
        f = '[MClient] plugins.multitranbin.get.Binary.get_parts2'
        chunks = []
        if DEBUG:
            mchunks = []
            mpos1   = []
            mpos2   = []
        if self.Success:
            if pattern == b'':
                poses = self.get_zero(start,end)
            else:
                poses = self.find_all(pattern,start,end)
            for pos11 in poses:
                lengths = self.get_lengths(pos11)
                if self.check_lengths(pattern,lengths):
                    pos21 = pos11 + lengths[0]
                    pos22 = pos21 + lengths[1]
                    chunk = self.read(pos21,pos22)
                    if chunk and not chunk in chunks:
                        chunks.append(chunk)
                        if DEBUG:
                            mpos1.append(sh.com.set_figure_commas(pos21))
                            mpos2.append(sh.com.set_figure_commas(pos22))
                            mchunks.append(com.get_string(chunk))
            if DEBUG:
                if mchunks:
                    mpattern = ['"{}"'.format(com.get_string(pattern)) \
                                for i in range(len(mchunks))
                               ]
                    mstart = ['{}'.format(sh.com.set_figure_commas(start)) \
                              for i in range(len(mchunks))
                             ]
                    mend = ['{}'.format(sh.com.set_figure_commas(end)) \
                              for i in range(len(mchunks))
                           ]
                    nos      = [i + 1 for i in range(len(chunks))]
                    mchunks  = ['"{}"'.format(chunk) \
                                for chunk in mchunks
                               ]
                    headers  = ('NO','PATTERN','START'
                               ,'END','POS1','POS2','CHUNK'
                               )
                    iterable = (nos,mpattern,mstart
                               ,mend,mpos1,mpos2,mchunks
                               )
                    mes = sh.FastTable (headers  = headers
                                       ,iterable = iterable
                                       ,maxrow   = 47
                                       ).run()
                    mes = '\n\n' + mes
                    sh.objs.get_mes(f,mes,True).show_debug()
                else:
                    mes = _('No debug info')
                    sh.objs.get_mes(f,mes,True).show_debug()
        else:
            sh.com.rep_lazy(f)
        return chunks
    
    def get_parts1(self,pattern,start=0,end=0):
        # Get suggestions
        f = '[MClient] plugins.multitranbin.get.Binary.get_parts1'
        chunks = []
        if DEBUG:
            mchunks = []
            mpos1   = []
            mpos2   = []
        if self.Success:
            if pattern:
                poses = self.find_all(pattern,start,end)
                for pos1 in poses:
                    lengths = self.get_lengths(pos1)
                    pos2 = pos1 + lengths[0]
                    chunk = self.read(pos1,pos2)
                    if chunk and not chunk in chunks:
                        chunks.append(chunk)
                        if DEBUG:
                            mpos1.append(sh.com.set_figure_commas(pos1))
                            mpos2.append(sh.com.set_figure_commas(pos2))
                            mchunks.append(com.get_string(chunk))
            else:
                sh.com.rep_empty(f)
            if DEBUG:
                if mchunks:
                    mpattern = ['"{}"'.format(com.get_string(pattern)) \
                                for i in range(len(mchunks))
                               ]
                    mstart = ['{}'.format(sh.com.set_figure_commas(start)) \
                              for i in range(len(mchunks))
                             ]
                    mend = ['{}'.format(sh.com.set_figure_commas(end)) \
                              for i in range(len(mchunks))
                           ]
                    nos      = [i + 1 for i in range(len(chunks))]
                    mchunks  = ['"{}"'.format(chunk) \
                                for chunk in mchunks
                               ]
                    headers  = ('NO','PATTERN','START'
                               ,'END','POS1','POS2','CHUNK'
                               )
                    iterable = (nos,mpattern,mstart
                               ,mend,mpos1,mpos2,mchunks
                               )
                    mes = sh.FastTable (headers  = headers
                                       ,iterable = iterable
                                       ,maxrow   = 47
                                       ).run()
                    mes = '\n\n' + mes
                    sh.objs.get_mes(f,mes,True).show_debug()
                else:
                    mes = _('No debug info')
                    sh.objs.get_mes(f,mes,True).show_debug()
        else:
            sh.com.rep_lazy(f)
        return chunks
    
    def find_all(self,pattern,start=0,end=0):
        f = '[MClient] plugins.multitranbin.get.Binary.find_all'
        matches = []
        if self.Success:
            while True:
                start = self.find(pattern,start,end)
                if start:
                    matches.append(start)
                    start += 1
                else:
                    break
            if DEBUG:
                mes = [sh.com.set_figure_commas(item) for item in matches]
                sh.objs.get_mes(f,mes,True).show_debug()
        else:
            sh.com.cancel(f)
        return matches
    
    def get_page_limit(self):
        f = '[MClient] plugins.multitranbin.get.Binary.get_page_limit'
        self.get_file_size()
        self.get_block_size()
        if self.Success:
            val = self.fsize // self.bsize
            if DEBUG:
                mes = sh.com.set_figure_commas(val)
                sh.objs.get_mes(f,mes,True).show_debug()
            return val
        else:
            sh.com.cancel(f)
    
    def get_file_size(self):
        ''' This should be equal to 'sh.File(self.vfile).get_size()'.
            #NOTE: size = max_pos + 1
        '''
        f = '[MClient] plugins.multitranbin.get.Binary.get_file_size'
        if self.Success:
            if not self.fsize:
                self.fsize = sh.File(self.file).get_size()
                if DEBUG:
                    mes  = _('File "{}" has the size of {}')
                    size = sh.com.get_human_size(self.fsize)
                    mes  = mes.format(self.file,size)
                    sh.objs.get_mes(f,mes,True).show_debug()
            if not self.fsize:
                self.Success = False
                mes = _('Empty output is not allowed!')
                sh.objs.get_mes(f,mes).show_warning()
        else:
            sh.com.cancel(f)
        return self.fsize
    
    def get_page_limits(self,page_no):
        # Return positions of a page based on MT indicators
        f = '[MClient] plugins.multitranbin.get.Binary.get_page_limits'
        if self.Success:
            if page_no is None or not self.get_block_size():
                sh.com.rep_empty(f)
            elif page_no == 0:
                if DEBUG:
                    sub = sh.com.get_human_size(self.bsize)
                    mes = _('Page size: {}').format(sub)
                    sh.objs.get_mes(f,mes,True).show_debug()
                    pos1 = 0
                    pos2 = self.bsize
                    sub  = sh.com.set_figure_commas(pos2)
                    mes  = _('Page limits: [{}:{}]')
                    mes  = mes.format(pos1,sub)
                    sh.objs.get_mes(f,mes,True).show_debug()
                return(0,self.bsize)
            else:
                pos = page_no * self.bsize
                read = self.read(pos+1,pos+3)
                if read:
                    if len(read) == 2:
                        size = struct.unpack('<h',read)[0]
                        size = com.overflowh(size)
                        if size > 0:
                            if DEBUG:
                                sub = sh.com.get_human_size(size)
                                mes = _('Page size: {}').format(sub)
                                sh.objs.get_mes(f,mes,True).show_debug()
                            pos1 = pos + 3
                            pos2 = pos1 + size
                            if DEBUG:
                                sub1 = sh.com.set_figure_commas(pos1)
                                sub2 = sh.com.set_figure_commas(pos2)
                                mes  = _('Page limits: [{}:{}]')
                                mes  = mes.format(sub1,sub2)
                                sh.objs.get_mes(f,mes,True).show_debug()
                            return(pos1,pos2)
                        else:
                            sub = '{} > 0'.format(size)
                            mes = _('The condition "{}" is not observed!')
                            mes = mes.format(sub)
                            sh.objs.get_mes(f,mes,True).show_warning()
                    else:
                        sub = '{} == 2'.format(len(read))
                        mes = _('The condition "{}" is not observed!')
                        mes = mes.format(sub)
                        sh.objs.get_mes(f,mes,True).show_warning()
                else:
                    sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def get_block_size(self):
        f = '[MClient] plugins.multitranbin.get.Binary.get_block_size'
        if self.Success:
            if not self.bsize:
                read = self.read(28,30)
                if read:
                    try:
                        self.bsize = struct.unpack('<h',read)[0]
                    except Exception as e:
                        self.Success = False
                        mes = _('Third-party module has failed!\n\nDetails: {}')
                        mes = mes.format(e)
                        sh.objs.get_mes(f,mes,True).show_warning()
                    if DEBUG:
                        mes = sh.com.set_figure_commas(self.bsize)
                        sh.objs.get_mes(f,mes,True).show_debug()
                else:
                    self.Success = False
                    sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
        return self.bsize
    
    def check_lengths(self,pattern,lengths):
        f = '[MClient] plugins.multitranbin.get.Binary.check_lengths'
        if self.Success:
            if lengths:
                if lengths[0] == len(pattern) and lengths[1] > 0:
                    return True
                elif DEBUG:
                    mes = _('The check has failed!')
                    sh.objs.get_mes(f,mes,True).show_warning()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def get_part2(self,pattern,start=0,end=0):
        f = '[MClient] plugins.multitranbin.get.Binary.get_part2'
        if self.Success:
            pos11 = self.find(pattern,start,end)
            if pos11 is None:
                ''' We look for combinations of stems, so a mismatch is
                    a common case.
                '''
                if DEBUG:
                    sh.com.rep_lazy(f)
            else:
                lengths = self.get_lengths(pos11)
                if self.check_lengths(pattern,lengths):
                    pos21 = pos11 + lengths[0]
                    pos22 = pos21 + lengths[1]
                    return self.read(pos21,pos22)
        else:
            sh.com.cancel(f)
    
    def get_lengths(self,index_):
        f = '[MClient] plugins.multitranbin.get.Binary.get_lengths'
        if self.Success:
            ''' There are 'M' pages at the beginning, so an index of
                the 1st part will always be positive.
            '''
            if index_ is None:
                sh.com.rep_empty(f)
            elif index_ > 2:
                pos1 = index_ - 2
                pos2 = index_ - 1
                len1 = self.read(pos1,pos1+1)
                len2 = self.read(pos2,pos2+1)
                if len1 and len2:
                    len1 = struct.unpack('<b',len1)[0]
                    len2 = struct.unpack('<b',len2)[0]
                    ''' The 2nd value of the index part can be negative
                        (at least in demo, e.g., dict.ert: 723,957 ->
                        b'\x03\x8a' -> (3; -118) -> (3; 138)).
                    '''
                    len1 = com.overflowb(len1)
                    len2 = com.overflowb(len2)
                    if DEBUG:
                        mes = _('Part #{} length: {}').format(1,len1)
                        sh.objs.get_mes(f,mes,True).show_debug()
                        mes = _('Part #{} length: {}').format(2,len2)
                        sh.objs.get_mes(f,mes,True).show_debug()
                    return(len1,len2)
                else:
                    sh.com.rep_empty(f)
            else:
                sub = '{} > 2'.format(index_)
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                sh.objs.get_mes(f,mes,True).show_warning()
        else:
            sh.com.cancel(f)
    
    def read(self,start,end):
        f = '[MClient] plugins.multitranbin.get.Binary.read'
        if self.Success:
            if start is None or end is None:
                sh.com.rep_empty(f)
            elif 0 <= start < end <= self.get_file_size():
                self.imap.seek(start)
                chunk = self.imap.read(end-start)
                if DEBUG:
                    mes = '"{}"'.format(com.get_string(chunk))
                    sh.objs.get_mes(f,mes,True).show_debug()
                return chunk
            else:
                self.Success = False
                sub1 = sh.com.set_figure_commas(start)
                sub2 = sh.com.set_figure_commas(end)
                sub3 = sh.com.set_figure_commas(self.fsize)
                sub = '0 <= {} < {} <= {}'.format(sub1,sub2,sub3)
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                sh.objs.get_mes(f,mes).show_warning()
        else:
            sh.com.cancel(f)
    
    def find(self,pattern,start=0,end=0):
        f = '[MClient] plugins.multitranbin.get.Binary.find'
        if self.Success:
            if pattern:
                if not end:
                    end = self.get_file_size()
                result = self.imap.find(pattern,start,end)
                if DEBUG:
                    if end == -1:
                        mes = '{}, "{}" => {}'
                        mes = mes.format (self.bname
                                         ,com.get_string(pattern)
                                         ,sh.com.set_figure_commas(result)
                                         )
                    else:
                        mes = '{}, [{}:{}], "{}" => {}'
                        mes = mes.format (self.bname
                                         ,sh.com.set_figure_commas(start)
                                         ,sh.com.set_figure_commas(end)
                                         ,com.get_string(pattern)
                                         ,sh.com.set_figure_commas(result)
                                         )
                    sh.objs.get_mes(f,mes,True).show_debug()
                if result >= 0:
                    return result
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def open(self):
        f = '[MClient] plugins.multitranbin.get.Binary.open'
        if self.Success:
            mes = _('Open "{}"').format(self.file)
            sh.objs.get_mes(f,mes,True).show_info()
            self.bin = open(self.file,'rb')
            # 'mmap' fails upon opening an empty file!
            try:
                self.imap = mmap.mmap (self.bin.fileno(),0
                                      ,access=mmap.ACCESS_READ
                                      )
            except Exception as e:
                self.Success = False
                mes = _('Third-party module has failed!\n\nDetails: {}')
                mes = mes.format(e)
                sh.objs.get_mes(f,mes,True).show_warning()
        else:
            sh.com.cancel(f)
    
    def close(self):
        f = '[MClient] plugins.multitranbin.get.Binary.close'
        if self.Success:
            mes = _('Close "{}"').format(self.file)
            sh.objs.get_mes(f,mes,True).show_info()
            self.imap.flush()
            self.bin.close()
        else:
            sh.com.cancel(f)



class UPage(Binary):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.page  = b''
        self.pos1  = 0
        self.pos2  = 0
        self.psize = 0
        self.part1 = []
        self.part2 = []
    
    def _get_no(self,stem):
        f = '[MClient] plugins.multitranbin.get.UPage._get_no'
        try:
            return self.part1.index(stem)
        except ValueError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f,mes).show_error()
            return -1
    
    def _get_ref(self,i):
        f = '[MClient] plugins.multitranbin.get.UPage._get_ref'
        if i is None:
            sh.com.rep_empty(f)
        else:
            try:
                page_ref = struct.unpack('<h',self.part2[i])[0]
                if DEBUG:
                    mes = _('#{}: {}').format(i,page_ref)
                    sh.objs.get_mes(f,mes,True).show_debug()
                return page_ref
            except IndexError:
                mes = _('Wrong input data!')
                sh.objs.get_mes(f,mes).show_error()
    
    def _decode(self,pattern):
        if self.file in (objs.get_files().iwalker.get_stems1()
                        ,objs.files.iwalker.get_stems2()
                        ):
            result = pattern.decode(CODING,'replace')
        else:
            result = com.get_string(pattern,0)
        return '"{}"'.format(result)
    
    def _log(self,pattern,i):
        f = '[MClient] plugins.multitranbin.get.UPage._log'
        if self.part1[i] == pattern:
            oper = '<='
        else:
            oper = '<'
        if self.part1[i] == b'':
            stem1 = _('Start')
        else:
            stem1 = _('{} (#{})')
            stem1 = stem1.format (self._decode(self.part1[i])
                                 ,self._get_no(self.part1[i])
                                 )
        if i + 1 < len(self.part1):
            stem2 = _('{} (#{})')
            stem2 = stem2.format (self._decode(self.part1[i+1])
                                 ,self._get_no(self.part1[i+1])
                                 )
        else:
            stem2 = _('End')
        mes = '{} {} {} {} {}'.format (stem1
                                      ,oper
                                      ,self._decode(pattern)
                                      ,'<'
                                      ,stem2
                                      )
        sh.objs.get_mes(f,mes,True).show_debug()
    
    def searchu(self,pattern):
        f = '[MClient] plugins.multitranbin.get.UPage.searchu'
        if self.Success:
            self.get_parts()
            if self.part1:
                i = 1
                while i < len(self.part1):
                    if self.part1[i-1] <= pattern < self.part1[i]:
                        break
                    i += 1
                i -= 1
                if DEBUG:
                    self._log(pattern,i)
                return self.get_page_limits(self._get_ref(i))
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def get_parts(self):
        f = '[MClient] plugins.multitranbin.get.UPage.get_parts'
        if self.Success:
            if not self.part2:
                if self.get_page():
                    pos = 0
                    while pos + 2 < len(self.page):
                        ''' #NOTE: indexing returns integers, slicing
                            returns bytes.
                        '''
                        read = self.page[pos:pos+2]
                        pos += 2
                        len1, len2 = struct.unpack('<2b',read)
                        len1 = com.overflowb(len1)
                        len2 = com.overflowb(len2)
                        if pos + len1 + len2 < len(self.page):
                            ''' Do this only after checking
                                the condition, otherwise, resulting
                                lists will have a different length.
                            '''
                            chunk1 = self.page[pos:pos+len1]
                            pos += len1
                            chunk2 = self.page[pos:pos+len2]
                            pos += len2
                            ''' #NOTE: Instructions for zero-length
                                chunks should be allowed - I encountered
                                such and they were necessary to parse
                                the page correctly to the end. However,
                                at least one of the chunks should be
                                non-empty, otherwise, checking output
                                will fail.
                            '''
                            if chunk1 or chunk2:
                                self.part1.append(chunk1)
                                self.part2.append(chunk2)
                        else:
                            com.report_status(pos,self.page)
                            if len(self.page) - pos > 1:
                                mes = _('Processing the pattern has not been completed, but the end of the file has already been reached!')
                                sh.objs.get_mes(f,mes,True).show_warning()
                            break
                    self.conform_parts()
                else:
                    sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def get_page(self):
        f = '[MClient] plugins.multitranbin.get.UPage.get_page'
        if self.Success:
            if not self.page:
                if self.get_size():
                    page = self.read(self.pos1,self.pos2)
                    # Keep 'self.page' iterable
                    if page is None:
                        sh.com.rep_empty(f)
                    else:
                        self.page = page
                else:
                    sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
        return self.page
    
    def get_size(self):
        f = '[MClient] plugins.multitranbin.get.UPage.get_size'
        if self.Success:
            if not self.psize:
                ''' The 1st page is an area with M identifier.
                    The 2nd page is an intermediate page with
                    U identifier.
                '''
                poses = self.get_page_limits(1)
                if poses:
                    self.pos1  = poses[0]
                    self.pos2  = poses[1]
                    self.psize = self.pos2 - self.pos1
                else:
                    sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
        return self.psize
    
    def check_parts(self):
        f = '[MClient] plugins.multitranbin.get.UPage.check_parts'
        if self.Success:
            if len(self.part1) == len(self.part2):
                Check = True
                for item in self.part2:
                    if len(item) != 2:
                        Check = False
                        break
                return Check
            else:
                self.Success = False
                sub = '{} == {}'.format (len(self.part1)
                                        ,len(self.part2)
                                        )
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                sh.objs.get_mes(f,mes).show_error()
        else:
            sh.com.cancel(f)
    
    def _get_missing(self):
        ''' Get the 1st page number that is not described in U page or
            create a new page number based on the max page number.
        '''
        f = '[MClient] plugins.multitranbin.get.UPage._get_missing'
        unpacked = sorted(set(self.part2))
        unpacked = [struct.unpack('<h',item)[0] for item in unpacked]
        # We need +1 for a new item and +1 for 'range'
        compare = [i for i in range(max(unpacked)+2)]
        # Page #0 is an M page area, and page #1 is U page
        compare = compare[2:]
        for item in compare:
            if item not in unpacked:
                sh.objs.get_mes(f,item,True).show_debug()
                return item
    
    def conform_parts(self):
        f = '[MClient] plugins.multitranbin.get.UPage.conform_parts'
        if self.Success:
            if self.part1:
                if self.check_parts():
                    old = self._get_missing()
                    new = struct.pack('<h',old)
                    mes = '{} -> "{}"'.format(old,new)
                    sh.objs.get_mes(f,mes,True).show_debug()
                    self.part1.insert(0,b'')
                    self.part2.append(new)
                else:
                    mes = _('The check has failed!')
                    sh.objs.get_mes(f,mes,True).show_warning()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)



class Walker:
    
    def __init__(self):
        self.set_values()
        if PATH:
            self.reset()
    
    def get_ending(self):
        f = '[MClient] plugins.multitranbin.get.Walker.get_ending'
        if self.Success:
            if not self.ending:
                fname = 'sik.' + self.lang13
                file  = self.get_file(fname)
                if file:
                    self.ending = file
                else:
                    self.Success = False
                    mes = _('File "{}" does not exist!').format(fname)
                    sh.objs.get_mes(f,mes,True).show_warning()
        else:
            sh.com.cancel(f)
        return self.ending
    
    def get_subject(self):
        f = '[MClient] plugins.multitranbin.get.Walker.get_subject'
        if self.Success:
            if not self.subject:
                fname = 'subjects.txt'
                file  = self.get_file(fname)
                if file:
                    self.subject = file
                else:
                    self.Success = False
                    mes = _('File "{}" does not exist!').format(fname)
                    sh.objs.get_mes(f,mes,True).show_warning()
        else:
            sh.com.cancel(f)
        return self.subject
    
    def get_typein1(self):
        f = '[MClient] plugins.multitranbin.get.Walker.get_typein1'
        if self.Success:
            if not self.typein1:
                fname = 'typein.' + self.lang11 + self.lang21
                file  = self.get_file(fname)
                if file:
                    self.typein1 = file
                    sh.objs.get_mes(f,self.typein1,True).show_debug()
                else:
                    self.Success = False
                    mes = _('File "{}" does not exist!').format(fname)
                    sh.objs.get_mes(f,mes,True).show_warning()
        else:
            sh.com.cancel(f)
        return self.typein1

    def get_typein2(self):
        f = '[MClient] plugins.multitranbin.get.Walker.get_typein2'
        if self.Success:
            if not self.typein2:
                fname = 'typein.' + self.lang21 + self.lang11
                file  = self.get_file(fname)
                if file:
                    self.typein2 = file
                    sh.objs.get_mes(f,self.typein2,True).show_debug()
                else:
                    self.Success = False
                    mes = _('File "{}" does not exist!').format(fname)
                    sh.objs.get_mes(f,mes,True).show_warning()
        else:
            sh.com.cancel(f)
        return self.typein2
    
    def get_files(self):
        f = '[MClient] plugins.multitranbin.get.Walker.get_files'
        if self.Success:
            return [self.get_typein1(),self.get_typein2()
                   ,self.get_stems1(),self.get_stems2()
                   ,self.get_glue1(),self.get_glue2()
                   ,self.get_article()
                   ]
        else:
            sh.com.cancel(f)
            return []
    
    def get_article(self):
        f = '[MClient] plugins.multitranbin.get.Walker.get_article'
        if self.Success:
            if not self.article:
                fname = 'dict.' + self.lang11 + self.lang21 + 't'
                if not fname in self.fnames:
                    fname = 'dict.' + self.lang21 + self.lang11 + 't'
                file = self.get_file(fname)
                if file:
                    self.article = file
                    sh.objs.get_mes(f,self.article,True).show_debug()
                else:
                    self.Success = False
                    mes = _('File "{}" does not exist!').format(fname)
                    sh.objs.get_mes(f,mes,True).show_warning()
        else:
            sh.com.cancel(f)
        return self.article
    
    def get_glue1(self):
        f = '[MClient] plugins.multitranbin.get.Walker.get_glue1'
        if self.Success:
            if not self.glue1:
                fname = 'dict.' + self.lang11 + self.lang21 + 'd'
                file  = self.get_file(fname)
                if file:
                    self.glue1 = file
                    sh.objs.get_mes(f,self.glue1,True).show_debug()
                else:
                    self.Success = False
                    mes = _('File "{}" does not exist!').format(fname)
                    sh.objs.get_mes(f,mes,True).show_warning()
        else:
            sh.com.cancel(f)
        return self.glue1
    
    def get_glue2(self):
        f = '[MClient] plugins.multitranbin.get.Walker.get_glue2'
        if self.Success:
            if not self.glue2:
                fname = 'dict.' + self.lang21 + self.lang11 + 'd'
                file  = self.get_file(fname)
                if file:
                    self.glue2 = file
                    sh.objs.get_mes(f,self.glue2,True).show_debug()
                else:
                    self.Success = False
                    mes = _('File "{}" does not exist!').format(fname)
                    sh.objs.get_mes(f,mes,True).show_warning()
        else:
            sh.com.cancel(f)
        return self.glue2
    
    def reset(self):
        self.set_values()
        self.check()
        self.set_langs()
        self.walk()
    
    def set_langs(self):
        f = '[MClient] plugins.multitranbin.get.Walker.set_langs'
        if self.Success:
            lang1       = LANG1.lower()
            lang2       = LANG2.lower()
            self.lang11 = lang1[0:1]
            self.lang21 = lang2[0:1]
            self.lang13 = lang1[0:3]
            self.lang23 = lang2[0:3]
        else:
            sh.com.cancel(f)
    
    def check(self):
        f = '[MClient] plugins.multitranbin.get.Walker.check'
        if PATH and LANG1 and LANG2:
            self.idir = sh.Directory(PATH)
            self.Success = self.idir.Success
        else:
            self.Success = False
            sh.com.rep_empty(f)
    
    def get_stems1(self):
        f = '[MClient] plugins.multitranbin.get.Walker.get_stems1'
        if self.Success:
            if not self.stems1:
                fname = 'stem.' + self.lang13
                file  = self.get_file(fname)
                if file:
                    self.stems1 = file
                else:
                    self.Success = False
                    mes = _('File "{}" does not exist!').format(fname)
                    sh.objs.get_mes(f,mes,True).show_warning()
        else:
            sh.com.cancel(f)
        return self.stems1
    
    def get_stems2(self):
        f = '[MClient] plugins.multitranbin.get.Walker.get_stems2'
        if self.Success:
            if not self.stems2:
                fname = 'stem.' + self.lang23
                file  = self.get_file(fname)
                if file:
                    self.stems2 = file
                else:
                    self.Success = False
                    mes = _('File "{}" does not exist!').format(fname)
                    sh.objs.get_mes(f,mes,True).show_warning()
        else:
            sh.com.cancel(f)
        return self.stems2
    
    def get_file(self,fname):
        f = '[MClient] plugins.multitranbin.get.Walker.get_file'
        if self.Success:
            try:
                ind = self.fnames.index(fname)
                return self.files[ind]
            except (ValueError,IndexError):
                mes = _('Wrong input data!')
                sh.objs.get_mes(f,mes,True).show_warning()
        else:
            sh.com.cancel(f)
    
    def set_values(self):
        self.Success = False
        self.idir    = None
        self.files   = []
        self.fnames  = []
        self.lang11  = ''
        self.lang21  = ''
        self.lang13  = ''
        self.lang23  = ''
        self.typein1 = ''
        self.typein2 = ''
        self.stems1  = ''
        self.stems2  = ''
        self.glue1   = ''
        self.glue2   = ''
        self.article = ''
        self.subject = ''
        self.ending  = ''
    
    def walk(self):
        f = '[MClient] plugins.multitranbin.get.Walker.walk'
        if self.Success:
            for dirpath, dirnames, filenames in os.walk(self.idir.dir):
                for filename in filenames:
                    self.fnames.append(filename.lower())
                    file = os.path.join(dirpath,filename)
                    self.files.append(file)
        else:
            sh.com.cancel(f)
        return self.files



class TypeIn(UPage):
    # Parse files like 'typein.er'
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    
    def search(self,pattern):
        f = '[MClient] plugins.multitranbin.get.TypeIn.search'
        if self.Success:
            if pattern:
                coded  = bytes(pattern,CODING)
                poses  = self.searchu(coded)
                chunks = self.run_reader(poses)
                if chunks:
                    matches = []
                    for chunk in chunks:
                        if chunk.startswith(coded):
                            matches.append(chunk)
                    decoded = [match.decode(CODING,'replace') \
                               for match in matches if match
                              ]
                    for i in range(len(decoded)):
                        ''' Sometimes MT provides for suggestions in
                            different case, e.g., 'aafc', 'AAFC'
                            separated by b'\x00'.
                        '''
                        decoded[i] = decoded[i].split('\x00')
                        decoded[i] = [item for item in decoded[i] \
                                      if item
                                     ]
                        if decoded[i][-1]:
                            decoded[i] = decoded[i][-1]
                        else:
                            decoded[i] = decoded[i][0]
                    if DEBUG:
                        sh.objs.get_mes(f,decoded,True).show_debug()
                    return decoded
                else:
                    sh.com.rep_empty(f)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def run_reader(self,poses):
        f = '[MClient] plugins.multitranbin.get.TypeIn.reader'
        if self.Success:
            if poses:
                stream = self.read(poses[0],poses[1])
                if stream:
                    chunks = []
                    pos = 0
                    while pos + 2 < len(stream):
                        ''' #NOTE: indexing returns integers,
                            slicing returns bytes.
                        '''
                        read = stream[pos:pos+2]
                        pos += 2
                        len1, len2 = struct.unpack('<2b',read)
                        len1 = com.overflowb(len1)
                        len2 = com.overflowb(len2)
                        if pos + len1 + len2 < len(stream):
                            ''' Do this only after checking
                                the condition, otherwise, resulting
                                lists will have a different length.
                            '''
                            chunk = stream[pos:pos+len1]
                            pos += len1 + len2
                            if chunk:
                                chunks.append(chunk)
                        else:
                            com.report_status(pos,stream)
                            break
                    return chunks
                else:
                    sh.com.rep_empty(f)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)



class Suggest:
    
    def __init__(self,pattern):
        self.set_values()
        if pattern:
            self.reset(pattern)
    
    def set_values(self):
        self.Success = True
        self.pattern = ''
    
    def reset(self,pattern):
        f = '[MClient] plugins.multitranbin.get.Suggest.reset'
        self.pattern = pattern
        if not self.pattern:
            self.Success = False
            sh.com.rep_empty(f)
    
    def get(self,limit=20):
        f = '[MClient] plugins.multitranbin.get.Suggest.get'
        if self.Success:
            suggestions = objs.get_files().get_typein1().search(self.pattern)
            if suggestions:
                return suggestions[0:20]
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.pattern = com.strip(self.pattern)
        return self.get()



class AllDics:
    
    def __init__(self):
        self.set_values()
        self.reset()
    
    def get_langs(self):
        # Return all available languages
        files = []
        f = '[MClient] plugins.multitranbin.get.AllDics.langs'
        if self.Success:
            #TODO: elaborate
            # Relative paths are already lowercased
            for fname in objs.get_files().iwalker.fnames:
                if fname.startswith('dict.') and fname.endswith('t'):
                    files.append(fname)
        else:
            sh.com.cancel(f)
        return files
    
    def get(self,search):
        f = '[MClient] plugins.multitranbin.get.AllDics.get'
        if self.Success:
            if search:
                pass
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def set_values(self):
        self.dics   = []
        self.path   = ''
        # Do not run anything if 'self.reset' was not run
        self.Success = False
    
    def reset(self):
        self.set_values()
        self.path = PATH
        self.Success = sh.Directory(self.path).Success
    
    def walk(self):
        f = '[MClient] plugins.multitranbin.get.AllDics.walk'
        if self.Success:
            pass
        else:
            sh.com.cancel(f)
    
    def locate(self):
        f = '[MClient] plugins.multitranbin.get.AllDics.locate'
        if self.Success:
            if not self.dics:
                if self.walk():
                    #TODO: implement
                    self.dics = []
                else:
                    sh.com.rep_lazy(f)
            mes = _('{} offline dictionaries are available')
            mes = mes.format(len(self.dics))
            sh.objs.get_mes(f,mes,True).show_info()
            return self.dics
        else:
            sh.com.cancel(f)
    
    def load(self):
        f = '[MClient] plugins.multitranbin.get.AllDics.load'
        if self.Success:
            pass
        else:
            sh.com.cancel(f)



class Articles(UPage):
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
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def search(self,coded):
        # Do not fail the whole class upon a failed search
        f = '[MClient] plugins.multitranbin.get.Articles.search'
        if self.Success:
            if coded:
                poses = self.searchu(coded)
                if poses:
                    chunk = self.get_part2 (pattern = coded
                                           ,start   = poses[0]
                                           ,end     = poses[1]
                                           )
                    return self.parse(chunk)
                else:
                    sh.com.rep_empty(f)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)



class Glue(UPage):
    # Parse files like 'dict.erd'
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    
    def search(self,coded):
        # Do not fail the whole class upon a failed search
        f = '[MClient] plugins.multitranbin.get.Glue.search'
        if self.Success:
            if coded:
                poses = self.searchu(coded)
                if poses:
                    chunk = self.get_part2 (pattern = coded
                                           ,start   = poses[0]
                                           ,end     = poses[1]
                                           )
                    if chunk:
                        return self.parse(chunk)
                    else:
                        ''' 'dict.erd' sometimes does not comprise
                            stem numbers provided by 'stem.eng'
                            (at least in the demo version).
                        '''
                        if DEBUG:
                            sh.com.rep_lazy(f)
                else:
                    sh.com.rep_empty(f)
            else:
                sh.com.rep_empty(f)
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
                    if DEBUG:
                        sh.objs.get_mes(f,chnos,True).show_debug()
                        sh.objs.get_mes(f,nos,True).show_debug()
                    return chnos
                else:
                    mes = _('Wrong input data: "{}"!')
                    mes = mes.format(com.get_string(chunk))
                    sh.objs.get_mes(f,mes).show_warning()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)



class Commands:
    
    def strip(self,pattern):
        if pattern is None:
            pattern = ''
        pattern = pattern.strip()
        pattern = sh.Text(pattern).convert_line_breaks()
        pattern = sh.Text(pattern).delete_line_breaks()
        pattern = sh.Text(pattern).delete_punctuation()
        pattern = sh.Text(pattern).delete_duplicate_spaces()
        pattern = pattern.lower()
        return pattern
    
    def report_status(self,pos,stream):
        f = '[MClient] plugins.multitranbin.get.Commands.report_status'
        if stream:
            mes = _('{}/{} bytes have been processed')
            mes = mes.format(pos,len(stream))
            sh.objs.get_mes(f,mes,True).show_info()
            if DEBUG:
                remains = stream[pos:len(stream)]
                remains = com.get_string(remains)
                mes = _('Unprocessed fragment: "{}"').format(remains)
                sh.objs.get_mes(f,mes,True).show_debug()
        else:
            sh.com.rep_empty(f)
    
    def unpackh(self,chno):
        return self.unpack(chno,'<h')
    
    def overflowh(self,no):
        # Limits: -32768 <= no <= 32767
        f = '[MClient] plugins.multitranbin.get.Commands.overflowh'
        if no < 0:
            result = 32768 + no
            if DEBUG:
                mes = '{} -> {}'.format(no,result)
                sh.objs.get_mes(f,mes,True).show_debug()
            return result
        else:
            return no
    
    def overflowb(self,no):
        f = '[MClient] plugins.multitranbin.get.Commands.overflowb'
        if no < 0:
            ''' Byte format requires -128 <= no <= 127, so it looks
                like, when a page size value is negative, it has just
                overflown the minimum negative -128, e.g., -106 actually
                means 150: 128 - 106 = 22 => 127 + 22 + 1 = 150.
            '''
            new = 256 + no
            if DEBUG:
                mes = '{} -> {}'.format(no,new)
                sh.objs.get_mes(f,mes,True).show_debug()
            return new
        else:
            return no
    
    def unpack(self,chno,mode='<L'):
        f = '[MClient] plugins.multitranbin.get.Commands.unpack'
        if chno:
            if mode == '<L':
                chno += b'\x00'
            try:
                return struct.unpack(mode,chno)[0]
            except Exception as e:
                mes = _('Third-party module has failed!\n\nDetails: {}')
                mes = mes.format(e)
                sh.objs.get_mes(f,mes,True).show_warning()
        else:
            sh.com.rep_empty(f)
    
    def is_accessible(self):
        return len(objs.get_all_dics().get_langs())
    
    def get_string(self,chunk,limit=200):
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
                if limit:
                    result = sh.Text(result).shorten(limit)
            except Exception as e:
                sh.objs.get_mes(f,str(e)).show_warning()
                result = str(chunk)
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
            sh.com.rep_empty(f)
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


class Files:
    
    def __init__(self):
        self.reset()
    
    def get_ending(self):
        if self.ending is None:
            self.ending = Ending(self.iwalker.get_ending())
        return self.ending
    
    def get_subject(self):
        if self.subject is None:
            self.subject = Subject(self.iwalker.get_subject())
        return self.subject
    
    def get_typein1(self):
        if self.typein1 is None:
            self.typein1 = TypeIn(self.iwalker.get_typein1())
        return self.typein1
    
    def get_typein2(self):
        if self.typein2 is None:
            self.typein2 = TypeIn(self.iwalker.get_typein2())
        return self.typein2
    
    def get_stems1(self):
        if self.stems1 is None:
            self.stems1 = Stems(self.iwalker.get_stems1())
        return self.stems1
    
    def get_stems2(self):
        if self.stems2 is None:
            self.stems2 = Stems(self.iwalker.get_stems2())
        return self.stems2
    
    def get_glue1(self):
        if self.glue1 is None:
            self.glue1 = Glue(self.iwalker.get_glue1())
        return self.glue1
    
    def get_glue2(self):
        if self.glue2 is None:
            self.glue2 = Glue(self.iwalker.get_glue2())
        return self.glue2
    
    def get_article(self):
        if self.article is None:
            self.article = Articles(self.iwalker.get_article())
        return self.article
    
    def open(self):
        f = '[MClient] plugins.multitranbin.get.Files.open'
        if self.Success:
            self.get_typein1()
            self.get_typein2()
            self.get_stems1()
            self.get_stems2()
            self.get_glue1()
            self.get_glue2()
            self.get_article()
        else:
            sh.com.cancel(f)
    
    def close(self):
        f = '[MClient] plugins.multitranbin.get.Files.close'
        if self.Success:
            self.get_typein1().close()
            self.get_typein2().close()
            self.get_stems1().close()
            self.get_stems2().close()
            self.get_glue1().close()
            self.get_glue2().close()
            self.get_article().close()
        else:
            sh.com.cancel(f)
    
    def reset(self):
        self.set_values()
        self.iwalker = Walker()
        self.Success = self.iwalker.Success
    
    def set_values(self):
        self.iwalker = None
        self.Success = False
        self.typein1 = None
        self.typein2 = None
        self.stems1  = None
        self.stems2  = None
        self.glue1   = None
        self.glue2   = None
        self.article = None
        self.subject = None
        self.ending  = None



class Objects:
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.alldics = self.files = None
    
    def get_files(self):
        if self.files is None:
            self.files = Files()
            self.files.open()
        return self.files
    
    def get_all_dics(self):
        if self.alldics is None:
            self.alldics = AllDics()
        return self.alldics



class Stems(UPage):
    # Parse files like 'stem.eng'
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.speech = {}
    
    def get_speech(self,chno):
        f = '[MClient] plugins.multitranbin.get.Stems.get_speech'
        if self.Success:
            if chno in self.speech:
                result = self.speech[chno]
                result = com.unpackh(result)
                if DEBUG:
                    mes = '{} -> {}'.format(com.get_string(chno),result)
                    sh.objs.get_mes(f,mes,True).show_debug()
                return result
        else:
            sh.com.cancel(f)
    
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
                ends  = []
                #NOTE: 0 % 7 == 0
                if len(chunk) > 1 and (len(chunk) - 1) % 7 == 0:
                    chunks = com.get_chunks(chunk[1:],7)
                    for i in range(len(chunks)):
                        chnos.append(chunks[i][0:3])
                        ends.append(chunks[i][3:5])
                        self.speech[chunks[i][0:3]] = chunks[i][5:7]
                    ends = [struct.unpack('<h',end)[0] for end in ends]
                    if DEBUG:
                        for chno in chnos:
                            nos.append(com.unpack(chno))
                        if chnos:
                            ids = [i + 1 for i in range(len(nos))]
                            tmp = [sh.com.set_figure_commas(no) \
                                   for no in nos
                                  ]
                            mends = [sh.com.set_figure_commas(end) \
                                     for end in ends
                                    ]
                            mchnos = ['"' + com.get_string(chno) + '"' \
                                      for chno in chnos
                                     ]
                            initial = ['"{}"'.format(com.get_string(chunk))\
                                       for i in range(len(mchnos))
                                      ]
                            headers  = ('NO','INITIAL','CHUNK'
                                       ,'UNPACKED','END'
                                       )
                            iterable = (ids,initial,mchnos,tmp,mends)
                            mes = sh.FastTable (headers  = headers
                                               ,iterable = iterable
                                               ,maxrow   = 50
                                               ).run()
                            mes = '\n\n' + mes
                            sh.objs.get_mes(f,mes,True).show_debug()
                        else:
                            mes = _('No debug info')
                            sh.objs.get_mes(f,mes,True).show_debug()
                    return(chnos,ends)
                else:
                    sub = com.get_string(chunk)
                    mes = _('Wrong input data: "{}"!').format(sub)
                    sh.objs.get_mes(f,mes,True).show_warning()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def search(self,stem,end=''):
        # Do not fail the whole class upon a failed search
        f = '[MClient] plugins.multitranbin.get.Stems.search'
        if self.Success:
            ''' MT demo does not comprise stem #3 ('-') at all,
                so we use this workaround.
            '''
            if stem == '-':
                return [b'\x03\x00\x00']
            else:
                # Zero-length stems should be allowed
                coded = bytes(stem,CODING,'ignore')
                poses = self.searchu(coded)
                if poses:
                    chunks = self.get_parts2 (pattern = coded
                                             ,start   = poses[0]
                                             ,end     = poses[1]
                                             )
                    matches  = []
                    unpacked = []
                    for chunk in chunks:
                        result = self.parse(chunk)
                        if result:
                            chnos, endnos = result[0], result[1]
                            for i in range(len(endnos)):
                                if objs.get_files().get_ending().has_match(endnos[i],end):
                                    if DEBUG:
                                        no = com.unpack(chnos[i])
                                        no = sh.com.set_figure_commas(no)
                                        unpacked.append(no)
                                    matches.append(chnos[i])
                    if DEBUG:
                        if matches:
                            mmatches = ['"' + com.get_string(match) + '"'\
                                        for match in matches
                                       ]
                            mnos = [i + 1 for i in range(len(mmatches))]
                            headers = ('NO','STEM','END'
                                      ,'CHUNK','UNPACKED'
                                      )
                            mstems = ['"{}"'.format(stem) \
                                      for i in range(len(mnos))
                                     ]
                            mends  = ['"{}"'.format(end) \
                                      for i in range(len(mnos))
                                     ]
                            iterable = (mnos,mstems,mends
                                       ,mmatches,unpacked
                                       )
                            mes = sh.FastTable (headers  = headers
                                               ,iterable = iterable
                                               ).run()
                            mes = '\n\n' + mes
                            sh.objs.get_mes(f,mes,True).show_debug()
                        else:
                            mes = _('No debug info')
                            sh.objs.get_mes(f,mes,True).show_debug()
                    return matches
                else:
                    sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)



class Get:
    
    def __init__(self,pattern):
        self.set_values()
        self.pattern = pattern
        self.speech  = ''
        self.spabbr  = ''
    
    def set_speech(self):
        f = '[MClient] plugins.multitranbin.get.Get.set_speech'
        if self.Success:
            if self.stemnos:
                chno = self.stemnos[0][0:3]
                speech = objs.get_files().get_stems1().get_speech(chno)
                if DEBUG:
                    mes = '{} -> {}'.format (com.get_string(chno)
                                            ,speech
                                            )
                    sh.objs.get_mes(f,mes,True).show_debug()
                if speech is None:
                    sh.com.rep_empty(f)
                elif speech == 0:
                    # MT: phrase;phrase
                    self.speech = _('Phrase')
                    self.spabbr = _('phrase')
                elif speech == 1:
                    # MT: Abbreviation;abbr;Сокращение;сокр.
                    self.speech = _('Abbreviation')
                    self.spabbr = _('abbr.')
                elif speech == 2:
                    # MT: Adverb;adv;Наречие;нареч.
                    self.speech = _('Adverb')
                    self.spabbr = _('adv.')
                elif speech == 3:
                    # MT: Interjection;interj.;
                    # My translation: Междометие;межд.
                    self.speech = _('Interjection')
                    self.spabbr = _('interj.')
                elif speech == 4:
                    # MT: Conjunction;conj.
                    # My translation: Союз;союз
                    self.speech = _('Conjunction')
                    self.spabbr = _('conj.')
                elif speech == 5:
                    # MT: Article;article
                    # My translation: Артикль;арт.
                    self.speech = _('Article')
                    self.spabbr = _('art.')
                elif speech == 6:
                    # MT: Numeral;num;
                    # My translation: Числительное;числ.
                    self.speech = _('Numeral')
                    self.spabbr = _('num.')
                elif speech == 7:
                    # MT: Ord Numeral;ord.num;
                    # My translation: Порядковое числительное;поряд.числ.
                    self.speech = _('Ordinal Numeral')
                    self.spabbr = _('ord.num.')
                elif speech == 8:
                    # MT: Preposition;prepos.;Предлог;предл.
                    self.speech = _('Preposition')
                    self.spabbr = _('prepos.')
                elif speech == 9:
                    # MT: Form;form
                    # My translation: Форма;форма (?)
                    self.speech = _('Form')
                    self.spabbr = _('form')
                elif speech == 10:
                    # MT: Particle;part.;
                    # My translation: Частица;част.
                    self.speech = _('Particle')
                    self.spabbr = _('part.')
                elif 11 <= speech < 16:
                    # MT: Predicative;predic.
                    # My translation: Предикатив;предик.
                    self.speech = _('Predicative')
                    self.spabbr = _('predic.')
                elif 16 <= speech < 32:
                    # MT: Pronoun;pron;Местоимение;мест.
                    self.speech = _('Pronoun')
                    self.spabbr = _('pron')
                elif 32 <= speech < 64:
                    # MT: Adjective;adj;Прилагательное;прил.
                    self.speech = _('Adjective')
                    self.spabbr = _('adj')
                elif 64 <= speech < 128:
                    # MT: Noun;n;Существительное;сущ.
                    self.speech = _('Noun')
                    self.spabbr = _('n')
                elif 128 <= speech:
                    # MT: Verb;v;Глагол,гл.
                    self.speech = _('Verb')
                    self.spabbr = _('v')
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def get_combos(self):
        f = '[MClient] plugins.multitranbin.get.Get.get_combos'
        if self.Success:
            self.stemnos = list(itertools.product(*self.stemnos))
            self.stemnos = [b''.join(item) for item in self.stemnos]
            if DEBUG:
                sh.objs.get_mes(f,self.stemnos,True).show_debug()
        else:
            sh.com.cancel(f)
    
    def check(self):
        f = '[MClient] plugins.multitranbin.get.Get.check'
        if not self.pattern:
            self.Success = False
            sh.com.rep_empty(f)
    
    def strip(self):
        f = '[MClient] plugins.multitranbin.get.Get.strip'
        if self.Success:
            # Split hyphened words as if they were separate words
            self.pattern = self.pattern.replace('-',' - ')
            self.pattern = com.strip(self.pattern)
        else:
            sh.com.cancel(f)
    
    def get_stems(self):
        f = '[MClient] plugins.multitranbin.get.Get.get_stems'
        if self.Success:
            words = self.pattern.split(' ')
            for word in words:
                word_stems = []
                i = len(word)
                # Zero-length stems should be allowed
                while i >= 0:
                    #NOTE: nltk: according -> accord -> No matches!
                    stem = word[0:i]
                    end  = word[i:]
                    mes  = _('Try for "{}|{}"').format(stem,end)
                    sh.objs.get_mes(f,mes,True).show_info()
                    ''' Since we swap languages, the needed stems will
                        always be stored in stem file #1.
                    '''
                    stemnos = objs.get_files().get_stems1().search(stem,end)
                    if stemnos:
                        mes = _('Found stem: "{}"').format(stem)
                        sh.objs.get_mes(f,mes,True).show_info()
                        word_stems += stemnos
                        ''' There can be several valid stems, e.g.,
                            'absolute' and 'absolut' (test on
                            'absolute measurements'). Since finding
                            valid stems significantly slows down
                            performance, we allow only 2 valid stems
                            of the same word.
                        '''
                        if len(word_stems) >= MAXSTEMS:
                            break
                    i -= 1
                self.stemnos.append(word_stems)
            self.stemnos = [item for item in self.stemnos if item]
            if DEBUG:
                sh.objs.get_mes(f,self.stemnos,True).show_debug()
        else:
            sh.com.cancel(f)
    
    def set_values(self):
        self.Success = True
        self.pattern = ''
        self.htm   = ''
        self.stemnos = []
    
    def search(self):
        f = '[MClient] plugins.multitranbin.get.Get.search'
        if self.Success:
            art_nos = []
            for combo in self.stemnos:
                art_no = objs.get_files().get_glue1().search(combo)
                if art_no:
                    art_nos += art_no
            if art_nos:
                mes = _('Found articles: {}').format(art_nos)
            else:
                mes = _('No articles have been found!')
            sh.objs.get_mes(f,mes,True).show_info()
            articles = []
            for art_no in art_nos:
                article = objs.get_files().get_article().search(art_no)
                if article:
                    articles.append(article)
            return articles
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.check()
        self.strip()
        objs.get_files().reset()
        self.get_stems()
        self.get_combos()
        self.set_speech()
        return self.search()


objs = Objects()
com  = Commands()
