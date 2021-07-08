#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sys
import io
import tkinter as tk
from skl_shared.localize import _
import skl_shared.shared as sh
import skl_shared.web as wb
import logic as lg
import gui as gi
#import debug_gui as gi
import cells as cl
import mkhtml as mh
import db
import subjects.priorities.controller as pr
import subjects.blacklist.controller as bl
import about.controller as ab
import third_parties.controller as tp
import subjects.subjects as sj


if __name__ == '__main__':
    if sh.objs.get_os().is_win():
        import keylistener.windows as kl
        import pythoncom
    else:
        import keylistener.linux as kl



class About(ab.About):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    
    def show_third_parties(self,event=None):
        objs.get_parties().show()



class ExportSettingsUI:
    
    def export_speech_area(self):
        sh.lg.globs['str']['speech1'] = objs.get_settings_ui().opt_sp1.choice
        sh.lg.globs['str']['speech2'] = objs.settings_ui.opt_sp2.choice
        sh.lg.globs['str']['speech3'] = objs.settings_ui.opt_sp3.choice
        sh.lg.globs['str']['speech4'] = objs.settings_ui.opt_sp4.choice
        sh.lg.globs['str']['speech5'] = objs.settings_ui.opt_sp5.choice
        sh.lg.globs['str']['speech6'] = objs.settings_ui.opt_sp6.choice
        sh.lg.globs['str']['speech7'] = objs.settings_ui.opt_sp7.choice
    
    def export_style_area(self):
        sh.lg.globs['str']['style'] = objs.get_settings_ui().opt_scm.choice
        sh.lg.globs['str']['col1_type'] = objs.settings_ui.opt_cl1.choice
        sh.lg.globs['str']['col2_type'] = objs.settings_ui.opt_cl2.choice
        sh.lg.globs['str']['col3_type'] = objs.settings_ui.opt_cl3.choice
        sh.lg.globs['str']['col4_type'] = objs.settings_ui.opt_cl4.choice
        com.export_style()
    
    def export_checkboxes(self):
        sh.lg.globs['bool']['SortByColumns'] = objs.get_settings_ui().cbx_no1.get()
        sh.lg.globs['bool']['AlphabetizeTerms'] = objs.settings_ui.cbx_no2.get()
        sh.lg.globs['bool']['BlockSubjects'] = objs.settings_ui.cbx_no3.get()
        sh.lg.globs['bool']['PrioritizeSubjects'] = objs.settings_ui.cbx_no4.get()
        sh.lg.globs['bool']['VerticalView'] = objs.settings_ui.cbx_no5.get()
        sh.lg.globs['bool']['ShortSubjects'] = objs.settings_ui.cbx_no6.get()
        sh.lg.globs['bool']['ShortSpeech'] = objs.settings_ui.cbx_no7.get()
        sh.lg.globs['bool']['ShowUserNames'] = objs.settings_ui.cbx_no8.get()
        objs.get_blocksdb().Selectable = sh.lg.globs['bool']['SelectTermsOnly']\
                                       = objs.settings_ui.cbx_no9.get()
        sh.lg.globs['bool']['Iconify'] = objs.settings_ui.cbx_no10.get()
        sh.lg.globs['bool']['Autocompletion'] = objs.settings_ui.cbx_no11.get()
        sh.lg.globs['bool']['Autoswap'] = objs.settings_ui.cbx_no12.get()
        sh.lg.globs['bool']['PhraseCount'] = objs.settings_ui.cbx_no13.get()
    
    def run(self):
        f = '[MClient] mclient.ExportSettingsUI.run'
        # 'objs.get_settings_ui' may not be used as often
        if objs.settings is None or objs.settings.gui is None:
            sh.com.rep_lazy(f)
        else:
            self.export_style_area()
            self.export_speech_area()
            self.export_checkboxes()



class Commands:
    ''' #NOTE: DB is in controller (not in logic), so DB-related code
        is here too.
    '''
    def get_dics(self,Block=False,Phrases=False):
        f = '[MClient] mclient.Commands.get_dics'
        new_dics = []
        dics = objs.get_blocksdb().get_dics(Block)
        if dics:
            dics = [item[0] for item in dics]
            for dic in dics:
                items = dic.split(', ')
                new_dics += items
            new_dics = [item.strip() for item in new_dics \
                        if item.strip()
                       ]
            new_dics = sorted(set(new_dics))
            if not Phrases:
                phdic = objs.blocksdb.get_phdic()
                if phdic:
                    try:
                        new_dics.remove(phdic[1])
                    except ValueError:
                        mes = _('Wrong input data: "{}"!')
                        mes = mes.format(phdic[1])
                        sh.objs.get_mes(f,mes,True).show_warning()
        else:
            sh.com.rep_empty(f)
        return new_dics
        
    def export_style(self):
        f = '[MClient] mclient.Commands.export_style'
        ''' Do not use 'gettext' to name internal types - this will make
            the program ~0,6s slower.
        '''
        lst = [choice for choice in (sh.lg.globs['str']['col1_type']
                                    ,sh.lg.globs['str']['col2_type']
                                    ,sh.lg.globs['str']['col3_type']
                                    ,sh.lg.globs['str']['col4_type']
                                    ) \
               if choice != _('Do not set')
              ]
        ''' #NOTE: The following assignment does not change the list:
            for item in lst:
                if item == something:
                    item = something_else
        '''
        for i in range(len(lst)):
            ''' #cur 'Dictionaries' are kept in order to comply with
                the old config.
            '''
            if lst[i] in (_('Subjects'),_('Dictionaries')):
                lst[i] = 'dic'
            elif lst[i] == _('Word forms'):
                lst[i] = 'wform'
            elif lst[i] == _('Parts of speech'):
                lst[i] = 'speech'
            elif lst[i] == _('Transcription'):
                lst[i] = 'transc'
            else:
                sub = (_('Subjects'),_('Word forms'),_('Transcription')
                      ,_('Parts of speech')
                      )
                sub = '; '.join(sub)
                mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
                mes = mes.format(lst[i],sub)
                sh.objs.get_mes(f,mes).show_error()
        if lst:
            lg.objs.get_request().cols = tuple(lst)
        else:
            sh.com.rep_lazy(f)
    
    def get_prioritized(self):
        f = '[MClient] mclient.Commands.get_prioritized'
        prioritized = objs.get_blocksdb().get_prioritized()
        if prioritized:
            prioritized = ', '.join(prioritized)
            prioritized = prioritized.split(', ')
            prioritized = set(prioritized)
            mes = '; '.join(prioritized)
            sh.objs.get_mes(f,mes,True).show_debug()
            return prioritized
        else:
            return []
    
    def get_skipped_dics(self):
        f = '[MClient] mclient.Commands.get_skipped_dics'
        skipped = objs.get_blocksdb().get_skipped_dics()
        if skipped:
            skipped = ', '.join(skipped)
            skipped = skipped.split(', ')
            skipped = sorted(set(skipped))
            mes = '; '.join(skipped)
            sh.objs.get_mes(f,mes,True).show_debug()
            return skipped
        else:
            return []
    
    def get_skipped_terms(self):
        f = '[MClient] mclient.Commands.get_skipped_terms'
        skipped = objs.get_blocksdb().get_skipped_terms()
        if skipped:
            # TERM can be empty for some reason
            skipped = [item for item in skipped if item]
            # We already use 'distinct' in DB, no need to use 'set'
            skipped.sort()
            mes = '; '.join(skipped)
            sh.objs.get_mes(f,mes,True).show_debug()
            return skipped
        else:
            return []



class UpdateSettingsUI:
    
    def __init__(self):
        self.gui = objs.get_settings_ui()
    
    def update_style_area(self):
        self.gui.opt_scm.set(sh.lg.globs['str']['style'])
        self.gui.opt_cl1.set(sh.lg.globs['str']['col1_type'])
        self.gui.opt_cl2.set(sh.lg.globs['str']['col2_type'])
        self.gui.opt_cl3.set(sh.lg.globs['str']['col3_type'])
        self.gui.opt_cl4.set(sh.lg.globs['str']['col4_type'])
    
    def update_speech_area(self):
        self.gui.opt_sp1.set(sh.lg.globs['str']['speech1'])
        self.gui.opt_sp2.set(sh.lg.globs['str']['speech2'])
        self.gui.opt_sp3.set(sh.lg.globs['str']['speech3'])
        self.gui.opt_sp4.set(sh.lg.globs['str']['speech4'])
        self.gui.opt_sp5.set(sh.lg.globs['str']['speech5'])
        self.gui.opt_sp6.set(sh.lg.globs['str']['speech6'])
        self.gui.opt_sp7.set(sh.lg.globs['str']['speech7'])
    
    def update_checkboxes(self):
        self.gui.cbx_no1.set(sh.lg.globs['bool']['SortByColumns'])
        self.gui.cbx_no2.set(sh.lg.globs['bool']['AlphabetizeTerms'])
        self.gui.cbx_no3.set(sh.lg.globs['bool']['BlockSubjects'])
        self.gui.cbx_no4.set(sh.lg.globs['bool']['PrioritizeSubjects'])
        self.gui.cbx_no5.set(sh.lg.globs['bool']['VerticalView'])
        self.gui.cbx_no6.set(sh.lg.globs['bool']['ShortSubjects'])
        self.gui.cbx_no7.set(sh.lg.globs['bool']['ShortSpeech'])
        self.gui.cbx_no8.set(sh.lg.globs['bool']['ShowUserNames'])
        self.gui.cbx_no9.set(sh.lg.globs['bool']['SelectTermsOnly'])
        self.gui.cbx_no10.set(sh.lg.globs['bool']['Iconify'])
        self.gui.cbx_no11.set(sh.lg.globs['bool']['Autocompletion'])
        self.gui.cbx_no12.set(sh.lg.globs['bool']['Autoswap'])
        self.gui.cbx_no13.set(sh.lg.globs['bool']['PhraseCount'])
    
    def run(self):
        self.update_style_area()
        self.update_speech_area()
        self.update_checkboxes()



