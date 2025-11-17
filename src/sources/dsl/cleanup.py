#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import rep, Message


class CleanUp:
    
    def __init__(self, text):
        self.text = text
    
    def delete_trash(self):
        while '  ' in self.text:
            self.text = self.text.replace('  ', ' ')
    
    def convert_dic_names(self):
        f = '[MClient] sources.dsl.cleanup.CleanUp.convert_dic_names'
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
    
    def convert_tags(self):
        # Code is unescaped at the step of 'tags', so this should be OK
        self.text = self.text.replace('<', '[')
        self.text = self.text.replace('>', ']')
    
    def add_wforms(self):
        f = '[MClient] sources.dsl.cleanup.CleanUp.add_wforms'
        if self.text.startswith('#'):
            rep.lazy(f)
            return
        self.text = self.text.splitlines()
        self.text[0] = '[wform]' + self.text[0] + '[/wform]'
        self.text = '\n'.join(self.text)
    
    def run(self):
        f = '[MClient] sources.dsl.cleanup.CleanUp.run'
        if not self.text:
            rep.empty(f)
            return ''
        self.delete_trash()
        self.convert_tags()
        self.add_wforms()
        self.convert_dic_names()
        return self.text
