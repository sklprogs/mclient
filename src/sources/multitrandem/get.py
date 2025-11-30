#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import mmap
import struct
import codecs
import locale
import itertools
from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.basic_text import Shorten
from skl_shared.text_file import Read
from skl_shared.logic import Text, Input, com as shcom
from skl_shared.paths import Home, Path, File, Directory
from skl_shared.table import Table

from config import CONFIG
# Do not localize language names here
CODING = 'windows-1251'
MAXSTEMS = 2
DEBUG = False


class Language:
    
    def __init__(self):
        ''' #NOTE: Change this if number of languages supported by binary
            Multitran changes.
        '''
        self.langint = ('English', 'Russian', 'German', 'Spanish', 'French'
                       ,'Italian', 'Dutch', 'Latvian', 'Estonian')
        self.langloc = (_('English'), _('Russian'), _('German'), _('Spanish')
                       ,_('French'), _('Italian'), _('Dutch'), _('Latvian')
                       ,_('Estonian'))
    
    def _adapt(self, lang):
        f = '[MClient] sources.multitrandem.run.Source._adapt'
        if not lang:
            rep.empty(f)
            return 'English'
        if lang in self.langloc:
            ind = self.langloc.index(lang)
            return self.langint[ind]
        elif lang in self.langint:
            ind = self.langint.index(lang)
            return self.langloc[ind]
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            modes = self.langloc + self.langint
            mes = mes.format(lang, ';'.join(modes))
            Message(f, mes, True).show_error()
        return 'English'
    
    def get_lang1(self):
        return self._adapt(CONFIG.new['lang1'])
    
    def get_lang2(self):
        return self._adapt(CONFIG.new['lang2'])



class Ending:
    # Parse files like 'sik.eng'
    def __init__(self, file):
        self.set_values()
        self.file = file
        self.load()
        self.parse()
    
    def overflow(self, no):
        f = '[MClient] sources.multitrandem.get.Ending.overflow'
        new = no
        if not self.Success:
            rep.cancel(f)
            return new
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
                mes = f'{no} -> {new}'
                Message(f, mes).show_debug()
        return new
    
    def has_match(self, no, pattern):
        f = '[MClient] sources.multitrandem.get.Ending.has_match'
        if not self.Success:
            rep.cancel(f)
            return
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
            match = pattern in self.ends[index_]
            if match:
                sub = _('Yes')
            else:
                sub = _('No')
            if DEBUG:
                mes = _('#: {}; Pattern: "{}"; Match: {}')
                mes = mes.format(no, pattern, sub)
                Message(f, mes).show_debug()
            return match
        except ValueError:
            mes = _('Wrong input data: "{}"!').format(no)
            Message(f, mes).show_warning()
    
    def load(self):
        f = '[MClient] sources.multitrandem.get.Ending.load'
        if not self.Success:
            rep.cancel(f)
            return
        self.text = Read(self.file).get()
        if not self.text:
            self.Success = False
            mes = _('Empty output is not allowed!')
            Message(f, mes).show_warning()
    
    def parse(self):
        f = '[MClient] sources.multitrandem.get.Ending.parse'
        if not self.Success:
            rep.cancel(f)
            return
        lines = self.text.splitlines()
        lines = [line for line in lines if line]
        if len(lines) <= 1:
            sub = f'{len(lines)} > 1'
            mes = _('The condition "{}" is not observed!').format(sub)
            Message(f, mes).show_warning()
            return
        if lines[0] == 'SIK PORTION':
            lines = lines[1:]
        for i in range(len(lines)):
            line = lines[i].strip()
            line = Text(line).delete_duplicate_spaces()
            # Remove comments
            line = line.split(';')[0]
            # Empty input means the entire line is a comment
            if not line:
                continue
            if len(line) < 2:
                mes = _('Wrong input data: "{}"!').format(line)
                Message(f, mes).show_warning()
                continue
            # Remove a gender separator
            line = line.replace('/', ' ')
            line = line.replace(',', ' ')
            line = line.split(' ')
            line = [item for item in line if item]
            no = Input(title=f, value=line[0]).get_integer()
            ends = line[1:]
            self.nos.append(no)
            self.ends.append(ends)
        self.ordered = sorted(set(self.nos))
    
    def set_values(self):
        self.file = ''
        self.text = ''
        self.Success = True
        self.nos = []
        self.ends = []
        self.ordered = []



class Subject:
    # Parse files like 'SUBJECTS.TXT'
    def __init__(self, file):
        f = '[MClient] sources.multitrandem.get.Subject.__init__'
        self.set_values()
        self.file = file
        self.get_locale()
        # Suppress useless error output
        if FILES.iwalker.Success:
            self.load()
            self.parse()
        else:
            rep.lazy(f)
    
    def get_pair(self, code):
        f = '[MClient] sources.multitrandem.get.Subject.get_pair'
        if not self.Success:
            rep.cancel(f)
            return
        if not code in self.dic_nos:
            mes = _('Wrong input data: "{}"!').format(code)
            Message(f, mes).show_warning()
            return
        ind = self.dic_nos.index(code)
        if self.lang == 'ru':
            pair = (self.ru_dic[ind], self.ru_dicf[ind])
        else:
            pair = (self.en_dic[ind], self.en_dicf[ind])
        mes = f'{code} -> {pair}'
        Message(f, mes).show_debug()
        return pair
    
    def get_locale(self):
        f = '[MClient] sources.multitrandem.get.Subject.get_locale'
        if not self.Success:
            rep.cancel(f)
            return
        info = locale.getdefaultlocale()
        # 'en' is set in 'set_values' by default
        if info and info[0] in ('ru_RU', 'ru_UA'):
            self.lang = 'ru'
    
    def set_values(self):
        self.Success = True
        self.file = ''
        self.text = ''
        self.dic_nos = []
        self.en_dicf = []
        self.ru_dicf = []
        self.en_dic = []
        self.ru_dic = []
        self.lang = 'en'
    
    def parse(self):
        f = '[MClient] sources.multitrandem.get.Subject.parse'
        if not self.Success:
            rep.cancel(f)
            return
        lst = self.text.splitlines()
        # This should not be needed. We do that just to be safe.
        lst = [item for item in lst if item]
        for line in lst:
            items = line.split(';')
            # Delete comments (which also start with ';')
            items = items[0:5]
            # Fail if items < 5
            if len(items) != 5:
                self.Success = False
                mes = _('Wrong input data: "{}"!').format(line)
                Message(f, mes, True).show_warning()
                break
            dic_no = Input(f, items[0]).get_integer()
            self.dic_nos.append(dic_no)
            self.en_dicf.append(items[1])
            self.en_dic.append(items[2])
            self.ru_dicf.append(items[3])
            self.ru_dic.append(items[4])
    
    def load(self):
        f = '[MClient] sources.multitrandem.get.Subject.load'
        if not self.Success:
            rep.cancel(f)
            return
        # We need silent logging here
        if not os.path.exists(self.file):
            self.Success = False
            mes = _('File "{}" does not exist!').format(self.file)
            Message(f, mes).show_warning()
            return
        iread = Read(self.file)
        iread._read(CODING)
        self.text = iread.get()
        if not self.text:
            self.Success = False
            mes = _('Empty output is not allowed!')
            Message(f, mes, True).show_warning()



