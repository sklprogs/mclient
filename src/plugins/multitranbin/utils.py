#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sys
import struct
import codecs
import termcolor

import skl_shared.shared as sh
from skl_shared.localize import _
import get as gt


COLOR  = 'cyan'
BUFFER = 200
DUMP1  = sh.Home().add('tmp','dump1')
DUMP2  = sh.Home().add('tmp','dump2')


class Tests:
    
    def navigate(self):
        Navigate(sh.Home().add('tmp','test.bin')).show_menu()
    
    def analyze_dumps(self):
        f = '[MClient] plugins.multitranbin.utils.Tests.analyze_dumps'
        iparse1 = Parser(DUMP1)
        iparse2 = Parser(DUMP2)
        pos1 = 0
        pos2 = min(iparse1.get_file_size(),iparse2.get_file_size())
        iparse1.reader(pos1,pos2)
        iparse2.reader(pos1,pos2)
        iparse1.parse_article()
        iparse2.parse_article()
        if iparse1.Success and iparse2.Success:
            lens11 = [len(chunk) for chunk in iparse1.chunks1]
            lens12 = [len(chunk) for chunk in iparse1.chunks2]
            lens21 = [len(chunk) for chunk in iparse2.chunks1]
            lens22 = [len(chunk) for chunk in iparse2.chunks2]
            len11  = len(iparse1.chunks1)
            len12  = len(iparse1.chunks2)
            len21  = len(iparse2.chunks1)
            len22  = len(iparse2.chunks2)
            mes = 'len(iparse1.chunks1): {}'.format(len11)
            sh.objs.mes(f,mes,True).debug()
            mes = 'len(iparse1.chunks2): {}'.format(len12)
            sh.objs.mes(f,mes,True).debug()
            mes = 'len(iparse2.chunks1): {}'.format(len21)
            sh.objs.mes(f,mes,True).debug()
            mes = 'len(iparse2.chunks2): {}'.format(len22)
            sh.objs.mes(f,mes,True).debug()
            max_ = max(len11,len12,len21,len22)
            nos = [i + 1 for i in range(max_)]
            headers = ('NO','D1P1','D1P2','D2P1','D2P2')
            iterable = [nos,lens11,lens12,lens21,lens22]
            mes = sh.FastTable (headers  = headers
                               ,iterable = iterable
                               ).run()
            sh.com.fast_debug(mes)
            mes  = 'len11: {}'.format(len11) + '\n'
            mes += 'len12: {}'.format(len12) + '\n'
            mes += 'len21: {}'.format(len21) + '\n'
            mes += 'len22: {}'.format(len22) + '\n'
            sh.com.fast_debug(mes)
            '''
            lens11 = sorted(set(lens11))
            lens12 = sorted(set(lens12))
            lens21 = sorted(set(lens21))
            lens22 = sorted(set(lens22))
            '''
            '''
            mes  = 'D1P1:\n' + str(lens11) + '\n\n'
            mes += 'D1P2:\n' + str(lens12) + '\n\n'
            mes += 'D2P1:\n' + str(lens21) + '\n\n'
            mes += 'D2P2:\n' + str(lens22) + '\n\n'
            '''
            '''
            lens21 = [item for item in lens21 if item not in lens11]
            lens22 = [item for item in lens22 if item not in lens12]
            mes  = 'UNIQUE lens21:\n' + str(lens21) + '\n\n'
            mes += 'UNIQUE lens22:\n' + str(lens22) + '\n\n'
            '''
            lens21 = [item for item in lens21 if item in lens11]
            lens22 = [item for item in lens22 if item in lens12]
            mes  = 'SHARED lens21:\n' + str(lens21) + '\n\n'
            mes += 'SHARED lens22:\n' + str(lens22) + '\n\n'
            sh.com.fast_debug(mes)
        else:
            sh.com.empty(f)
        iparse1.close()
        iparse2.close()
    
    def compare_bytes(self,maxlen=10):
        f = '[MClient] plugins.multitranbin.utils.Tests.compare_bytes'
        dump1 = gt.Binary(DUMP1)
        dump2 = gt.Binary(DUMP2)
        end1  = dump1.get_file_size()
        end2  = dump2.get_file_size()
        read1 = dump1.read(0,end1)
        read2 = dump2.read(0,end2)
        if read1 and read2:
            if len(read1) > maxlen and len(read2) > maxlen:
                sex = gt.com.get_subseq(read2,maxlen)
                matches = [seq for seq in sex if seq in read1]
                if matches:
                    matches = [gt.com.get_string(match,0) \
                               for match in matches
                              ]
                    for i in range(len(matches)):
                        matches[i] = '{}: {}'.format(i,matches[i])
                    mes = '\n'.join(matches)
                    sh.com.fast_debug(mes)
                else:
                    mes = _('No matches!')
                    sh.objs.mes(f,mes).info()
            else:
                sh.com.lazy(f)
        else:
            sh.com.empty(f)
        dump1.close()
        dump2.close()
    
    def show_dumps(self):
        CompareBinaries(DUMP1,DUMP2).show_menu()
    
    def get_shared_dumps(self):
        f = '[MClient] plugins.multitranbin.utils.Tests.get_shared_dumps'
        pos1 = 0
        pos2 = 16380
        ''' We do not use 'self._parse' here since 'Parser.parse'
            automatically selects the mode based on a file name.
        '''
        iparse1 = Parser(DUMP1)
        iparse1.reader(pos1,pos2)
        iparse1.parse_article()
        iparse2 = Parser(DUMP2)
        iparse2.reader(pos1,pos2)
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
            sh.com.fast_debug(mes)
        else:
            sh.com.empty(f)
    
    def parse_dumps(self):
        pos1 = 0
        pos2 = 16380
        ''' We do not use 'self._parse' here since 'Parser.parse'
            automatically selects the mode based on a file name.
        '''
        iparse = Parser(DUMP1)
        iparse.reader(pos1,pos2)
        iparse.parse_article()
        iparse.debug()
        iparse = Parser(DUMP2)
        iparse.reader(pos1,pos2)
        iparse.parse_article()
        iparse.debug()
    
    def _parse(self,file,pos1,pos2):
        iparse = Parser(file)
        iparse.reader(pos1,pos2)
        iparse.parse()
        iparse.debug()
    
    def parse_article(self):
        file = gt.objs.files().iwalker.get_article()
        pos1 = 655363
        pos2 = 656808
        self._parse(file,pos1,pos2)
    
    def parse_stems(self):
        file = gt.objs.files().iwalker.get_stems1()
        pos1 = 7479299
        pos2 = 7486690
        self._parse(file,pos1,pos2)
    
    def compare(self):
        file1 = '/home/pete/tmp/Multitran/network/eng_rus/dict.ert'
        file2 = '/home/pete/.wine/drive_c/Multitran/network/eng_rus/dict.ert'
        CompareBinaries(file1,file2).show_menu()
    
    def navigate_article(self):
        Navigate(gt.objs.files().iwalker.get_article()).show_menu()



