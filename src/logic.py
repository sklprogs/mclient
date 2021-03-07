#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import io
import urllib.request
import html
import ssl
import skl_shared.shared as sh
from skl_shared.localize import _
import manager


SPORDER = (_('Noun'),_('Verb'),_('Adjective'),_('Abbreviation')
          ,_('Adverb'),_('Preposition'),_('Pronoun')
          )

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

class DefaultKeys(sh.DefaultKeys):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.load()
    
    def load(self):
        self._load_bool()
        self._load_int()
        self._load_str()
        
    def _load_bool(self):
        sh.lg.globs['bool'].update ({
            'AlphabetizeTerms'   :True
           ,'AutoCloseSpecSymbol':False
           ,'Autocompletion'     :True
           ,'Autoswap'           :False
           ,'BlockDics'          :True
           ,'CaptureHotkey'      :True
           ,'Iconify'            :True
           ,'PrioritizeDics'     :True
           ,'SelectTermsOnly'    :True
           ,'ShortDicTitles'     :False
           ,'ShortSpeech'        :False
           ,'ShowUserNames'      :True
           ,'SortByColumns'      :True
           ,'VerticalView'       :False
                                   })
    
    def _load_int(self):
        sh.lg.globs['int'].update ({
            'colnum'            :4
           ,'col_width'         :250
           ,'font_col1_size'    :4
           ,'font_col2_size'    :4
           ,'font_col3_size'    :3
           ,'font_col4_size'    :3
           ,'font_comments_size':3
           ,'font_terms_size'   :4
           ,'timeout'           :5
                                  })
    
    def _load_str(self):
        sh.lg.globs['str'].update ({
            'bind_clear_history'          :'<Control-Shift-Delete>'
           ,'bind_clear_search_field'     :'<ButtonRelease-3>'
           ,'bind_col1_down'              :'<Control-Down>'
           ,'bind_col1_up'                :'<Control-Up>'
           ,'bind_col2_down'              :'<Alt-Down>'
           ,'bind_col2_up'                :'<Alt-Up>'
           ,'bind_col3_down'              :'<Shift-Down>'
           ,'bind_col3_up'                :'<Shift-Up>'
           ,'bind_copy_article_url'       :'<Control-F7>'
           ,'bind_copy_nominative'        :'<Control-w>'
           ,'bind_copy_sel'               :'<Control-Return>'
           ,'bind_copy_sel_alt'           :'<Control-KP_Enter>'
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
           ,'bind_open_in_browser'        :'<F7>'
           ,'bind_open_in_browser_alt'    :'<Control-b>'
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
           ,'bind_toggle_history'         :'<F4>'
           ,'bind_toggle_history_alt'     :'<Control-h>'
           ,'bind_toggle_priority'        :'<Alt-p>'
           ,'bind_toggle_sel'             :'<Control-t>'
           ,'bind_toggle_view'            :'<F6>'
           ,'bind_toggle_view_alt'        :'<Alt-v>'
           ,'col1_type'                   :_('Dictionaries')
           ,'col2_type'                   :_('Word forms')
           ,'col3_type'                   :_('Parts of speech')
           ,'col4_type'                   :_('Transcription')
           ,'color_col1'                  :'coral'
           ,'color_col2'                  :'cadet blue'
           ,'color_col3'                  :'slate gray'
           ,'color_col4'                  :'slate gray'
           ,'color_comments'              :'gray'
           ,'color_terms'                 :'black'
           ,'color_terms_sel_bg'          :'cyan'
           ,'color_terms_sel_fg'          :'black'
           ,'font_col1_family'            :'Arial'
           ,'font_col2_family'            :'Arial'
           ,'font_col3_family'            :'Mono'
           ,'font_col4_family'            :'Mono'
           ,'font_comments_family'        :'Mono'
           ,'font_history'                :'Sans 12'
           ,'font_style'                  :'Sans 14'
           ,'font_terms_family'           :'Serif'
           ,'font_terms_sel'              :'Sans 14 bold italic'
           ,'lang1'                       :_('Russian')
           ,'lang2'                       :_('English')
           ,'repeat_sign'                 :'!'
           ,'repeat_sign2'                :'!!'
           ,'source'                      :_('Multitran')
           ,'spec_syms'                   :'àáâäāæßćĉçèéêēёëəғĝģĥìíîïīĵķļñņòóôõöōœøšùúûūŭũüýÿžжҗқңөүұÀÁÂÄĀÆSSĆĈÇÈÉÊĒЁËƏҒĜĢĤÌÍÎÏĪĴĶĻÑŅÒÓÔÕÖŌŒØŠÙÚÛŪŬŨÜÝŸŽЖҖҚҢӨҮҰ'
           ,'speech1'                     :_('Noun')
           ,'speech2'                     :_('Verb')
           ,'speech3'                     :_('Adjective')
           ,'speech4'                     :_('Abbreviation')
           ,'speech5'                     :_('Adverb')
           ,'speech6'                     :_('Preposition')
           ,'speech7'                     :_('Pronoun')
           ,'style'                       :'MClient'
           ,'web_search_url'              :'http://www.google.ru/search?ie=UTF-8&oe=UTF-8&sourceid=navclient=1&q=%s'
                                  })



