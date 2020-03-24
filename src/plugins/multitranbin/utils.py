#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sys
import termcolor

import skl_shared.shared as sh
from skl_shared.localize import _
import get as gt


COLOR  = 'cyan'
BUFFER = 200


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
                mes1 = _('File {}: ').format(1)
                mes2 = _('File {}: ').format(2)
                filew1 = com.input_str(mes1)
                filew2 = com.input_str(mes2)
                if filew1 and filew2:
                    if sh.com.rewrite(filew1) \
                    and sh.com.rewrite(filew2):
                        chunk1 = self.bin1.read(pos1,pos2)
                        chunk2 = self.bin2.read(pos1,pos2)
                        if chunk1 and chunk2:
                            try:
                                mes = _('Write "{}"').format(filew1)
                                sh.objs.mes(f,mes,True).info()
                                with open(filew1,'wb') as f1:
                                    f1.write(chunk1)
                                mes = _('Write "{}"').format(filew2)
                                sh.objs.mes(f,mes,True).info()
                                with open(filew2,'wb') as f2:
                                    f2.write(chunk2)
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
    file1 = '/home/pete/tmp/mt_mod/dict_orig_f.ert'
    file2 = '/home/pete/tmp/mt_mod/dict_mod_f.ert'
    #file1 = '/home/pete/tmp/mt_mod/dict_orig_d.ert'
    #file2 = '/home/pete/tmp/mt_mod/dict_mod_d.ert'
    CompareBinaries(file1,file2).show_menu()
