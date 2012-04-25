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
