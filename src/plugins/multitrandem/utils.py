#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sys
import struct
import codecs
import termcolor

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message, rep
from skl_shared_qt.paths import Home
from skl_shared_qt.logic import OS, Input, nbspace, com as shcom
from skl_shared_qt.table import Table
from skl_shared_qt.graphics.clipboard.controller import CLIPBOARD
from skl_shared_qt.graphics.debug.controller import DEBUG
from skl_shared_qt.text_file import Write, rewrite
from skl_shared_qt.launch import Launch
import get as gt


COLOR = 'cyan'
BUFFER = 200
DUMP1 = Home().add('tmp', 'dump1')
DUMP2 = Home().add('tmp', 'dump2')


class Xor:
    
    def __init__(self, bytes1, bytes2):
        self.set_values()
        self.bytes1 = bytes1
        self.bytes2 = bytes2
        self.check()
    
    def set_values(self):
        self.Success = True
        self.bytes1 = b''
        self.bytes2 = b''
        self.ints1 = []
        self.ints2 = []
        self.syms = []
    
    def check(self):
        f = '[MClient] plugins.multitrandem.utils.Xor.check'
        if not self.bytes1 or not self.bytes2:
            self.Success = False
            rep.empty(f)
            return
        if len(self.bytes1) == len(self.bytes2):
            return True
        self.Success = False
        sub = f'{len(self.bytes1)} == {len(self.bytes2)}'
        mes = _('The condition "{}" is not observed!').format(sub)
        Message(f, mes).show_warning()
        
    def report(self):
        f = '[MClient] plugins.multitrandem.utils.Xor.report'
        if not self.Success:
            rep.cancel(f)
            return
        headers = ('NO', 'ORIG', 'INT1', 'INT2')
        nos = [i + 1 for i in range(len(self.syms))]
        iterable = (nos, self.syms, self.ints1, self.ints2)
        mes = Table(headers=headers, iterable=iterable, sep=nbspace * 2).run()
        return mes
    
    def analyze(self):
        f = '[MClient] plugins.multitrandem.utils.Xor.analyze'
        if not self.Success:
            rep.cancel(f)
            return
        for i in range(len(self.bytes1)):
            decoded = self.bytes1[i:i+1].decode(gt.CODING, 'replace')
            self.syms.append(f'"{decoded}"')
            self.ints1.append(self.bytes1[i])
            self.ints2.append(self.bytes2[i])



