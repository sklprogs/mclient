#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.shared as sh

import controller as ct


class External:
    
    def get_group(self,subject=''):
        # A dummy output
        return ('Информационная безопасность'
               ,'Компьютерная техника'
               ,'Техника'
               )
    
    def get_majors(self):
        # A dummy output
        return ('Информационная безопасность','Компьютерная техника')
    
    def get_priorities(self):
        #return ('1','2','3','4','5','Subject1','Компьютерная техника','Общая лексика')
        #return [i for i in range(1000)]
        ''' #NOTE: All items should be preconverted to a string,
            otherwise, there will be no matches while unprioritizing.
        '''
        return [str(i) for i in range(40)]
    
    def get_all_subjects(self):
        lst = ['Биология','Информационная безопасность'
              ,'Компьютерная техника','Общая лексика','Техника'
              ]
        lst_num = ['s' + str(i) for i in range(50)]
        return lst + lst_num
    
    def get_article_subjects(self):
        return('Компьютерная техника','Общая лексика','Техника')


if __name__ == '__main__':
    f = '[MClient] subjects.priorities.tests.External.__main__'
    sh.com.start()
    iext = External()
    iprior = ct.Priorities (lst1 = iext.get_priorities()
                           ,lst2 = iext.get_all_subjects()
                           ,art_subjects = iext.get_article_subjects()
                           ,majors = iext.get_majors()
                           ,func_group = iext.get_group
                           )
    iprior.show()
    sh.com.end()
