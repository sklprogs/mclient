#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
from skl_shared.localize import _
from skl_shared.message.controller import Message, rep


class CleanUp:
    
    def __init__(self, text):
        if text is None:
            text = ''
        self.text = text
    
    def delete_trash(self):
        self.text = self.text.replace('\r\n', '\n')
        # Non-breaking space
        self.text = self.text.replace('\xa0', ' ')
        while '  ' in self.text:
            self.text = self.text.replace('  ', ' ')
        self.text = re.sub(r'\>[\s]{0,1}\<', '\><', self.text)
    
    def delete_disamb(self):
        # TODO: Warn about unsupported tags while preserving their contents
        # This is done to speed up and eliminate tag disambiguation
        try:
            self.text = self.text.replace('<i>', '').replace('</i>', '')
            self.text = self.text.replace('<nu />', '')
            self.text = self.text.replace('<abr>', '').replace('</abr>', '')
            self.text = self.text.replace('[/&apos;]', '')
            self.text = self.text.replace('[&apos;]', '')
        # Encoding has failed
        except TypeError:
            self.text = ''
    
    def fix_tags(self):
        #TODO: Use regexp
        # This one is the only that is actually an opening tag
        self.text = self.text.replace('<dtrn\>', '<dtrn>')
        self.text = self.text.replace('</dic\>', '</dic>')
        self.text = self.text.replace('</k\>', '</k>')
        self.text = self.text.replace('</i\>', '</i>')
        self.text = self.text.replace('</c\>', '</c>')
        self.text = self.text.replace('</b\>', '</b>')
        self.text = self.text.replace('</abr\>', '</abr>')
    
    def run(self):
        f = '[MClient] sources.stardict.cleanup.CleanUp.run'
        if not self.text:
            rep.empty(f)
            return ''
        self.delete_trash()
        self.fix_tags()
        self.delete_disamb()
        return self.text