class CreateConfig(sh.CreateConfig):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    
    def fill_bool(self):
        section = _('Booleans')
        comment = _('The following values are allowed in this section: 0 (False) or 1 (True)')
        self.add_section(section,comment)
        section_abbr = self.sections[-1].abbr
        
        key = 'AlphabetizeTerms'
        comment = _('[Autosave] Sort terms by alphabet')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'AutoCloseSpecSymbol'
        comment = _('Hide the window with special characters after the 1st symbol is inserted')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'Autocompletion'
        comment = _('[Autosave] Show suggestions on input')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'Autoswap'
        comment = _('[Autosave] Autoswap Russian and the other language if appropriate')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'BlockDics'
        comment = _('[Autosave] Block dictionaries from the blacklist')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'CaptureHotkey'
        comment = _('[Autosave] Capture Ctrl-c-c and Ctrl-Ins-Ins system-wide')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'Iconify'
        comment = _('[Autosave] Minimize the application window after specific actions, e.g., copying')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'PrioritizeDics'
        comment = _('[Autosave] Prioritize dictionaries from the prioritization file')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'SelectTermsOnly'
        comment = _('[Autosave] Select blocks of all types (False) or terms only (True)')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'ShortDicTitles'
        comment = _('[Autosave] Shorten dictionary titles')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'ShortSpeech'
        comment = _('[Autosave] Shorten parts of speech')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'ShowUserNames'
        comment = _('[Autosave] Show user names')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'SortByColumns'
        comment = _('[Autosave] Sort by each column')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'VerticalView'
        comment = _('[Autosave] Vertical view')
        self.add_key(section,section_abbr,key,comment)
    
    def fill_int(self):
        section = _('Integers')
        self.add_section(section)
        section_abbr = self.sections[-1].abbr
        
        key = 'colnum'
        comment = _('[Autosave] Number of non-fixed columns')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'col_width'
        comment = _('A column width. Set to 0 to pick the value automatically.')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'font_comments_size'
        comment = _('A font size of comments')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'font_col1_size'
        comment = _('A font size of column #{}')
        comment = comment.format(1)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'font_col2_size'
        comment = _('A font size of column #{}')
        comment = comment.format(2)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'font_col3_size'
        comment = _('A font size of column #{}')
        comment = comment.format(3)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'font_col4_size'
        comment = _('A font size of column #{}')
        comment = comment.format(4)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'font_terms_size'
        comment = _('A font size of terms')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'timeout'
        comment = _('A connection timeout (in seconds)')
        self.add_key(section,section_abbr,key,comment)
    
    def fill_str(self):
        section = _('Strings')
        comment = _('Attention: some hotkeys, e.g., <Button-1> and <Double-Button-1> may conflict with each other. Reassign them with caution.')
        self.add_section(section,comment)
        section_abbr = self.sections[-1].abbr
        
        key = 'bind_clear_history'
        comment = _('Clear History')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_clear_search_field'
        comment = _('Clear the search field')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_col1_down'
        comment = _('Go to the next section of column #{}').format(1)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_col1_up'
        comment = _('Go to the previous section of column #{}')
        comment = comment.format(1)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_col2_down'
        comment = _('Go to the next section of column #{}').format(2)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_col2_up'
        comment = _('Go to the previous section of column #{}')
        comment = comment.format(2)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_col3_down'
        comment = _('Go to the next section of column #{}').format(3)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_col3_up'
        comment = _('Go to the previous section of column #{}')
        comment = comment.format(3)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_copy_article_url'
        comment = _('Copy URL of the current article')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_copy_nominative'
        comment = _('Copy an original word/phrase in a nominative case')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_copy_sel'
        comment = _('Copy a current selection from the article (combination #{})')
        comment = comment.format(1)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_copy_sel_alt'
        comment = _('Copy a current selection from the article (combination #{})')
        comment = comment.format(2)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_copy_url'
        comment = _('Copy URL of the current term')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_define'
        comment = _('Open a web-page defining the current term')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_go_back'
        comment = _('Go to the previous article')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_go_forward'
        comment = _('Go to the next article')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_go_phrases'
        comment = _('Go to the phrases section')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_next_lang1'
        comment = _('Set next language {} (combination {})')
        comment = comment.format(1,1)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_next_lang1_alt'
        comment = _('Set next language {} (combination {})')
        comment = comment.format(1,2)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_next_lang2'
        comment = _('Set next language {} (combination {})')
        comment = comment.format(2,1)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_next_lang2_alt'
        comment = _('Set next language {} (combination {})')
        comment = comment.format(2,2)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_paste_search_field'
        comment = _('Paste clipboard contents into the search field (system combination: Ctrl-V)')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_prev_lang1'
        comment = _('Set previous language #{} (combination #{})')
        comment = comment.format(1,1)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_prev_lang1_alt'
        comment = _('Set previous language #{} (combination #{})')
        comment = comment.format(1,2)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_prev_lang2'
        comment = _('Set previous language #{} (combination #{})')
        comment = comment.format(2,1)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_prev_lang2_alt'
        comment = _('Set previous language #{} (combination #{})')
        comment = comment.format(2,2)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_print'
        comment = _('Create a printer-friendly page')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_quit'
        comment = _('Quit the program')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_open_in_browser'
        comment = _('Open the current article in a browser (combination #{})')
        comment = comment.format(1)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_open_in_browser_alt'
        comment = _('Open the current article in a browser (combination #{})')
        comment = comment.format(2)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_reload_article'
        comment = _('Reload the current article (combination #{})')
        comment = comment.format(1)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_reload_article_alt'
        comment = _('Reload the current article (combination #{})')
        comment = comment.format(2)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_re_search_article'
        comment = _('Start a new term search in the current article')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_save_article'
        comment = _('Save or copy the current article (combination #{})')
        comment = comment.format(1)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_save_article_alt'
        comment = _('Save or copy the current article (combination #{})')
        comment = comment.format(2)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_search_article_backward'
        comment = _('Search the article backward')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_search_article_forward'
        comment = _('Search the article forward')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_settings'
        comment = _('Show settings (combination #{})')
        comment = comment.format(1)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_settings_alt'
        comment = _('Show settings (combination #{})')
        comment = comment.format(2)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_show_about'
        comment = _('About the program')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_spec_symbol'
        comment = _('Paste a special symbol')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_swap_langs'
        comment = _('Swap source and target languages')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_toggle_alphabet'
        comment = _('Toggle alphabetizing')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_toggle_block'
        comment = _('Toggle blacklisting')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_toggle_history'
        comment = _('Toggle History (combination #{})')
        comment = comment.format(1)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_toggle_history_alt'
        comment = _('Toggle History (combination #{})')
        comment = comment.format(2)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_toggle_priority'
        comment = _('Toggle prioritizing')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_toggle_sel'
        comment = _('Toggle selecting terms only')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_toggle_view'
        comment = _('Toggle the current article view (combination #{})')
        comment = comment.format(1)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'bind_toggle_view_alt'
        comment = _('Toggle the current article view (combination #{})')
        comment = comment.format(2)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'col1_type'
        comment = _('[Autosave] Type of column #{} in settings')
        comment = comment.format(1)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'col2_type'
        comment = _('[Autosave] Type of column #{} in settings')
        comment = comment.format(2)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'col3_type'
        comment = _('[Autosave] Type of column #{} in settings')
        comment = comment.format(3)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'col4_type'
        comment = _('[Autosave] Type of column #{} in settings')
        comment = comment.format(4)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'color_comments'
        comment = _('A font color for comments and user names')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'color_col1'
        comment = _('A font color for column #{}')
        comment = comment.format(1)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'color_col2'
        comment = _('A font color for column #{}')
        comment = comment.format(2)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'color_col3'
        comment = _('A font color for column #{}')
        comment = comment.format(3)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'color_col4'
        comment = _('A font color for column #{}')
        comment = comment.format(4)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'color_terms'
        comment = _('A font color for terms')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'color_terms_sel_bg'
        comment = _('A font background color for the current (selected) term')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'color_terms_sel_fg'
        comment = _('A font foreground color for the current (selected) term')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'font_comments_family'
        comment = _('A font of comments and user names')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'font_col1_family'
        comment = _('A font of column #{}')
        comment = comment.format(1)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'font_col2_family'
        comment = _('A font of column #{}')
        comment = comment.format(2)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'font_col3_family'
        comment = _('A font of column #{}')
        comment = comment.format(3)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'font_col4_family'
        comment = _('A font of column #{}')
        comment = comment.format(4)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'font_history'
        comment = _('A font color for History')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'font_style'
        comment = _('A program GUI font')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'font_terms_family'
        comment = _('A font of terms')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'font_terms_sel'
        comment = _('A font of the current (selected) term')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'lang1'
        comment = _('[Autosave] Source language')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'lang2'
        comment = _('[Autosave] Target language')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'repeat_sign'
        comment = _('Insert the last search request into the search field')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'repeat_sign2'
        comment = _('Insert the next-to-last search request into the search field')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'source'
        comment = _('[Autosave] The main dictionary source to use')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'spec_syms'
        comment = _('Characters that can be inserted into the search field')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'speech1'
        comment = _('[Autosave] A part of speech of column #{} in settings')
        comment = comment.format(1)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'speech2'
        comment = _('[Autosave] A part of speech of column #{} in settings')
        comment = comment.format(2)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'speech3'
        comment = _('[Autosave] A part of speech of column #{} in settings')
        comment = comment.format(3)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'speech4'
        comment = _('[Autosave] A part of speech of column #{} in settings')
        comment = comment.format(4)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'speech5'
        comment = _('[Autosave] A part of speech of column #{} in settings')
        comment = comment.format(5)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'speech6'
        comment = _('[Autosave] A part of speech of column #{} in settings')
        comment = comment.format(6)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'speech7'
        comment = _('[Autosave] A part of speech of column #{} in settings')
        comment = comment.format(7)
        self.add_key(section,section_abbr,key,comment)
        
        key = 'style'
        comment = _('[Autosave] A sorting style')
        self.add_key(section,section_abbr,key,comment)
        
        key = 'web_search_url'
        comment = _('URL for online search')
        self.add_key(section,section_abbr,key,comment)



