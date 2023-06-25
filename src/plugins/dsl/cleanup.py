#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


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
        f = '[MClient] plugins.dsl.cleanup.TagLike.check'
        if not self.code:
            # Avoid None on output
            self.code = ''
            self.Success = False
            sh.com.rep_empty(f)
    
    def conform(self):
        f = '[MClient] plugins.dsl.cleanup.TagLike.conform'
        if not self.Success:
            sh.com.cancel(f)
            return
        if len(self.start) != len(self.end):
            self.Success = False
            mes = _('Tag-like structures are invalid!')
            sh.objs.get_mes(f, mes, True).show_warning()
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
            sh.objs.get_mes(f, mes, True).show_warning()
    
    def get_start(self):
        f = '[MClient] plugins.dsl.cleanup.TagLike.get_start'
        if not self.Success:
            sh.com.cancel(f)
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
        f = '[MClient] plugins.dsl.cleanup.TagLike.get_end'
        if not self.Success:
            sh.com.cancel(f)
            return
        for pos in self.start:
            self.end.append(self.code.find(']', pos))
    
    def replace(self):
        f = '[MClient] plugins.dsl.cleanup.TagLike.replace'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.start:
            sh.com.rep_lazy(f)
            return
        count = 0
        self.code = list(self.code)
        i = len(self.start) - 1
        while i >= 0:
            if self.start[i] < self.end[i] < len(self.code):
                ''' That should be fine except when tag-like
                    structures are embedded in each other
                    (that should never happen though).
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
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                sh.objs.get_mes(f, mes).show_error()
            i -= 1
        self.code = ''.join(self.code)
        if count:
            mes = _('{} matches').format(count)
            sh.objs.get_mes(f, mes, True).show_debug()



class CleanUp:
    
    def __init__(self, text):
        self.text = text
    
    def delete_trash(self):
        while '  ' in self.text:
            self.text = self.text.replace('  ', ' ')

    def run(self):
        f = '[MClient] plugins.dsl.cleanup.CleanUp.run'
        if not self.text:
            sh.com.rep_empty(f)
            return ''
        self.delete_trash()
        self.text = sh.Text(self.text).delete_unsupported()
        return self.text
