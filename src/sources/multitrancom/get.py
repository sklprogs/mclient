#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import locale
import urllib.request
import html
import w3lib.url

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.online import Online
from skl_shared.get_url import Get as shGet

from config import CONFIG


CODING = 'UTF-8'
# 'https' is received faster than 'http' (~0.2s)
URL = 'https://www.multitran.com'
PAIRROOT = URL + '/m.exe?'


class Extension:
    
    def __init__(self):
        self.ext = '&SHL=1'
    
    def set_ext(self):
        f = '[MClient] sources.multitrancom.get.Extension.set_ext'
        result = locale.getdefaultlocale()
        # en: 1; ru: 2; de: 3; fr: 4; es: 5; he: 6; pl: 14; zh: 17; uk: 33
        if result and result[0]:
            result = result[0]
            if 'ru' in result:
                self.ext = '&SHL=2'
            elif 'de' in result:
                self.ext = '&SHL=3'
            elif 'fr' in result:
                self.ext = '&SHL=4'
            elif 'es' in result:
                self.ext = '&SHL=5'
            elif 'he' in result:
                self.ext = '&SHL=6'
            elif 'pl' in result:
                self.ext = '&SHL=14'
            elif 'zh' in result:
                self.ext = '&SHL=17'
            elif 'uk' in result:
                self.ext = '&SHL=33'
        mes = f'{result} -> {self.ext}'
        Message(f, mes).show_debug()
    
    def run(self):
        self.set_ext()
        return self.ext



class Suggest:
    
    def __init__(self, search):
        self.set_values()
        if search:
            self.reset(search)
    
    def set_values(self):
        self.Success = True
        self.pattern = ''
        self.url = ''
        self.pair = URL + '/ms.exe?s=%s'
    
    def reset(self, search):
        f = '[MClient] sources.multitrancom.get.Suggest.reset'
        self.pattern = search
        if not self.pattern:
            self.Success = False
            rep.empty(f)
    
    def get_url(self):
        f = '[MClient] sources.multitrancom.get.Suggest.get_url'
        if not self.Success:
            rep.cancel(f)
            return
        #NOTE: The encoding here MUST be 'utf-8' irrespective of the source!
        self.url = Online(base = self.pair, pattern = self.pattern
                         ,coding = 'utf-8').get_url()
        if not self.url:
            rep.empty(f)
            self.Success = False
            return
        if not '&SHL=' in self.url:
            self.url += EXT
    
    def get(self):
        f = '[MClient] sources.multitrancom.get.Suggest.get'
        if not self.Success:
            rep.cancel(f)
            return
        #NOTE: the encoding here (unlike 'self.url') is source-dependent
        self.items = shGet(url=self.url, coding=CODING).run()
        if not self.items:
            rep.empty(f)
            return
        self.items = html.unescape(self.items)
        self.items = [item for item in self.items.splitlines() if item]
        Message(f, self.items).show_debug()
        return self.items
    
    def run(self):
        self.get_url()
        return self.get()



class Get:
    
    def __init__(self, search='', url=''):
        f = '[MClient] sources.multitrancom.get.Get.__init__'
        self.Success = True
        self.code = ''
        self.pattern = search
        self.url = com.fix_url(url)
        if not self.url or not self.pattern or not CODING:
            self.Success = False
            rep.empty(f)
    
    def run(self):
        self.get()
        self.decode()
        return self.code
        
    def decode(self):
        f = '[MClient] sources.multitrancom.get.Get.decode'
        if not self.Success:
            rep.cancel(f)
            return
        # If the page is not loaded, we obviously cannot change its encoding
        if not self.code:
            rep.empty(f)
            return
        try:
            self.code = self.code.decode(CODING)
        except Exception as e:
            self.Success = False
            self.code = ''
            mes = _('Unable to change the web-page encoding!\n\nDetails: {}')
            mes = mes.format(e)
            Message(f, mes, True).show_error()
    
    def get(self):
        f = '[MClient] sources.multitrancom.get.Get.get'
        if not self.Success:
            rep.cancel(f)
            return
        while not self.code:
            try:
                mes = _('Get online: "{}"').format(self.pattern)
                Message(f, mes).show_info()
                ''' - If the page is loaded using
                      "page=urllib.request.urlopen(my_url)", we get
                      HTTPResponse as a result, which is useful only to remove
                      JavaScript tags. Thus, if we remove all excessive tags
                      manually, then we need a string as output.
                    - If 'self.url' is empty, then an error is thrown.
                '''
                self.code = urllib.request.urlopen(self.url, None, CONFIG.new['timeout']).read()
                mes = _('[OK]: "{}"').format(self.pattern)
                Message(f, mes).show_info()
            # Too many possible exceptions
            except Exception as e:
                mes = _('[FAILED]: "{}"').format(self.pattern)
                Message(f, mes).show_error()
                # For some reason, 'break' does not work here
                mes = _('Unable to get the webpage. Do you want to try again?\n\nDetails: {}')
                mes = mes.format(e)
                if not Message(f, mes, True).show_question():
                    return



class Commands:
    
    def get_url(self, code1, code2, search):
        f = '[MClient] sources.multitrancom.get.Commands.get_url'
        if not search or not code1 or not code2:
            rep.empty(f)
            return
        #NOTE: The encoding here should always be 'utf-8'!
        base = 'https://www.multitran.com/m.exe?s=%s&l1={}&l2={}'
        base = base.format(code1, code2)
        url = Online(base=base, pattern=search, coding='utf-8').get_url()
        if url and not '&SHL=' in url:
            url += EXT
        return url
    
    def fix_url(self, url):
        f = '[MClient] sources.multitrancom.get.Commands.fix_url'
        if not url:
            rep.empty(f)
            return ''
        try:
            ind = url.index('" title')
            url = url[:ind]
        except ValueError:
            pass
        url = w3lib.url.safe_url_string(url)
        if not url.startswith('http'):
            url = PAIRROOT + url
        if not '&SHL=' in url:
            url += EXT
        return url

    def count_valid(self):
        try:
            code = urllib.request.urlopen(url=URL, timeout=CONFIG.new['timeout']).code
            if (code / 100 < 4):
                return 1
        except: #urllib.error.URLError, socket.timeout
            return 0
        return 0
    
    def count_invalid(self):
        #TODO: Rework manager logic, will cause a delay
        if self.count_valid():
            return 0
        else:
            return 1


com = Commands()
EXT = Extension().run()