class Tests:
    
    def __init__(self):
        self.dump1 = self.dump2 = None
    
    def gen_patterns(self):
        f = '[MClient] plugins.multitrandem.utils.Tests.gen_patterns'
        table = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюя'
        i = 3
        len_ = 5
        result = com.gen_patterns(i=i, length=len_, table=table)
        DEBUG.reset(f, str(result))
        DEBUG.show()
    
    def analyze_xor(self):
        f = '[MClient] plugins.multitrandem.utils.Tests.analyze_xor'
        bytes1 = b'Bullshit!'
        bytes2 = b'-fcivqx\x89<'
        ixor = Xor(bytes1, bytes2)
        ixor.analyze()
        mes = ixor.report()
        DEBUG.reset(f, mes)
        DEBUG.show()
    
    def get_patch(self):
        #f = '[MClient] plugins.multitrandem.utils.Tests.get_patch'
        file = '/home/pete/.wine/drive_c/setup/Multitran/network/eng_rus/dict.ert'
        # A comment added for "Zerah"
        pos = 132779143
        sympos = 1
        #table = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюя'
        patterns = com.gen_patterns(i=sympos, length=2)
        messages = []
        ints1 = []
        ints2 = []
        for pattern in patterns:
            if pattern is None:
                mes = _('Warning: this step will be skipped!')
                messages.append(mes)
                messages.append('')
            else:
                mes = _('Pattern: "{}"').format(pattern)
                print(mes)
                CLIPBOARD.copy(pattern)
                input(_('Make changes to the dictionary and press any key'))
                result = com.get_patch(file=file, pattern=pattern, pos=pos
                                      ,sympos = sympos)
                if result:
                    messages.append(result[0])
                    ints1.append(result[1])
                    ints2.append(result[2])
        messages.append('')
        messages.append('')
        mes = _('Original positions:')
        messages.append(mes)
        messages.append(str(ints1))
        mes = _('Final positions:')
        messages.append(mes)
        messages.append(str(ints2))
        mes = '\n'.join(messages)
        CLIPBOARD.copy(str(ints2))
        #DEBUG.reset(f, mes)
        #DEBUG.show()
        filew = '/tmp/result.txt'
        Write(filew, True).write(mes)
        Launch(filew).launch_default()
    
    def corrupt(self):
        f = '[MClient] plugins.multitrandem.utils.Tests.corrupt'
        file = '/home/pete/wine/mt/drive_c/setup/mt/network/eng_rus/dict.ert'
        #pos = 132779147
        #subst = b'\x00'
        #pos = 319047096
        #319047082
        pos = 319047086
        subst = b'A'
        old = com.corrupt (filew = file
                          ,pos = pos
                          ,subst = subst
                          )
        mes = _('Restore the damaged file?')
        if not Message(f, mes).show_question():
            mes = _('Operation has been canceled by the user.')
            Message(f, mes).show_info()
            return
        com.corrupt (filew = file
                    ,pos = pos
                    ,subst = old
                    )
    
    def navigate(self):
        Navigate('/home/pete/tmp/dump2').show_menu()
    
    def analyze_dumps(self):
        f = '[MClient] plugins.multitrandem.utils.Tests.analyze_dumps'
        iparse1 = Parser(DUMP1)
        iparse2 = Parser(DUMP2)
        pos1 = 0
        pos2 = min(iparse1.get_file_size(), iparse2.get_file_size())
        iparse1.run_reader(pos1, pos2)
        iparse2.run_reader(pos1, pos2)
        iparse1.parse_article()
        iparse2.parse_article()
        if not iparse1.Success or not iparse2.Success:
            rep.cancel(f)
            iparse1.close()
            iparse2.close()
            return
        lens11 = [len(chunk) for chunk in iparse1.chunks1]
        lens12 = [len(chunk) for chunk in iparse1.chunks2]
        lens21 = [len(chunk) for chunk in iparse2.chunks1]
        lens22 = [len(chunk) for chunk in iparse2.chunks2]
        len11 = len(iparse1.chunks1)
        len12 = len(iparse1.chunks2)
        len21 = len(iparse2.chunks1)
        len22 = len(iparse2.chunks2)
        mes = f'len(iparse1.chunks1): {len11}'
        Message(f, mes).show_debug()
        mes = f'len(iparse1.chunks2): {len12}'
        Message(f, mes).show_debug()
        mes = f'len(iparse2.chunks1): {len21}'
        Message(f, mes).show_debug()
        mes = f'len(iparse2.chunks2): {len22}'
        Message(f, mes).show_debug()
        max_ = max(len11, len12, len21, len22)
        nos = [i + 1 for i in range(max_)]
        headers = ('NO', 'D1P1', 'D1P2', 'D2P1', 'D2P2')
        iterable = [nos, lens11, lens12, lens21, lens22]
        mes = Table(headers=headers, iterable=iterable).run()
        DEBUG.reset(f, mes)
        DEBUG.show()
        mes = f'len11: {len11}\n'
        mes += f'len12: {len12}\n'
        mes += f'len21: {len21}\n'
        mes += f'len22: {len22}\n'
        DEBUG.reset(f, mes)
        DEBUG.show()
        '''
        lens11 = sorted(set(lens11))
        lens12 = sorted(set(lens12))
        lens21 = sorted(set(lens21))
        lens22 = sorted(set(lens22))
        '''
        '''
        mes = 'D1P1:\n' + str(lens11) + '\n\n'
        mes += 'D1P2:\n' + str(lens12) + '\n\n'
        mes += 'D2P1:\n' + str(lens21) + '\n\n'
        mes += 'D2P2:\n' + str(lens22) + '\n\n'
        '''
        '''
        lens21 = [item for item in lens21 if item not in lens11]
        lens22 = [item for item in lens22 if item not in lens12]
        mes = 'UNIQUE lens21:\n' + str(lens21) + '\n\n'
        mes += 'UNIQUE lens22:\n' + str(lens22) + '\n\n'
        '''
        lens21 = [item for item in lens21 if item in lens11]
        lens22 = [item for item in lens22 if item in lens12]
        mes = 'SHARED lens21:\n' + str(lens21) + '\n\n'
        mes += 'SHARED lens22:\n' + str(lens22) + '\n\n'
        DEBUG.reset(f, mes)
        DEBUG.show()
        iparse1.close()
        iparse2.close()
    
    def close_dumps(self):
        f = '[MClient] plugins.multitrandem.utils.Tests.close_dumps'
        if self.dump1 is None:
            rep.empty(f)
        self.dump1.close()
        if self.dump2 is None:
            rep.empty(f)
        self.dump2.close()
    
    def compare_bytes(self, maxlen=10):
        f = '[MClient] plugins.multitrandem.utils.Tests.compare_bytes'
        self.dump1 = gt.Binary(DUMP1)
        self.dump2 = gt.Binary(DUMP2)
        end1 = self.dump1.get_file_size()
        end2 = self.dump2.get_file_size()
        read1 = self.dump1.read(0, end1)
        read2 = self.dump2.read(0, end2)
        if not read1 or not read2:
            rep.empty(f)
            self.close_dumps()
            return
        if len(read1) <= maxlen or len(read2) <= maxlen:
            rep.lazy(f)
            self.close_dumps()
            return
        sex = gt.com.get_subseq(read2, maxlen)
        matches = [seq for seq in sex if seq in read1]
        if not matches:
            mes = _('No matches!')
            Message(f, mes, True).show_info()
            self.close_dumps()
            return
        matches = [gt.com.get_string(match, 0) for match in matches]
        for i in range(len(matches)):
            matches[i] = f'{i}: {matches[i]}'
        mes = '\n'.join(matches)
        DEBUG.reset(f, mes)
        DEBUG.show()
        self.close_dumps()
    
    def show_dumps(self):
        CompareBinaries(DUMP1, DUMP2).show_menu()
    
    def get_shared_dumps(self):
        f = '[MClient] plugins.multitrandem.utils.Tests.get_shared_dumps'
        pos1 = 0
        pos2 = 16380
        ''' We do not use 'self._parse' here since 'Parser.parse'
            automatically selects the mode based on a file name.
        '''
        iparse1 = Parser(DUMP1)
        iparse1.run_reader(pos1, pos2)
        iparse1.parse_article()
        iparse2 = Parser(DUMP2)
        iparse2.run_reader(pos1, pos2)
        iparse2.parse_article()
        if iparse1.chunks1 and iparse1.chunks2 and iparse2.chunks1 \
        and iparse2.chunks2:
            shared1 = [chunk for chunk in iparse1.chunks1 \
                       if chunk in iparse2.chunks1
                      ]
            shared2 = [chunk for chunk in iparse1.chunks2 \
                       if chunk in iparse2.chunks2
                      ]
            mes = _('List {}:').format(1)
            mes += '\n' + str(shared1) + '\n'
            mes += _('List {}:').format(2)
            mes += '\n' + str(shared2)
            DEBUG.reset(f, mes)
            DEBUG.show()
        else:
            rep.empty(f)
    
    def parse_dumps(self):
        pos1 = 0
        pos2 = 16380
        ''' We do not use 'self._parse' here since 'Parser.parse' automatically
            selects the mode based on a file name.
        '''
        iparse = Parser(DUMP1)
        iparse.run_reader(pos1, pos2)
        iparse.parse_article()
        iparse.debug()
        iparse = Parser(DUMP2)
        iparse.run_reader(pos1, pos2)
        iparse.parse_article()
        iparse.debug()
    
    def _parse(self, file, pos1, pos2):
        iparse = Parser(file)
        iparse.run_reader(pos1, pos2)
        iparse.parse()
        iparse.debug()
    
    def parse_article(self):
        file = gt.objs.get_files().iwalker.get_article()
        pos1 = 655363
        pos2 = 656808
        self._parse(file, pos1, pos2)
    
    def parse_glue(self):
        file = gt.objs.get_files().iwalker.get_glue1()
        pos1 = 16387
        pos2 = 22119
        self._parse(file, pos1, pos2)
    
    def parse_stems(self):
        file = gt.objs.get_files().iwalker.get_stems1()
        pos1 = 7479299
        pos2 = 7486690
        self._parse(file, pos1, pos2)
    
    def compare(self):
        #file1 = '/home/pete/wine/backup/mt/drive_c/setup/mt/network/eng_rus/dict.ert'
        #file2 = '/home/pete/wine/mt/drive_c/setup/mt/network/eng_rus/dict.ert'
        file1 = '/home/pete/tmp/prev.ert'
        file2 = '/home/pete/wine/mt/drive_c/setup/mt/network/eng_rus/dict.ert'
        CompareBinaries(file1, file2).show_menu()
    
    def navigate_article(self):
        Navigate(gt.objs.get_files().iwalker.get_article()).show_menu()
    
    def navigate_glue(self):
        Navigate(gt.objs.get_files().iwalker.get_glue1()).show_menu()



