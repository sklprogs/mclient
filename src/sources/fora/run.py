#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep

from sources.fora.get import ALL_DICS
import sources.fora.stardict0.cleanup
import sources.fora.stardict0.elems
import sources.fora.dsl.cleanup
import sources.fora.dsl.tags
import sources.fora.dsl.elems
import sources.stardict.cleanup
import sources.stardict.tags
import sources.fora.stardictx.elems


class Source:
    
    def __init__(self):
        ''' - Extra unused input variables are preserved so it would be easy to
              use an abstract class for all dictionary sources.
            - #NOTE: 'Parallel' and 'Separate' are temporary variables that
              should be externally referred to only after getting a NEW article.
        '''
        self.Parallel = False
        self.Separate = False
        self.name = 'Fora'
    
    def is_parallel(self):
        return self.Parallel
    
    def is_separate(self):
        return self.Separate
    
    def get_subjects(self):
        #TODO: implement
        return []
    
    def fix_url(self, url):
        # This is needed only for compliance with a general method
        return url
    
    def get_title(self, short):
        #TODO: implement
        return short
    
    def quit(self):
        ALL_DICS.close()
    
    def get_server(self):
        # This is needed only for compliance with a general method
        return ''
    
    def count_valid(self):
        return len(ALL_DICS.get_valid())
    
    def count_invalid(self):
        return len(ALL_DICS.get_invalid())
    
    def suggest(self, search):
        #TODO: implement
        return []
    
    def _request_stardictx(self, dic):
        text = sources.stardict.cleanup.CleanUp(dic.article).run()
        blocks = sources.stardict.tags.Tags(text).run()
        return sources.fora.stardictx.elems.Elems(blocks).run()
    
    def _request_stardict0(self, dic):
        text = sources.fora.stardict0.cleanup.CleanUp(dic.article).run()
        return sources.fora.stardict0.elems.Elems(text, dic.pattern, dic.get_name()).run()
    
    def _request_stardicth(self, dic):
        text = sources.fora.stardicth.cleanup.CleanUp(dic.article).run()
        blocks = sources.fora.stardicth.tags.Tags(text).run()
        return sources.fora.stardicth.elems.Elems(blocks).run()
    
    def _request_stardictm(self, dic):
        text = sources.fora.stardictm.cleanup.CleanUp(dic.article).run()
        blocks = sources.fora.stardictm.tags.Tags(text).run()
        return sources.fora.stardictm.elems.Elems(blocks).run()
    
    def _request_dsl(self, dic):
        text = sources.fora.dsl.cleanup.CleanUp(dic.article).run()
        blocks = sources.fora.dsl.tags.Tags(text).run()
        return sources.fora.dsl.elems.Elems(blocks).run()
    
    def _request_xdxf(self, dic):
        text = sources.fora.xdxf.cleanup.CleanUp(dic.article).run()
        blocks = sources.fora.xdxf.tags.Tags(text).run()
        return sources.fora.xdxf.elems.Elems(blocks).run()
    
    def _request_dictd(self, dic):
        text = sources.fora.dictd.cleanup.CleanUp(dic.article).run()
        blocks = sources.fora.dictd.tags.Tags(text).run()
        return sources.fora.dictd.elems.Elems(blocks).run()
    
    def _join_blocks(self, groups):
        f = '[MClient] sources.fora.run.Source._join_blocks'
        if not groups:
            rep.empty(f)
            return []
        if not groups[0]:
            rep.wrong_input(f)
            return []
        delta = 0
        i = 1
        while i < len(groups):
            delta += groups[i-1][-1].cellno
            for block in groups[i]:
                block.cellno = block.cellno + delta
            i += 1
        blocks = []
        for group in groups:
            blocks += group
        return blocks
    
    def request(self, search='', url=''):
        f = '[MClient] sources.fora.run.Source.request'
        ALL_DICS.search(search)
        text = ''
        blocks = []
        for dic in ALL_DICS.dics:
            if not dic.Success or not dic.article:
                continue
            text += dic.article + '\n\n'
            ''' It is not necessary to warn about the format here, since
                the format support is already checked by
                sources.fora.get.Properties.check_format.
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
        blocks = [result for result in blocks if result]
        blocks = self._join_blocks(blocks)
        #TODO: Implement or drop
        #self.Parallel = ielems.Parallel
        #self.Separate = ielems.Separate
        return blocks
