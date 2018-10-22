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
import pystardict as pd
import shared     as sh
import sharedGUI  as sg
import offline    as of

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


class ExtDic:

    def __init__ (self,path,lang='English'
                 ,name='External',Block=False
                 ):
        # Full path without extension (as managed by pystardict)
        self._path = path
        self._lang = lang
        self._name = name
        self.Block = Block
        self._dic  = None
        self.load()

    def load(self):
        f = 'page.ExtDic.load'
        sh.log.append (f,_('INFO')
                      ,_('Load "%s"') % self._path
                      )
        try:
            self._dic = pd.Dictionary(self._path)
        except:
            sh.objs.mes (f,_('WARNING')
                        ,_('Failed to load "%s"!') % self._path
                        )

    def get(self,search):
        f = 'page.ExtDic.get'
        result = ''
        if self._dic:
            try:
                result = self._dic.get(k=search)
            except:
                sh.objs.mes (f,_('WARNING')
                            ,_('Failed to parse "%s"!') % self._path
                            )
        else:
            sh.com.empty(f)
        return result



class ExtDics:

    def __init__(self,path):
        self._dics    = []
        self._dics_en = []
        self._dics_de = []
        self._dics_es = []
        self._dics_it = []
        self._dics_fr = []
        self._path    = path
        self.dir      = sh.Directory(path=self._path)
        self._files   = self.dir.files()
        self.Success  = self.dir.Success
        self._list()
        self.load()

    def get(self,lang='English',search=''):
        f = 'page.ExtDics.get'
        if self.Success:
            dics = [dic for dic in self._dics if dic._lang == lang \
                    and not dic.Block
                   ]
            lst  = []
            for dic in dics:
                tmp = dic.get(search=search)
                if tmp:
                    # Set offline dictionary title
                    lst.append(p4 + dic._name + p8 + tmp)
            return '\n'.join(lst)
        else:
            sh.com.cancel(f)

    def load(self):
        f = 'page.ExtDics.load'
        if self.Success:
            sg.objs.waitbox().reset (func_title = f
                                    ,message    = _('Load offline dictionaries')
                                    )
            sg.objs._waitbox.show()
            for elem in self._en:
                path = os.path.join(self._path,elem)
                self._dics.append (ExtDic (path = path
                                          ,lang = 'English'
                                          ,name = elem
                                          )
                                  )
            for elem in self._de:
                path = os.path.join(self._path,elem)
                self._dics.append (ExtDic (path = path
                                          ,lang = 'German'
                                          ,name = elem
                                          )
                                  )
            for elem in self._es:
                path = os.path.join(self._path,elem)
                self._dics.append (ExtDic (path = path
                                          ,lang = 'Spanish'
                                          ,name = elem
                                          )
                                  )
            for elem in self._it:
                path = os.path.join(self._path,elem)
                self._dics.append (ExtDic (path = path
                                          ,lang = 'Italian'
                                          ,name = elem
                                          )
                                  )
            for elem in self._fr:
                path = os.path.join(self._path,elem)
                self._dics.append (ExtDic (path = path
                                          ,lang = 'French'
                                          ,name = elem
                                          )
                                  )
            sg.objs._waitbox.close()
            ''' Leave only those dictionaries that were successfully
                loaded
            '''
            self._dics = [x for x in self._dics if x._dic]
            sh.log.append (f,_('INFO')
                          ,_('%d offline dictionaries have been loaded')\
                          % len(self._dics)
                          )
        else:
            sh.com.cancel(f)

    def _list(self):
        if self._files:
            self._filenames = set([sh.Path(file).filename().replace('.dict','') for file in self._files])
            #todo: elaborate (make automatical, use language codes)
            #todo: forget 'Ru', check for 1st upper and 2nd lower letters
            self._en        = [elem for elem in self._filenames \
                               if 'RuEn' in elem or 'EnRu' in elem
                              ]
            self._de        = [elem for elem in self._filenames \
                               if 'RuDe' in elem or 'DeRu' in elem
                              ]
            self._es        = [elem for elem in self._filenames \
                               if 'RuEs' in elem or 'EsRu' in elem
                              ]
            self._it        = [elem for elem in self._filenames \
                               if 'RuIt' in elem or 'ItRu' in elem
                              ]
            self._fr        = [elem for elem in self._filenames \
                               if 'RuFr' in elem or 'FrRu' in elem
                              ]
        else:
            self._filenames = []
            self._en        = []
            self._de        = []
            self._es        = []
            self._it        = []
            self._fr        = []

    def debug(self):
        f = 'page.ExtDics.debug'
        message = 'English:\n'
        message += '\n'.join(self._en) + '\n\n'
        message += 'German:\n'
        message += '\n'.join(self._de) + '\n\n'
        message += 'French:\n'
        message += '\n'.join(self._fr) + '\n\n'
        message += 'Spanish:\n'
        message += '\n'.join(self._es) + '\n\n'
        message += 'Italian:\n'
        message += '\n'.join(self._it) + '\n\n'
        sh.objs.mes (f,_('INFO')
                    ,message
                    )