class Parser(gt.Binary):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chunks1 = []
        self.chunks2 = []
        self.xplain1 = []
        self.xplain2 = []
    
    def parsel23(self, chunk):
        f = '[MClient] plugins.multitrandem.utils.Parser.parsel23'
        if not self.Success:
            rep.cancel(f)
            return
        # 2 bytes + multiple sequences of 3 bytes
        if len(chunk) > 4 and (len(chunk) - 2) % 3 == 0:
            add = [struct.unpack('<h', chunk[0:2])[0]]
            for tmp in gt.com.get_chunks(chunk[2:], 3):
                tmp += b'\x00'
                add.append(struct.unpack('<L', tmp)[0])
            return add
    
    def chunk3(self, chunk):
        f = '[MClient] plugins.multitrandem.utils.Parser.chunk3'
        if not self.Success:
            rep.cancel(f)
            return
        if len(chunk) % 3 == 0:
            chunks = gt.com.get_chunks(chunk, 3)
            vals = []
            for chunk in chunks:
                chunk += b'\x00'
                vals.append(struct.unpack('<L', chunk)[0])
            return vals
    
    def parse_glue(self):
        f = '[MClient] plugins.multitrandem.utils.Parser.parse_glue'
        if not self.Success:
            rep.cancel(f)
            return
        for chunk in self.chunks1:
            tmp = self.chunk3(chunk)
            if tmp:
                self.xplain1.append(tmp)
            else:
                self.xplain1.append([_('UNKNOWN')])
        for chunk in self.chunks2:
            tmp = self.parsel23(chunk)
            if tmp:
                self.xplain2.append(tmp)
            else:
                self.xplain2.append([_('UNKNOWN')])
    
    def parse_article(self):
        f = '[MClient] plugins.multitrandem.utils.Parser.parse_article'
        if not self.Success:
            rep.cancel(f)
            return
        for chunk in self.chunks1:
            chunk = gt.com.get_string(chunk, 0)
            self.xplain1.append(chunk)
        for chunk in self.chunks2:
            chunk = gt.com.get_string(chunk, 0)
            self.xplain2.append(chunk)
    
    def debug(self):
        f = '[MClient] plugins.multitrandem.utils.Parser.debug'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.xplain1 or not self.xplain2:
            rep.empty(f)
            return
        if len(self.xplain1) != len(self.xplain2):
            self.Success = False
            sub = f'{len(self.xplain1)} == {len(self.xplain2)}'
            mes = _('The condition "{}" is not observed!').format(sub)
            Message(f, mes).show_warning()
            return
        nos = [i + 1 for i in range(len(self.xplain1))]
        len1 = [len(chunk) for chunk in self.chunks1]
        len2 = [len(chunk) for chunk in self.chunks2]
        headers = ('NOS', 'LEN1', 'PART1', 'LEN2', 'PART2')
        iterable = (nos, len1, self.xplain1, len2, self.xplain2)
        mes = Table(headers=headers, iterable=iterable, maxrow=45).run()
        if not mes:
            rep.empty(f)
            return
        sub = _('File: "{}"').format(self.file) += '\n\n'
        DEBUG.reset(f, sub + mes)
        DEBUG.show()
        
    def get_chunk7(self, chunk):
        f = '[MClient] plugins.multitrandem.utils.Parser.chunk7'
        ''' According to "libmtquery-0.0.1alpha3/doc/README.rus":
            the 1st byte - a type designating the use of capital letters
            (not used), further - a vector of 7-byte codes, each code
            including:
            3 bytes - a word number (4-byte long type compressed to 3 bytes)
            2 bytes - sik (terminations)
            2 bytes - lgk (speech part codes).
        '''
        if not self.Success:
            rep.cancel(f)
            return
        if chunk and (len(chunk) - 1) % 7 == 0:
            tmp = []
            chunks = gt.com.get_chunks(chunk[1:], 7)
            for item in chunks:
                delta = 7 - len(item)
                item = item + b'\x00' * delta
                word = item[0:3] + b'\x00'
                sik = item[3:5]
                lgk = item[5:7]
                tmp.append(struct.unpack('<L', word)[0])
                tmp.append(struct.unpack('<h', sik)[0])
                tmp.append(struct.unpack('<h', lgk)[0])
            return tmp
    
    def parsel1(self):
        f = '[MClient] plugins.multitrandem.utils.Parser.parsel1'
        if not self.Success:
            rep.cancel(f)
            return
        for chunk in self.chunks1:
            chunk = chunk.decode(gt.CODING, 'replace')
            self.xplain1.append(chunk)
    
    def parse_stem(self):
        f = '[MClient] plugins.multitrandem.utils.Parser.parse_stem'
        if not self.Success:
            rep.cancel(f)
            return
        self.parsel1()
        for chunk in self.chunks2:
            tmp = self.get_chunk7(chunk)
            if tmp:
                self.xplain2.append(tmp)
            else:
                self.xplain2.append([_('UNKNOWN')])
    
    def parse(self):
        f = '[MClient] plugins.multitrandem.utils.Parser.parse'
        if not self.Success:
            rep.cancel(f)
            return
        #FIX: Why base names are not lowercased?
        bname = self.bname.lower()
        if bname.startswith('stem'):
            self.parse_stem()
        elif bname.startswith('dict') and bname.endswith('d'):
            self.parse_glue()
        elif bname.startswith('dict') and bname.endswith('t'):
            self.parse_article()
        else:
            mes = '"{}"'.format(self.bname)
            Message(f, mes).show_debug()
            mes = _('Not implemented yet!')
            Message(f, mes, True).show_info()
    
    def run_reader(self, pos1, pos2):
        f = '[MClient] plugins.multitrandem.utils.Parser.reader'
        if not self.Success:
            rep.cancel(f)
            return
        stream = self.read(pos1, pos2)
        if not stream:
            rep.empty(f)
            return
        self.chunks1 = []
        self.chunks2 = []
        pos = 0
        while pos + 2 < len(stream):
            #NOTE: indexing returns integers, slicing returns bytes
            read = stream[pos:pos+2]
            pos += 2
            len1, len2 = struct.unpack('<2b', read)
            len1 = gt.com.overflowb(len1)
            len2 = gt.com.overflowb(len2)
            if pos + len1 + len2 >= len(stream):
                gt.com.report_status(pos, stream)
                return
            ''' Do this only after checking the condition, otherwise, resulting
                lists will have a different length.
            '''
            chunk1 = stream[pos:pos+len1]
            pos += len1
            chunk2 = stream[pos:pos+len2]
            pos += len2
            # Zero-length chunks should be allowed
            if chunk2:
                self.chunks1.append(chunk1)
                self.chunks2.append(chunk2)



