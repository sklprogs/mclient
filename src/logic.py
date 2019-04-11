#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import urllib.request
import html
import ssl
import shared    as sh
import sharedGUI as sg
import plugins.stardict.get
import plugins.stardict.run
import plugins.multitranru.run
import plugins.multitrancom.run

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')

pairs = ('ENG <=> RUS','DEU <=> RUS','SPA <=> RUS'
        ,'FRA <=> RUS','NLD <=> RUS','ITA <=> RUS'
        ,'LAV <=> RUS','EST <=> RUS','AFR <=> RUS'
        ,'EPO <=> RUS','RUS <=> XAL','XAL <=> RUS'
        ,'ENG <=> DEU','ENG <=> EST'
        )
langs = ('English'   # ENG <=> RUS
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
sources = (_('All'),_('Online'),_('Offline'))
sample_block = '''Австралийский сленг
Архаизм
Бранное выражение
Воровское выражение
Грубое выражение
Диалект
Жаргон
Презрительное выражение
Просторечие
Разговорное выражение
Расширение файла
Редкое выражение
Ругательство
Сленг
Табуированная лексика
Тюремный жаргон
Устаревшее слово
Фамильярное выражение
Шутливое выражение
Эвфемизм
'''
sample_prior = '''Общая лексика
Техника
Юридический термин
Юридический (Н.П.)
'''


class PhraseTerma:
    
    def __init__(self,dbc,articleid):
        f = '[MClient] logic.PhraseTerma.__init__'
        self.dbc        = dbc
        self._articleid = articleid
        self._no1       = -1
        self._no2       = -1
        if self.dbc and self._articleid:
            self.Success = True
        else:
            self.Success = False
            sh.com.empty(f)
            
    def second_phrase(self):
        f = '[MClient] logic.PhraseTerma.second_phrase'
        if self._no2 < 0:
            self.dbc.execute ('select NO from BLOCKS \
                               where ARTICLEID = ? and TYPE = ? \
                               order by NO',(self._articleid,'phrase',)
                             )
            result = self.dbc.fetchone()
            if result:
                self._no2 = result[0]
            sh.log.append (f,_('DEBUG')
                          ,str(self._no2)
                          )
        return self._no2
        
    def phrase_dic(self):
        f = '[MClient] logic.PhraseTerma.phrase_dic'
        if self._no1 < 0:
            if self._no2 >= 0:
                self.dbc.execute ('select NO from BLOCKS \
                                   where ARTICLEID = ? and TYPE = ? \
                                   and NO < ? order by NO desc'
                                   ,(self._articleid,'dic',self._no2,)
                                 )
                result = self.dbc.fetchone()
                if result:
                    self._no1 = result[0]
                    self.dbc.execute ('update BLOCKS set SELECTABLE=1 \
                                       where NO = ?',(self._no1,)
                                     )
            else:
                sh.log.append (f,_('WARNING')
                              ,_('Wrong input data!')
                              )
            sh.log.append (f,_('DEBUG')
                          ,str(self._no1)
                          )
        return self._no1
        
    def dump(self):
        f = '[MClient] logic.PhraseTerma.dump'
        # Autoincrement starts with 1 in sqlite
        if self._no1 > 0 and self._no2 > 0:
            sh.log.append (f,_('INFO')
                          ,_('Update DB, range %d-%d') \
                          % (self._no1,self._no2)
                          )
            self.dbc.execute ('update BLOCKS set TERMA=? where NO >= ? \
                               and NO < ?',('',self._no1,self._no2,)
                             )
        else:
            sh.log.append (f,_('WARNING')
                          ,_('Wrong input data!')
                          )
        
    def run(self):
        f = '[MClient] logic.PhraseTerma.run'
        if self.Success:
            self.second_phrase()
            self.phrase_dic()
            self.dump()
        else:
            sh.com.cancel(f)



class Translate:

    def __init__ (self,source=_('All'),search=''
                 ,url='',timeout=6,articleid=0
                 ):
        self.values()
        self._source    = source
        self._search    = search
        self._url       = url
        self._timeout   = timeout
        self._articleid = articleid
    
    def values(self):
        self._plugin  = None
        self.HasLocal = False
        self._text    = ''
        self._html    = ''
        self._blocks  = []
        self._data_sd = []
        self._data_mr = []
        self._data_mc = []
    
    def run(self):
        f = '[MClient] logic.Translate.run'
        if self._source and self._search:
            if self._source in sources:
                timer = sh.Timer(f)
                timer.start()
                plugin_sd = plugins.stardict.run.Plugin (search    = self._search
                                                        ,url       = self._url
                                                        ,timeout   = self._timeout
                                                        ,articleid = self._articleid
                                                        ,iabbr     = objs.order().dic
                                                        )
                plugin_mr = plugins.multitranru.run.Plugin (search    = self._search
                                                           ,url       = self._url
                                                           ,timeout   = self._timeout
                                                           ,articleid = self._articleid
                                                           ,iabbr     = objs._order.dic
                                                           )
                plugin_mc = plugins.multitrancom.run.Plugin (search    = self._search
                                                            ,url       = self._url
                                                            ,timeout   = self._timeout
                                                            ,articleid = self._articleid
                                                            ,iabbr     = objs._order.dic
                                                            )
                if self._source in (_('All'),_('Offline')):
                    plugin_sd.run()
                if self._source in (_('All'),_('Online')):
                    plugin_mr.run()
                    #cur
                    #todo: uncomment when URLs are fixed
                    #plugin_mc.run()
                self._text = [plugin_sd._text,plugin_mr._text
                             ,plugin_mc._text
                             ]
                self._text = [item for item in self._text if item]
                self._text = '\n'.join(self._text)
                #todo: integrate htmls
                self._html   = plugin_sd._html + plugin_mr._html \
                                               + plugin_mc._html
                self._blocks = plugin_sd._blocks + plugin_mr._blocks \
                                                 + plugin_mc._blocks
                if plugin_sd._blocks:
                    self.HasLocal = True
                self._data_sd = plugin_sd._data
                self._data_mr = plugin_mr._data
                self._data_mc = plugin_mc._data
                timer.end()
            else:
                sh.objs.mes (f,_('ERROR')
                            ,_('An unknown mode "%s"!\n\nThe following modes are supported: "%s".') \
                            % (str(self._source),';'.join(sources))
                            )
        else:
            sh.com.empty(f)



class Welcome:

    def __init__ (self,url=None,product='MClient'
                 ,version='current',timeout=6
                 ):
        if not url:
            ''' 'https://www.multitran.ru' is got faster than
                'http://www.multitran.ru' (~0.2s)
            '''
            url = 'https://www.multitran.ru'
        self._url       = url
        self._product   = product
        self._version   = version
        self._st_status = len(plugins.stardict.get.objs.all_dics()._dics)
        self._timeout   = timeout
        self._mt_status = 'not running'
        self._mt_color  = 'red'
        self._st_color  = 'red'
        self._desc      = sh.List (lst1 = [self._product
                                          ,self._version
                                          ]
                                  ).space_items()

    def online(self):
        f = '[MClient] logic.Welcome.online'
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



class Online(sh.Online):

    def __init__ (self,base_str='%s',search_str=''
                 ,encoding='UTF-8'
                 ):
        super().__init__()
    
    def get_bytes(self):
        if not self._bytes:
            # Otherwise, will not be able to encode 'Ъ'
            try:
                self._bytes = bytes (self.search_str
                                    ,encoding = 'windows-1251'
                                    )
            except:
                ''' Otherwise, will not be able to encode specific
                    characters
                '''
                try:
                    self._bytes = bytes (self.search_str
                                        ,encoding='UTF-8'
                                        )
                except:
                    self._bytes = ''
        return self._bytes



class DefaultConfig:
    
    def __init__(self,product='mclient'):
        self.values()
        self.ihome   = sh.Home(app_name=product.lower())
        self.Success = self.ihome.create_conf()
    
    def values(self):
        self._dics   = ''
        self._fabbr  = ''
        self._fblock = ''
        self._fprior = ''
        self._fdconf = ''
        self._fconf  = ''
    
    def dics(self):
        f = '[MClient] logic.DefaultConfig.dics'
        if self.Success:
            if not self._dics:
                self._dics = self.ihome.add_config('dics')
                if self._dics:
                    if os.path.exists(self._dics):
                        self.Success = sh.Directory(path=self._dics).Success
                    else:
                        self.Success = sh.Path(path=self._dics).create()
                else:
                    self.Success = False
                    sh.com.empty(f)
            return self._dics
        else:
            sh.com.cancel(f)
    
    def block(self):
        f = '[MClient] logic.DefaultConfig.block'
        if self.Success:
            self._fblock = self.ihome.add_config('block.txt')
            if self._fblock:
                if os.path.exists(self._fblock):
                    self.Success = sh.File(file=self._fblock).Success
                else:
                    iwrite = sh.WriteTextFile (file    = self._fblock
                                              ,Rewrite = True
                                              )
                    iwrite.write(sample_block)
                    self.Success = iwrite.Success
            else:
                self.Success = False
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def prioritize(self):
        f = '[MClient] logic.DefaultConfig.prioritize'
        if self.Success:
            if not self._fprior:
                self._fprior = self.ihome.add_config('prioritize.txt')
                if self._fprior:
                    if os.path.exists(self._fprior):
                        self.Success = sh.File(file=self._fprior).Success
                    else:
                        iwrite = sh.WriteTextFile (file    = self._fprior
                                                  ,Rewrite = True
                                                  )
                        iwrite.write(sample_prior)
                        self.Success = iwrite.Success
                else:
                    self.Success = False
                    sh.com.empty(f)
            return self._fprior
        else:
            sh.com.cancel(f)
    
    def abbr(self):
        f = '[MClient] logic.DefaultConfig.abbr'
        if self.Success:
            if not self._fabbr:
                self._fabbr  = sh.objs.pdir().add ('..','resources'
                                                  ,'abbr.txt'
                                                  )
                self.Success = sh.File(file=self._fabbr).Success
            return self._fabbr
        else:
            sh.com.cancel(f)
    
    def default_config(self):
        f = '[MClient] logic.DefaultConfig.default_config'
        if self.Success:
            if not self._fdconf:
                self._fdconf = sh.objs.pdir().add ('..','resources'
                                                  ,'default.cfg'
                                                  )
                self.Success = sh.File(file=self._fdconf).Success
            return self._fdconf
        else:
            sh.com.cancel(f)
    
    def config(self):
        f = '[MClient] logic.DefaultConfig.config'
        if self.Success:
            if not self._fconf:
                self._fconf = self.ihome.add_config('mclient.cfg')
                if os.path.exists(self._fconf):
                    self.Success = sh.File(file=self._fconf).Success
                else:
                    self.default_config()
                    if self.Success:
                        self.Success = sh.File (file = self._fdconf
                                               ,dest = self._fconf
                                               ).copy()
                    else:
                        sh.com.cancel(f)
            return self._fconf
        else:
            sh.com.cancel(f)
    
    def run(self):
        f = '[MClient] logic.DefaultConfig.run'
        if self.Success:
            self.default_config()
            self.config()
            self.abbr()
            self.dics()
            self.block()
            self.prioritize()
        else:
            sh.com.cancel(f)



class ConfigMclient(sh.Config):

    def __init__(self):
        super().__init__()
        self.sections         = [sh.SectionBooleans
                                ,sh.SectionIntegers
                                ,sh.SectionVariables
                                ]
        self.sections_abbr    = [sh.SectionBooleans_abbr
                                ,sh.SectionIntegers_abbr
                                ,sh.SectionVariables_abbr
                                ]
        self.sections_func    = [sh.config_parser.getboolean
                                ,sh.config_parser.getint
                                ,sh.config_parser.get
                                ]
        self.message          = _('The following sections and/or keys are missing:') + '\n'
        self.total_keys       = 0
        self.changed_keys     = 0
        self.missing_keys     = 0
        self.missing_sections = 0
        # Create these keys before reading the config
        self.path    = objs.default().ihome.add_config('mclient.cfg')
        self.reset()
        iread        = sh.ReadTextFile(self.path)
        self.text    = iread.get()
        self.Success = iread.Success
        self.default()
        if os.path.exists(self.path):
            self.open()
        else:
            self.Success = False
        self.check()
        self.load()

    def default(self):
        self._default_bool()
        self._default_int()
        self._default_var()
        
    def _default_bool(self):
        sh.globs['bool'].update ({
            'AutoCloseSpecSymbol':False
           ,'Autocompletion'     :True
           ,'SelectTermsOnly'    :True
           ,'Iconify'            :True
                                })
    
    def _default_int(self):
        sh.globs['int'].update ({
            'col_width'         :250
           ,'font_comments_size':3
           ,'font_col1_size'    :4
           ,'font_col2_size'    :4
           ,'font_col3_size'    :3
           ,'font_col4_size'    :3
           ,'font_terms_size'   :4
           ,'timeout'           :5
                               })
    
    def _default_var(self):
        sh.globs['var'].update ({
            'bind_clear_history'          :'<Control-Shift-Delete>'
           ,'bind_clear_search_field'     :'<ButtonRelease-3>'
           ,'bind_col1_down'              :'<Control-Down>'
           ,'bind_col1_up'                :'<Control-Up>'
           ,'bind_col2_down'              :'<Alt-Down>'
           ,'bind_col2_up'                :'<Alt-Up>'
           ,'bind_col3_down'              :'<Shift-Down>'
           ,'bind_col3_up'                :'<Shift-Up>'
           ,'bind_copy_article_url'       :'<Control-F7>'
           ,'bind_copy_sel_alt'           :'<Control-KP_Enter>'
           ,'bind_copy_sel'               :'<Control-Return>'
           ,'bind_copy_url'               :'<Shift-F7>'
           ,'bind_define'                 :'<Control-d>'
           ,'bind_go_back'                :'<Alt-Left>'
           ,'bind_go_forward'             :'<Alt-Right>'
           ,'bind_go_phrases'             :'<Alt-f>'
           ,'bind_next_pair'              :'<F8>'
           ,'bind_next_pair_alt'          :'<Control-l>'
           ,'bind_prev_pair'              :'<Shift-F8>'
           ,'bind_prev_pair_alt'          :'<Control-L>'
           ,'bind_open_in_browser_alt'    :'<Control-b>'
           ,'bind_open_in_browser'        :'<F7>'
           ,'bind_paste_search_field'     :'<ButtonRelease-2>'
           ,'bind_print'                  :'<Control-p>'
           ,'bind_quit_now_alt'           :'<F10>'
           ,'bind_quit_now'               :'<Control-q>'
           ,'bind_re_search_article'      :'<Control-F3>'
           ,'bind_reload_article_alt'     :'<Control-r>'
           ,'bind_reload_article'         :'<F5>'
           ,'bind_save_article_alt'       :'<Control-s>'
           ,'bind_save_article'           :'<F2>'
           ,'bind_search_article_backward':'<Shift-F3>'
           ,'bind_search_article_forward' :'<F3>'
           ,'bind_settings'               :'<Alt-s>'
           ,'bind_settings_alt'           :'<F12>'
           ,'bind_show_about'             :'<F1>'
           ,'bind_spec_symbol'            :'<Control-e>'
           ,'bind_toggle_alphabet'        :'<Alt-a>'
           ,'bind_toggle_block'           :'<Alt-b>'
           ,'bind_toggle_history_alt'     :'<Control-h>'
           ,'bind_toggle_history'         :'<F4>'
           ,'bind_toggle_priority'        :'<Alt-p>'
           ,'bind_toggle_sel'             :'<Control-t>'
           ,'bind_toggle_view'            :'<F6>'
           ,'bind_toggle_view_alt'        :'<Alt-v>'
           ,'color_comments'              :'gray'
           ,'color_col1'                  :'coral'
           ,'color_col2'                  :'cadet blue'
           ,'color_col3'                  :'slate gray'
           ,'color_col4'                  :'slate gray'
           ,'color_terms_sel_bg'          :'cyan'
           ,'color_terms_sel_fg'          :'black'
           ,'color_terms'                 :'black'
           ,'font_comments_family'        :'Mono'
           ,'font_col1_family'            :'Arial'
           ,'font_col2_family'            :'Arial'
           ,'font_col3_family'            :'Mono'
           ,'font_col4_family'            :'Mono'
           ,'font_history'                :'Sans 12'
           ,'font_style'                  :'Sans 14'
           ,'font_terms_sel'              :'Sans 14 bold italic'
           ,'font_terms_family'           :'Serif'
           ,'pair_afr_rus'                :'l1=31&l2=2&s=%s'
           ,'pair_deu_rus'                :'l1=3&l2=2&s=%s'
           ,'pair_eng_deu'                :'l1=1&l2=3&s=%s'
           ,'pair_eng_est'                :'l1=1&l2=26&s=%s'
           ,'pair_eng_rus'                :'l1=1&l2=2&s=%s'
           ,'pair_epo_rus'                :'l1=34&l2=2&s=%s'
           ,'pair_est_rus'                :'l1=26&l2=2&s=%s'
           ,'pair_fra_rus'                :'l1=4&l2=2&s=%s'
           ,'pair_ita_rus'                :'l1=23&l2=2&s=%s'
           ,'pair_lav_rus'                :'l1=27&l2=2&s=%s'
           ,'pair_nld_rus'                :'l1=24&l2=2&s=%s'
           ,'pair_root'                   :'https://www.multitran.ru/c/M.exe?'
           ,'pair_rus_xal'                :'l1=2&l2=35&s=%s'
           ,'pair_spa_rus'                :'l1=5&l2=2&s=%s'
           ,'pair_xal_rus'                :'l1=35&l2=2&s=%s'
           ,'repeat_sign'                 :'!'
           ,'repeat_sign2'                :'!!'
           ,'spec_syms'                   :'àáâäāæßćĉçèéêēёëəғĝģĥìíîïīĵķļñņòóôõöōœøšùúûūŭũüýÿžжҗқңөүұÀÁÂÄĀÆSSĆĈÇÈÉÊĒЁËƏҒĜĢĤÌÍÎÏĪĴĶĻÑŅÒÓÔÕÖŌŒØŠÙÚÛŪŬŨÜÝŸŽЖҖҚҢӨҮҰ'
           ,'web_search_url'              :'http://www.google.ru/search?ie=UTF-8&oe=UTF-8&sourceid=navclient=1&q=%s'
                               })

    def reset(self):
        sh.globs['bool']  = {}
        sh.globs['float'] = {}
        sh.globs['int']   = {}
        sh.globs['var']   = {}



class CurRequest:

    def __init__(self):
        self.values()
        self.reset()

    def values(self):
        ''' #note: this should be synchronized with the 'default' value
            of objs.webframe().menu_columns
        '''
        self._collimit     = 8
        # Default priorities of parts of speech
        self._pr_n         = 7
        self._pr_v         = 6
        self._pr_adj       = 5
        self._pr_abbr      = 4
        self._pr_adv       = 3
        self._pr_prep      = 2
        self._pr_pron      = 1
        self._source       = _('All')
        self._lang         = 'English'
        self._cols         = ('dic','wform','transc','speech')
        ''' Toggling blacklisting should not depend on a number of
            blocked dictionaries (otherwise, it is not clear how
            blacklisting should be toggled)
        '''
        self.Block         = True
        self.CaptureHotkey = True
        self.MouseClicked  = False
        self.Prioritize    = True
        self.Reverse       = False
        self.SortRows      = True
        self.SortTerms     = True
        ''' *Temporary* turn off prioritizing and terms sorting for
            articles with 'sep_words_found' and in phrases; use previous
            settings for new articles
        '''
        self.SpecialPage   = False
    
    def reset(self):
        self._page         = ''
        self._html         = ''
        self._html_raw     = ''
        self._search       = ''
        self._url          = ''



# Read the blocklist and the prioritize list
class Lists:

    def __init__(self):
        f = '[MClient] logic.Lists.__init__'
        self._blacklist  = objs.default()._fblock
        self._prioritize = objs._default._fprior
        self._abbr       = objs._default._fabbr
        self.Success     = objs._default.Success

    def abbr(self):
        if self.Success:
            dic = sh.Dic (file     = self._abbr
                         ,Sortable = True
                         )
            self.Success = dic.Success
            return dic
        else:
            sh.com.cancel(f)
    
    def blacklist(self):
        f = '[MClient] logic.Lists.blacklist'
        if self.Success:
            text = sh.ReadTextFile(file=self._blacklist).get()
            text = sh.Text(text=text,Auto=1).text
            return text.splitlines()
        else:
            sh.com.cancel(f)

    def prioritize(self):
        f = '[MClient] logic.Lists.prioritize'
        if self.Success:
            text = sh.ReadTextFile(file=self._prioritize).get()
            text = sh.Text(text=text,Auto=1).text
            return text.splitlines()
        else:
            sh.com.cancel(f)



class Objects:
    
    def __init__(self):
        self._online = self._request = self._order = self._default \
                     = self._online_mt = None
    
    def default(self,product='mclient'):
        if not self._default:
            self._default = DefaultConfig(product=product)
            self._default.run()
        return self._default
    
    def online_mt(self):
        if self._online_mt is None:
            self._online_mt = Online()
        return self._online_mt
    
    def online(self):
        #todo: create a sub-source
        if self.request()._source in (_('All'),_('Online')):
            return objs.online_mt()
        else:
            return sh.objs.online()
    
    def request(self):
        if self._request is None:
            self._request = CurRequest()
        return self._request
        
    def order(self):
        if self._order is None:
            self._order = Order()
        return self._order



# Create block and priority lists and complement them
class Order:
    
    def __init__(self):
        self.values()
        self._lists()
        self._dic()
        self._conform()
        
    def _fill_dic(self,lst,ind):
        lst = lst[1:]
        lst = lst[::-1]
        for item in lst:
            self._prioritize.insert(ind,item)
    
    def prioritize_by(self,Down=False):
        f = '[MClient] logic.Order.prioritize_by'
        if self.Success:
            if self._dic1 and self._dic2:
                ''' - Multiple dictionary titles share same blocks
                      for now, so we cannot distinguish them. Thus, all
                      titles of the same block must have the same
                      priority. Moreover, if any item of 'dic1' is
                      (un)prioritized, then all other items should be
                      (un)prioritized as well.
                    - Since we (un)prioritize one dictionary against
                      another here instead of simply (un)prioritizing
                      one dictionary (this logic is set in
                      'lm_auto'/'rm_auto'), both 'dic1' and 'dic2'
                      should comprise prioritized dictionaries. Since we
                      cannot distinguish multiple dictionary titles for
                      now, both 'dic1' and 'dic2' should be fully
                      introduced into 'self._prioritize'.
                    - The only way to get a position of 'dic1' being
                      prioritized over 'dic2' is to get the position of
                      'dic2' in 'self._prioritize' first. Since both
                      'dic1' and 'dic2' have prioritized items (this
                      logic is set in 'lm_auto'/'rm_auto') and are
                      previously sorted by priority, first items of
                      'dic1' and 'dic2' should always exist (otherwise,
                      it is a logic error).
                '''
                if self._dic1[0] in self._prioritize \
                and self._dic2[0] in self._prioritize:
                    
                    if Down:
                        message = _('Mode: "%s"') \
                                  % _('Decrease priority')
                    else:
                        message = _('Mode: "%s"') \
                                  % _('Increase priority')
                    sh.log.append (f,_('DEBUG')
                                  ,message
                                  )
                    
                    # This allows not to delete duplicates later
                    for i in range(len(self._dic1)):
                        if i > 0:
                            self.unprioritize(self._dic1[i])
                    for i in range(len(self._dic2)):
                        if i > 0:
                            self.unprioritize(self._dic2[i])
                    
                    ind1 = self._prioritize.index(self._dic1[0])
                    ind2 = self._prioritize.index(self._dic2[0])
                    
                    if Down:
                        Swap = ind1 < ind2
                    else:
                        Swap = ind1 > ind2
                    if Swap:
                        sh.log.append (f,_('DEBUG')
                                      ,_('Swap items: %d <-> %d; "%s" <-> "%s"') \
                                      % (ind1,ind2
                                        ,self._prioritize[ind1]
                                        ,self._prioritize[ind2]
                                        )
                                      )
                        self._prioritize[ind1], self._prioritize[ind2] \
                        = self._prioritize[ind2], self._prioritize[ind1]
                    
                    ind1 += 1
                    ind2 += 1
                    
                    if Swap:
                        dic1 = self._dic2
                        dic2 = self._dic1
                    else:
                        dic1 = self._dic1
                        dic2 = self._dic2
                    
                    if ind2 > ind1:
                        self._fill_dic(dic2,ind2)
                        self._fill_dic(dic1,ind1)
                    else:
                        self._fill_dic(dic1,ind1)
                        self._fill_dic(dic2,ind2)
                        
                    lst = sh.List(lst1=self._prioritize).duplicates()
                    if lst:
                        self._prioritize = list(lst)
                    else:
                        sh.com.empty(f)
                    
                    sh.log.append (f,_('DEBUG')
                                  ,'Dic1: ' + str(self._dic1)
                                  )
                    sh.log.append (f,_('DEBUG')
                                  ,'Dic2: ' + str(self._dic2)
                                  )
                    sh.log.append (f,_('DEBUG')
                                  ,str(self._prioritize)
                                  )
                else:
                    sh.objs.mes (f,_('ERROR')
                                ,_('Logic error!')
                                )
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
            
    def priority(self,search):
        f = '[MClient] logic.Order.priority'
        if self.Success:
            lst = self.get_list(search)
            if lst:
                prior = []
                for item in lst:
                    try:
                        ind = self._prioritize.index(item)
                        prior.append(len(self._prioritize)-ind)
                    except ValueError:
                        pass
                if prior:
                    return max(prior)
                else:
                    return 0
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def lm_auto(self,dic1,dic2=''):
        ''' A LM click on:
            1) A blocked dictionary     - unblock
            2) A common dictionary      - prioritize
            3) A prioritized dictionary - increase priority
        '''
        f = '[MClient] logic.Order.lm_auto'
        if self.Success:
            self.set(dic1,dic2)
            if self.is_blocked(self._dic1):
                for item in self._dic1:
                    self.unblock(item)
            elif self.is_prioritized(self._dic1) \
            and self.is_prioritized(self._dic2) \
            and not sh.List(self._dic1,self._dic2).shared():
                self.prioritize_by()
            else:
                for item in self._dic1:
                    self.prioritize(item)
        else:
            sh.com.cancel(f)
    
    def rm_auto(self,dic1,dic2=''):
        ''' A RM click on:
            1) A prioritized dictionary - decrease priority or
                                          unprioritize
                                          (at minimal priority)
            2) A blocked dictionary     - unblock
            3) A common dictionary      - block
        '''
        f = '[MClient] logic.Order.rm_auto'
        if self.Success:
            self.set(dic1,dic2)
            if self.is_blocked(self._dic1):
                for item in self._dic1:
                    self.unblock(item)
            elif self.is_prioritized(self._dic1):
                if self.is_prioritized(self._dic2) \
                and not sh.List(self._dic1,self._dic2).shared():
                    self.prioritize_by(Down=True)
                else:
                    for item in self._dic1:
                        self.unprioritize(item)
            else:
                ''' Multiple dictionary titles share same blocks
                    for now, so we cannot distinguish them. Thus,
                    if any item of 'dic1' is blocked, then all
                    other items should be blocked as well.
                '''
                for item in self._dic1:
                    self.block(item)
        else:
            sh.com.cancel(f)
    
    def is_prioritized(self,lst):
        f = '[MClient] logic.Order.is_prioritized'
        if self.Success:
            if lst:
                for item in lst:
                    if item in self._prioritize:
                        return True
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def is_blocked(self,lst):
        f = '[MClient] logic.Order.is_blocked'
        if self.Success:
            if lst:
                for item in lst:
                    if item in self._blacklist:
                        return True
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def _conform(self):
        f = '[MClient] logic.Order._conform'
        ''' Create new block and priority lists based on those that were
            read from user files. Lists from user files may comprise
            either dictionary abbreviations or full dictionary titles.
            New lists will be lowercased and stripped and will comprise
            both abbreviations and full titles.
        '''
        if self.Success:
            self._abbrs  = [item.lower().strip() \
                            for item in self.dic.orig
                           ]
            self._titles = [item.lower().strip() \
                            for item in self.dic.transl
                           ]
            ''' We recreate lists in order to preserve 
                the abbreviation + title order.
            '''
            if self._blacklist:
                blacklist = list(self._blacklist)
                self._blacklist = []
                for item in blacklist:
                    pair = self.get_pair(item)
                    if pair:
                        self.block(pair[0])
                        self.block(pair[1])
                    else:
                        sh.com.empty(f)
            else:
                sh.com.empty(f)
            if self._prioritize:
                prioritize = list(self._prioritize)
                self._prioritize = []
                for item in prioritize:
                    pair = self.get_pair(item)
                    if pair:
                        self.prioritize(pair[0])
                        self.prioritize(pair[1])
                    else:
                        sh.com.empty(f)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def _lists(self):
        f = '[MClient] logic.Order._lists'
        if self.Success:
            self.lists       = Lists()
            self._blacklist  = sh.Input (title = f
                                        ,value = self.lists.blacklist()
                                        ).list()
            self._prioritize = sh.Input (title = f
                                        ,value = self.lists.prioritize()
                                        ).list()
            self.Success     = self.lists.Success
        else:
            sh.com.cancel(f)
        
    def _dic(self):
        f = '[MClient] logic.Order._dic'
        if self.Success:
            self.dic     = self.lists.abbr()
            self.Success = self.dic.Success
        else:
            sh.com.cancel(f)
    
    def values(self):
        self.Success     = True
        self.lists       = None
        self.dic         = None
        self._abbrs      = []
        self._titles     = []
        self._blacklist  = []
        self._prioritize = []
        self._dic1       = ''
        self._dic2       = ''
            
    def sort_dic(self,lst):
        f = '[MClient] logic.Order.sort_dic'
        if self.Success:
            if lst:
                indexes = []
                for item in lst:
                    try:
                        ind = self._prioritize.index(item)
                    except ValueError:
                        # Place an unpriotitized dictionary at the end
                        ind = 1000
                    indexes.append(ind)
                lst = sorted(zip(indexes,lst))
                lst = [item[1] for item in lst]
                return lst
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def set(self,dic1,dic2=''):
        f = '[MClient] logic.Order.set'
        if self.Success:
            ''' This allows to return an empty value instead of the last
                memory in case there is no previous/next dictionary.
            '''
            self._dic1 = self._dic2 = ''
            if dic1:
                dic1 = self.get_list(dic1)
                dic1 = self.sort_dic(dic1)
                self._dic1 = list(dic1)
            else:
                sh.com.empty(f)
            if dic2:
                dic2 = self.get_list(dic2)
                dic2 = self.sort_dic(dic2)
                self._dic2 = list(dic2)
        else:
            sh.com.cancel(f)
    
    def title(self,abbr):
        f = '[MClient] logic.Order.title'
        if self.Success:
            try:
                ind = self._abbrs.index(abbr)
                return self._titles[ind]
            except ValueError:
                sh.log.append (f,_('WARNING')
                              ,_('Wrong input data!')
                              )
        else:
            sh.com.cancel(f)
        
    def abbr(self,title):
        f = '[MClient] logic.Order.abbr'
        if self.Success:
            try:
                ind = self._titles.index(title)
                return self._abbrs[ind]
            except ValueError:
                sh.log.append (f,_('WARNING')
                              ,_('Wrong input data!')
                              )
        else:
            sh.com.cancel(f)
    
    def get_pair(self,item):
        f = '[MClient] logic.Order.get_pair'
        if self.Success:
            if item:
                item = item.lower().strip()
                abbr = title = ''
                if item in self._titles:
                    title = item
                    abbr  = self.abbr(title)
                elif item in self._abbrs:
                    abbr  = item
                    title = self.title(abbr)
                else:
                    sh.log.append (f,_('WARNING')
                                  ,_('Unknown dictionary "%s"!') \
                                  % str(item)
                                  )
                    abbr = title = str(item)
                return([abbr,title])
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def get_list(self,search):
        f = '[MClient] logic.Order.get_list'
        if self.Success:
            if search:
                search = search.split(',')
                lst    = []
                for item in search:
                    pair = self.get_pair(item)
                    if pair:
                        lst += pair
                return lst
            # Prevents from None
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def block(self,item):
        if self.Success:
            if not item in self._blacklist:
                self._blacklist.append(item)
                          
    def unblock(self,item):
        f = '[MClient] logic.Order.unblock'
        if self.Success:
            try:
                self._blacklist.remove(item)
            except ValueError:
                pass
        else:
            sh.com.cancel(f)
                          
    def prioritize(self,item):
        f = '[MClient] logic.Order.prioritize'
        if self.Success:
            if not item in self._prioritize:
                self._prioritize.append(item)
        else:
            sh.com.cancel(f)
    
    def unprioritize(self,item):
        f = '[MClient] logic.Order.unprioritize'
        if self.Success:
            try:
                self._prioritize.remove(item)
            except ValueError:
                pass
        else:
            sh.com.cancel(f)



# Multitran-only
class Suggestion:
    
    def __init__(self,search,pair,limit=0):
        self._search = search
        self._pair   = pair
        self._limit  = limit
        self.values()
        self.check()
        self.pair()
        
    def values(self):
        self._url    = ''
        self._items  = []
        self.Success = True
    
    def pair(self):
        f = '[MClient] logic.Suggestion.pair'
        if self.Success:
            self._pair = self._pair.replace('M.exe?','ms.exe?').replace('m.exe?','ms.exe?')
        else:
            sh.com.cancel(f)
    
    def check(self):
        f = '[MClient] logic.Suggestion.check'
        if self._search:
            if not isinstance(self._search,str):
                self.Success = False
                sh.log.append (f,_('WARNING')
                              ,_('Wrong input data: "%s"') \
                              % str(self._search)
                              )
        else:
            self.Success = False
            sh.log.append (f,_('INFO')
                          ,_('Nothing to do!')
                          )
        if self._pair:
            if not self._pair in online_dic_urls:
                self.Success = False
                sh.log.append (f,_('WARNING')
                              ,_('Wrong input data: "%s"') \
                              % str(self._pair)
                              )
        else:
            self.Success = False
            sh.com.empty(f)
        if not isinstance(self._limit,int):
            self.Success = False
            sh.log.append (f,_('WARNING')
                          ,_('Wrong input data: "%s"') \
                          % str(self._limit)
                          )
    
    def url(self):
        f = '[MClient] logic.Suggestion.url'
        if self.Success:
            if not self._url:
                self._url = sh.Online (base_str   = self._pair
                                      ,search_str = self._search
                                      ).url()
            return self._url
        else:
            sh.com.cancel(f)
    
    def get(self):
        f = '[MClient] logic.Suggestion.get'
        if self.Success:
            if not self._items:
                if self.url():
                    self._items = sh.Get (url      = self._url
                                         ,encoding = 'windows-1251'
                                         ).run()
                    if self._items:
                        self._items = html.unescape(self._items)
                        self._items = [item for item \
                                       in self._items.splitlines() \
                                       if item
                                      ]
                        if self._limit:
                            self._items = self._items[0:self._limit]
                        return self._items
                    else:
                        sh.com.empty(f)
                else:
                    sh.com.empty(f)
        else:
            sh.com.cancel(f)



objs = Objects()
ConfigMclient()

online_dic_urls = (sh.globs['var']['pair_root'] + sh.globs['var']['pair_eng_rus']   # ENG <=> RUS, 'l1=1&l2=2&s=%s'
                  ,sh.globs['var']['pair_root'] + sh.globs['var']['pair_deu_rus']   # DEU <=> RUS, 'l1=3&l2=2&s=%s'
                  ,sh.globs['var']['pair_root'] + sh.globs['var']['pair_spa_rus']   # SPA <=> RUS, 'l1=5&l2=2&s=%s'
                  ,sh.globs['var']['pair_root'] + sh.globs['var']['pair_fra_rus']   # FRA <=> RUS, 'l1=4&l2=2&s=%s'
                  ,sh.globs['var']['pair_root'] + sh.globs['var']['pair_nld_rus']   # NLD <=> RUS, 'l1=24&l2=2&s=%s'
                  ,sh.globs['var']['pair_root'] + sh.globs['var']['pair_ita_rus']   # ITA <=> RUS, 'l1=23&l2=2&s=%s'
                  ,sh.globs['var']['pair_root'] + sh.globs['var']['pair_lav_rus']   # LAV <=> RUS, 'l1=27&l2=2&s=%s'
                  ,sh.globs['var']['pair_root'] + sh.globs['var']['pair_est_rus']   # EST <=> RUS, 'l1=26&l2=2&s=%s'
                  ,sh.globs['var']['pair_root'] + sh.globs['var']['pair_afr_rus']   # AFR <=> RUS, 'l1=31&l2=2&s=%s'
                  ,sh.globs['var']['pair_root'] + sh.globs['var']['pair_epo_rus']   # EPO <=> RUS, 'l1=34&l2=2&s=%s'
                  ,sh.globs['var']['pair_root'] + sh.globs['var']['pair_rus_xal']   # RUS <=> XAL, 'l1=2&l2=35&s=%s'
                  ,sh.globs['var']['pair_root'] + sh.globs['var']['pair_xal_rus']   # XAL <=> RUS, 'l1=35&l2=2&s=%s'
                  ,sh.globs['var']['pair_root'] + sh.globs['var']['pair_eng_deu']   # ENG <=> DEU, 'l1=1&l2=3&s=%s'
                  ,sh.globs['var']['pair_root'] + sh.globs['var']['pair_eng_est']   # ENG <=> EST, 'l1=1&l2=26&s=%s'
                  )

plugins.stardict.get.PATH = objs.default().dics()
plugins.stardict.get.objs.all_dics()
