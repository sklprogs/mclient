#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh
import skl_shared_qt.config as qc

PRODUCT_LOW = 'mclient'


class Paths:
    
    def __init__(self):
        self.set_values()
    
    def set_values(self):
        self.Success = True
        self.dics = ''
    
    def check(self):
        self.ihome = sh.Home(PRODUCT_LOW)
        self.Success = self.ihome.create_conf()
    
    def set_dics(self):
        f = '[MClient] config.Paths.set_dics'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.dics = self.ihome.add_config('dics')
        if not self.dics:
            self.Success = False
            sh.com.rep_empty(f)
            return
        if os.path.exists(self.dics):
            self.Success = sh.Directory(self.dics).Success
        else:
            self.Success = sh.Path(self.dics).create()
        return self.dics
    
    def get_default(self):
        return sh.objs.get_pdir().add('..', 'resources', 'config', 'default.json')
    
    def get_schema(self):
        return sh.objs.get_pdir().add('..', 'resources', 'config', 'schema.json')
    
    def get_local(self):
        return self.ihome.add_config(PRODUCT_LOW + '.json')
    
    def run(self):
        self.check()
        self.set_dics()



class Config(qc.Config):
    
    def __init__(self, default, schema, local):
        super().__init__(default, schema, local)
        self.set_values()
        self.default = default
        self.schema = schema
        self.local = local
    
    def update(self):
        f = '[MClient] config.Config.update'
        if not self.Success:
            sh.com.cancel(f)
            return
        self._copy()
        self.localize()
        if self.ilocal.Success:
            mes = _('Update default configuration')
            self.new = qc.Update(self.idefault.get(), self.ilocal.get()).run()
        else:
            mes = _('Use default configuration')
        sh.objs.get_mes(f, mes, True).show_info()
        self.convert_types()
    
    def quit(self):
        self.revert_types()
        self.save()
    
    def convert_types(self):
        f = '[MClient] config.Config.convert_types'
        if not self.Success:
            sh.com.cancel(f)
            return
        ''' JSON does not support floats. Do not rely on the schema here since
            it checks for a string.
        '''
        self.new['timeout'] = sh.Input(f, self.new['timeout']).get_float()
    
    def revert_types(self):
        f = '[MClient] config.Config.revert_types'
        if not self.Success:
            sh.com.cancel(f)
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
            sh.com.cancel(f)
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



class HistorySubjects:
    # Call externally only after validating the config
    def __init__(self):
        self.count = 0
    
    def get_pair(self, subject):
        f = '[MClient] config.HistorySubjects.get_pair'
        if not objs.get_config().Success:
            sh.com.cancel(f)
            return
        if not subject:
            sh.com.rep_empty(f)
            return
        try:
            return objs.config.new['subjects']['history'][subject]
        except KeyError:
            return
    
    def add(self, body):
        f = '[MClient] config.HistorySubjects.add'
        if not objs.get_config().Success:
            sh.com.cancel(f)
            return
        if not body:
            sh.com.rep_lazy(f)
            return
        self.count = 0
        for key in body:
            self._add_item(key, body[key])
        sh.com.rep_matches(f, self.count)
    
    def _add_item(self, short, full):
        f = '[MClient] config.HistorySubjects._add_item'
        ''' - 'short' must be different from 'full' since we need new expanded
              subjects. If the same value is returned after expanding, this
              means that a short-full subject pair has not been found.
            - JSON accepts empty keys and values.
        '''
        if not short or not full:
            sh.com.rep_empty(f)
            return
        if short == full or short in objs.config.new['subjects']['history']:
            sh.com.rep_lazy(f)
            return
        self.count += 2
        objs.config.new['subjects']['history'][short] = full
        objs.config.new['subjects']['history'][full] = short



class Objects:
    
    def __init__(self):
        self.paths = self.config = None
    
    def get_paths(self):
        if self.paths is None:
            self.paths = Paths()
            self.paths.run()
        return self.paths
    
    def get_config(self):
        if self.config is None:
            default = self.get_paths().get_default()
            schema = self.paths.get_schema()
            local = self.paths.get_local()
            self.config = Config(default, schema, local)
            self.config.run()
        return self.config


objs = Objects()