class Navigate(gt.Binary):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chunk = b''
        self.coms = ['buffer', 'help', 'load', 'quit', 'pgup', 'pgdn', 'pos'
                    ,'clear', 'exit', 'dump', 'find', 'findprev', 'findnext'
                    ,'findtext', 'findbytes', 'same', 'q'
                    ]
        self.buffer = round(BUFFER * 2.5)
        self.border = 20
        self.pos = 0
        self.spos = None
        self.coded = b''
        self.lastcom = ''
        self.coms.sort()
    
    def find_prev(self):
        f = '[MClient] plugins.multitrandem.utils.Navigate.find_prev'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.coded:
            self.find_nav()
            return
        if self.spos is None or self.spos == 0:
            mes = _('No matches!')
            Message(f, mes).show_info()
            return
        spos = self.imap.rfind(self.coded, 0, self.spos)
        if spos == -1:
            mes = _('No matches!')
            Message(f, mes).show_info()
            return
        self.spos = spos
        self._print_found()
    
    def find_next(self):
        f = '[MClient] plugins.multitrandem.utils.Navigate.find_next'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.coded:
            self.find_nav()
            return
        if self.spos is None:
            mes = _('No matches!')
            Message(f, mes).show_info()
            return
        spos = self.spos
        if spos < self.get_file_size() - 1:
            spos += 1
        else:
            spos = self.fsize - len(self.coded)
        spos = self.find(self.coded, spos)
        if spos is None:
            mes = _('No matches!')
            Message(f, mes).show_info()
            return
        self.spos = spos
        self._print_found()
    
    def _print_found(self):
        f = '[MClient] plugins.multitrandem.utils.Navigate._print_found'
        if self.spos is None:
            mes = _('No matches!')
            Message(f, mes).show_info()
            return
        if self.spos > self.border:
            b1 = pos1 = self.spos - self.border
            chunk1 = self.read(pos1, self.spos)
        elif self.spos:
            chunk1 = self.read(0, self.spos)
            b1 = 0
        else:
            chunk1 = b''
            b1 = self.spos
        min_ = min(self.buffer, self.get_file_size())
        ch2_len = min_ - len(chunk1) - len(self.coded)
        if ch2_len > 0:
            pos1 = self.spos + len(self.coded)
            b2 = pos2 = pos1 + ch2_len
            chunk2 = self.read(pos1, pos2)
        else:
            chunk2 = b''
            b2 = self.spos + len(self.coded)
        buffer1 = gt.com.get_string(chunk1, 0)
        buffer2 = gt.com.get_string(self.coded, 0)
        buffer2 = termcolor.colored(buffer2, COLOR)
        buffer3 = gt.com.get_string(chunk2, 0)
        mes = f'[{shcom.set_figure_commas(b1)} : {shcom.set_figure_commas(b2)}]'
        Message(f, mes).show_debug()
        sys.stdout.write(buffer1)
        sys.stdout.write(buffer2)
        print(buffer3)
    
    def _find(self):
        f = '[MClient] plugins.multitrandem.utils.Navigate._find'
        spos = self.find(self.coded)
        if spos is None:
            mes = _('No matches!')
            Message(f, mes).show_info()
        else:
            self.spos = spos
            self._print_found()
    
    def find_text(self):
        f = '[MClient] plugins.multitrandem.utils.Navigate.find_text'
        if not self.Success:
            rep.cancel(f)
            return
        pattern = com.input_str(_('Enter text to search for: '))
        self.coded = bytes(pattern, gt.CODING)
        self._find()
    
    def find_bytes(self):
        f = '[MClient] plugins.multitrandem.utils.Navigate.find_bytes'
        if not self.Success:
            rep.cancel(f)
            return
        pattern = com.input_str(_('Enter bytes to search for: '))
        try:
            pattern = codecs.decode(pattern, 'unicode_escape')
            self.coded = pattern.encode('latin1')
        except Exception as e:
            self.coded = b''
            mes = _('Operation has failed!\n\nDetails: {}')
            mes = mes.format(e)
            Message(f, mes).show_warning()
        self._find()
    
    def find_nav(self):
        f = '[MClient] plugins.multitrandem.utils.Navigate.find_nav'
        if not self.Success:
            rep.cancel(f)
            return
        choice = input(_('Search for text instead of bytes? Y/n '))
        choice = choice.strip()
        if choice in ('', 'y', 'Y'):
            self.find_text()
        elif choice in ('n', 'N'):
            self.find_bytes()
        else:
            self.find_nav()
        
    def dump(self):
        f = '[MClient] plugins.multitrandem.utils.Navigate.dump'
        if not self.Success:
            rep.cancel(f)
            return
        mes = _('This will extract data from the binary file from set positions')
        print(mes)
        mes1 = _('Position {}: ').format(1)
        mes2 = _('Position {}: ').format(2)
        pos1 = com.input_int(mes1)
        pos2 = com.input_int(mes2)
        if pos1 >= pos2:
            sub = f'{pos1} < {pos2}'
            mes = _('The condition "{}" is not observed!').format(sub)
            Message(f, mes).show_warning()
            return
        mes = _('An output file: ')
        filew = com.input_str(mes)
        if not filew:
            rep.empty(f)
            return
        if not rewrite(filew):
            mes = _('Operation has been canceled by the user.')
            Message(f, mes).show_info()
            return
        chunk = self.read(pos1, pos2)
        if not chunk:
            rep.empty(f)
            return
        try:
            mes = _('Write "{}"').format(filew)
            Message(f, mes).show_info()
            with open(filew, 'wb') as fw:
                fw.write(chunk)
        except Exception as e:
            mes = _('Operation has failed!\n\nDetails: {}').format(e)
            Message(f, mes).show_warning()
    
    def go_end(self):
        f = '[MClient] plugins.multitrandem.utils.Navigate.go_end'
        if not self.Success:
            rep.cancel(f)
            return
        self.pos = self.get_file_size() - self.buffer
        if self.pos < 0:
            self.pos = 0
        self.load()
    
    def go_start(self):
        f = '[MClient] plugins.multitrandem.utils.Navigate.go_start'
        if not self.Success:
            rep.cancel(f)
            return
        self.pos = 0
        self.load()
    
    def clear(self):
        f = '[MClient] plugins.multitrandem.utils.Navigate.clear'
        if not self.Success:
            rep.cancel(f)
            return
        try:
            if OS.is_win():
                os.system('cls')
            else:
                os.system('clear')
        except Exception as e:
            mes = _('Operation has failed!\n\nDetails: {}')
            mes = mes.format(e)
            Message(f, mes).show_error()
    
    def set_pos(self):
        f = '[MClient] plugins.multitrandem.utils.Navigate.set_pos'
        if not self.Success:
            rep.cancel(f)
            return
        mes = _('Enter a position to go or press Return to keep the current one ({}): ')
        mes = mes.format(shcom.set_figure_commas(self.pos))
        val = input(mes)
        val = val.strip()
        if not val:
            rep.lazy(f)
            return
        val = Input(f, val).get_integer()
        if val < 0:
            mes = _('Wrong input data!')
            Message(f, mes).show_warning()
            return
        self.pos = val
    
    def go_page_down(self):
        f = '[MClient] plugins.multitrandem.utils.Navigate.go_page_down'
        if not self.Success:
            rep.cancel(f)
            return
        self.pos += self.buffer
        if self.pos >= self.get_file_size():
            self.pos = self.get_file_size() - self.buffer
            if self.pos < 0:
                self.pos = 0
        self.load()
    
    def go_page_up(self):
        f = '[MClient] plugins.multitrandem.utils.Navigate.go_page_up'
        if not self.Success:
            rep.cancel(f)
            return
        self.pos -= self.buffer
        if self.pos < 0:
            self.pos = 0
        self.load()
    
    def load(self):
        f = '[MClient] plugins.multitrandem.utils.Navigate.load'
        if not self.Success:
            rep.cancel(f)
            return
        start = self.pos
        end = start + self.buffer
        if start > self.get_file_size():
            start = 0
        if end > self.get_file_size():
            end = self.get_file_size()
        self.chunk = self.read(start, end)
        self.report()
        self.print()
    
    def set_buffer(self):
        f = '[MClient] plugins.multitrandem.utils.Navigate.set_buffer'
        if not self.Success:
            rep.cancel(f)
            return
        mes = _('Enter a buffer size or press Return to keep the current one ({}): ')
        mes = mes.format(shcom.set_figure_commas(self.buffer))
        val = input(mes)
        val = val.strip()
        if not val:
            rep.lazy(f)
            return
        val = Input(f, val).get_integer()
        if not val:
            mes = _('Wrong input data!')
            Message(f, mes).show_warning()
            return
        self.buffer = val
    
    def show_help(self):
        f = '[MClient] plugins.multitrandem.utils.Navigate.show_help'
        if not self.Success:
            rep.cancel(f)
            return
        mes = _('Available commands: {}')
        mes = mes.format('; '.join(self.coms))
        print(mes)
    
    def show_menu(self, command=''):
        f = '[MClient] plugins.multitrandem.utils.Navigate.show_menu'
        if not self.Success:
            rep.cancel(f)
            return
        if not command:
            try:
                command = input(_('Enter a command: '))
            except (EOFError, KeyboardInterrupt):
                command = 'quit'
            command = command.strip()
            if command and command != 'same':
                self.lastcom = command
        if command in ('exit', 'quit', 'q'):
            self.quit()
        elif command == 'buffer':
            self.set_buffer()
            self.load()
            self.show_menu()
        elif command == 'clear':
            self.clear()
            self.show_menu()
        elif command == 'dump':
            self.dump()
            self.show_menu()
        elif command == 'end':
            self.go_end()
            self.show_menu()
        elif command == 'find':
            self.find_nav()
            self.show_menu()
        elif command == 'findbytes':
            self.find_bytes()
            self.show_menu()
        elif command == 'findnext':
            self.find_next()
            self.show_menu()
        elif command == 'findprev':
            self.find_prev()
            self.show_menu()
        elif command == 'findtext':
            self.find_text()
            self.show_menu()
        elif command == 'help':
            self.show_help()
            self.show_menu()
        elif command == 'load':
            self.load()
            self.show_menu()
        elif command == 'pgdn':
            self.go_page_down()
            self.show_menu()
        elif command == 'pgup':
            self.go_page_up()
            self.show_menu()
        elif command == 'pos':
            self.set_pos()
            self.load()
            self.show_menu()
        elif command in ('', 'same'):
            self.show_menu(self.lastcom)
        elif command == 'start':
            self.go_start()
            self.show_menu()
        else:
            mes = _('An unknown command! Enter "help" to get help.')
            print(mes)
            self.show_menu()
    
    def quit(self):
        f = '[MClient] plugins.multitrandem.utils.Navigate.quit'
        if not self.Success:
            rep.cancel(f)
            return
        self.close()
        mes = _('Goodbye!')
        Message(f, mes).show_debug()
    
    def print(self):
        f = '[MClient] plugins.multitrandem.utils.Navigate.print'
        if not self.Success:
            rep.cancel(f)
            return
        mes = gt.com.get_string(self.chunk, 0)
        print(mes)
    
    def report(self):
        f = '[MClient] plugins.multitrandem.utils.Navigate.report'
        if not self.Success:
            rep.cancel(f)
            return
        self.clear()
        sub = shcom.set_figure_commas(self.pos)
        mes = _('Current position: {}').format(sub)
        print(mes)



