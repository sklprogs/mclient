#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import mmap
import struct
import codecs
import itertools
import skl_shared.shared as sh
from skl_shared.localize import _

# Do not localize language names here
ENCODING = 'windows-1251'
LANG1    = 'English'
LANG2    = 'Russian'
PATH     = ''


class Binary:
    
    def __init__(self,file):
        self.fsize   = 0
        self.bsize   = 0
        self.file    = file
        self.bname   = sh.Path(file).basename()
        self.Success = sh.File(self.file).Success
        self.open()
    
    def get_file_size(self):
        ''' This should be equal to 'sh.File(self.vfile).size()'.
            #NOTE: size = max_pos + 1
        '''
        f = '[MClient] plugins.multitranbin.get.Binary.get_file_size'
        if self.Success:
            if not self.fsize:
                self.fsize = sh.File(self.file).size()
                mes  = _('File "{}" has the size of {}')
                size = sh.com.human_size(self.fsize)
                mes  = mes.format(self.file,size)
                sh.objs.mes(f,mes,True).debug()
            if not self.fsize:
                self.Success = False
                mes = _('Empty output is not allowed!')
                sh.objs.mes(f,mes).warning()
        else:
            sh.com.cancel(f)
        return self.fsize
    
    def get_page_limits(self,page_no):
        f = '[MClient] plugins.multitranbin.get.Binary.get_page_limits'
        if self.Success:
            if page_no is None or not self.get_block_size():
                sh.com.empty(f)
            elif page_no == 0:
                sub = sh.com.human_size(self.bsize)
                mes = _('Page size: {}').format(sub)
                sh.objs.mes(f,mes,True).debug()
                pos1 = 0
                pos2 = self.bsize
                sub  = sh.com.figure_commas(pos2)
                mes  = _('Page limits: [{}:{}]')
                mes  = mes.format(pos1,sub)
                sh.objs.mes(f,mes,True).debug()
                return(0,self.bsize)
            else:
                pos = page_no * self.bsize
                read = self.read(pos+1,pos+3)
                if read:
                    if len(read) == 2:
                        size = struct.unpack('<h',read)[0]
                        if size > 0:
                            sub = sh.com.human_size(size)
                            mes = _('Page size: {}').format(sub)
                            sh.objs.mes(f,mes,True).debug()
                            pos1 = pos + 3
                            pos2 = pos1 + size
                            sub1 = sh.com.figure_commas(pos1)
                            sub2 = sh.com.figure_commas(pos2)
                            mes  = _('Page limits: [{}:{}]')
                            mes  = mes.format(sub1,sub2)
                            sh.objs.mes(f,mes,True).debug()
                            return(pos1,pos2)
                        else:
                            sub = '{} > 0'.format(size)
                            mes = _('The condition "{}" is not observed!')
                            mes = mes.format(sub)
                            sh.objs.mes(f,mes,True).warning()
                    else:
                        sub = '{} == 2'.format(len(read))
                        mes = _('The condition "{}" is not observed!')
                        mes = mes.format(sub)
                        sh.objs.mes(f,mes,True).warning()
                else:
                    sh.com.empty(f)
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
                        mes = _('Third-party module has failed!\n\nDetails: {}')
                        mes = mes.format(e)
                        sh.objs.mes(f,mes,True).warning()
                    mes = sh.com.figure_commas(self.bsize)
                    sh.objs.mes(f,mes,True).debug()
                else:
                    self.Success = False
                    sh.com.empty(f)
        else:
            sh.com.cancel(f)
        return self.bsize
    
    def check_lengths(self,pattern,lengths):
        f = '[MClient] plugins.multitranbin.get.Binary.check_lengths'
        if self.Success:
            if lengths:
                if lengths[0] == len(pattern) and lengths[1] > 0:
                    return True
                else:
                    mes = _('The check has failed!')
                    sh.objs.mes(f,mes,True).warning()
            else:
                sh.com.empty(f)
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
                sh.com.lazy(f)
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
            elif 0 <= start < end <= self.get_file_size():
                self.imap.seek(start)
                chunk = self.imap.read(end-start)
                mes = '"{}"'.format(com.get_string(chunk))
                sh.objs.mes(f,mes,True).debug()
                return chunk
            else:
                self.Success = False
                sub1 = sh.com.figure_commas(start)
                sub2 = sh.com.figure_commas(end)
                sub3 = sh.com.figure_commas(self.fsize)
                sub = '0 <= {} < {} <= {}'.format(sub1,sub2,sub3)
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                sh.objs.mes(f,mes).warning()
        else:
            sh.com.cancel(f)
    
    def find(self,pattern,start=0,end=0):
        f = '[MClient] plugins.multitranbin.get.Binary.find'
        if self.Success:
            if pattern:
                if not end:
                    # Search to the end
                    end = -1
                result = self.imap.find(pattern,start,end)
                if end == -1:
                    mes = '{}, "{}" => {}'
                    mes = mes.format (self.bname
                                     ,com.get_string(pattern)
                                     ,sh.com.figure_commas(result)
                                     )
                else:
                    mes = '{}, [{}:{}], "{}" => {}'
                    mes = mes.format (self.bname
                                     ,sh.com.figure_commas(start)
                                     ,sh.com.figure_commas(end)
                                     ,com.get_string(pattern)
                                     ,sh.com.figure_commas(result)
                                     )
                sh.objs.mes(f,mes,True).debug()
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
            sh.objs.mes(f,mes).error()
            return -1
    
    def _get_ref(self,i):
        f = '[MClient] plugins.multitranbin.get.UPage._get_ref'
        if i is None:
            sh.com.empty(f)
        else:
            try:
                page_ref = struct.unpack('<h',self.part2[i])[0]
                mes = _('#{}: {}').format(i,page_ref)
                sh.objs.mes(f,mes,True).debug()
                return page_ref
            except IndexError:
                mes = _('Wrong input data!')
                sh.objs.mes(f,mes).error()
    
    def _decode(self,pattern):
        if self.file in (objs.files().iwalker.get_stems1()
                        ,objs._files.iwalker.get_stems2()
                        ):
            result = pattern.decode(ENCODING,'replace')
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
        sh.objs.mes(f,mes,True).debug()
    
    def searchu(self,pattern):
        f = '[MClient] plugins.multitranbin.get.UPage.searchu'
        if self.Success:
            self.get_parts()
            if pattern and self.part1:
                i = 1
                while i < len(self.part1):
                    if self.part1[i-1] <= pattern < self.part1[i]:
                        break
                    i += 1
                i -= 1
                #TODO: Comment this to speed up
                self._log(pattern,i)
                return self.get_page_limits(self._get_ref(i))
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
        
    
    def report_status(self,pos):
        f = '[MClient] plugins.multitranbin.get.UPage.report_status'
        if self.Success:
            mes = _('{}/{} bytes have been processed')
            mes = mes.format(pos,len(self.page))
            sh.objs.mes(f,mes,True).info()
            remains = self.page[pos:len(self.page)]
            remains = com.get_string(remains)
            mes = _('Unprocessed fragment: "{}"').format(remains)
            sh.objs.mes(f,mes,True).debug()
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
                        len1 = com.overflow(len1)
                        len2 = com.overflow(len2)
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
                            self.report_status(pos)
                            if len(self.page) - pos > 1:
                                mes = _('Processing the pattern has not been completed, but the end of the file has already been reached!')
                                sh.objs.mes(f,mes,True).warning()
                            break
                    self.conform_parts()
                else:
                    sh.com.empty(f)
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
                        sh.com.empty(f)
                    else:
                        self.page = page
                else:
                    sh.com.empty(f)
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
                    sh.com.empty(f)
        else:
            sh.com.cancel(f)
        return self.psize
    
    def conform_parts(self):
        f = '[MClient] plugins.multitranbin.get.UPage.conform_parts'
        if self.Success:
            if self.part1:
                if len(self.part1) == len(self.part2):
                    self.part1.insert(0,b'')
                    max_ = struct.unpack('<h',max(self.part2))[0]
                    try:
                        add_bytes = struct.pack('<h',max_+1)
                    except:
                        add_bytes = max(self.part2)
                    self.part2.append(add_bytes)
                else:
                    self.Success = False
                    sub = '{} == {}'.format (len(self.part1)
                                            ,len(self.part2)
                                            )
                    mes = _('The condition "{}" is not observed!')
                    mes = mes.format(sub)
                    sh.objs.mes(f,mes).error()
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)



