#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.config import Config as shConfig, Update as shUpdate
from skl_shared.logic import Input
from skl_shared.paths import Home, Path, Directory, PDIR

PRODUCT_LOW = 'mclient'


class Paths:
    
    def __init__(self):
        self.set_values()
    
    def set_values(self):
        self.Success = True
        self.dics = ''
    
    def check(self):
        self.ihome = Home(PRODUCT_LOW)
        self.Success = self.ihome.create_conf()
    
    def set_dics(self):
        f = '[MClient] config.Paths.set_dics'
        if not self.Success:
            rep.cancel(f)
            return
        self.dics = self.ihome.add_config('dics')
        if not self.dics:
            self.Success = False
            rep.empty(f)
            return
        if os.path.exists(self.dics):
            self.Success = Directory(self.dics).Success
        else:
            self.Success = Path(self.dics).create()
        return self.dics
    
    def get_default(self):
        return PDIR.add('..', 'resources', 'config', 'default.json')
    
    def get_schema(self):
        return PDIR.add('..', 'resources', 'config', 'schema.json')
    
    def get_local(self):
        return self.ihome.add_config(PRODUCT_LOW + '.json')
    
    def run(self):
        self.check()
        self.set_dics()



class Config(shConfig):
    
    def __init__(self, default, schema, local):
        super().__init__(default, schema, local)
        self.set_values()
        self.default = default
        self.schema = schema
        self.local = local
    
    def update(self):
        f = '[MClient] config.Config.update'
        if not self.Success:
            rep.cancel(f)
            return
        self._copy()
        self.localize()
        if self.ilocal.Success:
            mes = _('Update default configuration')
            self.new = shUpdate(self.idefault.get(), self.ilocal.get()).run()
        else:
            mes = _('Use default configuration')
        Message(f, mes).show_info()
        self.convert_types()
    
    def quit(self):
        self.revert_types()
        self.save()
    
    def convert_types(self):
        f = '[MClient] config.Config.convert_types'
        if not self.Success:
            rep.cancel(f)
            return
        ''' JSON does not support floats. Do not rely on the schema here since
            it checks for a string.
        '''
        self.new['timeout'] = Input(f, self.new['timeout']).get_float()
    
    def revert_types(self):
        f = '[MClient] config.Config.revert_types'
        if not self.Success:
            rep.cancel(f)
            return
        # JSON does not support floats
        self.new['timeout'] = str(self.new['timeout'])
    
    def _localize_subjects(self, section):
        for key in list(self.new['subjects'][section].keys()):
            if key == _(key):
                continue
            self.new['subjects'][section][_(key)] = self.new['subjects'][section][key]
            del self.new['subjects'][section][key]
    
    def localize(self):
        ''' Do this each time the default config is loaded since the local
            config can theoretically have absent sections that are present in
            the default config but are not localized (e.g. source names) which
            will cause warnings.
        '''
        f = '[MClient] config.Config.localize'
        if not self.Success:
            rep.cancel(f)
            return
        self.new['columns']['1']['type'] = _(self.new['columns']['1']['type'])
        self.new['columns']['2']['type'] = _(self.new['columns']['2']['type'])
        self.new['columns']['3']['type'] = _(self.new['columns']['3']['type'])
        self.new['columns']['4']['type'] = _(self.new['columns']['4']['type'])
        self.new['lang1'] = _(self.new['lang1'])
        self.new['lang2'] = _(self.new['lang2'])
        self.new['source'] = _(self.new['source'])
        self.new['speech1'] = _(self.new['speech1'])
        self.new['speech2'] = _(self.new['speech2'])
        self.new['speech3'] = _(self.new['speech3'])
        self.new['speech4'] = _(self.new['speech4'])
        self.new['speech5'] = _(self.new['speech5'])
        self.new['speech6'] = _(self.new['speech6'])
        self.new['speech7'] = _(self.new['speech7'])
        self.new['style'] = _(self.new['style'])
        
        self._localize_subjects('blocked')
        self._localize_subjects('prioritized')
        
        for action in self.new['actions']:
            self.new['actions'][action]['hint'] = _(self.new['actions'][action]['hint'])
    
    def run(self):
        self.load()
        self.update()
        self.set_local_dump()



class HistorySubjects:
    # Call externally only after validating the config
    def __init__(self):
        self.count = 0
    
    def get_pair(self, subject):
        f = '[MClient] config.HistorySubjects.get_pair'
        if not CONFIG.Success:
            rep.cancel(f)
            return
        if not subject:
            rep.empty(f)
            return
        try:
            return CONFIG.new['subjects']['history'][subject]
        except KeyError:
            return
    
    def add(self, body):
        f = '[MClient] config.HistorySubjects.add'
        if not CONFIG.Success:
            rep.cancel(f)
            return
        if not body:
            rep.lazy(f)
            return
        self.count = 0
        for key in body:
            self._add_item(key, body[key])
        rep.matches(f, self.count)
    
    def _add_item(self, short, full):
        f = '[MClient] config.HistorySubjects._add_item'
        ''' - 'short' must be different from 'full' since we need new expanded
              subjects. If the same value is returned after expanding, this
              means that a short-full subject pair has not been found.
            - JSON accepts empty keys and values.
        '''
        if not short or not full:
            rep.empty(f)
            return
        if short == full or short in CONFIG.new['subjects']['history']:
            # Messages will be too frequent there
            return
        self.count += 1
        CONFIG.new['subjects']['history'][short] = full


PATHS = Paths()
PATHS.run()
CONFIG = Config(PATHS.get_default(), PATHS.get_schema(), PATHS.get_local())
CONFIG.run()
