#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import io
import urllib.request
import html
import ssl
import skl_shared.shared as sh
import manager

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')


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
            mes = str(self._no2)
            sh.objs.mes(f,mes,True).debug()
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
                mes = _('Wrong input data!')
                sh.objs.mes(f,mes,True).warning()
            mes = str(self._no1)
            sh.objs.mes(f,mes,True).debug()
        return self._no1
        
    def dump(self):
        f = '[MClient] logic.PhraseTerma.dump'
        # Autoincrement starts with 1 in sqlite
        if self._no1 > 0 and self._no2 > 0:
            mes = _('Update DB, range {}-{}')
            mes = mes.format(self._no1,self._no2)
            sh.objs.mes(f,mes,True).info()
            self.dbc.execute ('update BLOCKS set TERMA=? where NO >= ? \
                               and NO < ?',('',self._no1,self._no2,)
                             )
        else:
            mes = _('Wrong input data!')
            sh.objs.mes(f,mes,True).warning()
        
    def run(self):
        f = '[MClient] logic.PhraseTerma.run'
        if self.Success:
            self.second_phrase()
            self.phrase_dic()
            self.dump()
        else:
            sh.com.cancel(f)



class Source:
    
    def __init__(self):
        self._title  = ''
        self._status = _('not running')
        self._color  = 'red'



