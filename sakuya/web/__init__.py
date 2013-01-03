#-*- coding:utf-8 -*-


def hello(environ, start_response):

    start_response('200 OK', [('Content-Type', 'text/plain')])

    return ['Hello']



def app_factory(*argl, **argd):

    return hello