class SpeechPrior:
    
    def __init__(self,order=SPORDER):
        self.reset(order)
    
    def reset(self,order=SPORDER):
        self.set_values()
        self.order = order
        self.check()
        self.prioritize()
    
    def get_abbr2full(self):
        f = '[MClient] logic.SpeechPrior.get_abbr2full'
        if self.Success:
            if not self.abbr2full:
                for i in range(len(self.abbr)):
                    self.abbr2full[self.abbr[i]] = self.full[i]
        else:
            sh.com.cancel(f)
        return self.abbr2full
    
    def get_full2abbr(self):
        f = '[MClient] logic.SpeechPrior.get_full2abbr'
        if self.Success:
            if not self.full2abbr:
                for i in range(len(self.full)):
                    self.full2abbr[self.full[i]] = self.abbr[i]
        else:
            sh.com.cancel(f)
        return self.full2abbr
    
    def get_all2prior(self):
        f = '[MClient] logic.SpeechPrior.get_all2prior'
        seq = {}
        if self.Success:
            for i in range(len(self.prior)):
                seq[self.abbr[i]] = self.prior[i]
                seq[self.full[i]] = self.prior[i]
        else:
            sh.com.cancel(f)
        return seq
    
    def debug(self):
        self.debug_all2prior()
        self.debug_pairs()
    
    def debug_all2prior(self):
        f = '[MClient] logic.SpeechPrior.debug_all2prior'
        if self.Success:
            all2prior = self.get_all2prior()
            if all2prior:
                all_ = all2prior.keys()
                prior = [all2prior.get(key) for key in all2prior.keys()]
                headers = (_('NAME'),_('PRIORITY'))
                iterable = [all_,prior]
                mes = sh.FastTable(iterable,headers).run()
                sh.com.run_fast_debug(f,mes)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def _debug_full2abbr(self):
        f = '[MClient] logic.SpeechPrior._debug_full2abbr'
        full2abbr = self.get_full2abbr()
        if full2abbr:
            full = sorted(full2abbr.keys())
            abbr = [full2abbr.get(item) for item in full]
            headers = (_('NAME'),_('ABBREVIATION'))
            iterable = [full,abbr]
            mes = sh.FastTable(iterable,headers).run()
            sh.com.run_fast_debug(f,mes)
        else:
            sh.com.rep_empty(f)
    
    def _debug_abbr2full(self):
        f = '[MClient] logic.SpeechPrior._debug_abbr2full'
        abbr2full = self.get_abbr2full()
        if abbr2full:
            abbr = sorted(abbr2full.keys())
            full = [abbr2full.get(item) for item in abbr]
            headers = (_('ABBREVIATION'),_('NAME'))
            iterable = [abbr,full]
            mes = sh.FastTable(iterable,headers).run()
            sh.com.run_fast_debug(f,mes)
        else:
            sh.com.rep_empty(f)
    
    def debug_pairs(self):
        f = '[MClient] logic.SpeechPrior.debug_pairs'
        if self.Success:
            self._debug_full2abbr()
            self._debug_abbr2full()
        else:
            sh.com.cancel(f)
    
    def prioritize(self):
        f = '[MClient] logic.SpeechPrior.prioritize'
        if self.Success:
            lst = [i + 1 for i in range(len(self.abbr))]
            for i in range(len(self.order)):
                try:
                    ind = self.full.index(self.order[i])
                    self.prior[ind] = lst[i]
                except ValueError:
                    mes = _('Wrong input data: "{}"!')
                    mes = mes.format(self.order[i])
                    sh.objs.get_mes(f,mes,True).show_warning()
            lst = lst[len(self.order):]
            try:
                ind = self.full.index(_('Phrase'))
                self.prior[ind] = 1000
                lst = lst[:-1]
            except ValueError:
                pass
            j = 0
            for i in range(len(self.prior)):
                if self.prior[i] == -1:
                    self.prior[i] = lst[j]
                    j += 1
        else:
            sh.com.cancel(f)
    
    def check(self):
        f = '[MClient] logic.SpeechPrior.check'
        if len(self.abbr):
            if len(self.abbr) == len(self.full):
                if len(self.order) > len(self.abbr):
                    self.Success = False
                    sub = '{} <= {}'.format (len(self.order)
                                            ,len(self.abbr)
                                            )
                    mes = _('The condition "{}" is not observed!')
                    mes = mes.format(sub)
                    sh.objs.get_mes(f,mes).show_error()
            else:
                self.Success = False
                sub = '{} == {}'.format(len(self.abbr),len(self.full))
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                sh.objs.get_mes(f,mes).show_error()
        else:
            self.Success = False
            sh.com.rep_empty(f)
    
    def set_values(self):
        self.abbr = [_('abbr.')
                    ,_('adj')
                    ,_('adv.')
                    ,_('art.')
                    ,_('conj.')
                    ,_('form')
                    ,_('interj.')
                    ,_('n')
                    ,_('num.')
                    ,_('ord.num.')
                    ,_('part.')
                    ,_('phrase')
                    ,_('predic.')
                    ,_('prepos.')
                    ,_('pron')
                    ,_('suf')
                    ,_('v')
                    ]
        self.full = [_('Abbreviation')
                    ,_('Adjective')
                    ,_('Adverb')
                    ,_('Article')
                    ,_('Conjunction')
                    ,_('Form')
                    ,_('Interjection')
                    ,_('Noun')
                    ,_('Numeral')
                    ,_('Ordinal Numeral')
                    ,_('Particle')
                    ,_('Phrase')
                    ,_('Predicative')
                    ,_('Preposition')
                    ,_('Pronoun')
                    ,_('Suffix')
                    ,_('Verb')
                    ]
        self.prior = [-1 for i in range(len(self.abbr))]
        self.Success = True
        self.abbr2full = {}
        self.full2abbr = {}