class Parser(gt.Binary):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.chunks1 = []
        self.chunks2 = []
        self.xplain1 = []
        self.xplain2 = []
    
    def parse_article(self):
        f = '[MClient] plugins.multitranbin.utils.Binary.parse_article'
        if self.Success:
            for chunk in self.chunks1:
                chunk = gt.com.get_string(chunk,0)
                self.xplain1.append(chunk)
            for chunk in self.chunks2:
                chunk = gt.com.get_string(chunk,0)
                self.xplain2.append(chunk)
        else:
            sh.com.cancel(f)
    
    def debug(self):
        f = '[MClient] plugins.multitranbin.utils.Binary.debug'
        if self.Success:
            if self.xplain1 and self.xplain2:
                if len(self.xplain1) == len(self.xplain2):
                    nos = [i + 1 for i in range(len(self.xplain1))]
                    len1 = [len(chunk) for chunk in self.chunks1]
                    len2 = [len(chunk) for chunk in self.chunks2]
                    headers = ('NOS','LEN1','PART1','LEN2','PART2')
                    iterable = (nos,len1,self.xplain1,len2,self.xplain2)
                    mes = sh.FastTable (headers  = headers
                                       ,iterable = iterable
                                       ,maxrow   = 45
                                       ).run()
                    if mes:
                        sub = _('File: "{}"').format(self.file)
                        sub += '\n\n'
                        mes = sub + mes
                        sh.com.fast_debug(mes)
                    else:
                        sh.com.empty(f)
                else:
                    self.Success = False
                    sub = '{} == {}'.format (len(self.xplain1)
                                            ,len(self.xplain2)
                                            )
                    mes = _('The condition "{}" is not observed!')
                    mes = mes.format(sub)
                    sh.objs.mes(f,mes,True).warning()
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
        
    def chunk7(self,chunk):
        f = '[MClient] plugins.multitranbin.utils.Binary.chunk7'
        ''' According to "libmtquery-0.0.1alpha3/doc/README.rus":
            the 1st byte - a type designating the use of capital letters
            (not used), further - a vector of 7-byte codes, each code
            including:
            3 bytes - a word number (4-byte long type compressed to
            3 bytes)
            2 bytes - sik (terminations)
            2 bytes - lgk (speech part codes)
        '''
        if self.Success:
            if chunk and (len(chunk) - 1) % 7 == 0:
                tmp    = []
                chunks = gt.com.get_chunks(chunk[1:],7)
                for item in chunks:
                    delta = 7 - len(item)
                    item  = item + b'\x00' * delta
                    word  = item[0:3] + b'\x00'
                    sik   = item[3:5]
                    lgk   = item[5:7]
                    tmp.append(struct.unpack('<L',word)[0])
                    tmp.append(struct.unpack('<h',sik)[0])
                    tmp.append(struct.unpack('<h',lgk)[0])
                return tmp
        else:
            sh.com.cancel(f)
    
    def parsel1(self):
        f = '[MClient] plugins.multitranbin.utils.Binary.parsel1'
        if self.Success:
            for chunk in self.chunks1:
                chunk = chunk.decode(gt.ENCODING,'replace')
                self.xplain1.append(chunk)
        else:
            sh.com.cancel(f)
    
    def parse_stem(self):
        f = '[MClient] plugins.multitranbin.utils.Binary.parse_stem'
        if self.Success:
            self.parsel1()
            for chunk in self.chunks2:
                tmp = self.chunk7(chunk)
                if tmp:
                    self.xplain2.append(tmp)
                else:
                    self.xplain2.append([_('UNKNOWN')])
        else:
            sh.com.cancel(f)
    
    def parse(self):
        f = '[MClient] plugins.multitranbin.utils.Binary.parse'
        if self.Success:
            #FIX: Why base names are not lowercased?
            bname = self.bname.lower()
            if bname.startswith('stem'):
                self.parse_stem()
            elif bname.startswith('dict') and bname.endswith('t'):
                self.parse_article()
            else:
                mes = '"{}"'.format(self.bname)
                sh.objs.mes(f,mes,True).debug()
                mes = _('Not implemented yet!')
                sh.objs.mes(f,mes).info()
        else:
            sh.com.cancel(f)
    
    def reader(self,pos1,pos2):
        f = '[MClient] plugins.multitranbin.utils.Binary.reader'
        if self.Success:
            stream = self.read(pos1,pos2)
            if stream:
                self.chunks1 = []
                self.chunks2 = []
                pos = 0
                while pos + 2 < len(stream):
                    ''' #NOTE: indexing returns integers, slicing
                               returns bytes.
                    '''
                    read = stream[pos:pos+2]
                    pos += 2
                    len1, len2 = struct.unpack('<2b',read)
                    len1 = gt.com.overflowb(len1)
                    len2 = gt.com.overflowb(len2)
                    if pos + len1 + len2 < len(stream):
                        ''' Do this only after checking the condition,
                            otherwise, resulting lists will have
                            a different length.
                        '''
                        chunk1 = stream[pos:pos+len1]
                        pos += len1
                        chunk2 = stream[pos:pos+len2]
                        pos += len2
                        # Zero-length chunks should be allowed
                        if chunk2:
                            self.chunks1.append(chunk1)
                            self.chunks2.append(chunk2)
                    else:
                        gt.com.report_status(pos,stream)
                        break
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)



