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
    
    def convert_tags(self):
        # Code is unescaped at the step of 'tags', so this should be OK
        self.text = self.text.replace('<', '[')
        self.text = self.text.replace('>', ']')
    
    def run(self):
        f = '[MClient] sources.dsl.cleanup.CleanUp.run'
        if not self.text:
            rep.empty(f)
            return ''
        self.delete_trash()
        self.convert_tags()
        return self.text