class Source:
    
    def __init__(self):
        self.title = ''
        self.status = _('not running')
        self.color = 'red'



class Welcome:

    def __init__ (self,product='MClient'
                 ,version='current'
                 ):
        self.set_values()
        self.product = product
        self.version = version
        self.desc = sh.List (lst1 = [self.product
                                    ,self.version
                                    ]
                            ).space_items()

    def set_values(self):
        self.sources = []
        self.sdstat = 0
        self.mtbstat = 0
        self.lgstat = 0
        self.sdcolor = 'red'
        self.mtbcolor = 'red'
        self.lgcolor = 'red'
        self.product = ''
        self.version = ''
        self.desc = ''
    
    def try_sources(self):
        f = '[MClient] logic.Welcome.try_sources'
        old = objs.get_plugins().source
        dics = objs.plugins.get_online_sources()
        if dics:
            for dic in dics:
                objs.plugins.set(dic)
                source = Source()
                source.title = dic
                if objs.plugins.is_accessible():
                    source.status = _('running')
                    source.color = 'green'
                self.sources.append(source)
        else:
            sh.com.rep_empty(f)
        # Try Stardict
        objs.plugins.set(_('Stardict'))
        self.sdstat = objs.get_plugins().is_accessible()
        if self.sdstat:
            self.sdcolor = 'green'
        # Try local Multitran
        objs.plugins.set(_('Local MT'))
        self.mtbstat = objs.plugins.is_accessible()
        if self.mtbstat:
            self.mtbcolor = 'green'
        # Try DSL
        objs.plugins.set('Lingvo (DSL)')
        self.lgstat = objs.plugins.is_accessible()
        if self.lgstat:
            self.lgcolor = 'green'
        objs.plugins.set(old)

    def gen_source_code(self,title,status,color):
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
        # Suppress useless warnings since the 2nd column may be empty
        if hotkey2:
            self.gen_hint(hint2)
            self.gen_hotkey(hotkey2)
        self.istr.write('</tr>')
    
    def set_hotkeys(self):
        self.istr.write('<font face="Serif" size="5">')
        self.istr.write('<table>')

        hint1 = _('Translate the current input or selection')
        hotkey1 = ('<Button-1>','<Return>')
        hint2 = _('Copy the current selection')
        hotkey2 = ('<Button-3>'
                   ,sh.lg.globs['str']['bind_copy_sel']
                   ,sh.lg.globs['str']['bind_copy_sel_alt']
                   )
        hint34 = _('Show the program window (system-wide)')
        hotkey34 = '<Alt_L-grave>'
        hint35 = _('Translate selection from an external program')
        hotkey35 = ('<Control_L-Insert-Insert>'
                   ,'<Control_L-c-c>'
                   )
        hint36 = _('Minimize the program window')
        hotkey36 = '<Escape>'
        hint37 = _('Quit the program')
        hotkey37 = ('<Control-q>'
                   ,sh.lg.globs['str']['bind_quit']
                   )
        hint3 = _('Copy the URL of the selected term')
        hotkey3 = sh.lg.globs['str']['bind_copy_url']
        hint4 = _('Copy the URL of the current article')
        hotkey4 = sh.lg.globs['str']['bind_copy_article_url']
        hint5 = _('Go to the previous section of column #%d') % 1
        hotkey5 = sh.lg.globs['str']['bind_col1_up']
        hint6 = _('Go to the next section of column #%d') % 1
        hotkey6 = sh.lg.globs['str']['bind_col1_down']
        hint7 = _('Go to the previous section of column #%d') % 2
        hotkey7 = sh.lg.globs['str']['bind_col2_up']
        hint8 = _('Go to the next section of column #%d') % 2
        hotkey8 = sh.lg.globs['str']['bind_col2_down']
        hint9 = _('Go to the previous section of column #%d') % 3
        hotkey9 = sh.lg.globs['str']['bind_col3_up']
        hint10 = _('Go to the next section of column #%d') % 3
        hotkey10 = sh.lg.globs['str']['bind_col3_down']
        hint11 = _('Open a webpage with a definition of the current term')
        hotkey11 = sh.lg.globs['str']['bind_define']
        hint12 = _('Look up phrases')
        hotkey12 = sh.lg.globs['str']['bind_go_phrases']
        hint13 = _('Go to the preceding article')
        hotkey13 = sh.lg.globs['str']['bind_go_back']
        hint14 = _('Go to the following article')
        hotkey14 = sh.lg.globs['str']['bind_go_forward']
        hint15 = _('Next source language')
        hotkey15 = (sh.lg.globs['str']['bind_next_lang1']
                   ,sh.lg.globs['str']['bind_next_lang1_alt']
                   )
        hint16 = _('Previous source language')
        hotkey16 = (sh.lg.globs['str']['bind_prev_lang1']
                   ,sh.lg.globs['str']['bind_prev_lang1_alt']
                   )
        hint17 = _('Create a printer-friendly page')
        hotkey17 = sh.lg.globs['str']['bind_print']
        hint18 = _('Open the current article in a default browser')
        hotkey18 = (sh.lg.globs['str']['bind_open_in_browser']
                   ,sh.lg.globs['str']['bind_open_in_browser_alt']
                   )
        hint19 = _('Reload the current article')
        hotkey19 = (sh.lg.globs['str']['bind_reload_article']
                   ,sh.lg.globs['str']['bind_reload_article_alt']
                   )
        hint20 = _('Save or copy the current article')
        hotkey20 = (sh.lg.globs['str']['bind_save_article']
                   ,sh.lg.globs['str']['bind_save_article_alt']
                   )
        hint21 = _('Start a new search in the current article')
        hotkey21 = sh.lg.globs['str']['bind_re_search_article']
        hint22 = _('Search the article forward')
        hotkey22 = sh.lg.globs['str']['bind_search_article_forward']
        hint23 = _('Search the article backward')
        hotkey23 = sh.lg.globs['str']['bind_search_article_backward']
        hint24 = _('Show settings')
        hotkey24 = (sh.lg.globs['str']['bind_settings']
                   ,sh.lg.globs['str']['bind_settings_alt']
                   )
        hint25 = _('About the program')
        hotkey25 = sh.lg.globs['str']['bind_show_about']
        hint26 = _('Paste a special symbol')
        hotkey26 = sh.lg.globs['str']['bind_spec_symbol']
        hint27 = _('Toggle alphabetizing')
        hotkey27 = sh.lg.globs['str']['bind_toggle_alphabet']
        hint28 = _('Toggle blacklisting')
        hotkey28 = sh.lg.globs['str']['bind_toggle_block']
        hint29 = _('Toggle History')
        hotkey29 = (sh.lg.globs['str']['bind_toggle_history']
                   ,sh.lg.globs['str']['bind_toggle_history_alt']
                   )
        hint30 = _('Toggle prioritizing')
        hotkey30 = sh.lg.globs['str']['bind_toggle_priority']
        hint31 = _('Toggle terms-only selection')
        hotkey31 = sh.lg.globs['str']['bind_toggle_sel']
        hint32 = _('Toggle the current article view')
        hotkey32 = (sh.lg.globs['str']['bind_toggle_view']
                   ,sh.lg.globs['str']['bind_toggle_view_alt']
                   )
        hint33 = _('Clear History')
        hotkey33 = sh.lg.globs['str']['bind_clear_history']
        hint38 = _('Next target language')
        hotkey38 = (sh.lg.globs['str']['bind_next_lang2']
                   ,sh.lg.globs['str']['bind_next_lang2_alt']
                   )
        hint39 = _('Previous target language')
        hotkey39 = (sh.lg.globs['str']['bind_prev_lang2']
                   ,sh.lg.globs['str']['bind_prev_lang2_alt']
                   )
        hint40 = _('Swap source and target languages')
        hotkey40 = sh.lg.globs['str']['bind_swap_langs']
        
        hint41 = _('Copy the nominative case')
        hotkey41 = sh.lg.globs['str']['bind_copy_nominative']
        
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
        self.gen_row(hint30,hotkey30,hint31,hotkey31)
        self.gen_row(hint32,hotkey32,hint33,hotkey33)
        self.gen_row(hint41,hotkey41,'','')
        
        self.istr.write('</font>')
        self.istr.write('</table>')
    
    def generate(self):
        f = '[MClient] logic.Welcome.generate'
        self.istr = io.StringIO()
        self.istr.write('<html>\n')
        self.istr.write('  <body>\n')
        self.istr.write('    <h1>')
        self.istr.write(_('Welcome to {}!').format(self.desc))
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
        for source in self.sources:
            self.gen_source_code (title = source.title
                                 ,status = source.status
                                 ,color = source.color
                                 )
        self.istr.write(_('Offline dictionaries loaded:'))
        self.istr.write(' Stardict: ')
        self.istr.write('\n')
        self.istr.write('      <font color="')
        self.istr.write(self.sdcolor)
        self.istr.write('">')
        self.istr.write('{}'.format(self.sdstat))
        self.istr.write('</font>, ')
        self.istr.write('Lingvo (DSL): ')
        self.istr.write('      <font color="')
        self.istr.write(self.lgcolor)
        self.istr.write('">')
        self.istr.write('{}'.format(self.lgstat))
        self.istr.write('</font>, ')
        self.istr.write('Multitran (Demo): ')
        self.istr.write('      <font color="')
        self.istr.write(self.mtbcolor)
        self.istr.write('">')
        self.istr.write('{}'.format(self.mtbstat))
        self.istr.write('</font>.')
        self.istr.write('<br><br><br><br>')
        self.istr.write('<h1>')
        self.istr.write(_('Main hotkeys'))
        self.istr.write('</h1>')
        self.istr.write('<h2>')
        self.istr.write(_('(see documentation for other hotkeys, mouse bindings and functions)'))
        self.istr.write('</h2>')
        self.set_hotkeys()
        self.istr.write('  </body>\n')
        self.istr.write('</html>')
        code = self.istr.getvalue()
        self.istr.close()
        return code

    def run(self):
        self.try_sources()
        return self.generate()



