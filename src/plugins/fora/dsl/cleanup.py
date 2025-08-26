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
