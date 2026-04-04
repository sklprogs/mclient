#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep

from sources.fora.get import ALL_DICS
import sources.dsl.cleanup
import sources.stardict.cleanup
import sources.fora.stardict0.cleanup
import sources.fora.stardict0.elems
import sources.fora.dsl.tags
import sources.fora.stardictx.tags
import sources.dsl.elems
import sources.stardict.elems


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
    
    def suggest(self, search, limit=0):
        return ALL_DICS.suggest(search, limit)
    
    def request(self, search):
        f = '[MClient] sources.fora.run.Source.request'
        blocks = []
        for article in ALL_DICS.search(search):
            blocks += self.get_blocks(article)
        #TODO: Implement or drop
        #self.Parallel = ielems.Parallel
        #self.Separate = ielems.Separate
        return blocks
    
    def _get_blocks_dsl(self, article):
        article.code = sources.dsl.cleanup.CleanUp(article.code).run()
        blocks = sources.fora.dsl.tags.Tags(article).run()
        return sources.dsl.elems.Elems(blocks).run()
    
    def _get_blocks_stardictx(self, article):
        article.code = sources.stardict.cleanup.CleanUp(article.code).run()
        blocks = sources.fora.stardictx.tags.Tags(article).run()
        return sources.stardict.elems.Elems(blocks).run()
    
    def get_blocks(self, article):
        f = '[MClient] sources.fora.run.Source.get_blocks'
        if not article:
            rep.empty(f)
            return []
        ''' The format support is already checked by
            sources.fora.get.Properties.check_format. The warning is kept for
            converters just to be safe.
        '''
        match article.format:
            case 'stardict-x':
                return self._get_blocks_stardictx(article)
            case 'dsl':
                return self._get_blocks_dsl(article)
            case other if True:
                mes = _('Format "{}" is not supported!').format(other)
                Message(f, mes).show_warning()
        return []