class DefaultConfig:
    
    def __init__(self,product='mclient'):
        self.set_values()
        self.ihome = sh.Home(app_name=product.lower())
        self.Success = self.ihome.create_conf()
    
    def set_values(self):
        self.dics = ''
        self.fblock = ''
        self.fconf = ''
        self.fdconf = ''
        self.fprior = ''
    
    def get_dics(self):
        f = '[MClient] logic.DefaultConfig.get_dics'
        if self.Success:
            if not self.dics:
                self.dics = self.ihome.add_config('dics')
                if self.dics:
                    if os.path.exists(self.dics):
                        self.Success = sh.Directory(path=self.dics).Success
                    else:
                        self.Success = sh.Path(path=self.dics).create()
                else:
                    self.Success = False
                    sh.com.rep_empty(f)
            return self.dics
        else:
            sh.com.cancel(f)
    
    def set_block(self):
        f = '[MClient] logic.DefaultConfig.set_block'
        if self.Success:
            self.fblock = self.ihome.add_config('block.txt')
            if self.fblock:
                if os.path.exists(self.fblock):
                    self.Success = sh.File(self.fblock).Success
                else:
                    iwrite = sh.WriteTextFile (file = self.fblock
                                              ,Rewrite = True
                                              )
                    iwrite.write(sample_block)
                    self.Success = iwrite.Success
            else:
                self.Success = False
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def prioritize(self):
        f = '[MClient] logic.DefaultConfig.prioritize'
        if self.Success:
            if not self.fprior:
                self.fprior = self.ihome.add_config('prioritize.txt')
                if self.fprior:
                    if os.path.exists(self.fprior):
                        self.Success = sh.File(file=self.fprior).Success
                    else:
                        iwrite = sh.WriteTextFile (file = self.fprior
                                                  ,Rewrite = True
                                                  )
                        iwrite.write(sample_prior)
                        self.Success = iwrite.Success
                else:
                    self.Success = False
                    sh.com.rep_empty(f)
            return self.fprior
        else:
            sh.com.cancel(f)
    
    def get_config(self):
        f = '[MClient] logic.DefaultConfig.get_config'
        if self.Success:
            if not self.fconf:
                self.fconf = self.ihome.add_config('mclient.cfg')
            return self.fconf
        else:
            sh.com.cancel(f)
    
    def run(self):
        f = '[MClient] logic.DefaultConfig.run'
        if self.Success:
            self.get_config()
            self.get_dics()
            self.set_block()
            self.prioritize()
        else:
            sh.com.cancel(f)



