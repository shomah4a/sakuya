#-*- coding: utf-8 -*-

import webob

from sakuya.web.template import zpt




def error_maker(status, message):


    def handler(req):

        res = webob.Response()

        res.status = status

        res.text =  zpt.rendering('error', dict(request=req,
                                                title=status,
                                                message=message))

        res.headerlist = [('Content-Type', 'text/html; charset=UTF-8')]

        return res


    return handler



not_found = error_maker('404 NotFound', 'Content Not Found')

method_not_allowed = error_maker('405 MethodNotAllowed', 'Method {request.method} Not Allowed')

