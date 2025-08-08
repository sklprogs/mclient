#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.message.controller import rep


class CleanUp:
    
    def __init__(self, text):
        if text is None:
            text = ''
        self.text = text

    def delete_trash(self):
        self.text = self.text.replace('m\t', '')
        self.text = self.text.replace('{{с|uk|', '\n')
        self.text = self.text.replace('{{t+|uk|', '\n')
        self.text = self.text.replace('|f}}', '\n')
        self.text = self.text.replace('|alt=', '\n')
        self.text = self.text.replace(' / [[', '\n')
    
    def strip(self):
        lines = self.text.splitlines()
        lines = [line.strip() for line in lines if line.strip()]
        lines = [line for line in lines if not line in ('{{с', '{{t')]
        ''' - For some reason, dictionaries can have duplicated translations.
            - If lines are not sorted, their order can be different each time.
        '''
        lines = sorted(set(lines))
        for i in range(len(lines)):
            if lines[i].startswith('(') and not ')' in lines[i]:
                lines[i] = lines[i].lstrip('(')
            if lines[i].endswith('}}') and not '{{' in lines[i]:
                lines[i] = lines[i].rstrip('}}')
        self.text = '\n'.join(lines)
    
    def delete_unsupported(self):
        self.text = self.text.replace('<u>', '').replace('</u>', '')
    
    def replace_punc(self):
        # Risky, but I found only 1 dic in Stardict-0 format & this is worth it
        self.text = self.text.replace(', ', '\n')
    
    def run(self):
        f = '[MClient] plugins.fora.cleanup.CleanUp.run'
        if not self.text:
            rep.empty(f)
            return ''
        self.delete_trash()
        self.delete_unsupported()
        self.replace_punc()
        self.strip()
        return self.text