class CurRequest:

    def __init__(self):
        self.set_values()
        self.reset()
    
    def set_values(self):
        self.cols = ('dic','wform','transc','speech')
        self.collimit = sh.lg.globs['int']['colnum'] + 4
        ''' Toggling blacklisting should not depend on a number of
            blocked dictionaries (otherwise, it is not clear how
            blacklisting should be toggled)
        '''
        self.MouseClicked = False
        ''' *Temporary* turn off prioritizing and terms sorting for
            articles with 'sep_words_found' and in phrases; use previous
            settings for new articles.
        '''
        self.SpecialPage = False
    
    def reset(self):
        self.page = ''
        self.htm = ''
        self.htmraw = ''
        self.search = ''
        self.url = ''



# Read the blocklist and the prioritize list
class Lists:

    def __init__(self):
        f = '[MClient] logic.Lists.__init__'
        self.blacklst = objs.get_default().fblock
        self.priorlst = objs.default.fprior
        self.Success = objs.default.Success
    
    def get_blacklist(self):
        f = '[MClient] logic.Lists.get_blacklist'
        if self.Success:
            text = sh.ReadTextFile(file=self.blacklst).get()
            text = sh.Text(text=text,Auto=1).text
            return text.splitlines()
        else:
            sh.com.cancel(f)

    def prioritize(self):
        f = '[MClient] logic.Lists.prioritize'
        if self.Success:
            text = sh.ReadTextFile(file=self.priorlst).get()
            text = sh.Text(text=text,Auto=1).text
            return text.splitlines()
        else:
            sh.com.cancel(f)



class Objects:
    
    def __init__(self):
        self.online = self.request = self.order = self.default \
                    = self.plugins = self.speech_prior = self.config \
                    = None
    
    def get_config(self):
        if self.config is None:
            self.config = sh.Config(objs.get_default().get_config())
            self.config.run()
        return self.config
    
    def get_speech_prior(self,order=[]):
        if self.speech_prior is None:
            self.speech_prior = SpeechPrior(order)
        return self.speech_prior
    
    def get_plugins (self,Debug=False
                    ,maxrow=20,maxrows=1000
                    ):
        if self.plugins is None:
            self.plugins = manager.Plugins (sdpath = self.get_default().get_dics()
                                           ,mbpath = self.default.get_dics()
                                           ,timeout = sh.lg.globs['int']['timeout']
                                           ,Debug = Debug
                                           ,maxrow = maxrow
                                           ,maxrows = maxrows
                                           )
        return self.plugins
    
    def get_default(self,product='mclient'):
        if not self.default:
            self.default = DefaultConfig(product=product)
            self.default.run()
        return self.default
    
    def get_request(self):
        if self.request is None:
            self.request = CurRequest()
        return self.request
        
    def get_order(self):
        if self.order is None:
            self.order = Order()
        return self.order



