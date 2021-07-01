#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _


class Compile:
    
    def __init__(self):
        self.Success = True
        self.file = '/home/pete/bin/mclient/tests/subjects_auto.txt'
        self.text = ''
        self.lst = []
    
    def load(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.compile.Compile.load'
        if self.Success:
            self.text = sh.ReadTextFile(self.file).get()
            if not self.text:
                self.Success = False
                sh.com.rep_out(f)
        else:
            sh.com.cancel(f)
    
    def split(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.compile.Compile.split'
        if self.Success:
            self.lst = self.text.splitlines()
            self.lst = [row.split('\t') for row in self.lst]
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.load()
        self.split()
