#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.graphics.root.controller import ROOT
from skl_shared.graphics.debug.controller import DEBUG as shDEBUG

from tests.sources import Get


if __name__ == '__main__':
    f = '[MClient] test.__main__'
    ROOT.get_root()
    ''' #NOTE: Putting QMainWindow.show() or QWidget.show() (without
        explicitly invoking QMainWindow in __main__) in a separate procedure,
        e.g. com.run_welcome, will cause an infinite loop.
    '''
    #mes = com.get_all_subjects()
    #mes = Subjects().run()
    #mes = Prioritize().run_multitrancom()
    #mes = CleanUp().run_dsl()
    mes = Get().run_dsl()
    #mes = Get().run_fora()
    #mes = Get().run_fora_many_matches()
    #mes = Get().run_mdic()
    #mes = Get().run_multitrancom()
    #mes = Get().run_multitrandem()
    #mes = Get().run_stardict()
    #mes = Tags().run_stardict()
    #mes = Tags().run_fora_stardictx()
    #mes = Tags().run_dsl()
    #mes = Tags().run_fora_dsl()
    #mes = Tags().run_multitrancom()
    #mes = Tags().run_stardict()
    #mes = Elems().run_dsl()
    #mes = Elems().run_mdic()
    #mes = Elems().run_stardict()
    #mes = Elems().run_stardict_cells()
    #mes = Elems().run_fora_stardictx()
    #mes = Elems().run_fora_dsl()
    #mes = Elems().run_fora()
    #mes = Elems().run_multitrandem()
    #mes = Elems().run_multitrancom()
    #mes = View().run_dsl()
    #mes = View().run_stardict()
    #mes = View().run_multitrancom()
    #mes = Wrap().run_multitrancom()
    #mes = Source().run_dsl()
    #mes = Source().run_fora()
    #mes = Source().run_mdic()
    #mes = Source().run_multitrancom()
    #mes = Source().run_multitrandem()
    #mes = Source().run_stardict()
    shDEBUG.reset(f, mes)
    shDEBUG.show()
    # This MUST be on a separate line, the widget will not be shown otherwise
    #idebug.show()
    #mes = com.run_speech()
    #Message(f, mes, True).show_debug()
    #isuggest = com.run_suggest()
    #isuggest.show()

    # Priorities
    #iprior = com.run_prior()
    #iprior.show()

    # Priorities (from the controller)
    #iprior = com.run_prior_contr()
    #iprior.show()

    '''
    # Popup
    ipopup = com.run_popup()
    ipopup.show()
    '''
    '''
    isave = com.run_save()
    isave.show()
    '''
    '''
    # Settings
    isettings = com.run_settings()
    isettings.show()
    '''
    '''
    # History
    ihis = com.run_history()
    ihis.show()
    '''
    '''
    # History (history.controller)
    ihis = com.run_history_contr()
    ihis.show()
    '''

    # Welcome
    #iwelcome = com.run_welcome()
    #iwelcome.show()

    mes = _('Goodbye!')
    Message(f, mes).show_debug()
    ROOT.end()
