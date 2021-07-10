#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.shared as sh
import plugins.multitrancom.utils.subjects.groups as gr
import plugins.multitrancom.subjects as sj


class Check:
    
    def __init__(self):
        self.Success = True
    
    def _has_title_en(self,title):
        for key in sj.SUBJECTS.keys():
            if title == sj.SUBJECTS[key]['en']['title']:
                return True
    
    def get_missing_subjects(self):
        f = 'plugins.multitrancom.utils.subjects.check.Check.get_missing_subjects'
        if self.Success:
            missing = []
            for row in gr.SUBJECTS:
                for subject in row:
                    if not self._has_title_en(subject):
                        missing.append(subject)
            if missing:
                sub = '\n'.join(sorted(set(missing)))
                mes = _('Those subjects ({}) were not found:')
                mes = mes.format(len(missing))
                mes += '\n\n' + sub
                sh.com.run_fast_debug(f,mes)
        else:
            sh.com.cancel(f)
    
    def _search_major(self,major):
        for key in sj.SUBJECTS.keys():
            if sj.SUBJECTS[key]['is_major'] \
            and sj.SUBJECTS[key]['en']['title'] == major:
                return True
    
    def get_missing_majors(self):
        f = 'plugins.multitrancom.utils.subjects.check.Check.get_missing_majors'
        if self.Success:
            majors = gr.objs.get_groups().get_majors()
            if majors:
                missing = []
                for major in majors:
                    if not self._search_major(major):
                        missing.append(major)
                if missing:
                    sub = '\n'.join(sorted(set(missing)))
                    mes = _('Those major subjects ({}) were not found:')
                    mes = mes.format(len(missing))
                    mes += '\n\n' + sub
                    sh.com.run_fast_debug(f,mes)
            else:
                self.Success = False
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.get_missing_majors()
        self.get_missing_subjects()