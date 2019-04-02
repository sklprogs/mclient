#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import re
''' В Python 3 не работает просто import urllib, импорт должен быть
    именно такой, как здесь
'''
import urllib.request
import html
import ssl
import shared    as sh
import sharedGUI as sg
import offline   as of

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')

sep_words_found = 'найдены отдельные слова'
message_board   = 'спросить в форуме'

p1 = '" href'
p2 = '<trash>'
p3 = '"</trash><a href'
p4 = '<a title="'
p5 = '</a>'
p6 = '<span STYLE="color:gray">'
p7 = '<span STYLE="color:black">'
p8 = '">'


class Page:

    def __init__ (self,source=_('All'),search='~'
                 ,url='',win_encoding='windows-1251'
                 ,ext_dics=None,file=None,timeout=6
                 ):
        f = '[MClient] page.Page.__init__'
        self.values()
        self._source       = source
        self._search       = search
        self._url          = url
        self._win_encoding = win_encoding
        self.ext_dics      = ext_dics
        self._file         = file
        self._timeout      = timeout
        if not self._source or not self._search \
                            or not self._win_encoding:
            self.Success   = False
            sh.com.empty(f)

    def values(self):
        self.Success   = True
        self._html_raw = self._page = ''
        self.HasLocal  = False
    
    def run(self):
        self.get()
        self.invalid()
        # HTML specific
        self.decode_entities()
        self.invalid2()
        # An excessive space must be removed after unescaping the page
        self.mt_specific_replace()
        # HTML specific
        self.common_replace()
        # HTML specific
        self.article_not_found()
        self.unsupported()
        return self._page

    ''' Remove characters from a range not supported by Tcl 
        (and causing a Tkinter error). Sample requests causing 
        the error: Multitran, EN-RU: 'top', 'et al.'
     '''
    def unsupported(self):
        self._page = [char for char in self._page if ord(char) \
                      in range(65536)
                     ]
    
    #todo: Make this MT-only
    def invalid(self):
        ''' Do this before unescaping, otherwise, some tags describing
            wforms will become exactly comments. It seems that 'wform'
            tags are already present. Replacing these tags with
            altertnative 'wform' tags does not work.
        '''
        self._page = self._page.replace('<span STYLE=&#34;color:gray&#34;>','').replace('<span STYLE=&#34;color:black&#34;>','')

    #todo: Make this MT-only
    def invalid2(self):
        ''' We need to close the tag since all following blocks with be
            'SAMECELL == 1' otherwise
        '''
        self._page = self._page.replace ('<span STYLE="color:black">'
                                        ,'</span>'
                                        )
        ''' These tags shall be replaced since they are not related to
            'useful_tags' (useless/undefined tags with their contents
            are further removed), but we need the contents, and we
            cannot determine the type of the block yet.
        '''
        self._page = self._page.replace('<b>','').replace('</b>','')
        ''' Do this before 'common_replace'. Splitting terms is hindered
            without this.
        '''
        self._page = self._page.replace ('>;  <'
                                        ,'><'
                                        )
        self._page = self._page.replace ('Требуется авторизация'
                                        ,''
                                        )
        self._page = self._page.replace ('Вы знаете перевод этого слова? Добавьте его в словарь:'
                                        ,''
                                        )
        self._page = self._page.replace ('Вы знаете перевод этого выражения? Добавьте его в словарь:'
                                        ,''
                                        )
        self._page = self._page.replace('</span>Наблюдаются проблемы со входом из Хрома<span lang="en-us"> (</span>на','</span><span lang="en-us"></span>')
        self._page = self._page.replace ('сайте кое-что устарело, но пока не удаётся поменять'
                                        ,''
                                        )
        self._page = self._page.replace ('</a>, содержащие <strong>'
                                        ,'</a><strong>'
                                        )

    # HTML specific
    def article_not_found(self):
        if self._source in (_('All'),_('Online')):
            ''' If separate words are found instead of a phrase, prepare
                those words only
            '''
            if sep_words_found in self._page:
                self._page = self._page.replace(sep_words_found,'')
                if message_board in self._page:
                    board_pos = self._page.index(message_board)
                else:
                    board_pos = -1
                while p1 in self._page:
                    if self._page.index(p1) < board_pos:
                        self._page = self._page.replace(p1,p3)
                    else:
                        break
                while p4 in self._page:
                    tag_pos = self._page.index(p4)
                    if tag_pos < board_pos:
                        self._page = self._page.replace(p4,p2,1)
                    else:
                        break
                self._page = self._page[:board_pos] + p5 + p6 \
                             + sep_words_found + p7
                self._page = self._page.replace(message_board,'')

    # HTML specific
    def common_replace(self):
        self._page = self._page.replace('\r\n','')
        self._page = self._page.replace('\n','')
        self._page = self._page.replace('\xa0',' ')
        while '  ' in self._page:
            self._page = self._page.replace('  ',' ')
        self._page = re.sub(r'\>[\s]{0,1}\<','><',self._page)

    def mt_specific_replace(self):
        if self._source in (_('All'),_('Online')):
            self._page = self._page.replace('&nbsp;Вы знаете перевод этого выражения? Добавьте его в словарь:','').replace('&nbsp;Вы знаете перевод этого слова? Добавьте его в словарь:','').replace('&nbsp;Требуется авторизация<br>&nbsp;Пожалуйста, войдите на сайт под Вашим именем','').replace('Термины, содержащие ','')
            self._page = re.sub('[:]{0,1}[\s]{0,1}все формы слов[а]{0,1} \(\d+\)','',self._page)

    def decode_entities(self):
        ''' HTML-specific
            Convert HTML entities to a human readable format, e.g.,
            '&copy;' -> '©'
        '''
        f = '[MClient] page.Page.decode_entities'
        #todo: do we need to check this?
        if self._source in (_('All'),_('Online')):
            try:
                self._page = html.unescape(self._page)
            except:
                sh.objs.mes (f,_('ERROR')
                            ,_('Unable to convert HTML entities to UTF-8!')
                            )

    def _get_online(self):
        f = '[MClient] page.Page._get_online'
        Got = False
        while not self._page:
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
                self._page = urllib.request.urlopen (self._url
                                                    ,None
                                                    ,self._timeout
                                                    ).read()
                sh.log.append (f,_('INFO')
                              ,_('[OK]: "%s"') % self._search
                              )
                Got = True
            # Too many possible exceptions
            except:
                sh.log.append (f,_('WARNING')
                              ,_('[FAILED]: "%s"') % self._search
                              )
                # For some reason, 'break' does not work here
                if not sg.Message (f,_('QUESTION')
                                  ,_('Unable to get the webpage. Check website accessibility.\n\nPress OK to try again.')
                                  ).Yes:
                    self._page = 'CANCELED'
        if self._page == 'CANCELED':
            self._page = ''
        ''' If the page is not loaded, it is obvious that we cannot
            change its encoding.
        '''
        if Got:
            try:
                ''' Replace sh.globs['var']['win_encoding'] with
                    the UTF-8 encoding.
                '''
                self._html_raw = self._page \
                               = self._page.decode(self._win_encoding)
            except:
                sh.objs.mes (f,_('ERROR')
                            ,_('Unable to change the web-page encoding!')
                            )

    def _get_offline(self):
        f = '[MClient] page.Page._get_offline'
        if self.ext_dics:
            self._page = self.ext_dics.get(self._search)
            if self._page:
                self.HasLocal = True
        else:
            sh.com.empty(f)

    def disamb_mt(self):
        # This is done to speed up and eliminate tag disambiguation
        try:
            self._page = self._page.replace('<tr>','').replace('</tr>','')
        # Encoding has failed
        except TypeError:
            self._page = ''

    def get(self):
        f = '[MClient] page.Page.get'
        if not self._page:
            if self._file:
                read         = sh.ReadTextFile(file=self._file)
                self._page   = read.get()
                self.Success = read.Success
                self.disamb_mt()
            else:
                page = ''
                ''' #todo: introduce sub-sources, make this code clear;
                    assign '_html_raw' for each sub-source
                '''
                if self._source == _('All'):
                    self._get_online()
                    self.disamb_mt()
                    page = self._page
                    self._get_offline()
                    if self.HasLocal:
                        self._page = of.stardict (text   = self._page
                                                 ,header = self._search
                                                 )
                elif self._source == _('Online'):
                    self._get_online()
                    self.disamb_mt()
                elif self._source == _('Offline'):
                    self._get_offline()
                    if self.HasLocal:
                        self._page = of.stardict (text   = self._page
                                                 ,header = self._search
                                                 )
                else:
                    sh.objs.mes (f,_('ERROR')
                                ,_('An unknown mode "%s"!\n\nThe following modes are supported: "%s".') \
                                % (str(self._source),';'.join(sources))
                                )
                if self._page is None:
                    self._page = ''
                if page and self._page:
                    self._page += page
                elif page:
                    self._page = page
        return self._page