class Binary:
    
    def __init__(self, file):
        self.fsize = 0
        self.bsize = 0
        self.file = file
        self.fname = Path(file).get_filename()
        # We need silent logging here (not 'File.Success')
        self.Success = os.path.exists(self.file)
        self.open()
    
    def get_zero(self, start, end):
        f = '[MClient] sources.multitrandem.get.Binary.get_zero'
        if not self.Success:
            rep.cancel(f)
            return []
        result = []
        pos = self.find(b'\x00', start, end)
        if pos:
            #TODO (?): implement finding multiple zero chunks
            result = [pos+2]
        return result
    
    def get_parts2(self, pattern, start=0, end=0):
        # Run 'get_part2' in loop (only useful for finding stems)
        f = '[MClient] sources.multitrandem.get.Binary.get_parts2'
        chunks = []
        if DEBUG:
            mchunks = []
            mpos1 = []
            mpos2 = []
        if not self.Success:
            rep.lazy(f)
            return chunks
        if pattern == b'':
            poses = self.get_zero(start, end)
        else:
            poses = self.find_all(pattern, start, end)
        for pos11 in poses:
            lengths = self.get_lengths(pos11)
            if not self.check_lengths(pattern, lengths):
                continue
            pos21 = pos11 + lengths[0]
            pos22 = pos21 + lengths[1]
            chunk = self.read(pos21, pos22)
            if not chunk or chunk in chunks:
                continue
            chunks.append(chunk)
            if DEBUG:
                mpos1.append(shcom.set_figure_commas(pos21))
                mpos2.append(shcom.set_figure_commas(pos22))
                mchunks.append(com.get_string(chunk))
        if not DEBUG:
            return chunks
        if not mchunks:
            mes = _('No debug info')
            Message(f, mes).show_debug()
            return chunks
            mpattern = [f'"{com.get_string(pattern)}"' for i in range(len(mchunks))]
            mstart = [f'{shcom.set_figure_commas(start)}' for i in range(len(mchunks))]
            mend = [f'{shcom.set_figure_commas(end)}' for i in range(len(mchunks))]
            nos = [i + 1 for i in range(len(chunks))]
            mchunks = [f'"{chunk}"' for chunk in mchunks]
            headers = ('NO', 'PATTERN', 'START', 'END', 'POS1', 'POS2', 'CHUNK')
            iterable = (nos, mpattern, mstart, mend, mpos1, mpos2, mchunks)
            mes = Table(headers=headers, iterable=iterable, maxrow=47).run()
            mes = '\n\n' + mes
            Message(f, mes).show_debug()
        return chunks
    
    def get_parts1(self, pattern, start=0, end=0):
        # Get suggestions
        f = '[MClient] sources.multitrandem.get.Binary.get_parts1'
        chunks = []
        if DEBUG:
            mchunks = []
            mpos1 = []
            mpos2 = []
        if not self.Success:
            rep.lazy(f)
            return chunks
        if pattern:
            poses = self.find_all(pattern, start, end)
            for pos1 in poses:
                lengths = self.get_lengths(pos1)
                pos2 = pos1 + lengths[0]
                chunk = self.read(pos1, pos2)
                if not chunk or chunk in chunks:
                    continue
                chunks.append(chunk)
                if DEBUG:
                    mpos1.append(shcom.set_figure_commas(pos1))
                    mpos2.append(shcom.set_figure_commas(pos2))
                    mchunks.append(com.get_string(chunk))
        else:
            rep.empty(f)
        if not DEBUG:
            mes = _('No debug info')
            Message(f, mes).show_debug()
            return chunks
        if not mchunks:
            return chunks
        mpattern = [f'"{com.get_string(pattern)}"' for i in range(len(mchunks))]
        mstart = [f'{shcom.set_figure_commas(start)}' for i in range(len(mchunks))]
        mend = [f'{shcom.set_figure_commas(end)}' for i in range(len(mchunks))]
        nos = [i + 1 for i in range(len(chunks))]
        mchunks = [f'"{chunk}"' for chunk in mchunks]
        headers = ('NO', 'PATTERN', 'START', 'END', 'POS1', 'POS2', 'CHUNK')
        iterable = (nos, mpattern, mstart, mend, mpos1, mpos2, mchunks)
        mes = Table(headers=headers, iterable=iterable, maxrow=47).run()
        mes = '\n\n' + mes
        Message(f, mes).show_debug()
        return chunks
    
    def find_all(self, pattern, start=0, end=0):
        f = '[MClient] sources.multitrandem.get.Binary.find_all'
        matches = []
        if not self.Success:
            rep.cancel(f)
            return matches
        while True:
            start = self.find(pattern, start, end)
            if not start:
                break
            matches.append(start)
            start += 1
        if DEBUG:
            mes = [shcom.set_figure_commas(item) for item in matches]
            Message(f, mes).show_debug()
        return matches
    
    def get_page_limit(self):
        f = '[MClient] sources.multitrandem.get.Binary.get_page_limit'
        self.get_file_size()
        self.get_block_size()
        if not self.Success:
            rep.cancel(f)
            return
        val = self.fsize // self.bsize
        if DEBUG:
            mes = shcom.set_figure_commas(val)
            Message(f, mes).show_debug()
        return val
    
    def get_file_size(self):
        ''' This should be equal to 'File(self.vfile).get_size()'.
            #NOTE: size = max_pos + 1
        '''
        f = '[MClient] sources.multitrandem.get.Binary.get_file_size'
        if not self.Success:
            rep.cancel(f)
            return self.fsize
        if not self.fsize:
            self.fsize = File(self.file).get_size()
            if DEBUG:
                size = shcom.get_human_size(self.fsize)
                mes = _('File "{}" has the size of {}').format(self.file, size)
                Message(f, mes).show_debug()
        if not self.fsize:
            self.Success = False
            rep.empty_output(f)
        return self.fsize
    
    def get_page_limits(self, page_no):
        # Return positions of a page based on MT indicators
        f = '[MClient] sources.multitrandem.get.Binary.get_page_limits'
        if not self.Success:
            rep.cancel(f)
            return
        if page_no is None or not self.get_block_size():
            rep.empty(f)
            return
        if page_no == 0:
            if DEBUG:
                sub = shcom.get_human_size(self.bsize)
                mes = _('Page size: {}').format(sub)
                Message(f, mes).show_debug()
                pos1 = 0
                pos2 = self.bsize
                sub = shcom.set_figure_commas(pos2)
                mes = _('Page limits: [{}:{}]').format(pos1, sub)
                Message(f, mes).show_debug()
            return(0, self.bsize)
        pos = page_no * self.bsize
        read = self.read(pos + 1, pos + 3)
        if not read:
            rep.empty(f)
            return
        if len(read) != 2:
            sub = f'{len(read)} == 2'
            mes = _('The condition "{}" is not observed!').format(sub)
            Message(f, mes).show_warning()
            return
        size = struct.unpack('<h', read)[0]
        size = com.overflowh(size)
        if size <= 0:
            sub = f'{size} > 0'
            mes = _('The condition "{}" is not observed!').format(sub)
            Message(f, mes).show_warning()
            return
        if DEBUG:
            sub = shcom.get_human_size(size)
            mes = _('Page size: {}').format(sub)
            Message(f, mes).show_debug()
        pos1 = pos + 3
        pos2 = pos1 + size
        if DEBUG:
            sub1 = shcom.set_figure_commas(pos1)
            sub2 = shcom.set_figure_commas(pos2)
            mes = _('Page limits: [{}:{}]').format(sub1, sub2)
            Message(f, mes).show_debug()
        return(pos1, pos2)
    
    def get_block_size(self):
        f = '[MClient] sources.multitrandem.get.Binary.get_block_size'
        if not self.Success:
            rep.cancel(f)
            return self.bsize
        if self.bsize:
            return self.bsize
        read = self.read(28, 30)
        if not read:
            self.Success = False
            rep.empty(f)
            return self.bsize
        try:
            self.bsize = struct.unpack('<h', read)[0]
        except Exception as e:
            self.Success = False
            mes = _('Third-party module has failed!\n\nDetails: {}').format(e)
            Message(f, mes).show_warning()
        if DEBUG:
            mes = shcom.set_figure_commas(self.bsize)
            Message(f, mes).show_debug()
        return self.bsize
    
    def check_lengths(self, pattern, lengths):
        f = '[MClient] sources.multitrandem.get.Binary.check_lengths'
        if not self.Success:
            rep.cancel(f)
            return
        if not lengths:
            rep.empty(f)
            return
        if lengths[0] == len(pattern) and lengths[1] > 0:
            return True
        if DEBUG:
            mes = _('The check has failed!')
            Message(f, mes).show_warning()
    
    def get_part2(self, pattern, start=0, end=0):
        f = '[MClient] sources.multitrandem.get.Binary.get_part2'
        if not self.Success:
            rep.cancel(f)
            return
        pos11 = self.find(pattern, start, end)
        if pos11 is None:
            # We look for combinations of stems, so a mismatch is a common case
            if DEBUG:
                rep.lazy(f)
            return
        lengths = self.get_lengths(pos11)
        if self.check_lengths(pattern, lengths):
            pos21 = pos11 + lengths[0]
            pos22 = pos21 + lengths[1]
            return self.read(pos21, pos22)
    
    def get_lengths(self, index_):
        f = '[MClient] sources.multitrandem.get.Binary.get_lengths'
        if not self.Success:
            rep.cancel(f)
            return
        ''' There are 'M' pages at the beginning, so the index of the 1st part
            will always be positive.
        '''
        if index_ is None:
            rep.empty(f)
            return
        if index_ <= 2:
            sub = f'{index_} > 2'
            mes = _('The condition "{}" is not observed!').format(sub)
            Message(f, mes).show_warning()
            return
        pos1 = index_ - 2
        pos2 = index_ - 1
        len1 = self.read(pos1, pos1 + 1)
        len2 = self.read(pos2, pos2 + 1)
        if not len1 or not len2:
            rep.empty(f)
            return
        len1 = struct.unpack('<b', len1)[0]
        len2 = struct.unpack('<b', len2)[0]
        ''' The 2nd value of the index part can be negative (at least in demo,
            e.g., dict.ert: 723,957 -> b'\x03\x8a' -> (3; -118) -> (3; 138)).
        '''
        len1 = com.overflowb(len1)
        len2 = com.overflowb(len2)
        if DEBUG:
            mes = _('Part #{} length: {}').format(1, len1)
            Message(f, mes).show_debug()
            mes = _('Part #{} length: {}').format(2, len2)
            Message(f, mes).show_debug()
        return(len1, len2)
    
    def read(self, start, end):
        f = '[MClient] sources.multitrandem.get.Binary.read'
        if not self.Success:
            rep.cancel(f)
            return
        if start is None or end is None:
            rep.empty(f)
            return
        if not (0 <= start < end <= self.get_file_size()):
            self.Success = False
            sub1 = shcom.set_figure_commas(start)
            sub2 = shcom.set_figure_commas(end)
            sub3 = shcom.set_figure_commas(self.fsize)
            sub = f'0 <= {sub1} < {sub2} <= {sub3}'
            mes = _('The condition "{}" is not observed!').format(sub)
            Message(f, mes, True).show_warning()
            return
        self.imap.seek(start)
        chunk = self.imap.read(end-start)
        if DEBUG:
            mes = f'"{com.get_string(chunk)}"'
            Message(f, mes).show_debug()
        return chunk
    
    def find(self, pattern, start=0, end=0):
        f = '[MClient] sources.multitrandem.get.Binary.find'
        if not self.Success:
            rep.cancel(f)
            return
        if not pattern:
            rep.empty(f)
            return
        if not end:
            end = self.get_file_size()
        result = self.imap.find(pattern, start, end)
        if DEBUG:
            if end == -1:
                s_result = shcom.set_figure_commas(result)
                mes = f'{self.fname}, "{com.get_string(pattern)}" => {s_result}'
            else:
                s_start = shcom.set_figure_commas(start)
                s_end = shcom.set_figure_commas(end)
                s_pattern = com.get_string(pattern)
                s_result = shcom.set_figure_commas(result)
                mes = f'{self.fname}, [{s_start}:{s_end}], "{s_pattern}" => {s_result}'
            Message(f, mes).show_debug()
        if result >= 0:
            return result
    
    def open(self):
        f = '[MClient] sources.multitrandem.get.Binary.open'
        if not self.Success:
            rep.cancel(f)
            return
        mes = _('Open "{}"').format(self.file)
        Message(f, mes).show_info()
        self.bin = open(self.file, 'rb')
        # 'mmap' fails upon opening an empty file!
        try:
            self.imap = mmap.mmap(self.bin.fileno(), 0, access=mmap.ACCESS_READ)
        except Exception as e:
            self.Success = False
            mes = _('Third-party module has failed!\n\nDetails: {}').format(e)
            Message(f, mes).show_warning()
    
    def close(self):
        f = '[MClient] sources.multitrandem.get.Binary.close'
        if not self.Success:
            rep.cancel(f)
            return
        mes = _('Close "{}"').format(self.file)
        Message(f, mes).show_info()
        self.imap.flush()
        self.bin.close()



