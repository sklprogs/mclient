#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import urllib.request
import html
import w3lib.url
import skl_shared.shared as sh
from skl_shared.localize import _


CODING = 'UTF-8'
# 'https' is received faster than 'http' (~0.2s)
URL = 'https://www.multitran.com'
TIMEOUT = 6
PAIRROOT = URL + '/m.exe?'


class Suggest:
    
    def __init__(self,search):
        self.set_values()
        if search:
            self.reset(search)
    
    def set_values(self):
        self.Success = True
        self.pattern = ''
        self.url = ''
        self.pair = URL + '/ms.exe?s=%s'
    
    def reset(self,search):
        f = '[MClient] plugins.multitrancom.get.Suggest.reset'
        self.pattern = search
        if not self.pattern:
            self.Success = False
            sh.com.rep_empty(f)
    
    def get_url(self):
        f = '[MClient] plugins.multitrancom.get.Suggest.get_url'
        if self.Success:
            ''' #NOTE: the encoding here MUST be 'utf-8' irrespective
                of the plugin!
            '''
            self.url = sh.Online (base = self.pair
                                 ,pattern = self.pattern
                                 ,coding = 'utf-8'
                                 ).get_url()
            if not self.url:
                sh.com.rep_empty(f)
                self.Success = False
        else:
            sh.com.cancel(f)
    
    def get(self):
        f = '[MClient] plugins.multitrancom.get.Suggest.get'
        if self.Success:
            ''' #NOTE: the encoding here (unlike 'self.url')
                is plugin-dependent.
            '''
            self.items = sh.Get (url = self.url
                                ,coding = CODING
                                ).run()
            if self.items:
                self.items = html.unescape(self.items)
                self.items = [item for item \
                              in self.items.splitlines() if item
                             ]
                sh.objs.get_mes(f,self.items,True).show_debug()
                return self.items
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.get_url()
        return self.get()



class Get:
    
    def __init__(self,search='',url=''):
        f = '[MClient] plugins.multitrancom.get.Get.__init__'
        self.set_values()
        self.pattern = search
        self.url = com.fix_url(url)
        if not self.url or not self.pattern or not CODING:
            self.Success = False
            sh.com.rep_empty(f)
    
    def set_values(self):
        self.Success = True
        self.htm = ''
        self.text = ''
    
    def run(self):
        self.get()
        self.decode()
        return self.text
        
    def decode(self):
        f = '[MClient] plugins.multitrancom.get.Get.decode'
        if self.Success:
            ''' If the page is not loaded, we obviously cannot change
                its encoding.
            '''
            if self.text:
                try:
                    self.htm = self.text = self.text.decode(CODING)
                except Exception as e:
                    self.Success = False
                    self.htm = ''
                    self.text = ''
                    mes = _('Unable to change the web-page encoding!\n\nDetails: {}')
                    mes = mes.format(e)
                    sh.objs.get_mes(f,mes).show_error()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def get(self):
        f = '[MClient] plugins.multitrancom.get.Get.get'
        if self.Success:
            while not self.text:
                try:
                    mes = _('Get online: "{}"').format(self.pattern)
                    sh.objs.get_mes(f,mes,True).show_info()
                    ''' - If the page is loaded using
                          "page=urllib.request.urlopen(my_url)", we get
                          HTTPResponse as a result, which is useful only
                          to remove JavaScript tags. Thus, if we remove
                          all excessive tags manually, then we need
                          a string as output.
                        - If 'self.url' is empty, then an error is
                          thrown.
                    '''
                    self.text = urllib.request.urlopen (self.url
                                                       ,None
                                                       ,TIMEOUT
                                                       ).read()
                    mes = _('[OK]: "{}"').format(self.pattern)
                    sh.objs.get_mes(f,mes,True).show_info()
                # Too many possible exceptions
                except Exception as e:
                    mes = _('[FAILED]: "{}"').format(self.pattern)
                    sh.objs.get_mes(f,mes,True).show_error()
                    # For some reason, 'break' does not work here
                    mes = _('Unable to get the webpage. Do you want to try again?\n\nDetails: {}')
                    mes = mes.format(e)
                    if not sh.objs.get_mes(f,mes).show_question():
                        return
        else:
            sh.com.cancel(f)



class Commands:
    
    #TODO: fix remaining links to localhost
    def fix_raw_htm(self,code):
        code = code.replace ('charset={}"'.format(CODING)
                            ,'charset=utf-8"'
                            )
        code = code.replace('<a href="/m.exe?','<a href="' + PAIRROOT)
        return code
    
    def get_url(self,code1,code2,search):
        f = '[MClient] plugins.multitrancom.get.Commands.get_url'
        if search and code1 and code2:
            #NOTE: The encoding here should always be 'utf-8'!
            base = 'https://www.multitran.com/m.exe?s=%s&l1={}&l2={}&SHL=2'
            base = base.format(code1,code2)
            return sh.Online (base = base
                             ,pattern = search
                             ,coding = 'utf-8'
                             ).get_url()
        else:
            sh.com.rep_empty(f)
    
    def fix_url(self,url):
        f = '[MClient] plugins.multitrancom.get.Commands.fix_url'
        if url:
            try:
                ind = url.index('" title')
                url = url[:ind]
            except ValueError:
                pass
            url = w3lib.url.safe_url_string(url)
            if not url.startswith('http'):
                url = PAIRROOT + url
                ''' #NOTE: this will change the UI language of
                    'multitran.com' so we would not have to add English
                    equivalents of dictionary titles into the 'abbr'
                    file. Still, we should probably add those titles
                    if we want our program to serve international users.
                '''
                if not '&SHL=2' in url:
                    url += '&SHL=2'
            return url
        else:
            sh.com.rep_empty(f)
            return ''

    def is_accessible(self):
        try:
            code = urllib.request.urlopen (url = URL
                                          ,timeout = TIMEOUT
                                          ).code
            if (code / 100 < 4):
                return True
        except: #urllib.error.URLError, socket.timeout
            return False


com = Commands()
