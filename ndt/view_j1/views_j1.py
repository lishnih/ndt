#!/usr/bin/env python
# coding=utf-8
# Stan 2012-02-04

import logging

from pyramid.view import view_config
from pyramid.security import authenticated_userid

from .view_j1_help import *
from .view_j1_funcs import *


@view_config(route_name='j1', renderer='json')
def view_j1(request):
    response = dict(
        version = 1,
        request_get  = repr(request.GET),
        request_post = repr(request.POST),
    )


    logged_in = authenticated_userid(request)
    if not logged_in:
        response['content_type'] = 'error'
        response['content'] = u'Необходима авторизация!'
        return response


    if   'action' in request.POST:
        request_items = request.POST
    elif 'action' in request.GET:
        request_items = request.GET
    else:
        response['content_type'] = 'error'
        response['content'] = u'Нет запроса!'
        return response


    action = request_items.get('action')
    response['action'] = action


# view_j1_help

    if   action == 'actions_list':
        actions_list_action(request_items, response)

    elif action == 'help':
        action_help(request_items, response)


# view_j1_funcs

    elif action == 'tables_list':
        tables_list_action(logged_in, request_items, response)

    elif action == 'columns_list':
        columns_list_action(logged_in, request_items, response)

    elif action == 'table_info':
        table_info_action(logged_in, request_items, response)

    elif action == 'table_count':
        table_count_action(logged_in, request_items, response)

    elif action == 'table_view':
        table_view_action(logged_in, request_items, response)

    elif action == 'column_district':
        column_district_action(logged_in, request_items, response)


    else:
        response['content_type'] = 'error'
        response['content'] = u'Запрос не опознан!'

    return response