class UpdateWebFrameUI:
    
    def __init__(self):
        self.gui = objs.get_webframe_ui()
    
    def restore(self):
        ''' Set widget values to those autosave values that were not
            previously restored by other procedures.
        '''
        f = '[MClient] mclient.UpdateWebFrameUI.restore'
        mes = _('Restore source language: {}')
        mes = mes.format(sh.lg.globs['str']['lang1'])
        sh.objs.get_mes(f,mes,True).show_info()
        lg.objs.get_plugins().set_lang1(sh.lg.globs['str']['lang1'])
        mes = _('Restore target language: {}')
        mes = mes.format(sh.lg.globs['str']['lang2'])
        sh.objs.get_mes(f,mes,True).show_info()
        lg.objs.plugins.set_lang2(sh.lg.globs['str']['lang2'])
        objs.get_webframe().reset_opt()
        self.gui.opt_src.set(sh.lg.globs['str']['source'])
        self.gui.opt_col.set(sh.lg.globs['int']['colnum'])
    
    def _update_alphabet_image(self):
        if sh.lg.globs['bool']['AlphabetizeTerms'] \
        and not lg.objs.request.SpecialPage:
            self.gui.btn_alp.activate()
        else:
            self.gui.btn_alp.inactivate()
    
    def _update_alphabet_hint(self):
        mes = [_('Sort terms by alphabet')]
        if sh.lg.globs['bool']['AlphabetizeTerms']:
            mes.append(_('Status: ON'))
        else:
            mes.append(_('Status: OFF'))
        if lg.objs.request.SpecialPage:
            mes.append(_('This page is not supported'))
        self.gui.btn_alp.hint = '\n'.join(mes)
        self.gui.btn_alp.set_hint()
    
    def _update_alphabetization(self):
        self._update_alphabet_image()
        self._update_alphabet_hint()
    
    def _update_vertical_view(self):
        mes = [_('Vertical mode')]
        if sh.lg.globs['bool']['VerticalView']:
            self.gui.btn_viw.inactivate()
            mes.append(_('Status: ON'))
        else:
            self.gui.btn_viw.activate()
            mes.append(_('Status: OFF'))
        self.gui.btn_viw.hint = '\n'.join(mes)
        self.gui.btn_viw.set_hint()
    
    def _update_global_hotkey(self):
        mes = [_('Capture Ctrl-c-c and Ctrl-Ins-Ins')]
        if sh.lg.globs['bool']['CaptureHotkey']:
            self.gui.btn_cap.activate()
            mes.append(_('Status: ON'))
        else:
            self.gui.btn_cap.inactivate()
            mes.append(_('Status: OFF'))
        self.gui.btn_cap.hint = '\n'.join(mes)
        self.gui.btn_cap.set_hint()
    
    def _update_prioritization(self):
        mes = [_('Subject prioritization')]
        prioritized = com.get_prioritized()
        if sh.lg.globs['bool']['PrioritizeSubjects'] and prioritized \
        and not lg.objs.request.SpecialPage:
            self.gui.btn_pri.activate()
        else:
            self.gui.btn_pri.inactivate()
        if sh.lg.globs['bool']['PrioritizeSubjects']:
            mes.append(_('Status: ON'))
        else:
            mes.append(_('Status: OFF'))
        if lg.objs.request.SpecialPage:
            sub = _('This page is not supported')
        elif prioritized:
            sub = _('{} subjects were prioritized')
            sub = sub.format(len(prioritized))
        else:
            sub = _('Nothing to prioritize')
        mes.append(sub)
        self.gui.btn_pri.hint = '\n'.join(mes)
        self.gui.btn_pri.set_hint()
    
    def _update_block(self):
        f = '[MClient] UpdateWebFrameUI._update_block'
        mes = [_('Subject blocking')]
        skipped_terms = len(com.get_skipped_terms())
        skipped_dics = len(com.get_skipped_dics())
        if sh.lg.globs['bool']['BlockSubjects'] and skipped_terms:
            self.gui.btn_blk.activate()
        else:
            self.gui.btn_blk.inactivate()
        if sh.lg.globs['bool']['BlockSubjects']:
            mes.append(_('Status: ON'))
        else:
            mes.append(_('Status: OFF'))
        ''' If this does not work as expected, then TERM might not be
            filled properply.
        '''
        if sh.lg.globs['bool']['BlockSubjects'] and skipped_terms:
            sub = _('Skipped {} terms in {} subjects')
            sub = sub.format(skipped_terms,skipped_dics)
        else:
            sub = _('Nothing was blocked')
        mes.append(sub)
        self.gui.btn_blk.hint = '\n'.join(mes)
        self.gui.btn_blk.set_hint()
    
    def _update_go_next(self):
        if objs.blocksdb.get_next_id(Loop=False):
            self.gui.btn_nxt.activate()
        else:
            self.gui.btn_nxt.inactivate()
    
    def _update_go_prev(self):
        # Update the button to move to the previous article
        if objs.get_blocksdb().get_prev_id(Loop=False):
            self.gui.btn_prv.activate()
        else:
            self.gui.btn_prv.inactivate()
    
    def _update_last_search(self,searches):
        # Update the button to insert a current search string
        if searches:
            self.gui.btn_rp1.activate()
        else:
            self.gui.btn_rp1.inactivate()
    
    def _update_prev_search(self,searches):
        # Update the button to insert a previous search string
        if searches and len(searches) > 1:
            self.gui.btn_rp2.activate()
        else:
            self.gui.btn_rp2.inactivate()
    
    def update_buttons(self):
        f = '[MClient] mclient.UpdateWebFrame.update_buttons'
        searches = objs.get_blocksdb().get_searches()
        self._update_last_search(searches)
        self._update_prev_search(searches)
        # Suppress useless error output
        if lg.objs.get_request().search:
            self._update_go_prev()
            self._update_go_next()
            self._update_block()
            self._update_prioritization()
        else:
            sh.com.rep_lazy(f)
        self._update_global_hotkey()
        self._update_vertical_view()
        self._update_alphabetization()
    
    def run(self):
        self.update_buttons()



class Sources:
    
    def __init__(self):
        f = '[MClient] mclient.Sources.__init__'
        self.set_values()
        sources = lg.objs.get_plugins().get_sources()
        if sources:
            self.sources = sources
        else:
            self.Success = False
            sh.com.rep_empty(f)
        self.gui = None
    
    def set_gui(self):
        self.gui = gi.Sources()
        self.set_bindings()
    
    def get_gui(self):
        if self.gui is None:
            self.set_gui()
        return self.gui
    
    def reset(self):
        self.set_values()
        self.get_gui().reset(self.sources)
    
    def set_values(self):
        self.select = []
        self.sources = []
        self.Success = True
    
    def get_sel(self):
        f = '[MClient] mclient.Sources.get_sel'
        if self.Success:
            for i in range(len(self.get_gui().cboxes)):
                if self.gui.cboxes[i].get():
                    try:
                        self.select.append(self.sources)
                    except IndexError:
                        self.Success = False
                        mes = _('Wrong input data!')
                        sh.objs.get_mes(f,mes).show_error()
            return self.select
        else:
            sh.com.cancel(f)
    
    def set_bindings(self):
        self.get_gui().btn_apl.action = self.apply
    
    def show(self,event=None):
        self.get_gui().show()
    
    def apply(self,event=None):
        #TODO: What is a purpose of this?
        f = '[MClient] mclient.Sources.apply'
        mes = self.get_sel()
        sh.objs.get_mes(f,mes,True).show_debug()
    
    def close(self,event=None):
        self.get_gui().close()



class Objects:

    def __init__(self):
        ''' #NOTE: Do not use 'super' to integrate with 'logic.Objects',
            since we modify some logic attributes in the controller,
            and, in case of integration, such changes will not be
            reflected in 'logic.Objects'.
        '''
        self.webframe = self.blocksdb = self.about = self.settings \
                      = self.search = self.symbols = self.save \
                      = self.history = self.suggest = self.parties \
                      = self.webframe_ui = self.settings_ui \
                      = self.priorities = self.blacklist = None

    def get_blacklist(self):
        if self.blacklist is None:
            self.blacklist = bl.Blacklist(func_group=lg.objs.get_plugins().get_group)
        return self.blacklist
    
    def get_priorities(self):
        if self.priorities is None:
            self.priorities = pr.Priorities(func_group=lg.objs.get_plugins().get_group)
        return self.priorities
    
    def get_parties(self):
        if self.parties is None:
            self.parties = tp.ThirdParties()
        return self.parties
    
    def get_suggest(self):
        if self.suggest is None:
            self.suggest = Suggest(entry=self.get_webframe().gui.ent_src)
        return self.suggest
    
    def get_history(self):
        if self.history is None:
            self.history = History()
        return self.history
    
    def get_save(self):
        if self.save is None:
            self.save = SaveArticle()
        return self.save
    
    def get_symbols(self):
        if self.symbols is None:
            self.symbols = sh.SymbolMap (items = sh.lg.globs['str']['spec_syms']
                                        ,icon = gi.ICON
                                        )
        return self.symbols
    
    def get_search(self):
        if self.search is None:
            self.search = SearchArticle()
        return self.search
    
    def get_settings(self):
        if self.settings is None:
            self.settings = Settings()
        return self.settings
    
    def get_about(self):
        if self.about is None:
            self.about = About()
        return self.about
    
    def get_blocksdb(self):
        ''' #NOTE: Do not move this function to 'logic.Objects', since
            we modify attributes of the present object in
            the controller, and, in case of moving, such changes
            will not be reflected in 'logic.Objects'.
        '''
        if self.blocksdb is None:
            self.blocksdb = db.Moves()
            self.blocksdb.Selectable = sh.lg.globs['bool']['SelectTermsOnly']
        return self.blocksdb

    def get_webframe(self):
        if self.webframe is None:
            self.webframe = WebFrame()
        return self.webframe
    
    def get_settings_ui(self):
        if self.settings_ui is None:
            self.settings_ui = self.get_settings().get_gui()
        return self.settings_ui
    
    def get_webframe_ui(self):
        if self.webframe_ui is None:
            self.webframe_ui = self.get_webframe().gui
        return self.webframe_ui



def call_app():
    # Use the same key binding to call the window
    sh.Geometry(objs.get_webframe().gui.obj).activate(MouseClicked=lg.objs.get_request().MouseClicked)
    ''' #TODO: check if this is still the problem
        In case of .focus_set() *first* Control-c-c can call an inactive
        widget.
    '''
    objs.get_webframe().gui.ent_src.widget.focus_force()

def run_timed_update():
    # Capture Control-c-c
    lg.objs.get_request().MouseClicked = False
    check = kl.keylistener.check()
    if check:
        if check == 1 and sh.lg.globs['bool']['CaptureHotkey']:
            # Prevent thread freezing in Windows newer than XP
            if sh.objs.get_os().is_win():
                kl.keylistener.cancel()
                kl.keylistener.restart()
            lg.objs.request.MouseClicked = True
            new_clipboard = sh.Clipboard().paste()
            if new_clipboard:
                lg.objs.request.search = new_clipboard
                objs.get_webframe().go_search()
        if check == 2 or sh.lg.globs['bool']['CaptureHotkey']:
            call_app()
    sh.objs.get_root().widget.after(300,run_timed_update)



class SaveArticle:

    def __init__(self):
        self.webtypes = ((_('Web-page'),'.htm')
                         ,(_('Web-page'),'.html')
                         ,(_('All files'),'*')
                        )
        self.txttypes = ((_('Plain text (UTF-8)'),'.txt')
                         ,(_('All files'),'*')
                        )
        self.gui = None
        self.Active = False
    
    def show(self,event=None):
        self.Active = True
        self.get_gui().show()
    
    def close(self,event=None):
        self.Active = False
        self.get_gui().close()
    
    def toggle(self,event=None):
        if self.Active:
            self.close()
        else:
            self.show()
    
    def get_gui(self):
        if self.gui is None:
            self.set_gui()
        return self.gui
    
    def set_gui(self):
        self.gui = gi.SaveArticle()
        self.set_bindings()
    
    def set_bindings(self):
        sh.com.bind (obj = self.get_gui()
                    ,bindings = [sh.lg.globs['str']['bind_save_article']
                                ,sh.lg.globs['str']['bind_save_article_alt']
                                ]
                    ,action = self.toggle
                    )
        sh.com.bind (obj = self.gui
                    ,bindings = ('<<ListboxSelect>>','<Return>'
                                ,'<KP_Enter>'
                                )
                    ,action = self.select
                    )
        self.gui.parent.btn_sav.action = self.select
    
    def fix_ext(self,ext='.htm'):
        if not self.file.endswith(ext):
            self.file += ext

    def select(self,event=None):
        f = '[MClient] mclient.SaveArticle.select'
        self.get_gui().parent.save()
        opt = self.gui.parent.get()
        if opt:
            if opt == _('Save the current view as a web-page (*.htm)'):
                self.save_view_as_htm()
            elif opt == _('Save the original article as a web-page (*.htm)'):
                self.save_raw_as_htm()
            elif opt == _('Save the article as plain text in UTF-8 (*.txt)'):
                self.save_view_as_txt()
            elif opt == _('Copy the code of the article to clipboard'):
                self.copy_raw()
            elif opt == _('Copy the text of the article to clipboard'):
                self.copy_txt()
        else:
            mes = _('Operation has been canceled by the user.')
            sh.objs.get_mes(f,mes,True).show_info()

    def save_view_as_htm(self):
        f = '[MClient] mclient.SaveArticle.save_view_as_htm'
        self.file = sh.com.show_save_dialog(self.webtypes)
        if self.file and lg.objs.get_request().htm:
            self.fix_ext('.htm')
            code = lg.objs.request.htm
            code = wb.WebPage(code).make_pretty()
            ''' We enable 'Rewrite' because the confirmation is already
                built in the internal dialog.
            '''
            sh.WriteTextFile (file = self.file
                             ,Rewrite = True
                             ).write(code)
        else:
            sh.com.rep_empty(f)

    def save_raw_as_htm(self):
        f = '[MClient] mclient.SaveArticle.save_raw_as_htm'
        ''' Key 'html' may be needed to write a file in the UTF-8
            encoding, therefore, in order to ensure that the web-page
            is read correctly, we change the encoding manually. We also
            replace abbreviated hyperlinks with full ones in order to
            ensure that they are also valid in the local file.
        '''
        self.file = sh.com.show_save_dialog(self.webtypes)
        code = objs.get_blocksdb().get_code()
        if self.file and code:
            self.fix_ext('.htm')
            lg.objs.get_plugins().set_htm(code)
            code = lg.objs.plugins.fix_raw_htm()
            sh.WriteTextFile (file = self.file
                             ,Rewrite = True
                             ).write(code)
        else:
            sh.com.rep_empty(f)

    def save_view_as_txt(self):
        f = '[MClient] mclient.SaveArticle.save_view_as_txt'
        self.file = sh.com.show_save_dialog(self.txttypes)
        text = objs.get_webframe().get_text()
        if self.file and text:
            self.fix_ext('.txt')
            sh.WriteTextFile (file = self.file
                             ,Rewrite = True
                             ).write(text.strip())
        else:
            sh.com.rep_empty(f)

    def copy_raw(self):
        sh.Clipboard().copy(objs.get_blocksdb().get_code())

    def copy_txt(self):
        f = '[MClient] mclient.SaveArticle.copy_txt'
        text = objs.get_webframe().get_text()
        if text:
            sh.Clipboard().copy(text.strip())
        else:
            sh.com.rep_empty(f)



