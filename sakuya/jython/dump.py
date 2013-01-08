#-*- coding:utf-8 -*-

import sys

from java import lang

import simplejson

from sakuya import constants
from sakuya.jython import utils, walker



def print_json(obj):

    print simplejson.dumps(obj)



def make_package_data(pkg, context):
    u'''
    パッケージ情報を生成
    '''

    return dict(type=constants.JAVA_PACKAGE,
                name=pkg.__name__)



def dump_package(pkg, context):
    u'''
    パッケージ情報を出力
    '''
    print_json(make_package_data(pkg, context))



def get_bases(cls, context):
    u'''
    継承元を出力
    '''

    return [x.__name__ for x in cls.__bases__]



def dump_typename(typ):
    u'''
    型を出力
    '''

    if typ != lang.Class and typ.isArray():
        com = typ.getComponentType()
        mod = com.__module__
        name = typ.getSimpleName()
    else:
        mod = typ.__module__
        name = typ.__name__


    if mod == '__builtin__':
        return name

    return '.'.join([mod, name])




def make_class_data(cls, context):
    u'''
    クラス情報を生成
    '''

    r = dict(type=constants.JAVA_CLASS,
             name=dump_typename(cls),
             bases=get_bases(cls, context))

    try:
        r['modifiers'] = cls.getModifiers()
    except TypeError, e:
        r['modifiers'] = 0

    return r



def dump_class(cls, context):
    u'''
    クラス情報を出力
    '''

    print_json(make_class_data(cls, context))




def make_method_data(method, context):
    u'''
    メソッド情報を生成
    '''


    funcdata = method.argslist[0].data

    rtype = dump_typename(funcdata.returnType)

    name = '.'.join([dump_typename(funcdata.getDeclaringClass()), funcdata.name])

    parameters = [dump_typename(x) for x in funcdata.parameterTypes]

    return {'type': constants.JAVA_METHOD,
            'name': funcdata.name,
            'fully_qualified': name,
            'class': dump_typename(funcdata.getDeclaringClass()),
            'parameters': parameters,
            'rtype': rtype,
            'modifiers': funcdata.getModifiers()}



def dump_method(method, context):
    u'''
    メソッドを出力
    '''

    print_json(make_method_data(method, context))



def dump_objects(names):

    packages = map(utils.import_package, names)

    handlers = {constants.JAVA_PACKAGE: dump_package,
                constants.JAVA_CLASS: dump_class,
                constants.JAVA_METHOD: dump_method}
    context = {}

    walker.walk_objects(packages, handlers, context)


