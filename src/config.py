#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import json
import jsonschema

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

PRODUCT_LOW = 'mclient'
MIN_VERSION = 2


class Schema:
    
    def __init__(self, file):
        self.Success = True
        self.code = ''
        self.dic = {}
        self.file = file
    
    def check_empty(self):
        f = '[MClient] config.Schema.check_empty'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.file:
            self.Success = False
            sh.com.rep_empty(f)
    
    def load(self):
        f = '[MClient] config.Schema.load'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.code = sh.ReadTextFile(self.file).get()
        if not self.code:
            self.Success = False
            sh.com.rep_empty(f)
    
    def set_dic(self):
        f = '[MClient] config.Validate.set_dic'
        if not self.Success:
            sh.com.cancel(f)
            return
        try:
            self.dic = json.loads(self.code)
        except Exception as e:
            self.Success = False
            mes = _('Schema "{}" is invalid!\n\nDetails: {}')
            mes = mes.format(self.file, e)
            sh.objs.get_mes(f, mes).show_error()
    
    def run(self):
        self.check_empty()
        self.load()
        self.set_dic()
        return self.dic



class Validate:
    
    def __init__(self, file, schema, Verbose=True):
        self.Success = True
        self.Verbose = Verbose
        self.code = ''
        self.dic = {}
        self.file = file
        self.schema = schema
    
    def check_empty(self):
        f = '[MClient] config.Validate.check_empty'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.file or not self.schema:
            self.Success = False
            sh.com.rep_empty(f)
    
    def load(self):
        f = '[MClient] config.Validate.load'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.code = sh.ReadTextFile(self.file).get()
        if not self.code:
            self.Success = False
            sh.com.rep_empty(f)
    
    def set_dic(self):
        f = '[MClient] config.Validate.set_dic'
        if not self.Success:
            sh.com.cancel(f)
            return
        try:
            self.dic = json.loads(self.code)
        except Exception as e:
            self.Success = False
            if self.Verbose:
                mes = _('Configuration file "{}" is invalid!\n\nDetails: {}')
                mes = mes.format(self.file, e)
                sh.objs.get_mes(f, mes).show_error()
    
    def validate(self):
        f = '[MClient] config.Validate.validate'
        if not self.Success:
            sh.com.cancel(f)
            return
        #NOTE: Setting empty schema passes validation
        try:
            jsonschema.validate(self.dic, self.schema)
        except jsonschema.exceptions.ValidationError as e:
            self.Success = False
            if self.Verbose:
                mes = _('Configuration file "{}" is invalid!\n\nDetails: {}')
                mes = mes.format(self.file, e)
                sh.objs.get_mes(f, mes).show_error()
    
    def _get_version(self):
        try:
            return self.dic['config']['min_version']
        except KeyError:
            return
    
    def check_version(self):
        f = '[MClient] config.Validate.check_version'
        if not self.Success:
            sh.com.cancel(f)
            return
        version = self._get_version()
        if version is None or version < MIN_VERSION:
            mes = _('Configuration file "{}" is oudated and will be overwritten!\n\nBack it up now if you need it.')
            mes = mes.format(self.file)
            sh.objs.get_mes(f, mes).show_error()
    
    def run(self):
        self.check_empty()
        self.load()
        self.set_dic()
        self.validate()
        self.check_version()
        return self.dic



class Config:
    
    def __init__(self, plocal, pdefault, pschema):
        self.Success = True
        self.Created = False
        self.schema = {}
        self.local = {}
        self.plocal = plocal
        self.pdefault = pdefault
        self.pschema = pschema
    
    def set_schema(self):
        f = '[MClient] config.Config.set_schema'
        if not self.Success:
            sh.com.cancel(f)
            return
        ischema = Schema(self.pschema)
        self.schema = ischema.run()
        self.Success = ischema.Success
    
    def _create(self):
        self.Created = True
        self.Success = sh.File(self.pdefault, self.plocal).copy()
        return self.Success
    
    def set_local(self):
        f = '[MClient] config.Config.set_local'
        if not self.Success:
            sh.com.cancel(f)
            return
        ivalid = Validate(self.plocal, self.schema, False)
        self.local = ivalid.run()
        if ivalid.Success:
            return
        if not self._create():
            return
        ivalid = Validate(self.plocal, self.schema, True)
        self.local = ivalid.run()
        self.Success = ivalid.Success
    
    def save(self):
        f = '[MClient] config.Config.save'
        if not self.Success:
            sh.com.cancel(f)
            return
        try:
            code = json.dumps(self.local, ensure_ascii=False, indent=4)
        except Exception as e:
            self.Success = False
            sh.com.rep_third_party(f, e)
            return
        self.Success = sh.WriteTextFile(self.plocal, True).write(code)
    
    def convert_types(self):
        f = '[MClient] config.Config.convert_types'
        if not self.Success:
            sh.com.cancel(f)
            return
        # JSON does not support floats
        self.local['timeout'] = float(self.local['timeout'])
    
    def revert_types(self):
        f = '[MClient] config.Config.revert_types'
        if not self.Success:
            sh.com.cancel(f)
            return
        # JSON does not support floats
        self.local['timeout'] = str(self.local['timeout'])
    
    def quit(self):
        self.revert_types()
        self.save()
    
    def localize(self):
        # This is needed when a default config is forced
        f = '[MClient] config.Config.localize'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.Created:
            sh.com.rep_lazy(f)
            return
        self.local['columns']['1']['type'] = _(self.local['columns']['1']['type'])
        self.local['columns']['2']['type'] = _(self.local['columns']['2']['type'])
        self.local['columns']['3']['type'] = _(self.local['columns']['3']['type'])
        self.local['columns']['4']['type'] = _(self.local['columns']['4']['type'])
        self.local['lang1'] = _(self.local['lang1'])
        self.local['lang2'] = _(self.local['lang2'])
        self.local['source'] = _(self.local['source'])
        self.local['speech1'] = _(self.local['speech1'])
        self.local['speech2'] = _(self.local['speech2'])
        self.local['speech3'] = _(self.local['speech3'])
        self.local['speech4'] = _(self.local['speech4'])
        self.local['speech5'] = _(self.local['speech5'])
        self.local['speech6'] = _(self.local['speech6'])
        self.local['speech7'] = _(self.local['speech7'])
        self.local['style'] = _(self.local['style'])
        for action in self.local['actions']:
            self.local['actions'][action]['hint'] = _(self.local['actions'][action]['hint'])
    
    def run(self):
        self.set_schema()
        self.set_local()
        self.localize()
        return self.local



