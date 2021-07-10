#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.shared as sh
import plugins.multitrancom.utils.subjects.groups as gr
import plugins.multitrancom.subjects as sj


class Check:
    
    def __init__(self):
        self.Success = True
    
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
                    sub = '\n'.join(missing)
                    mes = _('Those major subjects were not found:')
                    mes += '\n\n' + sub
                    sh.com.run_fast_debug(f,mes)
            else:
                self.Success = False
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.get_missing_majors()
