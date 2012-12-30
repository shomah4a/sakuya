#-*- coding:utf-8 -*-

import simplejson

from sakuya.jython import utils, constants, walker


def print_json(obj):

    print simplejson.dumps(obj)



def dump_package(pkg, context):
    u'''
    パッケージ情報を出力
    '''
    print_json(dict(type=constants.JAVA_PACKAGE,
                    name=pkg.__name__))




def get_bases(cls, context):
    u'''
    継承元を出力
    '''

    return [x.__name__ for x in cls.__bases__]




def dump_typename(typ):
    u'''
    型を出力
    '''

    mod = typ.__module__
    name = typ.__name__

    if mod == '__builtin__':
        return name

    return '.'.join([mod, name])



def dump_class(cls, context):
    u'''
    クラス情報を出力
    '''

    print_json(dict(type=constants.JAVA_CLASS,
                    name=dump_typename(cls),
                    bases=get_bases(cls, context)))



def dump_method(method, context):
    u'''
    メソッドを出力
    '''

    funcdata = method.argslist[0].data

    rtype = dump_typename(funcdata.returnType)

    name = '.'.join([dump_typename(funcdata.getDeclaringClass()), funcdata.name])

    parameters = [dump_typename(x) for x in funcdata.parameterTypes]

    print_json({'type': constants.JAVA_METHOD,
                'name': funcdata.name,
                'fully_qualified': name,
                'class': dump_typename(funcdata.getDeclaringClass()),
                'parameters': parameters})



def dump_objects(names):

    packages = map(utils.import_package, names)

    handlers = {constants.JAVA_PACKAGE: dump_package,
                constants.JAVA_CLASS: dump_class,
                constants.JAVA_METHOD: dump_method}
    context = {}

    walker.walk_objects(packages, handlers, context)