class Subjects:
    
    def __init__(self):
        self.set_values()
        self.ihome = sh.Home(PRODUCT_LOW)
        self.Success = self.ihome.create_conf()
    
    def set_values(self):
        self.Success = True
        self.file = ''
        self.body = {}
    
    def add(self, body):
        f = '[MClient] config.Subjects.add'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not body:
            sh.com.rep_lazy(f)
            return
        count = 0
        for key in body:
            # JSON accepts empty keys and values
            if not key:
                sh.com.rep_empty(f)
                continue
            value = body[key]
            if not value:
                sh.com.rep_empty(f)
                continue
            ''' 'key' must be different from 'value' since we need new expanded
                subjects. If the same value is returned after expanding, this
                means that a short-full subject pair has not been found.
            '''
            if not key in self.body and key != value:
                count += 1
                self.body[key] = value
        sh.com.rep_matches(f, count)
    
    def set_file(self):
        f = '[MClient] config.Subjects.set_file'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.file = self.ihome.add_config('subjects.json')
        if not self.file:
            self.Success = False
            sh.com.rep_empty(f)
            return
    
    def create(self):
        f = '[MClient] config.Subjects.create'
        if not self.Success:
            sh.com.cancel(f)
            return
        if os.path.exists(self.file):
            self.Success = sh.File(self.file).Success
        else:
            iwrite = sh.WriteTextFile(self.file)
            # JSON throws an error upon an empty file
            iwrite.write('{}')
            self.Success = iwrite.Success
    
    def load(self):
        f = '[MClient] config.Subjects.load'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.isubj = sh.Json(self.file)
        self.body = self.isubj.run()
        # '{}' is allowed, so we do not check the body
        self.Success = self.isubj.Success
    
    def save(self):
        f = '[MClient] config.Subjects.save'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.isubj.save(self.body)
        self.Success = self.isibj.Success
        
    def run(self):
        self.set_file()
        self.create()
        self.load()

        

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
    
    def get_default_config(self):
        return sh.objs.get_pdir().add('..', 'resources', 'config', 'default.json')
    
    def get_schema(self):
        return sh.objs.get_pdir().add('..', 'resources', 'config', 'schema.json')
    
    def get_local_config(self):
        return self.ihome.add_config(PRODUCT_LOW + '.json')
    
    def run(self):
        self.check()
        self.set_dics()



class Objects:
    
    def __init__(self):
        self.config = self.paths = self.subjects = None
    
    def get_subjects(self):
        if self.subjects is None:
            self.subjects = Subjects()
            self.subjects.run()
        return self.subjects
    
    def get_paths(self):
        if self.paths is None:
            self.paths = Paths()
            self.paths.run()
        return self.paths
    
    def get_config(self):
        if self.config is None:
            local = self.get_paths().get_local_config()
            default = self.paths.get_default_config()
            schema = self.paths.get_schema()
            local = sh.Path(local).get_absolute()
            default = sh.Path(default).get_absolute()
            schema = sh.Path(schema).get_absolute()
            self.config = Config(local, default, schema)
            self.config.run()
        return self.config


objs = Objects()


if __name__ == '__main__':
    f = '[MClient] config.__main__'
    sh.com.start()
    timer = sh.Timer(f)
    timer.start()
    objs.get_config()
    mes = _('The operation has taken {} s.').format(timer.end())
    code = json.dumps(objs.config.local, ensure_ascii=False, indent=4)
    mes += '\n\n' + code
    idebug = sh.Debug(f, mes)
    idebug.show()
    sh.com.end()