# Create block and priority lists and complement them
class Order:
    
    def __init__(self):
        self.set_values()
        self.set_lists()
        self.conform()
        
    def fill_dic(self,lst,ind):
        lst = lst[1:]
        lst = lst[::-1]
        for item in lst:
            self.priorlst.insert(ind,item)
    
    def prioritize_by(self,Down=False):
        f = '[MClient] logic.Order.prioritize_by'
        if self.Success:
            if self.dic1 and self.dic2:
                ''' - Multiple dictionary titles share same blocks
                      for now, so we cannot distinguish them. Thus, all
                      titles of the same block must have the same
                      priority. Moreover, if any item of 'dic1' is
                      (un)prioritized, then all other items should be
                      (un)prioritized as well.
                    - Since we (un)prioritize one dictionary against
                      another here instead of simply (un)prioritizing
                      one dictionary (this logic is set in
                      'run_lm_auto'/'run_rm_auto'), both 'dic1' and
                      'dic2' should comprise prioritized dictionaries.
                      Since we cannot distinguish multiple dictionary
                      titles for now, both 'dic1' and 'dic2' should be
                      fully introduced into 'self.prioritize'.
                    - The only way to get a position of 'dic1' being
                      prioritized over 'dic2' is to get the position of
                      'dic2' in 'self.priorlst' first. Since both
                      'dic1' and 'dic2' have prioritized items (this
                      logic is set in 'run_lm_auto'/'run_rm_auto') and
                      are previously sorted by priority, first items of
                      'dic1' and 'dic2' should always exist (otherwise,
                      it is a logic error).
                '''
                if self.dic1[0] in self.priorlst \
                and self.dic2[0] in self.priorlst:
                    if Down:
                        message = _('Mode: "{}"')
                        message = message.format(_('Decrease priority'))
                    else:
                        message = _('Mode: "{}"')
                        message = message.format(_('Increase priority'))
                    sh.objs.get_mes(f,message,True).show_debug()
                    
                    # This allows not to delete duplicates later
                    for i in range(len(self.dic1)):
                        if i > 0:
                            self.unprioritize(self.dic1[i])
                    for i in range(len(self.dic2)):
                        if i > 0:
                            self.unprioritize(self.dic2[i])
                    
                    ind1 = self.priorlst.index(self.dic1[0])
                    ind2 = self.priorlst.index(self.dic2[0])
                    
                    if Down:
                        Swap = ind1 < ind2
                    else:
                        Swap = ind1 > ind2
                    if Swap:
                        mes = _('Swap items: {} <-> {}; "{}" <-> "{}"')
                        mes = mes.format (ind1,ind2
                                         ,self.priorlst[ind1]
                                         ,self.priorlst[ind2]
                                         )
                        sh.objs.get_mes(f,mes,True).show_debug()
                        self.priorlst[ind1], self.priorlst[ind2] \
                        = self.priorlst[ind2], self.priorlst[ind1]
                    
                    ind1 += 1
                    ind2 += 1
                    
                    if Swap:
                        dic1 = self.dic2
                        dic2 = self.dic1
                    else:
                        dic1 = self.dic1
                        dic2 = self.dic2
                    
                    if ind2 > ind1:
                        self.fill_dic(dic2,ind2)
                        self.fill_dic(dic1,ind1)
                    else:
                        self.fill_dic(dic1,ind1)
                        self.fill_dic(dic2,ind2)
                        
                    lst = sh.List(lst1=self.priorlst).delete_duplicates()
                    if lst:
                        self.priorlst = list(lst)
                    else:
                        sh.com.rep_empty(f)
                    
                    mes = 'Dic1: {}'.format(self.dic1)
                    sh.objs.get_mes(f,mes,True).show_debug()
                    mes = 'Dic2: {}'.format(self.dic2)
                    sh.objs.get_mes(f,mes,True).show_debug()
                    mes = str(self.priorlst)
                    sh.objs.get_mes(f,mes,True).show_debug()
                else:
                    mes = _('Logic error!')
                    sh.objs.get_mes(f,mes).show_error()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
            
    def get_priority(self,search):
        f = '[MClient] logic.Order.get_priority'
        if self.Success:
            lst = self.get_list(search)
            if lst:
                prior = []
                for item in lst:
                    try:
                        ind = self.priorlst.index(item)
                        prior.append(len(self.priorlst)-ind)
                    except ValueError:
                        pass
                if prior:
                    return max(prior)
                else:
                    return 0
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def run_lm_auto(self,dic1,dic2=''):
        ''' A LM click on:
            1) A blocked dictionary     - unblock
            2) A common dictionary      - prioritize
            3) A prioritized dictionary - increase priority
        '''
        f = '[MClient] logic.Order.run_lm_auto'
        if self.Success:
            self.set(dic1,dic2)
            if self.is_blocked(self.dic1):
                for item in self.dic1:
                    self.unblock(item)
            elif self.is_prioritized(self.dic1) \
            and self.is_prioritized(self.dic2) \
            and not sh.List(self.dic1,self.dic2).get_shared():
                self.prioritize_by()
            else:
                for item in self.dic1:
                    self.prioritize(item)
        else:
            sh.com.cancel(f)
    
    def run_rm_auto(self,dic1,dic2=''):
        ''' A RM click on:
            1) A prioritized dictionary - decrease priority or
                                          unprioritize
                                          (at minimal priority)
            2) A blocked dictionary     - unblock
            3) A common dictionary      - block
        '''
        f = '[MClient] logic.Order.run_rm_auto'
        if self.Success:
            self.set(dic1,dic2)
            if self.is_blocked(self.dic1):
                for item in self.dic1:
                    self.unblock(item)
            elif self.is_prioritized(self.dic1):
                if self.is_prioritized(self.dic2) \
                and not sh.List(self.dic1,self.dic2).get_shared():
                    self.prioritize_by(Down=True)
                else:
                    for item in self.dic1:
                        self.unprioritize(item)
            else:
                ''' Multiple dictionary titles share same blocks
                    for now, so we cannot distinguish them. Thus,
                    if any item of 'dic1' is blocked, then all
                    other items should be blocked as well.
                '''
                for item in self.dic1:
                    self.block(item)
        else:
            sh.com.cancel(f)
    
    def is_prioritized(self,lst):
        f = '[MClient] logic.Order.is_prioritized'
        if self.Success:
            if lst:
                for item in lst:
                    if item in self.priorlst:
                        return True
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def is_blocked(self,lst):
        f = '[MClient] logic.Order.is_blocked'
        if self.Success:
            if lst:
                for item in lst:
                    if item in self.blacklst:
                        return True
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def conform(self):
        f = '[MClient] logic.Order.conform'
        ''' Create new block and priority lists based on those that were
            read from user files. Lists from user files may comprise
            either full or short dictionary titles. New lists will be
            lowercased and stripped and will comprise both full and
            short titles.
        '''
        if self.Success:
            ''' We recreate lists in order to preserve 
                the short + full title order.
            '''
            if self.blacklst:
                blacklst = list(self.blacklst)
                self.blacklst = []
                for item in blacklst:
                    pair = self.get_pair(item)
                    if pair:
                        self.block(pair[0])
                        self.block(pair[1])
                    else:
                        sh.com.rep_empty(f)
            else:
                sh.com.rep_lazy(f)
            if self.priorlst:
                priorlst = list(self.priorlst)
                self.priorlst = []
                for item in priorlst:
                    pair = self.get_pair(item)
                    if pair:
                        self.prioritize(pair[0])
                        self.prioritize(pair[1])
                    else:
                        sh.com.rep_empty(f)
            else:
                sh.com.rep_lazy(f)
        else:
            sh.com.cancel(f)
    
    def set_lists(self):
        f = '[MClient] logic.Order.set_lists'
        if self.Success:
            self.lists = Lists()
            self.blacklst = sh.Input (title = f
                                     ,value = self.lists.get_blacklist()
                                     ).get_list()
            self.priorlst = sh.Input (title = f
                                     ,value = self.lists.prioritize()
                                     ).get_list()
            self.Success = self.lists.Success
        else:
            sh.com.cancel(f)
    
    def set_values(self):
        self.Success = True
        self.lists = None
        self.blacklst = []
        self.priorlst = []
        self.dic1 = ''
        self.dic2 = ''
            
    def sort_dic(self,lst):
        f = '[MClient] logic.Order.sort_dic'
        if self.Success:
            if lst:
                indexes = []
                for item in lst:
                    try:
                        ind = self.priorlst.index(item)
                    except ValueError:
                        # Place an unpriotitized dictionary at the end
                        ind = 1000
                    indexes.append(ind)
                lst = sorted(zip(indexes,lst))
                lst = [item[1] for item in lst]
                return lst
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def set(self,dic1,dic2=''):
        f = '[MClient] logic.Order.set'
        if self.Success:
            ''' This allows to return an empty value instead of the last
                memory in case there is no previous/next dictionary.
            '''
            self.dic1 = self.dic2 = ''
            if dic1:
                dic1 = self.get_list(dic1)
                dic1 = self.sort_dic(dic1)
                self.dic1 = list(dic1)
            else:
                sh.com.rep_empty(f)
            if dic2:
                dic2 = self.get_list(dic2)
                dic2 = self.sort_dic(dic2)
                self.dic2 = list(dic2)
        else:
            sh.com.cancel(f)
    
    def get_pair(self,item):
        f = '[MClient] logic.Order.get_pair'
        if self.Success:
            if item:
                if objs.get_plugins().is_abbr(item):
                    abbr = item
                    title = objs.plugins.get_title(item)
                else:
                    abbr = objs.plugins.get_abbr(item)
                    title = item
                return([abbr,title])
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def get_list(self,search):
        f = '[MClient] logic.Order.get_list'
        if self.Success:
            if search:
                search = search.split(',')
                lst = []
                for item in search:
                    pair = self.get_pair(item)
                    if pair:
                        lst += pair
                return lst
            # Prevents from None
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def block(self,item):
        if self.Success:
            if not item in self.blacklst:
                self.blacklst.append(item)
                          
    def unblock(self,item):
        f = '[MClient] logic.Order.unblock'
        if self.Success:
            try:
                self.blacklst.remove(item)
            except ValueError:
                pass
        else:
            sh.com.cancel(f)
                          
    def prioritize(self,item):
        f = '[MClient] logic.Order.prioritize'
        if self.Success:
            if not item in self.priorlst:
                self.priorlst.append(item)
        else:
            sh.com.cancel(f)
    
    def unprioritize(self,item):
        f = '[MClient] logic.Order.unprioritize'
        if self.Success:
            try:
                self.priorlst.remove(item)
            except ValueError:
                pass
        else:
            sh.com.cancel(f)



