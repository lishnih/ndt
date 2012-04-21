#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-12

from pyramid.security import Allow, Everyone, Authenticated


class RootFactory(object):
    __acl__ = [
                (Allow, Everyone,       'all'),
                (Allow, Authenticated,  'member'),
                (Allow, 'group:admins', 'admin'),
              ]

    def __init__(self, request):
        pass


USERS = {
            'admin':    'admin',
            'stan':     '',
            'qc1':      '',
            'qc2':      '',
            'welding1': '',
            'welding2': '',
            'ndt1':     '',
            'ndt2':     '',
        }


GROUPS = {
            'admin':    ['group:admins'],
            'stan':     ['group:qc', 'group:phase1', 'group:phase2'],
            'qc1':      ['group:qc', 'group:phase1'],
            'qc2':      ['group:qc', 'group:phase2'],
            'welding1': ['group:qc', 'group:phase1'],
            'welding2': ['group:qc', 'group:phase2'],
            'ndt1':     ['group:qc', 'group:phase1'],
            'ndt2':     ['group:qc', 'group:phase2'],
         }


def groupfinder(userid, request):
    if userid in USERS:
        return GROUPS.get(userid, [])
