#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-13

from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy import create_engine, MetaData, ForeignKey

from .security import USERS, GROUPS


# GROUPS_DB_URLS = {
#     'phase1': {
#                 'avk':          'sqlite:///D:/opt/home/a94001-2/data/avk.sqlite',
#                 'welding':      'sqlite:///D:/opt/home/a94001/data/welding.sqlite',
#                 'ndt':          'mysql+oursql://root:54321@localhost/ndt_a94001',
#               },
# 
#     'phase2': {
#                 'avk':          'sqlite:///D:/opt/home/a94001-2/data/avk.sqlite',
#                 'certificates': 'sqlite:///D:/opt/home/a94001-2/data/certificates.sqlite',
#                 'schemes':      'sqlite:///D:/opt/home/a94001-2/data/schemes.sqlite',
#                 'welding':      'sqlite:///D:/opt/home/a94001-2/data/welding.sqlite',
#                 'ndt':          'mysql+oursql://root:54321@localhost/ndt_a94001-2',
#               },
# }


USERS_DB_URLS = {
    'admin':    {
                  'users': 'sqlite:///%(here)s/../users.sqlite',
                  'wiki':  'sqlite:///%(here)s/../wiki.sqlite',
                },
    'welding1': {
                  'welding': 'sqlite:///D:/opt/home/a94001/data/welding.sqlite',
#                 'ndt':     'mysql+oursql://root:54321@localhost/ndt_a94001',
                },
    'qc2':      {
                  'avk':      'sqlite:///D:/opt/home/a94001-2/data/avk.sqlite',
                  'request':  'sqlite:///D:/opt/home/a94001-2/data/request.sqlite',
                  'delivery': 'sqlite:///D:/opt/home/a94001-2/data/delivery.sqlite',
                },
    'welding2': {
                  'schemes': 'sqlite:///D:/opt/home/a94001-2/data/schemes.sqlite',
                  'welding': 'sqlite:///D:/opt/home/a94001-2/data/welding.sqlite',
#                 'ndt':     'mysql+oursql://root:54321@localhost/ndt_a94001-2',
                },
    'ndt1':     {
                  'ndt':     'mysql+oursql://root:54321@localhost/ndt_a94001',
                },
    'ndt2':     {
                  'ndt':     'mysql+oursql://root:54321@localhost/ndt_a94001-2',
                },
}

USERS_SESSIONS = {}
USERS_TABLES   = {}


def user_db_url_iter(userid):
    if userid in USERS:
        url = USERS_DB_URLS.get(userid)
        if isinstance(url, basestring):
            yield url, None
            return
        elif isinstance(url, dict):
            for tag, url in url.items():
                yield url, tag


def get_user_session(userid):
    if userid in USERS:
        if userid in USERS_SESSIONS:
            return USERS_SESSIONS.get(userid)
        else:

#             try:
                tables = {}
                for db_url, db_tag in user_db_url_iter(userid):
                    if db_url:
                        engine = create_engine(db_url)
                        metadata = MetaData(engine, reflect=True)

                        for table in metadata.tables:
                            tdata = metadata.tables.get(table)
                            if db_tag:
                                table = '{}.{}'.format(db_tag, table)
                            tables[table] = tdata

                            # Устанавливаем связи между таблицами
#                             for label in tdata.columns._data:
#                                 rel_table = None
#                                 if label[0] == '_':
#                                     rel_table, rel_key = label[1:].split('_', 1)
#                                 if rel_table in metadata.tables:
#                                     rel_tdata = metadata.tables[rel_table]
#                                     if rel_key in rel_tdata.c:
#                                         tdata.c[label].append_foreign_key( ForeignKey(rel_tdata.c[rel_key]) )
                    
                    #     tabledata_dirs.c['_tasks_id'].append_foreign_key( ForeignKey(tabledata_tasks.c['id']) )
                    #     tabledata_files.c['_dirs_id'].append_foreign_key( ForeignKey(tabledata_dirs.c['id']) )

                USERS_TABLES[userid] = tables

                UserSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
                USERS_SESSIONS[userid] = UserSession

                return UserSession
#             except Exception, e:
#                 pass          # !!!


def user_table_iter(userid):
    if userid in USERS:
        tables_dict = USERS_TABLES.get(userid, {})
        for table in tables_dict.keys():
            yield table


def get_user_table_data(userid, table):
    if userid in USERS:
        tables_dict = USERS_TABLES.get(userid, {})
        return tables_dict.get(table)
