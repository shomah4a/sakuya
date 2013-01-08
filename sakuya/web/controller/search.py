#-*- coding: utf-8 -*-

from . import utils

from sakuya.model import session, functions
from sakuya.web.template import zpt


def get(req):
    u'''
    メソッド探して返す
    '''

    fmt = req.GET.get('format')
    rtype = req.GET.get('return')
    args = req.GET.get('args')

    if args is None:
        args = []
    else:
        args = args.strip()

        if not args:
            args = []
        else:
            args = [x.strip() for x in args.split(',')]

    if not rtype:
        result = []
    else:
        with session.Session() as sess:
            result = functions.search_by_type(sess, rtype, args)

    if fmt == 'json':
        return utils.make_json_resp(result)

    return zpt.rendering('search', dict(results=result,
                                        request=req,
                                        return_type=rtype,
                                        args=', '.join(args)))


def make_app():

    return utils.method_map(dict(GET=get))