class UPage(Binary):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = b''
        self.pos1 = 0
        self.pos2 = 0
        self.psize = 0
        self.part1 = []
        self.part2 = []
    
    def _get_no(self, stem):
        f = '[MClient] sources.multitrandem.get.UPage._get_no'
        try:
            return self.part1.index(stem)
        except ValueError:
            mes = _('Wrong input data!')
            Message(f, mes, True).show_error()
            return -1
    
    def _get_ref(self, i):
        f = '[MClient] sources.multitrandem.get.UPage._get_ref'
        if i is None:
            rep.empty(f)
            return
        try:
            page_ref = struct.unpack('<h', self.part2[i])[0]
            if DEBUG:
                mes = _('#{}: {}').format(i, page_ref)
                Message(f, mes).show_debug()
            return page_ref
        except IndexError:
            mes = _('Wrong input data!')
            Message(f, mes, True).show_error()
    
    def _decode(self, pattern):
        if self.file in (FILES.iwalker.get_stems1()
                        ,FILES.iwalker.get_stems2()):
            result = pattern.decode(CODING, 'replace')
        else:
            result = com.get_string(pattern, 0)
        return f'"{result}"'
    
    def _log(self, pattern, i):
        f = '[MClient] sources.multitrandem.get.UPage._log'
        if self.part1[i] == pattern:
            oper = '<='
        else:
            oper = '<'
        if self.part1[i] == b'':
            stem1 = _('Start')
        else:
            stem1 = _('{} (#{})').format(self._decode(self.part1[i])
                                        ,self._get_no(self.part1[i]))
        if i + 1 < len(self.part1):
            stem2 = _('{} (#{})').format(self._decode(self.part1[i+1])
                                        ,self._get_no(self.part1[i+1]))
        else:
            stem2 = _('End')
        mes = f'{stem1} {oper} {self._decode(pattern)} < {stem2}'
        Message(f, mes).show_debug()
    
    def searchu(self, pattern):
        f = '[MClient] sources.multitrandem.get.UPage.searchu'
        if not self.Success:
            rep.cancel(f)
            return
        self.get_parts()
        if not self.part1:
            rep.empty(f)
            return
        i = 1
        while i < len(self.part1):
            if self.part1[i-1] <= pattern < self.part1[i]:
                break
            i += 1
        i -= 1
        if DEBUG:
            self._log(pattern, i)
        return self.get_page_limits(self._get_ref(i))
    
    def get_parts(self):
        f = '[MClient] sources.multitrandem.get.UPage.get_parts'
        if not self.Success:
            rep.cancel(f)
            return
        if self.part2:
            return
        if not self.get_page():
            rep.empty(f)
            return
        pos = 0
        while pos + 2 < len(self.page):
            # #NOTE: indexing returns integers, slicing returns bytes
            read = self.page[pos:pos+2]
            pos += 2
            len1, len2 = struct.unpack('<2b', read)
            len1 = com.overflowb(len1)
            len2 = com.overflowb(len2)
            if pos + len1 + len2 < len(self.page):
                ''' Do this only after checking the condition, otherwise,
                    resulting lists will have a different length.
                '''
                chunk1 = self.page[pos:pos+len1]
                pos += len1
                chunk2 = self.page[pos:pos+len2]
                pos += len2
                ''' #NOTE: Instructions for zero-length chunks should be
                    allowed - I encountered such and they were necessary to
                    parse the page correctly to the end. However, at least one
                    of the chunks should be non-empty, otherwise, checking
                    output will fail.
                '''
                if chunk1 or chunk2:
                    self.part1.append(chunk1)
                    self.part2.append(chunk2)
            else:
                com.report_status(pos, self.page)
                if len(self.page) - pos > 1:
                    mes = _('Processing the pattern has not been completed, but the end of the file has already been reached!')
                    Message(f, mes).show_warning()
                break
        self.conform_parts()
    
    def get_page(self):
        f = '[MClient] sources.multitrandem.get.UPage.get_page'
        if not self.Success:
            rep.cancel(f)
            return self.page
        if self.page:
            return self.page
        if not self.get_size():
            rep.empty(f)
            return self.page
        page = self.read(self.pos1, self.pos2)
        # Keep 'self.page' iterable
        if page is None:
            rep.empty(f)
            return self.page
        self.page = page
        return self.page
    
    def get_size(self):
        f = '[MClient] sources.multitrandem.get.UPage.get_size'
        if not self.Success:
            rep.cancel(f)
            return self.psize
        if self.psize:
            return self.psize
        ''' The 1st page is an area with M identifier.
            The 2nd page is an intermediate page with U identifier.
        '''
        poses = self.get_page_limits(1)
        if not poses:
            rep.empty(f)
            return self.psize
        self.pos1 = poses[0]
        self.pos2 = poses[1]
        self.psize = self.pos2 - self.pos1
        return self.psize
    
    def check_parts(self):
        f = '[MClient] sources.multitrandem.get.UPage.check_parts'
        if not self.Success:
            rep.cancel(f)
            return
        if len(self.part1) != len(self.part2):
            self.Success = False
            sub = f'{len(self.part1)} == {len(self.part2)}'
            mes = _('The condition "{}" is not observed!').format(sub)
            Message(f, mes, True).show_error()
            return
        for item in self.part2:
            if len(item) != 2:
                return
        return True
    
    def _get_missing(self):
        ''' Get the 1st page number that is not described in U page or
            create a new page number based on the max page number.
        '''
        f = '[MClient] sources.multitrandem.get.UPage._get_missing'
        unpacked = sorted(set(self.part2))
        unpacked = [struct.unpack('<h', item)[0] for item in unpacked]
        # We need +1 for a new item and +1 for 'range'
        compare = [i for i in range(max(unpacked) + 2)]
        # Page #0 is an M page area, and page #1 is U page
        compare = compare[2:]
        for item in compare:
            if item not in unpacked:
                Message(f, item).show_debug()
                return item
    
    def conform_parts(self):
        f = '[MClient] sources.multitrandem.get.UPage.conform_parts'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.part1:
            rep.empty(f)
            return
        if not self.check_parts():
            mes = _('The check has failed!')
            Message(f, mes).show_warning()
            return
        old = self._get_missing()
        new = struct.pack('<h', old)
        mes = f'{old} -> "{new}"'
        Message(f, mes).show_debug()
        self.part1.insert(0, b'')
        self.part2.append(new)



