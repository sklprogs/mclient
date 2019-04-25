#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import urllib.request
import html
import shared    as sh
import sharedGUI as sg

import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')


ENCODING  = 'windows-1251'
# 'https' is got faster than 'http' (~0.2s)
URL       = 'https://www.multitran.ru'
TIMEOUT   = 6
PAIR_ROOT = URL + '/c/M.exe?'
PAIRS = ('ENG <=> RUS','DEU <=> RUS','SPA <=> RUS'
        ,'FRA <=> RUS','NLD <=> RUS','ITA <=> RUS'
        ,'LAV <=> RUS','EST <=> RUS','AFR <=> RUS'
        ,'EPO <=> RUS','RUS <=> XAL','XAL <=> RUS'
        ,'ENG <=> DEU','ENG <=> EST'
        )
LANGS = ('English'   # ENG <=> RUS
        ,'German'    # DEU <=> RUS
        ,'Spanish'   # SPA <=> RUS
        ,'French'    # FRA <=> RUS
        ,'Dutch'     # NLD <=> RUS
        ,'Italian'   # ITA <=> RUS
        ,'Latvian'   # LAV <=> RUS
        ,'Estonian'  # EST <=> RUS
        ,'Afrikaans' # AFR <=> RUS
        ,'Esperanto' # EPO <=> RUS
        ,'Kazakh'    # RUS <=> XAL
        ,'Kazakh'    # XAL <=> RUS
        ,'German'    # ENG <=> DEU
        ,'Estonian'  # ENG <=> EST
        )
PAIR_URLS = (PAIR_ROOT + 'l1=1&l2=2&s=%s'  # ENG <=> RUS
            ,PAIR_ROOT + 'l1=3&l2=2&s=%s'  # DEU <=> RUS
            ,PAIR_ROOT + 'l1=5&l2=2&s=%s'  # SPA <=> RUS
            ,PAIR_ROOT + 'l1=4&l2=2&s=%s'  # FRA <=> RUS
            ,PAIR_ROOT + 'l1=24&l2=2&s=%s' # NLD <=> RUS
            ,PAIR_ROOT + 'l1=23&l2=2&s=%s' # ITA <=> RUS
            ,PAIR_ROOT + 'l1=27&l2=2&s=%s' # LAV <=> RUS
            ,PAIR_ROOT + 'l1=26&l2=2&s=%s' # EST <=> RUS
            ,PAIR_ROOT + 'l1=31&l2=2&s=%s' # AFR <=> RUS
            ,PAIR_ROOT + 'l1=34&l2=2&s=%s' # EPO <=> RUS
            ,PAIR_ROOT + 'l1=2&l2=35&s=%s' # RUS <=> XAL
            ,PAIR_ROOT + 'l1=35&l2=2&s=%s' # XAL <=> RUS
            ,PAIR_ROOT + 'l1=1&l2=3&s=%s'  # ENG <=> DEU
            ,PAIR_ROOT + 'l1=1&l2=26&s=%s' # ENG <=> EST
            )
PAIR = PAIR_URLS[0]


class Suggest:
    
    def __init__(self,search,pair):
        self.values()
        if search:
            self.reset (search = search
                       ,pair   = pair
                       )
    
    def values(self):
        self.Success = True
        self._search = ''
        self._url    = ''
        self._pair   = ''
    
    def reset(self,search,pair):
        f = '[MClient] plugins.multitranru.get.Suggest.reset'
        self._search = search
        self._pair   = pair
        if not self._search or not self._pair:
            self.Success = False
            sh.com.empty(f)
    
    def pair(self):
        f = '[MClient] plugins.multitranru.get.Suggest.pair'
        if self.Success:
            self._pair = self._pair.replace('M.exe?','ms.exe?')
            self._pair = self._pair.replace('m.exe?','ms.exe?')
        else:
            sh.com.cancel(f)
    
    def url(self):
        f = '[MClient] plugins.multitranru.get.Suggest.url'
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
        f = '[MClient] plugins.multitranru.get.Suggest.get'
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
        self.pair()
        self.url()
        return self.get()



class Get:
    
    def __init__(self,search='',url=''):
        f = '[MClient] plugins.multitranru.get.Get.__init__'
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
        f = '[MClient] plugins.multitranru.get.Get.decode'
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
        f = '[MClient] plugins.multitranru.get.Get.get'
        if self.Success:
            while not self._text:
                try:
                    sh.log.append (f,_('INFO')
                                  ,_('Get online: "%s"') % self._search
                                  )
                    ''' If the page is loaded using
                        "page=urllib.request.urlopen(my_url)", we get
                        HTTPResponse as a result, which is useful only
                        to remove JavaScript tags. Thus, if we remove all
                        excessive tags manually, then we need a string
                        as output.
                        If 'self._url' is empty, then an error is thrown.
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

    def fix_url(self,url):
        f = '[MClient] plugins.multitranru.get.Commands.fix_url'
        if url:
            if not url.startswith('http'):
                url = PAIR_ROOT + url
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
