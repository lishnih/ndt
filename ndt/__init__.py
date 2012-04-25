#!/usr/bin/env python
# coding=utf-8
# Stan 2012-01-26

from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .security import groupfinder, RootFactory
# from .models import users_init


def main(global_config, **settings):
    """ Функция возвращает Pyramid WSGI приложение """

    # Инициализация БД
#   users_init(settings)

    config = Configurator(settings=settings, root_factory=RootFactory)

    # Авторизация/аутентификация
    authn_policy = AuthTktAuthenticationPolicy('sosecret', callback=groupfinder)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.add_route('login',  '/login')
    config.add_route('logout', '/logout')
 
    # Прописываем пути
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('root', '/')
#   config.add_route('tables', '/view/*subpath')

    # json
#   config.add_route('j1', '/j1')
    config.add_route('j2', '/j2')

    # Тестирование
    config.add_route('hello', '/hello/{name}')
    config.add_route('test',  '/test/*subpath')

    config.add_route('currentuser', '/user')
    config.add_route('user',        '/user/{name}')

    config.scan()

    # wiki

    from sqlalchemy import engine_from_config
    from .wiki.models import DBSession

    engine = engine_from_config(settings, 'db_wiki.')
    DBSession.configure(bind=engine)

    config.add_static_view('/wiki/static', 'ndt.wiki:static', cache_max_age=3600)
    config.add_route('view_wiki', '/wiki/')
    config.add_route('view_page', '/wiki/{pagename}')
    config.add_route('add_page',  '/wiki/add_page/{pagename}')
    config.add_route('edit_page', '/wiki/{pagename}/edit_page')

    config.scan('ndt.wiki', 'wiki')
    return config.make_wsgi_app()