class SearchArticle:
    # Search IN an article
    def __init__(self):
        self.gui = None
        self.reset()
    
    def get_gui(self):
        if self.gui is None:
            self.set_gui()
            self.gui.center()
        return self.gui
    
    def set_gui(self):
        self.gui = gi.SearchArticle()
        self.set_bindings()

    def set_bindings(self):
        sh.com.bind (obj = self.get_gui()
                    ,bindings = sh.lg.globs['str']['bind_search_article_forward']
                    ,action = self.gui.close
                    )
    
    def reset(self,event=None):
        self.pos = -1
        self.last = -1
        self.first = -1
        self.pattern = ''

    def clear(self,event=None):
        self.get_gui().parent.clear_text()

    def close(self,event=None):
        self.get_gui().close()

    def insert(self,event=None):
        self.gui.insert(self.pattern)
    
    def show(self,event=None):
        self.get_gui().focus()
        self.gui.show()

    def search(self):
        if not self.pattern:
            self.show()
            self.pattern = self.get_gui().parent.get()
            self.pattern = self.pattern.strip(' ').strip('\n').lower()
        return self.pattern

    def get_next(self,event=None):
        f = '[MClient] mclient.SearchArticle.get_next'
        pos = objs.get_blocksdb().search_next (pos = self.pos
                                              ,search = self.search()
                                              )
        if pos or pos == 0:
            objs.get_webframe().pos = self.pos = pos
            objs.webframe.select()
            objs.webframe.shift_screen()
        elif self.pos < 0:
            mes = _('No matches!')
            sh.objs.get_mes(f,mes).show_info()
        else:
            mes = _('The end has been reached. Searching from the start.')
            sh.objs.get_mes(f,mes).show_info()
            self.pos = 0
            self.get_next()

    def get_first(self):
        if self.first == -1:
            self.first = \
            objs.get_blocksdb().search_next (pos = -1
                                            ,search = self.search()
                                            )
        return self.first

    def get_last(self):
        f = '[MClient] mclient.SearchArticle.get_last'
        if self.last == -1:
            max_cell = objs.blocksdb.get_max_cell()
            if max_cell:
                self.last = \
                objs.get_blocksdb().search_prev (pos = max_cell[2]+1
                                                ,search = self.search()
                                                )
            else:
                sh.com.rep_empty(f)
        return self.last

    def get_prev(self,event=None):
        f = '[MClient] mclient.SearchArticle.get_prev'
        if self.get_first():
            if self.pos == self.first:
                mes = _('The start has been reached. Searching from the end.')
                sh.objs.get_mes(f,mes).show_info()
                result = self.get_last()
                if str(result).isdigit():
                    objs.get_webframe().pos = self.pos = result
                    objs.webframe.select()
                    objs.webframe.shift_screen()
            else:
                pos = \
                objs.get_blocksdb().search_prev (pos = self.pos
                                                ,search = self.search()
                                                )
                if str(pos).isdigit():
                    self.pos = pos
                    objs.get_webframe().pos = pos
                    objs.webframe.select()
                    objs.webframe.shift_screen()
        else:
            mes = _('No matches!')
            sh.objs.get_mes(f,mes).show_info()



class History:

    def __init__(self):
        self.Active = False
        self.gui = None
    
    def toggle(self,event=None):
        if self.Active:
            self.close()
        else:
            self.show()
    
    def get_gui(self):
        if self.gui is None:
            self.set_gui()
        return self.gui
    
    def set_gui(self):
        self.gui = gi.History()
        self.gui.obj.action = self.go
        self.set_bindings()

    def set_bindings(self):
        sh.com.bind (obj = self.get_gui()
                    ,bindings = [sh.lg.globs['str']['bind_toggle_history']
                                ,sh.lg.globs['str']['bind_toggle_history_alt']
                                ]
                    ,action = self.toggle
                    )
        sh.com.bind (obj = self.gui
                    ,bindings = sh.lg.globs['str']['bind_clear_history']
                    ,action = self.clear
                    )
        ''' #NOTE: the list is reversed, but I think it is still more
            intuitive when Home goes top and End goes bottom.
        '''
        sh.com.bind (obj = self.gui
                    ,bindings = '<Home>'
                    ,action = self.go_first
                    )
        sh.com.bind (obj = self.gui
                    ,bindings = '<End>'
                    ,action = self.go_last
                    )
        self.gui.action = self.go

    def autoselect(self):
        self.get_gui().obj.clear_sel()
        item = str(objs.get_blocksdb().artid) \
               + ' ► ' + lg.objs.get_request().search
        self.gui.obj.set(item=item)

    def show(self,event=None):
        self.Active = True
        self.update()
        self.get_gui().show()

    def close(self,event=None):
        self.Active = False
        self.get_gui().close()

    def fill(self):
        searches = objs.get_blocksdb().get_searches()
        lst = []
        if searches:
            for item in searches:
                lst.append(str(item[0]) + ' ► ' + str(item[1]))
            self.get_gui().obj.reset(lst=lst)

    def update(self):
        self.fill()
        self.autoselect()

    def clear(self,event=None):
        objs.get_blocksdb().clear()
        objs.get_webframe().reset()
        lg.objs.get_request().reset()

    def go_first(self,event=None):
        f = '[MClient] mclient.History.go_first'
        if self.get_gui().obj.lst:
            self.gui.obj.clear_sel()
            self.gui.obj.set(item=self.gui.obj.lst[0])
            self.go()
        else:
            sh.com.rep_empty(f)
        
    def go_last(self,event=None):
        f = '[MClient] mclient.History.go_last'
        if self.get_gui().obj.lst:
            self.gui.obj.clear_sel()
            self.gui.obj.set(item=self.gui.obj.lst[-1])
            self.go()
        else:
            sh.com.rep_empty(f)
    
    def go(self,event=None):
        f = '[MClient] mclient.History.go'
        result = self.get_gui().obj.get()
        result = result.split(' ► ')
        if len(result) == 2:
            objs.get_blocksdb().artid = int(result[0])
            result = objs.blocksdb.get_article()
            if result:
                sh.lg.globs['str']['source'] = result[0] # SOURCE
                lg.objs.request.search = result[1] # TITLE
                lg.objs.request.url = result[2] # URL
                mes = _('Set source to "{}"')
                mes = mes.format(sh.lg.globs['str']['source'])
                sh.objs.get_mes(f,mes,True).show_info()
                lg.objs.get_plugins().set(sh.lg.globs['str']['source'])
                lg.objs.plugins.set_lang1(result[4])
                lg.objs.plugins.set_lang2(result[5])
                objs.webframe.reset_opt(sh.lg.globs['str']['source'])
                ''' #NOTE: Do not use wrapper procedures such as
                    'objs.webframe.go_url' (modifies
                    'lg.objs.request.search') and
                    'objs.webframe.go_search' (modifies
                    'lg.objs.request.url').
                '''
                objs.webframe.load_article()
            else:
                sh.com.rep_empty(f)
        else:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f,mes).show_error()



