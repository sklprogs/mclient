#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import struct
import os
import gzip
import zlib

import shared    as sh
import sharedGUI as sg

import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')


class DictZip:
    # Based on https://github.com/cz7asm/pyStarDictViewer
    # Read archives in '.dict.dz' format
    def __init__(self,path=''):
        if path:
            self.reset(path)
    
    def values(self):
        self.obj      = None
        self.Success  = True
        self.deflate  = zlib.decompressobj(-15)
        self._path    = ''
        self._len     = 0
        self._size    = 0
        self._offset  = 0
        self._offsets = 0
        self._count   = 0
    
    def reset(self,path):
        self.values()
        self._path   = path
        self.Success = sh.File(self._path).Success
        self.load()
    
    def load(self):
        f = '[MClient] stardict.DictZip.load'
        if self.Success:
            try:
                self.obj      = open(self._path,'rb')
                info          = self._read_header()
                self._len     = info[0]
                self._size    = info[1]
                self._offsets = info[2]
                self._count   = len(self._size)
            except Exception as e:
                self.Success = False
                sh.objs.mes (f,_('WARNING')
                            ,_('Failed to load "%s"!\n\nDetails: %s') \
                            % (str(self._path),str(e))
                            )
        else:
            sh.com.cancel(f)

    def _read_header(self):
        # This method is internal and should be wrapped with try-except
        self.obj.seek(0)
        # Check header parameters
        header = self.obj.read(10)
        #todo: fail on error
        if header[:2] != b'\x1f\x8b':
            message = _('GZIP signature is expected, but found "%s"!') \
                      % str(header[:2])
            raise ValueError(message)
        if header[2] != 8:
            raise ValueError(_('Only DEFLATE archives are supported!'))
        flags = header[3]
        if not flags&(1<<2):
            raise ValueError(_('An extra dictzip field is expected!'))
        # Read dictzip data
        XLEN, SI1, SI2, LEN = struct.unpack('<H2cH',self.obj.read(6))
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

    def seek(self,offset):
        # This is only to provide a file-like interface
        self._offset = offset

    def read(self,size):
        ''' - Determines which chunk to read and decompress.
            - It's possible that data overrun to the following chunk
              so this must be handled too.
            - Do not rename this function since 'read' can be called
              on a different class.
        '''
        f = '[MClient] stardict.DictZip.read'
        if self.Success:
            # Prevent 'ZeroDivisionError'
            if self._len:
                chunk = self._offset // self._len
                self.obj.seek(self._offsets[chunk])
                compr = self.obj.read(self._size[chunk])
                data  = self.deflate.decompress(compr)
                # Offset in the chunk
                chofs = self._offset % self._len
                if chofs + size > self._len:
                    # Data continue in the next chunk
                    out = data[chofs:]
                    self.seek(self._offset+len(out))
                    out += self.read(size-len(out))
                else:
                    # All in the current chunk
                    out = data[chofs:chofs+size]
                return out
            else:
                # You've probably forgot to run 'self.load' first
                sh.com.empty(f)
        else:
            sh.com.cancel(f)

    def close(self):
        f = '[MClient] stardict.DictZip.close'
        if self.Success:
            self.obj.close()
        else:
            sh.com.cancel(f)