class Page:

    def __init__(self,source=_('All'),lang='English'
                ,search='~',url='',win_encoding='windows-1251'
                ,ext_dics=[],file=None,timeout=6
                ):
        f = 'page.Page.__init__'
        self.values()
        self._source       = source
        self._lang         = lang
        self._search       = search
        self._url          = url
        self._win_encoding = win_encoding
        self.ext_dics      = ext_dics
        self._file         = file
        self._timeout      = timeout
        if not self._source or not self._lang or not self._search \
                            or not self._win_encoding:
            self.Success   = False
            sh.com.empty(f)

    def values(self):
        self.Success   = True
        self._html_raw = self._page = ''
        self.HasLocal  = False
    
    def run(self):
        self.get                ()
        self.invalid            ()
        # HTML specific
        self.decode_entities    ()
        self.invalid2           ()
        # An excessive space must be removed after unescaping the page
        self.mt_specific_replace()
        self.common_replace     () # HTML specific
        self.article_not_found  () # HTML specific
        self.unsupported        ()
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
        self._page = self._page.replace('>;  <','><')
        self._page = self._page.replace('Требуется авторизация','')
        self._page = self._page.replace('Вы знаете перевод этого слова? Добавьте его в словарь:','')
        self._page = self._page.replace('Вы знаете перевод этого выражения? Добавьте его в словарь:','')
        self._page = self._page.replace('</span>Наблюдаются проблемы со входом из Хрома<span lang="en-us"> (</span>на','</span><span lang="en-us"></span>')
        self._page = self._page.replace('сайте кое-что устарело, но пока не удаётся поменять','')
        self._page = self._page.replace('</a>, содержащие <strong>','</a><strong>')

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

    ''' Convert HTML entities to a human readable format, e.g.,
        '&copy;' -> '©'
    '''
    # HTML specific
    def decode_entities(self):
        f = 'page.Page.decode_entities'
        #todo: do we need to check this?
        if self._source in (_('All'),_('Online')):
            try:
                self._page = html.unescape(self._page)
            except:
                sh.objs.mes (f,_('ERROR')
                            ,_('Unable to convert HTML entities to UTF-8!')
                            )

    def _get_online(self):
        f = 'page.Page._get_online'
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
        if self.ext_dics:
            self._page = self.ext_dics.get (lang   = self._lang
                                           ,search = self._search
                                           )
            if self._page:
                self.HasLocal = True

    def disamb_mt(self):
        # This is done to speed up and eliminate tag disambiguation
        try:
            self._page = self._page.replace('<tr>','').replace('</tr>','')
        # Encoding has failed
        except TypeError:
            self._page = ''

    def get(self):
        f = 'page.Page.get'
        if not self._page:
            if self._file:
                read = sh.ReadTextFile(file=self._file)
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
                                                 ,header = self._search)
                elif self._source == _('Online'):
                    self._get_online()
                    self.disamb_mt()
                elif self._source == _('Offline'):
                    self._get_offline()
                    if self.HasLocal:
                        self._page = of.stardict (text   = self._page
                                                 ,header = self._search)
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
        f = 'page.Welcome.online'
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
    f = 'page.__main__'
    import logic as lg
    sg.objs.start()
    timer = sh.Timer(func_title=f)
    timer.start()
    page = Page (source   = _('Online')
                ,search   = 'preceding'
                ,file     = '/home/pete/tmp/ars/preceding.txt'
                ,ext_dics = ExtDics(path=lg.objs.default().dics())
                )
    '''
    page = Page (source = _('Online')
                ,search = 'иммуногенная'
                ,url    = 'https://www.multitran.ru/c/M.exe?l1=1&l2=2&s=%E8%EC%F3%ED%ED%EE%E3%E5%ED%ED%E0%FF'
                )
    '''
    page.run()
    timer.end()
    '''sh.WriteTextFile (file       = '/home/pete/tmp/ars/do.txt'
                        ,AskRewrite = 0
                        ).write(text=text)
    '''
    if page._page:
        page._page = ''.join(page._page)
        sg.objs.txt().insert(text=page._page)
        sg.objs._txt.show()
    sg.objs.end()