class Navigate(gt.Binary):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.chunk = b''
        self.coms = ['buffer','help','load','quit','pgup','pgdn'
                    ,'pos','clear','exit','dump','find','findprev'
                    ,'findnext','findtext','findbytes'
                    ]
        self.buffer = round(BUFFER * 2.5)
        self.border = 20
        self.pos = 0
        self.spos = None
        self.coded = b''
        self.lastcom = ''
        self.coms.sort()
    
    def find_prev(self):
        f = '[MClient] plugins.multitranbin.utils.Navigate.find_prev'
        if self.Success:
            if self.coded:
                if self.spos is None or self.spos == 0:
                    mes = _('No matches!')
                    sh.objs.mes(f,mes,True).info()
                else:
                    spos = self.imap.rfind(self.coded,0,self.spos)
                    if spos == -1:
                        mes = _('No matches!')
                        sh.objs.mes(f,mes,True).info()
                    else:
                        self.spos = spos
                        self._print_found()
            else:
                self.find_nav()
        else:
            sh.com.cancel(f)
    
    def find_next(self):
        f = '[MClient] plugins.multitranbin.utils.Navigate.find_next'
        if self.Success:
            if self.coded:
                if self.spos is None:
                    mes = _('No matches!')
                    sh.objs.mes(f,mes,True).info()
                else:
                    spos = self.spos
                    if spos < self.get_file_size() - 1:
                        spos += 1
                    else:
                        spos = self.fsize - len(self.coded)
                    spos = self.find(self.coded,spos)
                    if spos is None:
                        mes = _('No matches!')
                        sh.objs.mes(f,mes,True).info()
                    else:
                        self.spos = spos
                        self._print_found()
            else:
                self.find_nav()
        else:
            sh.com.cancel(f)
    
    def _print_found(self):
        f = '[MClient] plugins.multitranbin.utils.Navigate._print_found'
        if self.spos is None:
            mes = _('No matches!')
            sh.objs.mes(f,mes,True).info()
        else:
            if self.spos > self.border:
                pos1 = self.spos - self.border
                chunk1 = self.read(pos1,self.spos)
            elif self.spos:
                chunk1 = self.read(0,self.spos)
            else:
                chunk1 = b''
            min_ = min(self.buffer,self.get_file_size())
            ch2_len = min_ - len(chunk1) - len(self.coded)
            if ch2_len > 0:
                pos1 = self.spos + len(self.coded)
                pos2 = pos1 + ch2_len
                chunk2 = self.read(pos1,pos2)
            else:
                chunk2 = b''
            buffer1 = gt.com.get_string(chunk1,0)
            buffer2 = gt.com.get_string(self.coded,0)
            buffer2 = termcolor.colored(buffer2,COLOR)
            buffer3 = gt.com.get_string(chunk2,0)
            sys.stdout.write(buffer1)
            sys.stdout.write(buffer2)
            print(buffer3)
    
    def _find(self):
        f = '[MClient] plugins.multitranbin.utils.Navigate._find'
        spos = self.find(self.coded)
        if spos is None:
            mes = _('No matches!')
            sh.objs.mes(f,mes,True).info()
        else:
            self.spos = spos
            self._print_found()
    
    def find_text(self):
        f = '[MClient] plugins.multitranbin.utils.Navigate.find_text'
        if self.Success:
            pattern = com.input_str(_('Enter text to search for: '))
            self.coded = bytes(pattern,gt.ENCODING)
            self._find()
        else:
            sh.com.cancel(f)
    
    def find_bytes(self):
        f = '[MClient] plugins.multitranbin.utils.Navigate.find_bytes'
        if self.Success:
            pattern = com.input_str(_('Enter bytes to search for: '))
            try:
                pattern = codecs.decode(pattern,'unicode_escape')
                self.coded = pattern.encode('latin1')
            except Exception as e:
                self.coded = b''
                mes = _('Operation has failed!\n\nDetails: {}')
                mes = mes.format(e)
                sh.objs.mes(f,mes,True).warning()
            self._find()
        else:
            sh.com.cancel(f)
    
    def find_nav(self):
        f = '[MClient] plugins.multitranbin.utils.Navigate.find_nav'
        if self.Success:
            choice = input(_('Search for text instead of bytes? Y/n '))
            choice = choice.strip()
            if choice in ('','y','Y'):
                self.find_text()
            elif choice in ('n','N'):
                self.find_bytes()
            else:
                self.find_nav()
        else:
            sh.com.cancel(f)
        
    def dump(self):
        f = '[MClient] plugins.multitranbin.utils.Navigate.dump'
        if self.Success:
            mes = _('This will extract data from the binary file from set positions')
            print(mes)
            mes1 = _('Position {}: ').format(1)
            mes2 = _('Position {}: ').format(2)
            pos1 = com.input_int(mes1)
            pos2 = com.input_int(mes2)
            if pos1 < pos2:
                mes = _('An output file: ')
                filew = com.input_str(mes)
                if filew:
                    if sh.com.rewrite(filew):
                        chunk = self.read(pos1,pos2)
                        if chunk:
                            try:
                                mes = _('Write "{}"').format(filew)
                                sh.objs.mes(f,mes,True).info()
                                with open(filew,'wb') as fw:
                                    fw.write(chunk)
                            except Exception as e:
                                mes = _('Operation has failed!\n\nDetails: {}')
                                mes = mes.format(e)
                                sh.objs.mes(f,mes,True).warning()
                        else:
                            sh.com.empty(f)
                    else:
                        mes = _('Operation has been canceled by the user.')
                        sh.objs.mes(f,mes,True).info()
                else:
                    sh.com.empty(f)
            else:
                sub = '{} < {}'.format(pos1,pos2)
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                sh.objs.mes(f,mes,True).warning()
        else:
            sh.com.cancel(f)
    
    def go_end(self):
        f = '[MClient] plugins.multitranbin.utils.Navigate.go_end'
        if self.Success:
            self.pos = self.get_file_size() - self.buffer
            if self.pos < 0:
                self.pos = 0
            self.load()
        else:
            sh.com.cancel(f)
    
    def go_start(self):
        f = '[MClient] plugins.multitranbin.utils.Navigate.go_start'
        if self.Success:
            self.pos = 0
            self.load()
        else:
            sh.com.cancel(f)
    
    def clear(self):
        f = '[MClient] plugins.multitranbin.utils.Navigate.clear'
        if self.Success:
            try:
                if sh.objs.os().win():
                    os.system('cls')
                else:
                    os.system('clear')
            except Exception as e:
                mes = _('Operation has failed!\n\nDetails: {}')
                mes = mes.format(e)
                sh.objs.mes(f,mes,True).error()
        else:
            sh.com.cancel(f)
    
    def set_pos(self):
        f = '[MClient] plugins.multitranbin.utils.Navigate.set_pos'
        if self.Success:
            mes = _('Enter a position to go or press Return to keep the current one ({}): ')
            mes = mes.format(sh.com.figure_commas(self.pos))
            val = input(mes)
            val = val.strip()
            if val:
                val = sh.Input (title = f
                               ,value = val
                               ).integer()
                if val >= 0:
                    self.pos = val
                else:
                    mes = _('Wrong input data!')
                    sh.objs.mes(f,mes,True).warning()
            else:
                sh.com.lazy(f)
        else:
            sh.com.cancel(f)
    
    def go_page_down(self):
        f = '[MClient] plugins.multitranbin.utils.Navigate.go_page_down'
        if self.Success:
            self.pos += self.buffer
            if self.pos >= self.get_file_size():
                self.pos = self.get_file_size() - self.buffer
                if self.pos < 0:
                    self.pos = 0
            self.load()
        else:
            sh.com.cancel(f)
    
    def go_page_up(self):
        f = '[MClient] plugins.multitranbin.utils.Navigate.go_page_up'
        if self.Success:
            self.pos -= self.buffer
            if self.pos < 0:
                self.pos = 0
            self.load()
        else:
            sh.com.cancel(f)
    
    def load(self):
        f = '[MClient] plugins.multitranbin.utils.Navigate.load'
        if self.Success:
            start = self.pos
            end = start + self.buffer
            if start > self.get_file_size():
                start = 0
            if end > self.get_file_size():
                end = self.get_file_size()
            self.chunk = self.read(start,end)
            self.report()
            self.print()
        else:
            sh.com.cancel(f)
    
    def set_buffer(self):
        f = '[MClient] plugins.multitranbin.utils.Navigate.set_buffer'
        if self.Success:
            mes = _('Enter a buffer size or press Return to keep the current one ({}): ')
            mes = mes.format(sh.com.figure_commas(self.buffer))
            val = input(mes)
            val = val.strip()
            if val:
                val = sh.Input (title = f
                               ,value = val
                               ).integer()
                if val:
                    self.buffer = val
                else:
                    mes = _('Wrong input data!')
                    sh.objs.mes(f,mes,True).warning()
            else:
                sh.com.lazy(f)
        else:
            sh.com.cancel(f)
    
    def show_help(self):
        f = '[MClient] plugins.multitranbin.utils.Navigate.show_help'
        if self.Success:
            mes = _('Available commands: {}')
            mes = mes.format('; '.join(self.coms))
            print(mes)
        else:
            sh.com.cancel(f)
    
    def show_menu(self,command=''):
        f = '[MClient] plugins.multitranbin.utils.Navigate.show_menu'
        if self.Success:
            if not command:
                try:
                    command = input(_('Enter a command: '))
                except (EOFError,KeyboardInterrupt):
                    command = 'quit'
                command = command.strip()
                if command != 'same':
                    self.lastcom = command
            if command in ('','exit','quit'):
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
            elif command == 'same':
                self.show_menu(self.lastcom)
            elif command == 'start':
                self.go_start()
                self.show_menu()
            else:
                mes = _('An unknown command! Enter "help" to get help.')
                print(mes)
                self.show_menu()
        else:
            sh.com.cancel(f)
    
    def quit(self):
        f = '[MClient] plugins.multitranbin.utils.Navigate.quit'
        if self.Success:
            self.close()
            mes = _('Goodbye!')
            sh.objs.mes(f,mes,True).debug()
        else:
            sh.com.cancel(f)
    
    def print(self):
        f = '[MClient] plugins.multitranbin.utils.Navigate.print'
        if self.Success:
            mes = gt.com.get_string(self.chunk,0)
            print(mes)
        else:
            sh.com.cancel(f)
    
    def report(self):
        f = '[MClient] plugins.multitranbin.utils.Navigate.report'
        if self.Success:
            self.clear()
            sub = sh.com.figure_commas(self.pos)
            mes = _('Current position: {}').format(sub)
            print(mes)
        else:
            sh.com.cancel(f)



