#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep

from plugins.fora.get import Get, ALL_DICS
import plugins.fora.stardict0.cleanup
import plugins.fora.stardict0.elems
import plugins.stardict.cleanup
import plugins.stardict.tags
import plugins.stardict.elems
import plugins.fora.dsl.cleanup
import plugins.fora.dsl.tags
import plugins.fora.dsl.elems


class Plugin:
    
    def __init__(self, Debug=False, maxrows=1000):
        ''' Extra unused input variables are preserved so it would be easy to
            use an abstract class for all dictionary sources.
        '''
        self.set_values()
        self.Debug = Debug
        self.maxrows = maxrows
    
    def set_values(self):
        ''' #NOTE: 'fixed_urls', 'art_subj', 'Parallel' and 'Separate' are
            temporary variables that should be externally referred to only
            after getting a NEW article.
        '''
        self.Parallel = False
        self.Separate = False
        self.majors = []
        self.minors = []
        self.fixed_urls = {}
        self.art_subj = {}
        self.htm = ''
        self.text = ''
        self.search = ''
    
    def is_parallel(self):
        return self.Parallel
    
    def is_separate(self):
        return self.Separate
    
    def get_speeches(self):
        return {}
    
    def get_minors(self):
        return self.minors
    
    def get_fixed_urls(self):
        return self.fixed_urls
    
    def get_htm(self):
        return self.htm
    
    def get_text(self):
        return self.text
    
    def get_article_subjects(self):
        return self.art_subj
    
    def get_subjects(self):
        #TODO: implement
        return []
    
    def get_group_with_header(self, subject=''):
        #TODO: implement
        return []
    
    def get_majors(self):
        #TODO: implement
        return []
    
    def get_search(self):
        return self.search
    
    def set_htm(self, code):
        # This is needed only for compliance with a general method
        self.htm = code
    
    def fix_url(self, url):
        # This is needed only for compliance with a general method
        return url
    
    def is_oneway(self):
        return True
    
    def get_title(self, short):
        #TODO: implement
        return short
    
    def quit(self):
        ALL_DICS.close()
    
    def get_lang1(self):
        # This is needed only for compliance with a general method
        return _('Any')
    
    def get_lang2(self):
        # This is needed only for compliance with a general method
        return _('Any')
    
    def get_server(self):
        # This is needed only for compliance with a general method
        return ''
    
    def fix_raw_htm(self, code=''):
        # This is needed only for compliance with a general method
        return self.htm
    
    def get_url(self, search=''):
        # This is needed only for compliance with a general method
        return ''
    
    def set_lang1(self, lang1=''):
        # This is needed only for compliance with a general method
        pass
    
    def set_lang2(self, lang2=''):
        # This is needed only for compliance with a general method
        pass
    
    def set_timeout(self, timeout=0):
        # This is needed only for compliance with a general method
        pass
    
    def get_langs1(self, lang2=''):
        # This is needed only for compliance with a general method
        return(_('Any'),)
    
    def get_langs2(self, lang1=''):
        # This is needed only for compliance with a general method
        return(_('Any'),)
    
    def is_combined(self):
        # Whether or not the plugin is actually a wrapper over other plugins
        return True
    
    def count_valid(self):
        return len(ALL_DICS.get_valid())
    
    def count_invalid(self):
        return len(ALL_DICS.get_invalid())
    
    def suggest(self, search):
        #TODO: implement
        return []
    
    def _request_stardictx(self, dic):
        text = plugins.stardict.cleanup.CleanUp(dic.article).run()
        blocks = plugins.stardict.tags.Tags(text).run()
        return plugins.stardict.elems.Elems(blocks).run()
    
    def _request_stardict0(self, dic):
        text = plugins.fora.stardict0.cleanup.CleanUp(dic.article).run()
        return plugins.fora.stardict0.elems.Elems(text, dic.pattern, dic.get_name()).run()
    
    def _request_stardicth(self, dic):
        text = plugins.fora.stardicth.cleanup.CleanUp(dic.article).run()
        blocks = plugins.fora.stardicth.tags.Tags(text).run()
        return plugins.fora.stardicth.elems.Elems(blocks).run()
    
    def _request_stardictm(self, dic):
        text = plugins.fora.stardictm.cleanup.CleanUp(dic.article).run()
        blocks = plugins.fora.stardictm.tags.Tags(text).run()
        return plugins.fora.stardictm.elems.Elems(blocks).run()
    
    def _request_dsl(self, dic):
        text = plugins.fora.dsl.cleanup.CleanUp(dic.article).run()
        blocks = plugins.fora.dsl.tags.Tags(text).run()
        return plugins.fora.dsl.elems.Elems(blocks).run()
    
    def _request_xdxf(self, dic):
        text = plugins.fora.xdxf.cleanup.CleanUp(dic.article).run()
        blocks = plugins.fora.xdxf.tags.Tags(text).run()
        return plugins.fora.xdxf.elems.Elems(blocks).run()
    
    def _request_dictd(self, dic):
        text = plugins.fora.dictd.cleanup.CleanUp(dic.article).run()
        blocks = plugins.fora.dictd.tags.Tags(text).run()
        return plugins.fora.dictd.elems.Elems(blocks).run()
    
    def _join_cells(self, cells):
        f = '[MClient] plugins.fora.run.Plugin._join_cells'
        if not cells:
            rep.empty(f)
            return []
        if not cells[0] or not cells[0][-1].blocks:
            rep.wrong_input(f)
            return []
        no = cells[0][-1].no + 1
        rowno = cells[0][-1].rowno + 1
        cellno = cells[0][-1].blocks[-1].cellno + 1
        i = 1
        while i < len(cells):
            for cell in cells[i]:
                cell.no = no
                cell.rowno = rowno
                no += 1
                rowno += 1
                for block in cell.blocks:
                    block.cellno = cellno
                    cellno += 1
            i += 1
        result = []
        for items in cells:
            result += items
        return result
    
    def request(self, search='', url=''):
        f = '[MClient] plugins.fora.run.Plugin.request'
        self.search = search
        ALL_DICS.search(self.search)
        text = ''
        cells = []
        for dic in ALL_DICS.dics:
            if not dic.Success or not dic.article:
                continue
            text += dic.article + '\n\n'
            ''' It is not necessary to warn about the format here, since
                the format support is already checked by
                plugins.fora.get.Properties.check_format.
            '''
            match dic.get_format():
                case 'stardict-x':
                    cells.append(self._request_stardictx(dic))
                case 'dsl':
                    cells.append(self._request_dsl(dic))
                case 'stardict-0':
                    cells.append(self._request_stardict0(dic))
                case 'stardict-h':
                    cells.append(self._request_stardicth(dic))
                case 'stardict-m':
                    cells.append(self._request_stardictm(dic))
                case 'xdxf':
                    cells.append(self._request_xdxf(dic))
                case 'dictd':
                    cells.append(self._request_dictd(dic))
        self.htm = self.text = text
        cells = [result for result in cells if result]
        cells = self._join_cells(cells)
        #TODO: Implement or drop
        #self.fixed_urls = ielems.fixed_urls
        #self.art_subj = ielems.art_subj
        #self.Parallel = ielems.Parallel
        #self.Separate = ielems.Separate
        return cells
