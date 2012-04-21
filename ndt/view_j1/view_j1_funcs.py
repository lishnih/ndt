#!/usr/bin/env python
# coding=utf-8
# Stan 2012-02-06

from ..security_db import user_table_iter
from ..request_interface import *
from .query_interface import *


def tables_list_action(userid, request_items, response):
    tables_list = []
    for table in user_table_iter(userid):
        tables_list.append(table)

    response['content_type'] = 'list'
    response['content'] = tables_list


def columns_list_action(userid, request_items, response):
    tables = ri_get_str(request_items, 'table'),    # запятая в конце - это Tuple!
    tables = ri_get_tuple(request_items, 'tables', tables)

    fullnames_option = 1 if len(tables) > 1 else 0
    fullnames_option = ri_get_int(request_items, 'fullnames', fullnames_option)

    columns_list = qi_columns_list(userid, tables, fullnames_option)

    response['content_type'] = 'list'
    response['content'] = columns_list


def table_info_action(userid, request_items, response):
    pass


def table_count_action(userid, request_items, response):
    tables = ri_get_str(request_items, 'table'),    # запятая в конце - это Tuple!
    tables = ri_get_tuple(request_items, 'tables', tables)

    filter_dict = ri_get_obj(request_items, 'filter_json')

    query_params = dict(
        userid  = userid,
        tables  = tables,
        filter  = filter_dict,
    )

    count = qi_query_count(**query_params)

    response['content_type'] = 'int'
    response['content'] = count


def table_view_action(userid, request_items, response):
    tables = ri_get_str(request_items, 'table'),    # запятая в конце - это Tuple!
    tables = ri_get_tuple(request_items, 'tables', tables)

    offset_option = ri_get_int(request_items, 'offset')
    limit_option  = ri_get_int(request_items, 'limit', 50)

    columns_tuple = ri_get_tuple(request_items, 'columns')
    columns_except_tuple = ri_get_tuple(request_items, 'columns_except')

    # Если заданы короткие имена колонок - добавляем к ним название первой таблицы
    table = tables[0]
    if table:
        columns = list(columns_tuple)
        for i in range(len(columns)):
            if '.' not in columns[i]:
                columns[i] = u'{}.{}'.format(table, columns[i])

        columns_except = list(columns_except_tuple)
        for i in range(len(columns_except)):
            if '.' not in columns_except[i]:
                columns_except[i] = u'{}.{}'.format(table, columns_except[i])
    else:
        response['content_type'] = 'error'
        response['content'] = u'Таблица не задана!'
        return

    filter_dict = ri_get_obj(request_items, 'filter_json')

    query_params = dict(
        userid  = userid,
        tables  = tables,
        filter  = filter_dict,
        offset  = offset_option,
        limit   = limit_option,
        columns = columns,
        columns_except = columns_except,
    )

    table_dict = qi_query(**query_params)

    query_params.update(table_dict)

    response['content_type'] = 'table'
    response['content'] = query_params


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

    column_dict = qi_district_query(**query_params)

    query_params.update(column_dict)

    response['content_type'] = 'elist'
    response['content'] = query_params
