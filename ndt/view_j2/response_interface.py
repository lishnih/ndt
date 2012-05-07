#!/usr/bin/env python
# coding=utf-8
# Stan 2012-02-06


def prepare_response(request):
    response = dict(
        version = 2,
        request_get  = repr(request.GET),
        request_post = repr(request.POST),
    )

    response['rows']   = []
    response['aaData'] = []

    return response


def response_with_message(response, msg, msg_type='info'):
    if not response['rows']:
        response['rows'].append(msg)
    if not response['aaData']:
        response['iTotalRecords']        = 1
        response['iTotalDisplayRecords'] = 1
        response['aaData'] = [['' for i in range(10)]]
        response['aaData'][0][0] = msg
    if msg_type:
        response[msg_type] = msg

    return response
