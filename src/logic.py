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
            instance = sh.File (file = os.path.join (self.dir.dir
                                                    ,'abbr.txt'
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
        self._online = self._request = self._order = None
        
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
        
    def order(self):
        if self._order is None:
            self._order = Order()
        return self._order



# Create block and priority lists and complement them
class Order:
    
    # Takes ~0,046s
    def __init__(self):
        self.values()
        self._lists()
        self._dic()
        self._conform()
            
    def priority(self,search):
        if self.Success:
            if search:
                lst   = search.split(',')
                lst   = [item.lower().strip() for item in lst]
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
                sh.log.append ('Order.priority'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Order.priority'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    ''' A LM click on:
        1) A blocked dictionary     - unblock
        2) A common dictionary      - prioritize
        3) A prioritized dictionary - increase priority
    '''
    def lm_auto(self,search):
        if self.Success:
            if self.is_blocked(search=search):
                self.unblock_mult(search=search)
            else:
                self.prioritize_mult(search=search)
        else:
            sh.log.append ('Order.lm_auto'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    ''' A RM click on:
        1) A prioritized dictionary - decrease priority or unprioritize
                                      (at minimal priority)
        2) A blocked dictionary     - unblock
        3) A common dictionary      - block
    '''
    def rm_auto(self,search):
        if self.Success:
            if self.is_blocked(search=search):
                self.unblock_mult(search=search)
            elif self.is_prioritized(search=search):
                self.unprioritize_mult(search=search)
            else:
                self.block_mult(search=search)
        else:
            sh.log.append ('Order.rm_auto'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def is_prioritized(self,search):
        if self.Success:
            if search:
                lst = search.split(',')
                lst = [item.lower().strip() for item in lst]
                for item in lst:
                    if item in self._prioritize:
                        return True
            else:
                sh.log.append ('Order.is_prioritized'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Order.is_prioritized'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def is_blocked(self,search):
        if self.Success:
            if search:
                lst = search.split(',')
                lst = [item.lower().strip() for item in lst]
                for item in lst:
                    if item in self._blacklist:
                        return True
            else:
                sh.log.append ('Order.is_blocked'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Order.is_blocked'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    ''' Create new block and priority lists based on those that were
        read from user files. Lists from user files may comprise either
        dictionary abbreviations or full dictionary titles. New lists
        will be lowercased and stripped and will comprise both
        abbreviations and full titles.
    '''
    def _conform(self):
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
                    self.block(search=item)
            else:
                sh.log.append ('Order._conform'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
            if self._prioritize:
                prioritize = list(self._prioritize)
                self._prioritize = []
                for item in prioritize:
                    self.prioritize(search=item)
            else:
                sh.log.append ('Order._conform'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Order._conform'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def _lists(self):
        if self.Success:
            self.lists       = Lists()
            self._blacklist  = sh.Input (func_title = 'Order._lists'
                                        ,val        = self.lists.blacklist()
                                        ).list()
            self._prioritize = sh.Input (func_title = 'Order._lists'
                                        ,val        = self.lists.prioritize()
                                        ).list()
            self.Success     = self.lists.Success
        else:
            sh.log.append ('Order._lists'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
        
    def _dic(self):
        if self.Success:
            self.dic     = self.lists.abbr()
            self.Success = self.dic.Success
        else:
            sh.log.append ('Order._dic'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def values(self):
        self.Success     = True
        self.lists       = None
        self.dic         = None
        self._abbrs      = []
        self._titles     = []
        self._blacklist  = []
        self._prioritize = []
        self._abbr       = ''
        self._title      = ''
            
    def title(self):
        if self.Success:
            if not self._title:
                if self._abbr in self._abbrs:
                    ind = self._abbrs.index(self._abbr)
                    self._title = self._titles[ind]
                else:
                    sh.log.append ('Order.title'
                                  ,_('WARNING')
                                  ,_('Wrong input data!')
                                  )
            return self._title
        else:
            sh.log.append ('Order.title'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
        
    def abbr(self):
        if self.Success:
            if not self._abbr:
                if self._title in self._titles:
                    ind = self._titles.index(self._title)
                    self._abbr = self._abbrs[ind]
                else:
                    sh.log.append ('Order.abbr'
                                  ,_('WARNING')
                                  ,_('Wrong input data!')
                                  )
            return self._abbr
        else:
            sh.log.append ('Order.abbr'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def search(self,text):
        if self.Success:
            self._abbr  = ''
            self._title = ''
            text = str(text).lower().strip()
            if text:
                if text in self._abbrs:
                    self._abbr = text
                    self.title()
                elif text in self._titles:
                    self._title = text
                    self.abbr()
                else:
                    sh.log.append ('Order.search'
                                  ,_('WARNING')
                                  ,_('Unknown dictionary "%s"!') % text
                                  )
                    self._abbr = self._title = text
            else:
                sh.log.append ('Order.search'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Order.search'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def block_mult(self,search):
        if self.Success:
            if search:
                lst = search.split(',')
                for item in lst:
                    self.block(search=item)
            else:
                sh.log.append ('Order.block_mult'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Order.block_mult'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def block(self,search):
        if self.Success:
            self.search(text=search)
            if self._abbr and self._title:
                if self._abbr in self._blacklist \
                and self._title in self._blacklist:
                    sh.log.append ('Order.block'
                                  ,_('INFO')
                                  ,_('Nothing to do!')
                                  )
                else:
                    self._blacklist.append(self._abbr)
                    self._blacklist.append(self._title)
            else:
                sh.log.append ('Order.block'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Order.block'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
                          
    def unblock(self,search):
        if self.Success:
            self.search(text=search)
            if self._abbr and self._title:
                if self._abbr in self._blacklist \
                and self._title in self._blacklist:
                    self._blacklist.remove(self._abbr)
                    self._blacklist.remove(self._title)
                else:
                    sh.log.append ('Order.unblock'
                                  ,_('INFO')
                                  ,_('Nothing to do!')
                                  )
            else:
                sh.log.append ('Order.unblock'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Order.unblock'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
                          
    def prioritize(self,search):
        if self.Success:
            self.search(text=search)
            if self._abbr and self._title:
                if self._abbr in self._prioritize \
                and self._title in self._prioritize:
                    ind1 = self._prioritize.index(self._abbr)
                    ind2 = self._prioritize.index(self._title)
                    max_ind = max(ind1,ind2)
                    min_ind = min(ind1,ind2)
                    del self._prioritize[max_ind]
                    del self._prioritize[min_ind]
                    ''' We assume that 1 record occupies 2 lines
                        (abbreviation + title), thus, we move the record
                        2 lines up.
                    '''
                    if min_ind > 1:
                        min_ind -= 2
                    self._prioritize.insert(min_ind,self._title)
                    self._prioritize.insert(min_ind,self._abbr)
                else:
                    self._prioritize.append(self._abbr)
                    self._prioritize.append(self._title)
            else:
                sh.log.append ('Order.prioritize'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Order.prioritize'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def prioritize_mult(self,search):
        if self.Success:
            if search:
                lst = search.split(',')
                for item in lst:
                    self.prioritize(search=item)
            else:
                sh.log.append ('Order.prioritize_mult'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Order.prioritize_mult'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
                          
    def unprioritize_mult(self,search):
        if self.Success:
            if search:
                lst = search.split(',')
                ''' We need to prioritize multiple items in a direct
                    order, from a higher priority to a lower priority
                    (which is intuitive), but unprioritize them in
                    a reverse order (otherwise, unprioritizing will have
                    no effect: 'x1, x2' -> 'x2, x1' -> 'x1, x2').
                '''
                lst = lst[::-1]
                for item in lst:
                    self.unprioritize(search=item)
            else:
                sh.log.append ('Order.unprioritize_mult'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Order.unprioritize_mult'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
                          
    def unblock_mult(self,search):
        if self.Success:
            if search:
                lst = search.split(',')
                for item in lst:
                    self.unblock(search=item)
            else:
                sh.log.append ('Order.unblock_mult'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Order.unblock_mult'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def unprioritize(self,search):
        if self.Success:
            self.search(text=search)
            if self._abbr and self._title:
                if self._abbr in self._prioritize \
                and self._title in self._prioritize:
                    ind1 = self._prioritize.index(self._abbr)
                    ind2 = self._prioritize.index(self._title)
                    max_ind = max(ind1,ind2)
                    min_ind = min(ind1,ind2)
                    del self._prioritize[max_ind]
                    del self._prioritize[min_ind]
                    if min_ind == len(self._prioritize):
                        ''' Higher index means lower priority.
                            If a dictionary title + abbreviation pair
                            reaches the end, we just delete it from
                            the list (the prioritized dictionary becomes
                            a common one).
                        '''
                        pass
                    else:
                        min_ind += 2
                        self._prioritize.insert(min_ind,self._title)
                        self._prioritize.insert(min_ind,self._abbr)
                else:
                    sh.log.append ('Order.unprioritize'
                                  ,_('INFO')
                                  ,_('Nothing to do!')
                                  )
            else:
                sh.log.append ('Order.unprioritize'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Order.unprioritize'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    



objs = Objects()


if __name__ == '__main__':
    print('Old Priorities:',objs.order()._prioritize)
    #objs._order.prioritize(search='пив.')
    #objs._order.prioritize(search='тех.')
    objs._order.prioritize_mult(search='Британский английский, Пивное производство')
    print('New Priorities:',objs.order()._prioritize)
    objs._order.unprioritize_mult(search='Британский английский, Пивное производство')
    print('New Priorities:',objs.order()._prioritize)