class Commands:
    
    def __init__(self):
        self.use_unverified()
    
    def load_config(self):
        objs.get_config()
    
    def save_config(self):
        CreateConfig(objs.get_default().get_config()).run()
    
    def dump_elems(self,blocks,artid):
        f = '[MClient] logic.Commands.dump_elems'
        if blocks and artid:
            data = []
            for block in blocks:
                data.append (
                  (None               # (00) Skips the autoincrement
                  ,artid              # (01) ARTICLEID
                  ,block.dic          # (02) DIC (short title)
                  ,block.wform        # (03) WFORM
                  ,block.speech       # (04) SPEECH
                  ,block.transc       # (05) TRANSC
                  ,block.term         # (06) TERM
                  ,block.type_        # (07) TYPE
                  ,block.text         # (08) TEXT
                  ,block.url          # (09) URL
                  ,block.block        # (10) BLOCK
                  ,block.dprior       # (11) DICPR
                  ,block.select       # (12) SELECTABLE
                  ,block.same         # (13) SAMECELL
                  ,block.cellno       # (14) CELLNO
                  ,-1                 # (15) ROWNO
                  ,-1                 # (16) COLNO
                  ,-1                 # (17) POS1
                  ,-1                 # (18) POS2
                  ,''                 # (19) NODE1
                  ,''                 # (20) NODE2
                  ,-1                 # (21) OFFPOS1
                  ,-1                 # (22) OFFPOS2
                  ,-1                 # (23) BBOX1
                  ,-1                 # (24) BBOX2
                  ,-1                 # (25) BBOY1
                  ,-1                 # (26) BBOY2
                  ,block.text.lower() # (27) TEXTLOW
                  ,0                  # (28) IGNORE
                  ,block.sprior       # (29) SPEECHPR
                  ,block.dicf         # (30) DIC (full title)
                  )
                            )
            return data
        else:
            sh.com.rep_empty(f)
    
    def suggest(self,search,limit=0):
        f = '[MClient] logic.Commands.suggest'
        items = objs.get_plugins().suggest(search)
        if items:
            if limit:
                items = items[0:limit]
        else:
            items = []
            sh.com.rep_empty(f)
        return items
        
    def use_unverified(self):
        f = '[MClient] logic.Commands.use_unverified'
        ''' On *some* systems we can get urllib.error.URLError: 
            <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED].
            To get rid of this error, we use this small workaround.
        '''
        if hasattr(ssl,'_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context
        else:
            mes = _('Unable to use unverified certificates!')
            sh.objs.get_mes(f,mes,True).show_warning()


objs = Objects()
com = Commands()
DefaultKeys()
com.load_config()
