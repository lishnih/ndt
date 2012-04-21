#!/usr/bin/env python
# coding=utf-8
# Stan 2012-02-12

from pyramid.view import view_config
from pyramid.response import Response
from pyramid.security import authenticated_userid

from ..security_db import user_db_url_iter, get_user_session, user_table_iter, get_user_table_data


@view_config(route_name='hello')
def my_hello(request):
    return Response('Hello %(name)s!' % request.matchdict)


@view_config(route_name='test', renderer='ndt:templates/base.pt')
def view_test(request):
    logged_in = authenticated_userid(request)

#   body = request.matchdict

    from pyramid_debugtoolbar.repr import DebugReprGenerator
    gen = DebugReprGenerator()
    body = gen.dump_object(request)

    title = u'Test'
    return dict(title=title, body=body, debug='', logged_in=logged_in)


@view_config(route_name='currentuser', renderer='ndt:templates/base.pt', permission='member')
def view_currentuser(request):
    logged_in = authenticated_userid(request)

    body = u''
    if logged_in:
        body += u'Сессия пользователя: {}<br />\n'.format(repr(get_user_session(logged_in)).replace('<', '&lt;').replace('>', '&gt;'))
        body += u'Параметры БД: {}<br />\n'.format(repr([x for x, y in user_db_url_iter(logged_in)]))
        for table in user_table_iter(logged_in):
            body += u'{}: {!r}<br />\n'.format(table, '...')  # get_user_table_data(logged_in, table)

    title = u'User Info'
    return dict(title=title, body=body, debug='', logged_in=logged_in)


@view_config(route_name='user', renderer='ndt:templates/base.pt', permission='admin')
def view_user(request):
    logged_in = authenticated_userid(request)

    from pyramid_debugtoolbar.repr import DebugReprGenerator
    gen = DebugReprGenerator()
    body = gen.dump_object(request)

    title = u'User Test'
    return dict(title=title, body=body, debug='', logged_in=logged_in)