class WebFrame:

    def __init__(self):
        self.set_values()
        self.gui = gi.WebFrame()
        self.set_bindings()
    
    def debug_settings(self):
        # Use 'import debug_gui as gi' instead of 'import gui as gi'
        f = '[MClient] mclient.WebFrame.debug_settings'
        try:
            mes = []
            # WebFrame
            sub = objs.get_webframe_ui().debug()
            mes.append(sub)
            mes.append('')
            # GUI Settings
            sub = objs.get_settings_ui().debug()
            mes.append(sub)
            mes.append('')
            # Keys
            sub = sh.com.debug_globs()
            mes.append(sub)
            mes = '\n'.join(mes)
            sh.com.run_fast_debug(f,mes)
        except AttributeError:
            mes = _('Please import "{}" instead of "{}"')
            mes = mes.format('debug_gui','gui')
            sh.objs.get_mes(f,mes).show_error()
    
    def update_buttons(self):
        UpdateWebFrameUI().run()
    
    def auto_swap(self):
        f = '[MClient] mclient.WebFrame.auto_swap'
        lang1 = self.gui.opt_lg1.choice
        lang2 = self.gui.opt_lg2.choice
        if sh.lg.globs['bool']['Autoswap'] \
        and not lg.objs.get_plugins().is_oneway() \
        and lg.objs.get_request().search:
            if sh.Text(lg.objs.request.search).has_cyrillic():
                if lang2 in (_('Russian'),'Russian'):
                    mes = '{}-{} -> {}-{}'.format(lang1,lang2,lang2,lang1)
                    sh.objs.get_mes(f,mes,True).show_info()
                    self.swap_langs()
            elif lang1 in (_('Russian'),'Russian'):
                mes = '{}-{} -> {}-{}'.format(lang1,lang2,lang2,lang1)
                sh.objs.get_mes(f,mes,True).show_info()
                self.swap_langs()
        else:
            sh.com.rep_lazy(f)
    
    def run_final_debug(self,event=None):
        f = '[MClient] mclient.WebFrame.run_final_debug'
        if lg.objs.get_plugins().Debug:
            mes = _('Debug table:')
            sh.objs.get_mes(f,mes,True).show_info()
            ''' #NOTE: If all of a sudden you get IGNORE=1, then you
                have probably forgot to add new block types in
                'db.DB.reset'.
            '''
            query = 'select ROWNO,CELLNO,NO,DICPR,TYPE,DIC,DICF,WFORM \
                           ,SPEECH,TERM,SAMECELL,TEXT,BLOCK,IGNORE \
                     from BLOCKS where ARTICLEID = ? order by CELLNO,NO'
            objs.blocksdb.dbc.execute(query,(objs.get_blocksdb().artid,))
            objs.blocksdb.print (mode = 'BLOCKS'
                                ,Selected = 1
                                ,maxrows = lg.objs.plugins.maxrows
                                )
    
    def copy_wform(self,event=None):
        f = '[MClient] mclient.WebFrame.copy_wform'
        wform = objs.get_blocksdb().get_wform(pos=self.pos)
        if wform:
            sh.Clipboard().copy(wform)
            if sh.lg.globs['bool']['Iconify']:
                self.minimize()
        else:
            sh.com.rep_empty(f)
    
    def show(self,event=None):
        self.gui.show()
    
    def close(self,event=None):
        self.gui.close()
    
    def suggest_bottom(self,event=None):
        objs.get_suggest().move_bottom()
    
    def suggest_top(self,event=None):
        objs.get_suggest().move_top()
    
    def suggest_down(self,event=None):
        objs.get_suggest().move_down()
    
    def suggest_up(self,event=None):
        objs.get_suggest().move_up()
    
    def suggest_show(self,event=None):
        objs.get_suggest().suggest(event)
    
    def clear_history(self,event=None):
        objs.get_history().clear()
    
    def toggle_history(self,event=None):
        objs.get_history().toggle()
    
    def toggle_save(self,event=None):
        objs.get_save().toggle()
    
    def search_prev(self,event=None):
        objs.get_search().get_prev()
    
    def search_next(self,event=None):
        objs.get_search().get_next()
    
    def toggle_settings(self,event=None):
        objs.get_settings().toggle()
    
    def toggle_about(self,event=None):
        objs.get_about().toggle()
    
    def insert_sym(self,event=None):
        objs.get_symbols().show()
        self.gui.ent_src.insert (pos = 'end'
                                ,text = objs.symbols.get()
                                )
    
    def update_lang1(self,event=None):
        f = '[MClient] mclient.WebFrame.update_lang1'
        self.set_lang1()
        self.set_lang2()
        lang1 = lg.objs.get_plugins().get_lang1()
        lang2 = lg.objs.plugins.get_lang2()
        langs1 = lg.objs.plugins.get_langs1()
        if langs1:
            self.gui.opt_lg1.set(lang1)
            self.set_lang1()
        else:
            sh.com.rep_empty(f)
    
    def update_lang2(self,event=None):
        f = '[MClient] mclient.WebFrame.update_lang2'
        self.set_lang1()
        self.set_lang2()
        lang1 = lg.objs.get_plugins().get_lang1()
        lang2 = lg.objs.plugins.get_lang2()
        langs2 = lg.objs.plugins.get_langs2(lang1)
        if langs2:
            if not lang2 in langs2:
                lang2 = langs2[0]
            self.gui.opt_lg2.reset (items = langs2
                                   ,default = lang2
                                   ,action = self.go_search_focus
                                   )
            self.set_lang2()
        else:
            sh.com.rep_empty(f)
    
    def swap_langs(self,event=None):
        f = '[MClient] mclient.WebFrame.swap_langs'
        if lg.objs.get_plugins().is_oneway():
            mes = _('Cannot swap languages, this is a one-way dictionary!')
            sh.objs.get_mes(f,mes).show_info()
        else:
            self.update_lang1()
            self.update_lang2()
            lang1 = self.gui.opt_lg1.choice
            lang2 = self.gui.opt_lg2.choice
            lang1, lang2 = lang2, lang1
            langs1 = lg.objs.get_plugins().get_langs1()
            langs2 = lg.objs.plugins.get_langs2(lang1)
            if langs1:
                if langs2 and lang1 in langs1 and lang2 in langs2:
                    self.gui.opt_lg1.reset (items = langs1
                                           ,default = lang1
                                           ,action = self.go_search_focus
                                           )
                    self.gui.opt_lg2.reset (items = langs2
                                           ,default = lang2
                                           ,action = self.go_search_focus
                                           )
                    self.update_lang1()
                    self.update_lang2()
                else:
                    mes = _('Pair {}-{} is not supported!')
                    mes = mes.format(lang1,lang2)
                    sh.objs.get_mes(f,mes).show_warning()
            else:
                sh.com.rep_empty(f)
    
    def set_next_lang1(self,event=None):
        ''' We want to navigate through the full list of supported
            languages rather than through the list of 'lang2' pairs
            so we reset the widget first.
        '''
        self.gui.opt_lg1._get()
        old = self.gui.opt_lg1.choice
        self.gui.opt_lg1.reset (items = lg.objs.get_plugins().get_langs1()
                               ,default = old
                               ,action = self.go_search_focus
                               )
        self.gui.opt_lg1.set_next()
        self.update_lang1()
        self.update_lang2()
    
    def set_next_lang2(self,event=None):
        # We want to navigate through the limited list here
        self.update_lang1()
        self.update_lang2()
        self.gui.opt_lg2.set_next()
        self.update_lang2()
    
    def set_prev_lang1(self,event=None):
        ''' We want to navigate through the full list of supported
            languages rather than through the list of 'lang2' pairs
            so we reset the widget first.
        '''
        self.gui.opt_lg1._get()
        old = self.gui.opt_lg1.choice
        self.gui.opt_lg1.reset (items = lg.objs.get_plugins().get_langs1()
                               ,default = old
                               ,action = self.go_search_focus
                               )
        self.gui.opt_lg1.set_prev()
        self.update_lang1()
        self.update_lang2()
    
    def set_prev_lang2(self,event=None):
        # We want to navigate through the limited list here
        self.update_lang1()
        self.update_lang2()
        self.gui.opt_lg2.set_prev()
        self.update_lang2()
    
    def paste_search_field(self,event=None):
        objs.get_suggest().get_gui().close()
        self.gui.paste_search()
    
    def clear_search_field(self,event=None):
        objs.get_suggest().get_gui().close()
        self.gui.ent_src.clear_text()
        
    def escape(self,event=None):
        if objs.get_suggest().get_gui().parent:
            objs.suggest.gui.close()
        else:
            sh.Geometry(self.gui.obj).minimize()
    
    def minimize(self,event=None):
        objs.get_suggest().get_gui().close()
        sh.Geometry(self.gui.obj).minimize()
    
    def go_phdic(self,event=None):
        f = '[MClient] mclient.WebFrame.go_phdic'
        phdic = objs.get_blocksdb().get_phdic()
        if phdic:
            self.posn = phdic[2]
            if objs.blocksdb.Selectable:
                lg.objs.get_request().search = phdic[1]
                lg.objs.request.url = phdic[3]
                self.load_article()
            else:
                self.go_url()
        else:
            sh.com.rep_empty(f)
    
    def insert_repeat_sign2(self,event=None):
        # Insert the previous search string
        f = '[MClient] mclient.WebFrame.insert_repeat_sign2'
        result = objs.get_blocksdb().get_prev_id()
        if result:
            old = objs.blocksdb.artid
            objs.blocksdb.artid = result
            result = objs.blocksdb.get_article()
            if result:
                sh.Clipboard().copy(result[1])
                self.gui.paste_search()
            else:
                sh.com.rep_empty(f)
            objs.blocksdb.artid = old
        else:
            sh.com.rep_empty(f)
    
    def insert_repeat_sign(self,event=None):
        # Insert the current search string
        sh.Clipboard().copy(lg.objs.get_request().search)
        self.gui.paste_search()
        
    def reset(self):
        #'widget.reset' is already done in 'self.fill'
        welcome = lg.Welcome (product = gi.PRODUCT
                             ,version = gi.VERSION
                             )
        self.fill(welcome.run())
        self.update_buttons()
        UpdateWebFrameUI().restore()
        com.export_style()
        self.set_title()
        ''' We should ensure that a number of columns is based on
            a GUI value instead of relying on a default 'lg.CurRequest'
            value. This is especially needed when the column limit
            value is preset, for example, is read from a config file.
        '''
        self.reset_columns()

    def set_values(self):
        self.pos = -1
        self.posn = -1
        self.phdic = ''

    def go_search_focus(self,event=None):
        ''' Setting the focus explicitly can be useful in case of
            activating OptionMenus. Otherwise, it's preferred not to
            explicitly set the focus since loading an article may be
            triggered by History which should remain active.
        '''
        self.go_search()
        self.gui.ent_src.focus()
    
    def reset_opt(self,default=_('Multitran')):
        f = '[MClient] mclient.WebFrame.reset_opt'
        # Reset OptionMenus
        lang1 = lg.objs.get_plugins().get_lang1()
        lang2 = lg.objs.plugins.get_lang2()
        langs1 = lg.objs.plugins.get_langs1()
        langs2 = lg.objs.plugins.get_langs2(lang1)
        sources = lg.objs.plugins.get_sources()
        if langs1 and langs2 and lang1 and lang2 and sources:
            self.gui.opt_lg1.reset (items = langs1
                                   ,default = lang1
                                   ,action = self.go_search_focus
                                   )
            self.gui.opt_lg2.reset (items = langs2
                                   ,default = lang2
                                   ,action = self.go_search_focus
                                   )
            #NOTE: change this upon the change of the default source
            self.gui.opt_src.reset (items = sources
                                   ,action = self.set_source
                                   ,default = default
                                   )
        else:
            sh.com.rep_empty(f)
    
    def set_bindings(self):
        # 'gui.obj.widget' is 'Toplevel'; 'gui.widget' is 'TkinterHtml'
        sh.com.bind (obj = self.gui.obj
                    ,bindings = sh.lg.globs['str']['bind_copy_nominative']
                    ,action = self.copy_wform
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = sh.lg.globs['str']['bind_swap_langs']
                    ,action = self.swap_langs
                    )
        sh.com.bind (obj = self.gui.opt_lg1
                    ,bindings = ('<Return>'
                                ,'<KP_Enter>'
                                )
                    ,action = self.go_search_focus
                    )
        sh.com.bind (obj = self.gui.opt_lg2
                    ,bindings = ('<Return>'
                                ,'<KP_Enter>'
                                )
                    ,action = self.go_search_focus
                    )
        sh.com.bind (obj = self.gui.opt_src
                    ,bindings = ('<Return>'
                                ,'<KP_Enter>'
                                )
                    ,action = self.set_source
                    )
        sh.com.bind (obj = self.gui.opt_col
                    ,bindings = ('<Return>'
                                ,'<KP_Enter>'
                                )
                    ,action = self.set_columns
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = sh.lg.globs['str']['bind_quit']
                    ,action = self.gui.close
                    )
        sh.com.bind (obj = self.gui.ent_src
                    ,bindings = (sh.lg.globs['str']['bind_copy_sel']
                                ,sh.lg.globs['str']['bind_copy_sel_alt']
                                )
                    ,action = self.copy_text
                    )
        sh.com.bind (obj = self.gui
                    ,bindings = '<Button-1>'
                    ,action = self.go_url
                    )
        sh.com.bind (obj = self.gui.ent_src
                    ,bindings = ('<Return>'
                                ,'<KP_Enter>'
                                )
                    ,action = self.go_keyboard
                    )
        sh.com.bind (obj = self.gui.ent_src
                    ,bindings = sh.lg.globs['str']['bind_clear_search_field']
                    ,action = self.gui.ent_src.clear_text
                    )
        sh.com.bind (obj = self.gui.ent_src
                    ,bindings = sh.lg.globs['str']['bind_paste_search_field']
                    ,action = lambda e:self.gui.paste_search()
                    )
        # Go to the previous/next article
        sh.com.bind (obj = self.gui.obj
                    ,bindings = sh.lg.globs['str']['bind_go_back']
                    ,action = self.go_back
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = sh.lg.globs['str']['bind_go_forward']
                    ,action = self.go_forward
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = sh.lg.globs['str']['bind_col1_down']
                    ,action = lambda e:self.move_next_section(col_no=0)
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = sh.lg.globs['str']['bind_col1_up']
                    ,action = lambda e:self.move_prev_section(col_no=0)
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = sh.lg.globs['str']['bind_col2_down']
                    ,action = lambda e:self.move_next_section(col_no=1)
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = sh.lg.globs['str']['bind_col2_up']
                    ,action = lambda e:self.move_prev_section(col_no=1)
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = sh.lg.globs['str']['bind_col3_down']
                    ,action = lambda e:self.move_next_section(col_no=2)
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = sh.lg.globs['str']['bind_col3_up']
                    ,action = lambda e:self.move_prev_section(col_no=2)
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = sh.lg.globs['str']['bind_go_phrases']
                    ,action = self.go_phdic
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = sh.lg.globs['str']['bind_search_article_forward']
                    ,action = self.search_next
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = sh.lg.globs['str']['bind_search_article_backward']
                    ,action = self.search_prev
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = sh.lg.globs['str']['bind_re_search_article']
                    ,action = self.search_reset
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = (sh.lg.globs['str']['bind_reload_article']
                                ,sh.lg.globs['str']['bind_reload_article_alt']
                                )
                    ,action = self.reload
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = (sh.lg.globs['str']['bind_save_article']
                                ,sh.lg.globs['str']['bind_save_article_alt']
                                )
                    ,action = self.toggle_save
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = sh.lg.globs['str']['bind_show_about']
                    ,action = self.toggle_about
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = (sh.lg.globs['str']['bind_toggle_history']
                                ,sh.lg.globs['str']['bind_toggle_history']
                                )
                    ,action = self.toggle_history
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = (sh.lg.globs['str']['bind_toggle_history']
                                ,sh.lg.globs['str']['bind_toggle_history_alt']
                                )
                    ,action = self.toggle_history
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = (sh.lg.globs['str']['bind_open_in_browser']
                                ,sh.lg.globs['str']['bind_open_in_browser_alt']
                                )
                    ,action = self.open_in_browser
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = sh.lg.globs['str']['bind_copy_url']
                    ,action = self.copy_block_url
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = sh.lg.globs['str']['bind_copy_article_url']
                    ,action = self.copy_url
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = sh.lg.globs['str']['bind_spec_symbol']
                    ,action = self.insert_sym
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = sh.lg.globs['str']['bind_define']
                    ,action = lambda e:self.define(Selected=True)
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = (sh.lg.globs['str']['bind_prev_lang1']
                                ,sh.lg.globs['str']['bind_prev_lang1_alt']
                                )
                    ,action = self.set_prev_lang1
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = (sh.lg.globs['str']['bind_next_lang1']
                                ,sh.lg.globs['str']['bind_next_lang1_alt']
                                )
                    ,action = self.set_next_lang1
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = (sh.lg.globs['str']['bind_prev_lang2']
                                ,sh.lg.globs['str']['bind_prev_lang2_alt']
                                )
                    ,action = self.set_prev_lang2
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = (sh.lg.globs['str']['bind_next_lang2']
                                ,sh.lg.globs['str']['bind_next_lang2_alt']
                                )
                    ,action = self.set_next_lang2
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = (sh.lg.globs['str']['bind_settings']
                                ,sh.lg.globs['str']['bind_settings_alt']
                                )
                    ,action = self.toggle_settings
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = (sh.lg.globs['str']['bind_toggle_view']
                                ,sh.lg.globs['str']['bind_toggle_view_alt']
                                )
                    ,action = self.toggle_view
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = (sh.lg.globs['str']['bind_toggle_history']
                                ,sh.lg.globs['str']['bind_toggle_history_alt']
                                )
                    ,action = self.toggle_history
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = sh.lg.globs['str']['bind_clear_history']
                    ,action = self.clear_history
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = sh.lg.globs['str']['bind_toggle_alphabet']
                    ,action = self.toggle_alphabet
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = sh.lg.globs['str']['bind_toggle_block']
                    ,action = self.toggle_block
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = sh.lg.globs['str']['bind_toggle_priority']
                    ,action = self.toggle_priority
                    )
        sh.com.bind (obj = self.gui.btn_hst
                    ,bindings = '<ButtonRelease-3>'
                    ,action = self.clear_history
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = sh.lg.globs['str']['bind_print']
                    ,action = self.print
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = sh.lg.globs['str']['bind_toggle_sel']
                    ,action = self.toggle_sel
                    )
        sh.com.bind (obj = self.gui
                    ,bindings = '<Motion>'
                    ,action = self.set_mouse_sel
                    )
        ''' Key and mouse bindings must have different parents,
            otherwise, key bindings will not work, and mouse bindings
            (such as RMB) may fire up when not required. Keys must be
            bound to Top and mouse buttons - to specific widgets
            (Tkinterhtml widget, buttons on the button frame, etc.)
            Parents may be determined automatically, but this looks
            clumsy and unreliable. So I think it is better to hardcode
            mouse bindigs wherever possible and assume the config 
            provides for key bindigs only (or at least they are not
            to be bound to Top).
        '''
        sh.com.bind (obj = self.gui
                    ,bindings = '<Button-3>'
                    ,action = self.copy_text
                    )
        if sh.objs.get_os().is_win() or sh.objs.os.is_mac():
            sh.com.bind (obj = self.gui.obj
                        ,bindings = '<MouseWheel>'
                        ,action = self.set_mouse_wheel
                        )
        else:
            sh.com.bind (obj = self.gui.obj
                        ,bindings = ('<Button 4>'
                                    ,'<Button 5>'
                                    )
                        ,action = self.set_mouse_wheel
                        )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = '<Left>'
                    ,action = self.move_left
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = '<Right>'
                    ,action = self.move_right
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = '<Down>'
                    ,action = self.move_down
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = '<Up>'
                    ,action = self.move_up
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = '<Home>'
                    ,action = self.move_line_start
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = '<End>'
                    ,action = self.move_line_end
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = '<Control-Home>'
                    ,action = self.move_text_start
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = '<Control-End>'
                    ,action = self.move_text_end
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = '<Prior>'
                    ,action = self.move_page_up
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = '<Next>'
                    ,action = self.move_page_down
                    )
        sh.com.bind (obj = self.gui.obj
                    ,bindings = '<Escape>'
                    ,action = self.escape
                    )
        sh.com.bind (obj = self.gui
                    ,bindings = '<ButtonRelease-2>'
                    ,action = self.minimize
                    )
        sh.com.bind (obj = self.gui.ent_src
                    ,bindings = '<Control-a>'
                    ,action = self.gui.ent_src.select_all
                    )
        sh.com.bind (obj = self.gui.ent_src
                    ,bindings = '<KeyRelease>'
                    ,action = self.suggest_show
                    )
        sh.com.bind (obj = self.gui.ent_src
                    ,bindings = '<Up>'
                    ,action = self.suggest_up
                    )
        sh.com.bind (obj = self.gui.ent_src
                    ,bindings = '<Down>'
                    ,action = self.suggest_down
                    )
        sh.com.bind (obj = self.gui.ent_src
                    ,bindings = '<Control-Home>'
                    ,action = self.suggest_top
                    )
        sh.com.bind (obj = self.gui.ent_src
                    ,bindings = '<Control-End>'
                    ,action = self.suggest_bottom
                    )
        # Set config bindings
        hotkeys1 = (sh.lg.globs['str']['bind_toggle_history']
                   ,sh.lg.globs['str']['bind_toggle_history_alt']
                   )
        hotkeys1 = sh.Hotkeys(hotkeys1).run()
        hotkeys2 = (sh.lg.globs['str']['bind_clear_history']
                   ,'<ButtonRelease-3>'
                   )
        hotkeys2 = sh.Hotkeys(hotkeys2).run()
        self.gui.btn_hst.hint = _('Show history') + '\n' + hotkeys1 \
                                + '\n\n' + _('Clear history') + '\n' \
                                + hotkeys2
        self.gui.btn_abt.bindings = sh.lg.globs['str']['bind_show_about']
        self.gui.btn_alp.bindings = sh.lg.globs['str']['bind_toggle_alphabet']
        self.gui.btn_brw.bindings = (sh.lg.globs['str']['bind_open_in_browser']
                                    ,sh.lg.globs['str']['bind_open_in_browser_alt']
                                    )
        self.gui.btn_clr.bindings = sh.lg.globs['str']['bind_clear_search_field']
        self.gui.btn_def.bindings = sh.lg.globs['str']['bind_define']
        self.gui.btn_nxt.bindings = sh.lg.globs['str']['bind_go_forward']
        self.gui.btn_ins.bindings = '<Control-v>'
        self.gui.btn_prv.bindings = sh.lg.globs['str']['bind_go_back']
        self.gui.btn_prn.bindings = sh.lg.globs['str']['bind_print']
        self.gui.btn_qit.bindings = sh.lg.globs['str']['bind_quit']
        self.gui.btn_rld.bindings = (sh.lg.globs['str']['bind_reload_article']
                                    ,sh.lg.globs['str']['bind_reload_article_alt']
                                    )
        self.gui.btn_rp1.bindings = sh.lg.globs['str']['repeat_sign']
        self.gui.btn_rp2.bindings = sh.lg.globs['str']['repeat_sign2']
        self.gui.btn_sav.bindings = (sh.lg.globs['str']['bind_save_article']
                                    ,sh.lg.globs['str']['bind_save_article_alt']
                                    )
        self.gui.btn_set.bindings = (sh.lg.globs['str']['bind_settings']
                                    ,sh.lg.globs['str']['bind_settings_alt']
                                    )
        self.gui.btn_swp.bindings = sh.lg.globs['str']['bind_swap_langs']
        self.gui.btn_sym.bindings = sh.lg.globs['str']['bind_spec_symbol']
        self.gui.btn_ser.bindings = sh.lg.globs['str']['bind_re_search_article']
        self.gui.btn_trn.bindings = ('<Return>'
                                    ,'<KP_Enter>'
                                    )
        self.gui.btn_viw.bindings = (sh.lg.globs['str']['bind_toggle_view']
                                    ,sh.lg.globs['str']['bind_toggle_view_alt']
                                    )
        '''#NOTE: Reset 'hint' for those buttons which bindings have
           changed (in order to show these bindings in tooltip)
        '''
        self.gui.btn_abt.set_hint()
        self.gui.btn_alp.set_hint()
        self.gui.btn_blk.set_hint()
        self.gui.btn_brw.set_hint()
        self.gui.btn_clr.set_hint()
        self.gui.btn_def.set_hint()
        self.gui.btn_hst.set_hint()
        self.gui.btn_nxt.set_hint()
        self.gui.btn_ins.set_hint()
        self.gui.btn_prv.set_hint()
        self.gui.btn_pri.set_hint()
        self.gui.btn_prn.set_hint()
        self.gui.btn_qit.set_hint()
        self.gui.btn_rld.set_hint()
        self.gui.btn_rp1.set_hint()
        self.gui.btn_rp2.set_hint()
        self.gui.btn_sav.set_hint()
        self.gui.btn_swp.set_hint()
        self.gui.btn_set.set_hint()
        self.gui.btn_sym.set_hint()
        self.gui.btn_ser.set_hint()
        self.gui.btn_trn.set_hint()
        self.gui.btn_viw.set_hint()
        # Set controller actions
        self.gui.btn_abt.action = self.toggle_about
        self.gui.btn_alp.action = self.toggle_alphabet
        self.gui.btn_blk.action = self.edit_blacklist
        self.gui.btn_brw.action = self.open_in_browser
        self.gui.btn_cap.action = self.watch_clipboard
        self.gui.btn_clr.action = self.clear_search_field
        self.gui.btn_def.action = lambda x:self.define(Selected=False)
        self.gui.btn_hst.action = self.toggle_history
        self.gui.btn_ins.action = self.paste_search_field
        self.gui.btn_nxt.action = self.go_forward
        self.gui.btn_pri.action = self.edit_priorities
        self.gui.btn_prn.action = self.print
        self.gui.btn_prv.action = self.go_back
        self.gui.btn_rld.action = self.reload
        self.gui.btn_rp1.action = self.insert_repeat_sign
        self.gui.btn_rp2.action = self.insert_repeat_sign2
        self.gui.btn_sav.action = self.toggle_save
        self.gui.btn_ser.action = self.search_reset
        self.gui.btn_set.action = self.toggle_settings
        self.gui.btn_swp.action = self.swap_langs
        self.gui.btn_sym.action = self.insert_sym
        self.gui.btn_trn.action = self.go
        self.gui.btn_viw.action = self.toggle_view
        self.gui.opt_col.action = self.set_columns
        
    def set_title(self,arg=None):
        if not arg:
            arg = sh.List(lst1=[gi.PRODUCT,gi.VERSION]).space_items()
        self.gui.set_title(arg)

    def get_text(self,event=None):
        # We will have a Segmentation Fault on empty input
        if lg.objs.get_request().htm:
            return self.gui.widget.text('text')

    def set_mouse_sel(self,event=None):
        self.get_pos(event)
        self.select()

    def get_pos(self,event=None):
        f = '[MClient] mclient.WebFrame.get_pos'
        if event:
            pos = -1
            try:
                node1,node2 = self.gui.widget.node(True,event.x,event.y)
                pos = self.gui.widget.text('offset',node1,node2)
            # Need more than 0 values to unpack
            except ValueError:
                pass
                '''
                # Too frequent
                mes = _('Unable to get the position!')
                sh.objs.get_mes(f,mes,True).show_warning()
                '''
            if str(pos).isdigit():
                Selectable = objs.get_blocksdb().Selectable
                objs.blocksdb.Selectable = False
                result = objs.blocksdb.get_block_pos(pos)
                if result:
                    self.posn = pos
                if Selectable:
                    objs.blocksdb.Selectable = True
                    result = objs.blocksdb.get_block_pos(pos)
                    if result:
                        self.pos = pos
                else:
                    self.pos = self.posn
                objs.blocksdb.Selectable = Selectable

    def _select(self,result):
        f = '[MClient] mclient.WebFrame._select'
        try:
            self.gui.widget.tag ('delete','selection')
            self.gui.widget.tag ('add','selection',result[0]
                                ,result[2],result[1],result[3]
                                )
            self.gui.widget.tag ('configure','selection','-background'
                                ,sh.lg.globs['str']['color_terms_sel_bg']
                                )
            self.gui.widget.tag ('configure','selection','-foreground'
                                ,sh.lg.globs['str']['color_terms_sel_fg']
                                )
        except Exception as e:
            sh.com.rep_failed(f,e)
    
    def select(self):
        f = '[MClient] mclient.WebFrame.select'
        result = objs.get_blocksdb().get_sel(self.pos)
        if result:
            objs.get_blocksdb().set_bookmark(self.pos)
            self._select(result)
        else:
            pass
            # Too frequent
            #sh.com.rep_empty(f)

    def shift_x(self,bbox1,bbox2):
        f = '[MClient] mclient.WebFrame.shift_x'
        width = self.gui.get_width()
        result = objs.get_blocksdb().get_max_bbox()
        if width and result:
            max_bbox = result[0]
            page1_no = int(bbox1 / width)
            page2_no = int(bbox2 / width)

            if page1_no == page2_no:
                page_bbox = page1_no * width
                self.gui.scroll_x (bbox = page_bbox
                                  ,max_bbox = max_bbox
                                  )
            else:
                page1_bbox = page1_no * width
                page2_bbox = page2_no * width
                if page2_bbox - page1_bbox > width:
                    delta = 0
                    mes = _('The column is too wide to be fully shown')
                    sh.objs.get_mes(f,mes,True).show_warning()
                else:
                    delta = bbox2 - page2_bbox
                self.gui.scroll_x (bbox = page1_bbox + delta
                                  ,max_bbox = max_bbox
                                  )
        else:
            sh.com.rep_empty(f)
    
    def shift_y(self,bboy1,bboy2):
        f = '[MClient] mclient.WebFrame.shift_y'
        height = self.gui.get_height()
        result = objs.get_blocksdb().get_max_bboy()
        if height and result:
            max_bboy = result[0]
            page1_no = int(bboy1 / height)
            page2_no = int(bboy2 / height)
            if page1_no == page2_no:
                page_bboy = page1_no * height
                self.gui.scroll_y (bboy = page_bboy
                                  ,max_bboy = max_bboy
                                  )
            else:
                page1_bboy = page1_no * height
                page2_bboy = page2_no * height
                if page2_bboy - page1_bboy > height:
                    delta = 0
                    mes = _('The row is too wide to be fully shown')
                    sh.objs.get_mes(f,mes,True).show_warning()
                else:
                    delta = bboy2 - page2_bboy
                self.gui.scroll_y (bboy = page1_bboy + delta
                                  ,max_bboy = max_bboy
                                  )
        else:
            sh.com.rep_empty(f)

    def shift_screen(self):
        ''' In order to shift the screen correctly, we need to:
            - make visible the minimum BBOY1 and the maximum BBOY2 of
              the current row;
            - if BBOY2 - BBOY1 exceeds the current height, we should
              scroll to BBOY1 only
            - make visible the minimum BBOX1 and the maximum BBOX2 of
              the current column;
            - if BBOX2 - BBOX1 exceeds the current width, we should
              scroll to BBOX1 only
        '''
        f = '[MClient] mclient.WebFrame.shift_screen'
        result1 = objs.get_blocksdb().get_block_pos(pos=self.pos)
        if result1:
            result2 = objs.blocksdb.get_bbox_limits(col_no=result1[4])
            result3 = objs.blocksdb.get_bboy_limits(row_no=result1[3])
            if result2 and result3:
                self.shift_x (bbox1 = result2[0]
                             ,bbox2 = result2[1]
                             )
                self.shift_y (bboy1 = result3[0]
                             ,bboy2 = result3[1]
                             )
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.rep_empty(f)

    def fill(self,code=None):
        f = '[MClient] mclient.WebFrame.fill'
        self.gui.widget.reset()
        if not code:
            code = '<html><body><h1>' + _('Nothing has been loaded yet.')\
                                      + '</h1></body></html>'
        try:
            self.gui.widget.parse(code)
            ''' This should not happen now as we strip out non-supported
                characters.
            '''
        except Exception as e:
            sh.com.rep_failed(f,e)
            # Othewise, we will have a segmentation fault here
            self.reset()
            lg.objs.get_request().reset()

    def load_article(self):
        f = '[MClient] mclient.WebFrame.load_article'
        ''' #NOTE: each time the contents of the current page is changed
            (e.g., due to prioritizing), bookmarks must be deleted.
        '''
        # Suppress useless error output
        if not lg.objs.get_request().search:
            return
        timer = sh.Timer(f)
        timer.start()
        # Do not allow selection positions from previous articles
        self.pos = -1
        order = objs.get_settings().get_speech_prior()
        lg.objs.get_speech_prior().reset(order)
        artid = objs.get_blocksdb().is_present (source = sh.lg.globs['str']['source']
                                               ,title = lg.objs.request.search
                                               ,url = lg.objs.request.url
                                               )
        if artid:
            mes = _('Load article No. {} from memory').format(artid)
            sh.objs.get_mes(f,mes,True).show_info()
            objs.blocksdb.artid = artid
            self.get_bookmark()
        else:
            blocks = lg.objs.get_plugins().request (search = lg.objs.request.search
                                                   ,url = lg.objs.request.url
                                                   )
            # 'None' skips the autoincrement
            data = (None                              # (00) ARTICLEID
                   ,sh.lg.globs['str']['source']      # (01) SOURCE
                   ,lg.objs.request.search            # (02) TITLE
                   ,lg.objs.request.url               # (03) URL
                   ,lg.objs.get_plugins().get_lang1() # (04) LANG1
                   ,lg.objs.plugins.get_lang2()       # (05) LANG2
                   ,self.pos                          # (06) BOOKMARK
                   ,lg.objs.plugins.get_htm()         # (07) CODE
                   )
            objs.blocksdb.fill_articles(data)
            objs.blocksdb.artid = objs.blocksdb.get_max_artid()
            data = lg.com.dump_elems (blocks = blocks
                                     ,artid = objs.blocksdb.artid
                                     )
            if data:
                objs.blocksdb.fill_blocks(data)
            
            objs.blocksdb.update_phterm()
            
        self.phdic = objs.blocksdb.get_phdic()
        if self.phdic:
            if sh.lg.globs['bool']['ShortSubjects']:
                self.phdic = self.phdic[0]
            else:
                self.phdic = self.phdic[1]
        else:
            self.phdic = ''
        
        if self.phdic:
            lg.objs.request.SpecialPage = False
        else:
            # Otherwise, 'SpecialPage' will be inherited
            lg.objs.request.SpecialPage = True
        self.update_columns()
        
        SortTerms = sh.lg.globs['bool']['AlphabetizeTerms'] \
                    and not lg.objs.request.SpecialPage
        ''' We must reset DB as early as possible after setting 'elems',
            otherwise, real and loaded settings may not coincide, which,
            in turn, may lead to a data loss, see, for example, RU-EN:
            "цепь: провод".
        '''
        objs.blocksdb.reset (cols = lg.objs.request.cols
                            ,SortRows = sh.lg.globs['bool']['SortByColumns']
                            ,SortTerms = SortTerms
                            ,ExpandDic = not sh.lg.globs['bool']['ShortSubjects']
                            ,ShowUsers = sh.lg.globs['bool']['ShowUserNames']
                            ,PhraseCount = sh.lg.globs['bool']['PhraseCount']
                            )
        # Read lists from files
        #TODO: find the first occurrence
        lg.objs.get_order()
        sj.objs.get_article().reset (pairs = objs.blocksdb.get_dic_pairs()
                                    ,Debug = lg.objs.get_plugins().Debug
                                    )
        sj.objs.article.run()
        data = objs.blocksdb.assign_bp()
        spdic = lg.objs.speech_prior.get_all2prior()
        bp = cl.BlockPrioritize (data = data
                                ,Block = sh.lg.globs['bool']['BlockSubjects']
                                ,Prioritize = sh.lg.globs['bool']['PrioritizeSubjects']
                                ,phdic = self.phdic
                                ,spdic = spdic
                                ,Debug = lg.objs.plugins.Debug
                                ,maxrows = lg.objs.plugins.maxrows
                                )
        bp.run()
        objs.blocksdb.update(bp.query)
        
        objs.blocksdb.unignore()
        objs.blocksdb.ignore()
        
        data = objs.blocksdb.assign_cells()

        if sh.lg.globs['bool']['ShortSpeech']:
            spdic = {}
        else:
            spdic = lg.objs.speech_prior.get_abbr2full()
        
        cells = cl.Cells (data = data
                         ,cols = lg.objs.request.cols
                         ,collimit = lg.objs.request.collimit
                         ,phdic = self.phdic
                         ,spdic = spdic
                         ,Reverse = sh.lg.globs['bool']['VerticalView']
                         ,Debug = lg.objs.plugins.Debug
                         ,maxrows = lg.objs.plugins.maxrows
                         )
        cells.run()
        cells.dump(objs.blocksdb)
        
        mh.objs.get_htm().reset (data = objs.blocksdb.fetch()
                                ,cols = lg.objs.request.cols
                                ,collimit = lg.objs.request.collimit
                                ,width = sh.lg.globs['int']['col_width']
                                ,Reverse = sh.lg.globs['bool']['VerticalView']
                                ,phdic = self.phdic
                                ,skipped = len(com.get_skipped_dics())
                                )
        mh.objs.htm.run()
        
        lg.objs.request.htm = mh.objs.htm.htm
        self.fill(lg.objs.request.htm)

        data = objs.blocksdb.assign_pos()
        pos = cl.Pos (data = data
                     ,raw_text = self.get_text()
                     ,Debug = lg.objs.plugins.Debug
                     ,maxrows = lg.objs.plugins.maxrows
                     )
        pos.run()
        objs.blocksdb.update(pos.query)

        ''' We do no use Debug here since this causes too much errors
            when the entire program runs (debugging is GUI-based and
            conflicts with setting nodes).
        '''
        pages = cl.Pages (obj = objs.get_webframe().gui
                         ,blocks = pos.blocks
                         )
        pages.run()
        objs.blocksdb.update(pages.query)
        
        self.set_title(lg.objs.request.search)
        if self.pos >= 0:
            self.select()
            self.shift_screen()
        else:
            result = objs.blocksdb.get_start()
            if str(result).isdigit():
                self.pos = result
                self.select()
            else:
                mes = _('Wrong input data!')
                sh.objs.get_mes(f,mes,True).show_warning()
        ''' Empty article is not added either to DB or history, so we
            just do not clear the search field to be able to correct
            the typo.
        '''
        if pages.blocks or com.get_skipped_terms():
            self.gui.ent_src.clear_text()
        objs.get_search().reset()
        objs.get_suggest().close()
        self.update_buttons()
        timer.end()
        self.run_final_debug()
        #self.debug_settings()
    
    def go_keyboard(self,event=None):
        f = '[MClient] mclient.WebFrame.go_keyboard'
        search = self.gui.ent_src.widget.get().strip('\n').strip(' ')
        if search == '':
            self.go_url()
        elif search == sh.lg.globs['str']['repeat_sign']:
            self.insert_repeat_sign()
        elif search == sh.lg.globs['str']['repeat_sign2']:
            self.insert_repeat_sign2()
        else:
            lg.objs.get_request().search = search
            self.go_search()
    
    def go(self,event=None,Mouse=False):
        # Process either the search string or the URL
        f = '[MClient] mclient.WebFrame.go'
        if Mouse:
            self.go_url()
        else:
            self.go_keyboard()

    def go_url(self,event=None):
        # Follow the URL of the current block
        f = '[MClient] mclient.WebFrame.go_url'
        if not lg.objs.get_request().MouseClicked:
            url = objs.get_blocksdb().get_url(self.pos)
            if url:
                lg.objs.request.search = objs.blocksdb.get_text(self.pos)
                lg.objs.request.url = url
                mes = _('Open link: {}').format(lg.objs.request.url)
                sh.objs.get_mes(f,mes,True).show_info()
                self.load_article()
            # Do not warn when there are no articles yet
            elif objs.blocksdb.artid == 0:
                sh.com.rep_lazy(f)
            else:
                lg.objs.request.search = objs.blocksdb.get_text(self.pos)
                self.go_search()

    def go_search(self):
        f = '[MClient] mclient.WebFrame.go_search'
        if lg.objs.get_request().search is None:
            lg.objs.request.search = ''
        lg.objs.request.search = lg.objs.request.search.strip()
        if self.control_length():
            self.update_lang1()
            self.update_lang2()
            self.auto_swap()
            self.get_url()
            mes = '"{}"'.format(lg.objs.request.search)
            sh.objs.get_mes(f,mes,True).show_debug()
            self.load_article()

    def set_source(self,event=None):
        f = '[MClient] mclient.WebFrame.set_source'
        ''' Since Combo-type OptionMenus can be edited manually, we must
            get an actual value first.
        '''
        self.gui.opt_src._get()
        sh.lg.globs['str']['source'] = self.gui.opt_src.choice
        mes = _('Set source to "{}"')
        mes = mes.format(sh.lg.globs['str']['source'])
        sh.objs.get_mes(f,mes,True).show_info()
        lg.objs.get_plugins().set(sh.lg.globs['str']['source'])
        self.reset_opt(sh.lg.globs['str']['source'])
        self.go_search()
        self.gui.ent_src.focus()

    def get_url(self):
        f = '[MClient] mclient.WebFrame.get_url'
        #NOTE: update source and target languages first
        lg.objs.get_request().url = lg.objs.get_plugins().get_url(lg.objs.request.search)
        mes = lg.objs.request.url
        sh.objs.get_mes(f,mes,True).show_debug()

    def move_line_start(self,event=None):
        # Go to the 1st term of the current row
        #TODO: move 'move_*' procedures to Moves class
        f = '[MClient] mclient.WebFrame.move_line_start'
        result = objs.get_blocksdb().get_line_start(self.pos)
        if str(result).isdigit():
            self.pos = result
            self.select()
            self.shift_screen()
        else:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f,mes,True).show_warning()

    def move_line_end(self,event=None):
        # Go to the last term of the current row
        f = '[MClient] mclient.WebFrame.move_line_end'
        result = objs.get_blocksdb().get_line_end(self.pos)
        if str(result).isdigit():
            self.pos = result
            self.select()
            self.shift_screen()
        else:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f,mes,True).show_warning()

    def move_text_start(self,event=None):
        # Go to the 1st (non-)selectable block
        f = '[MClient] mclient.WebFrame.move_text_start'
        result = objs.get_blocksdb().get_start()
        if str(result).isdigit():
            self.pos = result
            self.select()
            self.shift_screen()
        else:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f,mes,True).show_warning()

    def move_text_end(self,event=None):
        # Go to the last term in the article
        f = '[MClient] mclient.WebFrame.move_text_end'
        result = objs.get_blocksdb().get_end()
        if str(result).isdigit():
            self.pos = result
            self.select()
            self.shift_screen()
        else:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f,mes,True).show_warning()

    def move_page_up(self,event=None):
        # Go to the previous page
        result = objs.get_blocksdb().get_sel(self.pos)
        height = self.gui.get_height()
        if result and height:
            result = objs.get_blocksdb().get_page_up (bboy = result[6]
                                                     ,height = height
                                                     )
            if str(result).isdigit():
                self.pos = result
                self.select()
                self.shift_screen()

    def move_page_down(self,event=None):
        # Go to the next page
        result = objs.get_blocksdb().get_sel(self.pos)
        height = self.gui.get_height()
        if result and height:
            result = objs.get_blocksdb().get_page_down (bboy = result[6]
                                                       ,height = height
                                                       )
            if str(result).isdigit():
                self.pos = result
                self.select()
                self.shift_screen()

    def move_left(self,event=None):
        # Go to the previous term
        f = '[MClient] mclient.WebFrame.move_left'
        result = objs.get_blocksdb().get_left(self.pos)
        if str(result).isdigit():
            self.pos = result
            self.select()
            self.shift_screen()
        else:
            mes = _('Wrong input data: "{}"!').format(result)
            sh.objs.get_mes(f,mes,True).show_warning()

    def move_right(self,event=None):
        # Go to the next term
        f = '[MClient] mclient.WebFrame.move_right'
        result = objs.get_blocksdb().get_right(self.pos)
        if str(result).isdigit():
            self.pos = result
            self.select()
            self.shift_screen()
        else:
            mes = _('Wrong input data: "{}"!').format(result)
            sh.objs.get_mes(f,mes,True).show_warning()

    def move_down(self,event=None):
        # Go to the next row
        f = '[MClient] mclient.WebFrame.move_down'
        result = objs.get_blocksdb().get_down(self.pos)
        if str(result).isdigit():
            self.pos = result
            self.select()
            self.shift_screen()
        else:
            mes = _('Wrong input data: "{}"!').format(result)
            sh.objs.get_mes(f,mes,True).show_warning()

    def move_up(self,event=None):
        # Go to the previous row
        f = '[MClient] mclient.WebFrame.move_up'
        result = objs.get_blocksdb().get_up(self.pos)
        if str(result).isdigit():
            self.pos = result
            self.select()
            self.shift_screen()
        else:
            mes = _('Wrong input data: "{}"!').format(result)
            sh.objs.get_mes(f,mes,True).show_warning()

    def set_mouse_wheel(self,event):
        # Use mouse wheel to scroll screen
        ''' #TODO: #FIX: too small delta in Windows
            delta is -120 in Windows XP, however, it is different in
            other versions.
        '''
        if event.num == 5 or event.delta < 0:
            if sh.objs.get_os().is_lin():
                self.move_page_down()
            else:
                self.move_down()
            ''' delta is 120 in Windows XP, however, it is different in
                other versions.
            '''
        if event.num == 4 or event.delta > 0:
            if sh.objs.get_os().is_lin():
                self.move_page_up()
            else:
                self.move_up()
        return 'break'

    def watch_clipboard(self,event=None):
        # Watch clipboard
        if sh.lg.globs['bool']['CaptureHotkey']:
            sh.lg.globs['bool']['CaptureHotkey'] = False
        else:
            sh.lg.globs['bool']['CaptureHotkey'] = True
        self.update_buttons()

    def open_in_browser(self,event=None):
        # Open URL of the current article in a browser
        ionline = sh.Online()
        url = lg.objs.get_request().url
        ionline.url = lg.objs.get_plugins().fix_url(url)
        ionline.browse()

    def copy_text(self,event=None):
        # Copy text of the current block
        f = '[MClient] mclient.WebFrame.copy_text'
        text = objs.get_blocksdb().get_text(self.pos)
        if text:
            sh.Clipboard().copy(text)
            if sh.lg.globs['bool']['Iconify']:
                self.minimize()
        # Do not warn when there are no articles yet
        elif objs.blocksdb.artid == 0:
            sh.com.rep_lazy(f)
        else:
            mes = _('This block does not contain any text!')
            sh.objs.get_mes(f,mes).show_warning()

    def copy_url(self,event=None):
        # Copy URL of the current article
        url = lg.objs.get_request().url
        url = lg.objs.get_plugins().fix_url(url)
        sh.Clipboard().copy(url)
        if sh.lg.globs['bool']['Iconify']:
            self.minimize()

    def copy_block_url(self,event=None):
        # Copy URL of the selected block
        f = '[MClient] mclient.WebFrame.copy_block_url'
        url = objs.get_blocksdb().get_url(self.pos)
        if url:
            url = lg.objs.get_plugins().fix_url(url)
            sh.Clipboard().copy(url)
            if sh.lg.globs['bool']['Iconify']:
                self.minimize()
        else:
            mes = _('This block does not contain a URL!')
            sh.objs.get_mes(f,mes).show_warning()

    def define(self,Selected=True):
        # Open a web-page with a definition of the current term
        # Selected: True: Selected term; False: Article title
        f = '[MClient] mclient.WebFrame.define'
        if Selected:
            result = objs.get_blocksdb().get_block_pos(self.pos)
            pattern = result[6]
        else:
            pattern = lg.objs.get_request().search
        if pattern:
            pattern = _('what is "{}"?').format(pattern)
            sh.Online (base = sh.lg.globs['str']['web_search_url']
                      ,pattern = pattern
                      ).browse()
        else:
            sh.com.rep_empty(f)

    def go_back(self,event=None):
        # Go to the previous search
        f = '[MClient] mclient.WebFrame.go_back'
        result = objs.get_blocksdb().get_prev_id()
        if result:
            objs.blocksdb.artid = result
            result = objs.blocksdb.get_article()
            if result:
                sh.lg.globs['str']['source'] = result[0]
                lg.objs.get_request().search = result[1]
                lg.objs.request.url = result[2]
                lg.objs.get_plugins().set(sh.lg.globs['str']['source'])
                lg.objs.plugins.set_lang1(result[4])
                lg.objs.plugins.set_lang2(result[5])
                self.reset_opt(sh.lg.globs['str']['source'])
                self.load_article()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.rep_empty(f)

    def go_forward(self,event=None):
        # Go to the next search
        f = '[MClient] mclient.WebFrame.go_forward'
        result = objs.get_blocksdb().get_next_id()
        if result:
            objs.blocksdb.artid = result
            result = objs.blocksdb.get_article()
            if result:
                sh.lg.globs['str']['source'] = result[0]
                lg.objs.get_request().search = result[1]
                lg.objs.request.url = result[2]
                lg.objs.get_plugins().set(sh.lg.globs['str']['source'])
                lg.objs.plugins.set_lang1(result[4])
                lg.objs.plugins.set_lang2(result[5])
                self.reset_opt(sh.lg.globs['str']['source'])
                self.load_article()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.rep_empty(f)

    def control_length(self):
        # Confirm too long requests
        f = '[MClient] mclient.WebFrame.control_length'
        Confirmed = True
        if len(lg.objs.get_request().search) >= 150:
            mes = _('The request is long ({} symbols). Do you really want to send it?')
            mes = mes.format(len(lg.objs.request.search))
            if not sh.objs.get_mes(f,mes).show_question():
                Confirmed = False
        return Confirmed

    def search_reset(self,event=None):
        # SearchArticle
        objs.get_search().reset()
        objs.search.get_next()

    def set_lang1(self,event=None):
        f = '[MClient] mclient.WebFrame.set_lang1'
        ''' Since Combo-type OptionMenus can be edited manually, we must
            get an actual value first.
        '''
        self.gui.opt_lg1._get()
        if lg.objs.get_plugins().get_lang1() != self.gui.opt_lg1.choice:
            mes = _('Set language: {}').format(self.gui.opt_lg1.choice)
            sh.objs.get_mes(f,mes,True).show_info()
            sh.lg.globs['str']['lang1'] = self.gui.opt_lg1.choice
            lg.objs.get_plugins().set_lang1(self.gui.opt_lg1.choice)
    
    def set_lang2(self,event=None):
        f = '[MClient] mclient.WebFrame.set_lang2'
        ''' Since Combo-type OptionMenus can be edited manually, we must
            get an actual value first.
        '''
        self.gui.opt_lg2._get()
        if lg.objs.get_plugins().get_lang2() != self.gui.opt_lg2.choice:
            mes = _('Set language: {}').format(self.gui.opt_lg2.choice)
            sh.objs.get_mes(f,mes,True).show_info()
            sh.lg.globs['str']['lang2'] = self.gui.opt_lg2.choice
            lg.objs.get_plugins().set_lang2(self.gui.opt_lg2.choice)

    def reset_columns(self,event=None):
        f = '[MClient] mclient.WebFrame.reset_columns'
        ''' Since Combo-type OptionMenus can be edited manually, we must
            get an actual value first.
        '''
        self.gui.opt_col._get()
        fixed = [col for col in lg.objs.get_request().cols \
                 if col != _('Do not set')
                ]
        sh.lg.globs['int']['colnum'] = sh.Input (title = f
                                                ,value = self.gui.opt_col.choice
                                                ).get_integer()
        lg.objs.request.collimit = sh.lg.globs['int']['colnum'] + len(fixed)
        mes = _('Set the number of columns to {}')
        mes = mes.format(lg.objs.request.collimit)
        sh.objs.get_mes(f,mes,True).show_info()

    
    def set_columns(self,event=None):
        self.reset_columns()
        objs.get_blocksdb().delete_bookmarks()
        self.load_article()
        self.gui.ent_src.focus()

    def reload(self,event=None):
        objs.get_blocksdb().clear_cur()
        self.load_article()

    def toggle_view(self,event=None):
        if sh.lg.globs['bool']['VerticalView']:
            sh.lg.globs['bool']['VerticalView'] = False
        else:
            sh.lg.globs['bool']['VerticalView'] = True
        objs.get_blocksdb().delete_bookmarks()
        self.load_article()

    def toggle_alphabet(self,event=None):
        if sh.lg.globs['bool']['AlphabetizeTerms']:
            sh.lg.globs['bool']['AlphabetizeTerms'] = False
        else:
            sh.lg.globs['bool']['AlphabetizeTerms'] = True
        objs.get_blocksdb().delete_bookmarks()
        self.load_article()

    def toggle_block(self,event=None):
        f = '[MClient] mclient.WebFrame.toggle_block'
        if sh.lg.globs['bool']['BlockSubjects']:
            sh.lg.globs['bool']['BlockSubjects'] = False
            objs.get_blocksdb().unblock()
        else:
            sh.lg.globs['bool']['BlockSubjects'] = True
            if not lg.objs.get_order().blacklst:
                mes = _('No subjects have been provided for blacklisting!')
                sh.objs.get_mes(f,mes).show_warning()
        objs.get_blocksdb().delete_bookmarks()
        self.load_article()

    def edit_blacklist(self,event=None):
        f = '[MClient] mclient.WebFrame.edit_blacklist'
        old_list = lg.objs.get_order().blacklst
        old_key = sh.lg.globs['bool']['BlockSubjects']
        objs.get_blacklist().reset (lst1 = old_list
                                   ,lst2 = lg.objs.get_plugins().get_subjects()
                                   ,art_subjects = com.get_dics()
                                   ,majors = lg.objs.plugins.get_majors()
                                   )
        objs.blacklist.set_checkbox(sh.lg.globs['bool']['BlockSubjects'])
        objs.blacklist.show()
        sh.lg.globs['bool']['BlockSubjects'] = objs.blacklist.get_checkbox()
        new_list = objs.blacklist.get1()
        if (old_list == new_list) \
        and (old_key == sh.lg.globs['bool']['BlockSubjects']):
            sh.com.rep_lazy(f)
        else:
            lg.objs.order.blacklst = new_list
            objs.get_blocksdb().delete_bookmarks()
            self.load_article()
    
    def edit_priorities(self,event=None):
        f = '[MClient] mclient.WebFrame.edit_priorities'
        old_list = lg.objs.get_order().priorlst
        old_key = sh.lg.globs['bool']['PrioritizeSubjects']
        objs.get_priorities().reset (lst1 = old_list
                                    ,lst2 = lg.objs.get_plugins().get_subjects()
                                    ,art_subjects = com.get_dics()
                                    ,majors = lg.objs.plugins.get_majors()
                                    )
        objs.priorities.set_checkbox(sh.lg.globs['bool']['PrioritizeSubjects'])
        objs.priorities.show()
        sh.lg.globs['bool']['PrioritizeSubjects'] = objs.priorities.get_checkbox()
        new_list = objs.priorities.get1()
        if (old_list == new_list) \
        and (old_key == sh.lg.globs['bool']['PrioritizeSubjects']):
            sh.com.rep_lazy(f)
        else:
            lg.objs.order.priorlst = new_list
            objs.get_blocksdb().delete_bookmarks()
            self.load_article()
    
    def toggle_priority(self,event=None):
        f = '[MClient] mclient.WebFrame.toggle_priority'
        if sh.lg.globs['bool']['PrioritizeSubjects']:
            sh.lg.globs['bool']['PrioritizeSubjects'] = False
            objs.get_blocksdb().unprioritize()
        else:
            sh.lg.globs['bool']['PrioritizeSubjects'] = True
            if not lg.objs.get_order().prioritize:
                mes = _('No subjects have been provided for prioritizing!')
                sh.objs.get_mes(f,mes).show_warning()
        objs.get_blocksdb().delete_bookmarks()
        self.load_article()

    def print(self,event=None):
        f = '[MClient] mclient.WebFrame.print'
        mh.objs.get_htm().reset (data = objs.blocksdb.fetch()
                                ,cols = lg.objs.request.cols
                                ,collimit = lg.objs.request.collimit
                                ,width = sh.lg.globs['int']['col_width']
                                ,Printer = True
                                ,Reverse = sh.lg.globs['bool']['VerticalView']
                                ,skipped = len(com.get_skipped_dics())
                                )
        code = mh.objs.htm.run()
        if code:
            tmp_file = sh.objs.get_tmpfile (suffix = '.htm'
                                           ,Delete = 0
                                           )
            sh.WriteTextFile (file = tmp_file
                             ,Rewrite = True
                             ).write(code)
            sh.Launch(sh.objs.get_tmpfile()).launch_default()
        else:
            sh.com.rep_empty(f)

    def update_columns(self):
        ''' Update a column number in GUI; adjust the column number
            (both logic and GUI) in special cases.
        '''
        f = '[MClient] mclient.WebFrame.update_columns'
        fixed = [col for col in lg.objs.get_request().cols \
                 if col != _('Do not set')
                ]
        if lg.objs.request.collimit > len(fixed):
            ''' A subject from the 'Phrases' section usually has
                an 'original + translation' structure, so we need to
                switch off sorting terms and ensure that the number of
                columns is divisible by 2
            '''
            if lg.objs.request.SpecialPage \
            and lg.objs.request.collimit % 2 != 0:
                if lg.objs.request.collimit == len(fixed) + 1:
                    lg.objs.request.collimit += 1
                else:
                    lg.objs.request.collimit -= 1
            non_fixed_len = lg.objs.request.collimit - len(fixed)
            self.gui.opt_col.set(non_fixed_len)
            mes = _('Set the column limit to {} ({} in total)')
            mes = mes.format(non_fixed_len,lg.objs.request.collimit)
            sh.objs.get_mes(f,mes,True).show_info()
        else:
            sub = '{} > {}'.format (lg.objs.request.collimit
                                   ,len(fixed)
                                   )
            mes = _('The condition "{}" is not observed!').format(sub)
            sh.objs.get_mes(f,mes).show_error()

    def ignore_column(self,col_no):
        f = '[MClient] mclient.WebFrame.ignore_column'
        if len(lg.objs.get_request().cols) > col_no + 1:
            if lg.objs.request.cols[col_no] == 'transc':
                mes = _('Select column "{}" instead of "{}"')
                mes = mes.format (lg.objs.request.cols[col_no]
                                 ,lg.objs.request.cols[col_no+1]
                                 )
                sh.objs.get_mes(f,mes,True).show_debug()
                col_no += 1
        return col_no
    
    # Go to the next section of column #col_no
    def move_next_section(self,event=None,col_no=0):
        f = '[MClient] mclient.WebFrame.move_next_section'
        col_no = self.ignore_column(col_no)
        result1 = objs.get_blocksdb().get_block_pos(self.pos)
        result2 = objs.blocksdb.get_next_section (pos = self.pos
                                                 ,col_no = col_no
                                                 )
        if result1 and result2:
            result3 = objs.blocksdb.get_next_col (row_no = result2[1]
                                                 ,col_no = result1[4]
                                                 )
            result4 = objs.blocksdb.get_next_col (row_no = result2[1]
                                                 ,col_no = 0
                                                 )
            if result3 or result4:
                if result4 and not result3:
                    pos = result4[0]
                else:
                    pos = result3[0]
                result = objs.get_blocksdb().get_next_block_pos(pos)
                if result:
                    self.pos = result[0]
                    self.select()
                    self.shift_screen()
                else:
                    sh.com.rep_empty(f)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.rep_empty(f)
        
    def move_prev_section(self,event=None,col_no=0):
        # Go to the previous section of column #col_no
        f = '[MClient] mclient.WebFrame.move_prev_section'
        col_no = self.ignore_column(col_no)
        result1 = objs.get_blocksdb().get_block_pos(self.pos)
        result2 = objs.blocksdb.get_prev_section (pos = self.pos
                                                 ,col_no = col_no
                                                 )
        if result1 and result2:
            result3 = objs.blocksdb.get_next_col (row_no = result2[1]
                                                 ,col_no = result1[4]
                                                 )
            result4 = objs.blocksdb.get_next_col (row_no = result2[1]
                                                 ,col_no = 0
                                                 )
            if result3 or result4:
                if result4 and not result3:
                    pos = result4[0]
                else:
                    pos = result3[0]
                result = objs.get_blocksdb().get_next_block_pos(pos)
                if result:
                    self.pos = result[0]
                    self.select()
                    self.shift_screen()
                else:
                    sh.com.rep_empty(f)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.rep_empty(f)
    
    def get_bookmark(self):
        f = '[MClient] mclient.WebFrame.get_bookmark'
        result = objs.get_blocksdb().get_article()
        if result:
            if str(result[3]).isdigit():
                self.pos = result[3]
                mes = _('Load bookmark {} for article #{}')
                mes = mes.format(self.pos,objs.blocksdb.artid)
                sh.objs.get_mes(f,mes,True).show_debug()
            else:
                mes = _('Wrong input data!')
                sh.objs.get_mes(f,mes,True).show_warning()
        else:
            sh.com.rep_empty(f)
            result = objs.blocksdb.get_start()
            if str(result).isdigit():
                self.pos = result()
            else:
                mes = _('Wrong input data!')
                sh.objs.get_mes(f,mes,True).show_warning()
    
    def toggle_sel(self,event=None):
        if objs.get_blocksdb().Selectable:
            objs.get_blocksdb().Selectable = sh.lg.globs['bool']['SelectTermsOnly']\
                                           = False
            objs.blocksdb.delete_bookmarks()
            self.load_article()
        else:
            objs.get_blocksdb().Selectable = sh.lg.globs['bool']['SelectTermsOnly']\
                                           = True
            objs.blocksdb.delete_bookmarks()
            self.load_article()