class Walker:
    
    def __init__(self):
        self.article = ''
        self.fnames = []
        self.ending = ''
        self.files = []
        self.glue1 = ''
        self.glue2 = ''
        self.idir = None
        self.lang11 = ''
        self.lang21 = ''
        self.lang13 = ''
        self.lang23 = ''
        self.typein1 = ''
        self.typein2 = ''
        self.stems1 = ''
        self.stems2 = ''
        self.subject = ''
        self.path = Home('mclient').add_config('dics', 'Multitran (Demo)')
        self.check()
        self.set_langs()
        self.walk()
    
    def get_ending(self):
        f = '[MClient] sources.multitrandem.get.Walker.get_ending'
        if not self.Success:
            rep.cancel(f)
            return self.ending
        if self.ending:
            return self.ending
        fname = 'sik.' + self.lang13
        file = self.get_file(fname)
        if not file:
            self.Success = False
            mes = _('File "{}" does not exist!').format(fname)
            Message(f, mes).show_warning()
            return self.ending
        self.ending = file
        return self.ending
    
    def get_subject(self):
        f = '[MClient] sources.multitrandem.get.Walker.get_subject'
        if not self.Success:
            rep.cancel(f)
            return self.subject
        # Suppress useless error output
        if not self.fnames:
            rep.lazy(f)
            return self.subject
        if self.subject:
            return self.subject
        fname = 'subjects.txt'
        file = self.get_file(fname)
        if not file:
            self.Success = False
            mes = _('File "{}" does not exist!').format(fname)
            Message(f, mes).show_warning()
            return self.subject
        self.subject = file
        return self.subject
    
    def get_typein1(self):
        f = '[MClient] sources.multitrandem.get.Walker.get_typein1'
        if not self.Success:
            rep.cancel(f)
            return self.typein1
        if self.typein1:
            return self.typein1
        fname = 'typein.' + self.lang11 + self.lang21
        file = self.get_file(fname)
        if not file:
            self.Success = False
            mes = _('File "{}" does not exist!').format(fname)
            Message(f, mes).show_warning()
            return self.typein1
        self.typein1 = file
        Message(f, self.typein1).show_debug()
        return self.typein1

    def get_typein2(self):
        f = '[MClient] sources.multitrandem.get.Walker.get_typein2'
        if not self.Success:
            rep.cancel(f)
            return self.typein2
        if self.typein2:
            return self.typein2
        fname = 'typein.' + self.lang21 + self.lang11
        file = self.get_file(fname)
        if not file:
            self.Success = False
            mes = _('File "{}" does not exist!').format(fname)
            Message(f, mes).show_warning()
            return self.typein2
        self.typein2 = file
        Message(f, self.typein2).show_debug()
        return self.typein2
    
    def get_files(self):
        f = '[MClient] sources.multitrandem.get.Walker.get_files'
        if not self.Success:
            rep.cancel(f)
            return []
        return [self.get_typein1(), self.get_typein2(), self.get_stems1()
               ,self.get_stems2(), self.get_glue1(), self.get_glue2()
               ,self.get_article()]
    
    def get_article(self):
        f = '[MClient] sources.multitrandem.get.Walker.get_article'
        if not self.Success:
            rep.cancel(f)
            return self.article
        if self.article:
            return self.article
        fname = 'dict.' + self.lang11 + self.lang21 + 't'
        if not fname in self.fnames:
            fname = 'dict.' + self.lang21 + self.lang11 + 't'
        file = self.get_file(fname)
        if not file:
            self.Success = False
            mes = _('File "{}" does not exist!').format(fname)
            Message(f, mes).show_warning()
            return self.article
        self.article = file
        Message(f, self.article).show_debug()
        return self.article
    
    def get_glue1(self):
        f = '[MClient] sources.multitrandem.get.Walker.get_glue1'
        if not self.Success:
            rep.cancel(f)
            return self.glue1
        if self.glue1:
            return self.glue1
        fname = 'dict.' + self.lang11 + self.lang21 + 'd'
        file = self.get_file(fname)
        if not file:
            self.Success = False
            mes = _('File "{}" does not exist!').format(fname)
            Message(f, mes).show_warning()
            return self.glue1
        self.glue1 = file
        Message(f, self.glue1).show_debug()
        return self.glue1
    
    def get_glue2(self):
        f = '[MClient] sources.multitrandem.get.Walker.get_glue2'
        if not self.Success:
            rep.cancel(f)
            return self.glue2
        if self.glue2:
            return self.glue2
        fname = 'dict.' + self.lang21 + self.lang11 + 'd'
        file = self.get_file(fname)
        if not file:
            self.Success = False
            mes = _('File "{}" does not exist!').format(fname)
            Message(f, mes).show_warning()
            return self.glue2
        self.glue2 = file
        Message(f, self.glue2).show_debug()
        return self.glue2
    
    def set_langs(self):
        f = '[MClient] sources.multitrandem.get.Walker.set_langs'
        if not self.Success:
            rep.cancel(f)
            return
        lang1 = LANGS.get_lang1().lower()
        lang2 = LANGS.get_lang2().lower()
        self.lang11 = lang1[0:1]
        self.lang21 = lang2[0:1]
        self.lang13 = lang1[0:3]
        self.lang23 = lang2[0:3]
    
    def check(self):
        f = '[MClient] sources.multitrandem.get.Walker.check'
        if not self.path:
            self.Success = False
            rep.empty(f)
            return
        self.idir = Directory(self.path)
        self.Success = self.idir.Success
    
    def get_stems1(self):
        f = '[MClient] sources.multitrandem.get.Walker.get_stems1'
        if not self.Success:
            rep.cancel(f)
            return self.stems1
        if self.stems1:
            return self.stems1
        fname = 'stem.' + self.lang13
        file = self.get_file(fname)
        if not file:
            self.Success = False
            mes = _('File "{}" does not exist!').format(fname)
            Message(f, mes).show_warning()
            return self.stems1
        self.stems1 = file
        return self.stems1
    
    def get_stems2(self):
        f = '[MClient] sources.multitrandem.get.Walker.get_stems2'
        if not self.Success:
            rep.cancel(f)
            return self.stems2
        if self.stems2:
            return self.stems2
        fname = 'stem.' + self.lang23
        file = self.get_file(fname)
        if not file:
            self.Success = False
            mes = _('File "{}" does not exist!').format(fname)
            Message(f, mes).show_warning()
            return self.stems2
        self.stems2 = file
        return self.stems2
    
    def get_file(self, fname):
        f = '[MClient] sources.multitrandem.get.Walker.get_file'
        if not self.Success:
            rep.cancel(f)
            return
        try:
            ind = self.fnames.index(fname)
            return self.files[ind]
        except (ValueError, IndexError):
            mes = _('Wrong input data!')
            Message(f, mes).show_warning()
    
    def walk(self):
        f = '[MClient] sources.multitrandem.get.Walker.walk'
        if not self.Success:
            rep.cancel(f)
            return self.files
        self.files = self.idir.get_subfiles()
        for file in self.files:
            self.fnames.append(Path(file).get_filename_low())
        self.Success = False
        for fname in self.fnames:
            if fname.startswith('dict.') and fname.endswith('t'):
                self.Success = True
                break
        return self.files



