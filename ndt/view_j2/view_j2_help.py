#!/usr/bin/env python
# coding=utf-8
# Stan 2012-02-29

from ..request_interface import *
from .view_j2_funcs import *


def actions_list_action(request_items, response):
    response['rows'] = [
        'actions_list',
        'action_params_list',
        'tables_list',
        'columns_list',
#       'table_info',
        'table_count',
        'table_view',
        'column_district',
    ]


def action_params_list_action(request_items, response):
    req_action = ri_get_str(request_items, 'req_action')

    if not req_action:
        return response_with_message(response, u'Команда не задана!', 'error')

    elif req_action == 'actions_list':
        response['description'] = u'Перечень команд'
        response['rows'] = []

    elif req_action == 'action_params_list':
        response['description'] = u'Перечень параметров команды'
        response['rows'] = ['req_action']

    elif req_action == 'tables_list':
        response['description'] = u'Список доступных таблиц'
        response['rows'] = []

    elif req_action == 'columns_list':
        response['description'] = u'Список колонок в таблице/таблицах'
        response['rows'] = ['table', 'tables', 'fullnames']

#   elif req_action == 'table_info':
#       response['description'] = u'Информация о таблице'
#       response['rows'] = ['table']

    elif req_action == 'table_count':
        response['description'] = u'Количество рядов в таблице/нескольких таблицах (связанных между собой)'
        response['rows'] = ['table', 'tables', 'search', 'filter_json']

    elif req_action == 'table_view':
        response['description'] = u'Вывод таблицы/нескольких таблиц (связанных между собой)'
        response['rows'] = ['table', 'tables', 'offset', 'limit', 'columns', 'columns_except', 'search', 'filter_json']

    elif req_action == 'column_district':
        response['description'] = u'Вывод среза значений заданной колонки таблицы'
        response['rows'] = ['table', 'column', 'filter', 'offset', 'limit']

    else:
        return response_with_message(response, u'Неизвестная команда!', 'error')
