#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-12

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, forbidden_view_config
from pyramid.security import remember, forget

from .security import USERS


@view_config(route_name='login', renderer='ndt:templates/login.pt')
@forbidden_view_config(renderer='ndt:templates/login.pt')
def login(request):
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/' # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        if USERS.get(login) == password:
            headers = remember(request, login)
            return HTTPFound(location = came_from, headers = headers)
        message = 'Failed login'

    return dict(
        message = message,
        url = request.application_url + '/login',
        came_from = came_from,
        login = login,
        password = password,
        )


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location = request.route_url('root'), headers = headers)
