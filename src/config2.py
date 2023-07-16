#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import json
import jsonschema

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

PRODUCT_LOW = 'mclient'


class Config:
    
    def __init__(self):
        self.Success = True
        self.pdefault = ''
        self.plocal = ''
        self.pschema = ''
        self.local = ''
        self.schema = ''
    
    def validate(self):
        f = '[MClient] config.Config.validate'
        if not self.Success:
            sh.com.cancel(f)
            return
        try:
            jsonschema.validate(self.local, self.schema)
        except jsonschema.exceptions.ValidationError as e:
            self.Success = False
            mes = _('Configuration file "{}" has values of a wrong type!\nFix or delete this file.\n\nDetails:\n{}')
            mes = mes.format(self.plocal, e)
            sh.objs.get_mes(f, mes).show_error()
    
    def load_schema(self):
        f = '[MClient] config.Config.load_schema'
        if not self.Success:
            sh.com.cancel(f)
            return
        code = sh.ReadTextFile(self.pschema).get()
        if not code:
            self.Success = False
            sh.com.rep_out(f)
            return
        try:
            self.schema = json.loads(code)
        except Exception as e:
            self.Success = False
            sh.com.rep_third_party(f, e)
    
    def load_local(self):
        f = '[MClient] config.Config.load_local'
        if not self.Success:
            sh.com.cancel(f)
            return
        code = sh.ReadTextFile(self.plocal).get()
        if not code:
            self.Success = False
            sh.com.rep_out(f)
            return
        try:
            self.local = json.loads(code)
        except Exception as e:
            self.Success = False
            sh.com.rep_third_party(f, e)
    
    def set_local(self):
        f = '[MClient] config.Config.set_local'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.plocal = sh.Home(PRODUCT_LOW).add_config(PRODUCT_LOW + '.json')
    
    def create(self):
        f = '[MClient] config.Config.create'
        if not self.Success:
            sh.com.cancel(f)
            return
        if os.path.exists(self.plocal) and os.path.isfile(self.plocal):
            sh.com.rep_lazy(f)
            return
        self.Success = sh.File(self.pdefault, self.plocal).copy()
    
    def set_default(self):
        f = '[MClient] config.Config.set_default'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.pdefault = sh.objs.get_pdir().add('..', 'resources', 'config', 'default.json')
        # Full path is more intuitive in case the file does not exist
        self.pdefault = os.path.abspath(self.pdefault)
        self.Success = sh.File(self.pdefault).Success
    
    def set_schema(self):
        f = '[MClient] config.Config.set_schema'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.pschema = sh.objs.get_pdir().add('..', 'resources', 'config', 'schema.json')
        # Full path is more intuitive in case the file does not exist
        self.pschema = os.path.abspath(self.pschema)
        self.Success = sh.File(self.pschema).Success
    
    def run(self):
        self.set_default()
        self.set_schema()
        self.set_local()
        self.create()
        self.load_local()
        self.load_schema()
        self.validate()


if __name__ == '__main__':
    f = '[MClient] config.__main__'
    sh.com.start()
    timer = sh.Timer(f)
    timer.start()
    iconfig = Config()
    iconfig.run()
    timer.end()
#    sub1 = f'Default config path: {iconfig.pdefault}'
#    sub2 = f'Schema path: {iconfig.pschema}'
#    sub3 = f'Local config path: {iconfig.plocal}'
#    sub4 = f'Schema:\n{iconfig.schema}'
#    sub5 = f'Config:\n{iconfig.local}'
#    mes = [sub1, sub2, sub3, sub4, sub5]
#    mes = '\n\n'.join(mes)
#    idebug = sh.Debug(f, mes)
#    idebug.show()
    mes = f'Success: {iconfig.Success}'
    sh.objs.get_mes(f, mes).show_info()
    mes = _('Goodbye!')
    sh.objs.get_mes(f, mes, True).show_debug()
    sh.com.end()