class Commands:
    
    def __init__(self):
        self.set_values()
    
    def set_values(self):
        # 'windows-1251' in ascending order
        self.table = ('!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+'
                     ,',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6'
                     ,'7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A'
                     ,'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L'
                     ,'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W'
                     ,'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b'
                     ,'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm'
                     ,'n', 'o', 'p', 'q',' r', 's', 't', 'u', 'v', 'w', 'x'
                     ,'y', 'z', '{', '|', '}','~', None, 'Ђ', 'Ѓ','‚ ','ѓ'
                     ,'„', '…', '†', '‡', '€', '‰', 'Љ', '‹', 'Њ', 'Ќ', 'Ћ'
                     ,'Џ', 'ђ', '‘', '’', '“', '”', '•', '–', '—', None, '™'
                     ,'љ', '›', 'њ', 'ќ', 'ћ', 'џ', None, 'Ў', 'ў', 'Ћ', '¤'
                     ,'Ґ', '¦', '§', 'Ё', '©', 'Є', '«', '¬', None, '®', 'Ї'
                     ,'°', '±', 'І', 'і', 'ґ', 'µ', '¶', '·', 'ё', '№', 'є'
                     ,'»', 'ј', 'Ѕ', 'ѕ', 'ї', 'А', 'Б', 'В', 'Г', 'Д', 'Е'
                     ,'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р'
                     ,'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы'
                     ,'Ь', 'Э', 'Ю', 'Я', 'а', 'б', 'в', 'г', 'д', 'е', 'ж'
                     ,'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с'
                     ,'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь'
                     ,'э', 'ю', 'я'
                     )
    
    def gen_patterns(self, i=4, length=5, repeat='!', table=[]):
        if not table:
            table = self.table
        patterns = []
        add = repeat * length
        for sym in table:
            if sym is not None:
                item = list(add)
                item[i] = sym
                patterns.append(''.join(item))
        return patterns
    
    def get_patch(self, file, pattern, pos, add_pos=20, sympos=0):
        f = '[MClient] plugins.multitrandem.utils.Commands.get_patch'
        if not file or not pattern:
            rep.empty(f)
            return
        ibin = gt.Binary(file)
        if not ibin.Success:
            rep.cancel(f)
            return
        coded = bytes(pattern, gt.CODING, 'replace')
        pos2 = pos + len(coded)
        chunk = ibin.read(pos, pos2)
        lchunk = ibin.read(pos, pos2 + add_pos)
        string = gt.com.get_string(chunk)
        lstring = gt.com.get_string(lchunk)
        string = f"b'''{string}'''"
        lstring = f"b'''{lstring}'''"
        ibin.close()
        messages = []
        mes = f'"{pattern}"'
        messages.append(mes)
        messages.append(string)
        messages.append(lstring)
        ixor = Xor(coded, chunk)
        ixor.analyze()
        mes = ixor.report()
        if mes:
            messages.append(mes)
        try:
            int1 = ixor.bytes1[sympos]
            int2 = ixor.bytes2[sympos]
        except IndexError:
            int1 = int2 = -1
            mes = _('Wrong input data!')
            Message(f, mes, True).show_warning()
        return('\n'.join(messages), int1, int2)
    
    def corrupt(self, filew, pos, subst=b'\x00'):
        f = '[MClient] plugins.multitrandem.utils.Commands.corrupt'
        if not filew or not subst:
            rep.empty(f)
            return
        ibin = gt.Binary(filew)
        chunk = ibin.read(pos, pos + len(subst))
        ibin.close()
        try:
            mes = _('Replace bytes "{}" with "{}" (file: {}, position: {})')
            mes = mes.format(gt.com.get_string(chunk), gt.com.get_string(subst)
                            ,filew, shcom.set_figure_commas(pos))
            Message(f, mes).show_info()
            ''' For some reason, opening with 'wb' or 'w+b' causes different
                results.
            '''
            with open(filew, 'r+b') as fw:
                fw.seek(pos)
                fw.write(subst)
        except Exception as e:
            mes = _('Operation has failed!\n\nDetails: {}').format(e)
            Message(f, mes).show_warning()
        return chunk
    
    def input_str(self, mes=''):
        if not mes:
            mes = _('Input a string: ')
        try:
            return input(mes)
        except (EOFError, KeyboardInterrupt):
            return ''
    
    def input_int(self, mes=''):
        f = '[MClient] plugins.multitrandem.utils.Commands.input_int'
        if not mes:
            mes = _('Input an integer: ')
        try:
            val = input(mes)
        except (EOFError, KeyboardInterrupt):
            val = 0
        return Input(f, val).get_integer()