class TypeIn(UPage):
    # Parse files like 'typein.er'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def search(self, pattern):
        f = '[MClient] sources.multitrandem.get.TypeIn.search'
        if not self.Success:
            rep.cancel(f)
            return
        if not pattern:
            rep.empty(f)
            return
        coded = bytes(pattern, CODING)
        poses = self.searchu(coded)
        chunks = self.run_reader(poses)
        if not chunks:
            rep.empty(f)
            return
        matches = []
        for chunk in chunks:
            if chunk.startswith(coded):
                matches.append(chunk)
        decoded = [match.decode(CODING, 'replace') \
                  for match in matches if match]
        for i in range(len(decoded)):
            ''' Sometimes MT provides for suggestions in different case, e.g.,
                'aafc', 'AAFC' separated by b'\x00'.
            '''
            decoded[i] = decoded[i].split('\x00')
            decoded[i] = [item for item in decoded[i] if item]
            if decoded[i][-1]:
                decoded[i] = decoded[i][-1]
            else:
                decoded[i] = decoded[i][0]
        if DEBUG:
            Message(f, decoded).show_debug()
        return decoded
    
    def run_reader(self, poses):
        f = '[MClient] sources.multitrandem.get.TypeIn.reader'
        if not self.Success:
            rep.cancel(f)
            return
        if not poses:
            rep.empty(f)
            return
        stream = self.read(poses[0], poses[1])
        if not stream:
            rep.empty(f)
            return
        chunks = []
        pos = 0
        while pos + 2 < len(stream):
            #NOTE: indexing returns integers, slicing returns bytes
            read = stream[pos:pos+2]
            pos += 2
            len1, len2 = struct.unpack('<2b', read)
            len1 = com.overflowb(len1)
            len2 = com.overflowb(len2)
            if pos + len1 + len2 >= len(stream):
                com.report_status(pos, stream)
                return chunks
            ''' Do this only after checking the condition, otherwise, resulting
                lists will have a different length.
            '''
            chunk = stream[pos:pos+len1]
            pos += len1 + len2
            if chunk:
                chunks.append(chunk)
        return chunks