class Settings:

    def __init__(self):
        self.gui = None
        self.Active = False
    
    def toggle(self,event=None):
        if self.Active:
            self.close()
        else:
            self.show()
    
    def get_gui(self):
        if self.gui is None:
            self.set_gui()
        return self.gui
    
    def set_gui(self):
        self.gui = gi.Settings()
        self.set_bindings()

    def show(self,event=None):
        self.Active = True
        self.get_gui()
        UpdateSettingsUI().run()
        self.gui.show()
    
    def close(self,event=None):
        self.Active = False
        self.get_gui().close()
    
    def get_block_settings(self,event=None):
        f = '[MClient] mclient.Settings.get_block_settings'
        mes = _('Not implemented yet!')
        sh.objs.get_mes(f,mes).show_info()

    def get_priority_settings(self,event=None):
        f = '[MClient] mclient.Settings.get_priority_settings'
        mes = _('Not implemented yet!')
        sh.objs.get_mes(f,mes).show_info()

    def apply(self,event=None):
        self.close()
        ExportSettingsUI().run()
        objs.get_webframe().set_columns()
    
    def set_bindings(self):
        self.get_gui().btn_apl.action = self.apply
        #TODO: implement
        #self.btn_blk.action = self.block_settings
        #self.btn_pri.action = self.priority_settings
        sh.com.bind (obj = self.gui.obj
                    ,bindings = [sh.lg.globs['str']['bind_settings']
                                ,sh.lg.globs['str']['bind_settings_alt']
                                ]
                    ,action = self.toggle
                    )

    def get_speech_prior(self):
        return (sh.lg.globs['str']['speech1']
               ,sh.lg.globs['str']['speech2']
               ,sh.lg.globs['str']['speech3']
               ,sh.lg.globs['str']['speech4']
               ,sh.lg.globs['str']['speech5']
               ,sh.lg.globs['str']['speech6']
               ,sh.lg.globs['str']['speech7']
               )



