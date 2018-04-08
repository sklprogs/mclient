#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import html
import shared as sh

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('shared','../resources/locale')


class Topics:
    
    def __init__(self):
        self.values()
        
    def values(self):
        self.Success    = True
        self._list_file = '/tmp/topics'
        self._url       = 'https://www.multitran.ru/c/m.exe?a=112&l1=1&l2=2'
        self._html      = ''
        self._list      = []
        self._titles    = []
        self._abbrs     = []
        
    def get_list(self):
        if self.Success:
            read         = sh.ReadTextFile(file=self._list_file)
            self._list   = read.get()
            self.Success = read.Success
            self._list   = sh.Input (func_title = 'Topics.get_list'
                                    ,val        = self._list
                                    ).not_none()
            self._list = self._list.splitlines()
        else:
            sh.log.append ('Topics.get_list'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def run(self):
        self.get_list()
        self.get_html()
        self.tags()
        
    def get_html(self):
        if self.Success:
            self._html = sh.Get (url      = self._url
                                ,encoding = 'windows-1251'
                                ).run()
            if not self._html:
                self.Success = False
                sh.log.append ('Topics.get_html'
                              ,_('WARNING')
                              ,_('Empty output is not allowed!')
                              )
        else:
            sh.log.append ('Topics.get_html'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
                          
    def tags(self):
        if self.Success:
            tags = Tags (text   = self._html
                        ,search = '<a href="m.exe?a='
                        )
            tags.run()
            self.Success = tags.Success
            if self.Success:
                for i in range(len(tags._urls)):
                    abbr = Abbr (url   = tags._urls[i]
                                ,title = tags._titles[i]
                                )
                    abbr.run()
                    if len(abbr._titles) == len(abbr._abbrs):
                        for i in range(len(abbr._abbrs)):
                            if not abbr._abbrs[i] in self._abbrs:
                                self._abbrs.append(abbr._abbrs[i])
                                self._titles.append(abbr._titles[i])
                    else:
                        #todo: Should we toggle 'self.Success' here?
                        #self.Success = False
                        sh.objs.mes ('Topics.tags'
                                    ,_('WARNING')
                                    ,_('The condition "%s" is not observed!') \
                                    % '%d == %d' % (len(abbr._titles)
                                                   ,len(abbr._abbrs)
                                                   )
                                    )
            else:
                sh.log.append ('Topics.tags'
                              ,_('WARNING')
                              ,_('Operation has been canceled.')
                              )
        else:
            sh.log.append ('Topics.tags'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )



class Abbr:
    
    def __init__(self,url,title):
        self.values()
        self._url   = url
        self._title = title
        if self._url and self._title:
            self.Success = True
        else:
            self.Success = False
            sh.log.append ('Abbr.__init__'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
                          
    def debug(self):
        if self.Success:
            text = ''
            for i in range(len(self._abbrs)):
                text += '%d: "%s": "%s"\n' % (i,self._titles[i]
                                             ,self._abbrs[i]
                                             )
            return text
        else:
            sh.log.append ('Abbr.debug'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def values(self):
        self._html   = ''
        self._html2  = ''
        self._url2   = ''
        self._titles = []
        self._abbrs  = []
                          
    def get(self):
        if self.Success:
            self._html = sh.Get (url      = self._url
                                ,encoding = 'windows-1251'
                                ).run()
            if not self._html:
                self.Success = False
                sh.log.append ('Abbr.get'
                              ,_('WARNING')
                              ,_('Empty output is not allowed!')
                              )
        else:
            sh.log.append ('Abbr.get'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def get2(self):
        if self.Success:
            self._html2 = sh.Get (url      = self._url2
                                 ,encoding = 'windows-1251'
                                 ).run()
            if not self._html2:
                self.Success = False
                sh.log.append ('Abbr.get2'
                              ,_('WARNING')
                              ,_('Empty output is not allowed!')
                              )
        else:
            sh.log.append ('Abbr.get2'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def tags(self):
        if self.Success:
            tags = Tags (text   = self._html
                        ,search = '<a href="m.exe?t='
                        )
            tags.run()
            self.Success = tags.Success
            if self.Success:
                if tags._urls and tags._urls[0]:
                    ''' #todo: try all URLs instead of the 1st one
                        (a Multitran's bug: some links may lead to
                        different dictionary titles).
                    '''
                    self._url2 = tags._urls[0]
                    ''' Avoid a Multitran's bug: the site generates URLs
                        with tabs, which cannot be downloaded. However,
                        those URLs work fine if tabs are deleted.
                    '''
                    self._url2 = self._url2.replace('\t','')
                else:
                    sh.log.append ('Abbr.tags'
                                  ,_('WARNING')
                                  ,_('Empty input is not allowed!')
                                  )
            else:
                sh.log.append ('Abbr.tags'
                              ,_('WARNING')
                              ,_('Operation has been canceled.')
                              )
        else:
            sh.log.append ('Abbr.tags'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def tags2(self):
        if self.Success:
            ''' Replace this so that 'Tags' would not treat this as
                a new tag.
            '''
            self._html2 = self._html2.replace('<i>','')
            tags = Tags (text   = self._html2
                        ,search = '<a title="'
                        )
            tags.run()
            self.Success = tags.Success
            if self.Success:
                self._titles = tags._urls
                self._abbrs  = tags._titles
            else:
                sh.log.append ('Abbr.tags2'
                              ,_('WARNING')
                              ,_('Operation has been canceled.')
                              )
        else:
            sh.log.append ('Abbr.tags2'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def titles(self):
        if self.Success:
            for i in range(len(self._titles)):
                if self._titles[i]:
                    self._titles[i] = self._titles[i].replace('<a title="','')
                    pos = sh.Search (text   = self._titles[i]
                                    ,search = '" href'
                                    ).next()
                    pos = sh.Input (func_title = 'Abbr.titles'
                                   ,val        = pos
                                   ).integer()
                    self._titles[i] = self._titles[i][:pos]
                    self._titles[i] = self._titles[i].strip()
                else:
                    sh.log.append ('Abbr.titles'
                                  ,_('WARNING')
                                  ,_('Empty input is not allowed!')
                                  )
        else:
            sh.log.append ('Abbr.titles'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def abbrs(self):
        if self.Success:
            for i in range(len(self._abbrs)):
                self._abbrs[i] = self._abbrs[i].replace('<i>','').replace('</i>','')
                self._abbrs[i] = self._abbrs[i].strip()
        else:
            sh.log.append ('Abbr.abbrs'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def run(self):
        self.get()
        self.tags()
        self.get2()
        self.tags2()
        self.titles()
        self.abbrs()



class Tags:
    
    def __init__(self,text,search='<a href="m.exe?a='):
        self.values()
        self.text   = text
        self.search = search
        if not self.text:
            self.Success = False
            sh.log.append ('Tags.__init__'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
        
    def values(self):
        self.Success = True
        self._tags   = []
        self._titles = []
        self._urls   = []
        self._start  = []
        self._end    = []
        
    def equalize(self):
        if self.Success:
            if len(self._end) > len(self._start):
                tmp = []
                for i in range(len(self._start)):
                    while self._start[i] > self._end[i]:
                        del self._end[i]
                    tmp.append(self._end[i])
                self._end = tmp
            else:
                sh.log.append ('Tags.equalize'
                              ,_('INFO')
                              ,_('Nothing to do!')
                              )
        else:
            sh.log.append ('Tags.equalize'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def split(self):
        if self.Success:
            self._start = sh.Search (text   = self.text
                                    ,search = self.search
                                    ).next_loop()
            self._end   = sh.Search (text   = self.text
                                    ,search = '</a>'
                                    ).next_loop()
            self.equalize()
            if len(self._start) == len(self._end):
                for i in range(len(self._start)):
                    self._tags.append(self.text[self._start[i]:self._end[i]])
            else:
                self.Success = False
                sh.objs.mes ('Tags.split'
                            ,_('WARNING')
                            ,_('The condition "%s" is not observed!') \
                            % '%d == %d' % (len(self._start)
                                           ,len(self._end)
                                           )
                            )
        else:
            sh.log.append ('Tags.split'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
                          
    def trash_urls(self):
        if self.Success:
            for i in range(len(self._urls)):
                if self._urls[i]:
                    self._urls[i] = self._urls[i].replace('<a href="m.exe?','https://www.multitran.ru/c/m.exe?')
                    if self._urls[i].endswith('"'):
                        self._urls[i] = self._urls[i][:-1]
                    else:
                        sh.log.append ('Tags.trash_urls'
                                      ,_('WARNING')
                                      ,_('Wrong input data: "%s"!') \
                                      % str(self._urls[i])
                                      )
                else:
                    sh.log.append ('Tags.trash_urls'
                                  ,_('WARNING')
                                  ,_('Empty input is not allowed!')
                                  )
        else:
            sh.log.append ('Tags.trash_urls'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )

    def trash_titles(self):
        if self.Success:
            for i in range(len(self._titles)):
                self._titles[i] = html.unescape(self._titles[i])
        else:
            sh.log.append ('Tags.trash_titles'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def links(self):
        if self.Success:
            for tag in self._tags:
                pos = sh.Search (text   = tag
                                ,search = '>'
                                ).next()
                pos = sh.Input (func_title = 'Tags.links'
                               ,val        = pos
                               ).integer()
                self._urls.append(tag[:pos])
                self._titles.append(tag[pos+1:])
        else:
            sh.log.append ('Tags.links'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
        
    def debug(self):
        if self.Success:
            text = ''
            for i in range(len(self._urls)):
                text += '%d: "%s": "%s"\n' % (i,self._urls[i]
                                             ,self._titles[i]
                                             )
            return text
        else:
            sh.log.append ('Tags.debug'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def run(self):
        self.split()
        self.links()
        self.trash_urls()
        self.trash_titles()



class Commands:
    
    def get_abbrs(self):
        topics = Topics()
        topics.run()
        if topics._abbrs and topics._titles:
            text = ''
            for i in range(len(topics._abbrs)):
                text += topics._abbrs[i] + '\t' + topics._titles[i] + '\n'
            sg.objs.txt().reset_data()
            sg.objs._txt.title(_('Abbreviations:'))
            sg.objs._txt.insert(text)
            sg.objs._txt.show()
        else:
            sh.log.append ('Commands.get_abbrs'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
                          
    def select_abbrs(self):
        ''' This is a list of dictionaries from
            https://www.multitran.ru/c/m.exe?a=112&l1=1&l2=2.
        '''
        file1 = '/tmp/topics'
        ''' This is basically data generated by 'Commands.get_abbrs'
            with some trash deleted. 'dic.orig' - dictionary
            abbreviations, 'dic.transl' - full titles.
        '''
        file2 = '/tmp/abbrs'
        topics = sh.ReadTextFile(file=file1).get()
        dic  = sh.Dic (file     = file2
                      ,Sortable = True
                      )
        if topics and dic.orig and dic.transl:
            i = 0
            count = 0
            while i < len(dic.orig):
                ''' Multitran proposes only one full dictionary title
                    even when several abbreviations are given, so we
                    need only one abbreviation per line.
                '''
                if '., ' in dic.orig[i]:
                    del dic.orig[i]
                    del dic.transl[i]
                    count += 1
                    i -= 1
                i += 1
            sh.log.append ('Commands.select_abbrs'
                          ,_('INFO')
                          ,_('%d duplicates have been deleted') % count
                          )
            dic.orig, dic.transl = (list(x) for x \
            in zip (*sorted (zip (dic.orig, dic.transl)
                            ,key = lambda x:x[0].lower()
                            )
                   )
                                   )
            message = ''
            timer = sh.Timer('string concatenation') #todo: del
            timer.start() #todo: del
            for i in range(len(dic.orig)):
                message += dic.orig[i] + '\t' + dic.transl[i] + '\n'
            timer.end() #todo: del
            sh.objs.mes ('Commands.select_abbrs'
                        ,_('INFO')
                        ,message
                        )
            topics  = topics.splitlines()
            missing = []
            for i in range(len(topics)):
                topics[i] = topics[i].strip()
                if not topics[i] in dic.transl:
                    missing.append(topics[i])
            if missing:
                message = _('The following dictionary titles do not have abbreviations:')
                message += '\n'
                message += '\n'.join(missing)
                sh.objs.mes ('Commands.select_abbrs'
                            ,_('WARNING')
                            ,message
                            )
        else:
            sh.log.append ('Commands.select_abbrs'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
        


if __name__ == '__main__':
    import sharedGUI as sg
    sg.objs.start()
    #Commands().select_abbrs()
    abbr = Abbr (url   = 'https://www.multitran.ru/c/m.exe?a=110&sc=753&l1=1&l2=2'
                ,title = 'Астроспектроскопия'
                )
    abbr.run()
    text = abbr.debug()
    sg.objs.txt().reset_data()
    sg.objs._txt.insert(text)
    sg.objs._txt.show()
    sg.objs.end()
                
