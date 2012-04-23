#!/usr/bin/env python
# coding=utf-8
# Stan 2012-02-25

from sqlalchemy import distinct, desc, or_

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


def qi_query_count(userid, tables, search=None, filter={}):
    if isinstance(tables, basestring):
        tables = tables,

    UserSession = get_user_session(userid)

    classes = []
    for table in tables:
        classes.append(get_user_table_data(userid, table))

    if None in classes:
        return {}, u'Некоторые таблицы недоступны: {!r}'.format(tables)

    query = UserSession.query(*classes)

    full_rows_count = query.count()

    columns_dict = qi_columns_dict(userid, tables)

    if search:
        search_str = u'%{}%'.format(search)
        or_query = or_(*[columns_dict[key].like(search_str) for key in columns_dict])
        query = query.filter(or_query)

    for key, value in filter.items():
        if key in columns_dict:
            if isinstance(value, basestring):
                query = query.filter(columns_dict[key] == value)
            else:
                condition, value = value
                if condition == '=' or condition == '==':
                    query = query.filter(columns_dict[key] == value)
                elif condition == '!=':
                    query = query.filter(columns_dict[key] != value)
                elif condition == '~':
                    query = query.filter(columns_dict[key].like(value))
                elif condition == 'like':
                    query = query.filter(columns_dict[key].like(u'%{}%'.format(value)))
                elif condition == '>':
                    query = query.filter(columns_dict[key] > value)
                elif condition == '>=':
                    query = query.filter(columns_dict[key] >= value)
                elif condition == '<':
                    query = query.filter(columns_dict[key] < value)
                elif condition == '<=':
                    query = query.filter(columns_dict[key] <= value)

    filtered_rows_count = query.count()

    return dict(
        full_rows_count     = full_rows_count,
        filtered_rows_count = filtered_rows_count,
#       rows_count          = rows_count,
        query = unicode(query)
    ), None


def qi_query(userid, tables, search=None, filter={}, sorting=[], offset=None, limit=None, columns=None):
    if isinstance(tables, basestring):
        tables = tables,

    UserSession = get_user_session(userid)

    classes = []
    for table in tables:
        classes.append(get_user_table_data(userid, table))

    if None in classes:
        return {}, [], u'Некоторые таблицы недоступны: {!r}'.format(tables)

    query = UserSession.query(*classes)

    additional_tables = tables[1:]
    if additional_tables:
        for table in additional_tables:
            query = query.join(get_user_table_data(userid, table))

    full_rows_count = query.count()

    columns_dict = qi_columns_dict(userid, tables)

    for column in sorting:
        if isinstance(column, basestring):
            query = query.order_by(columns_dict[column])
        else:
            column, directional = column
            if directional == 'desc':
                query = query.order_by(desc(columns_dict[column]))
            else:
                query = query.order_by(columns_dict[column])

    if search:
        search_str = u'%{}%'.format(search)
        or_query = or_(*[columns_dict[key].like(search_str) for key in columns_dict])
        query = query.filter(or_query)

    for key, value in filter.items():
        if key in columns_dict:
            if isinstance(value, basestring):
                query = query.filter(columns_dict[key] == value)
            else:
                condition, value = value
                if condition == '=' or condition == '==':
                    query = query.filter(columns_dict[key] == value)
                elif condition == '!=':
                    query = query.filter(columns_dict[key] != value)
                elif condition == '~':
                    query = query.filter(columns_dict[key].like(value))
                elif condition == 'like':
                    query = query.filter(columns_dict[key].like(u'%{}%'.format(value)))
                elif condition == '>':
                    query = query.filter(columns_dict[key] > value)
                elif condition == '>=':
                    query = query.filter(columns_dict[key] >= value)
                elif condition == '<':
                    query = query.filter(columns_dict[key] < value)
                elif condition == '<=':
                    query = query.filter(columns_dict[key] <= value)

    filtered_rows_count = query.count()

    rows = query.slice(offset, offset + limit) if limit else \
           query.offset(offset)
    rows_count = rows.count()

    th_list = []
    for column_description in query.column_descriptions:
#       th_list.append(column_description['name'])
        th_list.append(unicode(column_description['expr']).replace('.', '<br />'))

    td_list = [[i for i in row] for row in rows]
#     for row in rows:
#         tr = []
#         for label in row._labels:
#             tr.append(row.__getattribute__(label))
#         td_list.append(tr)

    return dict(
        full_rows_count     = full_rows_count,
        filtered_rows_count = filtered_rows_count,
        rows_count          = rows_count,
        columns = th_list,
        query   = unicode(query)
    ), td_list, None


def qi_district_query(userid, table, column, filter={}, sorting=[], offset=None, limit=None):
    UserSession = get_user_session(userid)

    columns_dict = qi_columns_dict(userid, table)

    if column not in columns_dict:
        return {}, [], u'Колонка недоступна: {!r}'.format(column)

    query = UserSession.query(distinct(columns_dict[column]))

    full_rows_count = query.count()

    for key, value in filter.items():
        if key in columns_dict:
            if isinstance(value, basestring):
                query = query.filter(columns_dict[key] == value)
            else:
                condition, value = value
                if condition == '=' or condition == '==':
                    query = query.filter(columns_dict[key] == value)
                elif condition == '!=':
                    query = query.filter(columns_dict[key] != value)
                elif condition == '~':
                    query = query.filter(columns_dict[key].like(value))
                elif condition == 'like':
                    query = query.filter(columns_dict[key].like(u'%{}%'.format(value)))
                elif condition == '>':
                    query = query.filter(columns_dict[key] > value)
                elif condition == '>=':
                    query = query.filter(columns_dict[key] >= value)
                elif condition == '<':
                    query = query.filter(columns_dict[key] < value)
                elif condition == '<=':
                    query = query.filter(columns_dict[key] <= value)

    filtered_rows_count = query.count()

    rows = query.slice(offset, offset + limit) if limit else \
           query.offset(offset)
    rows_count = rows.count()

    column_list = []
    for row in rows:
        column_list.append(row.__dict__[None])

    return dict(
        full_rows_count     = full_rows_count,
        filtered_rows_count = filtered_rows_count,
        rows_count          = rows_count,
        query      = unicode(query)
    ), column_list, None
