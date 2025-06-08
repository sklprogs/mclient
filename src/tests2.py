#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.message.controller as ms
from skl_shared.message.controller import Message, rep


class Config:
    
    def __init__(self):
        ms.GRAPHICAL = False
        from config import CONFIG, PATHS
        self.iconfig = CONFIG
        self.paths = PATHS
    
    def get_paths(self):
        f = '[MClient] tests.Config.get_paths'
        default = self.paths.get_default()
        local = self.paths.get_local()
        schema = self.paths.get_schema()
        mes = _('Default configuration file: {}').format(default)
        Message(f, mes).show_debug()
        mes = _('Local configuration file: {}').format(local)
        Message(f, mes).show_debug()
        mes = _('JSON schema: {}').format(schema)
        Message(f, mes).show_debug()
    
    def run_all(self):
        self.get_paths()
    
    def run(self):
        self.run_all()



class Articles:
    
    def __init__(self):
        ms.GRAPHICAL = False
        from articles import ARTICLES
        self.iarticles = ARTICLES
    
    def get_max_id(self):
        f = '[MClient] tests.Config.get_max_id'
        mes = _('Maximum ID: {}').format(self.iarticles.get_max_id())
        Message(f, mes).show_debug()
    
    def run_all(self):
        self.get_max_id()
    
    def run(self):
        self.run_all()


if __name__ == '__main__':
    #Config().run()
    Articles().run()
