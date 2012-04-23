#!/usr/bin/env python
# coding=utf-8
# Stan 2012-02-06

from request_interface import *


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