class Suggest:
    
    def __init__(self, pattern):
        self.set_values()
        if pattern:
            self.reset(pattern)
    
    def set_values(self):
        self.Success = True
        self.pattern = ''
    
    def reset(self, pattern):
        f = '[MClient] sources.multitrandem.get.Suggest.reset'
        self.pattern = pattern
        if not self.pattern:
            self.Success = False
            rep.empty(f)
    
    def get(self, limit=20):
        f = '[MClient] sources.multitrandem.get.Suggest.get'
        if not self.Success:
            rep.cancel(f)
            return
        suggestions = FILES.get_typein1().search(self.pattern)
        if suggestions:
            return suggestions[0:20]
    
    def run(self):
        self.pattern = com.strip(self.pattern)
        return self.get()



class AllDics:
    
    def __init__(self):
        self.dics = []
        self.langs = []
        self.path = Home('mclient').add_config('dics', 'Multitran (Demo)')
        self.Success = Directory(self.path).Success
    
    def get_langs(self):
        # Return all available languages
        f = '[MClient] sources.multitrandem.get.AllDics.langs'
        if not self.Success:
            rep.cancel(f)
            return self.langs
        #TODO: elaborate
        if self.langs:
            return self.langs
        if FILES.iwalker.Success:
            for fname in FILES.iwalker.fnames:
                # Relative paths are already lowercased
                if fname.startswith('dict.') and fname.endswith('t'):
                    self.langs.append(fname)
        return self.langs



