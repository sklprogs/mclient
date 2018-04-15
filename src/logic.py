#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import shared as sh

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')


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
        self.path    = sh.objs.pdir().add('..','user','mclient.cfg')
        self.reset()
        h_read       = sh.ReadTextFile(self.path)
        self.text    = h_read.get()
        self.Success = h_read.Success
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
           ,'bind_copy_article_url'       :'<Shift-F7>'
           ,'bind_copy_sel_alt'           :'<Control-KP_Enter>'
           ,'bind_copy_sel'               :'<Control-Return>'
           ,'bind_copy_url'               :'<Control-F7>'
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
           ,'pair_eng_rus'                :'CL=1&s=%s'
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
           ,'win_encoding'                :'windows-1251'
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



class Paths:

    def __init__(self):
        self.dir = sh.Directory (path=sh.objs.pdir().add ('..'
                                                         ,'user'
                                                         ,'dics'
                                                         )
                                )
        self.Success = self.dir.Success

    def blacklist(self):
        if self.Success:
            instance = sh.File (file = os.path.join (self.dir.dir
                                                    ,'block.txt'
                                                    )
                               )
            self.Success = instance.Success
            if self.Success:
                return instance.file
            else:
                sh.log.append ('Paths.blacklist'
                              ,_('WARNING')
                              ,_('Operation has been canceled.')
                              )
        else:
            sh.log.append ('Paths.blacklist'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )

    def prioritize(self):
        if self.Success:
            instance = sh.File (file = os.path.join (self.dir.dir
                                                    ,'prioritize.txt'
                                                    )
                               )
            self.Success = instance.Success
            if self.Success:
                return instance.file
            else:
                sh.log.append ('Paths.prioritize'
                              ,_('WARNING')
                              ,_('Operation has been canceled.')
                              )
        else:
            sh.log.append ('Paths.prioritize'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
                          
    def abbr(self):
        if self.Success:
            instance = sh.File (file = sh.objs.pdir().add ('..'
                                                          ,'user'
                                                          ,'dic_abbr.txt'
                                                          )
                                                    
                               )
            self.Success = instance.Success
            if self.Success:
                return instance.file
            else:
                sh.log.append ('Paths.abbr'
                              ,_('WARNING')
                              ,_('Operation has been canceled.')
                              )
        else:
            sh.log.append ('Paths.abbr'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )



# Read the blocklist and the prioritize list
class Lists:

    def __init__(self):
        paths            = Paths()
        self._blacklist  = paths.blacklist()
        self._prioritize = paths.prioritize()
        self._abbr       = paths.abbr()
        self.Success     = paths.Success

    def abbr(self):
        if self.Success:
            dic = sh.Dic (file     = self._abbr
                         ,Sortable = True
                         )
            self.Success = dic.Success
            return dic
        else:
            sh.log.append ('Lists.abbr'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def blacklist(self):
        if self.Success:
            text = sh.ReadTextFile(file=self._blacklist).get()
            text = sh.Text(text=text,Auto=1).text
            return text.splitlines()
        else:
            sh.log.append ('Lists.blacklist'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )

    def prioritize(self):
        if self.Success:
            text = sh.ReadTextFile(file=self._prioritize).get()
            text = sh.Text(text=text,Auto=1).text
            return text.splitlines()
        else:
            sh.log.append ('Lists.prioritize'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )



class Objects:
    
    def __init__(self):
        self._abbr = self._lists = self._request = self._online \
                   = self._blacklist = self._prioritize \
                   = self._abbrs_low = self._titles_low = None
        
    def titles_low(self):
        if self._titles_low is None:
            dic = self.abbr()
            if dic:
                self._titles_low = [item.lower() \
                                    for item in list(dic.transl)
                                   ]
            else:
                sh.log.append ('Objects.titles_low'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        return self._titles_low
    
    def abbrs_low(self):
        if self._abbrs_low is None:
            dic = self.abbr()
            if dic:
                self._abbrs_low = [item.lower() \
                                   for item in list(dic.orig)
                                  ]
            else:
                sh.log.append ('Objects.abbrs_low'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        return self._abbrs_low
    
    def prioritize(self):
        # Allow empty lists
        if self._prioritize is None:
            self._prioritize = sh.Input (func_title = 'Objects.prioritize'
                                        ,val        = self.lists().prioritize()
                                        ).list()
            abbrs = sh.Input (func_title = 'Objects.prioritize'
                             ,val        = self.abbrs_low()
                             ).list()
            titles = sh.Input (func_title = 'Objects.prioritize'
                              ,val        = self.titles_low()
                              ).list()
            
            tmp = []
            for i in range(len(self._prioritize)):
                # Fool-proof
                title = self._prioritize[i].strip()
                title = title.lower()
                if title in abbrs:
                    ind = abbrs.index(title)
                    tmp.append(title)
                    tmp.append(titles[ind])
                elif title in titles:
                    ind = titles.index(title)
                    tmp.append(title)
                    tmp.append(abbrs[ind])
                else:
                    tmp.append(title)
            self._prioritize = tmp
        return self._prioritize
    
    def blacklist(self):
        # Allow empty lists
        if self._blacklist is None:
            self._blacklist = sh.Input (func_title = 'Objects.blacklist'
                                       ,val        = self.lists().blacklist()
                                       ).list()
            abbrs = sh.Input (func_title = 'Objects.prioritize'
                             ,val        = self.abbrs_low()
                             ).list()
            titles = sh.Input (func_title = 'Objects.prioritize'
                              ,val        = self.titles_low()
                              ).list()
            
            tmp = []
            for i in range(len(self._blacklist)):
                # Fool-proof
                title = self._blacklist[i].strip()
                title = title.lower()
                if title in abbrs:
                    ind = abbrs.index(title)
                    tmp.append(title)
                    tmp.append(titles[ind])
                elif title in titles:
                    ind = titles.index(title)
                    tmp.append(title)
                    tmp.append(abbrs[ind])
                else:
                    tmp.append(title)
            self._blacklist = tmp
        return self._blacklist
    
    def online(self):
        #todo: create a sub-source
        if self.request()._source in (_('All'),_('Online')):
            return sh.objs.online_mt()
        else:
            return sh.objs.online_other()
    
    def request(self):
        if self._request is None:
            self._request = CurRequest()
        return self._request
    
    def lists(self):
        if self._lists is None:
           self._lists = Lists()
        return self._lists
    
    def abbr(self):
        if self._abbr is None:
            self._abbr = self.lists().abbr()
            if self._abbr:
                self._abbr.sort()
            else:
                sh.log.append ('Objects.abbr'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        return self._abbr



class Order:
    
    def __init__(self,lst=[]):
        self.reset(lst=lst)
        
    def reset(self,lst):
        self.lst = lst
        if self.lst:
            self.Success = True
        else:
            self.Success = False
    
    def prioritize(self):
        if self.Success:
            for item in self.lst:
                objs.prioritize().append(item)
        else:
            sh.log.append ('Order.prioritize'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
                          
    def unprioritize(self):
        if self.Success:
            for item in self.lst:
                if item in objs.prioritize():
                    objs._prioritize.remove(item)
        else:
            sh.log.append ('Order.unprioritize'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def block(self):
        if self.Success:
            for item in self.lst:
                objs.blacklist().append(item)
        else:
            sh.log.append ('Order.block'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def unblock(self):
        if self.Success:
            for item in self.lst:
                if item in objs.blacklist():
                    objs._blacklist.remove(item)
        else:
            sh.log.append ('Order.unblock'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )



objs = Objects()
