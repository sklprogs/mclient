#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from sources.stardict.tags import Tags as stTags


class Tags(stTags):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.source = 'Fora (StarDict-x)'