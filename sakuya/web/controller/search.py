#-*- coding: utf-8 -*-

from . import utils

from sakuya.model import session, functions
from sakuya.web.template import zpt


def is_empty(obj):

    return obj is None or not obj.strip()


def get(req):
    u'''
    メソッド探して返す
    '''

    fmt = req.GET.get('format')
    rtype = req.GET.get('return')
    args = req.GET.get('args')

    if is_empty(args):
        args = []
    else:
        args = args.strip()

        if not args:
            args = []
        else:
            args = [x.strip() for x in args.split(',')]


    if rtype is not None:
        rtype = rtype.strip()

    if is_empty(rtype) and not args:
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


