#-*- coding:utf-8 -*-

import java
from java import lang


javapackage = type(java)
reflectedfunction = type(lang.Object.toString)


def import_package(name):

    pkg = __import__(name)

    return reduce(lambda m, n: getattr(m, n), name.split('.')[1:], pkg)



def is_javaclass(obj):

    return isinstance(obj, type) and issubclass(obj, lang.Object)



def is_javapackage(obj):

    return isinstance(obj, javapackage)



def is_method(obj):

    return isinstance(obj, reflectedfunction)