class Commands:
    
    def input_str(self,mes=''):
        f = '[MClient] plugins.multitranbin.utils.Commands.input_str'
        if not mes:
            mes = _('Input a string: ')
        try:
            return input(mes)
        except (EOFError,KeyboardInterrupt):
            return ''
    
    def input_int(self,mes=''):
        f = '[MClient] plugins.multitranbin.utils.Commands.input_int'
        if not mes:
            mes = _('Input an integer: ')
        try:
            val = input(mes)
        except (EOFError,KeyboardInterrupt):
            val = 0
        return sh.Input (title = f
                        ,value = val
                        ).integer()



class CompareBinaries:
    
    def __init__(self,file1='',file2=''):
        self.set_values()
        self.reset(file1,file2)
    
    def set_files(self):
        f = '[MClient] plugins.multitranbin.utils.CompareBinaries.set_files'
        if self.Success:
            mes1  = _('File {}: ').format(1)
            mes2  = _('File {}: ').format(2)
            file1 = com.input_str(mes1)
            file2 = com.input_str(mes2)
            if file1 and file2:
                self.reset(file1,file2)
            else:
                self.Success = False
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def reset(self,file1='',file2=''):
        if self.bin1:
            self.close()
        if file1 and file2:
            self.set_values()
            self.bin1    = gt.Binary(file1)
            self.bin2    = gt.Binary(file2)
            self.Success = self.bin1.Success and self.bin2.Success
        else:
            self.files()
        
    def dump(self):
        f = '[MClient] plugins.multitranbin.utils.CompareBinaries.dump'
        if self.Success:
            mes = _('This will extract binary data from both files from set positions')
            print(mes)
            mes1 = _('Position {}: ').format(1)
            mes2 = _('Position {}: ').format(2)
            pos1 = com.input_int(mes1)
            pos2 = com.input_int(mes2)
            if pos1 < pos2:
                chunk1 = self.bin1.read(pos1,pos2)
                chunk2 = self.bin2.read(pos1,pos2)
                if chunk1 and chunk2:
                    try:
                        mes = _('Write "{}"').format(DUMP1)
                        sh.objs.mes(f,mes,True).info()
                        with open(DUMP1,'wb') as f1:
                            f1.write(chunk1)
                        mes = _('Write "{}"').format(DUMP2)
                        sh.objs.mes(f,mes,True).info()
                        with open(DUMP2,'wb') as f2:
                            f2.write(chunk2)
                    except Exception as e:
                        mes = _('Operation has failed!\n\nDetails: {}')
                        mes = mes.format(e)
                        sh.objs.mes(f,mes,True).warning()
                else:
                    sh.com.empty(f)
            else:
                sub = '{} < {}'.format(pos1,pos2)
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                sh.objs.mes(f,mes,True).warning()
        else:
            sh.com.cancel(f)
    
    def go_end(self):
        f = '[MClient] plugins.multitranbin.utils.CompareBinaries.go_end'
        if self.Success:
            min_ = min (self.bin1.get_file_size()
                       ,self.bin2.get_file_size()
                       )
            self.pos = min_ - self.buffer
            if self.pos < 0:
                self.pos = 0
            self.load()
        else:
            sh.com.cancel(f)
    
    def go_start(self):
        f = '[MClient] plugins.multitranbin.utils.CompareBinaries.go_start'
        if self.Success:
            self.pos = 0
            self.load()
        else:
            sh.com.cancel(f)
    
    def clear(self):
        f = '[MClient] plugins.multitranbin.utils.CompareBinaries.clear'
        if self.Success:
            try:
                if sh.objs.os().win():
                    os.system('cls')
                else:
                    os.system('clear')
            except Exception as e:
                mes = _('Operation has failed!\n\nDetails: {}')
                mes = mes.format(e)
                sh.objs.mes(f,mes,True).error()
        else:
            sh.com.cancel(f)
    
    def set_pos(self):
        f = '[MClient] plugins.multitranbin.utils.CompareBinaries.set_pos'
        if self.Success:
            mes = _('Enter a position to go or press Return to keep the current one ({}): ')
            mes = mes.format(sh.com.figure_commas(self.pos))
            val = input(mes)
            val = val.strip()
            if val:
                val = sh.Input (title = f
                               ,value = val
                               ).integer()
                if val >= 0:
                    self.pos = val
                else:
                    mes = _('Wrong input data!')
                    sh.objs.mes(f,mes,True).warning()
            else:
                sh.com.lazy(f)
        else:
            sh.com.cancel(f)
    
    def set_values(self):
        self.poses   = []
        self.posmov  = []
        self.coms    = ['buffer','help','load','quit','pgup','pgdn'
                       ,'next','prev','pos','clear','exit','dump'
                       ,'files'
                       ]
        self.chunks1 = b''
        self.chunks2 = b''
        self.buffer  = BUFFER
        self.pos     = 0
        self.Success = True
        self.bin1    = None
        self.bin2    = None
        self.coms.sort()
    
    def go_prev(self):
        f = '[MClient] plugins.multitranbin.utils.CompareBinaries.go_prev'
        if self.Success:
            while True:
                start = self.pos - self.buffer
                if start < 0:
                    start = 0
                end = start + self.buffer
                self.compare(start,end)
                if self.chunks1 and self.chunks2 and start > 0:
                    self.pos -= self.buffer
                    if self.pos < 0:
                        self.pos = 0
                    if self.poses:
                        break
                else:
                    break
            self.report()
            self.print()
        else:
            sh.com.cancel(f)
    
    def go_next(self):
        f = '[MClient] plugins.multitranbin.utils.CompareBinaries.go_next'
        if self.Success:
            while True:
                start = self.pos + self.buffer
                end   = start + self.buffer
                self.compare(start,end)
                if self.chunks1 and self.chunks2:
                    self.pos += self.buffer
                    if self.poses:
                        break
                else:
                    break
            self.report()
            self.print()
        else:
            sh.com.cancel(f)
    
    def go_page_down(self):
        f = '[MClient] plugins.multitranbin.utils.CompareBinaries.go_page_down'
        if self.Success:
            self.pos += self.buffer
            min_ = min (self.bin1.get_file_size()
                       ,self.bin2.get_file_size()
                       )
            if self.pos >= min_:
                self.pos = min_ - self.buffer
                if self.pos < 0:
                    self.pos = 0
            self.load()
        else:
            sh.com.cancel(f)
    
    def go_page_up(self):
        f = '[MClient] plugins.multitranbin.utils.CompareBinaries.go_page_up'
        if self.Success:
            self.pos -= self.buffer
            if self.pos < 0:
                self.pos = 0
            self.load()
        else:
            sh.com.cancel(f)
    
    def load(self):
        f = '[MClient] plugins.multitranbin.utils.CompareBinaries.load'
        if self.Success:
            start = self.pos
            end   = start + self.buffer
            if start > self.bin1.get_file_size() \
            or start > self.bin2.get_file_size():
                start = 0
            if end > self.bin1.get_file_size() \
            or end > self.bin2.get_file_size():
                end = min (self.bin1.get_file_size()
                          ,self.bin2.get_file_size()
                          )
            self.compare(start,end)
            self.report()
            self.print()
        else:
            sh.com.cancel(f)
    
    def set_buffer(self):
        f = '[MClient] plugins.multitranbin.utils.CompareBinaries.set_buffer'
        if self.Success:
            mes = _('Enter a buffer size or press Return to keep the current one ({}): ')
            mes = mes.format(sh.com.figure_commas(self.buffer))
            val = input(mes)
            val = val.strip()
            if val:
                val = sh.Input (title = f
                               ,value = val
                               ).integer()
                if val:
                    self.buffer = val
                else:
                    mes = _('Wrong input data!')
                    sh.objs.mes(f,mes,True).warning()
            else:
                sh.com.lazy(f)
        else:
            sh.com.cancel(f)
    
    def show_help(self):
        f = '[MClient] plugins.multitranbin.utils.CompareBinaries.show_help'
        if self.Success:
            mes = _('Available commands: {}')
            mes = mes.format('; '.join(self.coms))
            print(mes)
        else:
            sh.com.cancel(f)
    
    def show_menu(self):
        f = '[MClient] plugins.multitranbin.utils.CompareBinaries.show_menu'
        if self.Success:
            try:
                command = input(_('Enter a command: '))
            except (EOFError,KeyboardInterrupt):
                command = 'quit'
            command = command.strip()
            if command == '':
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
            elif command in ('exit','quit'):
                self.quit()
            elif command == 'start':
                self.go_start()
                self.show_menu()
            else:
                mes = _('An unknown command! Enter "help" to get help.')
                print(mes)
                self.show_menu()
        else:
            sh.com.cancel(f)
    
    def quit(self):
        f = '[MClient] plugins.multitranbin.utils.CompareBinaries.quit'
        if self.Success:
            self.close()
            mes = _('Goodbye!')
            sh.objs.mes(f,mes,True).debug()
        else:
            sh.com.cancel(f)
    
    def is_changed(self,i):
        f = '[MClient] plugins.multitranbin.utils.CompareBinaries.is_changed'
        if self.Success:
            if i in self.poses:
                return True
        else:
            sh.com.cancel(f)
    
    def print(self):
        f = '[MClient] plugins.multitranbin.utils.CompareBinaries.print'
        if self.Success:
            mes = _('Chunk 1:')
            sh.objs.mes(f,mes,True).debug()
            for i in range(len(self.chunks1)):
                sym = self.chunks1[i:i+1]
                sym = str(sym)[2:-1]
                if self.is_changed(i):
                    sym = termcolor.colored(sym,COLOR)
                sys.stdout.write(sym)
            print()
            mes = _('Chunk 2:')
            sh.objs.mes(f,mes,True).debug()
            for i in range(len(self.chunks2)):
                sym = self.chunks2[i:i+1]
                sym = str(sym)[2:-1]
                if self.is_changed(i):
                    sym = termcolor.colored(sym,COLOR)
                sys.stdout.write(sym)
            print()
        else:
            sh.com.cancel(f)
    
    def report(self):
        f = '[MClient] plugins.multitranbin.utils.CompareBinaries.report'
        if self.Success:
            self.clear()
            sub = sh.com.figure_commas(self.pos)
            mes = _('Current position: {}').format(sub)
            print(mes)
        else:
            sh.com.cancel(f)
    
    def compare(self,start=0,end=400):
        f = '[MClient] plugins.multitranbin.utils.CompareBinaries.compare'
        if self.Success:
            self.poses   = []
            self.chunks1 = self.bin1.read(start,end)
            self.chunks2 = self.bin2.read(start,end)
            if self.chunks1 and self.chunks2:
                # Checking this condition speeds up processing
                if self.chunks1 != self.chunks2:
                    min_ = min(len(self.chunks1),len(self.chunks2))
                    for i in range(min_):
                        if self.chunks1[i:i+1] != self.chunks2[i:i+1]:
                            self.poses.append(i)
            else:
                self.chunks1 = b''
                self.chunks2 = b''
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def close(self):
        f = '[MClient] plugins.multitranbin.utils.CompareBinaries.close'
        if self.Success:
            self.bin1.close()
            self.bin2.close()
        else:
            sh.com.cancel(f)


com = Commands()


if __name__ == '__main__':
    gt.PATH = '/home/pete/.config/mclient/dics'
    gt.DEBUG = True
    # max_len: 5 => \xbf\x11\x7f\x08u
    #Tests().compare_bytes(5)
    #Tests().compare()
    #Tests().show_dumps()
    #Tests().analyze_dumps()
    Tests().navigate_article()
    #Tests().navigate()
