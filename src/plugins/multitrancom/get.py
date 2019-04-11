#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import urllib.request
import shared    as sh
import sharedGUI as sg

import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')


ENCODING = 'utf-8'


class Get:
    
    def __init__ (self,search='',url=''
                 ,timeout=6
                 ):
        f = '[MClient] plugins.multitrancom.get.Get.__init__'
        self.values()
        self._search  = search
        self._url     = url
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
                except:
                    self.Success = False
                    self._html   = ''
                    self._text   = ''
                    sh.objs.mes (f,_('ERROR')
                                ,_('Unable to change the web-page encoding!')
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
                                                        ,self._timeout
                                                        ).read()
                    sh.log.append (f,_('INFO')
                                  ,_('[OK]: "%s"') % self._search
                                  )
                # Too many possible exceptions
                except:
                    sh.log.append (f,_('WARNING')
                                  ,_('[FAILED]: "%s"') % self._search
                                  )
                    # For some reason, 'break' does not work here
                    if not sg.Message (f,_('QUESTION')
                                      ,_('Unable to get the webpage. Check website accessibility.\n\nPress OK to try again.')
                                      ).Yes:
                        return
        else:
            sh.com.cancel(f)