class CompareBinaries:
    
    def __init__(self, file1='', file2=''):
        self.set_values()
        self.reset(file1, file2)
    
    def set_files(self):
        f = '[MClient] plugins.multitrandem.utils.CompareBinaries.set_files'
        if not self.Success:
            rep.cancel(f)
            return
        mes1 = _('File {}: ').format(1)
        mes2 = _('File {}: ').format(2)
        file1 = com.input_str(mes1)
        file2 = com.input_str(mes2)
        if not file1 or not file2:
            self.Success = False
            rep.empty(f)
            return
        self.reset(file1, file2)
    
    def reset(self, file1='', file2=''):
        if self.bin1:
            self.close()
        if file1 and file2:
            self.set_values()
            self.bin1 = gt.Binary(file1)
            self.bin2 = gt.Binary(file2)
            self.Success = self.bin1.Success and self.bin2.Success
        else:
            self.set_files()
        
    def dump(self):
        f = '[MClient] plugins.multitrandem.utils.CompareBinaries.dump'
        if not self.Success:
            rep.cancel(f)
            return
        mes = _('This will extract binary data from both files from set positions')
        print(mes)
        mes1 = _('Position {}: ').format(1)
        mes2 = _('Position {}: ').format(2)
        pos1 = com.input_int(mes1)
        pos2 = com.input_int(mes2)
        if pos1 >= pos2:
            sub = f'{pos1} < {pos2}'
            mes = _('The condition "{}" is not observed!').format(sub)
            Message(f, mes).show_warning()
            return
        chunk1 = self.bin1.read(pos1, pos2)
        chunk2 = self.bin2.read(pos1, pos2)
        if not chunk1 or not chunk2:
            rep.empty(f)
            return
        try:
            mes = _('Write "{}"').format(DUMP1)
            Message(f, mes).show_info()
            with open(DUMP1, 'wb') as f1:
                f1.write(chunk1)
            mes = _('Write "{}"').format(DUMP2)
            Message(f, mes).show_info()
            with open(DUMP2, 'wb') as f2:
                f2.write(chunk2)
        except Exception as e:
            mes = _('Operation has failed!\n\nDetails: {}')
            mes = mes.format(e)
            Message(f, mes).show_warning()
    
    def go_end(self):
        f = '[MClient] plugins.multitrandem.utils.CompareBinaries.go_end'
        if not self.Success:
            rep.cancel(f)
            return
        min_ = min(self.bin1.get_file_size(), self.bin2.get_file_size())
        self.pos = min_ - self.buffer
        if self.pos < 0:
            self.pos = 0
        self.load()
    
    def go_start(self):
        f = '[MClient] plugins.multitrandem.utils.CompareBinaries.go_start'
        if not self.Success:
            rep.cancel(f)
            return
        self.pos = 0
        self.load()
    
    def clear(self):
        f = '[MClient] plugins.multitrandem.utils.CompareBinaries.clear'
        if not self.Success:
            rep.cancel(f)
            return
        try:
            if OS.is_win():
                os.system('cls')
            else:
                os.system('clear')
        except Exception as e:
            mes = _('Operation has failed!\n\nDetails: {}')
            mes = mes.format(e)
            Message(f, mes).show_error()
    
    def set_pos(self):
        f = '[MClient] plugins.multitrandem.utils.CompareBinaries.set_pos'
        if not self.Success:
            rep.cancel(f)
            return
        mes = _('Enter a position to go or press Return to keep the current one ({}): ')
        mes = mes.format(shcom.set_figure_commas(self.pos))
        val = input(mes)
        val = val.strip()
        if not val:
            rep.lazy(f)
            return
        val = Input(f, val).get_integer()
        if val < 0:
            mes = _('Wrong input data!')
            Message(f, mes).show_warning()
            return
        self.pos = val
    
    def set_values(self):
        self.poses = []
        self.posmov = []
        self.coms = ['buffer', 'help', 'load', 'quit', 'pgup', 'pgdn', 'next'
                    ,'prev', 'pos', 'clear', 'exit', 'dump', 'files','q','same'
                    ]
        self.chunks1 = b''
        self.chunks2 = b''
        self.buffer = BUFFER
        self.pos = 0
        self.Success = True
        self.bin1 = None
        self.bin2 = None
        self.lastcom = ''
        self.coms.sort()
    
    def go_prev(self):
        f = '[MClient] plugins.multitrandem.utils.CompareBinaries.go_prev'
        if not self.Success:
            rep.cancel(f)
            return
        while True:
            start = self.pos - self.buffer
            if start < 0:
                start = 0
            end = start + self.buffer
            self.compare(start, end)
            if not self.chunks1 or not self.chunks2 or start <= 0:
                break
            self.pos -= self.buffer
            if self.pos < 0:
                self.pos = 0
            if self.poses:
                break
        self.report()
        self.print()
    
    def go_next(self):
        f = '[MClient] plugins.multitrandem.utils.CompareBinaries.go_next'
        if not self.Success:
            rep.cancel(f)
            return
        while True:
            start = self.pos + self.buffer
            end = start + self.buffer
            self.compare(start, end)
            if not self.chunks1 or not self.chunks2:
                break
            self.pos += self.buffer
            if self.poses:
                break
        self.report()
        self.print()
    
    def go_page_down(self):
        f = '[MClient] plugins.multitrandem.utils.CompareBinaries.go_page_down'
        if not self.Success:
            rep.cancel(f)
            return
        self.pos += self.buffer
        min_ = min(self.bin1.get_file_size(), self.bin2.get_file_size())
        if self.pos >= min_:
            self.pos = min_ - self.buffer
            if self.pos < 0:
                self.pos = 0
        self.load()
    
    def go_page_up(self):
        f = '[MClient] plugins.multitrandem.utils.CompareBinaries.go_page_up'
        if not self.Success:
            rep.cancel(f)
            return
        self.pos -= self.buffer
        if self.pos < 0:
            self.pos = 0
        self.load()
    
    def load(self):
        f = '[MClient] plugins.multitrandem.utils.CompareBinaries.load'
        if not self.Success:
            rep.cancel(f)
            return
        start = self.pos
        end = start + self.buffer
        if start > self.bin1.get_file_size() \
        or start > self.bin2.get_file_size():
            start = 0
        if end > self.bin1.get_file_size() \
        or end > self.bin2.get_file_size():
            end = min(self.bin1.get_file_size(), self.bin2.get_file_size())
        self.compare(start, end)
        self.report()
        self.print()
    
    def set_buffer(self):
        f = '[MClient] plugins.multitrandem.utils.CompareBinaries.set_buffer'
        if not self.Success:
            rep.cancel(f)
            return
        mes = _('Enter a buffer size or press Return to keep the current one ({}): ')
        mes = mes.format(shcom.set_figure_commas(self.buffer))
        val = input(mes)
        val = val.strip()
        if not val:
            rep.lazy(f)
            return
        val = Input(title=f, value=val).get_integer()
        if not val:
            mes = _('Wrong input data!')
            Message(f, mes).show_warning()
            return
        self.buffer = val
    
    def show_help(self):
        f = '[MClient] plugins.multitrandem.utils.CompareBinaries.show_help'
        if not self.Success:
            rep.cancel(f)
            return
        mes = _('Available commands: {}')
        mes = mes.format('; '.join(self.coms))
        print(mes)
    
    def show_menu(self, command=''):
        f = '[MClient] plugins.multitrandem.utils.CompareBinaries.show_menu'
        if not self.Success:
            rep.cancel(f)
            return
        if not command:
            try:
                command = input(_('Enter a command: '))
            except (EOFError, KeyboardInterrupt):
                command = 'quit'
            command = command.strip()
            if command and command != 'same':
                self.lastcom = command
        if command == 'buffer':
            self.set_buffer()
            self.load()
            self.show_menu()
        elif command == 'clear':
            self.clear()
            self.show_menu()
        elif command == 'dump':
            self.dump()
            self.show_menu()
        elif command == 'end':
            self.go_end()
            self.show_menu()
        elif command == 'files':
            self.set_files()
            self.show_menu()
        elif command == 'help':
            self.show_help()
            self.show_menu()
        elif command == 'load':
            self.load()
            self.show_menu()
        elif command == 'next':
            self.go_next()
            self.show_menu()
        elif command == 'pgdn':
            self.go_page_down()
            self.show_menu()
        elif command == 'pgup':
            self.go_page_up()
            self.show_menu()
        elif command == 'pos':
            self.set_pos()
            self.load()
            self.show_menu()
        elif command == 'prev':
            self.go_prev()
            self.show_menu()
        elif command in ('q', 'exit', 'quit'):
            self.quit()
        elif command in ('', 'same'):
            self.show_menu(self.lastcom)
        elif command == 'start':
            self.go_start()
            self.show_menu()
        else:
            mes = _('An unknown command! Enter "help" to get help.')
            print(mes)
            self.show_menu()
    
    def quit(self):
        f = '[MClient] plugins.multitrandem.utils.CompareBinaries.quit'
        if not self.Success:
            rep.cancel(f)
            return
        self.close()
        mes = _('Goodbye!')
        Message(f, mes).show_debug()
    
    def is_changed(self, i):
        f = '[MClient] plugins.multitrandem.utils.CompareBinaries.is_changed'
        if not self.Success:
            rep.cancel(f)
            return
        if i in self.poses:
            return True
    
    def print(self):
        f = '[MClient] plugins.multitrandem.utils.CompareBinaries.print'
        if not self.Success:
            rep.cancel(f)
            return
        mes = _('Chunk 1:')
        Message(f, mes).show_debug()
        for i in range(len(self.chunks1)):
            sym = self.chunks1[i:i+1]
            sym = str(sym)[2:-1]
            if self.is_changed(i):
                sym = termcolor.colored(sym, COLOR)
            sys.stdout.write(sym)
        print()
        mes = _('Chunk 2:')
        Message(f, mes).show_debug()
        for i in range(len(self.chunks2)):
            sym = self.chunks2[i:i+1]
            sym = str(sym)[2:-1]
            if self.is_changed(i):
                sym = termcolor.colored(sym, COLOR)
            sys.stdout.write(sym)
        print()
    
    def report(self):
        f = '[MClient] plugins.multitrandem.utils.CompareBinaries.report'
        if not self.Success:
            rep.cancel(f)
            return
        self.clear()
        sub = shcom.set_figure_commas(self.pos)
        mes = _('Current position: {}').format(sub)
        print(mes)
    
    def compare(self, start=0, end=400):
        f = '[MClient] plugins.multitrandem.utils.CompareBinaries.compare'
        if not self.Success:
            rep.cancel(f)
            return
        self.poses = []
        self.chunks1 = self.bin1.read(start, end)
        self.chunks2 = self.bin2.read(start, end)
        if not self.chunks1 or not self.chunks2:
            self.chunks1 = b''
            self.chunks2 = b''
            rep.empty(f)
            return
        # Checking this condition speeds up processing
        if self.chunks1 != self.chunks2:
            min_ = min(len(self.chunks1), len(self.chunks2))
            for i in range(min_):
                if self.chunks1[i:i+1] != self.chunks2[i:i+1]:
                    self.poses.append(i)
    
    def close(self):
        f = '[MClient] plugins.multitrandem.utils.CompareBinaries.close'
        if not self.Success:
            rep.cancel(f)
            return
        self.bin1.close()
        self.bin2.close()


