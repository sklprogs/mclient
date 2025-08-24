#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import rep, Message


"""
class TagLike:
    ''' Replace structures like '\[word\]' with '(word)'. This should be done
        before splitting text to tags. I have tried regular expressions, in
        particular, r'.*\\\[(.+)\\\].*', but that reacts to '\n'.
    '''
    def __init__(self, code):
        self.code = code
        self.end = []
        self.start = []
        self.Success = True
    
    def run(self):
        self.check()
        self.get_start()
        self.get_end()
        self.conform()
        self.replace()
        return self.code
    
    def check(self):
        f = '[MClient] plugins.fora.dsl.cleanup.TagLike.check'
        if not self.code:
            # Avoid None on output
            self.code = ''
            self.Success = False
            rep.empty(f)
    
    def conform(self):
        f = '[MClient] plugins.fora.dsl.cleanup.TagLike.conform'
        if not self.Success:
            rep.cancel(f)
            return
        if len(self.start) != len(self.end):
            self.Success = False
            mes = _('Tag-like structures are invalid!')
            Message(f, mes).show_warning()
            return
        i = 0
        count = 0
        while i < len(self.start):
            if self.end[i] == -1:
                count += 1
                del self.start[i]
                del self.end[i]
                i -= 1
            i += 1
        if count:
            mes = _('Number of invalid tag-like structures: {}')
            mes = mes.format(count)
            Message(f, mes).show_warning()
    
    def get_start(self):
        f = '[MClient] plugins.fora.dsl.cleanup.TagLike.get_start'
        if not self.Success:
            rep.cancel(f)
            return
        pos = 0
        while True:
            pos = self.code.find('\[', pos)
            if pos == -1:
                break
            else:
                self.start.append(pos)
                pos += 1
    
    def get_end(self):
        f = '[MClient] plugins.fora.dsl.cleanup.TagLike.get_end'
        if not self.Success:
            rep.cancel(f)
            return
        for pos in self.start:
            self.end.append(self.code.find(']', pos))
    
    def replace(self):
        f = '[MClient] plugins.fora.dsl.cleanup.TagLike.replace'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.start:
            rep.lazy(f)
            return
        count = 0
        self.code = list(self.code)
        i = len(self.start) - 1
        while i >= 0:
            if self.start[i] < self.end[i] < len(self.code):
                ''' That should be fine except when tag-like structures are
                    embedded in each other (that should never happen though).
                '''
                count += 1
                pos1 = self.end[i] - 1
                pos2 = self.end[i] + 1
                self.code[pos1:pos2] = ')'
                pos1 = self.start[i]
                pos2 = self.start[i] + 2
                self.code[pos1:pos2] = '('
            else:
                sub = f'{self.start[i]} < {self.end[i]} < {len(self.code)}'
                mes = _('The condition "{}" is not observed!').format(sub)
                Message(f, mes, True).show_error()
            i -= 1
        self.code = ''.join(self.code)
        if count:
            mes = _('{} matches').format(count)
            Message(f, mes).show_debug()
"""



class CleanUp:
    
    def __init__(self, text):
        self.text = text
    
    def delete_trash(self):
        while '  ' in self.text:
            self.text = self.text.replace('  ', ' ')
    
    def tag_wforms(self):
        self.text = self.text.splitlines()
        for i in range(len(self.text)):
            parts = self.text[i].split('</dic>')
            if len(parts) == 1:
                continue
            parts[0] += '</dic>'
            parts[1] = '[wform]' + parts[1] + '[/wform]'
            self.text[i] = parts[0] + parts[1]
        self.text = '\n'.join(self.text)
    
    def convert_dic_names(self):
        # Process cases like '#NAME\t"DicTitle (En-Ru)"'
        self.text = self.text.splitlines()
        for i in range(len(self.text)):
            parts = self.text[i].split('#NAME\t"')
            if len(parts) == 1:
                continue
            parts[0] = '[dic]'
            if parts[1].endswith('"'):
                parts[1] = parts[1].rstrip('"')
            parts[1] = parts[1] + '[/dic]'
            self.text[i] = parts[0] + parts[1]
        self.text = '\n'.join(self.text)
    
    def convert_dic_tag(self):
        self.text = self.text.replace('<dic>', '[dic]')
        self.text = self.text.replace('</dic>', '[/dic]')

    def run(self):
        f = '[MClient] plugins.fora.dsl.cleanup.CleanUp.run'
        if not self.text:
            rep.empty(f)
            return ''
        self.delete_trash()
        self.tag_wforms()
        self.convert_dic_names()
        self.convert_dic_tag()
        return self.text
