#!/usr/bin/env python
# coding=utf-8
# Stan 2012-02-29

from ..request_interface import *


def actions_list_action(request_items, response):
    actions_list = ['actions_list', 'help', 'tables_list', 'columns_list', 'table_info', 'table_count', 'table_view', 'column_district']

    response['content_type'] = 'list'
    response['content'] = actions_list


def action_help(request_items, response):
    action = ri_get_str(request_items, 'help')

    if   action == 'actions_list':
        content = dict(
            description = u'Синтаксис и описание команды',
            parameters = None,
            content_type = 'help'
        )

    elif action == 'help':
        content = dict(
            description = u'Синтаксис и описание команды',
            parameters = ['help'],
            content_type = 'help'
        )

    elif action == 'tables_list':
        content = dict(
            description = u'Список доступных таблиц',
            parameters = None,
            content_type = 'list'
        )

    elif action == 'columns_list':
        content = dict(
            description = u'Список колонок в таблице/таблицах',
            parameters = ['table', 'tables', 'fullnames'],
            content_type = 'list'
        )

    elif action == 'table_info':
        content = dict(
            description = u'Информация о таблице',
            parameters = ['table'],
            content_type = 'info'
        )

    elif action == 'table_count':
        content = dict(
            description = u'Количество рядов в таблице/нескольких таблицах (связанных между собой)',
            parameters = ['table', 'tables', 'filter_json'],
            content_type = 'int'
        )

    elif action == 'table_view':
        content = dict(
            description = u'Вывод таблицы/нескольких таблиц (связанных между собой)',
            parameters = ['table', 'tables', 'offset', 'limit', 'columns', 'columns_except', 'filter_json'],
            content_type = 'table'
        )

    elif action == 'column_district':
        content = dict(
            description = u'Вывод среза значений заданной колонки таблицы',
            parameters = ['table', 'column', 'filter', 'offset', 'limit'],
            content_type = 'elist'
        )

    else:
        response['content_type'] = 'error'
        response['content'] = u'Неизвестная команда!'
        return

    response['content_type'] = 'help'
    response['content'] = content