class StarDict:
    # Based on https://github.com/cz7asm/pyStarDictViewer
    def __init__(self,ifopath=''):
        if ifopath:
            self.reset(ifopath)
    
    def reset(self,ifopath):
        self.values()
        self._path = ifopath
        ipath      = sh.Path(self._path)
        ''' We need a filename with an absolute path here.
            'file'[:-4] basically does the same thing (providing that
            extensions are only 3 symbols long). 'sh.Path' is more
            precise for other cases.
        '''
        self._fname  = os.path.join(ipath.dirname(),ipath.filename())
        self.Success = sh.File(self._path).Success
        self.check()
        self.meta()

    def values(self):
        self.Success = True
        self.Block   = False
        self.dictf   = None
        self._idx    = []
        self._ifo    = {}
        self._wcount = 0
        self._path   = ''
        self._fname  = ''
        self._title  = ''
        self._transl = ''
    
    def meta(self):
        f = '[MClient] stardict.Stardict.meta'
        if self.Success:
            if self._ifo:
                if 'bookname' in self._ifo and 'wordcount' in self._ifo:
                    self._title  = str(self._ifo['bookname'])
                    self._wcount = sh.Input (title = f
                                            ,value = self._ifo['wordcount']
                                            ).integer()
                else:
                    self.Success = False
                    sh.objs.mes (f,_('WARNING')
                                ,_('File "%s" is incorrect!') \
                                % (self._fname + '.ifo')
                                )
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def fail(self,f,e):
        self.Success = False
        sh.objs.mes (f,_('WARNING')
                    ,_('Failed to load "%s"!\n\nDetails: %s') \
                    % (str(self._path),str(e))
                    )
    
    def check(self):
        ''' Load .ifo data and check that all needed dictionary files
            are present.
        '''
        f = '[MClient] stardict.Stardict.check'
        if self.Success:
            try:
                for line in open(self._fname+'.ifo').readlines()[1:]:
                    pair = line.split('=')
                    self._ifo[pair[0]] = pair[1][:-1]

                if (not os.path.exists(self._fname+'.idx')):
                    raise ValueError('An .idx file is missing!')

                if (not os.path.exists(self._fname+'.dict') and
                    not os.path.exists(self._fname+'.dict.dz')):
                    raise ValueError('A .dict file is missing!')
            except Exception as e:
                self.fail(f,e)
        else:
            sh.com.cancel(f)
    
    def load(self):
        ''' Build a list of (word, (dict_index, length)) tuples
            from .idx and open .dict[.dz] file for reading.
        '''
        f = '[MClient] stardict.Stardict.load'
        if self.Success:
            idx   = self._fname + '.idx'
            iopen = open(idx,'rb')
            data  = iopen.read(os.path.getsize(idx))
            iopen.close()
            a = 0
            b = data.find(b'\0',a)
            while b > 0:
                try:
                    bts = data[a:b].decode('utf-8')
                except UnicodeDecodeError as e:
                    print('type of data:',type(data))
                    self.Success = False
                self._idx.append ((bts,
                                   struct.unpack('>LL',data[b+1:b+9])
                                 ))
                a = b + 9
                b = data.find(b'\0',a)
            if self._wcount != len(self._idx):
                self.Success = False
                sh.objs.mes (f,_('ERROR')
                            ,_('The condition "%s" is not observed!') \
                            % ('%d = %d') % (self._wcount,len(self._idx)
                                            )
                            )
            if self.Success:
                # Compression of .dict is optional
                try:
                    self.dictf = open(self._fname+'.dict','rb')
                except IOError:
                    self.dictf = DictZip(self._fname+'.dict.dz') 
            else:
                sh.com.cancel(f)
        else:
            sh.com.cancel(f)

    def unload(self):
        # Release idx word list and opened .dict file
        f = '[MClient] stardict.Stardict.unload'
        if self.Success:
            self._idx = []
            self.dictf.close()
        else:
            sh.com.cancel(f)

    def __len__(self):
        return len(self._idx)

    def __getitem__(self,key):
        ''' int and slice return coresponding words string key is used
            for reverse lookup.
        '''
        f = '[MClient] stardict.Stardict.__getitem__'
        if self.Success:
            if type(key) is int:
                return self._idx[key][0]
            if type(key) is slice:
                return [w[0] for w in self._idx[key]]
            if type(key) is str:
                return sh.Input (title = f
                                ,value = self.search(key)
                                ).integer()
        else:
            sh.com.cancel(f)

    def search(self,word,prefix=False):
        ''' Binary search for words in idx list. In case prefix=True,
            the search will be performed for the lowest record
            with 'word' as its prefix.
        '''
        f = '[MClient] stardict.Stardict.search'
        if self.Success:
            if word == '':
                return -1
            a, b = 0, len(self._idx) - 1
            if (b < 0):
                 return -1
            word = word.lower()
            while a <= b:                
                i = a + (b - a) // 2
                if prefix:
                    # Search words that include 'word' in their prefix
                    if self._idx[i][0].lower().startswith(word):
                        if i and self._idx[i-1][0].lower().startswith(word):
                            b = i - 1
                            continue
                        else:
                            return i
                else:
                    # Search for the entire match
                    if self._idx[i][0].lower() == word:
                        return i
                if a == b:
                    # No match
                    return -1
                elif word > self._idx[i][0].lower():
                    # Move upward
                    a = i + 1
                else:
                    # Move downward
                    b = i - 1
            return -1
        else:
            sh.com.cancel(f)
    
    def dict_link(self,index):
        f = '[MClient] stardict.Stardict.dict_link'
        if self.Success:
            # Return (dict_index, len) tuple of a word on a given index
            return self._idx[index][1]
        else:
            sh.com.cancel(f)

    def dict_data(self,index):
        f = '[MClient] stardict.Stardict.dict_link'
        if self.Success:
            # Return a translation for a word on the given index
            if self.dictf:
                self.dictf.seek(self._idx[index][1][0])
                result = self.dictf.read(self._idx[index][1][1])
                if result:
                    return result.decode()
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)

    def __str__(self):
        return str(self._ifo)



