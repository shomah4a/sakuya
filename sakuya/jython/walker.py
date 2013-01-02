#-*- coding:utf-8 -*-

import sys

from java import lang

from sakuya import constants
from sakuya.jython import utils


def is_special_name(name):

    return name.startswith('__') and name.endswith('__')



def enum_attrs(obj, handlers, context, progress):
    u'''
    属性を列挙する
    '''

    for x in dir(obj):

        if is_special_name(x):
            continue

        try:
            attr = getattr(obj, x)
        except AttributeError, e:
            # インスタンス変数は見えないみたいだし、 AttributeError 来やがるので厄介
            print >> sys.stderr, e.message
            continue
        except TypeError, e:
            # wite only attribute とか TypeError で投げるなよアホか
            print >> sys.stderr, e.message
            continue
        except lang.ExceptionInInitializerError, e:
            print >> sys.stderr, e.message
            continue
        except lang.IllegalAccessException, e:
            continue

        handle_object(attr, handlers, context, progress)



def handle_method(method, handlers, context, progress):
    u'''
    メソッドを何とかする
    '''

    handler = handlers.get(constants.JAVA_METHOD)

    if handler:
        handler(method, context)



def handle_class(cls, handlers, context, progress):
    u'''
    クラスの属性を列挙する
    '''

    handler = handlers.get(constants.JAVA_CLASS)

    if handler:
        handler(cls, context)

    enum_attrs(cls, handlers, context, progress)



def handle_package(package, handlers, context, progress):
    u'''
    パッケージの属性を列挙する
    '''

    handler = handlers.get(constants.JAVA_PACKAGE)

    if handler:
        handler(package, context)

    enum_attrs(package, handlers, context, progress)




def handle_object(obj, handlers, context, progress):
    u'''
    オプジェクトの属性を列挙する感じ
    '''

    if obj in progress:
        return

    progress.add(obj)


    if utils.is_javapackage(obj):
        handle_package(obj, handlers, context, progress)
    elif utils.is_javaclass(obj):
        handle_class(obj, handlers, context, progress)
    elif utils.is_method(obj):
        handle_method(obj, handlers, context, progress)
    else:
        print >> sys.stderr, 'unknown object:', obj




def walk_objects(objects, handlers, context):

    progress = set()

    for obj in objects:
        handle_object(obj, handlers, context, progress)




