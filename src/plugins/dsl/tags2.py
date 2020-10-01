#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re

import skl_shared.shared as sh
from skl_shared.localize import _

#import plugins.dsl.cleanup as cu
import cleanup as cu

class Tag:
    
    def __init__(self):
        self.text = ''
        self.tags = []



class Tags:
    
    def __init__(self,code,Debug=False):
        self.code = code
        self.Debug = Debug
        self.fragms = []
        self.open = []
        self.Success = True
        self.tagged = []
    
    def _close_tag(self,tag):
        f = '[MClient] plugins.dsl.tags.Tags._close_tag'
        if tag in self.open:
            self.open.remove(tag)
        elif tag == 'm':
            for item in self.open:
                if re.match('m\d+',item):
                    self.open.remove(item)
        elif tag == 'ref':
            for item in self.open:
                if 'ref dict' in item:
                    self.open.remove(item)
        else:
            mes = _('Tag "{}" has not been opened yet!').format(tag)
            sh.objs.get_mes(f,mes,True).show_warning()
    
    def _get_tag_name(self,tag):
        tag = tag[:-1]
        tag = tag.replace('[','',1)
        if tag.startswith('/'):
            tag = tag[1:]
        return tag
    
    def set(self):
        f = '[MClient] plugins.dsl.tags.Tags.set'
        if self.Success:
            # The 1st fragment should always be an article title
            i = 1
            for fragm in self.fragms:
                if fragm.startswith('['):
                    tag = self._get_tag_name(fragm)
                    if fragm.startswith('[/'):
                        self._close_tag(tag)
                    elif not tag in self.open:
                        self.open.append(tag)
                else:
                    itag = Tag()
                    itag.text = fragm
                    itag.tags = list(self.open)
                    self.tagged.append(itag)
                i += 1
        else:
            sh.com.cancel(f)
    
    def delete_trash(self):
        ''' Delete unnecessary items by line (as opposite to
            manipulating the entire code in
            cleanup.CleanUp.delete_trash).
        '''
        f = '[MClient] plugins.dsl.tags.Tags.delete_trash'
        if self.Success:
            self.fragms = [fragm.strip() for fragm in self.fragms \
                           if fragm not in ('\n','\n\t')
                          ]
        else:
            sh.com.cancel(f)
    
    def _debug_code(self):
        return _('Code:') + '\n' + '"{}"'.format(self.code)
    
    def _debug_fragms(self):
        mes = []
        for i in range(len(self.fragms)):
            sub = '{}: "{}"'.format(i+1,self.fragms[i])
            mes.append(sub)
        return _('Fragments:') + '\n' + '\n'.join(mes)
    
    def _debug_tagged(self):
        nos = [i + 1 for i in range(len(self.tagged))]
        texts = [item.text for item in self.tagged]
        tags = [', '.join(item.tags) for item in self.tagged]
        iterable = [nos,tags,texts]
        headers = ('NO','TAGS','TEXT')
        mes = sh.FastTable (iterable = iterable
                           ,headers  = headers
                           ,maxrow   = 50
                           ,maxrows  = 0
                           ).run()
        return _('Tags:') + '\n' + mes
    
    def debug(self):
        f = '[MClient] plugins.dsl.tags.Tags.debug'
        if self.Debug:
            if self.Success:
                mes = [self._debug_code(),self._debug_fragms()
                      ,self._debug_tagged()
                      ]
                mes = '\n\n'.join(mes)
                sh.com.run_fast_debug(f,mes)
            else:
                sh.com.cancel(f)
        else:
            sh.com.rep_lazy(f)
    
    def check(self):
        f = '[MClient] plugins.dsl.tags.Tags.check'
        if not self.code:
            # Avoid None on output
            self.code = ''
            self.Success = False
            sh.com.rep_empty(f)
    
    def split(self):
        f = '[MClient] plugins.dsl.tags.Tags.split'
        if self.Success:
            fragm = ''
            for sym in list(self.code):
                if sym == '[':
                    if fragm:
                        self.fragms.append(fragm)
                    fragm = sym
                elif sym == ']':
                    fragm += sym
                    self.fragms.append(fragm)
                    fragm = ''
                else:
                    fragm += sym
            if fragm:
                self.fragms.append(fragm)
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.check()
        self.split()
        self.delete_trash()
        self.set()
        self.debug()
        return self.code


if __name__ == '__main__':
    f = '__main__'
    sh.com.start()
    file = '/home/pete/bin/mclient/tests/dsl/account balance.txt'
    code = sh.ReadTextFile(file).get()
    code = cu.CleanUp(code).run()
    code = cu.TagLike(code).run()
    Tags(code,True).run()
    sh.com.end()