class AllDics:
    
    def __init__(self,path=''):
        self.values()
        if path:
            self.reset(path)
    
    def get(self,search=''):
        f = '[MClient] stardict.AllDics.get'
        if self.Success:
            if search:
                dics = [dic for dic in self._dics if not dic.Block]
                lst  = []
                for dic in dics:
                    ind = dic.search(search,True)
                    # Returns True if ind >= 0
                    if str(ind).isdigit():
                        result = dic.dict_data(ind)
                        if result:
                            # Set offline dictionary title
                            lst.append ('<a title="' + dic._title \
                                                     + '">' + result \
                                                     + '</a>'
                                       )
                    else:
                        sh.com.empty(f)
                return '\n'.join(lst)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def values(self):
        self._ifos   = []
        self._dics   = []
        self._path   = ''
        # Do not run anything if 'self.reset' was not run
        self.Success = False
    
    def reset(self,path):
        self.values()
        self._path   = path
        self.Success = sh.Directory(self._path).Success
    
    def walk(self):
        ''' Explore all subdirectories of path searching for filenames
            that have all three .ifo, .idx and .dict[.dz] suffixes.
        '''
        f = '[MClient] stardict.AllDics.walk'
        if self.Success:
            if not self._ifos:
                for root, dirs, files in os.walk(self._path):
                    for file in files:
                        if not file.endswith('.ifo'):
                            continue
                        ''' #todo: #fix: sh.Path.basename works
                            incorrectly for cases like file.dict.dz.
                        '''
                        name = file[:-4]
                        if (name+'.idx' in files and (name+'.dict.dz' in files
                                                      or name+'.dict' in files
                                                     )
                           ):
                               self._ifos.append(os.path.join(root,name+'.ifo'))
            return self._ifos
        else:
            sh.com.cancel(f)
    
    def locate(self):
        f = '[MClient] stardict.AllDics.locate'
        if self.Success:
            if not self._dics:
                if self.walk():
                    for ifo in self._ifos:
                        self._dics.append(StarDict(ifo))
                    self._dics = sorted(self._dics,key=lambda d:d._title+str(d._wcount))
                else:
                    sh.com.empty(f)
            sh.log.append (f,_('INFO')
                          ,_('%d offline dictionaries are available') \
                          % len(self._dics)
                          )
            return self._dics
        else:
            sh.com.cancel(f)
    
    def load(self):
        f = '[MClient] stardict.AllDics.load'
        if self.Success:
            if self.locate():
                sh.log.append (f,_('INFO')
                              ,_('Load offline dictionaries')
                              )
                timer = sh.Timer(f)
                timer.start()
                for idic in self._dics:
                    idic.load()
                timer.end()
                total_no   = len(self._dics)
                self._dics = [dic for dic in self._dics if dic.Success]
                sh.log.append (f,_('INFO')
                              ,_('Dictionaries loaded: %d/%d') \
                              % (len(self._dics),total_no)
                              )
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)


if __name__ == '__main__':
    f = '[MClient] stardict.__main__'
    sg.objs.start()
    folder = '/home/pete/.config/mclient/dics/'
    search = 'компьютер'
    dics = AllDics(folder)
    sg.objs.waitbox().reset (func_title = f
                            ,message    = _('Load local dictionaries')
                            )
    sg.objs._waitbox.show()
    dics.load()
    sg.objs._waitbox.close()
    sg.fast_txt(dics.get(search))
    sg.objs.end()