class Suggest:
    
    def __init__(self,entry):
        self.entry = entry
        self.gui = None
    
    def close(self,event=None):
        self.get_gui().close()
    
    def get_gui(self):
        if self.gui is None:
            self.set_gui()
        return self.gui
    
    def set_gui(self):
        self.gui = gi.Suggest()
    
    def select(self,event=None):
        self._select()
        objs.get_webframe().go()
        
    def _select(self,event=None):
        ''' #NOTE: this works differently in Windows and Linux.
            In Windows selecting an item will hide suggestions,
            in Linux they will be kept open.
        '''
        f = '[MClient] mclient.Suggest._select'
        if self.gui.parent:
            self.entry.clear_text()
            self.entry.insert(text=self.gui.lbox.get())
            self.entry.select_all()
            self.entry.focus()
        else:
            sh.com.rep_empty(f)
        
    def move_down(self,event=None):
        f = '[MClient] mclient.Suggest.move_down'
        if self.get_gui().parent:
            # Necessary to use arrows on ListBox
            self.gui.lbox.focus()
            self.gui.lbox.index_add()
            self.gui.lbox.select()
            self._select()
        else:
            sh.com.rep_empty(f)
        
    def move_up(self,event=None):
        f = '[MClient] mclient.Suggest.move_up'
        if self.get_gui().parent:
            # Necessary to use arrows on ListBox
            self.gui.lbox.focus()
            self.gui.lbox.index_subtract()
            self.gui.lbox.select()
            self._select()
        else:
            sh.com.rep_empty(f)
        
    def move_top(self,event=None):
        f = '[MClient] mclient.Suggest.move_top'
        if self.get_gui().parent:
            # Necessary to use arrows on ListBox
            self.gui.lbox.focus()
            self.gui.lbox.move_top()
            self._select()
        else:
            sh.com.rep_empty(f)
                          
    def move_bottom(self,event=None):
        f = '[MClient] mclient.Suggest.move_bottom'
        if self.get_gui().parent:
            # Necessary to use arrows on ListBox
            self.gui.lbox.focus()
            self.gui.lbox.move_bottom()
            self._select()
        else:
            sh.com.rep_empty(f)
    
    def suggest(self,event=None):
        f = '[MClient] mclient.Suggest.suggest'
        self.get_gui()
        if sh.lg.globs['bool']['Autocompletion'] and event:
            text = self.entry.get()
            #TODO: avoid modifiers
            if text:
                ''' - Retrieving suggestions online is very slow, so we
                      just do this after a space. We may bind this
                      procedure to '<space>' as well, however, we also
                      would like to hide suggestions if there is no text
                      present in 'search_field', so we bind to
                      '<KeyRelease>'.
                    - For some reason, 'event.char' is always empty here
                      in Python 3.7.3.
                '''
                if event.keysym == 'space':
                    text = lg.com.suggest (search = text
                                          ,limit = 35
                                          )
                    if text:
                        self.gui.close()
                        self.gui.show (lst = list(text)
                                      ,action = self._select
                                      )
                        self.set_bindings()
                        sh.objs.get_root().update_idle()
                        sh.AttachWidget (obj1 = self.entry
                                        ,obj2 = self.gui.parent
                                        ,anchor = 'NE'
                                        ).run()
                    else:
                        sh.com.rep_empty(f)
            else:
                self.gui.close()
    
    def set_bindings(self):
        if self.get_gui().parent:
            sh.com.bind (obj = self.gui.parent
                        ,bindings = '<ButtonRelease-1>'
                        ,action = self.select
                        )



objs = Objects()
com = Commands()


if  __name__ == '__main__':
    f = '[MClient] mclient.__main__'
    sh.com.start()
    lg.objs.get_plugins(Debug=False,maxrows=1000)
    lg.objs.get_default(gi.PRODUCT)
    if lg.objs.default.Success:
        run_timed_update()
        objs.get_webframe().reset()
        objs.webframe.show()
        lg.objs.plugins.quit()
        kl.keylistener.cancel()
    else:
        mes = _('Unable to continue due to an invalid configuration.')
        sh.objs.get_mes(f,mes).show_warning()
    lg.objs.get_order().save()
    lg.com.save_config()
    mes = _('Goodbye!')
    sh.objs.get_mes(f,mes,True).show_debug()
    sh.com.end()