class Welcome:

    def __init__ (self,product='MClient'
                 ,version='current'
                 ):
        self.values()
        self._product = product
        self._version = version
        self._desc    = sh.List (lst1 = [self._product
                                        ,self._version
                                        ]
                                ).space_items()

    def values(self):
        self._sources   = []
        self._sd_status = 0
        self._sd_color  = 'red'
        self._product   = ''
        self._version   = ''
        self._desc      = ''
    
    def sources(self):
        f = '[MClient] logic.Welcome.sources'
        old  = objs.plugins()._source
        dics = objs._plugins.online_sources()
        if dics:
            for dic in dics:
                objs._plugins.set(dic)
                source        = Source()
                source._title = dic
                if objs._plugins.accessible():
                    source._status = _('running')
                    source._color  = 'green'
                self._sources.append(source)
        else:
            sh.com.empty(f)
        objs._plugins.set(_('Offline'))
        self._sd_status = objs.plugins().accessible()
        if self._sd_status:
            self._sd_color = 'green'
        objs._plugins.set(old)

    def source_code(self,title,status,color):
        self.istr.write('      <b>{}</b>\n'.format(title))
        self.istr.write('      <font face="Serif" color="')
        self.istr.write(color)
        self.istr.write('" size="6">')
        self.istr.write(status)
        self.istr.write('</font>.\n')
        self.istr.write('      <br>\n')
    
    def gen_hint(self,hint):
        self.istr.write('<td align="left" valign="top" col width="200">')
        self.istr.write(hint)
        self.istr.write('</td>')
    
    def gen_hotkey(self,hotkey):
        self.istr.write('<td align="center" valign="top" col width="100">')
        self.istr.write(sh.Hotkeys(hotkey).run())
        self.istr.write('</td>')
    
    def gen_row(self,hint1,hotkey1,hint2,hotkey2):
        self.istr.write('<tr>')
        self.gen_hint(hint1)
        self.gen_hotkey(hotkey1)
        self.gen_hint(hint2)
        self.gen_hotkey(hotkey2)
        self.istr.write('</tr>')
    
    def hotkeys(self):
        self.istr.write('<font face="Serif" size="5">')
        self.istr.write('<table>')

        hint1    = _('Translate the current input or selection')
        hotkey1  = ('<Button-1>','<Return>')
        hint2    = _('Copy the current selection')
        hotkey2  = ('<Button-3>'
                   ,sh.lg.globs['var']['bind_copy_sel']
                   ,sh.lg.globs['var']['bind_copy_sel_alt']
                   )
        hint34   = _('Show the program window (system-wide)')
        hotkey34 = '<Alt_L-grave>'
        hint35   = _('Translate selection from an external program')
        hotkey35 = ('<Control_L-Insert-Insert>'
                   ,'<Control_L-c-c>'
                   )
        hint36   = _('Minimize the program window')
        hotkey36 = '<Escape>'
        hint37   = _('Quit the program')
        hotkey37 = ('<Control-q>'
                   ,sh.lg.globs['var']['bind_quit']
                   )
        hint3    = _('Copy the URL of the selected term')
        hotkey3  = sh.lg.globs['var']['bind_copy_url']
        hint4    = _('Copy the URL of the current article')
        hotkey4  = sh.lg.globs['var']['bind_copy_article_url']
        hint5    = _('Go to the previous section of column #%d') % 1
        hotkey5  = sh.lg.globs['var']['bind_col1_up']
        hint6    = _('Go to the next section of column #%d') % 1
        hotkey6  = sh.lg.globs['var']['bind_col1_down']
        hint7    = _('Go to the previous section of column #%d') % 2
        hotkey7  = sh.lg.globs['var']['bind_col2_up']
        hint8    = _('Go to the next section of column #%d') % 2
        hotkey8  = sh.lg.globs['var']['bind_col2_down']
        hint9    = _('Go to the previous section of column #%d') % 3
        hotkey9  = sh.lg.globs['var']['bind_col3_up']
        hint10   = _('Go to the next section of column #%d') % 3
        hotkey10 = sh.lg.globs['var']['bind_col3_down']
        hint11   = _('Open a webpage with a definition of the current term')
        hotkey11 = sh.lg.globs['var']['bind_define']
        hint12   = _('Look up phrases')
        hotkey12 = sh.lg.globs['var']['bind_go_phrases']
        hint13   = _('Go to the preceding article')
        hotkey13 = sh.lg.globs['var']['bind_go_back']
        hint14   = _('Go to the following article')
        hotkey14 = sh.lg.globs['var']['bind_go_forward']
        hint15   = _('Next source language')
        hotkey15 = (sh.lg.globs['var']['bind_next_lang1']
                   ,sh.lg.globs['var']['bind_next_lang1_alt']
                   )
        hint16   = _('Previous source language')
        hotkey16 = (sh.lg.globs['var']['bind_prev_lang1']
                   ,sh.lg.globs['var']['bind_prev_lang1_alt']
                   )
        hint17   = _('Create a printer-friendly page')
        hotkey17 = sh.lg.globs['var']['bind_print']
        hint18   = _('Open the current article in a default browser')
        hotkey18 = (sh.lg.globs['var']['bind_open_in_browser']
                   ,sh.lg.globs['var']['bind_open_in_browser_alt']
                   )
        hint19   = _('Reload the current article')
        hotkey19 = (sh.lg.globs['var']['bind_reload_article']
                   ,sh.lg.globs['var']['bind_reload_article_alt']
                   )
        hint20   = _('Save or copy the current article')
        hotkey20 = (sh.lg.globs['var']['bind_save_article']
                   ,sh.lg.globs['var']['bind_save_article_alt']
                   )
        hint21   = _('Start a new search in the current article')
        hotkey21 = sh.lg.globs['var']['bind_re_search_article']
        hint22   = _('Search the article forward')
        hotkey22 = sh.lg.globs['var']['bind_search_article_forward']
        hint23   = _('Search the article backward')
        hotkey23 = sh.lg.globs['var']['bind_search_article_backward']
        hint24   = _('Show settings')
        hotkey24 = (sh.lg.globs['var']['bind_settings']
                   ,sh.lg.globs['var']['bind_settings_alt']
                   )
        hint25   = _('About the program')
        hotkey25 = sh.lg.globs['var']['bind_show_about']
        hint26   = _('Paste a special symbol')
        hotkey26 = sh.lg.globs['var']['bind_spec_symbol']
        hint27   = _('Toggle alphabetizing')
        hotkey27 = sh.lg.globs['var']['bind_toggle_alphabet']
        hint28   = _('Toggle blacklisting')
        hotkey28 = sh.lg.globs['var']['bind_toggle_block']
        hint29   = _('Toggle History')
        hotkey29 = (sh.lg.globs['var']['bind_toggle_history']
                   ,sh.lg.globs['var']['bind_toggle_history_alt']
                   )
        hint30   = _('Toggle prioritizing')
        hotkey30 = sh.lg.globs['var']['bind_toggle_priority']
        '''
        hint31   = _('Toggle terms-only selection')
        hotkey31 = sh.lg.globs['var']['bind_toggle_sel']
        '''
        hint32   = _('Toggle the current article view')
        hotkey32 = (sh.lg.globs['var']['bind_toggle_view']
                   ,sh.lg.globs['var']['bind_toggle_view_alt']
                   )
        hint33   = _('Clear History')
        hotkey33 = sh.lg.globs['var']['bind_clear_history']
        hint38   = _('Next target language')
        hotkey38 = (sh.lg.globs['var']['bind_next_lang2']
                   ,sh.lg.globs['var']['bind_next_lang2_alt']
                   )
        hint39   = _('Previous target language')
        hotkey39 = (sh.lg.globs['var']['bind_prev_lang2']
                   ,sh.lg.globs['var']['bind_prev_lang2_alt']
                   )
        hint40   = _('Swap source and target languages')
        hotkey40 = sh.lg.globs['var']['bind_swap_langs']
        
        self.gen_row(hint1,hotkey1,hint2,hotkey2)
        self.gen_row(hint34,hotkey34,hint35,hotkey35)
        self.gen_row(hint36,hotkey36,hint37,hotkey37)
        self.gen_row(hint3,hotkey3,hint4,hotkey4)
        self.gen_row(hint5,hotkey5,hint6,hotkey6)
        self.gen_row(hint7,hotkey7,hint8,hotkey8)
        self.gen_row(hint9,hotkey9,hint10,hotkey10)
        self.gen_row(hint11,hotkey11,hint12,hotkey12)
        self.gen_row(hint13,hotkey13,hint14,hotkey14)
        self.gen_row(hint15,hotkey15,hint16,hotkey16)
        self.gen_row(hint38,hotkey38,hint39,hotkey39)
        self.gen_row(hint40,hotkey40,hint17,hotkey17)
        self.gen_row(hint18,hotkey18,hint19,hotkey19)
        self.gen_row(hint20,hotkey20,hint22,hotkey22)
        self.gen_row(hint23,hotkey23,hint21,hotkey21)
        self.gen_row(hint24,hotkey24,hint25,hotkey25)
        self.gen_row(hint26,hotkey26,hint27,hotkey27)
        self.gen_row(hint28,hotkey28,hint29,hotkey29)
        self.gen_row(hint30,hotkey30,hint32,hotkey32)
        self.gen_row(hint33,hotkey33,'','')
        
        self.istr.write('</font>')
        self.istr.write('</table>')
    
    def generate(self):
        f = '[MClient] logic.Welcome.generate'
        self.istr = io.StringIO()
        self.istr.write('<html>\n')
        self.istr.write('  <body>\n')
        self.istr.write('    <h1>')
        self.istr.write(_('Welcome to {}!').format(self._desc))
        self.istr.write('</h1>\n')
        self.istr.write('    <font face="Serif" size="6">\n')
        self.istr.write('      <br>\n')
        self.istr.write('      {}'.format(_('This program retrieves translation from online/offline sources.')))
        self.istr.write('\n')
        self.istr.write('      <br>\n')
        self.istr.write('      {}'.format(_('Use an entry area below to enter a word/phrase to be translated.')))
        self.istr.write('\n')
        self.istr.write('\n')
        self.istr.write('      <br><br>\n')
        for source in self._sources:
            self.source_code (title  = source._title
                             ,status = source._status
                             ,color  = source._color
                             )
        self.istr.write('      {}'.format(_('Offline dictionaries loaded:')))
        self.istr.write('\n')
        self.istr.write('      <font color="')
        self.istr.write(self._sd_color)
        self.istr.write('">')
        self.istr.write('{}'.format(self._sd_status))
        self.istr.write('</font>.\n')
        self.istr.write('    </font>\n')
        self.istr.write('<br><br><br><br>')
        self.istr.write('<h1>')
        self.istr.write(_('Main hotkeys'))
        self.istr.write('</h1>')
        self.istr.write('<h2>')
        self.istr.write(_('(see documentation for other hotkeys, mouse bindings and functions)'))
        self.istr.write('</h2>')
        self.hotkeys()
        self.istr.write('  </body>\n')
        self.istr.write('</html>')
        code = self.istr.getvalue()
        self.istr.close()
        return code

    def run(self):
        self.sources()
        return self.generate()



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
                self._fabbr = sh.objs.pdir().add ('..','resources'
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
        self.sections         = [sh.lg.SectionBooleans
                                ,sh.lg.SectionIntegers
                                ,sh.lg.SectionVariables
                                ]
        self.sections_abbr    = [sh.lg.SectionBooleans_abbr
                                ,sh.lg.SectionIntegers_abbr
                                ,sh.lg.SectionVariables_abbr
                                ]
        self.sections_func    = [sh.lg.config_parser.getboolean
                                ,sh.lg.config_parser.getint
                                ,sh.lg.config_parser.get
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
        self._default()
        if os.path.exists(self.path):
            self.open()
        else:
            self.Success = False
        self.check()
        self.load()

    # Do not rename, this procedure is called by 'shared'
    def _default(self):
        self._default_bool()
        self._default_int()
        self._default_var()
        
    def _default_bool(self):
        sh.lg.globs['bool'].update ({
            'AutoCloseSpecSymbol':False
           ,'Autocompletion'     :True
           ,'SelectTermsOnly'    :True
           ,'Iconify'            :True
                                   })
    
    def _default_int(self):
        sh.lg.globs['int'].update ({
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
        sh.lg.globs['var'].update ({
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
           ,'bind_next_lang1'             :'<F8>'
           ,'bind_next_lang1_alt'         :'<Control-k>'
           ,'bind_next_lang2'             :'<F9>'
           ,'bind_next_lang2_alt'         :'<Control-l>'
           ,'bind_prev_lang1'             :'<Shift-F8>'
           ,'bind_prev_lang1_alt'         :'<Control-K>'
           ,'bind_prev_lang2'             :'<Shift-F9>'
           ,'bind_prev_lang2_alt'         :'<Control-L>'
           ,'bind_open_in_browser_alt'    :'<Control-b>'
           ,'bind_open_in_browser'        :'<F7>'
           ,'bind_paste_search_field'     :'<ButtonRelease-2>'
           ,'bind_print'                  :'<Control-p>'
           ,'bind_quit'                   :'<F10>'
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
           ,'bind_swap_langs'             :'<Control-space>'
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
           ,'repeat_sign'                 :'!'
           ,'repeat_sign2'                :'!!'
           ,'spec_syms'                   :'àáâäāæßćĉçèéêēёëəғĝģĥìíîïīĵķļñņòóôõöōœøšùúûūŭũüýÿžжҗқңөүұÀÁÂÄĀÆSSĆĈÇÈÉÊĒЁËƏҒĜĢĤÌÍÎÏĪĴĶĻÑŅÒÓÔÕÖŌŒØŠÙÚÛŪŬŨÜÝŸŽЖҖҚҢӨҮҰ'
           ,'web_search_url'              :'http://www.google.ru/search?ie=UTF-8&oe=UTF-8&sourceid=navclient=1&q=%s'
                                  })

    def reset(self):
        sh.lg.globs['bool']  = {}
        sh.lg.globs['float'] = {}
        sh.lg.globs['int']   = {}
        sh.lg.globs['var']   = {}



class CurRequest:

    def __init__(self):
        self.values()
        self.reset()
    
    def values(self):
        ''' #note: this should be synchronized with the 'default' value
            of objs.webframe().menu_columns
        '''
        self._collimit = 8
        # Default priorities of parts of speech
        self._pr_n    = 7
        self._pr_v    = 6
        self._pr_adj  = 5
        self._pr_abbr = 4
        self._pr_adv  = 3
        self._pr_prep = 2
        self._pr_pron = 1
        self._source  = objs.plugins()._source
        self._cols    = ('dic','wform','transc','speech')
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
        self.SpecialPage = False
    
    def reset(self):
        self._page     = ''
        self._html     = ''
        self._html_raw = ''
        self._search   = ''
        self._url      = ''



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
                     = self._plugins = None
    
    def plugins (self,Debug=False,Shorten=True
                ,MaxRow=20,MaxRows=100
                ):
        if self._plugins is None:
            self._plugins = manager.Plugins (sdpath  = self.default().dics()
                                            ,timeout = sh.lg.globs['int']['timeout']
                                            ,iabbr   = self.order().dic
                                            ,Debug   = Debug
                                            ,Shorten = Shorten
                                            ,MaxRow  = MaxRow
                                            ,MaxRows = MaxRows
                                            )
        return self._plugins
    
    def default(self,product='mclient'):
        if not self._default:
            self._default = DefaultConfig(product=product)
            self._default.run()
        return self._default
    
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
                        message = _('Mode: "{}"')
                        message = message.format(_('Decrease priority'))
                    else:
                        message = _('Mode: "{}"')
                        message = message.format(_('Increase priority'))
                    sh.objs.mes(f,message,True).debug()
                    
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
                        mes = _('Swap items: {} <-> {}; "{}" <-> "{}"')
                        mes = mes.format (ind1,ind2
                                         ,self._prioritize[ind1]
                                         ,self._prioritize[ind2]
                                         )
                        sh.objs.mes(f,mes,True).debug()
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
                    
                    mes = 'Dic1: {}'.format(self._dic1)
                    sh.objs.mes(f,mes,True).debug()
                    mes = 'Dic2: {}'.format(self._dic2)
                    sh.objs.mes(f,mes,True).debug()
                    mes = str(self._prioritize)
                    sh.objs.mes(f,mes,True).debug()
                else:
                    mes = _('Logic error!')
                    sh.objs.mes(f,mes).error()
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
            self.lists = Lists()
            self._blacklist = sh.Input (title = f
                                       ,value = self.lists.blacklist()
                                       ).list()
            self._prioritize = sh.Input (title = f
                                        ,value = self.lists.prioritize()
                                        ).list()
            self.Success = self.lists.Success
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
                mes = _('Wrong input data!')
                sh.objs.mes(f,mes,True).warning()
        else:
            sh.com.cancel(f)
        
    def abbr(self,title):
        f = '[MClient] logic.Order.abbr'
        if self.Success:
            try:
                ind = self._titles.index(title)
                return self._abbrs[ind]
            except ValueError:
                mes = _('Wrong input data!')
                sh.objs.mes(f,mes,True).warning()
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
                    mes = _('Unknown dictionary "{}"!').format(item)
                    sh.objs.mes(f,mes,True).warning()
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



class Commands:
    
    def __init__(self):
        self.unverified()
    
    def dump_elems(self,blocks,articleid):
        f = '[MClient] logic.Commands.dump_elems'
        if blocks and articleid:
            data = []
            for block in blocks:
                data.append (
                  (None                # (00) Skips the autoincrement
                  ,articleid           # (01) ARTICLEID
                  ,block._dica         # (02) DICA (abbreviation)
                  ,block._wforma       # (03) WFORMA
                  ,block._speecha      # (04) SPEECHA
                  ,block._transca      # (05) TRANSCA
                  ,block._terma        # (06) TERMA
                  ,block._type         # (07) TYPE
                  ,block._text         # (08) TEXT
                  ,block._url          # (09) URL
                  ,block._block        # (10) BLOCK
                  ,block._priority     # (11) PRIORITY
                  ,block._select       # (12) SELECTABLE
                  ,block._same         # (13) SAMECELL
                  ,block._cell_no      # (14) CELLNO
                  ,-1                  # (15) ROWNO
                  ,-1                  # (16) COLNO
                  ,-1                  # (17) POS1
                  ,-1                  # (18) POS2
                  ,''                  # (19) NODE1
                  ,''                  # (20) NODE2
                  ,-1                  # (21) OFFPOS1
                  ,-1                  # (22) OFFPOS2
                  ,-1                  # (23) BBOX1
                  ,-1                  # (24) BBOX2
                  ,-1                  # (25) BBOY1
                  ,-1                  # (26) BBOY2
                  ,block._text.lower() # (27) TEXTLOW
                  ,0                   # (28) IGNORE
                  ,0                   # (29) SPEECHPR
                  ,block._dicaf        # (30) DICA (full title)
                  )
                            )
            return data
        else:
            sh.com.empty(f)
    
    def suggest(self,search,limit=0):
        f = '[MClient] logic.Commands.suggest'
        items = objs.plugins().suggest(search)
        if items:
            if limit:
                items = items[0:limit]
        else:
            items = []
            sh.com.empty(f)
        return items
        
    def unverified(self):
        f = '[MClient] logic.Commands.unverified'
        ''' On *some* systems we can get urllib.error.URLError: 
            <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED].
            To get rid of this error, we use this small workaround.
        '''
        if hasattr(ssl,'_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context
        else:
            mes = _('Unable to use unverified certificates!')
            sh.objs.mes(f,mes,True).warning()



objs = Objects()
com  = Commands()
ConfigMclient()
