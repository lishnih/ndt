#!/usr/bin/env python
# coding=utf-8
# Stan 2012-02-06

from ..security_db import user_table_iter
from ..request_interface import *
from .query_interface import *


def prepare_response(request):
    response = dict(
        version = 2,
        request_get  = repr(request.GET),
        request_post = repr(request.POST),
    )

    response['rows']   = []
    response['aaData'] = []

    return response


def get_action(request, response):
    request_items = None
    action = None

    if   'action' in request.POST:
        request_items = request.POST
    elif 'action' in request.GET:
        request_items = request.GET

    if request_items:
        response['action'] = ri_get_str(request_items, 'action')
        action = response['action']

        if 'sEcho' in request_items:
            response['sEcho'] = ri_get_int(request_items, 'sEcho', 1)

    return action, request_items


def response_with_message(response, msg, msg_type='info'):
    if not response['rows']:
        response['rows'].append(msg)
    if not response['aaData']:
        response['iTotalRecords']        = 1
        response['iTotalDisplayRecords'] = 1
        response['aaData'] = [['' for i in range(20)]]
        response['aaData'][0][0] = msg
    if msg_type:
        response[msg_type] = msg

    return response


# !!! Если базы не загружены возращает пустой результат
def tables_list_action(userid, request_items, response):
    tables_list = []
    for table in user_table_iter(userid):
        tables_list.append(table)

    response['rows'] = tables_list


def columns_list_action(userid, request_items, response):
    tables = ri_get_str(request_items, 'table'),    # запятая в конце - это Tuple!
    tables = ri_get_tuple(request_items, 'tables', tables)

    if not tables[0]:
        return response_with_message(response, u'Таблица не задана!', 'error')

    fullnames_option = ri_get_int(request_items, 'fullnames')
    if len(tables) > 1:
        fullnames_option = 1

    columns_list = qi_columns_list(userid, tables, fullnames_option)

    response['rows'] = columns_list


# def table_info_action(userid, request_items, response):
#   pass


def table_count_action(userid, request_items, response):
    tables = ri_get_str(request_items, 'table'),    # запятая в конце - это Tuple!
    tables = ri_get_tuple(request_items, 'tables', tables)

    if not tables[0]:
        return response_with_message(response, u'Таблица не задана!', 'error')

    search = ri_get_str(request_items, 'search')    # Строка для поиска
    filter_dict = ri_get_obj(request_items, 'filter_json')

    query_params = dict(
        userid = userid,
        tables = tables,
        search = search,
        filter = filter_dict,
    )

    full_rows_count, filtered_rows_count, query_str = qi_query_count(**query_params)

    response['full_rows_count']     = full_rows_count
    response['filtered_rows_count'] = filtered_rows_count
    response['count']        = filtered_rows_count
    response['query_str']    = query_str
    response['query_params'] = query_params


def table_view_action(userid, request_items, response):
    tables = ri_get_str(request_items, 'table'),    # запятая в конце - это Tuple!
    tables = ri_get_tuple(request_items, 'tables', tables)

    if not tables[0]:
        return response_with_message(response, u'Таблица не задана!', 'error')

    import logging; logging.warning(request_items)

    offset = ri_get_int(request_items, 'offset')      # Требуемый первый ряд
    limit  = ri_get_int(request_items, 'limit', 200)  # Требуемое кол-во рядов
    search = ri_get_str(request_items, 'sSearch')     # Строка для поиска

    #
    columns_tuple = ri_get_tuple(request_items, 'columns')
#   columns_except_tuple = ri_get_tuple(request_items, 'columns_except')

    # Если заданы короткие имена колонок - добавляем к ним название первой таблицы
    table = tables[0]
    columns = list(columns_tuple)
    for i in range(len(columns)):
        if '.' not in columns[i]:
            columns[i] = u'{}.{}'.format(table, columns[i])

#   columns_except = list(columns_except_tuple)
#   for i in range(len(columns_except)):
#       if '.' not in columns_except[i]:
#           columns_except[i] = u'{}.{}'.format(table, columns_except[i])

    filter_dict  = ri_get_obj(request_items, 'filter_json')
    sorting_dict = ri_get_obj(request_items, 'sorting_json')

    query_params = dict(
        userid  = userid,
        tables  = tables,
        search  = search,
        filter  = filter_dict,
        sorting = sorting_dict,
        offset  = offset,
        limit   = limit,
        columns = columns,
#       columns_except = columns_except,
    )

    table_info, rows = qi_query(**query_params)

    response.update(table_info)
    response['query_params'] = query_params

    if 'sEcho' in response:
        response['iTotalRecords']        = table_info['full_rows_count']
        response['iTotalDisplayRecords'] = table_info['filtered_rows_count']
        response['aaData'] = rows
    else:
        response['rows'] = rows


def column_district_action(userid, request_items, response):
    table = ri_get_str(request_items, 'table')
    column = ri_get_str(request_items, 'column')

    offset_option = ri_get_int(request_items, 'offset')
    limit_option  = ri_get_int(request_items, 'limit', 200)

    filter_dict = ri_get_obj(request_items, 'filter_json')

    query_params = dict(
        userid = userid,
        table  = table,
        column = column,
        filter = filter_dict,
        offset = offset_option,
        limit  = limit_option,
    )

    column_info, rows = qi_district_query(**query_params)

    response.update(column_info)
    response['query_params'] = query_params

    if 'sEcho' in response:
        response['iTotalRecords']        = column_info['full_rows_count']
        response['iTotalDisplayRecords'] = column_info['filtered_rows_count']
        response['aaData'] = [[i] for i in rows]
    else:
        response['rows'] = rows
