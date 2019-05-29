#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import urllib.request
import urllib.parse
import html
import shared    as sh
import sharedGUI as sg

import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')


ENCODING  = 'UTF-8'
# 'https' is got faster than 'http' (~0.2s)
URL       = 'https://www.multitran.com'
TIMEOUT   = 6
PAIR_ROOT = URL + '/m.exe?'


class Suggest:
    
    def __init__(self,search):
        self.values()
        if search:
            self.reset(search)
    
    def values(self):
        self.Success = True
        self._search = ''
        self._url    = ''
        self._pair   = URL + '/ms.exe?s=%s'
    
    def reset(self,search):
        f = '[MClient] plugins.multitrancom.get.Suggest.reset'
        self._search = search
        if not self._search:
            self.Success = False
            sh.com.empty(f)
    
    def url(self):
        f = '[MClient] plugins.multitrancom.get.Suggest.url'
        if self.Success:
            ''' #NOTE: the encoding here MUST be 'utf-8' irrespective
                of the plugin!
            '''
            self._url = sh.Online (base_str   = self._pair
                                  ,search_str = self._search
                                  ,encoding   = 'utf-8'
                                  ).url()
            if not self._url:
                sh.log.append (f,_('WARNING')
                              ,_('Empty output is not allowed!')
                              )
                self.Success = False
        else:
            sh.com.cancel(f)
    
    def get(self):
        f = '[MClient] plugins.multitrancom.get.Suggest.get'
        if self.Success:
            ''' #NOTE: the encoding here (unlike 'self.url')
                is plugin-dependent.
            '''
            self._items = sh.Get (url      = self._url
                                 ,encoding = ENCODING
                                 ).run()
            if self._items:
                self._items = html.unescape(self._items)
                self._items = [item for item \
                               in self._items.splitlines() if item
                              ]
                sh.log.append (f,_('DEBUG')
                              ,'; '.join(self._items)
                              )
                return self._items
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.url()
        return self.get()



class Get:
    
    def __init__(self,search='',url=''):
        f = '[MClient] plugins.multitrancom.get.Get.__init__'
        self.values()
        self._search = search
        self._url    = com.fix_url(url)
        if not self._url or not self._search or not ENCODING:
            self.Success = False
            sh.com.empty(f)
    
    def values(self):
        self.Success = True
        self._html   = ''
        self._text   = ''
    
    def run(self):
        self.get()
        self.decode()
        return self._text
        
    def decode(self):
        f = '[MClient] plugins.multitrancom.get.Get.decode'
        if self.Success:
            ''' If the page is not loaded, we obviously cannot change
                its encoding.
            '''
            if self._text:
                try:
                    self._html = self._text \
                               = self._text.decode(ENCODING)
                except Exception as e:
                    self.Success = False
                    self._html   = ''
                    self._text   = ''
                    sh.objs.mes (f,_('ERROR')
                                ,_('Unable to change the web-page encoding!\n\nDetails: %s')\
                                % str(e)
                                )
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def get(self):
        f = '[MClient] plugins.multitrancom.get.Get.get'
        if self.Success:
            while not self._text:
                try:
                    sh.log.append (f,_('INFO')
                                  ,_('Get online: "%s"') % self._search
                                  )
                    ''' - If the page is loaded using
                          "page=urllib.request.urlopen(my_url)", we get
                          HTTPResponse as a result, which is useful only
                          to remove JavaScript tags. Thus, if we remove
                          all excessive tags manually, then we need
                          a string as output.
                        - If 'self._url' is empty, then an error is
                          thrown.
                    '''
                    self._text = urllib.request.urlopen (self._url
                                                        ,None
                                                        ,TIMEOUT
                                                        ).read()
                    sh.log.append (f,_('INFO')
                                  ,_('[OK]: "%s"') % self._search
                                  )
                # Too many possible exceptions
                except Exception as e:
                    sh.log.append (f,_('WARNING')
                                  ,_('[FAILED]: "%s"') % self._search
                                  )
                    # For some reason, 'break' does not work here
                    if not sg.Message (f,_('QUESTION')
                                      ,_('Unable to get the webpage. Press OK to try again.\n\nDetails: %s')\
                                      % str(e)
                                      ).Yes:
                        return
        else:
            sh.com.cancel(f)



class Commands:
    
    #todo: fix remaining links to localhost
    def fix_raw_html(self,code):
        f = '[MClient] plugins.multitrancom.get.Commands.fix_raw_html'
        if code:
            code = code.replace ('charset={}"'.format(ENCODING)
                                ,'charset=utf-8"'
                                )
            code = code.replace ('<a href="/m.exe?'
                                ,'<a href="' + PAIR_ROOT
                                )
            return code
        else:
            sh.com.empty(f)
    
    def get_url(self,code1,code2,search):
        f = '[MClient] plugins.multitrancom.get.Commands.get_url'
        if search and code1 and code2:
            #note: The encoding here should always be 'utf-8'!
            base_str = 'https://www.multitran.com/m.exe?s=%s&l1={}&l2={}&SHL=2'.format(code1,code2)
            return sh.Online (base_str   = base_str
                             ,search_str = search
                             ,encoding   = 'utf-8'
                             ).url()
        else:
            sh.com.empty(f)
    
    def fix_url(self,url):
        f = '[MClient] plugins.multitrancom.get.Commands.fix_url'
        ''' multitran.com provides for URLs that are not entirely
            correct: they still can contain spaces and unquoted symbols
            (such as 'à' or 'ф'). Browsers deal with this correctly but
            we must perform this additional step of quoting. Some
            symbols like '=', however, should not be quoted.
        '''
        if url:
            ''' We assume that 'multitran.com' does not provide for full
                URLs so that we would not have to run quoting for
                the entire URL which can increase a probability of
                errors.
            '''
            if not url.startswith('http'):
                url = list(url)
                for i in range(len(url)):
                    if not url[i] in (':','/','=','&','?'):
                        url[i] = urllib.parse.quote(url[i])
                url = PAIR_ROOT + ''.join(url)
                ''' #note: this will change the UI language of
                    'multitran.com' so we would not have to add English
                    equivalents of dictionary titles into the 'abbr'
                    file. Still, we should probably add those titles
                    if we want our program to serve international users.
                '''
                if not '&SHL=2' in url:
                    url += '&SHL=2'
            return url
        else:
            sh.com.empty(f)
            return ''

    def accessible(self):
        try:
            code = urllib.request.urlopen (url     = URL
                                          ,timeout = TIMEOUT
                                          ).code
            if (code / 100 < 4):
                return True
        except: #urllib.error.URLError, socket.timeout
            return False


com = Commands()
