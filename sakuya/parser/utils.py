#-*- coding:utf-8 -*-

from pygments import token


def find_next(listlike, start, typ, val=None):
    u'''
    次に現れるトークンの位置を取得する
    '''

    for idx, tok in enumerate(listlike, start):

        if typ == tok.type and (val is None or val == tok.text):
            return idx

    return None



