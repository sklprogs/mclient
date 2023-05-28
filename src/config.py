#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import json

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

PRODUCT_LOW = 'mclient'
sample_prior = _('General')


class DefaultKeys(sh.DefaultKeys):

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load()
    
    def load(self):
        self._load_bool()
        self._load_int()
        self._load_float()
        self._load_str()
        
    def _load_bool(self):
        sh.lg.globs['bool'].update ({
            'AdjustByWidth'      :True
           ,'AlphabetizeTerms'   :True
           ,'Autocompletion'     :True
           ,'Autoswap'           :False
           ,'BlockSubjects'      :True
           ,'CaptureHotkey'      :True
           ,'Iconify'            :True
           ,'PhraseCount'        :True
           ,'Ping'               :True
           ,'PrioritizeSubjects' :True
           ,'SelectTermsOnly'    :True
           ,'ShortSubjects'      :False
           ,'ShortSpeech'        :True
           ,'ShowUserNames'      :True
           ,'SortByColumns'      :True
           ,'VerticalView'       :False
                                   })
    
    def _load_float(self):
        sh.lg.globs['float'].update ({
            'timeout' : 5.0
                                    })
    
    def _load_int(self):
        sh.lg.globs['int'].update ({
            'colnum'            :4
           ,'fixed_col_width'   :63
           ,'font_col1_size'    :12
           ,'font_col2_size'    :12
           ,'font_col3_size'    :11
           ,'font_col4_size'    :11
           ,'font_comments_size':11
           ,'font_terms_size'   :12
           ,'term_col_width'    :157
           ,'hotkey_delay'      :600
                                  })
    
    def _load_str(self):
        sh.lg.globs['str'].update ({
            'bind_clear_history'          :'Ctrl+Shift+Del'
           ,'bind_col1_down'              :'Ctrl+Down'
           ,'bind_col1_up'                :'Ctrl+Up'
           ,'bind_col2_down'              :'Alt+Down'
           ,'bind_col2_up'                :'Alt+Up'
           ,'bind_col3_down'              :'Shift+Down'
           ,'bind_col3_up'                :'Shift+Up'
           ,'bind_col4_down'              :'Ctrl+Shift+Down'
           ,'bind_col4_up'                :'Ctrl+Shift+Up'
           ,'bind_copy_article_url'       :'Ctrl+F7'
           ,'bind_copy_nominative'        :'Ctrl+W'
           ,'bind_copy_sel'               :'Ctrl+Return'
           ,'bind_copy_sel_alt'           :'Ctrl+Enter'
           ,'bind_copy_url'               :'Shift+F7'
           ,'bind_define'                 :'Ctrl+D'
           ,'bind_go_back'                :'Alt+Left'
           ,'bind_go_next'                :'Alt+Right'
           ,'bind_go_phrases'             :'Alt+F'
           ,'bind_next_lang1'             :'F8'
           ,'bind_next_lang1_alt'         :'Ctrl+K'
           ,'bind_next_lang2'             :'F9'
           ,'bind_next_lang2_alt'         :'Ctrl+L'
           ,'bind_prev_lang1'             :'Shift+F8'
           ,'bind_prev_lang1_alt'         :'Ctrl+K'
           ,'bind_prev_lang2'             :'Shift+F9'
           ,'bind_prev_lang2_alt'         :'Ctrl+L'
           ,'bind_open_in_browser'        :'F7'
           ,'bind_open_in_browser_alt'    :'Ctrl+B'
           ,'bind_print'                  :'Ctrl+P'
           ,'bind_quit'                   :'F10'
           ,'bind_re_search_article'      :'Ctrl+F3'
           ,'bind_reload_article_alt'     :'Ctrl+R'
           ,'bind_reload_article'         :'F5'
           ,'bind_save_article_alt'       :'Ctrl+S'
           ,'bind_save_article'           :'F2'
           ,'bind_search_article_backward':'Shift+F3'
           ,'bind_search_article_forward' :'F3'
           ,'bind_settings'               :'Alt+S'
           ,'bind_settings_alt'           :'F12'
           ,'bind_show_about'             :'F1'
           ,'bind_spec_symbol'            :'Ctrl+E'
           ,'bind_swap_langs'             :'Ctrl+Space'
           ,'bind_toggle_alphabet'        :'Alt+A'
           ,'bind_toggle_block'           :'Alt+B'
           ,'bind_toggle_history'         :'F4'
           ,'bind_toggle_history_alt'     :'Ctrl+H'
           ,'bind_toggle_popup'           :'Alt+X'
           ,'bind_toggle_priority'        :'Alt+P'
           ,'bind_toggle_view'            :'F6'
           ,'bind_toggle_view_alt'        :'Alt+V'
           ,'col1_type'                   :_('Subjects')
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
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def fill_bool(self):
        section = _('Booleans')
        comment = _('The following values are allowed in this section: 0 (False) or 1 (True)')
        self.add_section(section, comment)
        section_abbr = self.sections[-1].abbr
        
        key = 'AdjustByWidth'
        comment = _('[Autosave] Adjust columns by width')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'AlphabetizeTerms'
        comment = _('[Autosave] Sort terms by alphabet')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'Autocompletion'
        comment = _('[Autosave] Show suggestions on input')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'Autoswap'
        comment = _('[Autosave] Autoswap Russian and the other language if appropriate')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'BlockSubjects'
        comment = _('[Autosave] Block subjects from the blacklist')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'CaptureHotkey'
        comment = _('[Autosave] Capture Ctrl-c-c and Ctrl-Ins-Ins system-wide')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'Iconify'
        comment = _('[Autosave] Minimize the application window after specific actions, e.g., copying')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'Ping'
        comment = _('Ping online sources at startup')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'PhraseCount'
        comment = _('[Autosave] Show a phrase count')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'PrioritizeSubjects'
        comment = _('[Autosave] Prioritize subjects from the prioritization file')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'SelectTermsOnly'
        comment = _('[Autosave] Select blocks of all types (False) or terms only (True)')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'ShortSubjects'
        comment = _('[Autosave] Shorten subject titles')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'ShortSpeech'
        comment = _('[Autosave] Shorten parts of speech')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'ShowUserNames'
        comment = _('[Autosave] Show user names')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'SortByColumns'
        comment = _('[Autosave] Sort by each column')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'VerticalView'
        comment = _('[Autosave] Vertical view')
        self.add_key(section, section_abbr, key, comment)
    
    def fill_float(self):
        section = _('Floatings')
        self.add_section(section)
        section_abbr = self.sections[-1].abbr
        
        key = 'timeout'
        comment = _('A connection timeout (fractions of a second)')
        self.add_key(section, section_abbr, key, comment)
    
    def fill_int(self):
        section = _('Integers')
        self.add_section(section)
        section_abbr = self.sections[-1].abbr
        
        key = 'colnum'
        comment = _('[Autosave] Number of non-fixed columns')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'fixed_col_width'
        comment = _('[Autosave] Fixed column width')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'font_comments_size'
        comment = _('A font size of comments')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'font_col1_size'
        comment = _('A font size of column #{}')
        comment = comment.format(1)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'font_col2_size'
        comment = _('A font size of column #{}')
        comment = comment.format(2)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'font_col3_size'
        comment = _('A font size of column #{}')
        comment = comment.format(3)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'font_col4_size'
        comment = _('A font size of column #{}')
        comment = comment.format(4)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'font_terms_size'
        comment = _('A font size of terms')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'hotkey_delay'
        comment = _('[Experts only] Delay in reacting to Ctrl-C-C and Ctrl-Ins-Ins hotkeys (in milliseconds)')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'term_col_width'
        comment = _('[Autosave] Term column width')
        self.add_key(section, section_abbr, key, comment)
    
    def fill_str(self):
        section = _('Strings')
        comment = _('Attention: some hotkeys, e.g., <Button-1> and <Double-Button-1> may conflict with each other. Reassign them with caution.')
        self.add_section(section, comment)
        section_abbr = self.sections[-1].abbr
        
        key = 'bind_clear_history'
        comment = _('Clear History')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_col1_down'
        comment = _('Go to the next section of column #{}').format(1)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_col1_up'
        comment = _('Go to the previous section of column #{}')
        comment = comment.format(1)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_col2_down'
        comment = _('Go to the next section of column #{}').format(2)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_col2_up'
        comment = _('Go to the previous section of column #{}')
        comment = comment.format(2)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_col3_down'
        comment = _('Go to the next section of column #{}').format(3)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_col3_up'
        comment = _('Go to the previous section of column #{}')
        comment = comment.format(3)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_col4_down'
        comment = _('Go to the next section of column #{}').format(4)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_col4_up'
        comment = _('Go to the previous section of column #{}')
        comment = comment.format(4)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_copy_article_url'
        comment = _('Copy URL of the current article')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_copy_nominative'
        comment = _('Copy an original word/phrase in a nominative case')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_copy_sel'
        comment = _('Copy a current selection from the article (combination #{})')
        comment = comment.format(1)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_copy_sel_alt'
        comment = _('Copy a current selection from the article (combination #{})')
        comment = comment.format(2)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_copy_url'
        comment = _('Copy URL of the current term')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_define'
        comment = _('Open a web-page defining the current term')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_go_back'
        comment = _('Go to the previous article')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_go_next'
        comment = _('Go to the next article')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_go_phrases'
        comment = _('Go to the phrases section')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_next_lang1'
        comment = _('Set next language {} (combination {})')
        comment = comment.format(1, 1)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_next_lang1_alt'
        comment = _('Set next language {} (combination {})')
        comment = comment.format(1, 2)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_next_lang2'
        comment = _('Set next language {} (combination {})')
        comment = comment.format(2, 1)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_next_lang2_alt'
        comment = _('Set next language {} (combination {})')
        comment = comment.format(2, 2)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_prev_lang1'
        comment = _('Set previous language #{} (combination #{})')
        comment = comment.format(1, 1)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_prev_lang1_alt'
        comment = _('Set previous language #{} (combination #{})')
        comment = comment.format(1, 2)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_prev_lang2'
        comment = _('Set previous language #{} (combination #{})')
        comment = comment.format(2, 1)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_prev_lang2_alt'
        comment = _('Set previous language #{} (combination #{})')
        comment = comment.format(2, 2)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_print'
        comment = _('Create a printer-friendly page')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_quit'
        comment = _('Quit the program')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_open_in_browser'
        comment = _('Open the current article in a browser (combination #{})')
        comment = comment.format(1)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_open_in_browser_alt'
        comment = _('Open the current article in a browser (combination #{})')
        comment = comment.format(2)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_reload_article'
        comment = _('Reload the current article (combination #{})')
        comment = comment.format(1)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_reload_article_alt'
        comment = _('Reload the current article (combination #{})')
        comment = comment.format(2)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_re_search_article'
        comment = _('Start a new term search in the current article')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_save_article'
        comment = _('Save or copy the current article (combination #{})')
        comment = comment.format(1)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_save_article_alt'
        comment = _('Save or copy the current article (combination #{})')
        comment = comment.format(2)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_search_article_backward'
        comment = _('Search the article backward')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_search_article_forward'
        comment = _('Search the article forward')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_settings'
        comment = _('Show settings (combination #{})')
        comment = comment.format(1)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_settings_alt'
        comment = _('Show settings (combination #{})')
        comment = comment.format(2)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_show_about'
        comment = _('About the program')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_spec_symbol'
        comment = _('Paste a special symbol')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_swap_langs'
        comment = _('Swap source and target languages')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_toggle_alphabet'
        comment = _('Toggle alphabetizing')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_toggle_block'
        comment = _('Toggle blacklisting')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_toggle_history'
        comment = _('Toggle History (combination #{})')
        comment = comment.format(1)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_toggle_history_alt'
        comment = _('Toggle History (combination #{})')
        comment = comment.format(2)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_toggle_popup'
        comment = _('Toggle popup')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_toggle_priority'
        comment = _('Toggle prioritizing')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_toggle_view'
        comment = _('Toggle the current article view (combination #{})')
        comment = comment.format(1)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'bind_toggle_view_alt'
        comment = _('Toggle the current article view (combination #{})')
        comment = comment.format(2)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'col1_type'
        comment = _('[Autosave] Type of column #{} in settings')
        comment = comment.format(1)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'col2_type'
        comment = _('[Autosave] Type of column #{} in settings')
        comment = comment.format(2)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'col3_type'
        comment = _('[Autosave] Type of column #{} in settings')
        comment = comment.format(3)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'col4_type'
        comment = _('[Autosave] Type of column #{} in settings')
        comment = comment.format(4)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'color_comments'
        comment = _('A font color for comments and user names')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'color_col1'
        comment = _('A font color for column #{}')
        comment = comment.format(1)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'color_col2'
        comment = _('A font color for column #{}')
        comment = comment.format(2)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'color_col3'
        comment = _('A font color for column #{}')
        comment = comment.format(3)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'color_col4'
        comment = _('A font color for column #{}')
        comment = comment.format(4)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'color_terms'
        comment = _('A font color for terms')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'color_terms_sel_bg'
        comment = _('A font background color for the current (selected) term')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'color_terms_sel_fg'
        comment = _('A font foreground color for the current (selected) term')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'font_comments_family'
        comment = _('A font of comments and user names')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'font_col1_family'
        comment = _('A font of column #{}')
        comment = comment.format(1)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'font_col2_family'
        comment = _('A font of column #{}')
        comment = comment.format(2)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'font_col3_family'
        comment = _('A font of column #{}')
        comment = comment.format(3)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'font_col4_family'
        comment = _('A font of column #{}')
        comment = comment.format(4)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'font_history'
        comment = _('A font color for History')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'font_style'
        comment = _('A program GUI font')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'font_terms_family'
        comment = _('A font of terms')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'font_terms_sel'
        comment = _('A font of the current (selected) term')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'lang1'
        comment = _('[Autosave] Source language')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'lang2'
        comment = _('[Autosave] Target language')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'repeat_sign'
        comment = _('Insert the last search request into the search field')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'repeat_sign2'
        comment = _('Insert the next-to-last search request into the search field')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'source'
        comment = _('[Autosave] The main dictionary source to use')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'spec_syms'
        comment = _('Characters that can be inserted into the search field')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'speech1'
        comment = _('[Autosave] A part of speech of column #{} in settings')
        comment = comment.format(1)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'speech2'
        comment = _('[Autosave] A part of speech of column #{} in settings')
        comment = comment.format(2)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'speech3'
        comment = _('[Autosave] A part of speech of column #{} in settings')
        comment = comment.format(3)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'speech4'
        comment = _('[Autosave] A part of speech of column #{} in settings')
        comment = comment.format(4)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'speech5'
        comment = _('[Autosave] A part of speech of column #{} in settings')
        comment = comment.format(5)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'speech6'
        comment = _('[Autosave] A part of speech of column #{} in settings')
        comment = comment.format(6)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'speech7'
        comment = _('[Autosave] A part of speech of column #{} in settings')
        comment = comment.format(7)
        self.add_key(section, section_abbr, key, comment)
        
        key = 'style'
        comment = _('[Autosave] A sorting style')
        self.add_key(section, section_abbr, key, comment)
        
        key = 'web_search_url'
        comment = _('URL for online search')
        self.add_key(section, section_abbr, key, comment)



class Subjects:
    
    def __init__(self):
        self.set_values()
        self.ihome = sh.Home(PRODUCT_LOW)
        self.Success = self.ihome.create_conf()
    
    def set_values(self):
        self.Success = True
        self.file = ''
        self.body = {}
    
    def add(self, body):
        f = '[MClient] config.Subjects.add'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not body:
            sh.com.rep_lazy(f)
            return
        count = 0
        for key in body:
            # JSON accepts empty keys and values
            if not key:
                sh.com.rep_empty(f)
                continue
            value = body[key]
            if not value:
                sh.com.rep_empty(f)
                continue
            ''' 'key' must be different from 'value' since we need new expanded
                subjects. If the same value is returned after expanding, this
                means that a short-full subject pair has not been found.
            '''
            if not key in self.body and key != value:
                count += 1
                self.body[key] = value
        sh.com.rep_matches(f, count)
    
    def set_file(self):
        f = '[MClient] config.Subjects.set_file'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.file = self.ihome.add_config('subjects.json')
        if not self.file:
            self.Success = False
            sh.com.rep_empty(f)
            return
    
    def create(self):
        f = '[MClient] config.Subjects.create'
        if not self.Success:
            sh.com.cancel(f)
            return
        if os.path.exists(self.file):
            self.Success = sh.File(self.file).Success
        else:
            iwrite = sh.WriteTextFile(self.file)
            # JSON throws an error upon an empty file
            iwrite.write('{}')
            self.Success = iwrite.Success
    
    def load(self):
        f = '[MClient] config.Subjects.load'
        if not self.Success:
            sh.com.cancel(f)
            return
        code = sh.ReadTextFile(self.file, True).get()
        try:
            self.body = json.loads(code)
        except Exception as e:
            self.Success = False
            sh.com.rep_third_party(f,e)
    
    def save(self):
        f = '[MClient] config.Subjects.save'
        if not self.Success:
            sh.com.cancel(f)
            return
        mes = _('Write file "{}"').format(self.file)
        sh.objs.get_mes(f,mes,True).show_info()
        try:
            with open(self.file, 'w', encoding='utf-8') as iopen:
                json.dump(self.body, iopen, ensure_ascii=False, indent=4)
        except Exception as e:
            ''' Failing a class which produced a writing error should not fail
                all writing operations some of which may actually be successful.
            '''
            mes = _('Third-party module has failed!\n\nDetails: {}').format(e)
            sh.objs.get_mes(f, mes).show_error()
    
    def run(self):
        self.set_file()
        self.create()
        self.load()



class PlainList:
    
    def __init__(self, basename):
        self.set_values()
        self.ihome = sh.Home(PRODUCT_LOW)
        self.basename = basename
    
    def set_values(self):
        self.Success = True
        self.basename = ''
        self.file = ''
        self.body = []
    
    def check(self):
        self.Success = self.ihome.create_conf() and self.basename
    
    def set_file(self):
        f = '[MClient] config.PlainList.set_file'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.file = self.ihome.add_config(self.basename)
        if not self.file:
            self.Success = False
            sh.com.rep_empty(f)
            return
    
    def create(self):
        f = '[MClient] config.PlainList.create'
        if not self.Success:
            sh.com.cancel(f)
            return
        if os.path.exists(self.file):
            self.Success = sh.File(self.file).Success
        else:
            iwrite = sh.WriteTextFile (file = self.file
                                      ,Empty = True
                                      )
            iwrite.write('')
            self.Success = iwrite.Success
    
    def load(self):
        f = '[MClient] config.PlainList.load'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.body = sh.ReadTextFile(self.file,True).get().splitlines()
        self.body = [line.strip() for line in self.body]
    
    def save(self):
        f = '[MClient] config.PlainList.save'
        if not self.Success:
            sh.com.cancel(f)
            return
        iwrite = sh.WriteTextFile(self.file,True,True)
        iwrite.write('\n'.join(self.body))
        self.Success = iwrite.Success
    
    def run(self):
        self.check()
        self.set_file()
        self.create()
        self.load()



class DefaultConfig:
    
    def __init__(self):
        self.set_values()
    
    def set_values(self):
        self.dics = ''
        self.fconf = ''
        self.fblock = ''
        self.fprior = ''
        self.fsubj = ''
        self.block = ''
        self.prior = ''
        self.subj = {}
    
    def check(self):
        self.ihome = sh.Home(PRODUCT_LOW)
        self.isubj = Subjects()
        self.iblock = PlainList('block.txt')
        self.iprior = PlainList('prioritize.txt')
        self.isubj.run()
        self.iblock.run()
        self.iprior.run()
        self.Success = self.ihome.create_conf() and self.isubj.Success \
                       and self.iblock.Success and self.iprior.Success
        
    
    def add_subjects(self, dic):
        self.isubj.add(dic)
    
    def set_files(self):
        self.fconf = self.ihome.add_config('mclientqt.cfg')
        self.fblock = self.iblock.file
        self.fprior = self.iprior.file
        self.fsubj = self.isubj.file
    
    def set_bodies(self):
        self.block = self.iblock.body
        self.prior = self.iprior.body
        self.subj = self.isubj.body
    
    def get_dics(self):
        f = '[MClient] config.DefaultConfig.get_dics'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.dics = self.ihome.add_config('dics')
        if not self.dics:
            self.Success = False
            sh.com.rep_empty(f)
            return
        if os.path.exists(self.dics):
            self.Success = sh.Directory(self.dics).Success
        else:
            self.Success = sh.Path(self.dics).create()
        return self.dics
    
    def save(self):
        self.isubj.save()
        self.iblock.save()
        self.iprior.save()
    
    def run(self):
        self.check()
        self.set_files()
        self.set_bodies()
        self.get_dics()