class Walker:
    def __init__(self):
        self.values()
        if PATH:
            self.reset()
    
    def get_typein1(self):
        f = '[MClient] plugins.multitranbin.get.Walker.get_typein1'
        if self.Success:
            if not self.typein1:
                fname = 'typein.' + self.lang11 + self.lang21
                file  = self.get_file(fname)
                if file:
                    self.typein1 = file
                    sh.objs.mes(f,self.typein1,True).debug()
                else:
                    self.Success = False
                    mes = _('File "{}" does not exist!').format(fname)
                    sh.objs.mes(f,mes,True).warning()
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
                    sh.objs.mes(f,self.typein2,True).debug()
                else:
                    self.Success = False
                    mes = _('File "{}" does not exist!').format(fname)
                    sh.objs.mes(f,mes,True).warning()
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
                    sh.objs.mes(f,self.article,True).debug()
                else:
                    self.Success = False
                    mes = _('File "{}" does not exist!').format(fname)
                    sh.objs.mes(f,mes,True).warning()
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
                    sh.objs.mes(f,self.glue1,True).debug()
                else:
                    self.Success = False
                    mes = _('File "{}" does not exist!').format(fname)
                    sh.objs.mes(f,mes,True).warning()
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
                    sh.objs.mes(f,self.glue2,True).debug()
                else:
                    self.Success = False
                    mes = _('File "{}" does not exist!').format(fname)
                    sh.objs.mes(f,mes,True).warning()
        else:
            sh.com.cancel(f)
        return self.glue2
    
    def reset(self):
        self.values()
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
            sh.com.empty(f)
    
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
                    sh.objs.mes(f,mes,True).warning()
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
                    sh.objs.mes(f,mes,True).warning()
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
                sh.objs.mes(f,mes,True).warning()
        else:
            sh.com.cancel(f)
    
    def values(self):
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



