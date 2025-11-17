#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import rep, Message

from sources.dsl.cleanup import CleanUp as DslCleanUp


class CleanUp(DslCleanUp):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def tag_wforms(self):
        self.text = self.text.splitlines()
        for i in range(len(self.text)):
            parts = self.text[i].split('[/dic]')
            if len(parts) == 1:
                continue
            parts[0] += '[/dic]'
            parts[1] = '[wform]' + parts[1] + '[/wform]'
            self.text[i] = parts[0] + parts[1]
        self.text = '\n'.join(self.text)
    
    def run(self):
        f = '[MClient] sources.fora.dsl.cleanup.CleanUp.run'
        if not self.text:
            rep.empty(f)
            return ''
        self.delete_trash()
        self.convert_tags()
        self.tag_wforms()
        return self.text
