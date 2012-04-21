#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-14

from pyramid.paster import setup_logging, get_appsettings
from wsgiref.simple_server import make_server

from ndt import main


if __name__ == '__main__':
    config_uri = '../development.ini'
    settings = get_appsettings(config_uri)

    app = main(global_config=None, **settings)
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
