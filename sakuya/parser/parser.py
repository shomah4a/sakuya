#-*- coding:utf-8 --*-


from pygments import lexers, token

from .parsers import java



def parse(filepath):

    return java.parse(filepath)


