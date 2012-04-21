#!/usr/bin/env python
# coding=utf-8
# Stan 2012-01-26

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config


@view_config(route_name='root')
def view_root(request):
    return HTTPFound(location = request.route_url('view_wiki'))
