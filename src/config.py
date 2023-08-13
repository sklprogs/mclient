#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh
import skl_shared_qt.config as qc

PRODUCT_LOW = 'mclient'


class Config(qc.Config):
    
    def __init__(self, default, schema, local):
        super().__init__(default, schema, local)
        self.set_values()
        self.default = default
        self.schema = schema
        self.local = local
    
    def update(self):
        f = '[SharedQt] config.Config.update'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.ilocal.Success:
            mes = _('Update default configuration')
            self.new = self.idefault.get() | self.ilocal.get()
        else:
            mes = _('Use default configuration')
            self._copy()
            self.localize()
        self.convert_types()
        sh.objs.get_mes(f, mes, True).show_info()
    
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
    
    def localize(self):
        # This is needed when a default config is forced
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
        for action in self.new['actions']:
            self.new['actions'][action]['hint'] = _(self.new['actions'][action]['hint'])
    
    def run(self):
        self.load()
        self.update()
