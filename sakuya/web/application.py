#-*- coding: utf-8 -*-

from webob import dec

from .controller import search



def hello(req):

    return u'hello'



def make_application():

    return dec.wsgify(search.make_app())