class Welcome:

    def __init__ (self,url=None,st_status=0
                 ,product='MClient',version='current'
                 ,timeout=6
                 ):
        if not url:
            ''' 'https://www.multitran.ru' is got faster than
                'http://www.multitran.ru' (~0.2s)
            '''
            url = 'https://www.multitran.ru'
        self._url       = url
        self._product   = product
        self._version   = version
        self._st_status = st_status #len(ext_dics._dics)
        self._timeout   = timeout
        self._mt_status = 'not running'
        self._mt_color  = 'red'
        self._st_color  = 'red'
        self._desc      = sh.List (lst1 = [self._product
                                          ,self._version
                                          ]
                                  ).space_items()

    def online(self):
        f = '[MClient] page.Welcome.online'
        ''' On *some* systems we can get urllib.error.URLError: 
            <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED].
            To get rid of this error, we use this small workaround.
        '''
        if hasattr(ssl,'_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context
        else:
            sh.log.append (f,_('WARNING')
                          ,_('Unable to use unverified certificates!')
                          )
        try:
            code = urllib.request.urlopen (url     = self._url
                                          ,timeout = self._timeout
                                          ).code
            if (code / 100 < 4):
                return True
        except: #urllib.error.URLError, socket.timeout
            return False

    def generate(self):
        return '''<html>
                <body>
                  <h1>
                    %s
                  </h1>
                  <font face='Serif' size='6'>
                  <br>
                    %s
                  <br>
                    %s
                  <br>
                    %s
                  <br><br>
                    %s
                  <font face='Serif' color='%s' size='6'>%s</font>.
                  <br>
                    %s <font color='%s'>%d</font>.
                  </font>
                </body>
              </html>
        ''' % (_('Welcome to %s!') % self._desc
              ,_('This program retrieves translation from online/offline sources.')
              ,_('Use an entry area below to enter a word/phrase to be translated.')
              ,_('Click the left mouse button on the selection to return its translation. Click the right mouse button on the selection to copy it to clipboard.')
              ,_('Multitran is ')
              ,self._mt_color
              ,self._mt_status
              ,_('Offline dictionaries loaded:')
              ,self._st_color
              ,self._st_status
              )

    def run(self):
        if self.online():
            self._mt_status = _('running')
            self._mt_color  = 'green'
        else:
            self._mt_status = _('not running')
            self._mt_color  = 'red'
        if self._st_status == 0:
            self._st_color = 'red'
        else:
            self._st_color = 'green'
        return self.generate()



if __name__ == '__main__':
    f = '[MClient] page.__main__'
    import logic as lg
    sg.objs.start()
    timer = sh.Timer(func_title=f)
    timer.start()
    page = Page (source = _('Online')
                ,search = 'preceding'
                ,file   = '/tmp/dics/painting.txt'
                )
    '''
    page = Page (source = _('Online')
                ,search = 'иммуногенная'
                ,url    = 'https://www.multitran.ru/c/M.exe?l1=1&l2=2&s=%E8%EC%F3%ED%ED%EE%E3%E5%ED%ED%E0%FF'
                )
    '''
    page.run()
    timer.end()
    '''sh.WriteTextFile (file    = '/home/pete/tmp/ars/do.txt'
                        ,Rewrite = True
                        ).write(text=text)
    '''
    if page._page:
        page._page = ''.join(page._page)
        sg.objs.txt().insert(text=page._page)
        sg.objs._txt.show()
    sg.objs.end()
