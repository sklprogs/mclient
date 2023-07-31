#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import copy
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
        self.default = {}
        self.local = {}
        self.schema = {}
        self.new = {}
    
    def check_local(self):
        f = '[MClient] config.Config.check_local'
        if not self.Success:
            sh.com.cancel(f)
            return
        try:
            jsonschema.validate(self.local, self.schema)
        except jsonschema.exceptions.ValidationError as e:
            self.Success = False
            mes = _('Configuration file "{}" has values of a wrong type!\nFix, restore or delete this file.\n\nDetails:\n{}')
            mes = mes.format(self.plocal, e)
            sh.objs.get_mes(f, mes).show_error()
    
    def check_default(self):
        f = '[MClient] config.Config.check_default'
        if not self.Success:
            sh.com.cancel(f)
            return
        try:
            jsonschema.validate(self.default, self.schema)
        except jsonschema.exceptions.ValidationError as e:
            self.Success = False
            mes = _('Configuration file "{}" has values of a wrong type!\nFix or restore this file.\n\nDetails:\n{}')
            mes = mes.format(self.pdefault, e)
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
    
    def load_default(self):
        f = '[MClient] config.Config.load_default'
        if not self.Success:
            sh.com.cancel(f)
            return
        code = sh.ReadTextFile(self.pdefault).get()
        if not code:
            self.Success = False
            sh.com.rep_out(f)
            return
        try:
            self.default = json.loads(code)
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
        self.new = copy.deepcopy(self.default)
        self.localize_new()
        self.save()
    
    def convert_types(self):
        f = '[MClient] config.Config.convert_types'
        if not self.Success:
            sh.com.cancel(f)
            return
        # JSON does not support floats
        self.new['timeout'] = float(self.new['timeout'])
    
    def revert_types(self):
        f = '[MClient] config.Config.revert_types'
        if not self.Success:
            sh.com.cancel(f)
            return
        # JSON does not support floats
        self.new['timeout'] = str(self.new['timeout'])
    
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
    
    def update(self):
        f = '[MClient] config.Config.update'
        if not self.Success:
            sh.com.cancel(f)
            return
        ''' Python 3.9 or newer is required. Combine dictionaries #1 and #2
            to #3 such that #3 has the values of #1, absent in #2, and existing
            values of #1 are updated with the values of #2. #1 and #2 are
            unchanged. If 'local' is empty this works like
            'self.new = copy.deepcopy(self.default)'.
        '''
        self.new = self.default | self.local
    
    def quit(self):
        self.revert_types()
        self.save()
    
    def save(self):
        f = '[MClient] config.Config.save'
        if not self.Success:
            sh.com.cancel(f)
            return
        try:
            code = json.dumps(self.new, ensure_ascii=False, indent=4)
        except Exception as e:
            self.Success = False
            sh.com.rep_third_party(f, e)
            return
        self.Success = sh.WriteTextFile(self.plocal, True).write(code)
    
    def localize_local(self):
        # This is needed when a default config is forced
        f = '[MClient] config.Config.localize_local'
        if not self.Success:
            sh.com.cancel(f)
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
    
    def localize_new(self):
        f = '[MClient] config.Config.localize_new'
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
    
    def _get_version(self):
        try:
            return self.local['config']['min_version']
        except KeyError:
            return
    
    def check_version(self):
        f = '[MClient] config.Config.check_version'
        if not self.Success:
            sh.com.cancel(f)
            return
        version = self._get_version()
        if version is None or version < self.default['config']['min_version']:
            mes = _('Configuration file "{}" is oudated and will be overwritten! Save it if you need it.')
            mes = mes.format(self.plocal)
            sh.objs.get_mes(f, mes).show_info()
            self.local = copy.deepcopy(self.default)
            self.localize_local()
    
    def run(self):
        self.set_schema()
        self.load_schema()
        self.set_default()
        self.load_default()
        self.check_default()
        self.set_local()
        self.create()
        self.load_local()
        self.check_local()
        self.check_version()
        self.update()
        self.convert_types()



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
        code = sh.ReadTextFile(self.file, True).get()
        try:
            self.body = json.loads(code)
        except Exception as e:
            self.Success = False
            sh.com.rep_third_party(f, e)
    
    def save(self):
        f = '[MClient] config.Subjects.save'
        if not self.Success:
            sh.com.cancel(f)
            return
        mes = _('Write file "{}"').format(self.file)
        sh.objs.get_mes(f, mes, True).show_info()
        try:
            with open(self.file, 'w', encoding='utf-8') as iopen:
                json.dump(self.body, iopen, ensure_ascii=False, indent=4)
        except Exception as e:
            ''' Failing a class which produced a writing error should not fail
                all writing operations some of which may actually be successful.
            '''
            mes = _('Third-party module has failed!\n\nDetails: {}').format(e)
            sh.objs.get_mes(f, mes).show_error()
    
    def run(self):
        self.set_file()
        self.create()
        self.load()

        

class Default:
    
    def __init__(self):
        self.set_values()
    
    def set_values(self):
        self.Success = True
        self.dics = ''
    
    def check(self):
        self.ihome = sh.Home(PRODUCT_LOW)
        self.Success = self.ihome.create_conf()
    
    def set_dics(self):
        f = '[MClient] config.Default.set_dics'
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
    
    def run(self):
        self.check()
        self.set_dics()



class Objects:
    
    def __init__(self):
        self.config = self.default = self.subjects = None
    
    def get_subjects(self):
        if self.subjects is None:
            self.subjects = Subjects()
            self.subjects.run()
        return self.subjects
    
    def get_default(self):
        if self.default is None:
            self.default = Default()
            self.default.run()
        return self.default
    
    def get_config(self):
        if self.config is None:
            self.config = Config()
            self.config.run()
        return self.config


objs = Objects()


if __name__ == '__main__':
    f = '[MClient] config.__main__'
    sh.com.start()
    timer = sh.Timer(f)
    timer.start()
    #objs.get_config().new["PrioritizeSubjects"] = False
    objs.get_config().save()
    timer.end()
    mes = f'Success: {objs.config.Success}'
    sh.objs.get_mes(f, mes).show_info()
    mes = _('Goodbye!')
    sh.objs.get_mes(f, mes, True).show_debug()
    sh.com.end()
