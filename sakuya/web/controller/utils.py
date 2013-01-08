#-*- coding: utf-8 -*-

import urllib
import json

import webob

from . import errors


def make_json_resp(data):
    u'''
    json のレスポンスを作る
    '''

    resp = webob.Response()
    resp.headerlist = [('Content-Type', 'application/json; charset=UTF-8')]

    resp.body = json.dumps(data)

    return resp



def redirect_to(url, params):
    u'''
    redirect する
    '''

    resp = webob.Response()

    resp.status = '303 See Other'
    resp.headerlist = [('Location', url + '?' + urllib.urlencode(params, True))]

    return resp



def method_map(d):

    def app(req):

        m = req.method

        if m in d:
            return d[m](req)

        return errors.method_not_allowed(req)


    return app
