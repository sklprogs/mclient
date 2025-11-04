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
import plugins.dsl.cleanup
import plugins.dsl.tags
import plugins.dsl.elems


class Plugin:
    
    def __init__(self):
        ''' - Extra unused input variables are preserved so it would be easy to
              use an abstract class for all dictionary sources.
            - #NOTE: 'Parallel' and 'Separate' are temporary variables that
              should be externally referred to only after getting a NEW article.
        '''
        self.Parallel = False
        self.Separate = False
        self.majors = []
        self.minors = []
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
    
    def get_htm(self):
        return self.htm
    
    def get_text(self):
        return self.text
    
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
        plugins.dsl.cleanup.FORA = True
        text = plugins.dsl.cleanup.CleanUp(dic.article).run()
        blocks = plugins.dsl.tags.Tags(text).run()
        return plugins.dsl.elems.Elems(blocks).run()
    
    def _request_xdxf(self, dic):
        text = plugins.fora.xdxf.cleanup.CleanUp(dic.article).run()
        blocks = plugins.fora.xdxf.tags.Tags(text).run()
        return plugins.fora.xdxf.elems.Elems(blocks).run()
    
    def _request_dictd(self, dic):
        text = plugins.fora.dictd.cleanup.CleanUp(dic.article).run()
        blocks = plugins.fora.dictd.tags.Tags(text).run()
        return plugins.fora.dictd.elems.Elems(blocks).run()
    
    def _join_blocks(self, groups):
        f = '[MClient] plugins.fora.run.Plugin._join_blocks'
        if not groups:
            rep.empty(f)
            return []
        if not groups[0]:
            rep.wrong_input(f)
            return []
        cellno = groups[0][-1].cellno + 1
        i = 1
        while i < len(groups):
            for block in groups[i]:
                block.cellno = cellno
                cellno += 1
            i += 1
        blocks = []
        for group in groups:
            blocks += group
        return blocks
    
    def request(self, search='', url=''):
        f = '[MClient] plugins.fora.run.Plugin.request'
        self.search = search
        ALL_DICS.search(self.search)
        text = ''
        blocks = []
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
                    blocks.append(self._request_stardictx(dic))
                case 'dsl':
                    blocks.append(self._request_dsl(dic))
                case 'stardict-0':
                    blocks.append(self._request_stardict0(dic))
                case 'stardict-h':
                    blocks.append(self._request_stardicth(dic))
                case 'stardict-m':
                    blocks.append(self._request_stardictm(dic))
                case 'xdxf':
                    blocks.append(self._request_xdxf(dic))
                case 'dictd':
                    blocks.append(self._request_dictd(dic))
        self.htm = self.text = text
        blocks = [result for result in blocks if result]
        blocks = self._join_blocks(blocks)
        #TODO: Implement or drop
        #self.Parallel = ielems.Parallel
        #self.Separate = ielems.Separate
        return blocks