class TypeIn(Binary):
    # Parse files like 'typein.er'
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    
    def parse(self,chunk):
        f = '[MClient] plugins.multitranbin.get.TypeIn.parse'
        if self.Success:
            if chunk:
                pass
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def search(self,coded):
        # Do not fail the whole class upon a failed search
        f = '[MClient] plugins.multitranbin.get.TypeIn.search'
        if self.Success:
            if coded:
                chunk = self.get_part2(coded)
                return self.parse(chunk)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)



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
                sh.com.empty(f)
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
                    sh.com.empty(f)
            else:
                sh.com.empty(f)
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
                        sh.com.lazy(f)
                else:
                    sh.com.empty(f)
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
    
    def overflow(self,no):
        f = '[MClient] plugins.multitranbin.get.Commands.overflow'
        if no < 0:
            ''' Byte format requires -128 <= no <= 127, so it looks
                like, when a page size value is negative, it has just
                overflown the minimum negative -128, e.g., -106 actually
                means 150: 128 - 106 = 22 => 127 + 22 + 1 = 150.
            '''
            new = 256 - abs(no)
            mes = '{} -> {}'.format(no,new)
            sh.objs.mes(f,mes,True).debug()
            return new
        else:
            return no
    
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


class Files:
    
    def __init__(self):
        self.reset()
    
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
        self.values()
        self.iwalker = Walker()
        self.Success = self.iwalker.Success
    
    def values(self):
        self.iwalker = None
        self.Success = False
        self.typein1 = None
        self.typein2 = None
        self.stems1  = None
        self.stems2  = None
        self.glue1   = None
        self.glue2   = None
        self.article = None



class Objects:
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self._all_dics = self._files = None
    
    def files(self):
        if self._files is None:
            self._files = Files()
            self._files.open()
        return self._files
    
    def all_dics(self):
        if self._all_dics is None:
            self._all_dics = AllDics()
        return self._all_dics



class Stems(UPage):
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
                    tmp = [sh.com.figure_commas(no) for no in nos]
                    sh.objs.mes(f,tmp,True).debug()
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
        # Do not fail the whole class upon a failed search
        f = '[MClient] plugins.multitranbin.get.Stems.search'
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
                    sh.com.empty(f)
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
            self.stemnos = list(itertools.product(*self.stemnos))
            #FIX: MemoryError
            #sh.objs.mes(f,self.stemnos,True).debug()
            self.stemnos = [b''.join(item) for item in self.stemnos]
            #FIX: MemoryError
            #sh.objs.mes(f,self.stemnos,True).debug()
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
                    #NOTE: nltk: according -> accord -> No matches!
                    stem = word[0:i]
                    mes = _('Try for "{}"').format(stem)
                    sh.objs.mes(f,mes,True).info()
                    coded = bytes(stem,ENCODING,'ignore')
                    ''' Since we swap languages, the needed stems will
                        always be stored in stem file #1.
                    '''
                    stem_nos = objs.files().get_stems1().search(coded)
                    if stem_nos:
                        mes = _('Found stem: "{}"').format(stem)
                        sh.objs.mes(f,mes,True).info()
                        all_stems += stem_nos
                        ''' #NOTE: A stem form of 'absolute' can be
                            either 'absolute' or 'absolut' (both forms
                            are stored in 'stems.eng'), so we
                            should NOT break here.
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
                art_no = objs.files().get_glue1().search(combo)
                if art_no:
                    art_nos += art_no
            if art_nos:
                mes = _('Found combinations: {}').format(art_nos)
            else:
                mes = _('No stem combinations have been found!')
            sh.objs.mes(f,mes,True).info()
            articles = []
            for art_no in art_nos:
                article = objs.files().get_article().search(art_no)
                if article:
                    articles.append(article)
            return articles
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.check()
        self.strip()
        objs.files().reset()
        self.get_stems()
        self.combos()
        return self.search()


objs = Objects()
com  = Commands()
