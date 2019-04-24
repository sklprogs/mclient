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
PAIR_ROOT = URL + '/m.exe?'
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
''' English  : 1
    Russian  : 2
    German   : 3
    French   : 4
    Spanish  : 5
    Italian  : 23
    Dutch    : 24
    Estonian : 26
    Latvian  : 27
    Afrikaans: 31
    Esperanto: 34
    Kalmyk   : 35
'''
PAIR_URLS = (PAIR_ROOT + 's=%s&l1=2&l2=1&SHL=2'  # ENG <=> RUS
            ,PAIR_ROOT + 's=%s&l1=3&l2=2&SHL=2'  # DEU <=> RUS
            ,PAIR_ROOT + 's=%s&l1=5&l2=2&SHL=2'  # SPA <=> RUS
            ,PAIR_ROOT + 's=%s&l1=4&l2=2&SHL=2'  # FRA <=> RUS
            ,PAIR_ROOT + 's=%s&l1=24&l2=2&SHL=2' # NLD <=> RUS
            ,PAIR_ROOT + 's=%s&l1=23&l2=2&SHL=2' # ITA <=> RUS
            ,PAIR_ROOT + 's=%s&l1=27&l2=2&SHL=2' # LAV <=> RUS
            ,PAIR_ROOT + 's=%s&l1=26&l2=2&SHL=2' # EST <=> RUS
            ,PAIR_ROOT + 's=%s&l1=31&l2=2&SHL=2' # AFR <=> RUS
            ,PAIR_ROOT + 's=%s&l1=34&l2=2&SHL=2' # EPO <=> RUS
            ,PAIR_ROOT + 's=%s&l1=2&l2=35&SHL=2' # RUS <=> XAL
            ,PAIR_ROOT + 's=%s&l1=35&l2=2&SHL=2' # XAL <=> RUS
            ,PAIR_ROOT + 's=%s&l1=1&l2=3&SHL=2'  # ENG <=> DEU
            ,PAIR_ROOT + 's=%s&l1=1&l2=26&SHL=2' # ENG <=> EST
            )


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
    
    def __init__ (self,search='',url=''
                 ,timeout=6
                 ):
        f = '[MClient] plugins.multitrancom.get.Get.__init__'
        self.values()
        self._search  = search
        self._url     = fix_url(url)
        self._timeout = timeout
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
                                                        ,self._timeout
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


def fix_url(url):
    f = '[MClient] plugins.multitrancom.fix_url'
    ''' multitran.com provides for URLs that are not entirely correct:
        they still can contain spaces and unquoted symbols (such as 'à'
        or 'ф'). Browsers deal with this correctly but we must perform
        this additional step of quoting. Some symbols like '=', however,
        should not be quoted.
    '''
    if url:
        ''' We assume that 'multitran.com' does not provide for full
            URLs so that we would not have to run quoting for the entire
            URL which can increase a probability of errors.
        '''
        if not url.startswith('http'):
            url = list(url)
            for i in range(len(url)):
                if not url[i] in (':','/','=','&','?'):
                    url[i] = urllib.parse.quote(url[i])
            url = PAIR_ROOT + ''.join(url)
            ''' #note: this will change the UI language of
                'multitran.com' so we would not have to add English
                equivalents of dictionary titles into the 'abbr' file.
                Still, we should probably add those titles if we want
                our program to serve international users.
            '''
            if not '&SHL=2' in url:
                url += '&SHL=2'
        return url
    else:
        sh.com.empty(f)
        return ''
