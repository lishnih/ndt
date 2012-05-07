#!/usr/bin/env python
# coding=utf-8
# Stan 2012-02-26

import json


def ri_get_str(request_items, name, default = ''):
    return request_items.get(name, default)


def ri_get_int(request_items, name, default = 0):
    atom = ri_get_str(request_items, name)
    try:
        return int(atom)
    except ValueError:
        return default


def ri_get_tuple(request_items, name, default = ()):
    atom = ri_get_str(request_items, name)
    if not atom:
        return default
    return tuple(atom.split('|'))


def ri_get_obj(request_items, name, default = {}):
    atom_json = ri_get_str(request_items, name)
    if not atom_json:
        return default
    try:
        return json.loads(atom_json)
    except ValueError, e:
        return default


def get_action(request, response=None):
    action = None
    request_items = None

    if   'action' in request.POST:
        request_items = request.POST
    elif 'action' in request.GET:
        request_items = request.GET

    if request_items:
        action = ri_get_str(request_items, 'action')

        if response:
            response['action'] = action

            if 'sEcho' in request_items:
                response['sEcho'] = ri_get_int(request_items, 'sEcho', 1)

    return action, request_items
