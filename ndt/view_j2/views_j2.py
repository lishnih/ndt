#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-11

from pyramid.view import view_config
from pyramid.security import authenticated_userid

from .view_j2_help import *
from .view_j2_funcs import *


@view_config(route_name='j2', renderer='json')
def view_j2(request):
    import logging
    logging.warning(request.GET)
    logging.warning(request.POST)

    response = prepare_response(request)

    logged_in = authenticated_userid(request)
    if not logged_in:
        return response_with_message(response, u'Необходима авторизация!', 'error')

    response['user'] = logged_in

    action, request_items = get_action(request, response)
    if not action:
        return response_with_message(response, u'Нет запроса!', 'warning')


# view_j2_help

    if   action == 'actions_list':
        actions_list_action(request_items, response)

    elif action == 'action_params_list':
        action_params_list_action(request_items, response)


# view_j2_funcs

    elif action == 'tables_list':
        tables_list_action(logged_in, request_items, response)

    elif action == 'columns_list':
        columns_list_action(logged_in, request_items, response)

#   elif action == 'table_info':
#       table_info_action(logged_in, request_items, response)

    elif action == 'table_count':
        table_count_action(logged_in, request_items, response)

    elif action == 'table_view':
        table_view_action(logged_in, request_items, response)

    elif action == 'column_district':
        column_district_action(logged_in, request_items, response)


    else:
        return response_with_message(response, u'Запрос не опознан!', 'exception')

    return response