class Xor:
    
    def __init__(self, data, offset=0, step=6):
        self.data = data
        self.offset = offset
        self.step = step
    
    def dexor(self):
        f = '[MClient] sources.multitrandem.get.Xor.dexor'
        if not self.data:
            rep.empty(f)
            return
        poses = []
        pos11 = 0
        pos12 = 0
        pos21 = 0
        coef = 0
        for i in range(len(self.data)):
            pos21 = self.data[i]
            pos = self.data[i] + self.offset - i * self.step + coef
            if not 0 <= pos <= 255:
                pos = abs(pos)
                overhead = pos - (pos // 255) * 255 - 1
                pos = 255 - overhead
                delta = pos11 - pos12 - pos21 + pos
                # This is a hack to comply with Multitran's internal logic
                if delta == 249:
                    pos  += 1
                    coef += 1
                elif delta == -261:
                    pos  -= 1
                    coef -= 1
                if DEBUG:
                    mes = _('Overflow: {} -> {}').format(pos21, pos)
                    Message(f, mes).show_debug()
            if DEBUG:
                mes = f'{self.data[i]} -> {pos}'
                Message(f, mes).show_debug()
            poses.append(pos)
            pos11 = self.data[i]
            pos12 = pos
        ''' If the algorithm is correct, this should not be needed. I keep this
            code, however, because a ValueError will be raised otherwise.
        '''
        for i in range(len(poses)):
            if poses[i] > 255:
                #NOTE: 257 was witnessed in mt_big_demo.rar
                poses[i] -= 255
            if not 0 <= poses[i] <= 255:
                mes = _('Invalid value "{}" at position {}!')
                mes = mes.format(poses[i], i)
                Message(f, mes).show_error()
                poses[i] = 0
        result = bytes(poses)
        if DEBUG:
            mes = com.get_string(result)
            Message(f, mes).show_debug()
        return result
    
    def xor(self):
        #TODO: Is this orphaned? Undefined 'data' was used.
        f = '[MClient] sources.multitrandem.get.Xor.xor'
        if not self.data:
            rep.empty(f)
            return
        poses = []
        pos11 = 0
        pos12 = 0
        pos21 = 0
        coef = 0
        for i in range(len(self.data)):
            pos21 = self.data[i]
            pos = self.data[i] + self.offset + i * self.step + coef
            if not 0 <= pos <= 255:
                pos = abs(pos)
                pos = pos - (pos // 255) * 255 - 1
                delta = pos11 - pos12 - pos21 + pos
                # This is a hack to comply with Multitran's internal logic
                if delta == -249:
                    pos  -= 1
                    coef -= 1
                elif delta == 261:
                    pos  += 1
                    coef += 1
                if DEBUG:
                    mes = _('Overflow: {} -> {}').format(pos21, pos)
                    Message(f, mes).show_debug()
            if DEBUG:
                mes = f'{self.data[i]} -> {pos}'
                Message(f, mes).show_debug()
            poses.append(pos)
            pos11 = self.data[i]
            pos12 = pos
        ''' If the algorithm is correct, this should not be needed. I keep this
            code, however, because a ValueError will be raised otherwise.
        '''
        for i in range(len(poses)):
            if not 0 <= poses[i] <= 255:
                mes = _('Invalid value "{}" at position {}!')
                mes = mes.format(poses[i], i)
                Message(f, mes).show_error()
                poses[i] = 0
        result = bytes(poses)
        if DEBUG:
            mes = com.get_string(result)
            Message(f, mes).show_debug()
        return result



class Articles(UPage):
    # Parse files like 'dict.ert'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def parse(self, chunk):
        f = '[MClient] sources.multitrandem.get.Articles.parse'
        if not self.Success:
            rep.cancel(f)
            return
        if not chunk:
            #rep.empty(f)
            return
        return Xor(data = chunk
                  ,offset = -251).dexor()
    
    def search(self, coded):
        # Do not fail the whole class upon a failed search
        f = '[MClient] sources.multitrandem.get.Articles.search'
        if not self.Success:
            rep.cancel(f)
            return
        if not coded:
            rep.empty(f)
            return
        poses = self.searchu(coded)
        if not poses:
            rep.empty(f)
            return
        chunk = self.get_part2(pattern = coded
                              ,start = poses[0]
                              ,end = poses[1])
        return self.parse(chunk)



class Glue(UPage):
    # Parse files like 'dict.erd'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def search(self, coded):
        # Do not fail the whole class upon a failed search
        f = '[MClient] sources.multitrandem.get.Glue.search'
        if not self.Success:
            rep.cancel(f)
            return
        if not coded:
            rep.empty(f)
            return
        poses = self.searchu(coded)
        if not poses:
            rep.empty(f)
            return
        chunk = self.get_part2(pattern = coded
                              ,start = poses[0]
                              ,end = poses[1])
        if chunk:
            return self.parse(chunk)
        ''' 'dict.erd' sometimes does not comprise stem numbers provided by
            'stem.eng' (at least in the demo version).
        '''
        if DEBUG:
            rep.lazy(f)
    
    def parse(self, chunk):
        f = '[MClient] sources.multitrandem.get.Glue.parse'
        if not self.Success:
            rep.cancel(f)
            return
        if not chunk:
            rep.empty(f)
            return
        if (len(chunk) - 2) % 3 != 0 or len(chunk) == 2:
            mes = _('Wrong input data: "{}"!').format(com.get_string(chunk))
            Message(f, mes, True).show_warning()
            return
        chunk = chunk[2:]
        nos = []
        chnos = com.get_chunks(chunk, 3)
        for chno in chnos:
            nos.append(com.unpack(chno))
        if DEBUG:
            Message(f, chnos).show_debug()
            Message(f, nos).show_debug()
        return chnos



class Commands:
    
    def strip(self, pattern):
        if pattern is None:
            pattern = ''
        pattern = pattern.strip()
        pattern = Text(pattern).convert_line_breaks()
        pattern = Text(pattern).delete_line_breaks()
        pattern = Text(pattern).delete_punctuation()
        pattern = Text(pattern).delete_duplicate_spaces()
        pattern = pattern.lower()
        return pattern
    
    def report_status(self, pos, stream):
        f = '[MClient] sources.multitrandem.get.Commands.report_status'
        if not stream:
            rep.empty(f)
            return
        mes = _('{}/{} bytes have been processed').format(pos, len(stream))
        Message(f, mes).show_info()
        if DEBUG:
            remains = stream[pos:len(stream)]
            remains = com.get_string(remains)
            mes = _('Unprocessed fragment: "{}"').format(remains)
            Message(f, mes).show_debug()
    
    def unpackh(self, chno):
        return self.unpack(chno, '<h')
    
    def overflowh(self, no):
        # Limits: -32768 <= no <= 32767
        f = '[MClient] sources.multitrandem.get.Commands.overflowh'
        if no >= 0:
            return no
        result = 32768 + no
        if DEBUG:
            mes = f'{no} -> {result}'
            Message(f, mes).show_debug()
        return result
    
    def overflowb(self, no):
        f = '[MClient] sources.multitrandem.get.Commands.overflowb'
        if no >= 0:
            return no
        ''' Byte format requires -128 <= no <= 127, so it looks like, when
            a page size value is negative, it has just overflown the minimum
            negative -128, e.g., -106 actually means 150:
            128 - 106 = 22 => 127 + 22 + 1 = 150.
        '''
        new = 256 + no
        if DEBUG:
            mes = f'{no} -> {new}'
            Message(f, mes).show_debug()
        return new
    
    def unpack(self, chno, mode='<L'):
        f = '[MClient] sources.multitrandem.get.Commands.unpack'
        if not chno:
            rep.empty(f)
            return
        if mode == '<L':
            chno += b'\x00'
        try:
            return struct.unpack(mode, chno)[0]
        except Exception as e:
            mes = _('Third-party module has failed!\n\nDetails: {}').format(e)
            Message(f, mes).show_warning()
    
    def count_valid(self):
        return len(ALL_DICS.get_langs())
    
    def count_invalid(self):
        if self.count_valid():
            return 0
        else:
            return 1
    
    def get_string(self, chunk, limit=200):
        ''' Only raw strings should be used in GUI (otherwise, for example,
            '\x00' will be treated like b'\x00').
        '''
        f = '[MClient] sources.multitrandem.get.Commands.get_string'
        if not chunk:
            return ''
        result = ''
        try:
            chunk = chunk.decode('latin1')
            result = codecs.encode(chunk, 'unicode_escape')
            result = str(result)
            result = result.replace('\\\\', '\\')
            result = result[2:-1]
            if limit:
                result = Shorten(result, limit).run()
        except Exception as e:
            Message(f, str(e), True).show_warning()
            result = str(chunk)
        return result
    
    def get_chunks(self, iterable, limit=3):
        ''' - Divide an iterable in a consecutive order.
            - Output chunks may have different lengths.
        '''
        f = '[MClient] sources.multitrandem.get.Commands.get_chunks'
        if not iterable:
            rep.empty(f)
            return []
        return [iterable[i:i+limit] for i in range(0, len(iterable), limit)]
    
    def get_subseq(self, iterable, length):
        # Orphaned
        ''' - Unlike 'self.get_chunks', this provides for combinations of
              chunks at different positions instead of slicing an iterable.
            - All chunk will have the same length.
        '''
        return [iterable[i: i + length] \
               for i in range(len(iterable) - length + 1)]


class Files:
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.iwalker = None
        self.typein1 = None
        self.typein2 = None
        self.stems1 = None
        self.stems2 = None
        self.glue1 = None
        self.glue2 = None
        self.article = None
        self.subject = None
        self.ending = None
        self.iwalker = Walker()
        self.Success = self.iwalker.Success
        self.open()
    
    def get_ending(self):
        if self.Success:
            if self.ending is None:
                self.ending = Ending(self.iwalker.get_ending())
        return self.ending
    
    def get_subject(self):
        if self.Success:
            if self.subject is None:
                self.subject = Subject(self.iwalker.get_subject())
        return self.subject
    
    def get_typein1(self):
        if self.Success:
            if self.typein1 is None:
                self.typein1 = TypeIn(self.iwalker.get_typein1())
        return self.typein1
    
    def get_typein2(self):
        if self.Success:
            if self.typein2 is None:
                self.typein2 = TypeIn(self.iwalker.get_typein2())
        return self.typein2
    
    def get_stems1(self):
        if self.Success:
            if self.stems1 is None:
                self.stems1 = Stems(self.iwalker.get_stems1())
        return self.stems1
    
    def get_stems2(self):
        if self.Success:
            if self.stems2 is None:
                self.stems2 = Stems(self.iwalker.get_stems2())
        return self.stems2
    
    def get_glue1(self):
        if self.Success:
            if self.glue1 is None:
                self.glue1 = Glue(self.iwalker.get_glue1())
        return self.glue1
    
    def get_glue2(self):
        if self.Success:
            if self.glue2 is None:
                self.glue2 = Glue(self.iwalker.get_glue2())
        return self.glue2
    
    def get_article(self):
        if self.Success:
            if self.article is None:
                self.article = Articles(self.iwalker.get_article())
        return self.article
    
    def open(self):
        f = '[MClient] sources.multitrandem.get.Files.open'
        if not self.Success:
            rep.lazy(f)
            return
        self.get_typein1()
        self.get_typein2()
        self.get_stems1()
        self.get_stems2()
        self.get_glue1()
        self.get_glue2()
        self.get_article()
    
    def close(self):
        f = '[MClient] sources.multitrandem.get.Files.close'
        if not self.Success:
            rep.lazy(f)
            return
        self.get_typein1().close()
        self.get_typein2().close()
        self.get_stems1().close()
        self.get_stems2().close()
        self.get_glue1().close()
        self.get_glue2().close()
        self.get_article().close()



class Stems(UPage):
    # Parse files like 'stem.eng'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.speech = {}
    
    def get_speech(self, chno):
        f = '[MClient] sources.multitrandem.get.Stems.get_speech'
        if not self.Success:
            rep.cancel(f)
            return
        if chno in self.speech:
            result = self.speech[chno]
            result = com.unpackh(result)
            if DEBUG:
                mes = f'{com.get_string(chno)} -> {result}'
                Message(f, mes).show_debug()
            return result
    
    def parse(self, chunk):
        ''' According to "libmtquery-0.0.1alpha3/doc/README.rus":
            the 1st byte - a type designating the use of capital letters
            (not used), further - a vector of 7-byte codes, each code
            including:
            3 bytes - a word number (4-byte long type compressed to
            3 bytes)
            2 bytes - sik (terminations)
            2 bytes - lgk (speech part codes)
        '''
        f = '[MClient] sources.multitrandem.get.Stems.parse'
        if not self.Success:
            rep.cancel(f)
            return
        if not chunk:
            rep.empty(f)
            return
        nos = []
        chnos = []
        ends = []
        #NOTE: 0 % 7 == 0
        if len(chunk) > 1 and (len(chunk) - 1) % 7 != 0:
            sub = com.get_string(chunk)
            mes = _('Wrong input data: "{}"!').format(sub)
            Message(f, mes).show_warning()
            return
        chunks = com.get_chunks(chunk[1:], 7)
        for i in range(len(chunks)):
            chnos.append(chunks[i][0:3])
            ends.append(chunks[i][3:5])
            self.speech[chunks[i][0:3]] = chunks[i][5:7]
        ends = [struct.unpack('<h', end)[0] for end in ends]
        if DEBUG:
            for chno in chnos:
                nos.append(com.unpack(chno))
            if chnos:
                ids = [i + 1 for i in range(len(nos))]
                tmp = [shcom.set_figure_commas(no) for no in nos]
                mends = [shcom.set_figure_commas(end) for end in ends]
                mchnos = [f'"{com.get_string(chno)}"' for chno in chnos]
                initial = [f'"{com.get_string(chunk)}"' for i in range(len(mchnos))]
                headers = ('NO', 'INITIAL', 'CHUNK', 'UNPACKED', 'END')
                iterable = (ids, initial, mchnos, tmp, mends)
                mes = Table(headers=headers, iterable=iterable, maxrow=50).run()
                mes = '\n\n' + mes
                Message(f, mes).show_debug()
            else:
                mes = _('No debug info')
                Message(f, mes).show_debug()
        return(chnos, ends)
    
    def search(self, stem, end=''):
        # Do not fail the whole class upon a failed search
        f = '[MClient] sources.multitrandem.get.Stems.search'
        if not self.Success:
            rep.cancel(f)
            return
        ''' MT demo does not comprise stem #3 ('-') at all, so we use this
            workaround.
        '''
        if stem == '-':
            return [b'\x03\x00\x00']
        # Zero-length stems should be allowed
        coded = bytes(stem, CODING, 'ignore')
        poses = self.searchu(coded)
        if not poses:
            rep.empty(f)
            return
        chunks = self.get_parts2 (pattern = coded
                                 ,start = poses[0]
                                 ,end = poses[1]
                                 )
        matches = []
        unpacked = []
        for chunk in chunks:
            result = self.parse(chunk)
            if result:
                chnos, endnos = result[0], result[1]
                for i in range(len(endnos)):
                    if FILES.get_ending().has_match(endnos[i], end):
                        if DEBUG:
                            no = com.unpack(chnos[i])
                            no = shcom.set_figure_commas(no)
                            unpacked.append(no)
                        matches.append(chnos[i])
        if DEBUG:
            if matches:
                mmatches = ['"' + com.get_string(match) + '"'\
                            for match in matches
                           ]
                mnos = [i + 1 for i in range(len(mmatches))]
                headers = ('NO', 'STEM', 'END', 'CHUNK', 'UNPACKED')
                mstems = ['"{}"'.format(stem) for i in range(len(mnos))]
                mends = ['"{}"'.format(end) for i in range(len(mnos))]
                iterable = (mnos, mstems, mends, mmatches, unpacked)
                mes = Table(headers=headers, iterable=iterable).run()
                mes = '\n\n' + mes
                Message(f, mes).show_debug()
            else:
                mes = _('No debug info')
                Message(f, mes).show_debug()
        return matches



class Get:
    
    def __init__(self, pattern):
        self.set_values()
        self.pattern = pattern
        self.speech = ''
        self.spabbr = ''
    
    def set_speech(self):
        f = '[MClient] sources.multitrandem.get.Get.set_speech'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.stemnos:
            rep.empty(f)
            return
        chno = self.stemnos[0][0:3]
        stems1 = FILES.get_stems1()
        if not stems1:
            rep.lazy(f)
            return
        speech = stems1.get_speech(chno)
        if DEBUG:
            mes = f'{com.get_string(chno)} -> {speech}'
            Message(f, mes).show_debug()
        if speech is None:
            rep.empty(f)
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
    
    def get_combos(self):
        f = '[MClient] sources.multitrandem.get.Get.get_combos'
        if not self.Success:
            rep.cancel(f)
            return
        self.stemnos = list(itertools.product(*self.stemnos))
        self.stemnos = [b''.join(item) for item in self.stemnos]
        if DEBUG:
            Message(f, self.stemnos).show_debug()
    
    def check(self):
        f = '[MClient] sources.multitrandem.get.Get.check'
        if not self.pattern:
            self.Success = False
            rep.empty(f)
    
    def strip(self):
        f = '[MClient] sources.multitrandem.get.Get.strip'
        if not self.Success:
            rep.cancel(f)
            return
        # Split hyphened words as if they were separate words
        self.pattern = self.pattern.replace('-', ' - ')
        self.pattern = com.strip(self.pattern)
    
    def get_stems(self):
        f = '[MClient] sources.multitrandem.get.Get.get_stems'
        if not self.Success:
            rep.cancel(f)
            return
        words = self.pattern.split(' ')
        for word in words:
            count = 0
            word_stems = []
            i = len(word)
            # Zero-length stems should be allowed
            while i >= 0:
                #NOTE: nltk: according -> accord -> No matches!
                stem = word[0:i]
                end = word[i:]
                mes = _('Try for "{}|{}"').format(stem, end)
                Message(f, mes).show_info()
                ''' Since we swap languages, the needed stems will always be
                    stored in stem file #1.
                '''
                stems1 = FILES.get_stems1()
                if not stems1:
                    rep.lazy(f)
                    return
                stemnos = stems1.search(stem, end)
                if stemnos:
                    mes = _('Found stem: "{}"').format(stem)
                    Message(f, mes).show_info()
                    word_stems += stemnos
                    ''' There can be several valid stems, e.g., 'absolute' and
                        'absolut' (test on 'absolute measurements'). Since
                        finding valid stems significantly slows down
                        performance, we allow only 2 valid stems of the same
                        word.
                    '''
                    if count == MAXSTEMS:
                        break
                i -= 1
            self.stemnos.append(word_stems)
        self.stemnos = [item for item in self.stemnos if item]
        if DEBUG:
            Message(f, self.stemnos).show_debug()
    
    def set_values(self):
        self.Success = True
        self.pattern = ''
        self.htm = ''
        self.stemnos = []
    
    def search(self):
        f = '[MClient] sources.multitrandem.get.Get.search'
        if not self.Success:
            rep.cancel(f)
            return
        glue1 = FILES.get_glue1()
        if not glue1:
            rep.lazy(f)
            return
        art_nos = []
        for combo in self.stemnos:
            art_no = glue1.search(combo)
            if art_no:
                art_nos += art_no
        if art_nos:
            mes = _('Found articles: {}').format(art_nos)
        else:
            mes = _('No articles have been found!')
        Message(f, mes).show_info()
        articles = []
        for art_no in art_nos:
            article = FILES.get_article().search(art_no)
            if article:
                articles.append(article)
        return articles
    
    def run(self):
        self.check()
        self.strip()
        FILES.reset()
        self.get_stems()
        self.get_combos()
        self.set_speech()
        return self.search()


ALL_DICS = AllDics()
LANGS = Language()
FILES = Files()
com = Commands()
