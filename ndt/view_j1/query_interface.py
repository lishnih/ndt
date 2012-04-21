#!/usr/bin/env python
# coding=utf-8
# Stan 2012-02-25

from sqlalchemy import distinct

from ..security_db import get_user_session, user_table_iter, get_user_table_data


def qi_columns_list(userid, tables, fullnames_option = 0):
    if isinstance(tables, basestring):
        tables = tables,

    columns_list = []

    for table in tables:
        tdata = get_user_table_data(userid, table)
        if tdata != None:       # !!! недоделка?
            for label in tdata.columns:
                l = unicode(label) if fullnames_option else label.name
                columns_list.append(l)

    return columns_list


def qi_columns_dict(userid, tables):
    if isinstance(tables, basestring):
        tables = tables,

    columns_dict = dict()

    # Для первой таблицы предусматриваем короткие названия колонок
#     table = tables[0]
#     columns_list = qi_columns_list(userid, table)
#     if columns_list:
#         tdata = get_user_table_data(userid, table)
#         for column in columns_list:
#             columns_dict[column] = tdata.c[column]

    for table in tables:
    
        # В этом странном коде мы убираем db_tag из имени колонки
        if '.' in table:
            table_list = table.split('.')
            table_brief = table_list[1]
        else:
            table_brief = table
    
        columns_list = qi_columns_list(userid, table)
        if columns_list:
            tdata = get_user_table_data(userid, table)
            for column in columns_list:
                full_column = u'{}.{}'.format(table_brief, column)
                columns_dict[full_column] = tdata.c[column]

    return columns_dict


def qi_query_count(userid, tables, filter=None):
    if isinstance(tables, basestring):
        tables = tables,

    UserSession = get_user_session(userid)

    query = UserSession.query()

    columns = qi_columns_list(userid, tables, 1)

    columns_dict = qi_columns_dict(userid, tables)
    for column in columns:
        if column in columns_dict:
            query = query.add_columns(columns_dict[column])

    # !!! если задать несуществующие колонки, то query не сформируется - будет ошибка
    # !!! то же самое и с несущесьвующей таблицей

    additional_tables = tables[1:]
    if additional_tables:
        for table in additional_tables:
            query = query.join(get_user_table_data(userid, table))

    tables_count = query.count()

    if filter:
#       query.filter_by(**filter)
        for key, value in filter.items():
            if key in columns_dict:
                if isinstance(value, list):
                    condition, value = value
                    if condition == '=' or condition == '==':
                        query = query.filter(columns_dict[key] == value)
                    elif condition == '!=':
                        query = query.filter(columns_dict[key] != value)
                    elif condition == '>':
                        query = query.filter(columns_dict[key] > value)
                    elif condition == '>=':
                        query = query.filter(columns_dict[key] >= value)
                    elif condition == '<':
                        query = query.filter(columns_dict[key] < value)
                    elif condition == '<=':
                        query = query.filter(columns_dict[key] <= value)
                    elif condition == 'like':
                        query = query.filter(columns_dict[key].like(u'%{}%'.format(value)))
                else:
                    query = query.filter(columns_dict[key] == value)

    filter_count = query.count()

    return filter_count


def qi_query(userid, tables, filter=None, offset=None, limit=None, columns=None, columns_except=None):
    if isinstance(tables, basestring):
        tables = tables,

    UserSession = get_user_session(userid)

    query = UserSession.query()

    if not columns:
        columns = qi_columns_list(userid, tables, 1)
        if columns_except:
            for column in columns_except:
                columns.remove(column)

    columns_dict = qi_columns_dict(userid, tables)
    for column in columns:
        if column in columns_dict:
            query = query.add_columns(columns_dict[column])

    # !!! если задать несуществующие колонки, то query не сформируется - будет ошибка
    # !!! то же самое и с несущесьвующей таблицей

    additional_tables = tables[1:]
    if additional_tables:
        for table in additional_tables:
            query = query.join(get_user_table_data(userid, table))

    tables_count = query.count()

    if filter:
#       query.filter_by(**filter)
        for key, value in filter.items():
            if key in columns_dict:
                if isinstance(value, list):
                    condition, value = value
                    if condition == '=' or condition == '==':
                        query = query.filter(columns_dict[key] == value)
                    elif condition == '!=':
                        query = query.filter(columns_dict[key] != value)
                    elif condition == '>':
                        query = query.filter(columns_dict[key] > value)
                    elif condition == '>=':
                        query = query.filter(columns_dict[key] >= value)
                    elif condition == '<':
                        query = query.filter(columns_dict[key] < value)
                    elif condition == '<=':
                        query = query.filter(columns_dict[key] <= value)
                    elif condition == 'like':
                        query = query.filter(columns_dict[key].like(u'%{}%'.format(value)))
                else:
                    query = query.filter(columns_dict[key] == value)

    filter_count = query.count()

    rows = query.slice(offset, offset + limit) if limit else query.offset(offset)
    rows_count = rows.count()

    th_list = []
    for column_description in query.column_descriptions:
#       th_list.append(column_description['name'])
        th_list.append(unicode(column_description['expr']).replace('.', '<br />'))

    td_list = []
    for row in rows:
        tr = []
        for label in row._labels:
            tr.append(row.__getattribute__(label))
        td_list.append(tr)

    return dict(
        tables_count = tables_count,
        filter_count = filter_count,
        rows_count   = rows_count,
        thead = th_list,
        tbody = td_list,
        query = unicode(query)
    )


def qi_district_query(userid, table, column, filter=None, offset=None, limit=None):
    UserSession = get_user_session(userid)

    columns_dict = qi_columns_dict(userid, table)

    query = UserSession.query(distinct(columns_dict[column]))

    tables_count = query.count()

    if filter:
        for key, value in filter.items():
            if key in columns_dict:
                if isinstance(value, list):
                    condition, value = value
                    if condition == '=' or condition == '==':
                        query = query.filter(columns_dict[key] == value)
                    elif condition == '!=':
                        query = query.filter(columns_dict[key] != value)
                    elif condition == '>':
                        query = query.filter(columns_dict[key] > value)
                    elif condition == '>=':
                        query = query.filter(columns_dict[key] >= value)
                    elif condition == '<':
                        query = query.filter(columns_dict[key] < value)
                    elif condition == '<=':
                        query = query.filter(columns_dict[key] <= value)
                    elif condition == 'like':
                        query = query.filter(columns_dict[key].like(u'%{}%'.format(value)))
                else:
                    query = query.filter(columns_dict[key] == value)

    filter_count = query.count()

    rows = query.slice(offset, offset + limit) if limit else query.offset(offset)
    rows_count = rows.count()

    column_list = []
    for row in rows:
        column_list.append(row.__dict__[None])

    return dict(
        tables_count = tables_count,
        filter_count = filter_count,
        rows_count   = rows_count,
        rows = column_list,
        query = unicode(query)
    )