com = Commands()


if __name__ == '__main__':
    gt.PATH = '/home/pete/.config/mclient/dics'
    #gt.DEBUG = True
    # max_len: 5 => \xbf\x11\x7f\x08u
    #Tests().compare_bytes(5)
    #Tests().analyze_dumps()
    #Tests().navigate_article()
    #Tests().navigate_glue()
    #Tests().parse_glue()
    #Navigate('/home/pete/tmp/unknown').show_menu()
    #file = '/home/pete/tmp/dump_zerah'
    #file = '/home/pete/.wine/drive_c/mt_demo_mln/Network/eng_rus/dict.ert'
    #Navigate(file).show_menu()
    #Tests().corrupt()
    Tests().compare()
    #Tests().navigate()
    #Tests().show_dumps()
    #Tests().get_patch()
    #Tests().gen_patterns()
    #Tests().analyze_xor()
    #file1 = '/tmp/dict.ert'
    #file2 = '/home/pete/.wine/drive_c/setup/Multitran/network/eng_rus/dict.ert'
    #file1 = '/home/pete/tmp/Multitran/network/eng_rus/typein.er'
    #file2 = '/home/pete/.wine/drive_c/setup/Multitran/network/eng_rus/typein.er'
    #file1 = '/home/pete/tmp/Multitran/network/eng_rus/dict.ert'
    #file1 = '/tmp/dict.ert (paramount)'
    #file2 = '/tmp/dict.ert (paramounu)'
    #CompareBinaries(file1, file2).show_menu()
